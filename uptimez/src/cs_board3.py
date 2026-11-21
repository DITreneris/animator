"""CUSTOMER SUCCESS (episode 11): storyboard v3, from script v10: the AI's site plan (its silhouette) and "Is this a
joke?", Pam stopping him at the door, his pocket and his embarrassed face, the robot's HUMAN ✓, Pam's hand on Don's mic
in its own shot, Mom over her shoulder onto Pam, "Still one star." and the end on the wide (= frame 0). The v2 cold
test's fixes (customer-success/cs_board_mute_test_v2.md) are in; no confetti on the floor.
Built on cs_board2 (v2, kept: it still draws storyboard v2).
  python3 cs_board3.py [out_dir]  ->  cs_storyboard_v3.png, cs_storyboard_v3_mute.png, cs_board_v3/*.png
  python3 cs_board3.py [out_dir] v4  ->  storyboard v4: the same frames with props v4 (the third props review)"""
import math
import os
import sys
import cairo
import fs_storyboard as sb
import cs_props as cp
import cs_board as b1
import cs_board2 as b2
from cs_board import S, at, base, roll
from cs_board2 import pam_at, buzz, phone_in, blue_sheet, _wide
from kit import Ctx, INK, ellipse, rect

V = "v3"
F = sb.F


class _ep11v3(b2._ep11v2):
    def __enter__(self):
        super().__enter__()
        self.conf = sb.fd.s3.confetti
        sb.fd.s3.confetti = lambda *a, **kw: None                            # the v2 test: confetti read as shredding
        return self

    def __exit__(self, *e):
        sb.fd.s3.confetti = self.conf
        super().__exit__(*e)


def flush(k, who, a=0.35):
    """Red from the collar up: embarrassed, or insulted."""
    x, y, r = sb.HEADS[who]
    c = k.c
    g = cairo.RadialGradient(x, y + 0.3 * r, 0, x, y + 0.3 * r, 1.0 * r)
    g.add_color_stop_rgba(0, 0.95, 0.25, 0.25, a); g.add_color_stop_rgba(1, 0.95, 0.25, 0.25, 0.0)
    c.set_source(g); c.arc(x, y + 0.3 * r, 1.0 * r, 0, 6.3); c.fill()


def v3(fn):
    def w(k):
        old = cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0]
        cp.REPLY_BIG[0] = cp.SAME_LAYOUT[0] = cp.GARAGE_LOGO[0] = True
        try:
            fn(k)
        finally:
            cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0] = old
    return w


def f_1_1(k):                                              # every phone buzzes; every head turns to Don
    _wide(k, looks=dict(sofia=(-1, 0), pam=(-1, 0.1), mom=(-1, 0), sofia_face="caught"), dn=at("don", face="grin", look=(0, 0)))


def f_2_1a(k):
    cp.phone2(k, "calling")


def f_3_4(k):
    cp.ai_site(k)


