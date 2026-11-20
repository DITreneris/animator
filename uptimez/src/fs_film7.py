"""FIRST SEARCH (episode 10): film v7 (19 Nov). fs_film6.py (film v6) is kept. v7, from the director: the Friday
shot redrawn (Sofia was standing on the Client again); the thumb in three clear steps (the lick, the travel, the
scrub); the robot from behind is the canon robot turned round, and Pam writes STUPID on its back in lipstick while
the week goes by. Below: v6's notes.
FIRST SEARCH (episode 10): film v6 (19 Nov). fs_film5.py (film v5) is kept. v6, from the director: the Client
threatens twice ("Friday. Or I sue." / "See you in court."); a lift bell at 0:00 (no silence); Sofia flirts in a
close-up and stands clear of him; Don is dazed, then hears "bank"; the PAID shot sits higher; the red zero is on a
terminal the robot works at, seen from behind. Below: v5's notes.
FIRST SEARCH (episode 10): film v5 (19 Nov). fs_film4.py (film v4) is kept. From the director and the cold test of
v4 (both viewers: the story repeats itself, Mom's act sits between the question and its answer, nobody can tell what
day it is). Picked by /grill-me:

- a week passes, and it shows: a tear-off calendar hangs by the portrait (MONDAY 1); "RETRY UNTIL FRIDAY" moves from
  the end to the middle and the pages fall to FRIDAY 5; at the end the page turns to MONDAY 8 (the loop);
- the order: MONDAY (he comes in, the bonk, "Friday, the bank", the promise, he pays), the cover-up (red zero, "It found
  nothing.", "make the zero green", "Approved.", the wipe, "Machines.", the plaster, the post, "That hussy." at the
  comments, "Young man.", the thumb, "Eww."), the week, FRIDAY (he is back: "Where's my blueprint?", the glance, LAST
  WEEK), the discussion (three new lines: "Where is his blueprint?" / "Ask the machine." / "ZERO RESULTS."), "Pam has a
  plan." (the first time we see her with it), the wrong plan, his fury, he slams out, the plaster drops, MONDAY again;
- out: the card insert, "The zero's green." with Pam behind (it gave the plan away), 100% COMPLETE;
- drawing: Mom beside Pam with her arm round Pam's back (not a band across her chest), her weight on Pam's side; Mom's
  sleeves thinner, from the shoulder; Sofía's arms with an elbow; a hand feeds the roll in LAST WEEK.

  python3 fs_film5.py [dir] [540|1080]   -> fs_film7_540.mp4 / fs_film7_1080.mp4, fs_timing_film7.json
"""
import os
import sys
import json
import math
import shutil
import subprocess
import numpy as np
import soundfile as sf
import cairo
import kit
from kit import Ctx, INK, ellipse, rect
import fs_storyboard as sb
import fs_animatic as an
import fs_anim as fa
import fs_film2 as f2
import fs_film4 as f4
import sound_xmas as sx
import sound_iwry as si
import sound_bc_mix as bm
import sound_ob_mix as om
import sound_fs_music as mus
import mom_fs as mfs
import mom_on as mo
import sofia_fs as sfs
import pam_bc as pb
import acts_ob as ac

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, DR = 540, 960, 15
SR = an.SR
F = sb.F
VOICES, LEAD = "fs_voices/film_v12", 0.15
ease = f2.ease
CUR_T, TALK, FORCE = f2.CUR_T, f2.TALK, f2.FORCE
A_LEN = 4.6
T_OPEN, T_IN, T_SHUT, T_SLAM, T_BACK0, T_BACK1, T_DROP0, T_DROP1 = (f4.T_OPEN, f4.T_IN, f4.T_SHUT, f4.T_SLAM, f4.T_BACK0,
                                                                    f4.T_BACK1, f4.T_DROP0, f4.T_DROP1)
DOOR_CAM = f2.DOOR_CAM

# (shot, [(beat, drawing, seconds or None = the line's length + lead + tail, the take or None)])
LIST = [
    ("A", [("open", "open", A_LEN, None)]),
    ("S", [("flirt", "flirt", 0.9, None)]),
    ("B", [("b", "bshot", None, "1.2")]),
    ("C", [("c1", "2.2", 0.5, None), ("c2", "2.2", None, "2.2"), ("c3", "2.2", 0.5, None)]),
    ("D", [("paid", "paid", None, "t1")]),
    ("E0", [("red", "term", 1.9, None)]),
    ("E", [("fright", "fright", 0.8, None), ("nothing", "3.3", None, "3.3")]),
    ("F", [("f1", "4.1", None, "4.1"), ("f2", "4.1", None, "4.2"), ("f3", "4.1", 1.3, "4.3")]),
    ("G", [("wipe", "4.5", 1.0, None)]),
    ("L", [("machines", "momdesk", None, "6.1b")]),
    ("E2", [("plaster", "3.4", 0.9, None)]),
    ("M", [("post", "6.2a", 1.0, None), ("comments", "6.2b", 1.2, None)]),
    ("L2", [("hussy", "momdesk", None, "7.5")]),
    ("N", [("youngman", "7.1", None, "7.1")]),
    ("O", [("round", "7.2", 0.7, None)]),
    ("O2", [("lick", "tlick", 0.9, None), ("travel", "ttravel", 0.5, None), ("scrub", "tscrub", 1.2, None)]),
    ("P", [("eww", "7.4", None, "7.4")]),
    ("T", [("week", "week", 2.8, None)]),
    ("RET", [("ret", "ret", 1.0, None)]),
    ("H", [("h1", "h51", 0.7, None), ("h2", "h51", None, "5.2")]),
    ("I", [("glance", "5.2b", 0.5, None)]),
    ("J", [("memory", "memory", 1.0, None)]),
    ("X", [("x1", "huddle", None, "x1"), ("x2", "huddle2", None, "x2")]),
    ("X3", [("x3", "robot", None, "x3")]),
    ("Q", [("hug", "hug", None, "8.1")]),
    ("R", [("show", "show", 1.1, None), ("fury", "fury", None, "t2")]),
    ("OUT", [("leave", "leave", 1.3, None)]),
    ("U", [("heal", "9.3", 1.2, None), ("zero", "9.4", 1.6, None), ("shake", "9.5", 0.35, None)]),
]
SHARE = {"E": "3.3", "F": "4.1", "X": "huddle"}
CAMD = dict(f4.CAMD)
MOVES = {"C", "F", "U", "E0"}
EXTRA = {"b": {"card": True}, "h2": {"cl_look": (1, -0.2), "cl_face": "suspicious"}, "h1": {"cl_face": "suspicious"}}
STATE = {"h51": "5.1", "tlick": "7.3", "ttravel": "7.3", "tscrub": "7.3", "open": "1.1a", "red": "3.1", "term": "3.1", "flirt": "1.2", "bshot": "1.2", "paid": "3.2", "fright": "3.3", "memory": "5.2c", "momdesk": "6.1b", "show": "8.2",
         "fury": "8.2", "week": "9.2", "ret": "5.1", "huddle": "5.3", "huddle2": "5.3", "robot": "5.3", "hug": "7.5",
         "leave": "8.2"}
