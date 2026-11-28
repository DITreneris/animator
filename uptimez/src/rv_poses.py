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


if __name__ == "__main__":
    {"sheet": sheet, "sprawl": sprawl_sheet}[sys.argv[1]]()
