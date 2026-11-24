"""PICK A SIDE (episode 14): stage 4, the blocking sheet for the hardest beat, 1.1-1.3 (Tomas, /grill-me 23 Nov): the
blinds tug at frame 0, the blind tearing onto Don, his face through the slats. Real 540x960 camera frames on the set
(ps_set v3) with the approved rigs: don_ps (v2), robot_ps, sofia_ps, pm_ps. Script v6, 1.1-1.3.
  1.1 S2, knees up (no floor: the tape never in this framing): Don at the left cord, the robot at the right.
      a frame 0: the blinds up, Don's hand on his cord · b he pulls: down, the room dims, a sun on the robot's visor ·
      c the robot pulls: up · d down again, faster (speed lines)
  1.2 split (Tomas, /grill-me: the wide made everyone tiny): 1.2a medium, the blind tears off and drops over Don;
      1.2b Pam, Mom, Sofía mid-room by the counter's end, Pam's cup stops halfway
  1.1 Don faces us, his eyes up to the cord (Tomas: no back view)
  1.3 medium: Don's face through the slats ("This meeting does not exist.")
  python3 ps_block.py [out_dir] -> ps_block_v1.png"""
import os
import sys
import math
import cairo
import kit
import fs_storyboard_v17 as sbv
import ps_set as pss
import don_ps as dp
import robot_ps as rp
import sofia_ps as sp
import pm_ps as pm
from kit import INK

F = pss.F
DON_X, ROB_X = 64, 186                                     # in front of the glass: Don under his cord, the robot under its
CAM_S2 = (112, 515, 2.05)                                   # knees up: y 281-749, the floor out of frame


def lines(c, pts, col=INK, w=3.0):
    c.set_source_rgb(*col); c.set_line_width(w); c.set_line_cap(1)
    for x0, y0, x1, y1 in pts:
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_line_cap(0)


def frame_11(phase):
    """1.1, S2: phase a (up, his hand on the cord), b (he pulls: down), c (it pulls: up), d (down, faster)."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sbv.view(c, *CAM_S2)
    down = phase in ("b", "d")
    pss.room(k, blind="down" if down else "up", u=0.92 if down else 0.0, phone=None, dim=False)
    don_pose = (-168, 6, 8, 0) if not down else (-150, -20, 8, 0)
    dp.don(k, DON_X, F, 0.60, don_pose, "squint" if not down else "smug", (-0.4, -0.6))
    rob_arms = ((-8, 0), (172, -4)) if not down else ((-8, 0), (8, 0))
    rp.robot(k, ROB_X, F + 4, rp.S_OFFICE, arms=rob_arms, visor="sun" if down else None)
    if down:                                                 # the room goes dark
        c.set_source_rgba(0.05, 0.05, 0.10, 0.30); c.rectangle(-200, 0, 900, 960); c.fill()
    if phase == "d":                                         # faster: speed lines along the slats
        lines(c, [(pss.GX0 + 20, 470, pss.GX0 + 20, 540), (pss.GX0 + 75, 450, pss.GX0 + 75, 560), (pss.GX0 + 130, 470, pss.GX0 + 130, 540)],
              (1, 1, 1), 2.4)
    c.restore()
    return surf


def frame_12a():
    """1.2a (Tomas, /grill-me: split), medium on Don: the blind tears off its rail and drops over him; CRASH."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sbv.view(c, DON_X + 40, 560, 1.7)
    pss.room(k, blind="torn", phone=None)
    o = dp.don(k, DON_X + 20, F + 10, 0.60, "stand", "shock", (0, 0))
    dp.blind_over(k, o["head"], 0.60)
    hx, hy = o["head"]
    lines(c, [(hx - 60, hy - 120, hx - 52, hy - 80), (hx, hy - 135, hx, hy - 92), (hx + 60, hy - 120, hx + 52, hy - 80)])   # it dropped
    for i, (dx, dy) in enumerate(((-80, 40), (86, 20), (-70, 160), (90, 150))):                                           # the CRASH
        lines(c, [(hx + dx, hy + dy, hx + dx * 1.3, hy + dy - 10)], INK, 3.4)
    rp.robot(k, ROB_X + 10, F + 4, rp.S_OFFICE, visor="sun")
    c.restore()
    return surf


def frame_12b():
    """1.2b, the three mid-room by the counter's end, where the tape will run: Pam's cup stops halfway."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sbv.view(c, 590, 640, 1.45)
    pss.room(k, blind="torn", phone="dark")
    pm.pam(k, 520, F + 40, 0.54, "cup_mid", "frozen", (-1, -0.1))
    pm.mom(k, 592, F + 34, 0.54, "folded", "unimpressed", (-1, 0))
    sp.sofia(k, 662, F + 44, 0.56, "hip_out", "smile", look=(-1, 0))
    c.restore()
    return surf


def frame_13():
    """1.3, medium: Don under the blind, his face through the bent slats; the line is whispered."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(surf); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sbv.view(c, DON_X + 20, 600, 2.4)
    pss.room(k, blind="torn", phone=None)
    o = dp.don(k, DON_X + 20, F + 10, 0.60, "stand", "neutral", (0, 0))
    dp.blind_over(k, o["head"], 0.60)
    c.restore()
    return surf


def sheet(out):
    frames = [("1.1a · FRAME 0", "the blinds up; Don's hand on his cord", frame_11("a")),
              ("1.1b · 0:00.4", "he pulls: down, the room dims, ☀ on its visor", frame_11("b")),
              ("1.1c · 0:00.8", "its hand pulls: up", frame_11("c")),
              ("1.1d · 0:01.2", "down, faster", frame_11("d")),
              ("1.2a · 0:01.8", "the blind tears off and drops over Don: CRASH", frame_12a()),
              ("1.2b · 0:02.3", "the three, mid-room: Pam's cup stops halfway", frame_12b()),
              ("1.3 · 0:02.8", "his face through the slats: \"This meeting does not exist.\"", frame_13())]
    W = len(frames) * 290 + 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 640); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    c.select_font_face("Inter", 0, 1); c.set_font_size(20); c.set_source_rgb(1, 1, 1); c.move_to(20, 36)
    c.show_text("PICK A SIDE · stage 4 · blocking 1.1-1.3, the hardest beat · real camera frames at 270 px · v1")
    for i, (n, txt, f) in enumerate(frames):
        x0 = 20 + i * 290
        c.save(); c.translate(x0, 60); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1); c.move_to(x0, 566); c.show_text(n)
        c.select_font_face("Inter", 0, 0); c.set_font_size(11.5)
        words, line, y = txt.split(), "", 586
        for w in words:
            if len(line) + len(w) > 40:
                c.move_to(x0, y); c.show_text(line); line, y = w, y + 16
            else:
                line = (line + " " + w).strip()
        c.move_to(x0, y); c.show_text(line)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_block_v1.png"))
