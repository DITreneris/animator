"""MOM, "First Search" (episode 10): the look sheet v2 (mom_fs_sheet_v1.py = v1, kept), after the design audit: the
switch acted by the whole body (sweet: leaning in, the candy out; real: fists, chin up, the glare; the switch in one
frame), a feed-size row. python3 mom_fs_sheet.py [out_dir] -> fs_mom_v2.png
MOM, "First Search" (episode 10): the look sheet v1 (mom_fs v3). Before (The Best Candidate: the interview
disguise) and after (the job is hers): the suit, the order, the bare curls and the curler; her two faces (sweet for
Pam and Don, the glare for Sofía and the robot); her desk.
python3 mom_fs_sheet.py [out_dir] -> fs_mom_v1.png"""
import os
import sys
import cairo
import kit
import brand
import mom_bc as mb
import mom_fs as mf
from charsheets import corp, wrap

W, H = 1080, 1350
BG = (0.95, 0.93, 0.88)


def head(k, cx, cy, s, face, look=(0, 0), fn=mf.mom):
    """A head close-up: the figure drawn large and clipped to a rounded box."""
    c = k.c
    c.save(); c.rectangle(cx - 150, cy - 150, 300, 300); c.clip()
    c.set_source_rgb(0.99, 0.98, 0.95); c.paint()
    fn(k, cx, cy - mb.HY * s + 10 * s, s, "stand", face, look=look)
    c.restore()
    c.set_source_rgb(*kit.INK); c.set_line_width(2); c.rectangle(cx - 150, cy - 150, 300, 300); c.stroke()


def main(d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(*BG); c.paint()
    corp(c, "MOM  ·  First Search  ·  look v2: the switch", 40, 62, 34, brand.NAVY, True)
    wrap(c, "Costume locked. The mask comes off in one frame, with the whole body: sugar for Pam and Don, ice for "
            "Sofía and the robot. She never thinks she is cruel: she is helping.", 40, 102, 19, 1000)
    figs = [("SWEET", "for Pam and Don: leans in, head tilted, the candy held out",
             dict(pose="offer", face="sweet", lean=-4, tilt=-12, candy_dish=True)),
            ("REAL", "for Sofía and the robot: fists, elbows out, chin up",
             dict(pose="fists", face="glare", look=(-1, 0.6), chin=True)),
            ("THE SWITCH", "the candy still out to Pam, the glare already on Sofía",
             dict(pose="offer", face="glare", look=(1, 0.6), chin=True, candy_dish=True))]
    for i, (t, sub, kw) in enumerate(figs):
        x = 200 + i * 340
        mf.mom(k, x, 640, 1.2, **kw)
        corp(c, t, x - 150, 690, 22, brand.NAVY, True)
        wrap(c, sub, x - 150, 716, 15, 290, (0.35, 0.35, 0.4))
    corp(c, "AT FEED SIZE (270 px wide frames)", 40, 812, 20, brand.NAVY, True)
    for i, (t, sub, kw) in enumerate(figs):
        tile = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        tc = cairo.Context(tile); tk = kit.Ctx(tc, 0)
        tc.set_source_rgb(*BG); tc.paint()
        mf.mom(tk, 270, 800, 1.5, **kw)
        c.save(); c.translate(40 + i * 150, 830); c.scale(0.25, 0.25); c.rectangle(0, 0, 540, 960); c.clip()
        c.set_source_surface(tile, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*kit.INK); c.set_line_width(1.5); c.rectangle(40 + i * 150, 830, 135, 240); c.stroke()
    head(k, 630, 990, 1.9, "sweet")
    corp(c, "sweet: eyes shut, sugar", 482, 1165, 16, brand.NAVY, True)
    head(k, 928, 990, 1.9, "glare", look=(-1, 0.6))
    corp(c, "glare: one brow down hard, one cocked", 780, 1165, 15, brand.NAVY, True)
    corp(c, "HER DESK", 40, 1110, 20, brand.NAVY, True)
    mf.mug(k, 80, 1190, 1.3); mf.candy(k, 190, 1195, 1.4); mf.knitting(k, 300, 1190, 1.15); mf.order(k, 430, 1185, 1.7)
    corp(c, "mug", 62, 1262, 14, brand.NAVY); corp(c, "candy: Pam only", 150, 1262, 14, brand.NAVY)
    corp(c, "scarf: DON", 280, 1262, 14, brand.NAVY); corp(c, "the order: she straightens it", 380, 1262, 14, brand.NAVY)
    corp(c, "when she asserts herself", 380, 1280, 14, brand.NAVY)
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "fs_mom_v2.png")
    s.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
