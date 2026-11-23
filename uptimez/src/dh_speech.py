"""Speech bubbles for Daddy's Home, by the rule in PR #62 (lessons: tails to the mouth).

install() is opt-in. Once called, every A.bubble(...) in scenes 1-8 draws through speech():
- the speaker is found, not guessed: every character rig drawn in the drawing is logged (its call and the cairo matrix at
  the time), and the speaker is the rig whose head is nearest the point the scene aimed at;
- the speaker is redrawn alone on a blank sheet, so its outline, skin and mouth are read from pixels of this very drawing
  (pose, lean and size included);
- face: the tail ends on the cheek at mouth height on the box's side, at most 0.4 face radius from the mouth, and comes
  round the outside of the whole head (hair, earrings and glasses chain included), entering only through skin;
- robot: the tail comes down onto the antenna ball and touches it;
- CARD lines (the speaker is off the frame): a quoted card with the name, no tail;
- the box sits in the top band beside the head on the tail's side, off the speaker, and stays put for the whole line
  while the head stays within 0.6 radius of where it was when the line began.
LAST holds what was drawn (for dh_tailcheck)."""
import math
import cairo
import numpy as np
import kit
from kit import Ctx

INK = (0.13, 0.11, 0.12)
REG = []                          # rigs drawn in the current drawing
KEEP = []                         # things a bubble must stay off (the price tag), logged like the rigs
_DEPTH = [0]
LAST = []                         # bubbles drawn in the current drawing
HELD = {}                         # text -> (bx, y, side, head x, head y, r): the box held for the line
ON = [False]
CARD = {"Then stand like one, Donnie.": "MOM", "I prefer green in cash.": "FATHER",
        "I didn't steal anything!": "DON"}   # the jump: his hands fill the space a tail would need (22 Nov tail check)
PLANT = [None]                    # dh_tailcheck's self-test: a function that draws a planted faulty bubble instead
SKIP = [None]                     # dh_tailcheck: the index (in REG order) of a rig to leave out of the picture
FORCE = [None]                    # dh_tailcheck: (index, mouth) to force a rig's mouth open or shut


def _wrap(mod, name, kind, mouth_kw):
    f = getattr(mod, name)
    if getattr(f, "_speech", False):
        return

    def g(k, *a, **kw):
        real = k.c.get_target().get_width() >= 270            # dl.draw also calls the scene on small scratch sheets
        idx = len(REG) if (_DEPTH[0] == 0 and real) else -1
        key = (id(f), tuple(k.c.get_matrix()), repr(a)) if idx >= 0 else None
        kk = k
        if idx >= 0 and SKIP[0] is not None and (SKIP[0] == key or (isinstance(SKIP[0], set) and key in SKIP[0])):                    # drawn on a scratch sheet: the scene still gets its points
            sc = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 8, 8)); sc.set_matrix(k.c.get_matrix())
            kk = Ctx(sc, 0)
        if idx >= 0 and FORCE[0] is not None and FORCE[0][0] == key and mouth_kw:
            kw = dict(kw); kw["mouth"] = FORCE[0][1]
        _DEPTH[0] += 1
        try:
            o = f(kk, *a, **kw)
        finally:
            _DEPTH[0] -= 1
        if idx >= 0 and isinstance(o, dict) and "head" in o:
            c = k.c
            REG.append(dict(f=f, k=k, a=a, kw=dict(kw), m=k.c.get_matrix(), idx=key, hi=c.get_target().get_width() / 540.0,
                            head_u=o["head"], kind=kind, mouth_kw=mouth_kw, name=name, mod=mod.__name__))
            rec_ = REG[-1]                                    # redrawn alone now, while the scene's state is as it drew it
            rec_["iso"] = alone(rec_)
            if mouth_kw:
                import dh_anim as DA
                rec_["iso_open"] = alone(rec_, mouth=DA.M_BIG)
                rec_["iso_shut"] = alone(rec_, mouth=None)
        return o
    g._speech = True
    g.__wrapped__ = f
    setattr(mod, name, g)


def install():
    """Opt-in: route every bubble through speech()."""
    import fs_storyboard as sb, dh_cast as dc, sofia_cs, sofia_dh, sofia_ob, pam_bc, mom_fs, robot_mf
    import dh_anim1 as A, dh_anim2, dh_anim3, dh_anim as DA
    if ON[0]:
        return
    ON[0] = True
    _wrap(sb, "don", "face", False)
    _wrap(dc, "father", "face", False)
    _wrap(dc, "repairman", "face", True)
    _wrap(sofia_cs, "sofia", "face", True)
    _wrap(sofia_dh, "sofia", "face", True)
    _wrap(sofia_ob, "sofia", "face", True)
    _wrap(pam_bc, "pam", "face", True)
    _wrap(mom_fs, "mom", "face", True)
    _wrap(robot_mf, "robot", "antenna", False)
    import dh_props as dp
    _wrap_keep(dp, "_price_tag")
    _wrap_keep(dp, "star_screen")
    _wrap_keep(dp, "wet_filter")                             # the filter on Don's head (scene 5): no tail through it
    _wrap_booth(dp)
    A.bubble = bubble
    for mod in (A, dh_anim2, dh_anim3):
        _fresh(mod, "frame")
    _fresh(DA.Scene, "frame")


def _wrap_keep(mod, name):
    f = getattr(mod, name)
    if getattr(f, "_speech", False):
        return

    def g(k, *a, **kw):
        o = f(k, *a, **kw)
        c = k.c
        if c.get_target().get_width() < 270:
            return o
        kp = dict(f=f, a=a, kw=dict(kw), m=c.get_matrix(), hi=c.get_target().get_width() / 540.0)
        kp["mask"] = _keep_one(kp)                          # now, while the tag hangs as the scene drew it
        KEEP.append(kp)
        return o
    g._speech = True
    setattr(mod, name, g)


