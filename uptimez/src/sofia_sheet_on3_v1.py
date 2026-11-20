"""PINNED v1 (19 Nov): draws sheet v1 from sofia_on3_v1.
Model sheet and phone check for Sofia's ring look in Office Noir 3: The Last Round (sofia_on3 v1).
Sheet: the look beside episode 11's (what changed), four poses, six faces close, the back of her legs (the seam, the
heels), the look as the dream shows it (black and white, her lips the only colour), the rules.
Phone: three 540x960 frames in the dream's look (wide, medium, close), shown at 270 px, as a phone shows them.
Usage: python3 sofia_sheet_on3.py [out_dir]  ->  uptimez-sofia-on3-v1-sheet.png, uptimez-sofia-on3-v1-phone.png"""
import sys
import math
import cairo
import kit
import engine_on as eo
import sofia_on3_v1 as r
import sofia_cs as cs
from kit import Ctx, INK

PAPER = (0.95, 0.93, 0.88)
WALL = kit.WALL
HY = r.HY


def label(c, t, x, y, size=22, bold=True, col=INK):
    c.select_font_face("Inter", 0, 1 if bold else 0); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(t); c.move_to(x - e.x_advance / 2, y); c.show_text(t)


def ring(c, w, h, floor, lamp_x=None):
    """The ring at night, before the noir pass: a dark hall, one lamp's cone, smoke, the ropes, hats in the dark."""
    lamp_x = w / 2 if lamp_x is None else lamp_x
    c.set_source_rgb(0.13, 0.13, 0.15); c.rectangle(0, 0, w, h); c.fill()
    g = cairo.RadialGradient(lamp_x, floor - h * 0.45, 10, lamp_x, floor - h * 0.45, h * 0.75)   # the haze the lamp lights
    g.add_color_stop_rgba(0, 0.74, 0.74, 0.76, 1); g.add_color_stop_rgba(0.55, 0.42, 0.42, 0.45, 1)
    g.add_color_stop_rgba(1, 0.13, 0.13, 0.15, 1)
    c.set_source(g); c.rectangle(0, 0, w, floor); c.fill()
    c.set_source_rgb(0.05, 0.05, 0.06)                                    # hats at ringside, dark against the haze
    for i in range(int(w / 46) + 2):
        hx = i * 46 - 12 + (9 if i % 2 else 0); hy = floor - 46 - (7 if i % 3 == 0 else 0)
        c.arc(hx, hy, 15, 0, 6.2832); c.fill()
        c.rectangle(hx - 21, hy - 12, 42, 5); c.fill(); c.rectangle(hx - 13, hy - 26, 26, 15); c.fill()
        c.rectangle(hx - 19, hy + 12, 38, 40); c.fill()
    c.set_source_rgb(0.62, 0.62, 0.64); c.rectangle(0, floor - 8, w, h - floor + 8); c.fill()     # the canvas
    c.set_source_rgb(0.86, 0.86, 0.88)
    for i, ry in enumerate((floor - 96, floor - 64, floor - 32)):         # three ropes
        c.rectangle(0, ry, w, 5); c.fill()
    c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(0, floor - 8, w, 4); c.fill()


def noir(surf):
    old = eo.TONE
    eo.TONE = "v3"
    try:
        eo.accent_pass(surf, r.ACCENTS)
    finally:
        eo.TONE = old


def dream_panel(w, h):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s); k = Ctx(c, 0)
    ring(c, w, h, h - 26, lamp_x=w * 0.36)
    r.sofia(k, w * 0.36, h + 250, 1.55, "r_card", "smile", (0.5, 0), card_="ROUND 1")
    c.save(); c.rectangle(w * 0.62, 0, w * 0.38, h); c.clip()
    c.set_source_rgb(0.30, 0.30, 0.32); c.paint()
    g = cairo.LinearGradient(w * 0.62, 0, w, 0); g.add_color_stop_rgba(0, 0.62, 0.62, 0.64, 1); g.add_color_stop_rgba(1, 0.16, 0.16, 0.18, 1)
    c.set_source(g); c.paint()
    r.sofia(k, w * 0.80, h + 640, 2.7, "r_down", "appraise", (-0.8, 0.2))
    c.restore()
    noir(s)
    c.set_source_rgb(0.02, 0.02, 0.02); c.rectangle(w * 0.62 - 3, 0, 6, h); c.fill()
    return s


