"""CUSTOMER SUCCESS (episode 11): storyboard v6, from the five cold viewers of v5 (customer-success/cs_board_mute_test_v5.md;
Tomas chose, /grill-me): Pam points at the strip in his pocket before he pulls it out (4.2b, new); her roll is held
away from him (4.1); the robot's sheet is big (3.1); its sign reads FOUND BY: HUMAN with an arrow at Pam (4.4); the hands
meet in the handshake (5.4a); Don's mic in two frames, crooked with her fingers on it, then straight (5.4b, 5.4c);
Sofía turns her phone to us: one star (6.5). Built on cs_board5 (v5, kept).
  python3 cs_board6.py [out_dir]  ->  cs_storyboard_v6.png, cs_storyboard_v6_mute.png, cs_board_v6/*.png"""
import os
import sys
import cairo
import fs_storyboard as sb
import cs_props as cp
import cs_board as b1
import cs_board2 as b2
import cs_board3 as b3
import cs_board5 as b5
from cs_board import S, at, base, roll
from cs_board2 import pam_at, blue_sheet
from kit import Ctx, INK, ellipse, rect

V = "v6"
F = sb.F
SKIN_PAM = (0.96, 0.82, 0.70)
PURPLE = (0.40, 0.26, 0.55)


def f_3_1(k):                                              # the robot prints a blue sheet, big
    def ex(k, o):
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        blue_sheet(k, sx + 0.2 * r, sy + 2.2 * r, 2.8 * r, 3.4 * r, -0.08)
    S(k, (410, 650, 2.2), auto=False, portrait=False, extra=ex,
      **base(cl=False, sf=False, pm=False, mm=False, dn=at("don", pose="reach", face="smug", look=(-1, 0))))


