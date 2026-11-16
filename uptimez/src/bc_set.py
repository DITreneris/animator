"""v4 (bc_set_v3.py = v3, kept): the room is dressed. A ficus in a pot stands by the door under the job notice (it is
in frame 0), the lower wall is a darker band under a rail, and a window we never see throws a soft patch of light
on the wall between the poster and the monitor. None of it is a sign; all of it sits behind the cast.
v3: room for speech bubbles. The storyboard's bubble pass (the series' lessons: a bubble
sits beside the face or just above the head, never over a face or a sign, inside the app's safe zones) needed clear
wall above every head, so:
  - the BIAS MONITOR hangs 96 higher and the poster 56 higher;
  - the chair stands 15 to the right and the poster 14, so the poster is centred over the chair and no longer
    touches the notice by the door: a close frame can now hold one without cutting the other;
  - the UptimeZ sign moves from beside the poster to the wall behind the robot;
  - the cameras are the storyboard's (v3): every sign in a frame is whole or absent.
v2, for script v4: the panel sits Sofia, Don, Pam (Sofia nearest the candidate's chair,
so the looks run in one line along the table), the robot stands at the far right end, and the client's phone lies
on the table by Don (table(phone="buzz" / "still")).
Set for "The Best Candidate", v1: the interview room. World units as tg_set / mf_set (floor line FLOOR_Y, standing
feet at FEET; a 9:16 camera (cx, cy, z[, roll]) maps the world into 540 x 960). Everyone faces us, as in the earlier
episodes; the staging is side-on. Left to right:
- the door in the far-left wall (frame 0 and the loop), plaque INTERVIEWS, and beside it the notice for the job:
  ASSISTANT TO DON, 1 POSITION;
- the candidate's chair, alone on the open floor, under the framed company poster WE HIRE ON MERIT (the reveal
  happens right here, under it);
- the HR robot, standing at the end of the panel table;
- the panel table: Don (his folded card, HEAD OF TALENT, in marker), Pam, Sofia; they look screen left at the chair;
- on the wall above the panel, the BIAS MONITOR: idle, PROCEED (green, with the reason in small print), AGEISM
  DETECTED (red), FAMILY STATUS: PROTECTED (red), NO BIAS DETECTED (green, a tick). It is in every panel shot,
  so the rulings read with the sound off.
Bare otherwise: the Day One wall and floor, the UptimeZ sign."""
import math
import cairo
import kit
import brand
import pt42
import tg_set as ts
import mf_set as ms
import mom_bc as mb
import props_bc as props
from kit import INK, cut, rect, ellipse

FLOOR_Y, FEET, FEET_BACK, SEAT_DROP, TABLE_TOP = ms.FLOOR_Y, ms.FEET, ms.FEET_BACK, ms.SEAT_DROP, ms.TABLE_TOP
SEAT = FEET + SEAT_DROP                      # panel sitters (their legs are behind the table)
CHAIR_SEAT = FEET - 92                       # the candidate's chair seat
POS = {"door": 70, "notice": 196, "chair": 350, "sofia": 665, "don": 825, "pam": 985, "robot": 1140}
TABLE_X0, TABLE_X1 = 572, 1072
POSTER = (262, 176, 176, 104)
MON = (692, 190, 264, 112)
DOOR_W, DOOR_H = ms.DOOR_W, ms.DOOR_H
GREEN = (0.13, 0.62, 0.36)
RED = (0.82, 0.16, 0.18)
NAVY = (0.12, 0.17, 0.33)
CAMS = {"wide": (600, 500, 0.455),
        "door": (240, 470, 1.1),                           # frame 0: the door, the notice, the poster, the chair
        "low": (357, 440, 1.27),                           # the small one, small in a tall frame
        "feet": (350, 694, 3.8), "legs": (350, 722, 2.5), "boot": (318, 722, 3.8),
        "small_say": (410, 570, 2.0),                      # a candidate left of centre, the bubble beside the face
        "loom": (359, 496, 2.4), "loom_say": (400, 496, 2.4), "macho_say": (413, 548, 1.9),
        "mom": (350, 455, 1.3), "mom_cu": (415, 585, 2.0),  # Mom under the poster, level and centred; and her one close-up
        "pov": (745, 590, 1.8),                            # up at the panel from the small one's chair
        "don": (825, 555, 2.4),                            # the question, three times
        "eyes": (825, 500, 6.0),
        "sofia": (610, 572, 2.4),
        "panel": (826, 455, 1.2),                          # all three and the whole monitor
        "sofia_don": (787, 420, 1.48), "don_pam": (856, 414, 1.53),
        "paddle": (735, 478, 4.2),
        "robot": (1196, 460, 1.7),
        "reveal": (416, 406, 1.6), "lick": (378, 500, 2.6), "stain": (461, 556, 3.4),
        "tilt": (510, 444, 3.65, 0.13)}                    # the one dutch angle