CAL = {"on": False, "day": "MONDAY", "num": 1, "fall": None}        # the wall calendar for the drawing being made
CALPOS = (564, 468)
DAYS = [("MONDAY", 1), ("TUESDAY", 2), ("WEDNESDAY", 3), ("THURSDAY", 4), ("FRIDAY", 5)]


# ---------------------------------------------------------------- the calendar
def calendar(k, x, y, s=1.0, day="MONDAY", num=1, fall=None):
    """A tear-off wall calendar: a red header, the day big, the date small. fall = (day, num, u): the page before it,
    torn off and fluttering down (u 0..1)."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgb(*INK); c.new_path(); c.arc(0, -40, 2.4, 0, 2 * math.pi); c.fill()          # the nail
    rect(k, -32, -36, 64, 76, (0.80, 0.78, 0.74), 1601, lw=1.6)                                   # the pad's back
    for i in range(3):                                                                            # the pages under
        c.set_source_rgb(0.90, 0.89, 0.86); c.rectangle(-30, 34 + i * 1.6, 60, 1.2); c.fill()

    def page(d_, n_):
        c.set_source_rgb(0.99, 0.99, 0.97); c.rectangle(-30, -34, 60, 68); c.fill()
        c.set_source_rgb(0.84, 0.14, 0.16); c.rectangle(-30, -34, 60, 13); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(-30, -34, 60, 68); c.stroke()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        size = 12 if len(d_) <= 6 else 10.5 if len(d_) <= 8 else 9
        c.set_font_size(size); e = c.text_extents(d_)
        c.set_source_rgb(*INK); c.move_to(-e.x_advance / 2, 4); c.show_text(d_)
        c.set_font_size(9); e = c.text_extents(str(n_))
        c.set_source_rgb(0.45, 0.47, 0.52); c.move_to(-e.x_advance / 2, 24); c.show_text(str(n_))
    page(day, num)
    if fall:
        d_, n_, u = fall
        c.save(); c.translate(-10 * u + 8 * math.sin(u * 9), 150 * u * u); c.rotate(0.9 * u + 0.25 * math.sin(u * 12))
        c.scale(1, max(0.25, 1 - 0.5 * abs(math.sin(u * 7))))
        page(d_, n_)
        c.restore()
    c.restore()


class _cal_on_wall:
    """The calendar is on the wall wherever CAL is on (drawn with the room, before the people)."""
    def __enter__(self):
        self.f = sb.fd.office_door
        f0 = self.f
        def door(k):
            f0(k)
            if CAL["on"] and not sb._DRY[0]:
                calendar(k, CALPOS[0], CALPOS[1], 1.0, CAL["day"], CAL["num"], CAL["fall"])
        sb.fd.office_door = door
        return self

    def __exit__(self, *e):
        sb.fd.office_door = self.f


def cal_for(drawing, tb):
    CAL.update(on=False, fall=None)
    if drawing == "open":
        CAL.update(on=True, day="MONDAY", num=1)
    elif drawing in ("9.4", "9.5"):
        if drawing == "9.4" and tb < 0.45:
            CAL.update(on=True, day="FRIDAY", num=5)
        else:
            u = (tb - 0.45) / 0.9 if drawing == "9.4" else 2.0
            CAL.update(on=True, day="MONDAY", num=8, fall=("FRIDAY", 5, u) if u < 1 else None)


# ---------------------------------------------------------------- drawings
def opening(k):
    """As film v4's (he comes in, the slam, then the bonk), with the portrait hung as in the last frame (crooked, full
    size) and the calendar beside it."""
    t = CUR_T[0]
    v = ease((t - 0.5) / 1.0) - ease((t - T_BACK0) / (T_BACK1 - T_BACK0))
    cam = tuple(a + (b - a) * v for a, b in zip(sb.WIDE27, DOOR_CAM))
    sh = 7 * math.sin(2 * math.pi * 13 * (t - T_SLAM)) * math.exp(-(t - T_SLAM) * 5) if t > T_SLAM else 0.0
    if t > T_DROP1:
        sh += 9 * math.sin(2 * math.pi * 12 * (t - T_DROP1)) * math.exp(-(t - T_DROP1) * 7)
    FORCE[0] = (cam[0] + sh / cam[2], cam[1] + 0.5 * sh / cam[2], cam[2])
    op = 0.85 * ease((t - T_OPEN) / 0.25) - 0.85 * ease((t - T_SHUT) / (T_SLAM - T_SHUT))
    wob = 0.10 * math.sin(2 * math.pi * 5 * (t - T_SLAM)) * math.exp(-(t - T_SLAM) * 0.8) if t > T_SLAM else 0.0
    s_p = sb.fs.PORTRAIT_S
    hit = t >= T_DROP1
    sag = 20 * math.exp(-(t - T_DROP1) * 5) * abs(math.cos(2 * math.pi * 2.2 * (t - T_DROP1))) + 5 if hit else 0
    crook = sb.fs.CROOK

    def ex(k_, o):
        c_ = k_.c
        hx, hy = o["don"]["head"]
        r = 50 * sb.SC["don"]
        px0, py0 = sb.PORT27
        if t < T_DROP0:
            up = -10 * math.exp(-(t - T_SLAM) * 9) if t > T_SLAM else 0
            sb.fs.portrait(k_, px0, py0 + up, s_p, ang=crook + wob, crack=False, patch=False)
        else:
            u = min(1.0, (t - T_DROP0) / (T_DROP1 - T_DROP0))
            y_end = hy - r - 113 + 22
            x_ = px0 + (hx - 14 - px0) * u
            y_ = py0 + (y_end - py0) * u * u
            sb.fs.portrait(k_, x_, y_, s_p, ang=crook + 0.22 * u + (0.05 * math.sin(2 * math.pi * 6 * (t - T_DROP1)) *
                                                                 math.exp(-(t - T_DROP1) * 4) if hit else 0),
                           crack=hit, patch=False)
        if hit:
            if t < T_DROP1 + 0.2:
                sb.lines(c_, hx, hy - r, 9, 46, 78, 200, 340)
            sb.stars(c_, hx, hy - 6, 58, 5, t * 7)
    sb.V32[0] = False
    try:
        walk = ease((t - T_IN) / 0.7)
        sb.scene(k, screen="query", portrait=None, door=max(0.0, op), rb=dict(x4=True, state="eager"),
                 cl=False if t < T_IN else dict(x4=True, x=70 + 90 * walk,
                                                feet=F - 14 - (4 * abs(math.sin(math.pi * 3 * walk)) if 0 < walk < 1 else 0),
                                                pose="arrive", face="confident", look=(1, 0) if t < T_SLAM else (1, -0.4)),
                 sf=False if t < 0.9 else dict(x4=True, face="charm", look=(-1, 0)),
                 dn=dict(x4=True, feet=F + 16 + sag, face="shock" if hit else "happy", look=(0, -1) if hit else (0, 0)),
                 extra=ex)
    finally:
        sb.V32[0] = True


def door_shot(k, leaving):
    """At the glass door. ret: Friday, he comes in again, sour. leave: he walks out and it slams behind him."""
    t = CUR_T[0]
    if leaving:
        slam = 0.95
        op = 0.85 * ease(t / 0.2) - 0.85 * ease((t - 0.7) / (slam - 0.7))
        sh = 9 * math.sin(2 * math.pi * 13 * (t - slam)) * math.exp(-(t - slam) * 5) if t > slam else 0.0
        walk = ease(t / 0.7)
        cl = False if t > 0.72 else dict(x4=True, x=170 - 110 * walk,
                                         feet=F - 14 - 4 * abs(math.sin(math.pi * 3 * walk)), pose="stand",
                                         face="suspicious", look=(-1, 0))
    else:
        op = 0.85 * ease(t / 0.2) - 0.85 * ease((t - 0.75) / 0.25)
        sh = 0.0
        walk = ease((t - 0.15) / 0.6)
        cl = False if t < 0.15 else dict(x4=True, x=70 + 90 * walk,
                                         feet=F - 14 - (4 * abs(math.sin(math.pi * 3 * walk)) if 0 < walk < 1 else 0),
                                         pose="stand", face="suspicious", look=(1, 0))
    FORCE[0] = (DOOR_CAM[0] + sh / DOOR_CAM[2], DOOR_CAM[1], DOOR_CAM[2])
    sb.scene(k, screen="green", portrait=None, door=max(0.0, op), rb=dict(x4=True, state="eager"), cl=cl, sf=False,
             dn=False, pm=False, mm=False)


def ret(k):
    door_shot(k, False)


def leave(k):
    door_shot(k, True)


def week(k):
    """T: the week goes by: RETRY UNTIL FRIDAY, the robot on ENTER, the pages falling to FRIDAY 5; and Pam, with her
    lipstick, writes STUPID across its back, a letter at a time."""
    t = CUR_T[0]
    step = 0.46
    i = min(4, int(t / step))
    u = (t - i * step) / 0.40
    fall = (DAYS[i - 1][0], DAYS[i - 1][1], u) if i > 0 and u < 1 else None
    n = max(0, min(6, int((t - 0.75) / 0.27) + 1)) if t > 0.75 else 0
    STUPID[0] = n
    try:
        terminal(k, "retry", 1.0 if (t % step) < 0.12 else 0.0,
                 cal=lambda: calendar(k, 462, 190, 1.55, DAYS[i][0], DAYS[i][1], fall))
    finally:
        STUPID[0] = 0
    c = k.c
    c.select_font_face("Lilita One"); c.set_font_size(23 * RB["s"])
    wd = [c.text_extents(ch).x_advance for ch in "STUPID"]
    nn = min(5, max(0, n - 1)) + (0 if n == 0 else min(1.0, ((t - 0.75) % 0.27) / 0.27))
    tx = RB["x"] - sum(wd) / 2 + (sum(wd[:int(nn)]) + (nn - int(nn)) * wd[min(5, int(nn))])
    ty = RB["feet"] - 108 * RB["s"] - 14 + 9 * math.sin(t * 23)
    ps = 1.5                                                                    # near the lens, as the robot is
    px = 140 - 300 * (1 - ease(t / 0.6))
    pf = 1085
    hands = ((-60, -150), ((tx - 6 - px) / ps, (ty - pf) / ps))
    with ac.arms():
        ac.pam(k, px, pf, ps, "stand", look=(1, 0.3), hands=hands)
    if t > 0.5:                                                                  # the lipstick in her hand
        c.save(); c.translate(tx - 6, ty); c.rotate(0.9)
        c.set_source_rgb(*INK); c.rectangle(-6, -15, 12, 30); c.fill()
        c.set_source_rgb(0.85, 0.72, 0.30); c.rectangle(-4.5, -4, 9, 17); c.fill()
        c.set_source_rgb(*LIP); c.move_to(-4, -4); c.line_to(-4, -13); c.line_to(4, -9); c.line_to(4, -4); c.close_path(); c.fill()
        c.restore()


def memory(k):
    sb.f_m52c(k)
    c = k.c
    kit.text(k, "LAST WEEK", 132, 196, 32, (1, 1, 1))              # under the rewind sign, clear of the hand
    c.save(); c.translate(388, 300); c.rotate(-0.08)
    kit.rect(k, -86, -24, 172, 48, (0.98, 0.97, 0.94), 1400, shadow=False, lw=2.4)
    c.restore()
    kit.text(k, "MY GARAGES", 388, 300, 24, (0.10, 0.20, 0.55))
    t = CUR_T[0]
    sb.thumb(k, 268, 150 + 26 * ease(t / 0.5), 1.15, sb.SKIN_DON, ang=0.0, who="don")       # whose hand fed it in


def huddle(k, two=False):
    sb.scene(k, cam=(262, 640, 2.3), sf=dict(face="charm" if two else "drop", look=(-1.2, -0.2) if two else (1.2, 0)),
             dn=dict(face="confused", look=(-1, -0.3) if two else (-1, -0.1)), cl=False, rb=False)


def huddle2(k):
    huddle(k, True)


STUPID = [0]                       # how many letters of STUPID are on the robot's back (Pam's lipstick)
LIP = (0.80, 0.10, 0.30)
RB = dict(x=392, feet=852, s=1.5)


def lipstick_word(c, x, y, size, n):
    """STUPID, in lipstick: fat, crooked capitals, each a little off its line; the first n letters."""
    c.select_font_face("Lilita One", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    word = "STUPID"
    wd = [c.text_extents(ch).x_advance for ch in word]
    x0 = x - sum(wd) / 2
    for i, ch in enumerate(word[:n]):
        c.save(); c.translate(x0 + sum(wd[:i]), y + (3, -4, 2, -2, 4, -3)[i] * size / 34)
        c.rotate((-0.10, 0.06, -0.04, 0.09, -0.07, 0.05)[i])
        c.move_to(0, 0); c.text_path(ch)
        c.set_source_rgb(*LIP); c.fill_preserve(); c.set_line_width(size * 0.07); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke()
        c.restore()
    if n >= 6:                                                                  # the smear under it
        c.set_source_rgba(LIP[0], LIP[1], LIP[2], 0.75); c.set_line_width(size * 0.14); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.new_path(); c.move_to(x0 + 4, y + size * 0.30); c.curve_to(x, y + size * 0.42, x + 20, y + size * 0.22, x0 + sum(wd) - 2, y + size * 0.34)
        c.stroke()


def robot_back(k, x, feet, s, press=0.0):
    """The canon robot (robot_mf), turned round: the same head, neck, body, arms and wheel; where the face was, the
    back of its head (vents, two bolts); no bow tie, no badge; a plain back for Pam's lipstick."""
    import robot_mf as rm
    c = k.c
    CREAM = (0.95, 0.94, 0.89)
    o = rm.robot(k, x, feet - 3 * press, s, (0.0, 0, 0, (-20, 0), (150, 24)), "eager", (0, 0), 1, badge=False)
    hx, hy = o["head"]
    ellipse(k, hx, hy, 47 * s, 40 * s, CREAM, 821, shadow=False, lw=2.6)       # the back of the head
    c.set_source_rgb(0.45, 0.47, 0.52)
    for j in range(3):
        c.rectangle(hx - 15 * s, hy - 9 * s + j * 8 * s, 30 * s, 3 * s); c.fill()
    for sx_ in (-1, 1):
        ellipse(k, hx + sx_ * 32 * s, hy + 22 * s, 3 * s, 3 * s, (0.62, 0.64, 0.68), 822 + sx_, shadow=False, lw=1.4)
    by = feet - 163 * s                                                         # the bow tie: gone (its knot was in front)
    c.set_source_rgb(*CREAM); c.new_path(); c.save(); c.translate(x, by + 4 * s); c.scale(24 * s, 12 * s)
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    rect(k, x - 9 * s, by - 22 * s, 18 * s, 30 * s, (0.36, 0.38, 0.43), 824, shadow=False, lw=2)   # the neck, over it
    if STUPID[0]:
        lipstick_word(c, x, feet - 108 * s, 23 * s, STUPID[0])
    sb.HEADS["robot"] = (hx, hy, 47 * s)
    return o