def _wrap_booth(dp):
    """The booth insert: Father's chin and mouth fill the top of the frame. Logged as a face of its own."""
    f = dp.booth
    if getattr(f, "_speech", False):
        return

    def g(k, *a, **kw):
        o = f(k, *a, **kw)
        c = k.c
        if c.get_target().get_width() < 270:
            return o
        REG.append(dict(f=f, k=k, a=a, kw=dict(kw), m=c.get_matrix(), idx=len(REG), hi=c.get_target().get_width() / 540.0,
                        head_u=c.device_to_user(*[v * c.get_target().get_width() / 540.0 for v in BOOTH_MOUTH]),
                        kind="booth", mouth_kw=False, name="booth", mod="dh_props"))
        return o
    g._speech = True
    dp.booth = g


BOOTH_MOUTH = (270.0, 83.0)       # where dp.booth draws Father's mouth line, in the frame (measured on drawing 29)


def keep_mask():
    """Everything logged in KEEP, redrawn alone: one mask."""
    M = np.zeros((960, 540), bool)
    for kp in KEEP:
        M |= kp.get("mask") if kp.get("mask") is not None else _keep_one(kp)
    return M


def _keep_one(kp):
    M = np.zeros((960, 540), bool)
    for kp in [kp]:
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
        c.set_source_rgb(0, 1, 0); c.paint(); c.set_matrix(_frame_matrix(kp))
        kp["f"](Ctx(c, 0), *kp["a"], **kp["kw"]); s.flush()
        a = np.frombuffer(s.get_data(), np.uint8).reshape(960, s.get_stride() // 4, 4)[:, :540, :3][:, :, ::-1].astype(int)
        m = ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
        from scipy import ndimage
        M |= _dilate(ndimage.binary_erosion(m, iterations=3), 3)   # the card and knot, not the thin cord
    return M


def others_mask(rec):
    """Everyone else in the drawing (the rigs logged besides the speaker), redrawn alone: a bubble keeps off them too."""
    M = np.zeros((960, 540), bool)
    seen = set()
    for r_ in REG:
        if r_ is rec or r_.get("kind") == "booth" or r_.get("idx") == rec.get("idx") or r_.get("idx") in seen:
            continue
        seen.add(r_.get("idx"))
        a, _, _ = r_.get("iso") or alone(r_)
        M |= ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
    return M


def _fresh(owner, name):
    f = getattr(owner, name)
    if getattr(f, "_speech", False):
        return

    def g(*a, **kw):
        del REG[:]; del LAST[:]; del KEEP[:]
        return f(*a, **kw)
    g._speech = True
    setattr(owner, name, g)


# ---------------------------------------------------------------- the speaker redrawn alone

def _frame_matrix(rec):
    m, h = rec["m"], rec["hi"]
    return cairo.Matrix(m.xx / h, m.yx / h, m.xy / h, m.yy / h, m.x0 / h, m.y0 / h)


def alone(rec, **over):
    """The rig redrawn alone at frame scale on pure green; returns (RGB int array, head in frame coords, scale)."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    c.set_source_rgb(0, 1, 0); c.paint()
    c.set_matrix(_frame_matrix(rec))
    kw = dict(rec["kw"]); kw.update(over)
    _DEPTH[0] += 1
    try:
        o = rec["f"](Ctx(c, 0), *rec["a"], **kw)
    finally:
        _DEPTH[0] -= 1
    hx, hy = c.user_to_device(*(o["head"] if isinstance(o, dict) and "head" in o else rec["head_u"]))
    s.flush()
    a = np.frombuffer(s.get_data(), np.uint8).reshape(960, s.get_stride() // 4, 4)[:, :540, :3][:, :, ::-1].astype(int)
    sc = math.hypot(*c.user_to_device_distance(1, 0))
    return a, (hx, hy), sc


def _scale_arg(rec):
    a = rec["a"]
    if len(a) >= 3:
        return a[2]
    return rec["kw"].get("s", 1.0)


def read_face(rec):
    """Outline, skin, mouth and face radius of the speaker from its lone redraw."""
    a, (hx, hy), sc = rec.get("iso") or alone(rec)
    s = _scale_arg(rec) * sc                                 # rig units -> frame px
    N = ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
    if rec["mouth_kw"]:
        import dh_anim as DA
        b, _, _ = rec.get("iso_open") or alone(rec, mouth=DA.M_BIG)
        z, _, _ = rec.get("iso_shut") or alone(rec, mouth=None)
        d = np.abs(b - z).sum(-1) > 40
        ys, xs = np.nonzero(d)
        if len(ys):
            mx, my = float(np.median(xs)), float(np.median(ys))
            mw = max(4.0, (np.percentile(xs, 95) - np.percentile(xs, 5)) / 2)
        else:
            mx, my, mw = hx, hy + 30 * s, 10 * s
    else:
        mx, my, mw = hx, hy + 28 * s, 11 * s
    # skin: the commonest colour on the face between the eyes and the mouth
    y0, y1 = int(hy + 4 * s), int(my - 4 * s)
    x0, x1 = int(hx - 22 * s), int(hx + 22 * s)
    patch = a[max(0, y0):max(1, y1), max(0, x0):min(540, x1)].reshape(-1, 3)
    patch = patch[N[max(0, y0):max(1, y1), max(0, x0):min(540, x1)].reshape(-1)] if len(patch) else patch
    if len(patch) == 0:
        sk = a[int(my), int(min(539, mx + mw + 3))]
    else:
        q = (patch // 8)
        keys, cnt = np.unique(q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2], return_counts=True)
        kk = keys[cnt.argmax()]
        sel = patch[(q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]) == kk]
        sk = sel.mean(0)
    S = (np.abs(a - sk).sum(-1) < 36) & N
    # the face's radius: its widest run of skin between the eyes and the mouth (one row can be all glasses)
    r = 0.0
    for yy in range(max(0, int(hy - 10 * s)), min(960, int(my) + 1), 2):
        row = np.nonzero(S[yy, max(0, int(hx - 90 * s)):min(540, int(hx + 90 * s))])[0]
        if len(row) > 4:
            r = max(r, (row.max() - row.min()) / 2.0)
    r = r if r > 14 else 40 * s
    if not rec["mouth_kw"]:                                 # Don, Father: the mouth the rig drew, the lowest dark shape
        from scipy import ndimage                           # inside the face (eyes have white in them)
        F = S.copy()
        lab, nl = ndimage.label(F)
        if nl:
            k_ = lab[int(hy), int(hx)] if (0 <= int(hy) < 960 and 0 <= int(hx) < 540 and lab[int(hy), int(hx)]) else np.bincount(lab[lab > 0]).argmax()
            F = lab == k_
            H = ndimage.binary_fill_holes(F) & ~F
            hl, nh = ndimage.label(H)
            widths = F.sum(1); fy_ = np.nonzero(widths >= 0.35 * widths.max())[0]
            ylow = fy_.max() if len(fy_) else 960
            best = None
            for i in range(1, nh + 1):
                yy, xx = np.nonzero(hl == i)
                if len(yy) < 12 or np.ptp(xx) < 0.15 * r or a[yy, xx].sum(-1).mean() >= 420:
                    continue
                if yy.mean() < hy or yy.mean() > ylow + 0.1 * r:
                    continue
                dprior = math.hypot(xx.mean() - hx, yy.mean() - (hy + 28 * s))   # nearest the rig's mouth place,
                if dprior > 0.3 * r:                                              # not a chin crease below it
                    continue
                if best is None or dprior < best[3]:
                    best = (yy.mean(), xx.mean(), np.ptp(xx) / 2.0, dprior)
            if best:
                my, mx, mw = best[0], best[1], max(mw * 0.6, best[2])
    return dict(a=a, N=N, S=S, head=(hx, hy), mouth=(mx, my), mw=mw, r=r, s=s, skin=sk)


def _dilate(M, n):
    out = M.copy()
    for _ in range(n):
        o = out.copy()
        o[1:] |= out[:-1]; o[:-1] |= out[1:]; o[:, 1:] |= out[:, :-1]; o[:, :-1] |= out[:, 1:]
        out = o
    return out


def read_booth(rec):
    """The booth: only Father's face counts as him (the booth around him is set)."""
    a, _, sc = alone(rec)
    mx, my = _frame_matrix(rec).transform_point(*rec["head_u"])
    sk = a[int(my) + 14, int(mx) + 46]
    S = np.abs(a - sk).sum(-1) < 60
    row = np.nonzero(S[int(my) + 14])[0]
    r = (row.max() - row.min()) / 2.0 if len(row) > 4 else 120.0
    N = _dilate(S, 6)
    import dh_props as dp
    was = dp.MOTTO[0]; dp.MOTTO[0] = not was
    b, _, _ = alone(rec); dp.MOTTO[0] = was
    K = _dilate(np.abs(a - b).sum(-1) > 30, 8)              # the neon sign on the wall
    K[330:, :] = True                                        # and the phone held up below his chin
    from scipy import ndimage
    H = ndimage.binary_fill_holes(S) & ~S                 # the mouth line is a hole in his face
    hl, nh = ndimage.label(H)
    mw = 0.28 * r
    if nh:
        i = hl[int(my) - 6:int(my) + 7, int(mx) - 40:int(mx) + 41]
        ids = i[i > 0]
        if len(ids):
            yy, xx = np.nonzero(hl == np.bincount(ids).argmax())
            mx, my, mw = float(xx.mean()), float(yy.mean()), (xx.max() - xx.min()) / 2.0
    return dict(a=a, N=N, S=S, K=K, head=(mx, my - 0.45 * r), mouth=(mx, my), mw=mw, r=r, s=sc, skin=sk)


def read_antenna(rec):
    a, (hx, hy), sc = rec.get("iso") or alone(rec)
    s = _scale_arg(rec) * sc
    N = ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
    band = N[:, max(0, int(hx - 14 * s)):min(540, int(hx + 14 * s))]
    ys = np.nonzero(band.any(1))[0]
    ys = ys[ys < hy]
    top = int(ys.min()) if len(ys) else int(hy - 62 * s)
    xs = np.nonzero(N[top + 2, :])[0]
    xs = xs[np.abs(xs - hx) < 20 * s]
    ax = float(xs.mean()) if len(xs) else hx
    return dict(N=N, head=(hx, hy), tip=(ax, top + 1.0), r=50 * s, s=s)


# ---------------------------------------------------------------- where the tail goes in

def door(fc, d, tier=1):
    """The tip on the cheek at mouth height, side d (+1 right, -1 left), and the way in.
    From the mouth's corner a ray goes out (level first, then slanting down, under a bob or long hair); it must cross
    only skin, then at most a thin ink line, then nothing of the speaker for 16 px in a band 10 px wide. Rows nearest the
    mouth and level rays are tried first. The tip is just inside the cheek's edge, at most 0.4 radius from the mouth."""
    N, S = fc["N"], fc["S"]
    mx, my, mw, r = fc["mouth"][0], fc["mouth"][1], fc["mw"], fc["r"]
    lim = (0.22 if fc.get("K") is not None else 0.28) * r
    for ang in (0, 20, 35, 50, 62):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        ux, uy = d * ca, sa
        for dy in sorted(range(-int(0.14 * r), int(0.14 * r) + 1), key=abs):
            y0 = my + dy
            x0 = mx + d * (mw + 2)
            px, py = x0, y0
            ok = False
            for j in range(0, 8):                          # off the lips onto skin
                xi, yi = int(round(px + d * j)), int(round(py))
                if 0 <= xi < 540 and 0 <= yi < 960 and S[yi, xi]:
                    px = px + d * j; ok = True; break
            if not ok:
                continue
            sx, sy = px, py
            steps = 0
            first_skip = None
            while True:
                xi, yi = int(round(px)), int(round(py))
                if not (0 <= xi < 540 and 0 <= yi < 960):
                    break
                if not S[yi, xi]:                          # a line drawn on the face (a fold, a wrinkle): skin again soon
                    jump = 0
                    for j in range(1, 7):
                        xj, yj = int(round(px + ux * j)), int(round(py + uy * j))
                        if 0 <= xj < 540 and 0 <= yj < 960 and S[yj, xj]:
                            jump = j; break
                    if not jump:
                        break
                    if first_skip is None and jump > 4:          # a wrinkle (4 px) is face; a mic boom is not
                        first_skip = math.hypot(px - sx, py - sy)
                    px += ux * jump; py += uy * jump; steps += jump
                    continue
                px += ux; py += uy; steps += 1
            ex, ey = px, py                                # first point past the skin
            # past the skin: thin lines only (the face's outline, a glasses chain, an earring's wire): at most three
            # runs of 7 px or less, 16 px in all, before open air
            runs, tot, bad = 0, 0, False
            for _ in range(60):
                xi, yi = int(round(px)), int(round(py))
                if not (0 <= xi < 540 and 0 <= yi < 960):
                    bad = True; break
                if not N[yi, xi]:
                    # open air for 16 px? then done; else keep walking
                    clear = all(not (0 <= int(round(px + ux * j)) < 540 and 0 <= int(round(py + uy * j)) < 960)
                                or not N[int(round(py + uy * j)), int(round(px + ux * j))] for j in range(1, 17 if tier == 1 else 31))
                    if clear:
                        break
                    px += ux; py += uy
                    continue
                run = 0
                while 0 <= int(round(px)) < 540 and 0 <= int(round(py)) < 960 and N[int(round(py)), int(round(px))] and run < 9:
                    px += ux; py += uy; run += 1
                runs += 1; tot += run
                if (run >= 9 or runs > 1) if tier == 1 else (run >= 27 or runs > 4 or tot > 36):
                    bad = True; break
            if bad:
                continue
            free = True
            for j in range(2, 18, 2):
                qx, qy = px + ux * j, py + uy * j
                for w in (-5, 0, 5):
                    xi, yi = int(round(qx - uy * w)), int(round(qy + ux * w))
                    if not (0 <= xi < 540 and 0 <= yi < 960) or N[yi, xi]:
                        free = False; break
                if not free:
                    break
            if not free:
                continue
            back = 11.0
            tx, ty = ex - ux * back, ey - uy * back
            if math.hypot(tx - sx, ty - sy) > lim:          # a wide cheek: the tip stops 0.4 r from the mouth
                t_ = lim / max(1e-6, math.hypot(ex - sx, ey - sy))
                tx, ty = sx + (ex - sx) * t_, sy + (ey - sy) * t_
            if (tx - sx) * d < 0:
                tx, ty = sx, sy
            if first_skip is not None and first_skip < math.hypot(tx - sx, ty - sy) + 2:
                continue                                   # a line (a mic boom, a fold) between the tip and the mouth
            return dict(tip=(float(tx), float(ty)), out=(float(px), float(py)), ray=(ux, uy), dy=dy, ang=ang, mouth_edge=float(sx), tier=tier)
    return None


def _outer(N, d, y0, y1, hx, lim):
    """The speaker's outermost column on side d between rows y0..y1 (within lim px of the head)."""
    y0, y1 = max(0, int(y0)), min(959, int(y1))
    xa, xb = max(0, int(hx - lim)), min(540, int(hx + lim))
    sub = N[y0:y1 + 1, xa:xb]
    cols = np.nonzero(sub.any(0))[0]
    if not len(cols):
        return hx
    return xa + (cols.max() if d > 0 else cols.min())


# ---------------------------------------------------------------- drawing

def _lines(c, text, maxw):
    c.select_font_face(kit.FONT); c.set_font_size(31)
    lines = [""]
    for w_ in text.split():
        cand = (lines[-1] + " " + w_).strip()
        if c.text_extents(cand).x_advance > maxw and lines[-1]:
            lines.append(w_)
        else:
            lines[-1] = cand
    bw = max(c.text_extents(l).x_advance for l in lines) + 44
    bh = 26 + 37 * len(lines)
    return lines, bw, bh


def _box_path(c, bx, y, bw, bh, r=16):
    c.new_path()
    c.arc(bx + r, y + r, r, math.pi, 1.5 * math.pi); c.arc(bx + bw - r, y + r, r, 1.5 * math.pi, 0)
    c.arc(bx + bw - r, y + bh - r, r, 0, 0.5 * math.pi); c.arc(bx + r, y + bh - r, r, 0.5 * math.pi, math.pi); c.close_path()


def _centre(B, Q, tip, ctrl):
    """Centre line: a quadratic from the box point B to Q (outside the head, at door height), then straight in to the tip."""
    pts = []
    for i in range(25):
        t = i / 24.0
        pts.append(((1 - t) ** 2 * B[0] + 2 * (1 - t) * t * ctrl[0] + t * t * Q[0],
                    (1 - t) ** 2 * B[1] + 2 * (1 - t) * t * ctrl[1] + t * t * Q[1]))
    n = max(2, int(math.hypot(tip[0] - Q[0], tip[1] - Q[1]) / 6))
    for i in range(1, n + 1):
        t = i / float(n)
        pts.append((Q[0] + (tip[0] - Q[0]) * t, Q[1] + (tip[1] - Q[1]) * t))
    return pts


def _tail_poly(pts, w0=13.0, w1=1.2):
    L = [0.0]
    tot0 = sum(math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]) for i in range(1, len(pts)))
    w0 = min(w0, max(5.0, 0.16 * tot0))
    for i in range(1, len(pts)):
        L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = L[-1] or 1.0
    left, right = [], []
    for i, p in enumerate(pts):
        j0, j1 = max(0, i - 1), min(len(pts) - 1, i + 1)
        dx, dy = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        w = w0 + (w1 - w0) * (L[i] / tot) ** 0.8
        left.append((p[0] + nx * w, p[1] + ny * w)); right.append((p[0] - nx * w, p[1] - ny * w))
    return left + right[::-1]


