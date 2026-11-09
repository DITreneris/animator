"""Cover thumbnail for Downloads Expedition v05 (1080x1920, key art safe inside the centre 1080x1440 that
profile grids crop to). Drawn with the episode's own kit, so the characters match the film.
Usage: python3 thumb_dlx.py out.png"""
import sys
import cairo
import kit
import anim
import brand
import dlx
import dlx_kit as dk
from kit import W, H, Ctx, grain, sfx, rect

dlx.ENDING = "B"
SCALE = 2
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * SCALE, H * SCALE)
c = cairo.Context(surf)
c.set_source_rgb(1, 1, 1); c.paint()
c.scale(SCALE, SCALE)
k = Ctx(c, 0)
dlx.STATE["t"] = 17.2                                # no one is talking: closed mouths

# the scene, pushed in a little on RUSH under FINAL (28), MAX staring, PAM typing on
kit.office_bg(k)                                     # wall behind the shifted set, so no white edge
c.save()
anim.camera(c, 270, 640, 1.0, dx=0, dy=70)
dlx.office(k, door_open=1.0, hook=(False, False), pam=True, pam_pose="type")
head, top = dlx.squashed_rush(k, 17.2, dlx.SQ, 1.0, gaze=(-0.8, -0.2), face="shock")
dlx.lid(k, top)
pm = dlx.person(k, "MAX", dlx.MX + 20, dlx.MF, dlx.MS, pose="shock", face="shock", look=(0.8, 0.1), seed=33)
c.restore()

# impact word on the sheet's corner
sfx(k, "THUNK!", 400, 520, 46, rot=0.12)

# title card above the set (the DOWNLOADS sign and the UPTIMEZ plaque stay visible below it)
rect(k, 24, 104, W - 48, 176, (1, 1, 1), 1401, lw=3)
kit.text(k, "WHERE'S THE", W / 2, 140, 40, kit.INK)
c.save(); c.translate(W / 2, 198); c.rotate(-0.03)
sfx(k, "FINAL?!", 0, 0, 72, rot=0, fill=(1.0, 0.86, 0.15))
c.restore()
kit.text(k, "(3)  >  (27)  >  (28)", W / 2, 254, 26, brand.NAVY)

grain(k, 0.05)
surf.write_to_png(sys.argv[1] if len(sys.argv) > 1 else "DLX_v05_thumbnail.png")
