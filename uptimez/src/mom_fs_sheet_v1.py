"""MOM, "First Search" (episode 10): the look sheet v1 (mom_fs v3). Before (The Best Candidate: the interview
disguise) and after (the job is hers): the suit, the order, the bare curls and the curler; her two faces (sweet for
Pam and Don, the glare for Sofía and the robot); her desk.
python3 mom_fs_sheet.py [out_dir] -> fs_mom_v1.png"""
import os
import sys
import cairo
import kit
import brand
import mom_bc as mb
import mom_fs_v1 as mf                                 # pinned: look sheet v1
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
    corp(c, "MOM  ·  First Search  ·  look v1: the mask off", 40, 62, 34, brand.NAVY, True)
    wrap(c, "She came to the interview as a sweet old lady. Now the job is hers. The colours, the curls, the one "
            "forgotten curler and the glasses on the pearl chain stay, so you know her at once.", 40, 102, 19, 1000)
    labels = [("BEFORE", "The Best Candidate: the hat, the coat"), ("AFTER · sweet", "for Pam and Don"),
              ("AFTER · glare", "for Sofía and the robot")]
    for i, (fn, pose, face, look) in enumerate(((mb.mom, "bag", "sweet", (0, 0)), (mf.mom, "bag", "sweet", (0, 0)),
                                               (mf.mom, "hip", "glare", (-1, 0)))):
        x = 190 + i * 350
        fn(k, x, 690, 1.28, pose, face, look=look)
        corp(c, labels[i][0], x - 150, 740, 22, brand.NAVY, True)
        corp(c, labels[i][1], x - 150, 768, 17, (0.35, 0.35, 0.4))
    c.set_source_rgba(0, 0, 0, 0.25); c.set_line_width(2)
    c.move_to(365, 180); c.line_to(365, 780); c.stroke()
    head(k, 190, 960, 2.2, "sweet")
    head(k, 520, 960, 2.2, "glare", look=(-1, 0))
    corp(c, "sweet: eyes shut, a sugary smile", 50, 1140, 17, brand.NAVY, True)
    corp(c, "glare: over the frames, lips pressed", 375, 1140, 17, brand.NAVY, True)
    corp(c, "HER DESK", 720, 820, 22, brand.NAVY, True)
    mf.mug(k, 790, 900, 1.6)
    corp(c, "WORLD'S BEST MOM", 860, 900, 15, brand.NAVY, True)
    mf.candy(k, 790, 1010, 1.6)
    corp(c, "candy: for Pam only", 860, 1012, 15, brand.NAVY, True)
    mf.knitting(k, 780, 1110, 1.3)
    corp(c, "a scarf for Don", 860, 1120, 15, brand.NAVY, True)
    mf.order(k, 790, 1215, 2.0)
    corp(c, "the order (her brooch)", 860, 1222, 15, brand.NAVY, True)
    wrap(c, "Suit: boxy teal jacket, shoulder pads, mustard notched lapels and piping, two big buttons; darker teal "
            "pencil skirt; cream blouse to the top; plum lips.", 40, 1200, 17, 640)
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "fs_mom_v1.png")
    s.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
