"""CUSTOMER SUCCESS (episode 11): storyboard v2, from script v9 (the post is the crisis; the AI fails; Pam finds it; his
UPDATE), with the fixes of the v1 cold mute test (customer-success/cs_board_mute_test_v1.md): the shredder out of every
shot not about it; Mom at her desk in frame 0; the 7 strip out of *his* pocket; Sofía walked past with his back to her;
no near-identical robot frames. Pam, her episode (Tomas, /grill-me): glasses up and sleeves up from 4.1, Don's mic,
the phone face down and the peek, "Some post. Others find."
Built on cs_board (v1, kept: it still draws storyboard v1) and ep 10's board code.
  python3 cs_board2.py [out_dir]  ->  cs_storyboard_v2.png, cs_storyboard_v2_mute.png, cs_board_v2/*.png"""
import math
import os
import sys
import cairo
import kit
import fs_set as fs
import fs_storyboard as sb
import pam_bc as pb
import cs_props as cp
import cs_board as b1
from cs_board import S, at, base, robot_signs, calendar_on, roll
from kit import Ctx, INK, ellipse, rect

V = "v2"
F = sb.F
WIDE = (470, 560, 1.3)                                     # frame 0: the robot, Don, Sofía, Pam and Mom at the counter


class _ep11v2(b1._ep11):
    """v1's swaps, and: no monitor on the counter (it hid Mom and Pam), no shredder unless a shot asks for it."""
    def __enter__(self):
        super().__enter__()
        self.mon, self.shr = sb.fd.s3.monitor, sb.fd.shredder
        sb.fd.s3.monitor = lambda *a, **kw: None
        sb.fd.shredder = lambda *a, **kw: None
        return self

    def __exit__(self, *e):
        sb.fd.s3.monitor, sb.fd.shredder = self.mon, self.shr
        super().__exit__(*e)


def pam_at(x, front=False, face="neutral", look=(-1, 0), glasses="low", pose="stand"):
    """Pam behind the counter (back) or in front of it (pre)."""
    def draw(k):
        pb.pam(k, x, (F + 6) if front else (F - 66), 0.54, pose, face, look, glasses=glasses)
    return draw


def buzz(k, who=("don", "sofia", "pam", "mom", "robot")):
    """Every phone buzzing: zig-zags beside each head."""
    c = k.c
    c.set_source_rgb(*cp.RED); c.set_line_width(2.4); c.set_line_cap(1)
    for w in who:
        if w not in sb.HEADS:
            continue
        x, y, r = sb.HEADS[w]
        for sx in (-1, 1):
            x0 = x + sx * 1.35 * r
            c.move_to(x0, y - 0.5 * r)
            for i in range(4):
                c.line_to(x0 + sx * (0.18 * r if i % 2 == 0 else 0), y - 0.5 * r + (i + 1) * 0.25 * r)
            c.stroke()


def phone_in(k, who, dx=0.9, dy=1.6, lit=True, s=1.0, ang=-0.1, face_down=False):
    x, y, r = sb.HEADS[who]
    c = k.c
    c.save(); c.translate(x + dx * r, y + dy * r); c.rotate(ang); c.scale(s, s)
    if lit:
        c.set_source_rgba(0.6, 0.9, 1.0, 0.35); c.arc(0, 0, 0.9 * r, 0, 6.3); c.fill()
    rect(k, -0.32 * r, -0.55 * r, 0.64 * r, 1.1 * r, (0.10, 0.11, 0.14), 997, lw=1.6)
    if lit and not face_down:
        c.set_source_rgb(*cp.LIGHT); c.rectangle(-0.26 * r, -0.47 * r, 0.52 * r, 0.94 * r); c.fill()
        c.set_source_rgb(*cp.RED); c.rectangle(-0.20 * r, -0.10 * r, 0.40 * r, 0.06 * r); c.fill()
    c.restore()