def terminal(k, state, press=0.0, cal=None):
    """The machine's desk: a monitor on a stand, a keyboard, the robot at it, seen from behind."""
    c = k.c
    sb.bg(c)
    c.set_source_rgb(0.72, 0.62, 0.48); c.rectangle(0, 690, 540, 270); c.fill()                # the floor
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.move_to(0, 690); c.line_to(540, 690); c.stroke()
    sb.fs.screen(k, state, 60, 120, 330, 215, cursor=state == "query")
    rect(k, 212, 340, 26, 44, (0.30, 0.32, 0.36), 801, shadow=False, lw=2)                      # the stand
    rect(k, 166, 382, 118, 12, (0.30, 0.32, 0.36), 802, shadow=False, lw=2)
    rect(k, 14, 394, 500, 22, (0.62, 0.45, 0.28), 803, lw=2.4)                                  # the desk
    for x_ in (30, 482):
        rect(k, x_, 416, 16, 274, (0.50, 0.36, 0.22), 804 + x_, shadow=False, lw=2)
    rect(k, 396, 372, 112, 22, (0.22, 0.23, 0.27), 806, shadow=False, lw=2)                     # the keyboard
    c.set_source_rgb(0.75, 0.77, 0.80)
    for i in range(7):
        for j in range(2):
            c.rectangle(402 + i * 13, 376 + j * 8, 9, 5); c.fill()
    c.set_source_rgb(0.95, 0.80, 0.25) if press > 0.5 else c.set_source_rgb(0.85, 0.87, 0.90)   # ENTER
    c.rectangle(493, 376, 11, 13); c.fill()
    if cal:
        cal()
    return robot_back(k, RB["x"], RB["feet"], RB["s"], press)