to_screen, with_cam, seated = ms.to_screen, ms.with_cam, ms.seated
DADO_Y = 598                                               # the rail: below every seated chin, above the table top
DADO = (0.84, 0.78, 0.66)
STATES = {
    "idle": (NAVY, ["BIAS MONITOR"], "ACTIVE"),
    "proceed_height": (GREEN, ["PROCEED"], "HEIGHT: NOT PROTECTED"),
    "proceed_looks": (GREEN, ["PROCEED"], "ATTRACTIVENESS: NOT PROTECTED"),
    "ageism": (RED, ["AGEISM", "DETECTED"], None),
    "family": (RED, ["FAMILY STATUS:", "PROTECTED"], None),
    "clear": (GREEN, ["NO BIAS", "DETECTED"], None),
}


def wall(k):
    rect(k, -600, -400, 2400, FLOOR_Y + 400, kit.WALL, 100, shadow=False, outline=False)
    rect(k, -600, FLOOR_Y, 2400, 900, kit.FLOOR, 101, shadow=False)
    c = k.c                                                # v4: window light, then the dado band and its rail
    c.save()
    for dx in (0, 62, 124):
        c.move_to(486 + dx, 196); c.line_to(538 + dx, 196); c.line_to(506 + dx, 560); c.line_to(454 + dx, 560); c.close_path()
    c.set_source_rgba(1.0, 0.97, 0.82, 0.30); c.fill()
    c.restore()
    rect(k, -600, DADO_Y, 2400, FLOOR_Y - DADO_Y, DADO, 103, shadow=False, outline=False)
    c.set_source_rgb(0.56, 0.47, 0.36); c.set_line_width(2.4); c.move_to(-600, DADO_Y); c.line_to(1800, DADO_Y); c.stroke()
    rect(k, -600, FLOOR_Y - 10, 2400, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)
    pt42.wall_sign(k, 1100, 250, 24)                       # v3: behind the robot


def ficus(k, x=197, sway=0.0):
    """The office ficus, by the door under the notice. sway: degrees, for a breath of air when the door opens."""
    c = k.c
    base = FLOOR_Y + 14
    cut(k, [(x - 26, base - 44), (x + 26, base - 44), (x + 20, base), (x - 20, base)], (0.72, 0.42, 0.28), lw=2.2)
    rect(k, x - 30, base - 52, 60, 10, (0.78, 0.47, 0.32), 141, shadow=False, lw=2)
    c.save(); c.translate(x, base - 50); c.rotate(math.radians(sway)); c.translate(-x, -(base - 50))
    c.set_source_rgb(0.36, 0.26, 0.18); c.set_line_width(5); c.set_line_cap(1)
    c.move_to(x, base - 50); c.curve_to(x - 6, base - 96, x + 8, base - 128, x + 2, base - 170); c.stroke()
    leaves = [(-26, -76, -0.9, 0), (24, -86, 0.8, 1), (-34, -108, -0.6, 1), (30, -118, 0.5, 0), (-22, -138, -0.3, 0),
              (22, -150, 0.35, 1), (-38, -160, -0.7, 0), (36, -170, 0.75, 1), (-12, -178, -0.2, 1), (12, -192, 0.15, 0),
              (-28, -196, -0.5, 1), (30, -200, 0.55, 0), (0, -212, 0.0, 1)]   # the top leaf stays under the notice
    for i, (dx, dy, rot, tone) in enumerate(leaves):
        c.save(); c.translate(x + dx, base - 50 + dy); c.rotate(rot)
        col = ((0.20, 0.50, 0.30), (0.26, 0.60, 0.36))[tone]
        ellipse(k, 0, 0, 13, 23, col, 143 + i, shadow=False, lw=1.8)
        c.set_source_rgb(0.14, 0.36, 0.22); c.set_line_width(1.2); c.move_to(0, -17); c.line_to(0, 17); c.stroke()
        c.restore()
    c.restore()