def _dseg(p, a, b):
    ax, ay = a; bx, by = b
    L2 = (bx - ax) ** 2 + (by - ay) ** 2 or 1.0
    t = max(0.0, min(1.0, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / L2))
    return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))


def _clear_tail(NK, pts, tip, skip, seg=None, wmax=13.0):
    """Is the drawn tail (its own width at each point, plus 4 px) clear of NK, except within skip px of the tip?"""
    L = [0.0]
    for i in range(1, len(pts)):
        L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = L[-1] or 1.0
    w0 = min(wmax, max(5.0, 0.16 * tot))
    for i, (x, y) in enumerate(pts):
        if math.hypot(x - tip[0], y - tip[1]) <= skip and (seg is None or _dseg((x, y), tip, seg) <= 8):
            continue                                       # the last stretch, along the way door() found clear
        w = int(w0 + (1.2 - w0) * (L[i] / tot) ** 0.8 + 4)
        xi, yi = int(x), int(y)
        y0, y1, x0, x1 = max(0, yi - w), min(960, yi + w + 1), max(0, xi - w), min(540, xi + w + 1)
        if y0 < y1 and x0 < x1 and NK[y0:y1, x0:x1].any():
            return False
    return True


def _hits(N, poly_pts, upto):
    """Does the tail's centre line (before index upto) come within 9 px of the speaker?"""
    for (x, y) in poly_pts[:upto]:
        xi, yi = int(x), int(y)
        y0, y1, x0, x1 = max(0, yi - 9), min(960, yi + 10), max(0, xi - 9), min(540, xi + 10)
        if y0 < y1 and x0 < x1 and N[y0:y1, x0:x1].any():
            return True
    return False


