"""Model sheet and phone check for Sofía's Customer Success look (sofia_cs v1).
Sheet: the look beside The Onboarding's (what changed), four poses, eight faces close, the earring and the waves.
Phone: two 540x960 frames (her medium single and the master wide's scale) shown at 270 px, as a phone shows them.
Usage: python3 sofia_sheet_cs_v1.py [out_dir]  ->  uptimez-sofia-cs-v1-sheet.png, uptimez-sofia-cs-v1-phone.png"""
import sys
import cairo
import kit
import sofia_cs_v1 as cs                                     # pinned: the v1 figure
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
    c.move_to(50, 70); c.show_text("SOFÍA · Customer Success (ep. 11) · v1 · dressed for him")
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
    faces = (("smile", (0, 0)), ("interested", (0.5, 0)), ("appraise", (0.3, 1)), ("knowing", (0.8, 0)),
             ("caught", (1, 0)), ("recover", (-0.6, 0)), ("real", (0, 0)), ("deadpan", (0, 0)))
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
             "· Faces and poses: everything from sofia_ob works."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(760, 1360 + 38 * i); c.show_text(t)
    s.write_to_png(out)


def phone(out):
    frames = []
    for kind in ("medium", "wide"):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); c.set_source_rgb(*WALL); c.paint(); k = Ctx(c, 0)
        if kind == "medium":
            cs.sofia(k, 290, 400 - cs.HY * 2.6, 2.6, "hold", "interested", (-0.6, 0))   # the head under the bar
        else:
            c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(0, 800, 540, 160); c.fill()
            cs.sofia(k, 372, 803, 0.70, "hold", "smile", (-0.6, 0))
        frames.append(f)
    W = 2 * 270 + 3 * 20
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 70); c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, f in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 525); c.show_text(("medium single" if i == 0 else "master wide scale") + " · at 270 px")
    s.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../characters"
    sheet(d + "/uptimez-sofia-cs-v1-sheet.png")
    phone(d + "/uptimez-sofia-cs-v1-phone.png")
