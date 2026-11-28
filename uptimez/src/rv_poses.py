"""Approved. (episode 16): the pose sandbox (Tomas 28 Nov: "Pose sandbox": new poses drawn here, silhouette-tested
(rules-hands-and-phones §0.2: three silhouettes at 270 px, two cold viewers) before any shot uses them; the canon rigs
don_ps / dh_cast / sofia_da / client_ps are imported, never edited, until the episode is done).

  don_seated(k, x, seat_y, floor_y, s, face, lean, arms)
      Don seated in the throne: don_ps's own rig, clipped above the belt (don_ps's `knee` method, 5.4), its belt set on
      the seat; under it new legs: the thighs toward us (short, foreshortened), the shins down to the floor, his shoes.
      Asleep = face "squint" (da_layouts' measure 27 Nov: "squint draws shut eyes: it reads as asleep") and a lean back
      about the belt. The arms rest on the armrests (relax, relax).
  python3 rv_poses.py sheet -> ../the-review/rv_poses_v1.png (the pose, its silhouette, at 540 and 270)
"""
import math
import sys
import cairo
from PIL import Image
import kit
import don_ps as dp
import don_v4 as dv
import ps_set as pss
import dh_cast as dc

EP = "../the-review/"
SHOE = (0.24, 0.18, 0.13)


def _cap(c, pts, t, col, lw=2.0):
    dp._cap(c, pts, t, col, lw)


def don_seated(k, x, seat_y, floor_y, s=0.60, face="squint", lean=-0.10, arms=(-18, -6, 18, 6), look=(0, 0.2),
               v=2):
    """v2 (28 Nov, the key-still review: "asleep only by the eyes", "the knees are two blocks hung on the belt", "the
    shoes melt into the base"): the top half leans further and to one side (asleep, not posed), his screen-right arm
    slips off the armrest and hangs (`quiet`); the thighs are foreshortened trapezoids widening toward us with round
    knee fronts; the shoes stand forward of the throne's base (lower in frame, nearer), a gap of floor between them and
    the casters. v=1 draws as before."""
    c = k.c
    w = dp.WAIST_Y
    vfeet = seat_y - w * s
    if v >= 2:
        lean, arms, look = -0.20, (-18, -6, 10, 2), (0.3, 0.5)
    c.save(); c.translate(x, seat_y); c.rotate(lean); c.translate(-x, -seat_y)
    c.save(); c.rectangle(x - 400, seat_y - 2000, 800, 2000 + 4 * s); c.clip()
    o = dp.don(k, x, vfeet, s, arms, face, look, hands=("relax", "quiet") if v >= 2 else ("relax", "relax"))
    c.restore()
    c.restore()
    c.save(); c.translate(x, seat_y); c.scale(s, s)
    fl = (floor_y - seat_y) / s
    if v < 2:
        for side in (-1, 1):
            hx = side * 22
            kx, ky = side * 26, 26
            ax, ay = side * 30, fl - 14
            _cap(c, [(hx, 2), (kx, ky)], 40, dv.KHAKI)
            _cap(c, [(kx, ky), (ax, ay)], 36, dv.KHAKI)
            kit.cut(k, [(ax - 24 + side * 6, fl - 16), (ax + 24 + side * 6, fl - 16), (ax + 26 + side * 6, fl),
                        (ax - 26 + side * 6, fl)], SHOE, shadow=False, lw=2)
        c.restore(); return o
    fwd = 10                                                 # the shoes a little nearer than the base
    for side in (-1, 1):                                     # the shins first: under the knees, in their shade
        ax = side * 30
        kit.cut(k, [(side * 14, 30), (side * 42, 30), (side * 42, fl + fwd - 16), (side * 18, fl + fwd - 16)],
                (0.62, 0.55, 0.40), shadow=False, lw=2)
        kit.cut(k, [(ax - 24, fl + fwd - 18), (ax + 24, fl + fwd - 18), (ax + 27, fl + fwd), (ax - 27, fl + fwd)],
                SHOE, shadow=False, lw=2)
    for side in (-1, 1):                                     # v2b: the thighs come AT us: two big round knees over the
        kit.cut(k, [(side * 2, -4), (side * 46, -4), (side * 52, 22), (side * 0, 22)], dv.KHAKI, shadow=False, lw=2)
        kit.ellipse(k, side * 27, 24, 28, 17, dv.KHAKI, 7 + side, shadow=False, lw=2.2)        # seat's edge
        c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(2.5)
        c.new_path(); c.arc(side * 27 - 6, 18, 9, math.pi * 1.1, math.pi * 1.6); c.stroke()  # the knee's light
    c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(0, fl + fwd + 1); c.scale(1, 0.18)
    c.new_path(); c.arc(0, 0, 70, 0, 2 * math.pi); c.restore(); c.fill()                        # their contact shadow
    c.restore()
    return o


