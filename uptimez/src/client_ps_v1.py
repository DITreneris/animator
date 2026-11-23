"""THE CLIENT in "Pick a Side" (episode 14): his garage look from 13 (client_of), in Father's velvet booth, filthy with oil.
Tomas, 23 Nov, /grill-me: arms, face and shirt; leans in to point at the phone, then sits back and leaves a black
handprint on the velvet; bored, then the watch; the red rag over his shoulder, never used.
Nothing in client_of / client_ob changes: the oil goes in through client_of's own globals (its `limb`, for the forearm
and the hand) for the length of one call, and the rest is drawn over him.
  client(k, x, feet, s, pose="open", face="bored", look=(0, 0), turn=0.0)       client_of.client, oily
  cast_client(k, x, feet, s, look, targets, clip_hip, face)                     of_cast.client (IK arms), oily
  overlay(k, x, feet, s, turn=0.0)                                              the cheek, the shirt, the rag
  python3 client_ps.py [out_dir]  ->  ps_client_v1.png (sheet), ps_client_phone_v1.png (phone check)"""
import math
import os
import sys
from contextlib import contextmanager
import cairo
import kit
import client_ob as co
import client_of as cof
from kit import Ctx, INK, cut, rect, ellipse

OIL = (0.17, 0.13, 0.11)
OIL_SHINE = (0.42, 0.36, 0.32)
VELVET, VELVET_D = (0.42, 0.06, 0.12), (0.26, 0.03, 0.07)
TABLE, TABLE_D = (0.20, 0.12, 0.08), (0.12, 0.07, 0.05)


@contextmanager
def oily():
    """client_of draws its forearm and hand with SKIN through `limb`; for this call they are oil."""
    g = cof.client.__globals__
    old = g["limb"]

    def limb(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, *a, **kw):
        if col2 == co.SKIN:
            col2 = OIL
        if skin == co.SKIN:
            skin = OIL
        return old(k, sx, sy, a1, a2, ln1, ln2, w1, w2, col1, col2, skin, hand_r, seed, *a, **kw)
    g["limb"] = limb
    try:
        yield
    finally:
        g["limb"] = old