def _draw(c, lines, bx, y, bw, bh, tail, dark, card=None):
    c.set_line_join(1)
    for fill in (False, True):
        _box_path(c, bx, y, bw, bh)
        if tail:
            c.move_to(*tail[0])
            for p in tail[1:]:
                c.line_to(*p)
            c.close_path()
        if fill:
            c.set_source_rgb(*((0.16, 0.05, 0.08) if dark else (1, 1, 1))); c.fill()
        else:
            c.set_source_rgb(*((0.93, 0.25, 0.35) if dark else INK)); c.set_line_width(7); c.stroke()
    c.select_font_face(kit.FONT); c.set_font_size(31)
    c.set_source_rgb(*((1, 1, 1) if dark else INK))
    top = y
    if card:
        c.set_font_size(19)
        c.move_to(bx + 20, y + 30); c.show_text(card)
        top = y + 22; c.set_font_size(31)
    for i, l in enumerate(lines):
        c.move_to(bx + (bw - c.text_extents(l).x_advance) / 2, top + 42 + 37 * i); c.show_text(l)


def _clamp_box(bx, bw):
    return min(max(bx, 24), 462 - bw)


def bubble(c, text, tip, y=128, up=False, side=0, maxw=372, dark=False, shift=0):
    """Same call as dh_anim1.bubble; draws by the PR #62 rule. tip only says whose line it is (the nearest head)."""
    if PLANT[0] is not None:
        return PLANT[0](c, text, tip, y, up, side, maxw, dark, shift)
    if text in CARD:
        return card(c, text, CARD[text], side, maxw)
    rec = pick(tip)
    if rec is None:
        return card(c, text, "", side, maxw)
    if rec["kind"] == "antenna":
        return _antenna(c, text, rec, side, maxw, dark, y)
    return _face(c, text, rec, side, maxw, dark, y)