def term(k):
    """E0: the robot types, hits ENTER: 0 RESULTS, red. Then the push-in."""
    t = CUR_T[0]
    press = 1.0 if 0.40 <= t < 0.55 else 0.0
    terminal(k, "query" if t < 0.5 else "red", press)
    if 0.5 <= t < 0.7:
        sb.lines(k.c, 225, 228, 9, 190, 230, 0, 360)


def flirt(k):
    """S: Sofia, close: she likes what walked in. Her eyes go to him; a heart; his shoulder at the edge."""
    t = CUR_T[0]
    def ex(k_, o):
        c = k_.c
        hx, hy = o["sofia"]["head"]
        for i, (dx, t0) in enumerate(((34, 0.15), (52, 0.4))):
            if t > t0:
                u = min(1.0, (t - t0) / 0.5)
                r_ = 7 + 2 * i
                c.save(); c.translate(hx + dx, hy - 30 - 34 * u); c.scale(0.5 + 0.5 * ease(u * 3), 0.5 + 0.5 * ease(u * 3))
                c.move_to(0, r_); c.curve_to(-r_ * 1.6, -r_ * 0.2, -r_ * 0.6, -r_ * 1.4, 0, -r_ * 0.5)
                c.curve_to(r_ * 0.6, -r_ * 1.4, r_ * 1.6, -r_ * 0.2, 0, r_); c.close_path()
                c.set_source_rgb(0.90, 0.25, 0.35); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
                c.restore()
    blink = 0.3 < t < 0.4 or 0.55 < t < 0.65
    sb.scene(k, cam=(220, 560, 1.7), door=0.85, rb=False,
             cl=dict(x4=True, x=226, feet=F + 96, s=sb.D("client", 1.3), pose="arrive", face="confident", look=(1, -0.3)),
             sf=dict(x4=True, x=356, pose="_flirt", face="better" if blink else "charm", look=(-1, -0.1)),
             dn=False, extra=ex)


def bshot(k):
    """B: "Friday, the bank. I need my blueprint." He glances at her, then says it to Don. Don is still seeing stars and
    rubbing his head; at "bank" he straightens and beams (money)."""
    t = CUR_T[0]
    bank = t > 1.05
    def ex(k_, o):
        if sb.ANIM.get("card"):
            hx, hy = o["client"]["hands"][1]
            sb.fs.phone2(k_, hx + 10, hy - 36, 0.40, "cal")
        if not bank:
            hx, hy = o["don"]["head"]
            sb.stars(k_.c, hx, hy - 8, 40, 4, t * 7)
    wob = 0 if bank else 5 * math.sin(2 * math.pi * 1.6 * t)
    sb.scene(k, cam=(220, 560, 1.7), door=0.85, rb=False,
             cl=dict(x4=True, x=226, feet=F + 96, s=sb.D("client", 1.3), pose="arrive",
                     face="suspicious" if t < 0.3 else "confident", look=(1, -0.3)),
             sf=dict(x4=True, x=356, pose="_flirt", face="charm", look=(-1, -0.1)),
             dn=dict(x4=True, x=452 + wob, pose="vest" if bank else (-8, 0, 150, 118),
                     face="happy" if bank else "confused", look=(-1, -0.1)), extra=ex)


def h51(k):
    """H: Friday. He is back, and nobody stands on anybody: him near the lens on the left, Sofia clear of his sleeve,
    Don behind her, grinning at the green zero."""
    sb.CAM4[0] = (250, 560, 1.6)
    try:
        sb.scene(k, screen="green", rb=False, pm=False, mm=False,
                 cl=dict(x4=True, x=188, feet=F + 112, s=sb.D("client", 1.4), pose="stand",
                         face=sb.ANIM.get("cl_face", "puzzled"), look=sb.ANIM.get("cl_look", (-1, -1))),
                 sf=dict(x4=True, x=318, face="drop", look=(-1, 0)),
                 dn=dict(x4=True, x=400, face="grin", look=(-1, -0.2)))
    finally:
        sb.CAM4[0] = None