def overlay(k, x, feet, s, turn=0.0, seed=4400):
    """In his own units: the smear across his screen-left cheek, three blotches and a wiped handprint on the T-shirt,
    the red rag over his screen-right shoulder."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s * (1 - 0.18 * abs(turn)), s)
    hy, bt = co.HY, co.BT
    c.save(); c.translate(20 * turn, 0)
    c.set_source_rgba(*OIL, 0.80); c.set_line_cap(1)                   # the cheek: one wipe of a dirty thumb
    c.set_line_width(8); c.move_to(-50, hy - 2); c.curve_to(-46, hy + 8, -40, hy + 14, -32, hy + 20); c.stroke()   # up the outer cheek, away from the mouth
    c.set_line_width(4); c.move_to(-54, hy + 10); c.line_to(-46, hy + 22); c.stroke()
    c.restore()
    for (bx, by, r) in ((-34, bt + 70, 13), (30, bt + 112, 9), (-8, bt + 128, 7)):     # blotches on the white T-shirt
        c.set_source_rgba(*OIL, 0.85)
        c.save(); c.translate(bx, by); c.scale(1.0, 0.82); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); c.fill()
        c.arc(bx + r * 0.9, by + r * 0.5, r * 0.35, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(36, bt + 46); c.rotate(-0.35)                 # a handprint, wiped downward
    c.set_source_rgba(*OIL, 0.70)
    c.save(); c.scale(1, 1.2); c.arc(0, 0, 11, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_line_width(5.5)
    for i, fx in enumerate((-10, -4, 3, 10)):
        c.move_to(fx, -10); c.line_to(fx * 1.3, -26 - (3 if i in (1, 2) else 0)); c.stroke()
    c.set_line_width(4); c.move_to(-12, 4); c.line_to(-20, -4); c.stroke()
    c.set_source_rgba(*OIL, 0.35); c.set_line_width(14); c.move_to(0, 10); c.line_to(3, 34); c.stroke()
    c.restore()
    c.save(); c.translate(co.SH[0] - 18, bt + 6)                        # the rag over his shoulder, front and back
    cut(k, [(-14, -10), (18, -14), (26, 6), (20, 58), (8, 70), (2, 56), (-8, 66), (-14, 40)], co.RAG, lw=2.2)
    c.set_source_rgba(0.35, 0.08, 0.08, 0.6); c.set_line_width(1.6)
    for a_, b_ in (((-6, 10), (14, 24)), ((-8, 36), (10, 46))):
        c.move_to(*a_); c.line_to(*b_); c.stroke()
    c.set_source_rgba(*OIL, 0.5); c.arc(6, 30, 5, 0, 2 * math.pi); c.fill()
    c.restore()
    c.restore()


def client(k, x, feet, s=1.0, pose="open", face="bored", look=(0, 0), seed=900, turn=0.0):
    with oily():
        o = cof.client(k, x, feet, s, pose, face, look=look, seed=seed, turn=turn)
    overlay(k, x, feet, s, turn)
    return o


def cast_client(k, x, feet, s, look=(-1, 0), targets=(), clip_hip=False, face="bored"):
    import of_cast as oc
    with oily():
        o = oc.client(k, x, feet, s, look=look, targets=targets, clip_hip=clip_hip, face=face)
    overlay(k, x, feet, s)
    return o


# --- the booth (a wider version of 12's, for the two-shot 4.3) --------------------------------------------------------
def booth_room(k, w, h, seat_y, table_y, x0=0):
    """The velvet booth seen front on: the dark club, red neon, a buttoned burgundy bench back, a dark table in front."""
    import dh_props as dp
    c = k.c
    g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, 0.10, 0.02, 0.05); g.add_color_stop_rgb(1, 0.03, 0.01, 0.03)
    c.set_source(g); c.rectangle(x0, 0, w, h); c.fill()
    for yy, a in ((seat_y - 330, 0.9), (seat_y - 290, 0.55)):
        for wd, al in ((26, 0.10), (14, 0.22), (5, a)):
            c.set_source_rgba(*dp.NEON, al); c.set_line_width(wd); c.set_line_cap(1)
            c.move_to(x0 + 20, yy); c.line_to(x0 + w - 20, yy); c.stroke()
    top = seat_y - 250
    c.set_source_rgb(*VELVET); c.rectangle(x0 + 10, top, w - 20, seat_y - top + 40); c.fill()
    c.set_source_rgb(*VELVET_D); c.set_line_width(3)
    for i in range(1, int(w / 90) + 1):                                  # the channel tufting
        xx = x0 + 10 + i * 90
        c.move_to(xx, top + 10); c.line_to(xx, seat_y + 30); c.stroke()
        for yy in range(int(top + 40), int(seat_y), 70):
            c.arc(xx, yy, 4, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0 + 10, top, w - 20, seat_y - top + 40); c.stroke()


def table(k, w, table_y, x0=0, h=320):
    c = k.c
    rect(k, x0 - 10, table_y, w + 20, 26, TABLE, 4500, shadow=False, lw=2.4)
    c.set_source_rgb(*TABLE_D); c.rectangle(x0 - 10, table_y + 26, w + 20, h); c.fill()


def handprint(k, x, y, s=1.0, ang=0.2):
    """The black handprint he leaves on the velvet."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgba(*OIL, 0.92)
    c.save(); c.scale(1, 1.15); c.arc(0, 0, 14, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_line_cap(1); c.set_line_width(7)
    for i, (fx, ln) in enumerate(((-12, 18), (-4, 24), (5, 24), (13, 18))):
        c.move_to(fx, -10); c.line_to(fx * 1.25, -10 - ln); c.stroke()
    c.move_to(-14, 4); c.line_to(-28, -6); c.stroke()
    c.restore()


def phone_on_table(k, x, y, s=1.0, prints=True):
    """Bodyguard 1's phone propped up on the table (its bottom edge at y + 76 s), its screen to us: the #TeamDon post,
    and his oily prints on it (on Pam, then on the heel)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(k, -46, -76, 92, 152, (0.08, 0.08, 0.09), 4510, shadow=False, lw=2.2)
    c.set_source_rgb(0.95, 0.95, 0.97); c.rectangle(-40, -68, 80, 136); c.fill()
    c.set_source_rgb(0.86, 0.80, 0.68); c.rectangle(-36, -48, 72, 70); c.fill()                # the photo
    for px_, col in ((-22, (0.15, 0.25, 0.55)), (-6, (0.45, 0.25, 0.60)), (10, (0.99, 0.97, 0.91)), (24, (0.6, 0.6, 0.62))):
        c.set_source_rgb(*col); c.rectangle(px_ - 5, -36, 10, 50); c.fill()
    c.set_source_rgb(0.95, 0.78, 0.15); c.rectangle(15, 6, 3, 16); c.fill()                   # the tape in it
    c.set_source_rgb(0.2, 0.2, 0.25); c.select_font_face("Inter", 0, 1); c.set_font_size(11)
    c.move_to(-34, 40); c.show_text("#TeamDon")
    if prints:
        for (fx, fy) in ((-6, -20), (12, 16)):
            c.set_source_rgba(*OIL, 0.55); c.save(); c.translate(fx, fy); c.scale(1, 1.3); c.arc(0, 0, 7, 0, 2 * math.pi)
            c.restore(); c.fill()
    c.restore()


def sheet(out):
    import dh_cast as dc
    import fs_storyboard as sb
    W, H = 2200, 1820
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    k = Ctx(c, 0)
    cof._label(c, "PICK A SIDE · THE CLIENT · in Father's booth, filthy with oil · v1 · client_of's garage look, the same man", 40, 50, 30, center=False)
    cof._label(c, "Oil black to the elbows · a smear on his cheek · blotches and a wiped handprint on the white T-shirt · the red rag over his shoulder, never used",
               40, 84, 18, col=(0.3, 0.3, 0.3), center=False)
    cof._label(c, "1  The look, at the series' scale", 40, 140, 22, center=False)
    F = 640
    sb.don(k, 150, F, 0.60 / 0.52, "stand", "neutral", look=(1, 0))
    cof.client(k, 360, F, 1.0, "open", "bored", look=(-1, 0))
    client(k, 580, F, 1.0, "open", "bored", look=(-1, 0))
    dc.father(k, 800, F, 0.62 / 0.52, face="hard", look=(-1, 0))
    for x, n in ((150, "Don"), (360, "13: clean"), (580, "14: oily"), (800, "Father")):
        cof._label(c, n, x, 680)
    cof._label(c, "2  Faces", 1000, 140, 22, center=False)
    for i, (fc, lk, nm) in enumerate((("bored", (0, 0), "bored (rest)"), ("glance", cof.GLANCE, "the watch, at the end"))):
        c.save(); c.rectangle(1000 + i * 300, 170, 280, 300); c.clip()
        c.translate(1140 + i * 300, 340); c.scale(2.2, 2.2); c.translate(0, -co.HY)
        client(k, 0, 0, 1.0, "open", fc, look=lk)
        c.restore()
        cof._label(c, nm, 1140 + i * 300, 500)
    cof._label(c, "3  The booth, 4.3: he leans in and points, Father nods; he sits back: the handprint; the watch", 40, 780, 22, center=False)
    for j, (x0, title) in enumerate(((40, "4.3a · leans in, the black finger on the photo"), (1120, "4.3b · sits back: a black handprint on the velvet"))):
        PW, PH = 1040, 860
        c.save(); c.rectangle(x0, 820, PW, PH); c.clip()
        seat = 820 + 560
        tbl = seat - 30
        booth_room(k, PW, 820 + PH, seat, tbl, x0)
        dc.father(k, x0 + 300, seat + 170, 0.62 / 0.52 * 1.15, face="hard", look=(0.8 if j == 0 else 0.2, 0.4))
        s = 1.15
        hip_feet = seat - co.HIP * s
        phone_on_table(k, x0 + 520, tbl - 90, 1.2, prints=True)        # propped up behind his hand
        if j == 0:
            c.save(); c.translate(x0 + 720, seat); c.rotate(-0.10); c.translate(-(x0 + 720), -seat)
            cast_client(k, x0 + 720, hip_feet, s, look=(-1.2, 1.4), targets=[(x0 + 536, tbl - 118), (x0 + 760, tbl - 6)], clip_hip=True)
            c.restore()
        else:
            handprint(k, x0 + 870, seat - 120, 1.4, 0.25)
            import of_cast as oc
            cast_client(k, x0 + 700, hip_feet, s, look=cof.GLANCE, targets=oc.watch_pose(x0 + 700, hip_feet, s),
                        clip_hip=True, face="glance")
        table(k, PW, tbl, x0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0, 820, PW, PH); c.stroke()
        cof._label(c, title, x0 + PW / 2, 820 + PH + 34, 17)
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    import dh_cast as dc
    frames = []
    for name, txt in (("two-shot", "4.3: Father and the Client in the booth"), ("medium", "4.3: the finger, the oil"),
                      ("close", "the cheek, the shirt, the rag")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        if name == "two-shot":
            seat, tbl = 760, 720
            booth_room(k, 540, 960, seat, tbl)
            dc.father(k, 140, seat + 200, 0.62 / 0.52 * 1.25, face="hard", look=(0.8, 0.4))
            s = 1.25
            phone_on_table(k, 262, tbl - 92, 1.2)
            cast_client(k, 410, seat - co.HIP * s, s, look=(-1.2, 1.2), targets=[(262, tbl - 120), (420, tbl - 4)], clip_hip=True)
            table(k, 540, tbl)
        elif name == "medium":
            seat, tbl = 900, 870
            booth_room(k, 540, 960, seat, tbl)
            s = 1.7
            cast_client(k, 330, seat - co.HIP * s, s, look=(-1.2, 1.4), targets=[(130, tbl - 10), (330, tbl)], clip_hip=True)
            table(k, 540, tbl)
        else:
            booth_room(k, 540, 960, 1400, 1500)
            s = 2.6
            client(k, 290, 420 - co.HY * s, s, "open", "bored", look=(-0.6, 0))
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_client_v1.png"))
    phone(os.path.join(d, "ps_client_phone_v1.png"))