def f_3_5(k):                                              # "Is this a joke?" red from the collar up
    S(k, (250, 640, 3.0), auto=False, portrait=False,
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", face="suspicious", look=(1, 0))))
    flush(k, "client", 0.40)


def f_4_1(k):                                              # he turns for the door; Pam steps into his way
    S(k, (210, 640, 2.0), auto=False, portrait=False, pre=pam_at(150, front=True, face="neutral", look=(1, 0), glasses="up"),
      **base(door=0.6, rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", x=250, face="suspicious", look=(-1, 0))))
    roll(k, "pam", dx=1.0, dy=1.9, ang=0.3)


def f_4_3a(k):                                             # the 7 out of HIS pocket; he freezes, embarrassed
    def ex(k, o):
        hx, hy = o["client"]["hands"][1]
        c = k.c
        c.save(); c.translate(hx, hy - 20); c.rotate(-0.35)
        rect(k, -14, -60, 28, 76, (0.18, 0.42, 0.85), 773, lw=2)
        c.set_source_rgb(*cp.RED); c.set_line_width(3); c.new_path(); c.arc(0, -24, 13, 0, 6.3); c.stroke()
        cp.T(c, "7", 0, -15, 26, col=(1, 1, 1))
        c.restore()
    S(k, (250, 640, 2.8), auto=False, portrait=False, extra=ex,
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", pose="open", face="shock", look=(0.6, 0.8))))
    flush(k, "client", 0.30)


def f_4_4(k):                                              # a beat of defeat, then HUMAN ✓ at Pam
    def ex(k, o):
        hx, hy = o["robot"]["hands"][1]
        c = k.c
        c.save(); c.translate(hx + 10, hy - 30)
        rect(k, -34, -16, 68, 32, (1, 1, 1), 982, lw=2)
        cp.T(c, "HUMAN", -6, 6, 14, col=INK)
        c.set_source_rgb(*cp.GRN); c.set_line_width(3.5); c.set_line_cap(1)
        c.move_to(20, 0); c.line_to(25, 6); c.line_to(32, -6); c.stroke()
        c.restore()
    S(k, (420, 670, 2.0), auto=False, portrait=False, extra=ex, pre=pam_at(520, front=True, face="pleased", look=(-1, 0), glasses="up"),
      **base(cl=False, sf=False, dn=False, mm=False, pm=False, rb=at("robot", arm="none")))


def f_5_4a(k):                                             # Don takes the handshake
    S(k, (380, 620, 2.0), mic="down", portrait=False,
      **base(rb=False, sf=False, pm=False, mm=False, cl=at("client", x=300, pose="offer", face="plain", look=(1, 0)),
             dn=at("don", x=440, pose="reach", face="grin", look=(-1, 0))))


def f_5_4b(k):                                             # close: Pam's hand straightens his mic; his eyes on the Client
    def ex(k, o):
        c = k.c
        hx, hy = o["don"]["head"]
        s = sb.SC["don"]
        c.save(); c.translate(hx + 44 * s, hy - 10 * s)
        c.set_source_rgb(0.40, 0.26, 0.55); c.set_line_width(20 * s); c.set_line_cap(1)
        c.move_to(150 * s, 140 * s); c.line_to(70 * s, 64 * s); c.stroke()                         # her sleeve, shoved up
        c.set_source_rgb(0.96, 0.82, 0.70); c.set_line_width(15 * s)
        c.move_to(74 * s, 68 * s); c.line_to(14 * s, 8 * s); c.stroke()
        ellipse(k, 10 * s, 4 * s, 12 * s, 10 * s, (0.96, 0.82, 0.70), 999, lw=1.6)
        c.restore()
    S(k, (480, 664, 3.0), auto=False, mic="down", portrait=False, extra=ex,
      pre=pam_at(540, front=True, face="pleased", look=(-1, -0.3), glasses="up"),
      **base(cl=False, rb=False, sf=False, mm=False, dn=at("don", x=450, pose="reach", face="grin", look=(-1, 0))))


def f_5_5(k):                                              # "He's not looking at you."
    S(k, (500, 690, 3.0), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, pm=False, mm=False, sf=at("sofia", face="deadpan", look=(-1, 0))))


def f_6_4(k):                                              # over Mom's shoulder onto Pam and her lit phone
    import mom_fs as mfs

    def both(k_):
        pam_at(470, front=True, face="pleased", look=(-0.2, 1), glasses="up")(k_)
        mfs.mom(k_, 600, F + 120, sb.D("mom", 1.7), "bag", "sweet", look=(-1, 0.2))   # near the lens, in front of the counter
    S(k, (520, 640, 2.0), auto=False, portrait=False, counter_plan=False, pre=both,
      **base(cl=False, rb=False, dn=False, sf=False, pm=False, mm=False))
    phone_in(k, "pam", dx=0.1, dy=1.5, lit=True, s=1.0)


def f_6_5(k):                                              # "Still one star."
    S(k, (500, 690, 3.0), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, pm=False, mm=False, sf=at("sofia", pose="hold", face="deadpan", look=(0, 1))))
    phone_in(k, "sofia", dx=-0.2, dy=1.7, lit=True, s=1.1)
    x, y, r = sb.HEADS["sofia"]
    cp._stars(k.c, x - 0.95 * r, y + 1.15 * r, 1, 0.24 * r)


def f_6_6(k):                                              # = frame 0: every phone buzzing; Don, praise
    _wide(k, dn=at("don", pose="vest", face="grin", look=(0, 0.6)),
          looks=dict(sofia_face="deadpan", sofia=(0, 1), pam_face="pleased", pam=(-1, 0.2), mom=(-1, 0)))


SHOTS = [
    ("1.1", 1.4, f_1_1, "Every phone buzzes; every head turns to Don"),
    ("1.2", 2.5, v3(b2.f_1_2), "The post: \"My lawyer will call.\""),
    ("1.4", 2.6, b2.f_1_4, "ROBOT: \"Reply drafted...\" DON: \"Approved.\""),
    ("1.4b", 1.4, v3(b2.f_1_4b), "\"Correct. We will recover.\""),
    ("2.1a", 0.8, v3(f_2_1a), "Calling 10 GARAGES"),
    ("2.1", 1.8, b2.f_2_1, "DON: \"Let's fix this together.\""),
    ("2.2", 2.0, b2.f_2_2, "CLIENT (phone): \"Nine o'clock. Your office.\""),
    ("3.1", 3.0, b2.f_3_1, "ROBOT: \"Blueprint generated...\" DON: \"Approved.\""),
    ("3.2", 1.2, b2.f_3_2, "9:00: he walks in, past her"),
    ("3.3", 1.2, b2.f_3_3, "DON: \"Recovered.\""),
    ("3.4", 2.0, f_3_4, "The site plan: its silhouette"),
    ("3.5", 1.8, f_3_5, "CLIENT: \"Is this a joke?\""),
    ("4.1", 1.4, f_4_1, "He turns to go; Pam steps into his way"),
    ("4.2", 1.4, b2.f_4_2, "The taped plan: a hole at 7"),
    ("4.3a", 1.4, f_4_3a, "The 7 out of his pocket; he freezes"),
    ("4.3b", 1.6, b2.f_4_3b, "6 turned back, 7 in, Pam tapes it"),
    ("4.4", 2.8, f_4_4, "ROBOT: \"...obtained by a h-human.\" HUMAN ✓"),
    ("5.1", 1.6, b2.f_5_1, "His back to Sofía. CLIENT: \"Your number.\""),
    ("5.2", 1.6, b2.f_5_2, "Pam writes her number on the tape"),
    ("5.3", 1.0, lambda k: cp.phone(k, "contact3"), "Contact saved: Pam, 555 0142"),
    ("5.4a", 1.2, f_5_4a, "DON: \"Customer success.\""),
    ("5.4b", 1.0, f_5_4b, "Pam straightens his mic; he doesn't notice"),
    ("5.5", 1.4, f_5_5, "SOFÍA: \"He's not looking at you.\""),
    ("6.1", 1.2, b2.f_6_1, "At the door, typing"),
    ("6.2", 2.2, v3(b2.f_6_2), "UPDATE: Pam found it. Still one star"),
    ("6.3", 1.4, b2.f_6_3, "Pam: face down, the peek"),
    ("6.3b", 1.6, v3(b2.f_6_3b), "PAM: \"Some post. Others find.\""),
    ("6.4", 1.0, f_6_4, "Over Mom's shoulder: a nod to Pam"),
    ("6.5", 1.4, f_6_5, "SOFÍA: \"Still one star.\""),
    ("6.6", 1.2, f_6_6, "Every phone buzzing; Don, praise (= frame 0)"),
]


def frames(d):
    os.makedirs(d, exist_ok=True)
    out = {}
    with _ep11v3():
        for shot, ln, fn, _ in SHOTS:
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
            c = cairo.Context(s); k = Ctx(c, 0)
            sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
            fn(k)
            s.write_to_png("%s/cs_board_%s.png" % (d, shot))
            out[shot] = s
    return out


def sheet(out, surfs, mute=False):
    old = b1.SHOTS, b1.V, b1.SCRIPT[0]
    b1.SHOTS, b1.V, b1.SCRIPT[0] = SHOTS, V if not cp.PROPS4[0] else "v4", "script v10"
    try:
        b1.sheet(out, surfs, mute)
    finally:
        b1.SHOTS, b1.V, b1.SCRIPT[0] = old


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "v4"]
    if "v4" in sys.argv[1:]:                                              # board v4: v3's frames with props v4
        V = "v4"; cp.PROPS4[0] = True
    d = args[0] if args else "../customer-success"
    surfs = frames(os.path.join(d, "cs_board_%s" % V))
    sheet(os.path.join(d, "cs_storyboard_%s.png" % V), surfs)
    sheet(os.path.join(d, "cs_storyboard_%s_mute.png" % V), surfs, mute=True)
    print("wrote")
