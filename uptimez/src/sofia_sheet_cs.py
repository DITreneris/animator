"""v2 (sofia_sheet_cs_v1.py = v1, kept): the sheet with sofia_cs v2's faces; the phone check is now the episode's
three camera presets (close, medium, wide for acting at 62 % of the frame height), and an earring test (head turns
with lag, every face, at 270 px).
Model sheet and phone check for Sofía's Customer Success look (sofia_cs v1).
Sheet: the look beside The Onboarding's (what changed), four poses, eight faces close, the earring and the waves.
Phone: two 540x960 frames (her medium single and the master wide's scale) shown at 270 px, as a phone shows them.
Usage: python3 sofia_sheet_cs.py [out_dir]  ->  uptimez-sofia-cs-v1-sheet.png, uptimez-sofia-cs-v1-phone.png"""
import sys
import cairo
import kit
import sofia_cs as cs
import sofia_ob as so
from kit import Ctx, INK

PAPER = (0.95, 0.93, 0.88)
WALL = kit.WALL


def label(c, t, x, y, size=22, bold=True):
    c.select_font_face("Inter", 0, 1 if bold else 0); c.set_font_size(size); c.set_source_rgb(*INK)
    e = c.text_extents(t); c.move_to(x - e.x_advance / 2, y); c.show_text(t)


def sheet(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.set_source_rgb(*INK)
    c.move_to(50, 70); c.show_text("SOFÍA · Customer Success (ep. 11) · v2 · dressed for him")
    c.select_font_face("Inter", 0, 0); c.set_font_size(22)
    c.move_to(50, 108); c.show_text("Wine blazer-dress, satin lapels edged in gold, no pearls, a gold cuff · open gold triangle earrings · "
                                   "waves over her right shoulder, the other ear showing")
    # what changed: ep 9-10 beside ep 11
    for i, (mod, t) in enumerate(((so, "ep 9–10 (The Onboarding)"), (cs, "ep 11 (Customer Success)"))):
        mod.sofia(k, 190 + 300 * i, 760, 1.45, "hold", "smile", (0.3, 0))
        label(c, t, 190 + 300 * i, 800, 22)
    # poses
    for i, (p, f, lk, t) in enumerate((("hold", "interested", (0.6, 0), "hold"), ("show", "recover", (-0.8, 0), "show (the tablet)"),
                                       ("low", "knowing", (0.9, 0.1), "low"), ("lapel", "smile", (0, 0), "lapel (she has won)"))):
        cs.sofia(k, 860 + 330 * i, 760, 1.45, p, f, lk)
        label(c, t, 860 + 330 * i, 800, 22)
    # faces, close
    faces = (("knowing", (0.8, 0)), ("caught", (1, 0)), ("recover", (-0.6, 0)), ("interested", (0.5, 0)),
             ("appraise", (0.3, 1)), ("smile", (0, 0)), ("real", (0, 0)), ("deadpan", (0, 0)))
    for i, (f, lk) in enumerate(faces):
        x = 150 + 270 * i; y = 1060
        c.save(); c.rectangle(x - 125, 860, 250, 380); c.clip()
        c.set_source_rgb(*WALL); c.paint()
        cs.sofia(k, x, y + 560, 2.3, "low", f, lk)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, 860, 250, 380); c.stroke()
        label(c, f, x, 1275, 22)
    # the earring and the waves, close
    c.save(); c.rectangle(60, 1320, 640, 340); c.clip(); c.set_source_rgb(*WALL); c.paint()
    cs.sofia(k, 380, 1320 + 1200, 4.2, "low", "smile", (0, 0))
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(60, 1320, 640, 340); c.stroke()
    c.select_font_face("Inter", 0, 0); c.set_font_size(22); c.set_source_rgb(*INK)
    notes = ["Rules for this look",
             "· Earrings show on one side only: the other ear is under the waves.",
             "· The triangle swings with lag, like the pearl drop did; about twice her hoop.",
             "· No pearls: the PEARL RULE (lift = interested) is ep 9–10; here her tell is",
             "  checking who noticed (her silent signature) and the lapel smooth when she wins.",
             "· Wine is darker than her lips: the red mouth still reads first in close-ups.",
             "· KNOWING → CAUGHT → RECOVER is her run: the smile comes back before she does.",
             "· Faces and poses: everything from sofia_ob works."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(760, 1360 + 38 * i); c.show_text(t)
    s.write_to_png(out)


PRESETS = {                                                 # ep 11's three framings for her (540x960): feet, scale
    "close": ("face, shoulders, the earring: reactions", lambda: (290, 380 - cs.HY * 3.4, 3.4)),
    "medium": ("head to hips: lines, two-shots", lambda: (290, 360 - cs.HY * 2.2, 2.2)),
    "wide": ("full figure, 62 % of the frame: acting in a wide", lambda: (290, 900, 1.76)),
}


def _wall(c, k):
    import brand
    c.set_source_rgb(*WALL); c.paint()
    brand.mark(c, 40, 120, 70, zzz=False)


def phone(out):
    frames = []
    for name, (txt, f_) in PRESETS.items():
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0); _wall(c, k)
        x, feet, sc = f_()
        if name == "wide":
            c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(0, 900, 540, 60); c.fill()
        cs.sofia(k, x, feet, sc, "hold" if name != "close" else "low", {"close": "knowing", "medium": "interested", "wide": "smile"}[name],
                 (-0.6, 0))
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s.write_to_png(out)


def earring(out):
    """Head turns with lag, at the medium preset, shown at 270 px: the triangle about its stud, never on the jaw."""
    faces = ("knowing", "caught", "recover", "interested", "deadpan", "smile")
    lags = (-14, -7, 0, 7, 14)
    tw, th = 135, 140
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, len(lags) * (tw + 6) + 6, len(faces) * (th + 6) + 6)
    c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for j, f in enumerate(faces):
        for i, lg in enumerate(lags):
            fr = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 560); cc = cairo.Context(fr); k = Ctx(cc, 0); cc.set_source_rgb(*WALL); cc.paint()
            cs.sofia(k, 270, 360 - cs.HY * 2.2, 2.2, "low", f, (lg / 14.0, 0), lag=(lg, 0), lean=lg * 0.25)
            c.save(); c.translate(6 + i * (tw + 6), 6 + j * (th + 6)); c.scale(0.25, 0.25)
            c.rectangle(0, 0, 540, 560); c.clip(); c.set_source_surface(fr, 0, 0); c.paint(); c.restore()
    s.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../characters"
    sheet(d + "/uptimez-sofia-cs-v2-sheet.png")
    phone(d + "/uptimez-sofia-cs-v2-phone.png")
    earring(d + "/uptimez-sofia-cs-v2-earring.png")
