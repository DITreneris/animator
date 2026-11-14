"""Santa robot model sheet for the Christmas special "Happy Compliance" (santa_robot.py on waiter_kit.py).
Writes santa_robot_sheet_v1.png at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import waiter_kit as w
import santa_robot_v2 as sr
import sofia_xmas as sx
import pam_xmas as px
import don_xmas as dx
from kit import Ctx, INK
from charsheets import corp, wrap
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.86, 0.92, 0.90)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "ROBOT, PROMOTED TO HR", 68, 44, 28, bold=True)
    corp(c, "Christmas special \"Happy Compliance\"  ·  enforces policy, not sense", 470, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · XMAS v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    c.save(); c.rectangle(24, 80, 240, 450); c.clip()
    sr.robot(k, 144, 505, 1.3, "stand", "eager", seed=71)
    c.restore()
    corp(c, "FRONT · EAGER", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. before / after and the cast
    corp(c, "LAST EPISODE  AND  NOW, WITH THE CAST", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    w.robot(k, 322, 296, 0.5, "stand", "eager", seed=72)
    sr.robot(k, 384, 296, 0.5, "stand", "proud", seed=72)
    dx.don(k, 454, 296, 0.5, dx.POSE_RAZOR, "smug", seed=74)
    sx.sofia(k, 520, 296, 0.5, "hold2", "unimpressed", seed=73)
    px.pam(k, 582, 296, 0.5, px.POSE_THERMOS, "neutral", thermos_in_hand=True, seed=75)
    c.restore()
    corp(c, "Body, wheel, screen faces and bow tie unchanged; hat, beard, HR badge added.", 290, 322, 9, col=GREY)

    # 3. screen faces under the hat
    corp(c, "SCREEN FACES  (hat and beard never cover the eyes or mouth)", 284, 348, 10, bold=True)
    for i, (f, lab, alarm, talk) in enumerate([("eager", "eager", False, 0), ("stern", "\"detected\"", True, 0.6),
                                                ("smug", "\"resolved\" (smug, new)", False, 0), ("proud", "\"Happy compliance!\"", False, 0.7),
                                                ("blink", "screen blink", False, 0), ("proud", "proud", False, 0)]):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, lab, fill=(1, 0.99, 0.97) if f != "stern" else (0.99, 0.93, 0.92))
        c.save(); c.rectangle(x, y, 106, 70); c.clip()
        sr.robot(k, x + 50, y + 162, 0.5, "stand", f, alarm=alarm, talk=talk, seed=80 + i)
        c.restore()

    # 4. action poses in story order
    corp(c, "ACTION POSES", 634, 92, 10, bold=True)
    poses = [("travel", "eager", True, None, 1, "shot 6: enters, siren"),
             ("detect", "stern", True, None, -1, "shot 7: \"detected\""),
             ("slap_up", "stern", False, "held", 1, "8a: bar up"),
             ("slap", "stern", False, "on", 1, "8b: contact"),
             ("stand", "smug", False, None, 1, "8c: hand away, it stays")]
    for i, (p, f, alarm, bar, sd, lab) in enumerate(poses):
        x = 634 + i * 110
        boxed(c, x, 98, 104, 210, lab)
        c.save(); c.rectangle(x, 98, 104, 194); c.clip()
        sr.robot(k, x + (16 if p == "slap" else (24 if f == "smug" and p == "stand" else (34 if p == "slap_up" else 52))), 286, 0.5, p, f, side=sd, alarm=alarm, bar=bar,
                 talk=0.6 if p == "present" else 0, seed=90 + i)
        if p == "stand" and f == "smug":                 # the bar left behind on the ornament
            sx.ornament(k, x + 84, 222, 10, 7); sr.censor_bar(k, x + 84, 222, 28, 8.5, rot=-0.08, label=False)
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "pompom = antenna light (red = alarm)")
    c.save(); c.rectangle(634, 354, 170, 162); c.clip()
    sr.robot(k, 700, 745, 1.2, "stand", "stern", alarm=True)
    c.restore()
    boxed(c, 812, 354, 170, 178, "big HR badge (reads in the wide)")
    c.save(); c.rectangle(812, 354, 170, 162); c.clip()
    sr.robot(k, 897, 640, 1.2, "stand", "eager")
    c.restore()
    boxed(c, 990, 354, 186, 178, "censor bar on an ornament")
    sx.ornament(k, 1050, 438, 34, 5)
    sr.censor_bar(k, 1050, 438, 80, 24)
    sx.ornament(k, 1130, 446, 22, 6)
    sr.censor_bar(k, 1130, 446, 52, 16, rot=-0.15)

    # 6. phone-size check
    corp(c, "PHONE-SIZE CHECK  (as small as it gets in the wide shot, on the wall colour)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(24, 722, 590, 30); c.fill()
    for i, (p, f, alarm, bar, sd) in enumerate((("travel", "eager", False, None, 1), ("detect", "stern", True, None, -1),
                                                 ("slap", "stern", False, "on", 1), ("present", "smug", False, None, 1))):
        sr.robot(k, 100 + i * 140, 736, 0.5, p, f, side=sd, alarm=alarm, bar=bar, seed=95 + i)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Same robot as \"I Will Replace You\": promoted, so a big badge now reads HR.",
             "Santa hat over the screen; the pompom is the antenna light, red when it detects.",
             "Cotton beard hooked under the screen, stopping above the bow tie.",
             "A 0.3 s still beat after \"Nice balls\", then red eyes, alarm lines, the rigid point.",
             "Smug face on \"Violation resolved.\": delighted with the wrong solution.",
             "It points at Don, then rolls straight past him to the tree.",
             "Slap: bar up, contact (impact ticks), hand away, bar stays. Three, then a cascade."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "santa_robot_sheet_v2.png")