def _box_ok(NK, bx, y, bw, bh):
    if bx < 24 or bx + bw > 516 or y < 100 or y + bh > 700:
        return False
    if bx + bw > 470 and y + bh > 380:                      # the right rail
        return False
    y0, y1, x0, x1 = int(max(0, y - 8)), int(min(960, y + bh + 8)), int(max(0, bx - 8)), int(min(540, bx + bw + 8))
    return not NK[y0:y1, x0:x1].any()


def _candidates(NK, d, bw, bh, hx, y_ideal, door_pt):
    """Free places for the box, best first: near y_ideal, on side d, close to where the tail goes in."""
    out = []
    for y in range(100, 700 - int(bh), 8):
        for bx in range(24, int(516 - bw) + 1, 8):
            if not _box_ok(NK, bx, y, bw, bh):
                continue
            cx = bx + bw / 2.0
            wrong = (cx - hx) * d < 0
            near = abs(min(max(door_pt[0], bx), bx + bw) - door_pt[0]) + max(0.0, max(y - door_pt[1], door_pt[1] - (y + bh)))
            out.append((abs(y - y_ideal) * 1.0 + 0.35 * near + (120 if wrong else 0) + (60 if y > door_pt[1] else 0), bx, y))
    out.sort()
    return out


def _quad(B, ctrl, tip, n=40):
    return [((1 - t) ** 2 * B[0] + 2 * (1 - t) * t * ctrl[0] + t * t * tip[0],
             (1 - t) ** 2 * B[1] + 2 * (1 - t) * t * ctrl[1] + t * t * tip[1]) for t in [i / float(n) for i in range(n + 1)]]


