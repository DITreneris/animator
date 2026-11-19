"""v2 (client_sheet_on3_v1.py = v1, kept): the street tracksuit, the hard face, the darker stubble of the dream.
Model sheet and phone check for the Client as the boxer in Office Noir 3: The Last Round (client_on3 v2).
Sheet: the boxer beside the Client of episodes 9-11 (what changed), six poses, six faces close, his waking twin, the
look as the dream shows it, his size beside Sofia, the rules.
Phone: three 540x960 frames in the dream's look (the street, the car's headlights, frame 0), shown at 270 px.
Usage: python3 client_sheet_on3.py [out_dir]  ->  uptimez-client-on3-v2-sheet.png, uptimez-client-on3-v2-phone.png"""
import sys
import math
import cairo
import kit
import engine_on as eo
import client_on3 as b
import client_ob as co
import sofia_on3 as r
import sofia_sheet_on3 as ssh
from kit import Ctx, INK

PAPER = (0.95, 0.93, 0.88)
WALL = kit.WALL
ACC = b.ACCENTS + r.ACCENTS
label = ssh.label


def noir(surf):
    old = eo.TONE
    eo.TONE = "v3"
    try:
        eo.accent_pass(surf, ACC)
    finally:
        eo.TONE = old


def street(c, w, h, floor, lamp_x, lamp_y=None):
    """A street at night, before the noir pass: a dark wall, one lamp's pool on it, wet stones, rain."""
    lamp_y = floor - h * 0.5 if lamp_y is None else lamp_y
    c.set_source_rgb(0.10, 0.10, 0.12); c.rectangle(0, 0, w, h); c.fill()
    g = cairo.RadialGradient(lamp_x, lamp_y, 10, lamp_x, lamp_y, h * 0.62)
    g.add_color_stop_rgba(0, 0.72, 0.72, 0.74, 1); g.add_color_stop_rgba(0.5, 0.36, 0.36, 0.39, 1)
    g.add_color_stop_rgba(1, 0.10, 0.10, 0.12, 1)
    c.set_source(g); c.rectangle(0, 0, w, floor); c.fill()
    c.set_source_rgba(0, 0, 0, 0.30); c.set_line_width(2)                    # the wall's courses
    for i in range(1, 9):
        c.move_to(0, floor - i * h * 0.085); c.line_to(w, floor - i * h * 0.085); c.stroke()
    g2 = cairo.LinearGradient(0, floor, 0, h); g2.add_color_stop_rgba(0, 0.50, 0.50, 0.53, 1); g2.add_color_stop_rgba(1, 0.16, 0.16, 0.18, 1)
    c.set_source(g2); c.rectangle(0, floor, w, h - floor); c.fill()
    c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(1.6)
    rr = kit.Ctx(c, 0).rng(77)
    for _ in range(int(w * h / 9000)):
        x0, y0 = rr.uniform(0, w), rr.uniform(0, h)
        c.move_to(x0, y0); c.line_to(x0 - 5, y0 + 22); c.stroke()


def dream_panel(w, h):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s); k = Ctx(c, 0)
    half = w // 2
    c.save(); c.rectangle(0, 0, half, h); c.clip()
    street(c, half, h, h - 30, half * 0.5, h * 0.42)
    b.boxer(k, half * 0.5, h - 14, 0.62, "b_walk", "hard", (0.6, 0), outfit="street")
    c.restore()
    c.save(); c.translate(half, 0); c.rectangle(0, 0, w - half, h); c.clip()
    ssh.ring(c, w - half, h, h - 26, lamp_x=(w - half) * 0.5)
    b.boxer(k, (w - half) * 0.5, h + 150, 0.86, "b_guard", "hard", (0.9, 0), tape=True)
    c.restore()
    noir(s)
    c.set_source_rgb(0.02, 0.02, 0.02); c.rectangle(half - 3, 0, 6, h); c.fill()
    return s