def _thumb(k, phase):
    """O2: the thumb, in three steps anyone can follow. lick: her thumb up to her tongue. travel: the wet thumb, in an
    arc, to his forehead (the camera goes with it). scrub: round and round on his brow; his head goes round with it."""
    t = CUR_T[0]
    ds, ms = sb.D("don", 1.3), sb.D("mom", 1.3)
    dx_, df = 470, F + 100
    mx, mf = 566, F + 96
    dhead = (dx_, df - 302 * ds)
    mhead = (mx, mf - 294 * ms)
    mouth = (mhead[0] - 10, mhead[1] + 24 * ms / 0.7)
    brow = (dhead[0] + 12, dhead[1] - 26)
    rest = (mx - 30, mf - 150 * ms)
    wob = (0.0, 0.0)
    if phase == "lick":
        u = ease(t / 0.4)
        T = (rest[0] + (mouth[0] - rest[0]) * u, rest[1] + (mouth[1] - rest[1]) * u)
        cam = (mhead[0] - 14, mhead[1] + 26, 3.3)
        tongue = t > 0.4
    elif phase == "travel":
        u = ease(t / 0.45)
        T = (mouth[0] + (brow[0] - mouth[0]) * u, mouth[1] + (brow[1] - mouth[1]) * u - 26 * math.sin(math.pi * u))
        cam = (T[0] + 6, T[1] + 30, 3.3 - 0.5 * u)
        tongue = False
    else:
        a = 2 * math.pi * 2.6 * t
        wob = (7 * math.cos(a), 4 * math.sin(a))
        T = (brow[0] + wob[0], brow[1] + wob[1])
        cam = ((dhead[0] + mhead[0]) / 2 - 6, dhead[1] + 22, 2.8)
        tongue = False
    FORCE[0] = cam

    def ex(k_, o):
        c = k_.c
        sb.fd.shadow(k_, dx_, df + 2, 50); sb.fd.shadow(k_, mx, mf + 2, 50)
        dn = sb.don(k_, dx_ + 0.5 * wob[0], df, ds, "panic" if phase == "lick" else "stand",
                    "shock" if phase != "scrub" else "squint", look=(1, -0.5))
        if phase == "scrub":                                                     # the smudge she is after, going
            al = max(0.0, 1 - t / 0.9)
            c.set_source_rgba(0.45, 0.30, 0.22, 0.55 * al); c.new_path(); c.save()
            c.translate(brow[0] + 0.5 * wob[0], brow[1] + 4); c.scale(13, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        pose = mo.ik(-1, (T[0] - mx) / ms, (T[1] - mf) / ms) + mo.ik(1, 30, mo.SASH + 2)
        mfs.mom(k_, mx, mf, ms, pose, "sweet", look=(-1, -0.4) if phase != "lick" else (-0.4, 0.4), bag=False,
                lean=-6 if phase != "lick" else 0)
        if tongue:
            tx_, ty_ = mouth[0] + 2, mouth[1] + 2
            c.save(); c.translate(tx_, ty_); c.rotate(0.3); c.scale(8, 4.6); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi)
            c.restore(); c.set_source_rgb(0.92, 0.45, 0.52); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2)
            c.stroke()
        sb.thumb(k_, T[0], T[1] + 4, 0.20, skin=(0.96, 0.80, 0.70), ang=-2.2, who="mom")
        if phase != "lick" or t > 0.5:                                           # wet: a drop, a shine
            c.set_source_rgb(0.80, 0.90, 1.0)
            for j, (ox, oy) in enumerate(((10, -12), (-12, -4))):
                c.new_path(); c.arc(T[0] + ox, T[1] + oy + 6 * ((t * 3 + j * 0.4) % 1), 2.4, 0, 2 * math.pi); c.fill()
        if phase == "scrub":
            c.set_source_rgb(*INK); c.set_line_width(1.8)
            for dd in (0, 6):
                c.new_path(); c.arc(brow[0], brow[1], 20 + dd, -2.7 + t * 6, -1.4 + t * 6); c.stroke()
            if t > 0.9:
                sb.lines(c, brow[0], brow[1] - 6, 5, 16, 28, 200, 340)             # clean
    sb.scene(k, cl=False, dn=False, pm=False, rb=False, mm=False, sf=False, extra=ex)


def tlick(k):
    _thumb(k, "lick")


def ttravel(k):
    _thumb(k, "travel")


def tscrub(k):
    _thumb(k, "scrub")


def paid(k):
    """D: PREMIUM, PAID $999, and the threat: "Friday. Or I sue." Higher in the frame than v5 (the phone's dead zone)."""
    sb.scene(k, cam=(92, 560, 3.0), cl=dict(face="suspicious", look=(1.2, -0.2)), rb=False, sf=False, dn=False, pm=False,
             mm=False)
    sb.fs.phone2(k, 400, 575, 1.25, "paid_price")


def robot_cu(k):
    """X3 (v6): the machine, asked: ZERO RESULTS, green, on its terminal."""
    STUPID[0] = 6
    try:
        terminal(k, "green", 1.0 if 0.2 <= CUR_T[0] < 0.35 else 0.0)
    finally:
        STUPID[0] = 0


def _robot_cu_v5(k):
    """X3: the machine, asked: ZERO RESULTS (the zero green over it)."""
    c = k.c
    sb.bg(c)
    sb.fs.screen(k, "green", 40, 250, 460, 290, cursor=False)
    c.save(); sb.view(c, sb.P["robot"][0], 600, 2.6)
    sb.robot(k, sb.P["robot"][0], sb.P["robot"][1], sb.P["robot"][2], "eager", arm="none")
    c.restore()