def _cubic(B, c1, c2, tip, n=48):
    out = []
    for i in range(n + 1):
        t = i / float(n); u = 1 - t
        out.append((u ** 3 * B[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * tip[0],
                    u ** 3 * B[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * tip[1]))
    return out


def _route(NK, N, hx, r, tip, out, d, box, ray=(1, 0), tier=1):
    """One smooth curve from the box to the tip: out round the head (first control point outside its widest part), then
    in along the way the door was found (second control point on that ray, outside the face), so the last stretch
    crosses only what door() allowed. Only that last stretch may touch the speaker."""
    bx, y, bw, bh = box
    ux, uy = ray
    inside = math.hypot(tip[0] - out[0], tip[1] - out[1]) + 24
    for push in range(0, 160, 8):
        c2 = (out[0] + ux * (22 + push * 0.6), out[1] + uy * (22 + push * 0.6))
        if y + bh < c2[1] - 16:
            X = _outer(N, d, y + bh, c2[1], hx, 2.2 * r) + d * (24 + push)
            B = (min(max(X, bx + 26), bx + bw - 26), y + bh - 14)
            c1 = (X, B[1] + 0.55 * (c2[1] - B[1]))
        elif y > c2[1] + 16:
            X = _outer(N, d, c2[1], y, hx, 2.2 * r) + d * (24 + push)
            B = (min(max(X, bx + 26), bx + bw - 26), y + 14)
            c1 = (X, B[1] + 0.55 * (c2[1] - B[1]))
        else:
            X = c2[0]
            by = min(max(c2[1], y + 20), y + bh - 20)
            B = (bx + 16, by) if X < bx + bw / 2 else (bx + bw - 16, by)
            c1 = ((B[0] + c2[0]) / 2, (B[1] + c2[1]) / 2)
        if not (0 <= X < 540 and 0 <= c2[0] < 540):
            return None
        pts = _cubic(B, c1, c2, tip)
        if _clear_tail(NK, pts, tip, math.hypot(tip[0] - out[0], tip[1] - out[1]) + 6, seg=c2 if tier == 1 else None):
            return pts
    return None


def pick(tip):
    """The speaker: the logged rig whose head is nearest the point the scene aimed the old tail at."""
    rec, best = None, 1e9
    for r_ in REG:
        hx, hy = _frame_matrix(r_).transform_point(*r_["head_u"])
        dd = math.hypot(hx - tip[0], hy - tip[1])
        if dd < best:
            best, rec = dd, r_
    return rec


def _face_try(c, text, rec, fc, NK, N, hx, hy, r, head_top, held, sides, maxw, dark, y_pref):
    tries = [(d_, 1) for d_ in sides] + [(d_, 2) for d_ in sides]   # tier 2: across an earring or a chain, not hair
    for d, tier in tries:
        dr = door(fc, d, tier)
        if not dr:
            continue
        tip, out = dr["tip"], dr["out"]
        tried = []
        for mw in sorted({maxw, maxw * 0.75, maxw * 0.55, min(maxw, 170), min(maxw, 140), min(maxw, 110)}, reverse=True):
            lines, bw, bh = _lines(c, text, mw)
            if held:
                if len(held) > 6 and held[6] == (bw, bh) and _box_ok(NK, held[0], held[1], bw, bh):
                    tried.append((0, held[0], held[1], lines, bw, bh))
                continue
            y_ideal = max(104.0, min(float(y_pref), head_top - bh - 26))
            for sc, bx, y in _candidates(NK, d, bw, bh, hx, y_ideal, out)[:400]:
                tried.append((sc + 70 * (len(lines) - 1) + 0.8 * abs(y - y_ideal), bx, y, lines, bw, bh))
        tried.sort(key=lambda z: z[0])
        good = []
        for sc_, bx, y, lines, bw, bh in tried[:900]:
            pts = _route(NK, N, hx, r, tip, out, d, (bx, y, bw, bh), dr["ray"], dr["tier"])
            if pts:
                ln = sum(math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]) for i in range(1, len(pts)))
                good.append((sc_ + 0.3 * ln, bx, y, lines, bw, bh, pts))
                if len(good) >= 14 or held:
                    break
        if good:
            _, bx, y, lines, bw, bh, pts = min(good, key=lambda z: z[0])
            HELD[text] = (bx, y, d, hx, hy, r, (bw, bh))
            _draw(c, lines, bx, y, bw, bh, _tail_poly(pts), dark)
            LAST.append(dict(kind="face", text=text, tip=tip, mouth=fc["mouth"], r=r, box=(bx, y, bw, bh), side=d, rec=rec, dy=dr["dy"], tier=dr["tier"]))
            return True
    return False


