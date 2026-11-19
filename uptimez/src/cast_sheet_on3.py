"""Model sheet and phone check for Pam (the corner) and the Referee in Office Noir 3: The Last Round (cast_on3 v4, sheet v5; cast_sheet_on3_v1.py to _v4.py draw the sheets v1 to v4).
Sheet v5: Pam at work on him. Two panels in the dream's look, her hands placed on the Client: 5.1 (she pulls the robe
off his shoulder; the sleeve stops at the glove) and 6.1 (medium, he sits, she tapes his brow). Her poses alone on a
sheet reached at nothing. The phone check is unchanged, so v4's stands and no v5 is written..
Sheet: each beside the Office Noir 2 figure it comes from, their poses, faces close, the silhouette check (the Referee
beside the Client, as black shapes), the corner as the dream shows it, the whole cast at its relative sizes, the rules.
Phone: each figure alone at three sizes, in the dream's look (the rule from the robot's sheet v2 on).
Usage: python3 cast_sheet_on3.py [out_dir]  ->  uptimez-corner-on3-v5-sheet.png"""
import sys
import math
import cairo
import kit
import noir2_cast as n2
import cast_on3 as ca
import client_on3 as b
import robot_on3 as r
import mom_on3 as q
import sofia_on3 as so3
import cand_bc as cb
import sofia_sheet_on3 as ssh
import client_sheet_on3 as csh
from kit import Ctx, INK

PAPER = (0.95, 0.93, 0.88)
WALL = kit.WALL
label = ssh.label
noir = csh.noir


def ring(c, w, h, floor, lamp_x=None, lamp_y=None):
    """v4: the placeholder ring for this sheet (sofia_sheet_on3.ring draws as before). The ringside is one low dark
    mass with a few uneven hats, not a row of equal boxes, and the three ropes are plain bright lines in front of it.
    The real ring is the set's job."""
    lamp_x = w / 2 if lamp_x is None else lamp_x
    c.set_source_rgb(0.13, 0.13, 0.15); c.rectangle(0, 0, w, h); c.fill()
    ly = floor - h * 0.45 if lamp_y is None else lamp_y
    g = cairo.RadialGradient(lamp_x, ly, 10, lamp_x, ly, h * 0.75)
    g.add_color_stop_rgba(0, 0.74, 0.74, 0.76, 1); g.add_color_stop_rgba(0.55, 0.42, 0.42, 0.45, 1)
    g.add_color_stop_rgba(1, 0.13, 0.13, 0.15, 1)
    c.set_source(g); c.rectangle(0, 0, w, floor); c.fill()
    c.set_source_rgb(0.10, 0.10, 0.12)
    c.rectangle(0, floor - 40, w, 40); c.fill()
    x, i = -10.0, 0
    while x < w + 30:
        r = (13, 17, 11, 15, 19, 12)[i % 6]; top = floor - 40 - (4, 12, 0, 9, 5, 14)[i % 6]
        c.arc(x, top, r, 0, 6.2832); c.fill()
        if i % 3 != 1:
            c.rectangle(x - r * 1.5, top - r * 0.7, r * 3, 4); c.fill(); c.rectangle(x - r * 0.9, top - r * 1.6, r * 1.8, r); c.fill()
        x += (52, 78, 44, 96, 60, 70)[i % 6]; i += 1
    c.set_source_rgb(0.62, 0.62, 0.64); c.rectangle(0, floor - 8, w, h - floor + 8); c.fill()
    c.set_source_rgb(0.90, 0.90, 0.92)
    for ry in (floor - 96, floor - 64, floor - 32):
        c.rectangle(0, ry, w, 6); c.fill()
    c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(0, floor - 8, w, 4); c.fill()


def silhouette(c, w, h, draw):
    """draw(k) on a clear surface; its shape is laid down in black."""
    f = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); cc = cairo.Context(f); draw(Ctx(cc, 0))
    c.set_source_rgb(0.03, 0.03, 0.04); c.mask_surface(f, 0, 0)


def _reach(px_, feet, s, left, right):
    """Pam's arms as a pose, her hands at two points of the frame (left: her screen-left hand)."""
    (ax, ay), (bx, by) = left, right
    return ca._ik(-1, (ax - px_) / s, (ay - feet) / s) + ca._ik(1, (bx - px_) / s, (by - feet) / s)


