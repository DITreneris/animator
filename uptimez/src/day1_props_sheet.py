"""Model sheet for the robot and the coffee maker ("How Sofía Survived Day One"). Writes props_sheet.png (2400x1560)."""
import sys
import cairo
import kit
import brand
import pt42
import day1_kit as dk
from kit import Ctx
from charsheets import corp, wrap
from sofia_sheet import boxed, flush_labels, GREY

W2, H2 = 1200, 780


def seated_don(k, x, feet, s, pose="stand", face="smug", look=(0, 0)):
    """Don behind a desk: the desk front hides everything below its top (feet - 130*s)."""
    p = pt42.branded_person(k, "DON", x, feet, s, pose=pose, face=face, look=look, seed=500)
    kit.desk(k, x - 110 * s, feet - 130 * s, 220 * s, 501)
    kit.rect(k, x - 104 * s, feet - 104 * s, 208 * s, 104 * s, (0.55, 0.40, 0.28), 502)
    return p


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "ROBOT  +  COFFEE MAKER", 68, 44, 26, bold=True)
    corp(c, "\"How Sofía Survived Day One\"", 410, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    tw = c.text_extents("UPTIMEZ INC. · MODEL SHEET · v1").x_advance
    corp(c, "UPTIMEZ INC. · MODEL SHEET · v1", W2 - 24 - tw, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. framing A check: robot head level with seated Don's head
    corp(c, "FRAMING A: HEADS LEVEL", 24, 92, 10, bold=True)
    boxed(c, 24, 98, 420, 330, "the robot's screen sits at Don's seated head height, so one camera fits both")
    c.save(); c.rectangle(24, 98, 420, 316); c.clip()
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 98, 420, 316); c.fill()
    seated_don(k, 160, 410, 0.82, face="smug")
    dk.robot(k, 330, 410, 0.82, "stand", look=(-0.6, 0))
    hy = 410 - 302 * 0.82
    c.set_source_rgb(0.85, 0.2, 0.2); c.set_line_width(1.2); c.set_dash([5, 4])
    c.move_to(30, hy); c.line_to(438, hy); c.stroke(); c.set_dash([])
    c.restore()

    # 2. robot poses
    corp(c, "ROBOT: POSES", 464, 92, 10, bold=True)
    for i, (ps, ey, lk, lbl) in enumerate([("stand", "neutral", (0, 0), "stand"), ("tug", "neutral", (0, 0), "tie tug (copies Don)"),
                                            ("wave", "neutral", (0.8, 0), "the wave + tilt: \"Pam?\""),
                                            ("hold", "neutral", (-0.5, 0.2), "17:00 with a paper")]):
        x = 464 + i * 180
        boxed(c, x, 98, 172, 230, lbl)
        c.save(); c.rectangle(x, 98, 172, 214); c.clip()
        dk.robot(k, x + 86, 306, 0.6, ps, ey, look=lk, tilt=0.12 if ps == "wave" else 0, paper=ps == "hold",
                 talk=0.6 if ps == "wave" else 0)
        c.restore()

    # 3. robot screen faces
    corp(c, "ROBOT: SCREEN FACES", 464, 352, 10, bold=True)
    for i, (ey, lk, lbl) in enumerate([("neutral", (0, 0), "neutral"), ("neutral", (-1, 0), "watching Don"),
                                        ("wide", (0, 0), "wide"), ("happy", (0, 0), "happy"), ("flat", (0, 0), "flat")]):
        x = 464 + i * 144
        boxed(c, x, 358, 136, 110, lbl)
        c.save(); c.rectangle(x, 358, 136, 94); c.clip()
        dk.robot(k, x + 68, 358 + 52 + 302 * 0.62, 0.62, "stand", ey, look=lk)
        c.restore()

    # 4. coffee maker states
    corp(c, "COFFEE MAKER: STATES", 24, 452, 10, bold=True)
    for i, (st, pr, ov, lbl) in enumerate([("waiting", 0, 0, "9:00 waiting"), ("approved", 0.5, 0, "17:00 approved, pouring"),
                                            ("approved", 1.0, 1.0, "17:00 overflow")]):
        x = 24 + i * 142
        boxed(c, x, 458, 136, 190, lbl)
        c.save(); c.rectangle(x, 458, 136, 174); c.clip()
        dk.counter(k, x + 4, x + 132, 600)
        dk.coffee_maker(k, x + 68, 600, 0.85, st, pour=pr, overflow=ov)
        c.restore()

    # 5. railway + train
    corp(c, "RAILWAY + APPROVE TRAIN", 464, 492, 10, bold=True)
    boxed(c, 464, 498, 300, 150, "button rides a tall pedestal to desk-top height")
    c.save(); c.rectangle(464, 498, 300, 134); c.clip()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(464, 498, 300, 134); c.fill()
    dk.railway(k, 614, 600, 130, 26, front=False)
    dk.railway(k, 614, 600, 130, 26, front=True)
    dk.train(k, 614, 600, 130, 26, 1.2, button_y=540)
    c.restore()
    corp(c, "PAM'S THERMOS + MUG", 784, 492, 10, bold=True)
    boxed(c, 784, 498, 160, 150, "thermos, mug")
    c.save(); c.rectangle(784, 498, 160, 134); c.clip()
    dk.thermos(k, 830, 610, 1.2); dk.mug(k, 900, 610, 1.4, steam=1)
    c.restore()

    wrap(c, "Robot: waist-high, on wheels, screen face, tiny red tie, long arms (60 + 60) so Don's lazy wave reads "
            "at phone size. It copies Don's poses exactly: tie tug, the wave with a head tilt. Its lines are made "
            "from Don's and Sofía's takes, pitched up.", 24, 684, 11, 560)
    wrap(c, "Coffee maker: the office in one appliance. Screen text 13-17 px at sheet scale = 28 px or more in the "
            "film's 540 frame. Sticker \"99.9% UPTIME\" is the brand joke; the 17:00 overflow is the closing gag.",
         620, 684, 11, 560)
    corp(c, "Drawn with day1_kit.py, the same code the film will use.", 24, 762, 9, col=GREY)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "props_sheet.png")