def door(k, open_=0.0):
    """open_ 0 = shut; 1 = wide open (the panel swings into the room, we see the corridor)."""
    c = k.c
    x0, y0 = POS["door"] - DOOR_W / 2, FLOOR_Y - DOOR_H
    rect(k, x0 - 10, y0 - 10, DOOR_W + 20, DOOR_H + 10, (0.93, 0.92, 0.88), 110, shadow=False, lw=2.2)
    rect(k, x0, y0, DOOR_W, DOOR_H, (0.18, 0.19, 0.24), 111, shadow=False, lw=2)
    c.set_source_rgba(1, 1, 1, 0.08); c.rectangle(x0, FLOOR_Y - 40, DOOR_W, 40); c.fill()
    w = DOOR_W * (1 - 0.82 * open_)
    cut(k, [(x0, y0), (x0 + w, y0 - 14 * open_), (x0 + w, FLOOR_Y + 14 * open_), (x0, FLOOR_Y)], ms.DOOR, lw=2.2)
    if open_ < 0.5:
        for (yy, hh) in ((y0 + 30, 160), (y0 + 220, 170)):
            rect(k, x0 + 18, yy, w - 36, hh, ms.DOOR_DARK, 112 + yy, shadow=False, lw=1.6)
        ellipse(k, x0 + w - 18, y0 + 222, 7, 7, (0.80, 0.70, 0.30), 113, shadow=False, lw=1.6)
        rect(k, x0 + 22, y0 + 58, w - 44, 26, (0.97, 0.97, 0.95), 114, shadow=False, lw=1.4)
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
        t = "INTERVIEWS"; e = c.text_extents(t)
        sq = min(1.0, (w - 52) / e.x_advance)               # v4: the word narrows with the door as it swings
        c.save(); c.translate(x0 + w / 2, y0 + 75); c.scale(max(sq, 0.05), 1)
        c.set_source_rgb(*INK); c.move_to(-e.x_advance / 2, 0); c.show_text(t)
        c.restore()


def notice(k, x=None, y=318):
    """The job, on a sheet taped by the door."""
    c = k.c
    x = POS["notice"] if x is None else x
    c.save(); c.translate(x, y); c.rotate(-0.03)
    rect(k, -42, -52, 84, 104, (0.99, 0.99, 0.97), 130, lw=1.8)
    c.set_source_rgb(*brand.GREEN); c.rectangle(-40.5, -50.5, 81, 14); c.fill()
    kit.text(k, "NOW HIRING", 0, -40, 9.5, (1, 1, 1), font="Inter", bold=True)
    kit.text(k, "ASSISTANT", 0, -16, 13.5, NAVY)
    kit.text(k, "TO DON", 0, 2, 13.5, NAVY)
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.move_to(-30, 14); c.line_to(30, 14); c.stroke()
    kit.text(k, "1 POSITION", 0, 28, 9, INK, font="Inter", bold=True)
    kit.text(k, "interviews today", 0, 42, 7.5, (0.4, 0.42, 0.5), font="Inter")
    for sx in (-1, 1):                                                     # tape
        c.set_source_rgba(0.95, 0.90, 0.60, 0.9); c.rectangle(sx * 30 - 9, -57, 18, 9); c.fill()
    c.restore()


