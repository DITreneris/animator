"""PAM model sheet for the Thanksgiving film "Raises for Everyone" (pam_tg.py). Writes pam_sheet_tg_v1.png
at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import pt42
import pam_xmas as px
import pam_tg_v1 as pt
import don_tg as dt
import sofia_tg as st
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.93, 0.90, 0.84)
LABELS = []
HY = -300 * kit.PEOPLE["PAM"]["h"] + 78 - 44


def boxed(c, x, y, w, h, label=None, fill=(1, 1, 1)):
    c.set_source_rgb(*fill); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(x, y, w, h); c.stroke()
    LABELS.append((x, y, w, h, label))


def flush(c):
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 17, w - 2, 16); c.fill()
            corp(c, label, x + 6, y + h - 5, 9, col=GREY)
    LABELS.clear()


def table(c, x, y, w):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w, 60); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w, 60); c.stroke()


def head_at(k, cx, cy, s, face, look=(0, 0), mouth=None):
    pt.pam(k, cx, cy - HY * s, s, "stand", face, look=look, mouth=mouth)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "Thanksgiving film \"Raises for Everyone\"  ·  says the quiet part calmly  ·  a soft spot for Don", 140, 44,
         13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · THANKSGIVING v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    pt.pam(k, 144, 512, 1.18, "stand", "neutral", seed=71)
    corp(c, "FRONT · BUTTONED TO THE TOP", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. office / Christmas / Thanksgiving
    corp(c, "OFFICE  ·  CHRISTMAS  ·  THANKSGIVING", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    pt42.branded_person(k, "PAM", 345, 296, 0.56, seed=72)
    px.pam(k, 449, 296, 0.56, "stand", "neutral", mask="neck", seed=72)
    pt.pam(k, 553, 296, 0.56, "stand", "neutral", seed=72)
    c.restore()
    corp(c, "Same Pam. New: orange cardigan, leaf brooch, a silver streak.", 290, 322, 9, col=GREY)

    # 3. faces + mouths
    corp(c, "FACES  (flat is the default; \"soft\" is new)", 284, 348, 10, bold=True)
    faces = [("neutral", (0, 0), "flat"), ("read", (0, 1), "reading the form"), ("stare", (0.6, 0), "the verdict"),
             ("soft", (0.8, 0.8), "soft spot for Don")]
    for i, (e, lk, lab) in enumerate(faces):
        x, y = 284 + i * 83, 354
        boxed(c, x, y, 79, 92, lab, fill=(1, 0.99, 0.97) if e != "soft" else (0.99, 0.93, 0.92))
        c.save(); c.rectangle(x, y, 79, 92); c.clip()
        head_at(k, x + 40, y + 40, 0.46, e, lk)
        c.restore()
    corp(c, "\"I'm expecting.\" · \"No.\" · \"walking policy violation\"  mouths M · E · A · O · F", 284, 466, 9, col=GREY,
         bold=True)
    for i, m in enumerate(("M", "E", "A", "O", "F")):
        x, y = 284 + i * 67, 472
        boxed(c, x, y, 63, 60)
        c.save(); c.rectangle(x, y, 63, 60); c.clip()
        head_at(k, x + 31, y + 26, 0.42, "neutral", (0.6, 0), mouth=m)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(pt.POSE_READ, "read", True, "3/7: reading"), (pt.POSE_PUSH, "stare", False, "7: pushes it back"),
             ("stand", "stare", False, "7: \"No.\""), (pt.POSE_TUG, "neutral", False, "9: stands, tugs"),
             (pt.POSE_PRIMP, "soft", False, "soft spot: primps"), ("stand", "stare", False, "9: eye to eye")]
    for i, (p, f, fm, lab) in enumerate(poses):
        x = 634 + i * 91
        boxed(c, x, 98, 87, 210, lab, fill=(1, 1, 1) if f != "soft" else (0.99, 0.95, 0.94))
        c.save(); c.rectangle(x, 98, 87, 210); c.clip()
        pt.pam(k, x + (36 if p is not pt.POSE_PUSH else 30), 290, 0.48, p, f, look=(0.7, 0), seed=80 + i, form=fm)
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "brooch: red enamel, gold rim")
    pt.brooch(k, 719, 436, 4.0)
    boxed(c, 812, 354, 170, 178, "one silver lock, smile lines")
    c.save(); c.rectangle(812, 354, 170, 160); c.clip()
    head_at(k, 897, 440, 1.05, "neutral", (0.3, 0))
    c.restore()
    boxed(c, 990, 354, 186, 178, "the primp: bare hands, no ring")
    c.save(); c.rectangle(990, 354, 186, 160); c.clip()
    pt.pam(k, 1068, 440 - HY * 0.95, 0.95, pt.POSE_PRIMP, "soft", look=(0.8, 0.8), seed=90, badge=False)
    c.restore()

    # 6. two-shots: colour check with Sofía and with Don
    corp(c, "PHONE-SIZE CHECK  (two-shots behind the table: with Sofía, shots 3/7  ·  with Don, shot 9)", 24, 556, 10,
         bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    st.sofia(k, 84, 760, 0.42, "aside", "neutral", look=(0.9, 0), lean=7, seed=95)
    pt.pam(k, 172, 760, 0.42, pt.POSE_READ, "read", seed=96, form=True)
    pt.pam(k, 300, 760, 0.42, pt.POSE_PRIMP, "soft", look=(0.8, 0.8), seed=97)
    dt.don(k, 400, 770, 0.42, dt.POSE_SLAP, "grin", look=(-0.6, 0), seed=98)
    pt.pam(k, 486, 760, 0.42, "stand", "stare", look=(0.8, 0), seed=99)
    dt.don(k, 572, 770, 0.42, dt.POSE_SLUMP, "collapse", seed=100, slump=1.3)
    c.restore()
    table(c, 24, 700, 590)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Office Pam: blouse collar, lanyard with badge and too many keys, beige trousers, trainers.",
             "Burnt-orange cardigan buttoned to the top; red enamel maple-leaf brooch, gold rim.",
             "Older and single: a silver streak in the bob, smile lines, no ring. No new props.",
             "Flat face by default; she says the quiet part calmly and never raises her voice.",
             "Soft spot for Don: a faint blush and a hand to her hair, used once and small.",
             "The contradiction: she primps for him, then calls him a walking policy violation."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_tg_v1.png")
