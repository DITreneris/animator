"""DON model sheet for the Christmas special "Happy Compliance" (don_xmas.py). Writes don_sheet_xmas_v1.png
at 2400x1560 (drawn at 1200x780, 2x). The v4 office look (don_v4.py) is shown beside it."""
import sys
import cairo
import kit
import brand
import pt42
import don_v4 as dv
import don_xmas_v1 as dx
import sofia_xmas as sx
from kit import Ctx, INK
from charsheets import corp, wrap
from sofia_sheet_v4 import boxed, flush_labels

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.80, 0.86, 0.93)
HY = -300 * kit.PEOPLE["DON"]["h"] + 78 - 44


def head_at(k, cx, cy, s, face, look=(0, 0)):
    dx.don(k, cx, cy - HY * s, s, "stand", face, look=look, razor_in_hand=False)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "DON", 68, 44, 28, bold=True)
    corp(c, "Christmas special \"Happy Compliance\"  ·  walks into the party mid-shave", 140, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · XMAS v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front: the entrance
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    c.save(); c.rectangle(24, 80, 240, 450); c.clip()
    dx.don(k, 150, 512, 1.12, dx.POSE_RAZOR, "smug", seed=71)
    c.restore()
    corp(c, "FRONT · THE ENTRANCE (FRAME 0)", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. office look and costume, with Sofía for height
    corp(c, "OFFICE LOOK (v4)  AND  COSTUME, WITH SOFÍA", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    dv.don(k, 350, 296, 0.6, seed=74)
    dx.don(k, 450, 296, 0.6, "stand", "smug", seed=74, razor_in_hand=False)
    sx.sofia(k, 548, 296, 0.6, "hold2", "unimpressed", look=(-0.8, 0), seed=73)
    c.restore()
    corp(c, "Same head, face and height (1.12). Badge stays on, even on the robe.", 290, 322, 9, col=GREY)

    # 3. expressions (foam on, mouth always clear for the lip-sync)
    corp(c, "EXPRESSIONS  (the foam never covers his mouth)", 284, 348, 10, bold=True)
    for i, (e, lk) in enumerate([("neutral", (0, 0)), ("smug", (0.6, 0.4)), ("happy", (0, 0)),
                                 ("grin", (0, 0)), ("shock", (0, 0)), ("confused", (0.4, 0))]):
        x, y = 284 + (i % 3) * 112, 354 + (i // 3) * 92
        boxed(c, x, y, 106, 86, e, fill=(1, 0.99, 0.97) if e != "smug" else (0.93, 0.95, 0.98))
        c.save(); c.rectangle(x, y, 106, 70); c.clip()
        head_at(k, x + 53, y + 34, 0.46, e, look=lk)
        c.restore()

    # 4. poses, in story order
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(dx.POSE_RAZOR, "smug", "shot 1: \"the ball\"", True, (0, 0)),
             (dx.POSE_HIPS, "smug", "shot 4: \"Nice balls\"", True, (0.6, 0.5)),
             (dx.POSE_CLUTCH, "shock", "shot 7: panic", False, (0, 0)),
             (dx.POSE_THUMB, "grin", "shot 9: relief", False, (0, 0)),
             ("stand", "confused", "shot 10: smile drops", True, (-0.6, 0))]
    for i, (ps, fk, lbl, rz, lk) in enumerate(poses):
        x = 634 + i * 110
        boxed(c, x, 98, 104, 210, lbl)
        c.save(); c.rectangle(x, 98, 104, 194); c.clip()
        o = dx.don(k, x + 56, 286, 0.5, ps, fk, look=lk, seed=80 + i, razor_in_hand=rz)
        if fk == "grin":
            dv.thumbs_up(k, o["hands"][1], 0.5)
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "foam: one stroke shaved through")
    c.save(); c.rectangle(634, 354, 170, 162); c.clip()
    head_at(k, 719, 440, 1.25, "smug")
    c.restore()
    boxed(c, 812, 354, 170, 178, "boxers, hairy shins, socks, slippers")
    c.save(); c.rectangle(812, 354, 170, 162); c.clip()
    dx.don(k, 897, 512, 1.1, "stand", "neutral", razor_in_hand=False)
    c.restore()
    boxed(c, 990, 354, 186, 178, "undershirt: tuft, ketchup; badge on robe")
    c.save(); c.rectangle(990, 354, 186, 162); c.clip()
    dx.don(k, 1083, 700, 1.15, "stand", "neutral", razor_in_hand=False)
    c.restore()

    # 6. phone-size check on the wall colour
    corp(c, "PHONE-SIZE CHECK  (as small as he gets in the wide shot, on the wall colour)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(24, 722, 590, 30); c.fill()
    for i, (ps, fk, rz) in enumerate(((dx.POSE_RAZOR, "smug", True), (dx.POSE_HIPS, "smug", True),
                                      (dx.POSE_CLUTCH, "shock", False), (dx.POSE_THUMB, "grin", False))):
        o = dx.don(k, 100 + i * 140, 736, 0.4, ps, fk, seed=95 + i, razor_in_hand=rz)
        if fk == "grin":
            dv.thumbs_up(k, o["hands"][1], 0.4)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Navy robe matches his fleece vest; UptimeZ mark on the chest pocket.",
             "Ribbed undershirt with the ketchup squiggle: always there, never mentioned.",
             "Red heart boxers, hairy shins, white socks, fuzzy slippers. Robe open at the chest only.",
             "Foam on his right cheek and half the chin; mouth always clear for the lip-sync.",
             "Razor in his left hand on the entrance and the line; dropped by the panic.",
             "Shot 11: the razor slides into frame alone after the off-screen thud."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush_labels(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_xmas_v1.png")