def blue_sheet(k, x, y, w, h, ang=0.0):
    """The AI's glossy blueprint, seen in a shot (not the insert)."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(k, -w / 2, -h / 2, w, h, (0.20, 0.45, 0.85), 998, lw=2)
    c.set_source_rgb(1, 1, 1); c.set_line_width(max(1.0, w * 0.02))
    for i in range(4):
        for j in range(3):
            bx, by = -w / 2 + w * (0.14 + i * 0.22), -h / 2 + h * (0.22 + j * 0.27)
            c.move_to(bx - w * 0.06, by + h * 0.1); c.line_to(bx - w * 0.06, by); c.line_to(bx, by - h * 0.06)
            c.line_to(bx + w * 0.06, by); c.line_to(bx + w * 0.06, by + h * 0.1); c.stroke()
    c.restore()


# ---- the frames ---------------------------------------------------------------------------------------------------------

def _wide(k, buzzing=True, looks=None, dn=None, extra=None):
    lk = looks or {}
    S(k, WIDE, auto=False, back=lambda k_: (calendar_on(k_), pam_at(580, face=lk.get("pam_face", "neutral"), look=lk.get("pam", (-1, 0)))(k_)),
      extra=extra, **base(cl=False, door=0.0, rb=at("robot", arm="none"),
                          dn=dn or at("don", face="neutral", look=lk.get("don", (-1, 0.6))),
                          sf=at("sofia", pose="hold", face=lk.get("sofia_face", "smile"), look=lk.get("sofia", (0, 1))),
                          pm=False, mm=dict(x=650, x4=True, pose="bag", face="sweet", look=lk.get("mom", (-1, 0.5)))))
    if buzzing:
        buzz(k)


def f_1_1(k):                                              # frame 0: every phone buzzes at once
    _wide(k)


def f_1_2(k):
    cp.phone2(k, "crisis")


def f_1_3(k):                                              # every head turns to Don
    _wide(k, buzzing=False, looks=dict(sofia=(-1, 0), pam=(-1, 0.1), mom=(-1, 0), sofia_face="caught", pam_face="neutral"),
          dn=at("don", face="grin", look=(0, 0)))


def f_1_4(k):                                              # Don thumbs the robot's pad without reading
    def ex(k, o):
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        ellipse(k, sx, sy, 0.80 * r, 0.62 * r, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        cp.T(k.c, "REPLY", sx, sy + 0.12 * r, 0.36 * r, col=cp.CYAN)
    S(k, (410, 650, 2.2), auto=False, portrait=False, extra=ex,
      **base(cl=False, sf=False, pm=False, mm=False, dn=at("don", pose="reach", face="grin", look=(1, 0))))


def f_1_4b(k):
    cp.phone2(k, "reply")


def f_2_1(k):                                              # "Let's fix this together." mic down, the phone at his ear
    S(k, (452, 600, 2.6), auto=False, mic="down", portrait=False,
      **base(cl=False, sf=False, rb=False, pm=False, mm=False, dn=at("don", pose="thumb", face="grin", look=(-1, 0))))
    phone_in(k, "don", dx=1.15, dy=0.1, lit=True, s=1.0, ang=0.2)


def f_2_2(k):
    cp.phone2(k, "cal")


def f_3_1(k):                                              # "Blueprint generated." the robot prints a blue sheet
    def ex(k, o):
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        blue_sheet(k, sx + 0.1 * r, sy + 1.55 * r, 1.2 * r, 1.5 * r, -0.08)
    S(k, (410, 650, 2.2), auto=False, portrait=False, extra=ex,
      **base(cl=False, sf=False, pm=False, mm=False, dn=at("don", pose="reach", face="grin", look=(-1, 0))))


def f_3_2(k):                                              # 9:00: he walks in, past her lapel
    S(k, (330, 600, 1.9), portrait=False,
      **base(sf=at("sofia", x=330, pose="lapel", face="knowing", look=(-1, 0)),
             cl=at("client", x=220, face="plain", look=(1, 0)), rb=False, dn=False, pm=False, mm=False))


def f_3_3(k):                                              # "Recovered." Don unrolls the AI's sheet
    def ex(k, o):
        hx, hy = o["don"]["hands"][0]
        blue_sheet(k, hx - 30, hy - 20, 90, 110, 0.1)
    S(k, (380, 620, 1.8), portrait=False, extra=ex,
      **base(rb=False, sf=False, pm=False, mm=False, cl=at("client", x=280, face="plain", look=(1, 0.4)),
             dn=at("don", x=440, pose="tablet", face="grin", look=(-1, 0))))


def f_3_4(k):
    cp.ai_plan(k, True)


def f_3_5(k):                                              # "I have ten garages."
    S(k, (250, 640, 3.0), auto=False, portrait=False,
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", face="suspicious", look=(1, 0))))


def f_4_1(k):                                              # Pam comes out with the roll; glasses up, sleeves up
    S(k, (560, 640, 2.4), auto=False, portrait=False, counter_plan=False,
      pre=pam_at(560, front=True, face="neutral", look=(-1, 0), glasses="up"),
      **base(cl=False, rb=False, sf=False, dn=False, pm=False, mm=False))
    roll(k, "pam")


def f_4_2(k):
    cp.plan(k, "before")


def f_4_3a(k):                                             # the strip out of HIS pocket
    def ex(k, o):
        hx, hy = o["client"]["hands"][1]
        c = k.c
        c.save(); c.translate(hx, hy - 14); c.rotate(-0.4)
        rect(k, -8, -36, 16, 44, (0.18, 0.42, 0.85), 773, lw=1.6)
        cp.T(c, "7", 0, -6, 18, col=(1, 1, 1))
        c.restore()
    S(k, (250, 640, 2.8), auto=False, portrait=False, extra=ex,
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", pose="open", face="dawning", look=(0.6, 0.8))))


def f_4_3b(k):                                             # the 6 turned back, the 7 in, Pam's thumb tapes it
    cp.plan(k, "whole")
    sb.thumb(k, 250, 700, 1.3, who="pam")


def f_4_4(k):                                              # "...obtained by a h-human." the plan in front, the paddle green
    def ex(k, o):
        c = k.c
        c.save(); c.translate(o["robot"]["screen"][0] + 60, F + 30); c.scale(0.9, 0.9); fs.plan_patched(k, 0, 0, 1.0); c.restore()
    S(k, (400, 690, 2.5), auto=False, portrait=False, extra=ex,
      **base(cl=False, sf=False, dn=False, pm=False, mm=False, rb=at("robot", arm="paddle", paddle="green")))


def f_5_1(k):                                              # his back to Sofía; "Your number." to Pam
    S(k, (470, 640, 1.8), portrait=False, pre=pam_at(570, front=True, face="pleased", look=(-1, 0), glasses="up"),
      **base(rb=False, dn=False, mm=False, cl=at("client", x=480, face="plain", look=(1, 0)),
             sf=at("sofia", x=370, pose="lapel", face="interested", look=(1, 0))))
    phone_in(k, "client", dx=1.0, dy=1.4, lit=True)


def f_5_2(k):
    cp.plan(k, "number")


def f_5_3(k):
    cp.phone(k, "contact")


def f_5_4(k):                                              # Don takes the handshake; Pam straightens his mic; Sofía, low
    def ex(k, o):
        c = k.c
        hx, hy = o["don"]["head"]
        s = sb.SC["don"]
        c.save(); c.translate(hx + 44 * s, hy - 10 * s)                    # Pam's hand at his mic, her sleeve shoved up
        c.set_source_rgb(0.96, 0.82, 0.70); c.set_line_width(14 * s); c.set_line_cap(1)
        c.move_to(80 * s, 70 * s); c.line_to(12 * s, 6 * s); c.stroke()
        ellipse(k, 8 * s, 2 * s, 11 * s, 9 * s, (0.96, 0.82, 0.70), 999, lw=1.6)
        c.set_source_rgb(0.40, 0.26, 0.55); c.set_line_width(18 * s); c.move_to(120 * s, 110 * s); c.line_to(84 * s, 74 * s); c.stroke()
        c.restore()
    S(k, (440, 600, 2.0), mic="down", portrait=False, extra=ex, pre=pam_at(540, front=True, face="pleased", look=(-1, -0.3), glasses="up"),
      **base(cl=False, rb=False, mm=False, sf=at("sofia", x=380, face="deadpan", look=(1, 0)),
             dn=at("don", x=450, pose="reach", face="grin", look=(-1, 0))))


def f_6_1(k):                                              # at the door, his thumb typing
    S(k, (230, 620, 2.6), auto=False, portrait=False,
      **base(rb=False, sf=False, dn=False, pm=False, mm=False, cl=at("client", pose="open", face="plain", look=(0.4, 1))))
    phone_in(k, "client", dx=0.2, dy=1.6, lit=True, s=1.2)


def f_6_2(k):
    cp.phone2(k, "update")


def f_6_3(k):                                              # Pam: face down, then the peek, almost a smile
    S(k, (540, 650, 2.7), auto=False, portrait=False, counter_plan=False,
      pre=pam_at(540, front=True, face="pleased", look=(-0.2, 1), glasses="up"),
      **base(cl=False, rb=False, sf=False, dn=False, pm=False, mm=False))
    x, y, r = sb.HEADS["pam"]
    c = k.c
    g = cairo.RadialGradient(x, y, 0, x, y, 1.3 * r)                         # the screen's light on her face
    g.add_color_stop_rgba(0, 0.6, 0.9, 1.0, 0.35); g.add_color_stop_rgba(1, 0.6, 0.9, 1.0, 0.0)
    c.set_source(g); c.arc(x, y, 1.3 * r, 0, 6.3); c.fill()
    c.save(); c.translate(x + 0.15 * r, y + 1.45 * r); c.rotate(0.35)            # its back to us, tipped up: the peek
    rect(k, -0.42 * r, -0.62 * r, 0.84 * r, 1.24 * r, (0.10, 0.11, 0.14), 980, lw=2)
    c.set_source_rgba(0.6, 0.9, 1.0, 0.8); c.set_line_width(3); c.move_to(-0.42 * r, -0.62 * r); c.line_to(0.42 * r, -0.62 * r); c.stroke()
    c.restore()
    for hx in (-0.35, 0.6):                                                     # her hands on it
        ellipse(k, x + hx * r, y + 1.9 * r, 0.16 * r, 0.14 * r, (0.96, 0.82, 0.70), 981, lw=1.6)


def f_6_3b(k):
    cp.phone2(k, "pam")


def f_6_3c(k):                                             # = frame 0: Don reads it as praise
    _wide(k, dn=at("don", pose="vest", face="grin", look=(0, 0.6)),
          looks=dict(sofia_face="deadpan", sofia=(-1, 0), pam_face="pleased", pam=(-1, 0.2), mom=(-1, 0)))


def f_6_4(k):                                              # Mom: Don, then the nod to Pam
    S(k, (650, 600, 2.8), auto=False, portrait=False, counter_plan=False,
      **base(cl=False, rb=False, dn=False, sf=False, pm=False, mm=dict(x=650, x4=True, pose="bag", face="sweet", look=(-1, 0))))


def f_6_5(k):                                              # "Nobody noticed."
    S(k, (500, 690, 3.0), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, pm=False, mm=False, sf=at("sofia", pose="lapel", face="deadpan", look=(1, 0))))


SHOTS = [
    ("1.1", 0.8, f_1_1, "Every phone buzzes at once"),
    ("1.2", 2.5, f_1_2, "The post: \"My lawyer will call.\""),
    ("1.3", 1.0, f_1_3, "Every head turns to Don"),
    ("1.4", 2.6, f_1_4, "ROBOT: \"Reply drafted...\" DON: \"Approved.\""),
    ("1.4b", 1.4, f_1_4b, "\"Correct. We will recover.\""),
    ("2.1", 2.0, f_2_1, "DON (phone): \"Let's fix this together.\""),
    ("2.2", 2.2, f_2_2, "CLIENT (phone): \"Nine o'clock. Your office.\""),
    ("3.1", 3.0, f_3_1, "ROBOT: \"Blueprint generated...\" DON: \"Approved.\""),
    ("3.2", 1.2, f_3_2, "9:00: he walks in, past her"),
    ("3.3", 1.2, f_3_3, "DON: \"Recovered.\""),
    ("3.4", 1.6, f_3_4, "12 garages; 7 a car wash"),
    ("3.5", 2.0, f_3_5, "CLIENT: \"I have ten garages.\""),
    ("4.1", 1.4, f_4_1, "Pam comes out with the roll"),
    ("4.2", 1.4, f_4_2, "The taped plan: a hole at 7"),
    ("4.3a", 1.2, f_4_3a, "The 7 out of his pocket"),
    ("4.3b", 1.6, f_4_3b, "6 turned back, 7 in, Pam tapes it"),
    ("4.4", 2.6, f_4_4, "ROBOT: \"...obtained by a h-human.\""),
    ("5.1", 1.6, f_5_1, "His back to Sofía. CLIENT: \"Your number.\""),
    ("5.2", 1.6, f_5_2, "Pam writes her number on the tape"),
    ("5.3", 1.0, f_5_3, "PAM · FINDS THINGS"),
    ("5.4", 2.8, f_5_4, "SOFÍA: \"He's not looking...\" DON: \"Customer success.\" Pam fixes his mic"),
    ("6.1", 1.2, f_6_1, "At the door, typing"),
    ("6.2", 2.2, f_6_2, "UPDATE: Pam found it."),
    ("6.3", 1.6, f_6_3, "Pam: face down, the peek"),
    ("6.3b", 1.6, f_6_3b, "PAM: \"Some post. Others find.\""),
    ("6.3c", 1.2, f_6_3c, "Don: praise. (= frame 0)"),
    ("6.4", 1.0, f_6_4, "Mom: Don, then a nod to Pam"),
    ("6.5", 1.6, f_6_5, "SOFÍA: \"Nobody noticed.\""),
]


def frames(d):
    os.makedirs(d, exist_ok=True)
    out = {}
    with _ep11v2():
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
    b1.SHOTS, b1.V, b1.SCRIPT[0] = SHOTS, V, "script v9"
    try:
        b1.sheet(out, surfs, mute)
    finally:
        b1.SHOTS, b1.V, b1.SCRIPT[0] = old


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../customer-success"
    surfs = frames(os.path.join(d, "cs_board_v2"))
    sheet(os.path.join(d, "cs_storyboard_%s.png" % V), surfs)
    sheet(os.path.join(d, "cs_storyboard_%s_mute.png" % V), surfs, mute=True)
    print("wrote")
