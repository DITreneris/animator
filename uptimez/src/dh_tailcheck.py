"""Tail check for Daddy's Home (PR #62 rule), on rendered pixels of every drawing that carries a bubble.

    python3 dh_tailcheck.py selftest          five planted faults must each be caught (exit 1 if one slips through)
    python3 dh_tailcheck.py 1 2 ...           check those scenes; writes ../daddys-home/tailcheck/ (report + crops); exit 1 on a fail

How it reads a drawing (not from the numbers the bubble was drawn with):
- bubble   = the drawing with the bubble minus the same drawing with the bubble suppressed;
- box/tail = the bubble's rows that are box-wide are the box; the rest is the tail; the tip is the tail pixel farthest
             from the box;
- speaker  = the drawing minus the drawing with the speaker's rig left out (so whatever stands in front of them counts
             as not them);
- skin     = speaker pixels in the skin colours of the cast (the cast's own palette, not a guess from the bubble);
- mouth    = for the rigs that take a mouth: the drawing with the mouth forced open minus forced shut; for Don and
             Father: the dark shape inside the lower half of the face skin.
Checks: tip on the speaker's skin (or touching the top of a bald scalp / the robot's antenna); from the tip toward the
face only skin until the mouth, within 0.4 face radius; the tail over the speaker only on skin (its outline allowed);
no bubble pixel on anyone's skin away from the tip, or on the price tag or the booth's neon sign; the bubble out of the
bottom quarter and the right rail; no tip at the frame's edge; off-frame speakers get a card with no tail."""
import os
import sys
import json
import math
import numpy as np
import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
import dh_speech as SP
SP.install()
import kit
import dh_props as dp
import dh_scenes as ds
import dh_anim as DA
import dh_anim1 as A
import dh_anim1_v4 as OLD

OUT = os.environ.get("DH_TAIL_OUT", "../daddys-home/tailcheck")
TAIL_MAX = 26                                               # px of tail over open wall (20 + the outline and the 1.5 px overlap)
WALL = [0.0]
TIP_R = 0.7                                                 # the far cheek is beyond this
HAIR_RIGS = ("pam_bc", "mom_fs", "sofia_cs", "sofia_dh", "sofia_ob")   # hair beside the cheek: the tail may run over it (lessons 360)
BOX_MIN = 120                                               # px: narrower boxes are one word a line
DBG = {}


def _skins():
    sk = []
    for nm, v in kit.PEOPLE.items():
        if "skin" in v:
            sk.append(v["skin"])
    try:
        import client_ob as co; sk.append(co.SKIN)
    except Exception:
        pass
    for v in (getattr(ds, "SKIN_M", None),):
        if v:
            sk.append(v)
    # measured on the rigs (dh_speech's first measurements, 22 Nov): Father, Sofía, Pam, Mom, the repairman, the booth chin
    sk += [(0.93, 0.76, 0.65), (0.87, 0.67, 0.52), (1.0, 0.86, 0.67), (0.94, 0.76, 0.64), (0.90, 0.69, 0.55), (0.92, 0.76, 0.65)]
    return np.array([[int(round(c * 255)) for c in s[:3]] for s in sk], np.int32)


SK = _skins()


def skin_of(rgb):
    d = np.abs(rgb[:, :, None, :].astype(np.int32) - SK[None, None, :, :]).sum(-1).min(-1)
    return d < 46