def _face(c, text, rec, side, maxw, dark, y_pref):
    fc = read_booth(rec) if rec["kind"] == "booth" else read_face(rec)
    hx, hy = fc["head"]; r = fc["r"]; N = fc["N"]
    NK = N | keep_mask() if KEEP else N.copy()
    NK = NK | _dilate(others_mask(rec), 4)
    if "K" in fc:
        NK = NK | fc["K"]
    top = np.nonzero(N[:, max(0, int(hx - 1.6 * r)):min(540, int(hx + 1.6 * r))].any(1))[0]
    head_top = float(top.min()) if len(top) else hy - 1.4 * r
    held0 = HELD.get(text)
    d0 = side if side else (1 if hx < 270 else -1)
    if held0 and math.hypot(held0[3] - hx, held0[4] - hy) < 0.6 * r and len(held0) > 6 and _box_ok(NK, held0[0], held0[1], *held0[6]):
        attempts = [(held0, [held0[2], -held0[2]]), (None, [d0, -d0])]   # the held box first; a fresh place if it fails
    else:
        attempts = [(None, [d0, -d0])]
    for held, sides in attempts:
        if _face_try(c, text, rec, fc, NK, N, hx, hy, r, head_top, held, sides, maxw, dark, y_pref):
            return
    held = None
    return _overhead(c, text, fc, d0, maxw, dark, y_pref, None, NK, rec)


NAME = {"don": "DON", "father": "FATHER", "repairman": "REPAIRMAN", "pam": "PAM", "mom": "MOM", "booth": "FATHER"}


def _overhead(c, text, fc, d, maxw, dark, y_pref, held, NK, rec):
    """No clean way in at the cheek: onto the top of a bare scalp, touching it. A speaker with hair, or a scalp with no
    clean way down to it, gets the quoted card with their name instead of a tail across their hair."""
    hx0, hy = fc["head"]; N, S, r = fc["N"], fc["S"], fc["r"]
    who = NAME.get(rec.get("name"), "SOFÍA" if rec.get("name") == "sofia" else "")
    cols = []
    for off in (0, -0.15, 0.15, -0.3, 0.3, -0.45, 0.45):     # columns where the scalp's skin is the top of him,
        x = int(hx0 + off * r)                               # least in the way above first (a curl, the headset)
        ks = np.nonzero(S[:int(hy), x])[0]
        if not len(ks):
            continue
        st = int(ks.min())
        if S[st + 2:st + 10, x - 3:x + 4].mean() <= 0.6:    # not bare scalp there
            continue
        if N[max(0, st - 60):max(0, st - 8), x - 2:x + 3].any():   # hair (or anything of him) right above: not a bare top
            continue
        busy = int(N[max(0, st - 40):max(0, st - 6), max(0, x - 16):x + 17].sum()) + int(abs(off) * 40)
        cols.append((busy, x, st))
    cols.sort()
    if not cols:
        return card(c, text, who, d, maxw)
    allc = {}
    found = None
    for busy, x, st in cols[:4]:
        hx, ty = float(x), float(st)
        tip = (hx, ty + 7.0)
        clear = NK.copy(); clear[max(0, int(ty) - 14):, max(0, int(hx - 0.5 * r)):int(hx + 0.5 * r)] = False   # the last bit reaches the scalp
        if KEEP:                                             # ...but never through the tag or the filter on his head
            clear |= keep_mask()
        cands = []
        for mw in sorted({maxw, maxw * 0.75, min(maxw, 140), min(maxw, 110)}, reverse=True):
            lines, bw, bh = _lines(c, text, mw)
            cs = [cd for cd in _candidates(NK, 0, bw, bh, hx, max(104.0, min(float(y_pref), ty - bh - 40)), (hx, ty - 30))
                  if cd[2] + bh < ty - 24]
            cands += [(sc + 70 * (len(lines) - 1), bx, y, lines, bw, bh) for sc, bx, y in cs[:150]]
        cands.sort(key=lambda z: z[0])
        hb = HELD.get(text)
        if hb and len(hb) > 6:                              # the box already up for this line, if it still works
            lines_h, bw_h, bh_h = None, hb[6][0], hb[6][1]
            for mw in sorted({maxw, maxw * 0.75, min(maxw, 140), min(maxw, 110)}, reverse=True):
                l_, w_, h_ = _lines(c, text, mw)
                if (w_, h_) == (bw_h, bh_h):
                    lines_h = l_
            if lines_h and _box_ok(NK, hb[0], hb[1], bw_h, bh_h) and hb[1] + bh_h < ty - 24:
                cands.insert(0, (-1e9, hb[0], hb[1], lines_h, bw_h, bh_h))
        for _, bx, y, lines, bw, bh in cands[:300]:
            B = (min(max(hx, bx + 26), bx + bw - 26), y + bh - 14)
            for off in (0, 40, -40, 80, -80, 130, -130):    # a curve round whatever hangs above him (the tag, the crown)
                pts = _quad(B, (hx + off, (B[1] + ty) / 2), tip)
                if _clear_tail(clear, pts, tip, 14, wmax=8.0):   # a slim tail threads between the tag and a curl
                    found = (bx, y, pts, lines, bw, bh, tip); break
            if found:
                break
        if found:
            break
    if not found:                                           # nothing clean even onto the scalp: the card
        return card(c, text, who, d, maxw)
    bx, y, pts, lines, bw, bh, tip = found
    HELD[text] = (bx, y, d, hx0, hy, r, (bw, bh))
    _draw(c, lines, bx, y, bw, bh, _tail_poly(pts, 8.0), dark)
    LAST.append(dict(kind="overhead", text=text, tip=tip, mouth=fc["mouth"], r=r, box=(bx, y, bw, bh), side=d, rec=rec))