def sheet(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.set_source_rgb(*INK)
    c.move_to(50, 70); c.show_text("THE CLIENT · Office Noir 3: The Last Round · v2 · the boxer")
    c.select_font_face("Inter", 0, 0); c.set_font_size(22)
    c.move_to(50, 106); c.show_text("STREET: a charcoal hooded tracksuit, the garages' gear small on the chest · RING: the red hooded robe, ivory trim · red gloves he never takes off")
    c.move_to(50, 136); c.show_text("HARD is his face in the dream: low brows, narrow eyes, a pressed mouth, darker stubble · the same head as episodes 9–11 · wide eyes only for SHOCK")
    S, F = 0.86, 730
    co.client(k, 150, F, S, "stand", "confident", (0.3, 0)); label(c, "ep 9–11", 150, F + 42, 22)
    b.boxer(k, 410, F, S, "b_walk", "hard", (0.3, 0), outfit="street"); label(c, "STREET (beats 02–04)", 410, F + 42, 22)
    b.boxer(k, 670, F, S, "b_walk", "hard", (0.3, 0)); label(c, "RING (beats 05–07)", 670, F + 42, 22)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(815, 170); c.line_to(815, F + 50); c.stroke()
    st = dict(outfit="street")
    row = ((960, "b_fist", "hard", (0.8, 0), st, "b_fist: his finger"),
           (1225, "b_ask", "hard", (0.6, 0), dict(outfit="street", cig=True), "b_ask: a light?"),
           (1480, "b_pay", "hard", (0.9, 0.3), dict(outfit="street", note=True), "b_pay: the hundred"),
           (1765, "b_swing", "hard", (0.9, 0), dict(), "b_swing"),
           (2050, "b_reach", "dawning", (0.3, -1), dict(tape=True), "b_reach: the roll"))
    for x, p, f, lk, kw, t in row:
        b.boxer(k, x, F, S, p, f, lk, **kw); label(c, t, x, F + 42, 22)
    faces = (("hard", dict(outfit="street"), "hard · street"), ("hard", dict(outfit="street", cig=True), "hard · cigarette"),
             ("hard", dict(), "hard · ring"), ("dawning", dict(), "dawning: the roll"), ("shock", dict(tape=True), "shock · taped"),
             ("tired", dict(tape=True), "tired · taped"))
    for i, (f, kw, t) in enumerate(faces):
        x = 150 + 270 * i; y0 = 880
        c.save(); c.rectangle(x - 125, y0, 250, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()
        b.boxer(k, x + 6, y0 + 200 - b.HY * 1.75, 1.75, "b_walk", f, (0.4, 0), **kw)
        c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, y0, 250, 380); c.stroke()
        label(c, t, x, y0 + 415, 22)
    c.save(); c.rectangle(1660, 880, 480, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()        # awake
    b.boxer(k, 1790, 1246, 0.74, "b_walk", "tired", (0.3, 0), awake=True)
    b.boxer(k, 2020, 1246, 0.74, "b_walk", "hard", (-0.3, 0))
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(1660, 880, 480, 380); c.stroke()
    label(c, "awake: the dressing gown, and its dream twin", 1900, 1295, 22)
    dp = dream_panel(760, 340)
    c.set_source_surface(dp, 60, 1330); c.paint()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(60, 1330, 760, 340); c.stroke()
    c.save(); c.rectangle(850, 1330, 330, 340); c.clip(); c.set_source_rgb(*WALL); c.paint()        # beside Sofia
    c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(850, 1640, 330, 30); c.fill()
    r.sofia(k, 930, 1644, 0.78, "r_hips", "spotted", (1, 0))
    b.boxer(k, 1085, 1644, 0.78 * b.REL, "b_walk", "hard", (-0.5, 0))
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(850, 1330, 330, 340); c.stroke()
    c.select_font_face("Inter", 0, 0); c.set_font_size(21); c.set_source_rgb(*INK)
    notes = ["Rules for this look",
             "· The gloves never come off. On the street they are the only red; the robe comes with the ring.",
             "· The change of clothes is a cut at the arena door (04 to 05). It is never shown.",
             "· HARD is his neutral in the dream. He shows almost nothing; SHOCK is kept for the punches.",
             "· The tracksuit is charcoal, not black: it needs a lit wall behind it and the pale edge on the hood.",
             "· The gloves are larger than his hands and have no fingers: every glove gag reads from that.",
             "· The gear on the chest is his garages' mark, the same as the pin in episode 9. Never words.",
             "· Tape: Pam's strip over the nicked brow, from the corner (6.1) to the end.",
             "· Awake: a duller red towelling gown, his watch, his everyday stubble: the robe's twin.",
             "· Beside the others he is drawn at 0.70 of their scale, as in episode 9 (panel, left)."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(1215, 1362 + 32 * i); c.show_text(t)
    s.write_to_png(out)


def phone(out):
    frames = []
    for name, txt in (("wide", "2.1: the street, hood up"), ("medium", "2.3: the glove he means as a finger"), ("close", "1.1: frame 0, the glove an inch away")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        if name == "wide":
            street(c, 540, 960, 860, 270, 430)
            b.boxer(k, 270, 884, 1.22, "b_walk", "hard", (0, 0.3), outfit="street")
        elif name == "medium":
            street(c, 540, 960, 1300, 230, 640)                                # the headlights: light from low in front
            b.boxer(k, 230, 1250, 1.75, "b_fist", "hard", (0.2, 0.6), outfit="street")
        else:
            ssh.ring(c, 540, 960, 1500, lamp_x=250, lamp_y=380)
            b.boxer(k, 205, 470 - b.HY * 3.1, 3.1, "b_walk", "dawning", (1.6, 0.1))
            b.robot_glove(k, 452, 500, 3.1 * 0.8, math.pi + 0.06)
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
    sheet(d + "/uptimez-client-on3-v2-sheet.png")
    phone(d + "/uptimez-client-on3-v2-phone.png")