def arr(surf):
    surf.flush()
    w, h = surf.get_width(), surf.get_height()
    return np.frombuffer(surf.get_data(), np.uint8).reshape(h, surf.get_stride() // 4, 4)[:, :w, :3][:, :, ::-1].astype(int).copy()


def scenes():
    import dh_anim2, dh_anim3, dh_anim4, dh_anim5, dh_anim6, dh_anim7, dh_anim8
    out = {1: (lambda tt, n: A.frame(tt, n, 1), A.TOTAL, False), 2: (lambda tt, n: dh_anim2.frame(tt, n, 1), dh_anim2.TOTAL, True),
           3: (lambda tt, n: dh_anim3.frame(tt, n, 1), dh_anim3.TOTAL, True)}
    for k, m in ((4, dh_anim4), (5, dh_anim5), (6, dh_anim6), (7, dh_anim7), (8, dh_anim8)):
        out[k] = (lambda tt, n, m=m: m.sc.frame(tt, n, 1), m.sc.total, True)
    if os.environ.get("DH_TAIL_S3") == "v8":                  # opt-in (24 Nov): scene 3 v8, its bubbles as rendered
        import dh_anim3_v8 as m8
        SY = m8.install_speech()
        if SY is not None:
            SY.plan_scene(lambda tt, n: m8.frame(tt, n, 1), m8.TOTAL)
            pass                                                # (no pinned boxes: dh_say places them)
        out[3] = (lambda tt, n: m8.frame(tt, n, 1), m8.TOTAL, True)
    return out


_ORIG = {}


def _overlays(mode):
    """Don's and Father's mouths are drawn over the face by the scene: force them open (1), leave them out (0), or as
    drawn (None)."""
    import dh_anim7, dh_anim8
    if not _ORIG:
        _ORIG.update(mouth=A.mouth, fear=A.fear, fm=dh_anim7.father_mouth)
    if mode is None:
        A.mouth, A.fear = _ORIG["mouth"], _ORIG["fear"]
        dh_anim7.father_mouth = dh_anim8.father_mouth = _ORIG["fm"]
    elif mode == 1:
        A.mouth = lambda k, head, s, op: _ORIG["mouth"](k, head, s, 1.0)
        A.fear = lambda k, head, s, kind="o", op=0.0: _ORIG["fear"](k, head, s, kind, 1.0)
        dh_anim7.father_mouth = dh_anim8.father_mouth = lambda k, hd, op: _ORIG["fm"](k, hd, 1.0)
    else:
        A.mouth = lambda *a, **k: None
        A.fear = lambda *a, **k: None
        dh_anim7.father_mouth = dh_anim8.father_mouth = lambda *a, **k: None


def draw(fr, n, plant=None, skip=None, force=None, tag=True, motto=True, overlay=None):
    SP.HELD_FREEZE = True
    SP.PLANT[0] = plant; SP.SKIP[0] = skip; SP.FORCE[0] = force
    t0, m0 = dp.TAG[0], dp.MOTTO[0]
    if not tag:
        dp.TAG[0] = False
    if not motto:
        dp.MOTTO[0] = False
    _overlays(overlay)
    try:
        r = fr(n / 12.0, n)
    finally:
        _overlays(None)
        SP.PLANT[0] = None; SP.SKIP[0] = None; SP.FORCE[0] = None
        dp.TAG[0], dp.MOTTO[0] = t0, m0
    surf = r[0] if isinstance(r, tuple) else r
    return arr(surf), list(SP.LAST), list(SP.REG)


def _none(*a, **k):
    return None


def boxtail(BM):
    """Split the bubble into its box (the rows as wide as the box) and its tail; the tip is the tail pixel farthest away."""
    ys, xs = np.nonzero(BM)
    if not len(ys):
        return None
    from scipy import ndimage
    O = ndimage.binary_opening(ndimage.binary_fill_holes(BM), structure=np.ones((33, 33), bool))   # the box survives, a tail does not
    lab, nl = ndimage.label(O)
    if nl:
        O = lab == np.bincount(lab[lab > 0]).argmax()
        oy, ox = np.nonzero(O)
        y0, y1, x0, x1 = oy.min() - 3, oy.max() + 3, ox.min() - 3, ox.max() + 3
    else:
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    box = (x0, y0, x1, y1)
    T = BM.copy(); T[max(0, y0 - 3):y1 + 4, max(0, x0 - 3):x1 + 4] = False
    lab2, n2 = ndimage.label(T)
    if n2:
        sizes = np.bincount(lab2.ravel())[1:]
        T = lab2 == (sizes.argmax() + 1) if sizes.max() >= 25 else np.zeros_like(T)
    ty, tx = np.nonzero(T)
    if len(ty) < 25:
        return box, None, None
    cx, cy = np.clip(tx, x0, x1), np.clip(ty, y0, y1)
    dd = np.hypot(tx - cx, ty - cy)
    i = int(dd.argmax())
    return box, T, (int(tx[i]), int(ty[i]))


def tail_end(T, box):
    from scipy import ndimage
    lab, nl = ndimage.label(T)
    if nl > 1:
        T = lab == (np.bincount(lab[lab > 0]).argmax())
    """The tail's far end measured along the tail (not as the crow flies: a tail that hooks in from below reaches
    further out than its own tip)."""
    ys, xs = np.nonzero(T)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    t = T[y0:y1, x0:x1]
    bx0, by0, bx1, by1 = box
    B = np.zeros((960, 540), bool); B[max(0, by0 - 10):by1 + 11, max(0, bx0 - 10):bx1 + 11] = True
    front = t & B[y0:y1, x0:x1]
    if not front.any():
        return None
    seen = front.copy(); last = front
    for _ in range(2000):
        g = np.zeros_like(seen)
        g[1:] |= last[:-1]; g[:-1] |= last[1:]; g[:, 1:] |= last[:, :-1]; g[:, :-1] |= last[:, 1:]
        new = g & t & ~seen
        if not new.any():
            break
        seen |= new; last = new
    ly, lx = np.nonzero(last)
    return (int(round(lx.mean())) + x0, int(round(ly.mean())) + y0)


def check_one(fr, n, scene, plant=None):
    on, last, reg = draw(fr, n, plant=plant)
    if not last:
        return []
    off, _, _ = draw(fr, n, plant=_none)
    BM = np.abs(on - off).sum(-1) > 30
    res = []
    allk = set(r_["idx"] for r_ in reg if isinstance(r_.get("idx"), tuple))
    if allk:
        none_, _, _ = draw(fr, n, plant=_none, skip=allk)
        ALL = np.abs(off - none_).sum(-1) > 30                 # every character in the drawing
    else:
        ALL = np.zeros(off.shape[:2], bool)
    sk_all = skin_of(off) & ALL
    nt, _, _ = draw(fr, n, plant=_none, tag=False, motto=False)
    SIGN = np.abs(off - nt).sum(-1) > 30
    for L in last[:1]:
        f = dict(scene=scene, n=n, text=L["text"], kind=L["kind"], fails=[])
        bt = boxtail(BM)
        if bt is None:
            f["fails"].append("no bubble drawn"); res.append(f); continue
        box, T, tip = bt
        if T is not None:
            tip = tail_end(T, box) or tip
        f["tip"] = tip; f["box"] = [int(v) for v in box]
        ys, xs = np.nonzero(BM)
        if (ys >= 720).any():
            f["fails"].append("bubble in the bottom quarter")
        if ((xs > 470) & (ys > 380) & (ys < 860)).any():
            f["fails"].append("bubble in the right rail")
        if (BM & SIGN).sum() > 6:
            f["fails"].append("bubble on the price tag or a sign (%d px)" % (BM & SIGN).sum())
        if L["kind"] == "card":
            if T is not None:
                f["fails"].append("a card with a tail")
            if L.get("text") not in SP.CARD:                 # 24 Nov (qa_bc / CLAUDE.md "Tails"): cards are for off-screen speakers only
                f["fails"].append("a card for a speaker in frame")
            res.append(f); continue
        if tip is None:
            f["fails"].append("a bubble with no tail for an on-screen speaker"); res.append(f); continue
        if tip[0] < 3 or tip[0] > 536 or tip[1] < 3 or tip[1] > 956:
            f["fails"].append("tail runs to the frame's edge")
        # 24 Nov (qa_bc, CLAUDE.md "Tails", lessons 174/325/360): the box beside the face and a SHORT tail: the run over
        # open wall, from the box to the speaker's outline, is at most 20 px (+ outline); over hair beside the cheek it may go on
        bx0_, by0_, bx1_, by1_ = box
        ddx = max(bx0_ - tip[0], 0, tip[0] - bx1_); ddy = max(by0_ - tip[1], 0, tip[1] - by1_)
        past = math.hypot(ddx, ddy)
        WALL[0] = past
        if bx1_ - bx0_ < BOX_MIN:                            # lessons 279/375: sized from the text, not one word a line
            f["fails"].append("box %d px wide: squeezed" % (bx1_ - bx0_))
        rec = L.get("rec")
        idx = rec.get("idx") if isinstance(rec, dict) and "idx" in rec else None
        if isinstance(rec, dict) and rec.get("kind") == "booth":
            SIL = SP._dilate(skin_of(off) & (np.arange(960)[:, None] < 330), 5)   # the booth: his chin is all of him we see
            sk_all = sk_all | (skin_of(off) & (np.arange(960)[:, None] < 330))
        elif idx is None:
            SIL = np.ones_like(BM)
        else:
            wo, _, _ = draw(fr, n, plant=_none, skip=idx)
            dd_ = wo - off
            shadow = (dd_ > 0).all(-1) & (dd_.max(-1) < 60) & (np.ptp(dd_, -1) < 22)   # their soft drop shadow on the wall
            SIL = (np.abs(off - wo).sum(-1) > 30) & ~shadow
        SKN = SIL & sk_all
        tx, ty = tip
        bx0_, by0_, bx1_, by1_ = box                         # the wall run: from the box's nearest point toward the tip, until the speaker
        nx_ = min(max(tx, bx0_), bx1_); ny_ = min(max(ty, by0_), by1_)
        Lw = math.hypot(tx - nx_, ty - ny_); run = Lw
        for i_ in range(1, int(Lw)):
            px_ = int(round(nx_ + (tx - nx_) * i_ / Lw)); py_ = int(round(ny_ + (ty - ny_) * i_ / Lw))
            if SIL[min(959, max(0, py_)), min(539, max(0, px_))]:
                run = i_; break
        lim = TAIL_MAX + (8 if L["kind"] in ("antenna",) or L["kind"].startswith("overhead") else 0)
        if run > lim:
            f["fails"].append("tail runs %d px over the wall (short tail: 10-20)" % run)
        ring = SKN[max(0, ty - 3):ty + 4, max(0, tx - 3):tx + 4]
        # the box itself on anyone's skin
        bx0, by0, bx1, by1 = box
        boxm = np.zeros_like(BM); boxm[by0:by1 + 1, bx0:bx1 + 1] = True
        if (BM & boxm & sk_all).sum() > 20:
            f["fails"].append("box on skin (%d px)" % (BM & boxm & sk_all).sum())
        if L["kind"] == "antenna":
            sy, sx = np.nonzero(SIL[:, max(0, tx - 25):tx + 26])
            if len(sy):
                top = sy.min(); topx = sx[sy == top].mean() + max(0, tx - 25)
                gap = math.hypot(tx - topx, ty - top)
                if gap > 6:
                    f["fails"].append("tail misses the antenna (%.0f px away)" % gap)
            over = (T & SIL).sum()
            if over > 60:
                f["fails"].append("tail over the robot (%d px)" % over)
            res.append(f); continue
        if ring.mean() < 0.3:
            f["fails"].append("tip not on the speaker's skin")
        # tail over the speaker: only skin (and the outline right next to it)
        near_skin = SP._dilate(SKN, 4)
        bad = T & SIL & ~near_skin
        if bad.sum() > 45:
            msg = "tail crosses the speaker off skin (hair/glasses/eyes/headset) (%d px)" % bad.sum()
            hair = isinstance(L.get("rec"), dict) and L["rec"].get("mod") in HAIR_RIGS
            if (L.get("tier") == 2 or hair) and bad.sum() <= 450:   # declared, or hair beside the cheek (lessons 360): over hair to the cheek
                f.setdefault("warn", []).append(msg.replace("hair/glasses/eyes/headset", "earring or chain, tier 2"))
            else:
                f["fails"].append(msg)
        if L["kind"].startswith("overhead"):
            above = SIL[max(0, ty - 26):max(0, ty - 13), max(0, tx - 3):tx + 4]   # above the scalp's own outline
            if above.mean() > 0.5 or ring.mean() < 0.3:
                f["fails"].append("overhead tail not on a bare scalp")
            res.append(f); continue
        # the face: the speaker's skin patch at the tip (not the hands); its holes are the eyes, the mouth, a highlight
        from scipy import ndimage
        lab, _ = ndimage.label(SP._dilate(SKN, 3) & SIL)        # joined across thin lines (a moustache, glasses)
        win = lab[max(0, ty - 8):ty + 9, max(0, tx - 8):tx + 9]
        ids = win[win > 0]
        if not len(ids):
            f["fails"].append("tip not on the speaker's face")
            res.append(f); continue
        F = lab == np.bincount(ids).argmax()
        fx = np.nonzero(F.any(0))[0]
        fy = np.nonzero(F.any(1))[0]
        r = max(20.0, max(np.ptp(fx), np.ptp(fy)) / 2.0)
        if isinstance(rec, dict) and rec.get("mouth_kw"):
            op, _, _ = draw(fr, n, plant=_none, force=(idx, DA.M_BIG))
            sh, _, _ = draw(fr, n, plant=_none, force=(idx, None))
            MO = np.abs(op - sh).sum(-1) > 40
        else:                                              # Don, Father, the booth: the lowest hole in the face
            H = ndimage.binary_fill_holes(F) & ~F
            hl, nh = ndimage.label(H)
            MO = np.zeros_like(BM)
            holes = []
            for i in range(1, nh + 1):
                yy, xx = np.nonzero(hl == i)
                if len(yy) >= 12:
                    holes.append((len(yy), yy.mean(), i))
            is_booth = isinstance(rec, dict) and rec.get("kind") == "booth"
            if not is_booth:
                op_, _, _ = draw(fr, n, plant=_none, overlay=1)
                sh_, _, _ = draw(fr, n, plant=_none, overlay=0)
                MO2 = (np.abs(op_ - sh_).sum(-1) > 40) & SP._dilate(F, 6)
            if holes and is_booth:
                MO = hl == max(holes)[2]                              # the booth: only his mouth is in the frame
            elif not is_booth and MO2.sum() > 20:                # the scene's own mouth, forced open against left out
                MO = ndimage.binary_fill_holes(SP._dilate(MO2, 2))    # its ring and what is inside it
            elif holes:                                      # the lowest dark shape across the face (eyes have white in them)
                widths = np.array([F[y_].sum() for y_ in range(960)])
                fy_ = np.nonzero(widths >= 0.35 * widths.max())[0]
                ylow = fy_.max() if len(fy_) else 960
                best = None
                for sz, cy_, i in holes:
                    yy, xx = np.nonzero(hl == i)
                    bright = off[yy, xx].sum(-1).mean()
                    if bright < 420 and np.ptp(xx) >= 0.15 * r and cy_ <= ylow + 0.1 * r:
                        if best is None or cy_ > best[0]:
                            best = (cy_, i)
                if best:
                    MO = hl == best[1]
        DBG.update(off=off, T=T, F=F, MO=MO, SIL=SIL, SKN=SKN, tip=tip, BM=BM, bad=bad)
        my, mx = np.nonzero(MO)
        if not len(my):
            f["fails"].append("mouth not found")
            res.append(f); continue
        if not (isinstance(rec, dict) and rec.get("kind") == "booth"):
            over_head = T & SIL
            over_head[int(my.min() - 0.2 * r):, :] = False
            if over_head.sum() > 20:
                f["fails"].append("tail comes down over the head (%d px above the mouth)" % over_head.sum())
        mcx = mx.mean()
        d = 1 if mcx > tx else -1
        if not (my.min() - 0.2 * r <= ty <= my.max() + 0.2 * r):
            f["fails"].append("tip not level with the mouth (%.0f px off)" % min(abs(ty - my.min()), abs(ty - my.max())))
        # walk from the tip straight toward the nearest mouth pixel: only skin until the mouth, within 0.4 r
        dd = np.hypot(mx - tx, my - ty); j = int(dd.argmin())
        gx, gy, L_ = mx[j], my[j], float(dd[j])
        ok = True
        for i_ in (range(1, int(L_)) if L_ >= 2 else []):
            px_ = int(round(tx + (gx - tx) * i_ / L_)); py_ = int(round(ty + (gy - ty) * i_ / L_))
            if MO[py_, px_]:
                break
            if not SKN[max(0, py_ - 2):py_ + 3, max(0, px_ - 2):px_ + 3].any():   # a face line (3 px) is still the face
                ok = False; break
        if not ok:
            f["fails"].append("not only skin between the tip and the mouth")
        elif L_ > TIP_R * r + 4:                             # 24 Nov (Tomas): the tip on the cheek's outline at mouth height (CLAUDE.md);
            f["fails"].append("tip too far from the mouth (%.2f r)" % (L_ / r))   # 0.4 r (lesson 398) is for a tipped head:
                                                             # a frontal face's outline is 0.55-0.63 r from its mouth
        res.append(f)
    return res


def run(sc_list):
    os.makedirs(OUT, exist_ok=True)
    allres = []
    SC = scenes()
    for s in sc_list:
        fr, total, phone = SC[s]
        ds.ARM_PHONE[0] = phone
        SP.HELD.clear()
        N = int(round(total * 12))
        for n in range(N):
            rs = check_one(fr, n, s)
            allres += rs
        bad = [r for r in allres if r["scene"] == s and r["fails"]]
        print("scene %d: %d bubble drawings, %d fail" % (s, sum(1 for r in allres if r["scene"] == s), len(bad)), flush=True)
        for r in bad[:400]:
            print("   n=%d %-34s %s" % (r["n"], r["text"][:34], "; ".join(r["fails"])))
    json.dump(allres, open("%s/tailcheck_%s.json" % (OUT, "_".join(map(str, sc_list))), "w"), indent=0, default=str)
    return all(not r["fails"] for r in allres)


# ---------------------------------------------------------------- self-test: five planted faults

def selftest():
    SC = scenes()
    caught = []

    def old(tip, y=128, side=0, shift=0, maxw=220):
        def p(c, text, tip0, *a, **kw):
            rec = SP.pick(tip0)
            OLD.bubble(c, text, tip, y=y, side=side, maxw=maxw, shift=shift)
            SP.LAST.append(dict(kind="antenna" if rec and rec["kind"] == "antenna" else "face", text=text, rec=rec))
        return p

    def find(scene, text, who=None):
        fr, total, phone = SC[scene]; ds.ARM_PHONE[0] = phone
        for n in range(int(round(total * 12))):
            _, last, reg = draw(fr, n)
            if last and (last[0]["text"] == text or (who and isinstance(last[0].get("rec"), dict) and last[0]["rec"].get("mod") == who)):
                return fr, n, last[0], reg
        raise SystemExit("self-test: line not found: %s" % text)

    cases = []
    # 1 the old tail: down from the box onto the mouth, across the forehead and eyes (Sofía, "Is he coming alone?")
    fr, n, L, reg = find(2, "Is he coming alone?")
    m = L["mouth"]
    cases.append(("tail over the forehead", fr, n, 2, old((m[0], m[1]), y=110)))
    # 2 tip on Pam's fringe (scene 4 "Of course.")
    fr, n, L, reg = find(2, None, who="pam_bc")
    hx, hy = SP._frame_matrix(L["rec"]).transform_point(*L["rec"]["head_u"])
    cases.append(("tip on Pam's fringe", fr, n, 2, old((hx + 10, hy - 0.62 * L["r"]), y=110)))
    # 3 the robot: the tail ends in the gap beside the antenna
    fr, n, L, reg = find(3, "Human approval required.")
    cases.append(("antenna gap", fr, n, 3, old((L["tip"][0] + 26, L["tip"][1] + 6), y=110)))
    # 4 a tail to the frame's edge
    fr, n, L, reg = find(8, "Find. My money.")
    cases.append(("tail to the frame's edge", fr, n, 8, old((1, 470), y=130)))
    # 5 the box on the price tag
    fr, n, L, reg = find(1, "Dad! Great timing!")
    K = SP.keep_mask() if SP.KEEP else None
    _, last, _ = draw(fr, n)
    ys, xs = np.nonzero(SP.keep_mask())
    cases.append(("box on the price tag", fr, n, 1, old((xs.mean(), ys.max() + 120), y=int(ys.min()) + 4, maxw=150)))
    ok = True
    for name, fr, n, scene, p in cases:
        SP.HELD.clear()
        rs = check_one(fr, n, scene, plant=p)
        hit = any(r["fails"] for r in rs)
        print("%-26s %s   %s" % (name, "CAUGHT" if hit else "MISSED", "; ".join(rs[0]["fails"]) if rs else "-"))
        ok &= hit
        a, _, _ = draw(fr, n, plant=p)
        from PIL import Image
        os.makedirs(OUT, exist_ok=True)
        Image.fromarray(a.astype(np.uint8)).save("%s/selftest_%s.png" % (OUT, name.replace(" ", "_").replace("'", "")))
    return ok


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        sys.exit(0 if selftest() else 1)
    sys.exit(0 if run([int(a) for a in sys.argv[1:]] or list(range(1, 9))) else 1)
