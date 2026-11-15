"""v2 (sofia_sheet_tg_v1.py writes v1 from sofia_tg_v1.py). SOFÍA model sheet for the Thanksgiving film
"Raises for Everyone" (sofia_tg.py). Writes sofia_sheet_tg_v2.png
at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import sofia_v4 as sf4
import sofia_xmas as sxm
import sofia_tg as st
import sofia_tg_v1 as st1
import iwry_mouths as im
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.96, 0.88, 0.78)
LABELS = []
HY = -300 * st.H + 78 - 44


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


def head_at(k, cx, cy, s, kind, look=(0, 0), lag=(0, 0), mouth=None, boil=0):
    """Head centred at (cx, cy). mouth: a viseme code drawn over the face (as in the film)."""
    c = k.c
    c.save(); c.translate(cx, cy); c.scale(s, s)
    k2 = Ctx(c, boil)
    st.sofia(k2, 0, -HY, 1.0, "stand", kind, look=look, lag=lag, badge=False)
    if mouth:
        im.sof_mouth(k2, (0, 0), mouth)
    c.restore()


def table(c, x, y, w):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w, 60); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w, 60); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "Thanksgiving film \"Raises for Everyone\"  ·  main character  ·  office look, autumn touches", 172, 44, 13,
         col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · THANKSGIVING v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front, full body
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    st.sofia(k, 144, 512, 1.18, "stand", "neutral", seed=71)
    corp(c, "FRONT · THANKSGIVING LOOK", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. lineage
    corp(c, "OFFICE v4  ·  THANKSGIVING v1  ·  THANKSGIVING v2", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    sf4.sofia(k, 345, 296, 0.56, "stand", "neutral", seed=73, folder="none")
    st1.sofia(k, 449, 296, 0.56, "stand", "neutral", seed=73)
    st.sofia(k, 553, 296, 0.56, "stand", "neutral", seed=73)
    c.restore()
    corp(c, "v2: silver stars, short teal jacket over a blush blouse, narrower mustard scarf.", 290, 322, 9, col=GREY)

    # 3. faces for this film + talking mouths
    corp(c, "FACES IN THIS FILM", 284, 348, 10, bold=True)
    faces = [("eyebrow", (0.8, 0), "shot 4: one eyebrow"), ("closed", (0, 0), "shot 8: closed eyes"),
             ("tiny", (-0.6, 0), "shot 10: tiny smile (new)")]
    for i, (e, lk, lab) in enumerate(faces):
        x, y = 284 + i * 112, 354
        boxed(c, x, y, 106, 92, lab, fill=(1, 0.99, 0.97) if e != "tiny" else (0.98, 0.95, 0.88))
        c.save(); c.rectangle(x, y, 106, 92); c.clip()
        head_at(k, x + 53, y + 42, 0.5, e, lk)
        c.restore()
    corp(c, "\"She refused. She didn't fail.\"  mouths M · E · A · O · F", 284, 466, 9, col=GREY, bold=True)
    for i, m in enumerate(("M", "E", "A", "O", "F")):
        x, y = 284 + i * 67, 472
        boxed(c, x, y, 63, 60)
        c.save(); c.rectangle(x, y, 63, 60); c.clip()
        head_at(k, x + 31, y + 26, 0.42, "neutral", (-0.8, 0), mouth=m)
        c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [("aside", "neutral", (0.9, 0.3), 7, "shot 3: lean to Pam"), ("stand", "eyebrow", (-0.8, 0), 0, "shot 4"),
             ("correct", "neutral", (-0.9, 0), -3, "shot 8: correcting Don"), ("stand", "tiny", (-0.6, 0), 0, "shot 10")]
    for i, (p, f, lk, ln, lab) in enumerate(poses):
        x = 634 + i * 137
        boxed(c, x, 98, 131, 210, lab)
        c.save(); c.rectangle(x, 98, 131, 210); c.clip()
        st.sofia(k, x + 66, 290, 0.56, p, f, look=lk, lean=ln, seed=80 + i, lag=(-4 if ln > 0 else 0, 0))
        c.restore()

    # 5. earring motion + scarf detail
    corp(c, "EARRINGS: SWING ON A HEAD TURN, SPARKLE ON THE BOIL  (lag -8 · -4 · 0 · 4 · 8)", 634, 348, 10, bold=True)
    for i, lg in enumerate((-8, -4, 0, 4, 8)):
        x, y = 634 + i * 108, 354
        boxed(c, x, y, 102, 104, "boil %d" % (i % 3))
        c.save(); c.rectangle(x, y, 102, 88); c.clip()
        head_at(k, x + 51, y + 26, 0.62, "neutral", (lg / 9, 0), lag=(lg, 0), boil=i % 3)
        c.restore()
    boxed(c, 634, 466, 170, 66, "jacket open, blush V-neck, belt")
    c.save(); c.rectangle(634, 466, 170, 50); c.clip()
    st.sofia(k, 719, 491 + 190 * 0.62, 0.62, "stand", "neutral", seed=71)
    c.restore()
    boxed(c, 812, 466, 170, 66, "silver star reads on the braid")
    c.save(); c.rectangle(812, 466, 170, 50); c.clip()
    st.sofia(k, 897 + 30 * 1.0, 491 + 232 * 1.0, 1.0, "stand", "neutral", badge=False)
    c.restore()

    # 6. phone-size check: with Pam (burnt-orange cardigan) behind the table, as in shots 3 and 7
    corp(c, "PHONE-SIZE CHECK  (shots 3 / 7: Sofía beside Pam in her burnt-orange cardigan, behind the table)", 24, 556,
         10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    pam = dict(kit.PEOPLE["PAM"]); kit.PEOPLE["PAM"]["body"] = (0.80, 0.40, 0.14)
    for i, (p, f, lk, ln) in enumerate((("aside", "neutral", (0.9, 0), 7), ("correct", "closed", (0, 0), -3))):
        x0 = 90 + i * 290
        st.sofia(k, x0, 760, 0.42, p, f, look=lk, lean=ln, seed=95 + i)
        kit.person(k, "PAM", x0 + 92, 760, 0.42, "stand", "neutral", seed=97 + i, look=(-0.6, 0))
    kit.PEOPLE["PAM"].clear(); kit.PEOPLE["PAM"].update(pam)
    table(c, 24, 700, 590)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["Red lips stay: they are her face, not her costume.",
             "Silver stars, dark outline, white glint: they no longer merge with her hair.",
             "Short teal jacket, open over a blush V-neck: elegant, not a uniform.",
             "Scarf ~20 % smaller, loose; mustard ground keeps her apart from Pam's orange.",
             "Badge smaller, on the jacket. No more accessories than these.",
             "Tiny smile = one lip corner + dimple, 0.5 s. She stays the straight woman."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_tg_v2.png")
