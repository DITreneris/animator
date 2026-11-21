"""PINNED v1 (19 Nov): draws sheet v1 from robot_on3_v1.
Model sheet and phone check for the robot in Office Noir 3: The Last Round (robot_on3 v1).
Sheet: the ring robot beside the office robot (what changed), four poses, five screens close, its corner, the look as
the dream shows it, its size beside the Client, the rules.
Phone: three 540x960 frames in the dream's look (the two in the ring, the words on its screen, frame 0), at 270 px.
Usage: python3 robot_sheet_on3.py [out_dir]  ->  uptimez-robot-on3-v1-sheet.png, uptimez-robot-on3-v1-phone.png"""
import sys
import math
import cairo
import kit
import robot_on3_v1 as r
import client_on3 as b
import acts_ob as ac
import sofia_sheet_on3 as ssh
import client_sheet_on3 as csh
from kit import Ctx, INK, cut, rect

PAPER = (0.95, 0.93, 0.88)
WALL = kit.WALL
label = ssh.label
noir = csh.noir
HEAD = r.w.HEAD_Y


def roll_on_rope(k, x, y, s=1.0):
    c = k.c
    c.set_source_rgb(0.86, 0.86, 0.88); c.set_line_width(2.4 * s); c.move_to(x, 0); c.line_to(x, y - 10 * s); c.stroke()
    ac.roll(k, x - 4 * s, y, s * 0.7, 0.10, ln=150)


def corner(k, x, feet, s):
    """Its corner: a post with a socket, the cable, a stool nobody sits on; a service arm oils its elbow."""
    c = k.c
    rect(k, x + 150 * s, feet - 250 * s, 22 * s, 250 * s, (0.30, 0.30, 0.34), 5, lw=2)
    for i in range(3):
        c.set_source_rgb(0.86, 0.86, 0.88); c.rectangle(x - 200 * s, feet - (96 - i * 32) * s - 150 * s, 350 * s, 5 * s); c.fill()
    r.cable(k, x - 30 * s, feet - 120 * s, x + 150 * s, feet - 60 * s, 7)
    r.robot(k, x, feet, s, "r_oil", "proud", oil=True)


def dream_panel(w, h):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s); k = Ctx(c, 0)
    ssh.ring(c, w, h, h - 24, lamp_x=w * 0.5)
    roll_on_rope(k, w * 0.5, 62, 0.8)
    b.boxer(k, w * 0.26, h - 12, 0.62, "b_guard", "hard", (0.9, 0), tape=True)
    r.robot(k, w * 0.72, h - 12, 0.62 / b.REL * r.REL, "r_jab", "furious", side=-1)
    noir(s)
    return s


