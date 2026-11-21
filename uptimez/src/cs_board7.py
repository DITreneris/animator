"""CUSTOMER SUCCESS (episode 11): storyboard v7, the weak points of v6 (two cold viewers; Tomas chose, /grill-me):
5.4a Don shakes the Client's hand, beaming, while the Client looks away at Pam; 5.4b-c tight on Don's head and the mic,
the boom in orange; 6.5 a phone in Sofía's hand, the five stars filling it; 6.6 the same wide, but Pam's phone glows
in her hand and she alone smiles, glasses up. Built on cs_board6 (v6, kept).
  python3 cs_board7.py [out_dir]  ->  cs_storyboard_v7.png, cs_storyboard_v7_mute.png, cs_board_v7/*.png"""
import os
import sys
import fs_storyboard as sb
import cs_props as cp
import cs_board as b1
import cs_board2 as b2
import cs_board3 as b3
import cs_board5 as b5
import cs_board6 as b6
from cs_board import S, at, base
from cs_board2 import pam_at, phone_in
from kit import INK, ellipse, rect

V = "v7"
F = sb.F
ORANGE = (0.95, 0.45, 0.15)


def f_5_4a(k):                                             # Don shakes and beams; the Client looks at Pam
    def ex(k, o):
        a = max(o["client"]["hands"], key=lambda p: p[0]); d = min(o["don"]["hands"], key=lambda p: p[0])
        mx, my = (a[0] + d[0]) / 2, min(a[1], d[1]) - 14
        c = k.c
        c.set_line_cap(1)
        for (px, py), col in ((a, (0.42, 0.44, 0.24)), (d, (0.98, 0.97, 0.94))):
            c.set_source_rgb(*INK); c.set_line_width(15); c.move_to(px, py); c.line_to(mx, my); c.stroke()
            c.set_source_rgb(*col); c.set_line_width(11.5); c.move_to(px, py); c.line_to(mx, my); c.stroke()
        ellipse(k, mx - 5, my, 10, 9, (0.86, 0.66, 0.50), 983, lw=1.8)
        ellipse(k, mx + 5, my, 10, 9, (0.96, 0.80, 0.66), 984, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(2)                          # the shake
        for sx in (-1, 1):
            c.new_path(); c.arc(mx, my - 16 * sx, 20, 0.25 if sx < 0 else 3.4, 2.9 if sx < 0 else 6.0); c.stroke()
    S(k, (338, 650, 2.3), auto=False, mic="down", portrait=False, extra=ex,
      pre=pam_at(250, front=True, face="pleased", look=(1, 0), glasses="up"),
      **base(rb=False, sf=False, pm=False, mm=False, cl=at("client", x=340, pose="open", face="warm", look=(-1, 0)),
             dn=at("don", x=445, pose="stand", face="happy", look=(-1, -0.3))))


def f_5_4b(k):
    b6._mic_shot(k, True, cam=(482, 652, 4.2), boom=ORANGE)


def f_5_4c(k):
    b6._mic_shot(k, False, cam=(482, 652, 4.2), boom=ORANGE)


def f_6_5(k):                                              # the phone in her hand: five stars, one gold
    S(k, (540, 690, 3.0), auto=False, portrait=False,
      **base(cl=False, rb=False, dn=False, pm=False, mm=False, sf=at("sofia", pose="low", face="deadpan", look=(1, 0.3))))
    c = k.c
    c.save(); c.translate(372, 480); c.rotate(0.10); c.scale(0.78, 0.78)
    rect(k, -92, -160, 184, 320, (0.10, 0.11, 0.14), 984, lw=3)
    c.set_source_rgb(*cp.LIGHT); c.rectangle(-80, -140, 160, 280); c.fill()
    cp._stars(c, -62, -20, 1, 28)
    c.new_path()
    cp.T(c, "1 / 5", 0, 50, 34, col=cp.RED)
    c.restore()
    for i in range(4):                                                      # her fingers round its edge
        ellipse(k, 300, 432 + i * 28, 16, 11, (0.80, 0.56, 0.40), 985 + i, lw=2)
    c.set_source_rgb(*INK); c.set_line_width(16); c.set_line_cap(1); c.move_to(250, 640); c.line_to(292, 540); c.stroke()
    c.set_source_rgb(0.42, 0.07, 0.18); c.set_line_width(12); c.move_to(250, 640); c.line_to(292, 540); c.stroke()


def f_6_6(k):                                              # the wide again: Pam's phone glows, she alone smiles
    orig = b2.pam_at
    b2.pam_at = lambda x, **kw: orig(x, **dict(kw, glasses="up", face="pleased", look=(-0.2, 1)))
    try:
        b2._wide(k, dn=at("don", pose="vest", face="grin", look=(0, 0.6)),
                 looks=dict(sofia_face="deadpan", sofia=(0, 1), mom=(-1, 0)))
    finally:
        b2.pam_at = orig
    phone_in(k, "pam", dx=-0.9, dy=1.5, lit=True, s=1.5)


REPL = {"5.4a": (f_5_4a, "Don shakes, beaming; the Client looks at Pam. DON: \"Customer success.\""), "5.4b": (f_5_4b, None),
        "5.4c": (f_5_4c, None), "6.5": (f_6_5, None), "6.6": (f_6_6, "The same room, every phone buzzing; Pam's glows, she smiles (loop)")}
SHOTS = [(sh, ln, REPL.get(sh, (fn,))[0], (REPL.get(sh, (0, None))[1] or note)) for sh, ln, fn, note in b6.SHOTS]


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