def _with_throne(k, x, s):
    tx, tf, ts = pss.THRONE
    pss.throne(k)
    o = don_seated(k, tx, 742, tf, s)
    return o


def sheet(out=EP + "rv_poses_v2.png"):
    """1: the pose in the throne; 2: its silhouette (black on white: the §0.2 read); 3: the silhouette alone, at 270."""
    W, H = 540, 960
    tiles = []
    for mode in ("colour", "sil", "sil_alone"):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = cairo.Context(s); c.set_source_rgb(1, 1, 1); c.paint(); k = kit.Ctx(c, 0)
        c.save(); c.translate(270, 480); c.scale(1.7, 1.7); c.translate(-452, -700)
        if mode == "colour":
            _with_throne(k, 452, 0.60)
        else:
            lay = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); lc = cairo.Context(lay); lk = kit.Ctx(lc, 0)
            lc.translate(270, 480); lc.scale(1.7, 1.7); lc.translate(-452, -700)
            if mode == "sil":
                _with_throne(lk, 452, 0.60)
            else:
                don_seated(lk, 452, 742, 808, 0.60)
            c.restore()
            c.set_source_rgb(0, 0, 0); c.mask_surface(lay, 0, 0)
            c.save()
        c.restore()
        tiles.append(s)
    sheet_ = Image.new("RGB", (W * 3, H), (255, 255, 255))
    feed = Image.new("RGB", (W * 3 // 2, H // 2), (255, 255, 255))
    for i, t in enumerate(tiles):
        t.flush()
        im = Image.frombuffer("RGBA", (W, H), bytes(t.get_data()), "raw", "BGRA", 0, 1).convert("RGB")
        sheet_.paste(im, (i * W, 0)); feed.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    sheet_.save(out); feed.save(out.replace(".png", "_270.png"))
    print("wrote", out)


SPRAWL = {"A": dict(tilt=-0.90, hip=(470, 736), knee=(516, 704), foot=(540, 790), look=(-0.2, 0.4)),
          "B": dict(tilt=-0.60, hip=(466, 738), knee=(516, 704), foot=(546, 786), look=(0.0, -0.8)),
          "C": dict(tilt=-1.25, hip=(476, 734), knee=(518, 702), foot=(536, 796), look=(-0.4, 0.6))}


def don_sprawl(k, var="A", s=0.60, face="squint", report=False):
    """v3 premise (Tomas 28 Nov, after four rounds of the front-on seated pose read as "standing in front of the
    chair"): Don asleep ACROSS the throne, his back against its screen-left armrest, his legs over the screen-right
    one, the shins hanging outside it. don_ps's rig clipped above the belt and tilted about the hip; new legs. Hands:
    both `quiet` (rules-hands-and-phones, Jobs: At rest). report=True: the unread report lying on his belly."""
    c = k.c
    v = SPRAWL[var]
    hx, hy = v["hip"]
    w = dp.WAIST_Y
    kx, ky = v["knee"]; fx, fy = v["foot"]
    for d in (-1, 1):                                        # v3b (cold 2 of 2: "huge tube legs, not joined"): thinner,
        off = 0 if d > 0 else -9                             # drawn FIRST so the hip and the report cover their root
        col = dv.KHAKI if d > 0 else (0.62, 0.55, 0.40)
        _cap(c, [(hx - 14, hy - 4 + off * 0.3), (kx, ky + off)], 36 * s, col)
        _cap(c, [(kx, ky + off), (fx + off * 0.6, fy + off)], 31 * s, col)
        ax, ay = fx + off * 0.6, fy + off
        kit.cut(k, [(ax - 6, ay - 4), (ax + 20, ay - 2), (ax + 22, ay + 8), (ax - 8, ay + 7)], SHOE, shadow=False, lw=2)
    c.save(); c.translate(hx, hy); c.rotate(v["tilt"]); c.translate(-hx, -hy)
    c.save(); c.rectangle(hx - 400, hy - 2000, 800, 2000 + 4 * s); c.clip()
    o = dp.don(k, hx, hy - w * s, s, (-18, -6, 10, 2), face, v["look"], hands=("quiet", "quiet"))
    c.restore()
    if report:
        c.save(); c.translate(hx + 6, hy - 40 * s); c.rotate(-0.1); c.scale(1.0, 0.7)
        import rv_props as pr
        pr.report(k, 0, 0, 1.1); c.restore()
    c.restore()
    return o


def sprawl_sheet(out=EP + "rv_poses_v3.png"):
    """§0.2: the three variants in the throne (colour), then as black silhouettes, at 540 and 270."""
    W, H = 540, 960
    tiles = []
    for mode in ("colour", "sil"):
        for var in "ABC":
            sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            c = cairo.Context(sf); c.set_source_rgb(1, 1, 1); c.paint(); k = kit.Ctx(c, 0)
            def place(cc):
                cc.translate(270, 480); cc.scale(1.96, 1.96); cc.translate(-454, -756)
            if mode == "colour":
                c.save(); place(c); pss.throne(k); don_sprawl(k, var, report=True); c.restore()
            else:
                lay = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); lc = cairo.Context(lay); lk = kit.Ctx(lc, 0)
                tl = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); tc = cairo.Context(tl); tk = kit.Ctx(tc, 0)
                place(tc); pss.throne(tk)
                c.set_source_rgb(0.80, 0.80, 0.80); c.mask_surface(tl, 0, 0)   # the throne pale: Don's shape alone
                place(lc); don_sprawl(lk, var, report=True)
                c.set_source_rgb(0, 0, 0); c.mask_surface(lay, 0, 0)
            tiles.append(sf)
    sheet_ = Image.new("RGB", (W * 3, H * 2), (255, 255, 255))
    for i, t in enumerate(tiles):
        t.flush()
        im = Image.frombuffer("RGBA", (W, H), bytes(t.get_data()), "raw", "BGRA", 0, 1).convert("RGB")
        sheet_.paste(im, ((i % 3) * W, (i // 3) * H))
    sheet_.save(out); sheet_.resize((W * 3 // 2, H)).save(out.replace(".png", "_270.png"))
    print("wrote", out)


# ---- Act I layout round 2 (Tomas 28 Nov "Ieskom" -> "Tesk"): three poses REUSED from approved films, silhouette-tested
# before any shot uses them (rules-hands-and-phones §0.2). Jobs (§ Jobs table): Don's cup = Holding a thing (on a palm:
# episode 15's cups canon, SAUCER_SUPPORT); Father's hands = At rest (quiet); the Client's hands = Holding a thing (grab),
# at the chair's short leg.
def don_on_back(k, x, floor, s=0.60, var="A", cup=True, arm=(-8, 0, 92, 2), cup_k=1.0):
    """1.2: Don flat on his back, head to screen left. The front rig turned a quarter (garage_on3's sofa, Office Noir 3)
    and clipped at the belt (don_seated's method); his legs drawn lying: khaki thighs and shins to screen right, the
    shoes toe-up (episode 15's shoe). The empty cup and saucer stand on his raised palm (episode 15's cups canon, on a
    palm). A: legs straight; B: the near knee up; C: A with the chin on the chest (still asleep)."""
    import da_cups as cups
    import don_v4 as dv
    cups.install()
    c = k.c
    a = -math.pi / 2
    w = dp.WAIST_Y                                          # -98: the belt above the feet, rig units
    hip_x = x                                               # (x, floor): the floor under his belt
    feet_x = hip_x - w * s                                  # the virtual feet, turned: to screen right of the belt
    lift = 10 * s                                           # his back's thickness off the floor
    oy = floor - lift
    c.save(); c.translate(feet_x, oy); c.rotate(a); c.translate(-feet_x, -oy)
    c.save(); c.rectangle(feet_x - 400, oy - 2000, 800, 2000 + w * s + 2); c.clip()
    o = dp.don(k, feet_x, oy, s, arm, "squint", (0, 0.4 if var == "C" else 0), hands=("quiet", "relax"))
    c.restore(); c.restore()
    def r(px, py):
        dx, dy = px - feet_x, py - oy
        return (feet_x + dx * math.cos(a) - dy * math.sin(a), oy + dx * math.sin(a) + dy * math.cos(a))
    # the legs, lying: from the belt (hip_x) to screen right; the far leg a shade darker, a touch higher
    SHOE = (0.24, 0.18, 0.13)
    hy = oy - 4 * s
    for d, col in ((-1, (0.66, 0.60, 0.48)), (1, dv.KHAKI)):
        y0 = hy + d * 13 * s
        if var == "B" and d == 1:
            kx, ky = hip_x + 70 * s, y0 - 54 * s            # the knee up
            fx, fy = hip_x + 128 * s, oy - 6 * s
            dp._cap(c, [(hip_x, y0), (kx, ky)], 30 * s, col); dp._cap(c, [(kx, ky), (fx, fy)], 27 * s, col)
        else:
            fx, fy = hip_x + 150 * s, y0
            dp._cap(c, [(hip_x, y0), (fx, fy)], 30 * s, col)
        kit.cut(k, [(fx - 2 * s, fy - 24 * s), (fx + 12 * s, fy - 22 * s), (fx + 14 * s, fy + 12 * s),
                    (fx - 2 * s, fy + 12 * s)], SHOE, shadow=False, lw=2)          # the shoe, toe up
    hx, hy_ = r(*o["head"][:2])
    if cup:
        px, py = r(*o["hands"][1])                          # the raised hand, as the rig drew it
        cups.cup_saucer(k, px, py - 6 * s, cups.CUP_FLOOR * s / 0.6 * cup_k, state="held")
    return dict(head=(hx, hy_))


def father_folding(k, x, floor, s, var="A", lean_side=0.0, chair_s=0.9, look=(0.5, 0.1), head_level=False,
                   arms=(-30, 26, 30, -26), hands=("quiet", "quiet")):
    """1.6: Father on the folding chair. REUSED: da_sheets.feet_up (episode 15, from dh_poses.don_seated): his rig
    clipped at the seat, leaning back, the legs in his black out to screen right with a knee and a shoe. Here the feet
    stay on the floor. A: knees out to screen right, the shins down (sitting, three-quarter); B: the legs crossed at the
    knee, the top shin out (at ease, the owner); C: A with lean_side (he leans hard to test the chair)."""
    import rv_props as pr
    import da_sheets as dsh
    c = k.c
    seat_y = floor - 70 * chair_s
    pr.folding_chair(k, x, floor, chair_s, "open")
    waist = -98 * 1.12
    vfeet = seat_y - waist * s
    lean = -0.06 + lean_side
    import hands_ps as hp
    neck = vfeet + (-300 * 1.12 + 78 + 2) * s               # dh_cast's neck line (FATHER_NOD's two passes)
    c.save(); c.translate(x, seat_y); c.rotate(lean); c.translate(-x, -seat_y)
    c.save(); c.rectangle(x - 400, (neck if head_level else seat_y - 2000), 800,
                          (seat_y + 2 - neck) if head_level else 2000 + 2); c.clip()
    hp.reset(*hands)
    o = dc.father(k, x, vfeet, s, pose=arms, look=look)
    c.restore(); c.restore()
    if head_level:                                          # the head kept level over the leaning body (v2, 1.6: a
        dx, dy = 0.0, neck - seat_y                         # tilted head read as fainting 2/2): the neck point turned,
        nx = x + dx * math.cos(lean) - dy * math.sin(lean)  # the head drawn there unturned
        ny = seat_y + dx * math.sin(lean) + dy * math.cos(lean)
        c.save(); c.translate(nx - x, ny - neck); c.rectangle(x - 400, neck - 2000, 800, 2000); c.clip()
        hp.reset(*hands)
        o2 = dc.father(k, x, vfeet, s, pose=arms, look=look)
        c.restore()
        hx, hy = o2["head"][:2]
        return dict(head=(hx + nx - x, hy + ny - neck))
    # the legs (feet_up's line): hip -> knee (out to screen right, a little down) -> ankle (down to the floor)
    c.save(); c.translate(x, seat_y); c.scale(s, s)
    fl = (floor - seat_y) / s
    if var == "B":
        legs = [([(-8, -4), (70, 6), (70, fl - 14)], 1), ([(10, -8), (78, -10), (128, fl - 60)], 2)]
    else:
        legs = [([(-6, -4), (62, 4), (64, fl - 14)], 1), ([(12, -6), (84, 0), (92, fl - 14)], 2)]
    for pts, sd in legs:
        for (a_x, a_y), (b_x, b_y) in zip(pts, pts[1:]):
            an = math.atan2(b_y - a_y, b_x - a_x); nx, ny = -math.sin(an) * 15, math.cos(an) * 15
            kit.cut(k, [(a_x + nx, a_y + ny), (b_x + nx, b_y + ny), (b_x - nx, b_y - ny), (a_x - nx, a_y - ny)],
                    dc.BLACK, shadow=False, lw=2)
        kx, ky = pts[1]
        kit.ellipse(k, kx, ky, 15, 15, dc.BLACK, 4700 + sd, shadow=False, lw=2)
        ax, ay = pts[2]
        kit.cut(k, [(ax - 12, ay + 2), (ax + 26, ay + 4), (ax + 28, ay + 14), (ax - 14, ay + 14)], (0.05, 0.05, 0.06),
                shadow=False, lw=2)                          # the shoe, toe to screen right
    c.restore()
    hx, hy = o["head"][:2]
    dx, dy = hx - x, hy - seat_y
    return dict(head=(x + dx * math.cos(lean) - dy * math.sin(lean), seat_y + dx * math.sin(lean) + dy * math.cos(lean)))


def client_fix(k, x, floor, s, target, var="A"):
    """1.5: the Client at the chair's short leg. REUSED: client_of.profile (The Offer, approved: the true side view; lean
    0.6 'over an engine'), facing screen left, both hands at the leg (target). A: lean 0.7; B: lean 1.0; C: lean 1.25."""
    import client_of as cof
    lean = {"A": 0.7, "B": 1.0, "C": 1.25}[var]
    return cof.profile(k, x, floor, s, facing=-1, lean=lean, face="bored", hands=[target, (target[0] + 6, target[1] - 8)])


def act1_sheet(out=EP + "rv_poses_v4.png"):
    """§0.2: the three poses x three variants, colour then silhouette (the furniture pale), at 540 and 270."""
    import rv_props as pr
    W, H = 540, 540
    rows = []
    def tile(mode, fn):
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = cairo.Context(sf); c.set_source_rgb(1, 1, 1); c.paint(); k = kit.Ctx(c, 0)
        def place(cc):
            cc.translate(270, 300); cc.scale(1.6, 1.6); cc.translate(-560, -760)
        if mode == "colour":
            c.save(); place(c); fn(k, True); c.restore()
        else:
            for col, people in (((0.80, 0.80, 0.80), False), ((0, 0, 0), True)):
                lay = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); lc = cairo.Context(lay); lk = kit.Ctx(lc, 0)
                place(lc); fn(lk, people)
                c.set_source_rgb(*col); c.mask_surface(lay, 0, 0)
        return sf
    F0 = 808
    def don_fn(var):
        def f(k, people):
            if people:
                don_on_back(k, 580, F0, 0.60, var)
        return f
    def father_fn(var):
        def f(k, people):
            if people:
                father_folding(k, 540, F0, 0.60 * 1.12 / 1.12 * 0.97, var, lean_side=(-0.22 if var == "C" else 0.0))
            else:
                pr.folding_chair(k, 540, F0, 0.9, "open")
        return f
    def client_fn(var):
        def f(k, people):
            pr.folding_chair(k, 520, F0, 0.9, "wobble")
            if people:
                client_fix(k, 630, F0, 0.52, (556, F0 - 6), var)
                pr.washer(k, 556, F0 - 4, 0.9)
        return f
    for fn in (don_fn, father_fn, client_fn):
        rows.append([tile(m, fn(v)) for m in ("colour",) for v in "ABC"] + [tile("sil", fn(v)) for v in "ABC"])
    sheet_ = Image.new("RGB", (W * 6, H * 3), (255, 255, 255))
    for r_, row in enumerate(rows):
        for i, t in enumerate(row):
            t.flush()
            im = Image.frombuffer("RGBA", (W, H), bytes(t.get_data()), "raw", "BGRA", 0, 1).convert("RGB")
            sheet_.paste(im, (i * W, r_ * H))
    sheet_.save(out); sheet_.resize((W * 3, H * 3 // 2)).save(out.replace(".png", "_270.png"))
    sil = Image.new("RGB", (W * 3, H * 3), (255, 255, 255))
    for r_ in range(3):
        sil.paste(sheet_.crop((W * 3, r_ * H, W * 6, (r_ + 1) * H)), (0, r_ * H))
    sil.resize((W * 3 // 2, H * 3 // 2)).save(out.replace(".png", "_sil_270.png"))
    print("wrote", out)


if __name__ == "__main__":
    {"sheet": sheet, "sprawl": sprawl_sheet, "act1": act1_sheet}[sys.argv[1]]()
