"""CUSTOMER SUCCESS (episode 11): storyboard v5, from script v11, with props v4. From the storyboard v3 review (Tomas,
20 Nov): Don gets three faces (smug when he approves unread, a flash of panic at "Is this a joke?", pride the moment Pam
has fixed it); the pocket freeze is held, with a close on the strip in his hand; the call is about 3 s; Sofía's "He's
not looking at you." and Mom's nod are cut (Tomas chose); the ending runs Pam's line, "Still one star.", the wide.
Built on cs_board3 (v3/v4, kept).
  python3 cs_board5.py [out_dir]  ->  cs_storyboard_v5.png, cs_storyboard_v5_mute.png, cs_board_v5/*.png"""
import os
import sys
import cairo
import fs_storyboard as sb
import cs_props as cp
import cs_board as b1
import cs_board2 as b2
import cs_board3 as b3
from cs_board import S, at, base
from kit import Ctx, INK, rect

V = "v5"
F = sb.F


def f_1_4(k):                                              # smug: he approves without reading
    def ex(k, o):
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        from kit import ellipse
        ellipse(k, sx, sy, 0.80 * r, 0.62 * r, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        cp.T(k.c, "REPLY", sx, sy + 0.12 * r, 0.36 * r, col=cp.CYAN)
    S(k, (410, 650, 2.2), auto=False, portrait=False, extra=ex,
      **base(cl=False, sf=False, pm=False, mm=False, dn=at("don", pose="reach", face="smug", look=(1, -0.3))))


def f_3_5b(k):                                             # a flash of panic
    S(k, (452, 640, 3.0), auto=False, mic="down", portrait=False,
      **base(cl=False, sf=False, rb=False, pm=False, mm=False, dn=at("don", face="panic", look=(-1, 0))))


def f_4_3c(k):                                             # close: the strip in his hand, its 7 ringed in red
    c = k.c
    sb.bg(c, (0.42, 0.44, 0.24))                                            # his jacket behind
    c.save(); c.translate(270, 520); c.rotate(-0.25)
    rect(k, -70, -230, 140, 380, (0.18, 0.42, 0.85), 774, lw=4)
    c.set_source_rgb(*cp.RED); c.set_line_width(10); c.new_path(); c.arc(0, -40, 62, 0, 6.3); c.stroke()
    cp.T(c, "7", 0, 0, 120, col=(1, 1, 1))
    c.restore()
    from kit import ellipse
    rect(k, 120, 700, 330, 300, (0.86, 0.66, 0.50), 779, lw=3)              # his palm, from below
    for i, (x, y) in enumerate(((200, 662), (262, 650), (324, 656), (380, 676))):   # thick fingers over the strip's end
        ellipse(k, x, y, 30, 52, (0.86, 0.66, 0.50), 775 + i, lw=3)
        c.set_source_rgba(0.22, 0.17, 0.14, 0.5); c.set_line_width(3)       # oil in the creases
        c.move_to(x - 16, y + 10); c.line_to(x + 14, y + 14); c.stroke()


def f_5_4a(k):                                             # pride: the moment it's fixed, it was his
    S(k, (380, 620, 2.0), mic="down", portrait=False,
      **base(rb=False, sf=False, pm=False, mm=False, cl=at("client", x=300, pose="offer", face="plain", look=(1, 0)),
             dn=at("don", x=440, pose="reach", face="happy", look=(-1, 0))))


SHOTS = [
    ("1.1", 1.4, b3.f_1_1, "Every phone buzzes; every head turns to Don"),
    ("1.2", 2.4, b3.v3(b2.f_1_2), "The post: \"My lawyer will call.\""),
    ("1.4", 2.6, f_1_4, "ROBOT: \"Reply drafted...\" DON (smug, unread): \"Approved.\""),
    ("1.4b", 1.3, b3.v3(b2.f_1_4b), "\"Correct. We will recover.\""),
    ("2.1a", 0.5, b3.v3(b3.f_2_1a), "Calling 10 GARAGES"),
    ("2.1", 1.5, b2.f_2_1, "DON: \"Let's fix this together.\""),
    ("2.2", 1.5, b2.f_2_2, "CLIENT (phone): \"Nine o'clock. Your office.\""),
    ("3.1", 2.8, b2.f_3_1, "ROBOT: \"Blueprint generated...\" DON: \"Approved.\""),
    ("3.2", 1.0, b2.f_3_2, "9:00: he walks in, past her"),
    ("3.3", 1.0, b2.f_3_3, "DON: \"Recovered.\""),
    ("3.4", 2.0, b3.f_3_4, "99% CONFIDENT: the silhouette"),
    ("3.5", 1.6, b3.f_3_5, "CLIENT: \"Is this a joke?\""),
    ("3.5b", 0.6, f_3_5b, "Don: a flash of panic"),
    ("4.1", 1.3, b3.f_4_1, "He turns to go; Pam steps into his way"),
    ("4.2", 1.3, b2.f_4_2, "The taped plan: the hole at 7"),
    ("4.3a", 1.4, b3.f_4_3a, "His pocket: he freezes"),
    ("4.3c", 1.0, f_4_3c, "The 7, in his own hand"),
    ("4.3b", 1.5, b2.f_4_3b, "6 turned back, 7 in, Pam tapes it"),
    ("4.4", 2.6, b3.f_4_4, "ROBOT: \"...obtained by a h-human.\" HUMAN ✓"),
    ("5.1", 1.4, b2.f_5_1, "His back to Sofía. CLIENT: \"Your number.\""),
    ("5.2", 1.4, b2.f_5_2, "Pam writes her number on the tape"),
    ("5.3", 0.9, lambda k: cp.phone(k, "contact3"), "Contact saved: Pam, 555 0142"),
    ("5.4a", 1.2, f_5_4a, "Don, proud: \"Customer success.\""),
    ("5.4b", 1.0, b3.f_5_4b, "Pam straightens his mic; he doesn't notice"),
    ("6.1", 1.0, b2.f_6_1, "At the door, typing"),
    ("6.2", 2.0, b3.v3(b2.f_6_2), "UPDATE: Pam found it. Still one star"),
    ("6.3", 1.2, b2.f_6_3, "Pam: face down, the peek"),
    ("6.3b", 1.6, b3.v3(b2.f_6_3b), "PAM: \"Some post. Others find.\""),
    ("6.5", 1.4, b3.f_6_5, "SOFÍA: \"Still one star.\""),
    ("6.6", 1.0, b3.f_6_6, "Every phone buzzing; Don, praise (= frame 0)"),
]


def frames(d):
    os.makedirs(d, exist_ok=True)
    out = {}
    old = cp.PROPS4[0]
    cp.PROPS4[0] = True                                                     # props v4
    try:
        with b3._ep11v3():
            for shot, ln, fn, _ in SHOTS:
                s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
                c = cairo.Context(s); k = Ctx(c, 0)
                sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
                fn(k)
                s.write_to_png("%s/cs_board_%s.png" % (d, shot))
                out[shot] = s
    finally:
        cp.PROPS4[0] = old
    return out


def sheet(out, surfs, mute=False):
    old = b1.SHOTS, b1.V, b1.SCRIPT[0]
    b1.SHOTS, b1.V, b1.SCRIPT[0] = SHOTS, V, "script v11"
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
