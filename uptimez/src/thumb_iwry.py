"""Cover thumbnail for "I Will Replace You" (1080x1920). Key art inside the centre 1080x1440 that profile
grids crop to (y 120-840 at the 540x960 drawing scale). Drawn with the film's own kit:
the robot snapped upright and pointing, its shout as the title; Sofía horrified; Don giving a thumbs-up
behind it; the whisper as the hook. Usage: python3 thumb_iwry.py out.png"""
import sys
import math
import cairo
import kit
import anim
import pt42
import waiter_kit as w
import cafe_kit as ck
import sofia_v4 as sf
import don_v4 as dv
from kit import W, H, Ctx, grain, rect

SCALE = 2
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * SCALE, H * SCALE)
c = cairo.Context(surf)
c.scale(SCALE, SCALE)
k = Ctx(c, 0)

# the cafeteria, pushed in
c.save(); c.translate(270, 480); c.scale(1.35, 1.35); c.translate(-250, -560)
ck.room(k)
ck.menu_board(k, 40, 300)
c.restore()
c.set_source_rgba(1, 0.97, 0.9, 0.35); c.paint()                      # quiet the background

# Don at the back right, small: the flattered thumbs-up (the one who approves)
c.save(); c.translate(474, 690); c.scale(0.82, 0.82); c.translate(-474, -690)
p = dv.don(k, 474, 950, 1.0, anim.key(dv.POSE_THUMB), "grin", look=(-1, 0))
dv.thumbs_up(k, p["hands"][1])
c.restore()

# Sofía left, horrified: chest at the robot's arm height, face clear of the finger
sf.sofia(k, 82, 962, 1.4, "stand", "horrified", look=(0.8, 0), folder="none")

# the robot: locked, upright, pointing at her chest (fingertip stops ~35 px short of her hair)
rb = w.robot(k, 372, 905, 1.4, "lock", "stern", look=(-1.6, 0.1), talk=0.9)

# table edge in front
rect(k, -20, 838, 600, 30, ck.TABLE_TOP_COL, 1801, lw=2.6)
rect(k, -10, 862, 580, 120, ck.TABLE_FRONT, 1802, lw=2.6)
ck.bolt(k, 60, 840, 1.1, 1.3, 1803)

# title: the robot's own shout
hx, hy = rb["head"]
ck.shout(k, "I WILL\nREPLACE YOU!", (hx - 30, hy - 60), 270, 215, size=64)

# the hook: the whisper
ck.whisper(k, "...if that's okay, sir?", (hx + 46, hy + 10), 352, 792, size=30)

grain(k, 0.05)
surf.write_to_png(sys.argv[1] if len(sys.argv) > 1 else "iwry_thumbnail.png")