def f_4_1(k):                                              # Pam in his way, the roll upright on her far side
    S(k, (210, 640, 2.0), auto=False, portrait=False, pre=pam_at(150, front=True, face="neutral", look=(1, 0), glasses="up"),
      **base(door=0.6, rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", x=260, face="suspicious", look=(-1, 0))))
    roll(k, "pam", dx=-0.75, dy=1.7, ang=1.35)


def _big_strip(k, o, pt):
    hx, hy = o["client"]["hands"][1]
    c = k.c
    c.save(); c.translate(hx - 2, hy - 30); c.rotate(-0.3)
    rect(k, -9, -30, 18, 44, (0.18, 0.42, 0.85), 776, lw=1.8)
    c.set_source_rgb(*cp.RED); c.set_line_width(1.8); c.new_path(); c.arc(0, -14, 7.5, 0, 6.3); c.stroke()
    cp.T(c, "7", 0, -9, 14, col=(1, 1, 1))
    c.restore()
    pt[:] = c.user_to_device(hx - 2, hy - 44)


def f_4_2b(k):                                             # Pam points at the strip in his pocket; he looks down
    pt = [0, 0]
    S(k, (220, 660, 2.6), auto=False, portrait=False, extra=lambda k_, o: _big_strip(k_, o, pt),
      pre=pam_at(140, front=True, face="neutral", look=(1, 0.6), glasses="up"),
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", x=280, pose="stand", face="puzzled", look=(0.3, 1))))
    x, y, r = sb.HEADS["pam"]
    c = k.c
    sx_, sy_ = x + 0.7 * r, y + 1.7 * r
    c.set_line_cap(1)
    for w, col in ((30, INK), (25, PURPLE)):                                # her sleeve, shoved up
        c.set_source_rgb(*col); c.set_line_width(w); c.move_to(sx_, sy_); c.line_to(sx_ + (pt[0] - sx_) * 0.45, sy_ + (pt[1] - sy_) * 0.45); c.stroke()
    for w, col in ((20, INK), (15, SKIN_PAM)):                              # her forearm and finger
        c.set_source_rgb(*col); c.set_line_width(w); c.move_to(sx_ + (pt[0] - sx_) * 0.45, sy_ + (pt[1] - sy_) * 0.45)
        c.line_to(pt[0] - 26, pt[1] + 4); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(3)                              # there
    for dy in (-34, -6, 22):
        c.move_to(pt[0] + 40, pt[1] + dy); c.line_to(pt[0] + 62, pt[1] + dy * 1.5); c.stroke()


def f_4_3a(k):                                             # his hand at his pocket, the strip coming out; he freezes
    pt = [0, 0]
    S(k, (250, 640, 2.8), auto=False, portrait=False, extra=lambda k_, o: _big_strip(k_, o, pt),
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", pose="stand", face="shock", look=(0.6, 0.8))))
    b3.flush(k, "client", 0.30)


def f_4_4(k):                                              # FOUND BY: HUMAN, an arrow at Pam
    def ex(k, o):
        hx, hy = o["robot"]["hands"][1]
        c = k.c
        c.save(); c.translate(hx + 26, hy - 34)
        rect(k, -44, -24, 88, 48, (1, 1, 1), 982, lw=2)
        cp.T(c, "FOUND BY:", 0, -5, 11, col=cp.GREY)
        cp.T(c, "HUMAN", 0, 15, 19, col=cp.GRN)
        c.set_source_rgb(*cp.GRN); c.set_line_width(5); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(50, 0); c.line_to(78, 0); c.stroke()
        c.move_to(68, -9); c.line_to(80, 0); c.line_to(68, 9); c.stroke()
        c.restore()
    S(k, (440, 670, 2.2), auto=False, portrait=False, extra=ex, pre=pam_at(520, front=True, face="pleased", look=(-1, 0), glasses="up"),
      **base(cl=False, sf=False, dn=False, mm=False, pm=False, rb=at("robot", arm="none")))


def f_5_4a(k):                                             # the hands meet; Don proud, the Client's eyes elsewhere
    def ex(k, o):
        (ax, ay), (bx, by) = o["client"]["hands"][1], o["don"]["hands"][0]
        mx, my = (ax + bx) / 2, min(ay, by) - 6
        c = k.c
        c.set_line_cap(1)
        for (px, py), col in (((ax, ay), (0.42, 0.44, 0.24)), ((bx, by), (0.98, 0.97, 0.94))):
            c.set_source_rgb(*INK); c.set_line_width(13); c.move_to(px, py); c.line_to(mx, my); c.stroke()
            c.set_source_rgb(*col); c.set_line_width(10); c.move_to(px, py); c.line_to(mx, my); c.stroke()
        ellipse(k, mx, my, 11, 8, (0.90, 0.72, 0.58), 983, lw=1.8)
    S(k, (385, 620, 2.2), mic="down", portrait=False, extra=ex,
      **base(rb=False, sf=False, pm=False, mm=False, cl=at("client", x=340, pose="open", face="plain", look=(0.2, 0.9)),
             dn=at("don", x=430, pose="stand", face="happy", look=(-1, 0))))


def _mic_shot(k, crooked, cam=(480, 664, 3.0), boom=(0.45, 0.45, 0.50)):
    """cam, boom (board v7, opt-in): a tighter camera and a boom colour that reads at phone size."""
    def signs(k_, head, s, mic, hair):
        if not crooked:
            orig(k_, head, s, "down", hair)
            if boom != (0.45, 0.45, 0.50):
                c = k_.c; hx, hy = head
                c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1)
                c.set_source_rgb(*boom); c.set_line_width(3.6); c.move_to(47, 10); c.curve_to(40, 40, 18, 40, 10, 32); c.stroke()
                c.restore()
            return
        orig(k_, head, s, "up", hair) if False else None
        c = k_.c
        hx, hy = head
        c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1)
        for w, col in ((6, INK), (3.2, boom)):               # the boom, hanging out and down
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(47, 10); c.curve_to(72, 22, 84, 48, 78, 78); c.stroke()
        ellipse(k_, 78, 78, 6.5, 5, (0.12, 0.12, 0.14), 711, shadow=False, lw=1.6)
        c.set_source_rgb(*INK); c.set_line_width(4.6)
        c.move_to(2, -50); c.curve_to(0, -74, 24, -84, 20, -67); c.curve_to(17, -57, 7, -64, 14, -70); c.stroke()
        c.restore()

    def ex(k_, o):
        c = k_.c
        hx, hy = o["don"]["head"]
        s = sb.SC["don"]
        tx, ty = (78, 78) if crooked else (70, 30)                           # her fingers: on the boom / leaving
        c.save(); c.translate(hx, hy); c.scale(s, s); c.set_line_cap(1)
        for w, col in ((24, INK), (20, PURPLE)):
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(210, 190); c.line_to(tx + 70, ty + 62); c.stroke()
        for w, col in ((19, INK), (15, SKIN_PAM)):
            c.set_source_rgb(*col); c.set_line_width(w); c.move_to(tx + 70, ty + 62); c.line_to(tx + 12, ty + 10); c.stroke()
        ellipse(k_, tx + 6, ty + 4, 12, 10, SKIN_PAM, 999, lw=1.6)
        if not crooked:                                                       # done: two small marks
            c.set_source_rgb(*INK); c.set_line_width(3)
            for a, b_ in ((24, 16), (30, 34)):
                c.move_to(10 + a, 32 + b_ - 30); c.line_to(18 + a, 32 + b_ - 38); c.stroke()
        c.restore()
    orig = sb.don_signs
    sb.don_signs = signs
    try:
        S(k, cam, auto=False, mic="down", portrait=False, extra=ex,
          pre=pam_at(545, front=True, face="neutral" if crooked else "pleased", look=(-1, -0.3), glasses="up"),
          **base(cl=False, rb=False, sf=False, mm=False, dn=at("don", x=450, pose="stand", face="happy", look=(-1, 0))))
    finally:
        sb.don_signs = orig


def f_5_4b(k):
    _mic_shot(k, True)


def f_5_4c(k):
    _mic_shot(k, False)


def f_6_5(k):                                              # her phone turned to us: one star
    S(k, (545, 690, 3.0), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, pm=False, mm=False, sf=at("sofia", pose="low", face="deadpan", look=(1, 0.2))))
    c = k.c
    c.save(); c.translate(390, 500); c.rotate(0.06)
    rect(k, -120, -200, 240, 400, (0.10, 0.11, 0.14), 984, lw=3)
    c.set_source_rgb(*cp.LIGHT); c.rectangle(-104, -180, 208, 360); c.fill()
    cp.T(c, "UptimeZ Find", 0, -110, 28)
    cp._stars(c, -84, -40, 1, 38)
    cp.T(c, "Pam found it.", 0, 50, 26, col=(0.55, 0.16, 0.46))
    c.restore()
    ellipse(k, 300, 690, 26, 20, (0.80, 0.56, 0.40), 985, lw=2)             # her hand on it


REPL = {"3.1": (f_3_1, None), "4.1": (f_4_1, None), "4.3a": (f_4_3a, "His hand at his pocket; he freezes"),
        "4.4": (f_4_4, "ROBOT: \"...obtained by a h-human.\" FOUND BY: HUMAN →"),
        "5.4a": (f_5_4a, None), "5.4b": (f_5_4b, "His mic hangs crooked; Pam's fingers on it"), "6.5": (f_6_5, None)}
SHOTS = []
for sh, ln, fn, note in b5.SHOTS:
    if sh in REPL:
        fn, note = REPL[sh][0], REPL[sh][1] or note
    if sh == "5.4b":
        ln = 0.8
    SHOTS.append((sh, ln, fn, note))
    if sh == "4.2":
        SHOTS.append(("4.2b", 1.0, f_4_2b, "Pam points at the strip in his pocket"))
    if sh == "5.4b":
        SHOTS.append(("5.4c", 0.7, f_5_4c, "Straight. He never noticed"))


def frames(d):
    old = b5.SHOTS
    b5.SHOTS = SHOTS
    try:
        return b5.frames(d)
    finally:
        b5.SHOTS = old


def sheet(out, surfs, mute=False):
    old = b1.SHOTS, b1.V, b1.SCRIPT[0]
    b1.SHOTS, b1.V, b1.SCRIPT[0] = SHOTS, V, "script v12"
    try:
        b1.sheet(out, surfs, mute)
    finally:
        b1.SHOTS, b1.V, b1.SCRIPT[0] = old


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    surfs = frames(os.path.join(d, "cs_board_%s" % V))
    sheet(os.path.join(d, "cs_storyboard_%s.png" % V), surfs)
    sheet(os.path.join(d, "cs_storyboard_%s_mute.png" % V), surfs, mute=True)
    print("wrote")