def hug(k):
    """Q: "Pam has a plan." Mom beside Pam, her weight on Pam's side, her arm round Pam's back: the sleeve goes behind
    Pam, the hand comes over Pam's far shoulder. Pam, pleased, her mouth shut (Mom is the one talking)."""
    def ex(k_, o):
        c = k_.c
        ms, ps = sb.D("mom", 1.3), sb.D("pam", 1.3)
        px, pf = 512, F + 100
        mx, mf = 606, F + 96
        sb.fd.shadow(k_, mx, mf + 2, 52); sb.fd.shadow(k_, px, pf + 2, 52)
        with ac.arms():
            dry = pb.pam(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0), px, pf, ps, "stand",
                         "mirror", look=(1, -0.2))
        hx_, hy_ = dry["head"]
        back = (hx_ + 6 * ps, hy_ + 96 * ps)                                    # behind her shoulder blades
        pose = mo.ik(-1, (back[0] - mx) / ms, (back[1] - mf) / ms) + mo.ik(1, 58, mo.SASH + 6)
        mfs.mom(k_, mx, mf, ms, pose, "sweet", look=(-1.2, 0.2), lean=-8, tilt=-12)
        with ac.arms():
            pm_ = pb.pam(k_, px, pf, ps, "stand", "mirror", look=(1, -0.2))
        sx_, sy_ = pm_["head"][0] - 46 * ps, pm_["head"][1] + 80 * ps           # her hand over Pam's far shoulder
        c.save(); c.translate(sx_, sy_); c.rotate(0.5); c.scale(ps / 0.6, ps / 0.6)
        c.new_path(); c.save(); c.scale(11, 8.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(0.96, 0.80, 0.70); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
        c.set_line_width(1.2); c.set_line_cap(1)
        for dx in (-4, 0, 4):
            c.new_path(); c.move_to(dx, 1); c.line_to(dx * 1.1, 8); c.stroke()
        c.restore()
        r_ = 9
        c.save(); c.translate((mx + px) / 2 + 8, pm_["head"][1] - 62 * ps - sb.ANIM.get("hearts", 0) * 0.4)
        c.move_to(0, r_); c.curve_to(-r_ * 1.6, -r_ * 0.2, -r_ * 0.6, -r_ * 1.4, 0, -r_ * 0.5)
        c.curve_to(r_ * 0.6, -r_ * 1.4, r_ * 1.6, -r_ * 0.2, 0, r_); c.close_path()
        c.set_source_rgb(0.90, 0.25, 0.35); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()
        c.restore()
    sb.scene(k, cl=False, dn=False, pm=False, rb=False, mm=False, sf=False, extra=ex)


# ---------------------------------------------------------------- arms
def mom_arm(k, sx, sy, a1, a2, col, skin, seed, ln=48, w=17):
    return f4.mom_arm(k, sx, sy, a1, a2, col, skin, seed, ln, w * 0.78)


def sofia_arm(k, sx, sy, a1, a2, seed, ln=48, w=15):
    """Sofía's sleeve with an elbow: one rounded stroke, a little bend even when the arm hangs; the cuff; her hand."""
    c = k.c
    if abs(a2) < 6:
        a2 = 10 if sx < 0 else -10                          # a hanging arm is not a ruler
    d = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    ex, ey = sx + d(a1)[0] * ln, sy + d(a1)[1] * ln
    hx, hy = ex + d(a1 + a2)[0] * ln, ey + d(a1 + a2)[1] * ln
    fx, fy = d(a1 + a2)
    wx, wy = hx - fx * 8, hy - fy * 8
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for colr, lw in ((INK, w + 4), (sfs.FUCHSIA, w)):
        c.set_source_rgb(*colr); c.set_line_width(lw)
        c.new_path(); c.move_to(sx, sy); c.line_to(ex, ey); c.line_to(wx, wy); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    for colr, lw, g in ((INK, w + 5, 1.2), (sfs.SLEEVE_CUFF, w + 1, 0)):
        c.set_source_rgb(*colr); c.set_line_width(lw)
        c.new_path(); c.move_to(wx - fx * (3 + g), wy - fy * (3 + g)); c.line_to(wx + fx * (3 + g), wy + fy * (3 + g)); c.stroke()
    ellipse(k, hx + fx * 3, hy + fy * 3, w * 0.58, w * 0.58, sfs.SKIN, seed, shadow=False, lw=2)
    ellipse(k, hx + fx * 10, hy + fy * 10, 3.2, 3.2, sfs.RED, seed + 1, shadow=False, outline=False)
    return hx + fx * 3, hy + fy * 3


class _arms:
    def __enter__(self):
        self.s, self.m, self.fl = sfs.arm_long, f4.mom_arm, kit.ARM_POSES.get("_flirt")
        sfs.arm_long = sofia_arm
        kit.ARM_POSES["_flirt"] = (-34, 118, 12, -8)       # a hand on her hip (the raised hand read as detached)
        self.ctx = f4._mom_arms(); self.ctx.__enter__()
        self.orig_arm = f4.mom_arm
        return self

    def __exit__(self, *e):
        self.ctx.__exit__(*e)
        sfs.arm_long = self.s
        if self.fl is not None:
            kit.ARM_POSES["_flirt"] = self.fl


# ---------------------------------------------------------------- the camera inside a shot, the overlays
def move(shot, t, ln, hl, anch, port):
    if shot == "A":
        return (270, 480, 1.0)
    if shot == "E0":
        v = ease((t - 0.85) / 0.6)
        return (270 + (225 - 270) * v, 480 + (250 - 480) * v, 1 + 0.55 * v)
    if shot == "C" and hl.get("don") and t < 1.0:
        h = hl["don"]
        v = 1 - ease((t - 0.45) / 0.55)
        return (270 + (h[0] - 270) * v, 480 + (h[1] + 30 - 480) * v, 1 + 0.8 * v)
    if shot == "F" and hl.get("robot") and t > ln - 0.5:
        h = hl["robot"]
        v = ease((t - (ln - 0.5)) / 0.45)
        return (270 + (h[0] - 270) * v, 480 + (h[1] + 1.4 * h[2] - 480) * v, 1 + 1.0 * v)
    if shot == "O" and hl.get("mom") and 0.55 <= t < 0.9:
        h = hl["mom"]
        v = ease((t - 0.55) / 0.35)
        return (270 + (h[0] - 270) * v, 480 + (h[1] - 480) * v, 1 + 1.2 * v)
    if shot == "U":
        if t < 1.2:
            return (270, 480, 1 + 0.03 * t / 1.2)
        if port and t < 2.4:
            v = 1 - ease((t - 1.2) / 1.2)
            return (270 + (port[0] - 270) * v, 480 + (port[1] - 480) * v, 1 + 1.6 * v)
        return (270, 480, 1.0)                              # the last frames are frame 0's framing exactly
    return (270, 480, 1 + 0.03 * t / ln)


def overlay(shot, beat, tb, c, tf, hl, anch):
    if shot == "C" and beat == "c3" and "tablet" in anch.get("2.2", {}):
        x, y, w = anch["2.2"]["tablet"]
        x, y = tf(x, y)
        v = ease(tb / 0.35)
        sb.thumb(Ctx(c, 0), x + 30, y + 40 + 260 * (1 - v), 0.9, sb.SKIN_CL, oil=True, ang=2.55, who="client")
    if shot == "F" and beat == "f3" and hl.get("robot") and tb >= 0.5:
        h = hl["robot"]
        x, y = tf(h[0], h[1] + 2.0 * h[2])
        z = tf(1, 0)[0] - tf(0, 0)[0]
        sw, sh = 1.7 * h[2] * z, 0.5 * h[2] * z
        c.set_source_rgb(0.12, 0.13, 0.16); c.rectangle(x - sw / 2 - 4, y - sh / 2 - 4, sw + 8, sh + 8); c.fill()
        c.set_source_rgb(0.20, 0.72, 0.40); c.rectangle(x - sw / 2, y - sh / 2, sw, sh); c.fill()
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        c.set_font_size(sh * 0.5); e = c.text_extents("APPROVED")
        c.set_source_rgb(1, 1, 1); c.move_to(x - e.x_advance / 2, y + e.height / 2); c.show_text("APPROVED")


# ---------------------------------------------------------------- the build
fns_base = {}


def timeline(takes):
    rows, t = [], 0.0
    for shot, beats in LIST:
        for beat, drawing, ln, take in beats:
            if ln is None:
                ln = LEAD + takes[take]["len"] + 0.30
            elif take:
                ln = max(ln, LEAD + takes[take]["len"] + 0.30)
            rows.append(dict(shot=beat, start=round(t, 3), len=round(ln, 3), of=shot, drawing=drawing, take=take))
            t += ln
    return rows, t


def build(d, S=1, music="A"):
    import sound_bc as bc
    takes = json.load(open(os.path.join(HERE, VOICES, "takes.json")))
    an.SPEAKER["PAM+SOFIA"] = ["sofia"]
    for kk, vv in (("5.1", "portrait"), ("2.2", "portrait"), ("8.2", "shredder"), ("8.2", "portrait"),
                   ("7.5", "portrait"), ("5.3", "counter")):
        sb.DROP32.setdefault(kk, set()).add(vv)
    rows, total = timeline(takes)
    json.dump(rows, open(os.path.join(d, "fs_timing_film7.json"), "w"), indent=1)
    row = {r["shot"]: r for r in rows}
    fns = {s: fn for s, _, fn, _ in sb.SHOTS}
    fns_base.update(fns)
    for name, fn in (("open", opening), ("red", f4.red), ("fright", f4.fright), ("memory", memory),
                     ("momdesk", f4.momdesk), ("show", f4.show), ("fury", f4.fury), ("week", week), ("ret", ret),
                     ("leave", leave), ("term", term), ("flirt", flirt), ("h51", h51), ("tlick", tlick), ("ttravel", ttravel), ("tscrub", tscrub), ("bshot", bshot), ("paid", paid), ("huddle", huddle), ("huddle2", huddle2), ("robot", robot_cu), ("hug", hug)):
        fns[name] = sb._with_state(STATE[name], fn)
    CAMD.update({"hug": (556, 742, 2.2), "bshot": (338, 655, 1.8), "paid": (110, 635, 3.0)})
    CAMD["h51"] = (292, 690, 1.8)
    sb.DROP32.setdefault("1.2", set()).add("portrait")
    lines_abs = []
    voice = np.zeros(int((total + 1) * SR))
    for r in rows:
        if r["take"]:
            m = takes[r["take"]]
            a, _ = sf.read(os.path.join(HERE, VOICES, "%s.wav" % r["take"]))
            a = a.mean(1) if a.ndim > 1 else a
            t0 = r["start"] + LEAD
            an._at(voice, a, t0, 1.0)
            vis = bc.visemes(np.asarray(a, dtype=np.float64), m["text"]) if m["who"] != "ROBOT" else []
            lines_abs.append((m["who"], m["text"], t0, t0 + m["len"], vis))
    out_dir = "/tmp/fs_film7_%d" % (540 * S)
    shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    anch = {}

    def draw(drawing, beat, tb, ln, shared, S_, Z):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W * S_ * Z), int(H * S_ * Z)); surf.set_device_scale(S_ * Z, S_ * Z)
        c = cairo.Context(surf); k = Ctx(c, 0)
        sb.bg(c)
        sb.ANIM.clear(); sb.ANIM.update(fa.motion_all(drawing, tb, ln)); sb.ANIM.update(EXTRA.get(beat, {}))
        if drawing == "hug":
            sb.ANIM["hearts"] = 50 * tb / ln
        if drawing == "7.4":
            sb.ANIM["shudder"] = sb.ANIM.get("shudder", 0) - 60
        FORCE[0] = CAMD.get(drawing) or shared
        CUR_T[0] = tb
        cal_for(drawing, tb)
        sb.HEADS.clear(); sb.AVOID.clear(); f2.ANCH.clear()
        with sb._norm(record_only=True):
            fns[drawing](k)
        anch.setdefault(drawing, {}).update(f2.ANCH)
        if os.environ.get("FS_DEBUG") and tb == 0.0 and S_ == 1 and Z == 1:
            print("CAM", drawing, FORCE[0], sb.LASTCAM[0], {n: tuple(round(v) for v in h) for n, h in sb.HEADS.items()}, flush=True)
        FORCE[0] = None
        return surf, dict(sb.HEADS), list(sb.AVOID)

    n = 0
    with f2._forced(), f2._anchors(), f2._mouths(), _arms(), f4._no_roll(), _cal_on_wall():
        for d_ in ("show", "fury"):                          # headroom for his line: the picture a little down and out
            draw(d_, d_, 0.0, 1.0, None, 1, 1)
            cam_ = sb.LASTCAM[0]
            CAMD[d_] = (cam_[0], cam_[1] - 46 / cam_[2], cam_[2] * 0.92)
        f4_arm = f4.mom_arm
        f4.mom_arm = f4_arm                                  # (the thinner sleeve is set below, on kit.arm's stand-in)
        for shot, beats in LIST:
            t0s = row[beats[0][0]]["start"]
            ln_s = sum(row[b[0]]["len"] for b in beats)
            TALK.clear(); anch.clear()
            shared = None
            if shot in SHARE:
                draw(SHARE[shot], SHARE[shot], 0.0, 1.0, None, 1, 1)
                shared = sb.LASTCAM[0]
            _, hl, _ = draw(beats[0][1], beats[0][0], 0.0, row[beats[0][0]]["len"], shared, 1, 1)
            for beat, drawing, _, _ in beats[1:]:
                draw(drawing, beat, 0.0, row[beat]["len"], shared, 1, 1)
            port = None
            if shot == "U":
                p = sb.PORT27
                port = (270 + (p[0] - sb.WIDE27[0]) * sb.WIDE27[2], 480 + (p[1] - sb.WIDE27[1]) * sb.WIDE27[2])
            local = [(w, tx, a - t0s, b - t0s, e) for w, tx, a, b, e in lines_abs if a < t0s + ln_s and b + 0.25 > t0s]
            bub = {}
            Z = 3 if shot in MOVES else 1
            for j in range(int(round(ln_s * DR))):
                t = j / DR
                acc = 0.0
                for beat, drawing, _, _ in beats:
                    if t < acc + row[beat]["len"] - 1e-6 or beat == beats[-1][0]:
                        break
                    acc += row[beat]["len"]
                tb = t - acc
                TALK.clear()
                for who, text, a0, a1, vis in local:
                    if a0 - 0.1 <= t < a1 + 0.05:
                        for nm in f2.WHO2.get(who, []):
                            TALK[nm] = f2._vis(vis, int((t - a0) * 12) + 1) or "M"
                surf_b, heads, avoid = draw(drawing, beat, tb, row[beat]["len"], shared, S, Z)
                fx, fy, z = move(shot, t, ln_s, hl, anch, port)
                out = cairo.ImageSurface(cairo.FORMAT_RGB24, W * S, H * S); out.set_device_scale(S, S)
                c0 = cairo.Context(out)
                sb.bg(c0)
                c0.save(); c0.translate(270, 480); c0.scale(z, z); c0.translate(-fx, -fy)
                pat = cairo.SurfacePattern(surf_b); pat.set_filter(cairo.FILTER_GOOD)
                c0.set_source(pat); c0.paint(); c0.restore()
                tf = lambda x, y: ((x - fx) * z + 270, (y - fy) * z + 480)
                heads_t = {nm: tf(x, y) + (r * z,) for nm, (x, y, r) in heads.items()}
                overlay(shot, beat, tb, c0, tf, hl, anch)
                for who, text, a0, a1, vis in local:
                    if a0 <= t < a1 + 0.25:
                        bk = (text, drawing)
                        if bk not in bub:
                            bub[bk] = (heads_t, [tf(b[0], b[1]) + tf(b[2], b[3]) for b in avoid], t)
                        hh, av, tb0 = bub[bk]
                        sb.AVOID[:] = av
                        nn = int(round((t - tb0) * DR))
                        pop = (0.82, 1.05)[nn] if (nn < 2 and abs(tb0 - a0) < 0.07) else 1.0
                        dry = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); dc = cairo.Context(dry)
                        box = fa._say_box(dc, Ctx(dc, 0), who, text, hh)
                        bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                        c0.save(); c0.translate(bx, by); c0.scale(pop, pop); c0.translate(-bx, -by)
                        an.say(c0, Ctx(c0, 0), who, text, hh)
                        c0.restore()
                out.write_to_png("%s/f%05d.png" % (out_dir, n)); n += 1
    sb.ANIM.clear(); TALK.clear(); FORCE[0] = None; CAL["on"] = False
    # ---- sound: the voices, the effects on this film's own timeline, theme A from the bonk
    at = {r["shot"]: r["start"] for r in rows}
    m = np.zeros_like(voice)
    put = lambda a, t, g: an._at(m, a, t, g)
    put(bm.chime([1319, 1047], 0.32, 1.1), 0.0, 0.20)                             # the lift: ding-dong, at frame 0
    put(si.servo(1.1, 180, 120), 0.25, 0.10)                                      # its doors
    put(om.door(0.30), T_OPEN, 0.30)
    for i_ in range(3):
        put(sx.thunk(0.04, 600), T_IN + 0.08 + i_ * 0.24, 0.12)
    put(om.door(0.25), T_SHUT, 0.25); put(sx.thunk(0.3, 80), T_SLAM, 0.90)
    put(si.servo(0.25, 700, 760), T_DROP0 - 0.3, 0.10)
    put(sx.thunk(0.35, 150), T_DROP1, 1.0); put(sx.thunk(0.12, 420), T_DROP1 + 0.01, 0.6)
    put(bm.chime([2400, 3100, 2700], 0.05, 0.5), T_DROP1 + 0.06, 0.16)
    put(bm.chime([1568, 2093], 0.08, 0.5), at["c3"] + 0.15, 0.16)                 # ka-ching
    for i_ in range(4):
        put(sx.thunk(0.03, 1500), at["red"] + 0.05 + i_ * 0.08, 0.08)             # typing
    put(sx.thunk(0.05, 1100), at["red"] + 0.40, 0.16)                             # ENTER
    put(an.buzz(), at["red"] + 0.50, 0.30)
    put(sx.thunk(0.05, 900), at["f3"] + 0.75, 0.20)                               # approved
    put(bm.chime([1047, 1319, 1568], 0.09, 0.7), at["wipe"] + 0.6, 0.20)
    put(sx.thunk(0.08, 300), at["plaster"] + 0.3, 0.15)
    put(bm.chime([1760, 2349], 0.07, 0.3), at["post"] + 0.3, 0.14)
    for i_ in range(3):
        put(sx.thunk(0.04, 700), at["round"] + 0.05 + i_ * 0.25, 0.05)
    put(an.slurp(), at["lick"] + 0.40, 0.35)
    put(sx.whoosh(0.05), at["travel"] + 0.05, 0.18)
    for i_ in range(3):
        put(an.squeak(), at["scrub"] + 0.08 + i_ * 0.36, 0.11)
    put(an.squeak(), at["eww"] + 0.05, 0.10); put(an.squeak(), at["eww"] + 0.30, 0.10)
    for i_ in range(5):                                                           # the week: ENTER, a page, ENTER, a page
        put(sx.thunk(0.03, 1400), at["week"] + i_ * 0.46, 0.10)
        if i_:
            put(sx.rustle(0.18), at["week"] + i_ * 0.46 + 0.03, 0.10)
    for i_ in range(6):                                                           # the lipstick, letter by letter
        put(an.squeak(), at["week"] + 0.75 + i_ * 0.27, 0.05)
    put(om.door(0.25), at["ret"], 0.25)
    put(sx.whoosh(0.08)[::-1].copy(), at["memory"], 0.35)
    put(an.buzz(0.35) * 0.4, at["show"] + 0.2, 0.4)
    put(sx.thunk(0.2, 90), at["fury"] + 0.05, 0.5)
    put(bm.chime([2093, 2637], 0.06, 0.4), at["flirt"] + 0.15, 0.12)
    for i_ in range(3):
        put(sx.thunk(0.04, 600), at["leave"] + 0.05 + i_ * 0.2, 0.14)
    put(sx.thunk(0.3, 80), at["leave"] + 0.95, 0.90)                              # he slams it
    put(sx.whoosh(0.05), at["heal"] + 0.15, 0.25)
    put(sx.rustle(0.25), at["zero"] + 0.45, 0.12)                                 # the page turns: MONDAY
    m += voice
    m += si.lp(np.random.default_rng(5).standard_normal(len(m)), 160) * 0.006
    env = (np.abs(voice) > 0.01).astype(float)
    env = si.lp(env, int(SR * 0.35)); env = env / max(1e-6, env.max())
    b = mus.bed(music, len(voice) / SR, 0.9)                                      # the theme from the first second
    b = b[:len(voice)] if len(b) >= len(voice) else np.pad(b, (0, len(voice) - len(b)))
    mix = m + b * (0.16 - 0.12 * np.clip(env * 4, 0, 1))
    mix = mix[:int(total * SR)]
    mix *= 0.5 / max(1e-6, np.abs(mix).max())
    wav = os.path.join(out_dir, "mix.wav")
    sf.write(wav, np.stack([mix, mix], 1).astype(np.float32), SR)
    out = os.path.join(d, "fs_film7_%d.mp4" % (540 * S))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(DR), "-i", "%s/f%%05d.png" % out_dir, "-i", wav,
                    "-vf", "fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "18", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-color_range", "tv", "-frames:v", str(int(round(total * 30))),
                    "-af", "loudnorm=I=-14.5:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    for _ in range(2):
        r_ = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
        I = float([l for l in r_.stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        g = -15.0 - I
        if abs(g) < 0.3:
            break
        tmp = out + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-c:v", "copy", "-af",
                        "volume=%.2fdB,alimiter=limit=0.66:level=false" % g, "-ar", "48000", "-c:a", "aac", "-b:a",
                        "192k", "-movflags", "+faststart", tmp], check=True)
        os.replace(tmp, out)
    print("wrote", out, "%.2f s, %d shots" % (total, len(LIST)))
    return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    build(d, 2 if (len(sys.argv) > 2 and sys.argv[2] == "1080") else 1)