def sheet(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.set_source_rgb(*INK)
    c.move_to(50, 70); c.show_text("THE ROBOT · Office Noir 3: The Last Round · v1 · the other corner")
    c.select_font_face("Inter", 0, 0); c.set_font_size(22)
    c.move_to(50, 106); c.show_text("The same small HR robot · big grey gloves on two piston arms, carried by a steel yoke over its shoulders · two outriggers with casters beside its wheel")
    c.move_to(50, 136); c.show_text("A champion's belt under the HR badge · a FURIOUS screen · the words, the tick and the crack are all on its face · nothing on it is red")
    S, F = 1.42, 740
    r.robot(k, 170, F, S, "r_wait", "eager", rig=False); label(c, "at work (ep 9–11)", 170, F + 42, 22)
    r.robot(k, 500, F, S, "r_guard", "furious"); label(c, "in the ring", 500, F + 42, 22)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(720, 170); c.line_to(720, F + 50); c.stroke()
    row = ((900, "r_wait", "ask", dict(), "r_wait: it asks, and waits"),
           (1260, "r_jab", "furious", dict(), "r_jab: one piston, straight"),
           (1640, "r_wait", "tick", dict(), "the tick, after \"Approved.\""),
           (1990, "r_guard", "furious", dict(crack=True, side=-1), "cracked (7.2 on)"))
    for x, p, st, kw, t in row:
        r.robot(k, x, F, S, p, st, **kw); label(c, t, x, F + 42, 22)
    screens = (("furious", False, "furious"), ("ask", False, "ask"), ("tick", False, "tick"), ("proud", False, "proud"), ("ask", True, "ask · cracked"))
    for i, (st, cr, t) in enumerate(screens):
        x = 150 + 270 * i; y0 = 880
        c.save(); c.rectangle(x - 125, y0, 250, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()
        r.robot(k, x, y0 + 200 - HEAD * 2.25, 2.25, "r_wait", st, crack=cr)
        c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, y0, 250, 380); c.stroke()
        label(c, t, x, y0 + 415, 22)
    c.save(); c.rectangle(1390, 880, 750, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()        # its corner
    c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(1390, 1225, 750, 35); c.fill()
    corner(k, 1690, 1236, 1.12)
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(1390, 880, 750, 380); c.stroke()
    label(c, "its corner (6.2): plugged in, and oiled by its own service arm", 1765, 1295, 22)
    dp = dream_panel(760, 340)
    c.set_source_surface(dp, 60, 1330); c.paint()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(60, 1330, 760, 340); c.stroke()
    c.save(); c.rectangle(850, 1330, 330, 340); c.clip(); c.set_source_rgb(*WALL); c.paint()        # beside the Client
    c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(850, 1640, 330, 30); c.fill()
    b.boxer(k, 935, 1644, 0.74 * b.REL, "b_walk", "hard", (0.6, 0.3))
    r.robot(k, 1095, 1644, 0.74 * r.REL, "r_wait", "furious", side=-1)
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(850, 1330, 330, 340); c.stroke()
    c.select_font_face("Inter", 0, 0); c.set_font_size(21); c.set_source_rgb(*INK)
    notes = ["Rules for this look",
             "· It is the office robot, small: drawn at 0.82 of the others' scale. The joke is the size.",
             "· The gloves are grey and bigger than its screen. Red is the Client's.",
             "· The yoke carries the pistons; the outriggers are training wheels. Both come off at work.",
             "· Its face is the screen: FURIOUS, the three words when it asks, the tick, PROUD between rounds.",
             "· It never hits without the tick. The words fill an insert so they read on a phone.",
             "· The crack stays from 7.2 to the end. It still asks, through the crack.",
             "· No trainer: a cable and a service arm with an oil can. With gloves on, it cannot hold the can.",
             "· It does not speak. The antenna flashes when it is furious."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(1215, 1362 + 32 * i); c.show_text(t)
    s.write_to_png(out)


def phone(out):
    frames = []
    for name, txt in (("wide", "5.2: the two of them, under the roll"), ("medium", "5.3: the words, filling the frame"),
                      ("close", "1.1: frame 0, its glove an inch away")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        if name == "wide":
            ssh.ring(c, 540, 960, 860, lamp_x=270, lamp_y=420)
            roll_on_rope(k, 270, 250, 1.3)
            b.boxer(k, 150, 884, 0.98, "b_swing", "hard", (0.9, 0))
            r.robot(k, 415, 884, 0.98 / b.REL * r.REL, "r_wait", "ask", side=-1)
        elif name == "medium":
            ssh.ring(c, 540, 960, 1500, lamp_x=270, lamp_y=420)
            r.robot(k, 270, 470 - HEAD * 4.6, 4.6, "r_wait", "ask")
        else:
            ssh.ring(c, 540, 960, 1500, lamp_x=250, lamp_y=380)
            b.boxer(k, 190, 470 - b.HY * 3.0, 3.0, "b_walk", "dawning", (1.6, 0.1))
            b.robot_glove(k, 452, 500, 3.0 * 0.8, math.pi + 0.06)
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
    sheet(d + "/uptimez-robot-on3-v1-sheet.png")
    phone(d + "/uptimez-robot-on3-v1-phone.png")