def sheet(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.set_source_rgb(*INK)
    c.move_to(50, 70); c.show_text("SOFÍA · Office Noir 3: The Last Round · v1 · the ring")
    c.select_font_face("Inter", 0, 0); c.set_font_size(22)
    c.move_to(50, 106); c.show_text("Short black satin leotard, 1940s, an ivory bow on the hip · bare arms · waves over her right shoulder · one big gold hoop")
    c.move_to(50, 136); c.show_text("A white feather · a ribbon at the neck · a beauty mark · seamed stockings · black patent heels · her lips the only colour in the dream")
    cs.sofia(k, 180, 780, 1.45, "hold", "smile", (0.3, 0)); label(c, "ep 11 (Customer Success)", 180, 822, 22)
    r.sofia(k, 500, 780, 1.45, "r_hips", "smile", (0.3, 0)); label(c, "the ring (Office Noir 3)", 500, 822, 22)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(700, 150); c.line_to(700, 830); c.stroke()
    for x, p, f, lk, cd, t in ((1010, "r_card", "smile", (0.4, 0), "ROUND 1", "r_card (5.1: she walks it round)"),
                               (1330, "r_down", "interested", (0.8, 0), None, "r_down"),
                               (1740, "r_side", "appraise", (0.8, 0.3), "LAST ROUND", "r_side (between rounds)"),
                               (2050, "r_hips", "knowing", (-0.7, 0), None, "r_hips")):
        r.sofia(k, x, 780, 1.45, p, f, lk, card_=cd)
        label(c, t, x - (60 if cd else 0), 822, 22)
    faces = (("smile", (0, 0)), ("interested", (0.5, 0)), ("appraise", (0.3, 1)), ("knowing", (0.8, 0)), ("caught", (1, 0)),
             ("deadpan", (0, 0)))
    for i, (f, lk) in enumerate(faces):
        x = 150 + 270 * i; y = 1080
        c.save(); c.rectangle(x - 125, 880, 250, 380); c.clip()
        c.set_source_rgb(*WALL); c.paint()
        r.sofia(k, x - 6, y + 560, 2.3, "r_down", f, lk)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, 880, 250, 380); c.stroke()
        label(c, f, x, 1295, 22)
    c.save(); c.rectangle(1660, 880, 480, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()      # the back of her legs
    c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(1660, 1215, 480, 45); c.fill()
    r.legs_back(k, 1900, 1218, 3.3)
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(1660, 880, 480, 380); c.stroke()
    label(c, "from behind: the seam, the heels", 1900, 1295, 22)
    dp = dream_panel(980, 340)                                                                     # as the dream shows her
    c.set_source_surface(dp, 60, 1330); c.paint()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(60, 1330, 980, 340); c.stroke()
    c.select_font_face("Inter", 0, 0); c.set_font_size(21); c.set_source_rgb(*INK)
    notes = ["Rules for this look",
             "· In the dream she is black and white. Her lips are the only colour on her (Tomas, 19 Nov);",
             "  the film's other red is the Client's robe and gloves. The hoop keeps a third of its gold.",
             "· The heels are black patent, not red: a white glint on each toe says patent.",
             "· One hoop shows: the other ear is under the waves. It hangs from the lobe and swings with lag.",
             "· The card is held high in one hand, beside her head, so the head never covers its words.",
             "  ROUND 1 on one row; LAST ROUND on two.",
             "· Black satin: in the dream her hair goes white, so the leotard is the dark that holds her shape,",
             "  and it keeps her apart from the Referee's white shirt. The bow and the feather are the lights.",
             "· The seam is only seen from behind: one shot of her walking away is enough.",
             "· Faces and poses: everything from sofia_ob works."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(1080, 1362 + 30 * i); c.show_text(t)
    s.write_to_png(out)


def phone(out):
    frames = []
    specs = (("wide", "5.1: the card, the ring, full figure", (335, 870, 1.55), "r_card", "smile", (0.6, 0), "ROUND 1"),
             ("medium", "7.1: LAST ROUND goes past", (375, 360 - HY * 2.2 + 190, 2.2), "r_card", "knowing", (0.7, 0), "LAST ROUND"),
             ("close", "her eyes on him", (270, 400 - HY * 3.4, 3.4), "r_down", "appraise", (-0.8, 0.2), None))
    for name, txt, (x, feet, sc), pose, face, lk, cd in specs:
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        ring(c, 540, 960, 880 if name == "wide" else 1400, lamp_x=x)
        r.sofia(k, x, feet, sc, pose, face, lk, card_=cd)
        noir(f)
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../characters"
    sheet(d + "/uptimez-sofia-on3-v1-sheet.png")
    phone(d + "/uptimez-sofia-on3-v1-phone.png")