def poster(k):
    """The framed company poster behind the candidate's chair."""
    c = k.c
    x, y, w, h = POSTER
    rect(k, x - 7, y - 7, w + 14, h + 14, (0.22, 0.20, 0.20), 140, lw=2.2)
    rect(k, x, y, w, h, (0.99, 0.98, 0.95), 141, shadow=False, lw=1.4)
    c.set_source_rgb(*NAVY); c.rectangle(x + 1, y + 1, w - 2, 20); c.fill()
    brand.mark(c, x + 6, y + 3, 15, zzz=False)
    kit.text(k, "UPTIMEZ VALUES", x + w / 2 + 8, y + 12, 8.5, (1, 1, 1), font="Inter", bold=True)
    kit.text(k, "WE HIRE", x + w / 2, y + 48, 27, NAVY)
    kit.text(k, "ON MERIT", x + w / 2, y + 80, 27, brand.GREEN)


def monitor(k, state="idle", t=0.0):
    """The BIAS MONITOR on the wall above the panel. state: a key of STATES."""
    c = k.c
    x, y, w, h = MON
    col, lines, small = STATES[state]
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(x + w / 2, y - 26); c.line_to(x + w / 2, y); c.stroke()   # bracket
    rect(k, x - 8, y - 8, w + 16, h + 16, (0.14, 0.14, 0.17), 150, lw=2.4)
    rect(k, x, y, w, h, col, 151, shadow=False, lw=1.6)
    c.set_source_rgba(1, 1, 1, 0.10); c.move_to(x, y); c.line_to(x + w * 0.42, y); c.line_to(x + w * 0.2, y + h)
    c.line_to(x, y + h); c.close_path(); c.fill()
    if state != "idle":
        kit.text(k, "BIAS MONITOR", x + 44, y + 12, 7.5, (1, 1, 1), font="Inter", bold=True)
    n = len(lines)
    top = y + (h - (16 if small else 0)) / 2 - (n - 1) * 17 + (6 if state != "idle" else 0)
    for i, t_ in enumerate(lines):
        c.select_font_face("Lilita One", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        size = 34
        c.set_font_size(size); e = c.text_extents(t_)
        size = min(size, size * (w - 34 - (38 if state == "clear" else 0)) / e.x_advance)
        kit.text(k, t_, x + w / 2 - (17 if state == "clear" else 0), top + i * 34, size, (1, 1, 1))
    if small:
        kit.text(k, small, x + w / 2, y + h - 15, 9.5 if len(small) < 24 else 8.2, (1, 1, 1), font="Inter", bold=True)
    if state == "clear":                                                   # the tick
        c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(x + w - 46, y + h / 2 + 2); c.line_to(x + w - 36, y + h / 2 + 14); c.line_to(x + w - 16, y + h / 2 - 14)
        c.stroke()
    ellipse(k, x + w - 10, y + h + 3, 2.6, 2.6, (0.3, 0.95, 0.5) if state != "idle" or int(t * 2) % 2 == 0 else (0.2, 0.3, 0.25),
            152, shadow=False, outline=False)


def chair(k, x=None, seed=0):
    """The candidate's chair: plain, a little too tall for some and too small for others."""
    x = POS["chair"] if x is None else x
    col, dark = (0.36, 0.39, 0.46), (0.22, 0.23, 0.27)
    rect(k, x - 40, CHAIR_SEAT - 112, 80, 104, col, seed + 160, lw=2.2)
    for sx in (-1, 1):
        rect(k, x + sx * 36 - 4, CHAIR_SEAT + 10, 8, FEET - CHAIR_SEAT - 6, dark, seed + 162 + sx, shadow=False, lw=1.8)
    rect(k, x - 46, CHAIR_SEAT, 92, 14, col, seed + 161, lw=2.2)


def mom_on_chair(k, x=None, **kw):
    """Mom seated on the candidate's chair: her body down to the seat, her lap, her shins and shoes in front."""
    c = k.c
    x = POS["chair"] if x is None else x
    feet = CHAIR_SEAT + 150                                               # her hips come down to the seat
    c.save(); c.rectangle(-2000, -2000, 5000, 2000 + CHAIR_SEAT + 12); c.clip()
    out = mb.mom(k, x, feet, 1.0, **kw)
    c.restore()
    cut(k, [(x - 62, CHAIR_SEAT - 2), (x + 62, CHAIR_SEAT - 2), (x + 60, CHAIR_SEAT + 30), (x - 60, CHAIR_SEAT + 30)],
        mb.TEAL, shadow=False, lw=2.2)                                    # her lap: the coat over her knees
    for sx in (-1, 1):
        rect(k, x + sx * 22 - 9, CHAIR_SEAT + 30, 18, FEET - CHAIR_SEAT - 44, mb.LEGS, 170 + sx, shadow=False, lw=2)
        ellipse(k, x + sx * 25, FEET - 8, 19, 9, mb.SHOE, 173 + sx, lw=2)
    return out


def nameplate(k, x, y):
    """Don's folded card on the table: HEAD OF TALENT, in marker."""
    c = k.c
    cut(k, [(x - 44, y), (x + 44, y), (x + 40, y - 24), (x - 40, y - 24)], (0.99, 0.99, 0.97), lw=1.8)
    kit.text(k, "HEAD OF TALENT", x, y - 11, 9.5, props.MARKER, font="Permanent Marker")


def table(k, items=True, phone=None):
    """Drawn after the sitters: the top, the apron, the modesty panel, and what lies on it."""
    c = k.c
    t0 = TABLE_TOP
    cut(k, [(TABLE_X0 + 10, t0), (TABLE_X1 - 10, t0), (TABLE_X1, t0 + 18), (TABLE_X0, t0 + 18)], ts.WOOD, lw=2.2)
    rect(k, TABLE_X0, t0 + 18, TABLE_X1 - TABLE_X0, 12, ts.WOOD_DARK, 970, shadow=False, lw=2)
    rect(k, TABLE_X0 + 12, t0 + 30, TABLE_X1 - TABLE_X0 - 24, FEET + 14 - (t0 + 30), ts.WOOD, 972, lw=2)
    c.set_source_rgb(*ts.WOOD_DARK); c.set_line_width(2)
    for gx in range(TABLE_X0 + 80, TABLE_X1 - 40, 120):
        c.move_to(gx, t0 + 32); c.line_to(gx, FEET + 12); c.stroke()
    if items:
        nameplate(k, POS["don"] - 44, t0 + 9)
    if phone:
        props.phone_small(k, POS["don"] + 70, t0 + 7, 1.0, buzz=(phone == "buzz"))


def backdrop(k, door_open=0.0, state="idle", t=0.0, with_chair=True, with_poster=True, ficus_sway=0.0):
    wall(k)
    door(k, door_open)
    notice(k)
    ficus(k, sway=ficus_sway)
    if with_poster:
        poster(k)
    monitor(k, state, t)
    for name in ("don", "pam", "sofia"):
        ms.chair_back(k, POS[name])
    if with_chair:
        chair(k)


def hired_stamp(k, x, y, s=1.0, rot=-0.12, paper=False):
    """The robot's stamp: HIRED, and the job. paper: on a cream slip, for dark backgrounds."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if paper:
        kit.rect(k, -112, -52, 224, 104, (0.98, 0.96, 0.90), 961, lw=2.4)
    c.set_source_rgba(*GREEN, 0.92); c.set_line_width(5)
    ms_r = 8
    c.new_path(); c.arc(-96 + ms_r, -38 + ms_r, ms_r, math.pi, 1.5 * math.pi); c.arc(96 - ms_r, -38 + ms_r, ms_r, 1.5 * math.pi, 0)
    c.arc(96 - ms_r, 38 - ms_r, ms_r, 0, 0.5 * math.pi); c.arc(-96 + ms_r, 38 - ms_r, ms_r, 0.5 * math.pi, math.pi); c.close_path()
    c.stroke()
    kit.text(k, "HIRED", 0, -6, 44, GREEN)
    kit.text(k, "ASSISTANT TO DON", 0, 24, 12.5, GREEN, font="Inter", bold=True)
    c.restore()
