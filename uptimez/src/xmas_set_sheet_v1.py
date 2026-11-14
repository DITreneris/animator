"""Set sheet for the Christmas special "Happy Compliance" (xmas_set.py) with the four characters, and 9:16
frames for the key shots: does everyone fit, and do faces read? Writes xmas_set_sheet_v1.png (2400x1560)."""
import sys
import cairo
import kit
import brand
import xmas_set_v1 as xs
import sofia_xmas as sx
import pam_xmas as px
import don_xmas as dx
import santa_robot_v2 as sr
from kit import Ctx, INK
from charsheets import corp
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)


def shot1(k):          # frame 0: Don in the doorway, mid-shave
    xs.set_dressing(k); xs.door(k, open_amt=1.0); xs.tree(k)
    px.pam(k, xs.POS["pam"], xs.FEET_BACK, 0.95, px.POSE_THERMOS, "neutral", look=(0.8, 0), thermos_in_hand=True)
    sx.sofia(k, xs.POS["sofia"], xs.FEET, 1.0, "hold2", "unimpressed", look=(0.9, 0))
    dx.don(k, xs.POS["don_door"], xs.FEET, 1.0, dx.POSE_RAZOR, "smug")


def shot1b(k):         # the alternative frame 0: Don alone in the doorway (the hook reads on a phone)
    xs.set_dressing(k); xs.door(k, open_amt=1.0); xs.tree(k)
    dx.don(k, xs.POS["don_door"], xs.FEET, 1.0, dx.POSE_RAZOR, "smug")


def shot2(k):          # Sofía and Pam stare
    xs.set_dressing(k); xs.tree(k)
    px.pam(k, 420, xs.FEET_BACK, 0.95, px.POSE_THERMOS, "neutral", look=(0.8, 0), thermos_in_hand=True)
    sx.sofia(k, 235, xs.FEET, 1.0, "hold2", "unimpressed", look=(0.9, 0))


def shot7(k):          # the robot points at Don
    xs.set_dressing(k); xs.door(k, open_amt=1.0)
    dx.don(k, 650, xs.FEET, 1.0, dx.POSE_CLUTCH, "shock", look=(-0.8, 0), razor_in_hand=False)
    sr.robot(k, 500, xs.FEET, 1.0, "detect", "stern", side=-1, alarm=True)


def shot8(k):          # the wide: censoring the tree
    xs.set_dressing(k); xs.tree(k, censored=(0, 1, 2, 3, 4))   # v1 sheet finding: Pam and Don cheated out
    sx.sofia(k, xs.POS["sofia"], xs.FEET, 1.0, "hold2", "horrified", look=(0.9, 0))
    sr.robot(k, 462, xs.FEET, 1.0, "slap_up", "stern", side=-1, bar="held")


def shot10(k):         # Pam: mask on, the hero
    xs.set_dressing(k); xs.tree(k, censored=tuple(range(8)))
    sx.sofia(k, 360, xs.FEET + 10, 1.0, "give", "knowing", look=(0.9, 0))
    px.pam(k, 480, xs.FEET, 1.0, px.POSE_HERO, "neutral", mask="down", **px.HERO)


SHOTS = [("1 as written: wide", shot1, (440, 470, 0.85)), ("1 proposed: Don", shot1b, (700, 560, 1.7)),
         ("2 · Sofía and Pam", shot2, (330, 570, 1.6)), ("7 · robot and Don", shot7, (575, 570, 1.6)),
         ("8 · tree, robot, Sofía", shot8, (325, 560, 1.3)), ("10 · Pam, the hero", shot10, (425, 570, 1.6))]


def frame(c, k, x, y, sc, cam, draw):
    c.save(); c.rectangle(x, y, 540 * sc, 960 * sc); c.clip()
    c.translate(x, y); c.scale(sc, sc); xs.with_cam(c, cam); draw(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE OFFICE, CHRISTMAS EVE", 68, 44, 28, bold=True)
    corp(c, "\"Happy Compliance\"  ·  Day One office wall, decorated  ·  one location", 500, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · SET SHEET · XMAS v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. the set, wide, empty but for the tree
    corp(c, "THE SET (WORLD VIEW)", 24, 92, 10, bold=True)
    c.save(); c.rectangle(24, 98, 470, 330); c.clip()
    c.translate(24, 98); c.scale(0.52, 0.52); c.translate(60, -60)
    shot1(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(24, 98, 470, 330); c.stroke()
    corp(c, "Sofía left of the tree, Pam behind on the right, Don and the robot come in through the door.", 24, 444, 9, col=GREY)

    # 2. the tree: clean and fully censored
    corp(c, "THE TREE: BEFORE  AND  AFTER", 24, 476, 10, bold=True)
    for i, cen in enumerate(((), tuple(range(8)))):
        x = 24 + i * 238
        boxed(c, x, 482, 230, 280, "8 ornaments, red and gold" if not cen else "every ball censored")
        c.save(); c.rectangle(x, 482, 230, 264); c.clip()
        c.set_source_rgb(*kit.WALL); c.rectangle(x, 482, 230, 264); c.fill()
        c.translate(x + 115 - xs.TREE_X * 0.62, 482 + 250 - xs.TREE_BASE * 0.62); c.scale(0.62, 0.62)
        xs.tree(k, censored=cen)
        c.restore()

    # 3. 9:16 frames
    corp(c, "9:16 FRAMES FOR THE KEY SHOTS  (does everyone fit; do faces read?)", 514, 92, 10, bold=True)
    sc = 0.205
    for i, (lab, fn, cam) in enumerate(SHOTS):
        x = 514 + i * 114
        frame(c, k, x, 98, sc, cam, fn)
        corp(c, lab, x, 98 + 960 * sc + 14, 9, col=GREY)

    # 4. notes
    corp(c, "NOTES", 514, 500, 10, bold=True)
    notes = ["Same wall, floor and UptimeZ sign as Day One: viewers know the place.",
             "One banner (MERRY CHRISTMAS TO ALL), string lights, tinsel, one sign. No more.",
             "\"0 days since last incident\" is a quiet gag; it is never pointed at.",
             "The tree is about Sofía's height; 8 big ornaments at fixed spots, red and gold.",
             "Censor bars sit on each ornament; on small balls the bar drops its lettering.",
             "Finding: in a 9:16 wide, faces are tiny. Wides carry action only; no face beats there.",
             "Proposal: open on Don alone in the doorway, so frame 0 reads on a phone.",
             "Shot 8 tighter: tree, robot and Sofía; Don's relief goes to shot 9.",
             "Pam stands slightly back (smaller, higher feet) to give the wide some depth."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 514, 524 + i * 24, 11, col=INK)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "xmas_set_sheet_v1.png")
