"""Cover thumbnail for "How Sofía Survived Day One" (1080x1920; key art inside the centre 1080x1440 that
profile grids crop to, i.e. y 120-840 at the 540x960 drawing scale). Drawn with the film's own kit:
Sofía in a close-up with her raised eyebrow, DAY 1 sticker and Pam's coffee; the coffee maker still
WAITING FOR APPROVAL behind her; the robot in its DON 2.0 badge peeking in.
Usage: python3 thumb_day1.py out.png"""
import sys
import cairo
import kit
import pt42
import sofia as sf
import day1_kit as dk
import day1_sb_v3 as sb
import anim
from kit import W, H, Ctx, grain, sfx, rect

SCALE = 2
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * SCALE, H * SCALE)
c = cairo.Context(surf)
c.set_source_rgb(1, 1, 1); c.paint()
c.scale(SCALE, SCALE)
k = Ctx(c, 0)

# set: wall, floor line, sign
rect(k, -40, -40, W + 80, 760, kit.WALL, 100, shadow=False, outline=False)
rect(k, -40, 700, W + 80, 400, kit.FLOOR, 101, shadow=False)
rect(k, -40, 690, W + 80, 16, (0.62, 0.5, 0.36), 102, shadow=False, lw=2)

# coffee maker behind her, left: still waiting
c.save(); c.translate(-40, 0)
dk.counter(k, -60, 300, 560)
dk.coffee_maker(k, 120, 560, 1.45, "waiting", sticker_at=sb.STICKER_V2)
c.restore()

# the robot peeks in from the right, watching her
c.save(); c.translate(485, 905); c.scale(1.25, 1.25); c.translate(-485, -905)
dk.robot(k, 485, 905, 1.0, "stand", "wide", look=(-1, 0.2), tilt=-0.10, badge="DON 2.0")
c.restore()

# Sofía, close: eyebrow up, looking at us, Pam's coffee raised, DAY 1 sticker
sf.BADGE_HOOK = lambda k_, bt, seed: sb.day1_sticker(k_, 2, bt + 30)
s = 2.15
sx, feet = 245, 1150
sb.shadow(k, sx, feet, 60, 10)
sof = sf.sofia(k, sx, feet, s, anim.key((-14, 40, 70, 100)), "eyebrow", look=(0.15, 0.05), seed=7, folder="none")
hx, hy = sof["hands"][1]
c.save(); c.translate(hx + 4 * s, hy + 8 * s); c.scale(s, s)
dk.mug(k, 0, 0, 1.0, steam=0.55)
c.restore()
sf.BADGE_HOOK = None

# title, top of the safe area
rect(k, 22, 128, W - 44, 150, (1, 1, 1), 1401, lw=3)
kit.text(k, "HOW SOFÍA SURVIVED", W / 2, 166, 36, kit.INK)
c.save(); c.translate(W / 2, 228); c.rotate(-0.03)
sfx(k, "DAY ONE", 0, 0, 74, rot=0, fill=(1.0, 0.86, 0.15))
c.restore()

# the 9:00 stamp, as in the film
c.save(); c.translate(448, 338); c.rotate(0.08)
rect(k, -62, -32, 124, 64, (1, 1, 1), 1501, lw=3)
kit.text(k, "9:00", 0, 2, 44, kit.INK)
c.restore()

sb.look(k, 0.0)
grain(k, 0.05)
surf.write_to_png(sys.argv[1] if len(sys.argv) > 1 else "day1_thumbnail.png")
print("head", sof["head"], "mug hand", (round(hx), round(hy)))