def panel_51(w, h):
    """5.1: she pulls the robe back off his shoulder; the sleeve stops at the glove."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s); k = Ctx(c, 0)
    ring(c, w, h, h - 24, lamp_x=w * 0.45)
    sc, F = 0.92, h - 12
    cx, px_ = w * 0.36, w * 0.36 + 118 * sc
    ca.bucket(k, w * 0.90, F - 2, 0.7)
    o = b.boxer(k, cx, F, sc * b.REL, "b_walk", "hard", (0.2, -0.6))
    sy = F + (b.BT + 26) * sc * b.REL                                     # his shoulder line
    sx = cx + (b.SH[0] - 6) * sc * b.REL
    ca.pam_corner(k, px_, F, sc, _reach(px_, F, sc, (sx - 6 * sc, sy + 2 * sc), (sx + 16 * sc, sy + 34 * sc)), "curious", (-0.9, 0.3))
    noir(s)
    return s


def panel_61(w, h):
    """6.1, medium, square on: he sits (the frame cuts at his chest), she tapes his brow."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s); k = Ctx(c, 0)
    ring(c, w, h, h + 300, lamp_x=w * 0.4, lamp_y=h * 0.55)
    sc = 1.25
    F = h + 120                                                           # her feet, far below the frame
    cx, cf = w * 0.30, F + 92 * sc                                        # he is on the stool: lower by a seat
    px_ = cx + 120 * sc
    o = b.boxer(k, cx, cf, sc * b.REL, "b_walk", "hard", (0.6, 0.2), tape=True)
    hx, hy = o["head"]
    bx, by = hx + 34 * sc * b.REL, hy - 34 * sc * b.REL                   # the end of the tape, on his brow
    ca.pam_corner(k, px_, F, sc, _reach(px_, F, sc, (bx + 4 * sc, by + 2 * sc), (bx + 40 * sc, by + 20 * sc)), "neutral", (-0.9, 0.2), tape=True)
    noir(s)
    return s


def lineup(c, k, x0, y0, w, h):
    c.save(); c.rectangle(x0, y0, w, h); c.clip(); c.set_source_rgb(*WALL); c.paint()
    c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(x0, y0 + h - 30, w, 30); c.fill()
    F, S = y0 + h - 26, 0.62
    xs = [x0 + w * t for t in (0.09, 0.25, 0.42, 0.57, 0.73, 0.89)]
    q.queen(k, xs[0], F, S, "q_stand", "bored")
    so3.sofia(k, xs[1], F, S, "r_hips", "spotted", (1, 0))
    b.boxer(k, xs[2], F, S * b.REL, "b_walk", "hard", (0.3, 0))
    ca.pam_corner(k, xs[3], F, S, "p_stand", "neutral", (-0.5, 0))
    ca.referee(k, xs[4], F, S * ca.REL_REF, "ref_stand")
    r.robot(k, xs[5], F, S * r.REL, "r_wait", "furious", side=-1)
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0, y0, w, h); c.stroke()