def _antenna(c, text, rec, side, maxw, dark, y_pref):
    an = read_antenna(rec)
    ax, ay = an["tip"]
    lines, bw, bh = _lines(c, text, maxw)
    d = side if side else (1 if ax < 270 else -1)
    held = HELD.get(text)
    if held and math.hypot(held[3] - an["head"][0], held[4] - an["head"][1]) < 0.6 * an["r"]:
        bx, y = held[0], held[1]
    else:
        y = max(104.0, min(float(y_pref), ay - bh - 50))
        if ay - (y + bh) >= 50:
            bx = _clamp_box(ax - 40 if d > 0 else ax + 40 - bw, bw)
        else:                                               # no room above: beside the antenna, a level tail 40 px long
            y = max(104.0, ay - bh / 2.0 - 10)
            bx = ax + 40 if d > 0 else ax - 40 - bw
            if bx < 24 or bx + bw > 462:
                bx = ax - 40 - bw if d > 0 else ax + 40
            bx = _clamp_box(bx, bw)
        HELD[text] = (bx, y, d, an["head"][0], an["head"][1], an["r"])
    if y + bh < ay - 12:
        B = (min(max(ax + d * 24, bx + 26), bx + bw - 26), y + bh - 14)
        ctrl = (ax + d * 6, (B[1] + ay) / 2)
    else:
        B = (bx + 16 if ax < bx else bx + bw - 16, min(max(ay - 10, y + 20), y + bh - 20))
        ctrl = ((B[0] + ax) / 2, ay - 4)
    tip = (ax, ay)
    pts = _centre(B, tip, tip, ctrl)
    _draw(c, lines, bx, y, bw, bh, _tail_poly(pts, 12.0, 1.6), dark)
    LAST.append(dict(kind="antenna", text=text, tip=tip, box=(bx, y, bw, bh), side=d, rec=rec, r=an["r"]))


def card(c, text, who, side, maxw):
    """Off the frame (or no clean way to the mouth): a quoted card with the speaker's name, no tail, on the side they
    are on, off the tag and off everyone in the drawing."""
    q = "\u201c%s\u201d" % text
    M = _dilate(keep_mask(), 6) if KEEP else np.zeros((960, 540), bool)
    for r_ in REG:
        if r_.get("kind") != "booth":
            a, _, _ = r_.get("iso") or alone(r_)
            M |= ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
    M2 = _dilate(keep_mask(), 6) if KEEP else np.zeros((960, 540), bool)   # second choice: off skin and signs only
    for r_ in REG:
        if r_.get("kind") == "face":
            try:
                fc_ = read_face(r_); M2 |= _dilate(fc_["S"], 6)
                hx_, hy_ = fc_["head"]; rr = fc_["r"]
                M2[max(0, int(hy_ - 1.5 * rr)):int(hy_ + 1.1 * rr), max(0, int(hx_ - 1.4 * rr)):int(hx_ + 1.4 * rr)] = True
            except Exception:
                pass
        elif r_.get("kind") == "antenna":
            a, _, _ = r_.get("iso") or alone(r_)
            M2 |= ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
    held = HELD.get(text)
    best = None
    for mw in sorted({maxw, 200, 160, 130, 110, 96}, reverse=True):
        lines, bw, bh = _lines(c, q, mw)
        bh += 22 if who else 0
        if held and len(held) > 6 and held[6] == (bw, bh) and _box_ok(M2, held[0], held[1], bw, bh):
            best = (0, held[0], held[1], lines, bw, bh); break      # a card stays where it went up while it is clear
        pref = 24 if side < 0 else (462 - bw if side > 0 else (540 - bw) / 2)
        for y in range(104, 600, 8):
            for bx in range(24, int(462 - bw) + 1, 8):
                if _box_ok(M, bx, y, bw, bh):
                    sc = abs(bx - pref) * 0.5 + (y - 104) * 1.0 + 60 * (len(lines) - 1)
                    if best is None or sc < best[0]:
                        best = (sc, bx, y, lines, bw, bh)
    if best is None:                                        # over a body is all right; over a face, a hand or a sign is not
        for mw in sorted({maxw, 200, 160, 130}, reverse=True):
            lines, bw, bh = _lines(c, q, mw)
            bh += 22 if who else 0
            pref = 24 if side < 0 else (462 - bw if side > 0 else (540 - bw) / 2)
            for y in range(104, 600, 8):
                for bx in range(24, int(462 - bw) + 1, 8):
                    if _box_ok(M2, bx, y, bw, bh):
                        sc = abs(bx - pref) * 0.5 + (y - 104) * 1.0 + 60 * (len(lines) - 1)
                        if best is None or sc < best[0]:
                            best = (sc, bx, y, lines, bw, bh)
    if best is None:
        lines, bw, bh = _lines(c, q, maxw); bh += 22 if who else 0
        best = (0, 24 if side < 0 else 462 - bw, 112, lines, bw, bh)
    _, bx, y, lines, bw, bh = best
    HELD[text] = (bx, y, side, 0, 0, 1, (bw, bh))
    _draw(c, lines, bx, y, bw, bh, None, False, card=(who + ":") if who else None)
    LAST.append(dict(kind="card", text=text, box=(bx, y, bw, bh), side=side, who=who))