def sheet(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.set_source_rgb(*INK)
    c.move_to(50, 70); c.show_text("PAM AND THE REFEREE · Office Noir 3: The Last Round · v5 · the corner and the ring")
    c.select_font_face("Inter", 0, 0); c.set_font_size(22)
    c.move_to(50, 106); c.show_text("PAM, his cutman: the flat cap and apron of Office Noir 2 · a towel on her shoulder · a cotton bud behind her ear · a stopwatch on a cord, held up for the count · tape, a bucket, a sponge")
    c.move_to(50, 136); c.show_text("THE REFEREE: the Bartender of Office Noir 2 without his glass · white shirt, black bow tie, bare forearms · the only bare hands in the ring")
    F, SP, SR = 740, 1.0, 0.64
    n2.LOOK[0], old = 9, n2.LOOK[0]
    try:
        n2.sweeper(k, 120, F, SP, "lean", "neutral", (0.6, 0.1))
    finally:
        n2.LOOK[0] = old
    label(c, "Noir 2", 120, F + 42, 22)
    ca.pam_corner(k, 320, F, SP, "p_stand", "neutral", (0.4, 0)); label(c, "the corner", 320, F + 42, 22)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(425, 170); c.line_to(425, F + 50); c.stroke()
    ca.pam_corner(k, 570, F, SP, "p_tape", "neutral", (-0.8, 0)); label(c, "p_tape (6.1)", 560, F + 42, 20)
    ca.pam_corner(k, 730, F, SP, "p_pull", "curious", (-0.8, 0.2)); label(c, "p_pull (5.1)", 722, F + 42, 20)
    ca.pam_corner(k, 895, F, SP, "p_sponge", "knowing", (-0.6, 0)); label(c, "p_sponge (6.1)", 890, F + 42, 20)
    ca.pam_corner(k, 1070, F, SP, "p_watch", "neutral", (-0.7, 0.2)); label(c, "p_watch (5.2, 5.6)", 1062, F + 42, 20)
    ca.bucket(k, 1150, F - 2, 0.6)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(1175, 170); c.line_to(1175, F + 50); c.stroke()
    n2.bartender(k, 1265, F, SR, look=(-0.6, 0), clean=True); label(c, "Noir 2", 1265, F + 42, 22)
    for x, p, kw, t in ((1437, "ref_stand", dict(), "ref_stand"), (1607, "ref_bell", dict(), "ref_bell (5.2)"),
                        (1790, "ref_count", dict(count=3), "ref_count (5.6)"), (2085, "ref_break", dict(brow=True), "ref_break (7.2b)")):
        ca.referee(k, x, F, SR, p, **kw); label(c, t, x, F + 42, 22)
    for i, (f, lk, t) in enumerate((("neutral", (-0.6, 0), "neutral"), ("curious", (-0.8, 0.2), "curious"), ("knowing", (-0.8, 0), "knowing"))):
        x = 150 + 270 * i; y0 = 880
        c.save(); c.rectangle(x - 125, y0, 250, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()
        ca.pam_corner(k, x - 6, y0 + 215 - ca.HY * 2.1, 2.1, "p_stand", f, lk)
        c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, y0, 250, 380); c.stroke()
        label(c, "Pam · " + t, x, y0 + 415, 22)
    for i, (br, t) in enumerate(((False, "Referee · plain"), (True, "Referee · the eyebrow"))):
        x = 960 + 270 * i; y0 = 880
        c.save(); c.rectangle(x - 125, y0, 250, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()
        ca.referee(k, x, y0 + 200 - cb.M_HY * 1.75, 1.75, "ref_stand", look=(-0.8, 0.1), brow=br)
        c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, y0, 250, 380); c.stroke()
        label(c, t, x, y0 + 415, 22)
    x0, y0, w, h = 1500, 880, 640, 380                                    # the silhouette check
    c.save(); c.rectangle(x0, y0, w, h); c.clip()
    g = cairo.RadialGradient(x0 + w / 2, y0 + 170, 10, x0 + w / 2, y0 + 170, 420)
    g.add_color_stop_rgba(0, 0.82, 0.82, 0.84, 1); g.add_color_stop_rgba(1, 0.36, 0.36, 0.40, 1)
    c.set_source(g); c.paint()
    S2 = 1.02
    silhouette(c, W, H, lambda kk: b.boxer(kk, x0 + 170, y0 + 360, S2 * b.REL, "b_walk", "hard"))
    silhouette(c, W, H, lambda kk: ca.referee(kk, x0 + 470, y0 + 360, S2 * ca.REL_REF, "ref_stand"))
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0, y0, w, h); c.stroke()
    label(c, "silhouettes: the Client, the Referee", x0 + w / 2, y0 + 415, 22)
    for x0, fn in ((60, panel_51), (415, panel_61)):
        c.set_source_surface(fn(345, 340), x0, 1330); c.paint()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0, 1330, 345, 340); c.stroke()
    lineup(c, k, 790, 1330, 700, 340)
    c.select_font_face("Inter", 0, 0); c.set_font_size(20); c.set_source_rgb(*INK)
    notes = ["Rules",
             "· Pam is on his side and says one line. She fixes him;",
             "  she never looks at the plan over the ring.",
             "· Her tape is the tape that mends his plan in episode 11.",
             "· The towel and the cotton bud are hers in every corner",
             "  shot. The stopwatch: started on the bell, held up for",
             "  the count. The bucket stands by the post.",
             "· The Referee sees everything and does nothing. His face",
             "  is plain; the one eyebrow is his only reaction (6.4).",
             "· His hands are bare: fingers to count, a flat palm for",
             "  \"Break!\". He never touches the robot.",
             "· Panels: 5.1, 6.1 (her hands on him), the cast at its sizes."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(1520, 1362 + 30 * i); c.show_text(t)
    s.write_to_png(out)


def phone(out):
    rows = []
    specs = ((lambda k, x, f, sc, **kw: ca.pam_corner(k, x, f, sc, **kw), ca.HY, 1.0,
              (("wide", "Pam, full figure", dict(pose="p_stand", face="neutral", look=(-0.5, 0))),
               ("medium", "Pam, the count", dict(pose="p_watch", face="neutral", look=(-0.7, 0.2))),
               ("close", "Pam, her one line", dict(pose="p_stand", face="knowing", look=(-0.8, 0))))),
             (lambda k, x, f, sc, **kw: ca.referee(k, x, f, sc, **kw), cb.M_HY, ca.REL_REF,
              (("wide", "the Referee, full figure", dict(pose="ref_stand")),
               ("medium", "the Referee, counting", dict(pose="ref_count", count=3)),
               ("close", "the Referee, the eyebrow", dict(pose="ref_stand", brow=True)))))
    for fn, hy, rel, shots in specs:
        for (name, txt, kw), sc0 in zip(shots, (1.5, 2.6, 4.2)):
            sc = sc0 * rel
            f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
            if name == "wide":
                feet = 860
            elif name == "medium":
                feet = 420 - hy * sc + 150
            else:
                feet = 440 - hy * sc
            x = 300 if (name == "medium" and rel == 1.0) else (230 if name == "medium" else 270)
            ring(c, 540, 960, 860 if name == "wide" else 1500, lamp_x=270, lamp_y=feet + hy * sc)
            fn(k, x, feet, sc, **kw)
            noir(f)
            rows.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 2 * 560); c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(rows):
        ox, oy = 20 + (i % 3) * 290, 20 + (i // 3) * 560
        c.save(); c.translate(ox, oy); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(ox, oy + 502); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(ox, oy + 522); c.show_text(txt)
    s.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../characters"
    sheet(d + "/uptimez-corner-on3-v5-sheet.png")
