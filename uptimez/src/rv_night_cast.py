"""Approved. (episode 16): night look-dev stills with the cast (stage 3; Tomas 28 Nov: "Padaryk kelias patobulintas
nakties su charakteriais, improve do not break").

The night is rv_night.py's grade (v3: the glass door shows the street at night) with its v4 options on: the light
lands (monitor and machine pools on the counter and on the faces near them, the robot's screen on the face it faces,
one cold patch on the floor in front of the door), the wall and floor fall off away from those sources, the door's
highlights quieter, contact shadows darkened. People and props keep their day colours (the canon night, bp_frame).
The throne keeps the warm rim (Tomas's pick).

The cast is drawn with episode 15's layout helpers (da_layouts: don_ps, pm_ps, robot_ps, dh_cast Father, sofia_da,
client_ps, with the series' scales): this script runs on a checkout that has episode 15's modules (branch
uptimez-double-agent, until it is merged). Sofía is in her episode 15 suit here: her episode 16 CEO power suit is not
drawn yet (stage 3, her sheet). Father stands: his folding chair is not drawn yet.
  python3 rv_night_cast.py all   -> ../the-review/rv_night_cast_N1_v1.png (the master wide), _N2_ (the counter),
                                    _N3_ (Don lit by the robot's screen), each with a _270.png
"""
import os
import sys
import math
import cairo
import kit
import fs_set4 as s4
import ps_set as pss
import dh_props as dprops
import fs_storyboard_v17 as sbv
import bp_frame as bp
import rv_night as rn
import da_layouts as L
import da_set as ds
import don_ps as dp
import pm_ps as pm
import robot_ps as rp
import dh_cast as dc
import sofia_da as sd
import client_ps as cp

EP = "../the-review/"
F = pss.F
MON = (s4.HOME["pam"][0] - 10, F - 210)                       # Pam's monitor, world
MACH = (dprops.MACHINE[0], dprops.MACHINE[1] - 70)            # the machine's front
DOOR = (97, 600)                                              # the glass door's middle


def _shadow(k, x, f, w, a=0.30):
    """a darker contact shadow for the night (the review's P1; the day ones wash out in the grade)."""
    if _PASS[0] == "mask":
        return
    c = k.c
    c.save(); c.translate(x, f + 1); c.scale(w, 6); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*bp.NIGHT_SHADOW, a); c.fill()


def _screen_text(k, o, lines, s=1.0):
    """v2 (cold round 4: "unreadable at 270", "covers the robot's face"): the text IS the robot's face. The visor goes
    dark and the words fill it, as episode 14's visor icons (robot_ps.visor_icon) replace its smile."""
    c = k.c
    x, y = o["screen"][:2]
    r = 50 * L.SC["robot"] * 1.02
    c.save()
    c.set_source_rgb(0.04, 0.07, 0.13); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*bp.NIGHT_MONITOR); c.select_font_face("Inter", 0, 1)
    size = 7.2 * s
    for i, t in enumerate(lines):
        c.set_font_size(size); e = c.text_extents(t)
        c.move_to(x - e.width / 2 - e.x_bearing, y + (i - (len(lines) - 1) / 2.0) * size * 1.15 + size * 0.38)
        c.show_text(t)
    c.restore()


# The lock (28 Nov, after cold round 6: the v4 band and rim read as "a ghost", "a hologram", "glassy legs", 2 of 2):
# the people keep only the shade away from the lights; no rim, no band (as v2, without its halos)
LOCK_CAST = dict(shade=0.30, key=(0, 0), rim=(0, 0, 0), rim_a=0.0, band=0)
PEOPLE = [False]       # set while the people are drawn: _frame records them into a mask for the cast light
_PASS = [None]


def person(fn):
    """draw one person; in the mask pass only people are drawn."""
    return fn()


def _people_mask(cam, draw):
    import numpy as np
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.save(); sbv.view(c, *cam)
    _PASS[0] = "mask"
    try:
        draw(k)
    finally:
        _PASS[0] = None
    c.restore(); s.flush()
    a = np.ndarray((960, s.get_stride() // 4, 4), np.uint8, s.get_data())[:, :540, 3]
    return a.astype(np.float64) / 255.0


def _frame(cam, draw, glows, lights, out, cast=None):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sbv.view(c, *cam); ds._floor_on(c)
    draw(k)
    c.restore()
    fx, fy, z = cam
    floor_y = 480 + (F - fy) * z
    old = rn.FALLOFF[0], rn.GLASS_HI[0]
    rn.FALLOFF[0], rn.GLASS_HI[0] = 0.32, 0.12
    rn.RIM_SEEN[0] = True; rn.FLOOR_END[0] = False; rn.CAST_LIGHT[0] = cast
    try:
        rn.grade(s, cam, floor_y, glows, rim=lambda k_: pss.throne(k_), lights=lights,
                 after=lambda c_: rn.moon_patch(c_, cam), people=_people_mask(cam, draw) if cast else None)
    finally:
        rn.FALLOFF[0], rn.GLASS_HI[0] = old
        rn.RIM_SEEN[0] = False; rn.FLOOR_END[0] = True; rn.CAST_LIGHT[0] = None
    s.write_to_png(out)
    sm = cairo.ImageSurface(cairo.FORMAT_ARGB32, 270, 480)
    c2 = cairo.Context(sm); c2.scale(0.5, 0.5); c2.set_source_surface(s, 0, 0); c2.get_source().set_filter(cairo.FILTER_GOOD)
    c2.paint(); sm.write_to_png(out.replace(".png", "_270.png"))
    print("wrote", out)


def _counter_dark(k):
    """v6 (the third night review, Tomas "itraukiam"): the counter's front falls off away from Pam's monitor, about
    30 % at its far end; drawn on the counter before the machine and the people in front of it."""
    c = k.c
    x0, x1, f = s4.CX0 - 6, s4.CX1 + 2, F
    g = cairo.LinearGradient(MON[0], 0, x1, 0)
    g.add_color_stop_rgba(0, *bp.NIGHT_SHADOW, 0.0); g.add_color_stop_rgba(1, *bp.NIGHT_SHADOW, 0.42)
    c.save(); c.set_source(g)
    c.move_to(x0, f); c.line_to(x0, f - 196); c.line_to(x1, f - 196); c.line_to(x1, f); c.close_path(); c.fill()
    g2 = cairo.LinearGradient(MON[0], 0, x0 - 4, 0)          # and toward its left end
    g2.add_color_stop_rgba(0, *bp.NIGHT_SHADOW, 0.0); g2.add_color_stop_rgba(1, *bp.NIGHT_SHADOW, 0.22)
    c.set_source(g2); c.rectangle(x0 - 4, f - 200, MON[0] - x0 + 4, 202); c.fill()
    c.restore()


def _machine_glow():
    """v6: the machine is the warm source (its lamp, 2700-3200 K): a small warm pool at its front and its red lamp."""
    x, base, sc = dprops.MACHINE
    return [(x, base - 20 * sc, 46, 26, bp.NIGHT_WARM, 0.32), (x - 38 * sc, base - 108 * sc, 14, 14, (1.0, 0.30, 0.25), 0.55)]


def _room(k, pam_behind=True, machine="rattle"):
    heads = {}
    if _PASS[0] == "mask":                                    # the mask pass: no room, only the people
        return heads

    def pam_b(k_):
        o = pm.pam(k_, MON[0] + 20, F - 72, L.SC["pam"], "stand", "neutral", look=(-1, 0.2), mug=False)
        heads["pam"] = o["head"]
    def office_dark(k_):                                     # the office lights are off at night: its glass goes dark
        x, y, w, h = ds.WIN
        k_.c.set_source_rgba(*bp.NIGHT_SHADOW, 0.62); k_.c.rectangle(x, y, w, h); k_.c.fill()
    ds.room(k, inside=False, behind=(office_dark, pam_b) if pam_behind else (office_dark,))
    rn.night_street(k)
    pss.blinds(k, "rehung")
    _counter_dark(k)
    dprops.coffee_machine(k, dprops.MACHINE[0], dprops.MACHINE[1], dprops.MACHINE[2], machine, t=0.0)
    x, feet, sc = pss.THRONE
    _shadow(k, x, feet, 70); _shadow(k, s4.CX0 + 150, F + 6, 170, 0.22)
    return heads


def n1(out=EP + "rv_night_cast_N1_v6.png"):
    """The master wide: the review is set up at night. Father at the tape beside the throne, Don facing him, Sofía and
    the robot on Don's side, Pam behind the counter in her monitor's light, the Client at the counter's end."""
    cam = (440, 545, 0.78)

    def draw(k):
        h = _room(k)
        _shadow(k, 210, F + 12, 26); o = rp.robot(k, 210, F + 10, L.SC["robot"], look=(1, 0))
        _shadow(k, 300, F + 26, 26); sd.sofia(k, 300, F + 24, L.SC["sofia"], "hold", "smile", look=(1, 0))
        _shadow(k, 690, F + 8, 34); cp.client(k, 690, F + 6, L.SC["client"], look=(-1, 0))
        _shadow(k, 590, F + 64, 30); dc.father(k, 590, F + 62, L.SC["father"], look=(-1, 0))
        _shadow(k, 372, F + 70, 34); dp.don(k, 372, F + 68, L.SC["don"], "stand", "neutral", look=(1, -0.2))
        return h
    rx, ry = 210, F - 120
    glows = [(MON[0], MON[1], 46, 34, bp.NIGHT_MONITOR, 0.45),     # lock: small, at the screen (the big pool lit the Client as a ghost)
             (MACH[0], MACH[1], 70, 50, bp.NIGHT_MONITOR, 0.32), (rx, ry, 40, 32, bp.NIGHT_MONITOR, 0.26)] + _machine_glow()
    lights = [(DOOR[0], DOOR[1], 260, 1.0), (MON[0], MON[1], 200, 0.9), (MACH[0], MACH[1], 180, 0.7),
              (rx, ry, 140, 0.5), (pss.THRONE[0], F - 200, 160, 0.4)]
    _frame(cam, draw, glows, lights, out, cast=LOCK_CAST)


def n2(out=EP + "rv_night_cast_N2_v6.png"):
    """S6, the counter at night: Pam in her monitor's light, the machine with its needle in the red, the Client at the
    counter's end, the first to look at it."""
    cam = (750, 660, 1.9)                                     # v2 (G3): the price tag and DON's door plate out

    def draw(k):
        h = _room(k)
        _shadow(k, 668, F + 30, 34); cp.client(k, 668, F + 28, L.SC["client"], look=(1, -0.4))
        return h
    glows = [(MON[0], MON[1], 42, 30, bp.NIGHT_MONITOR, 0.45), (MACH[0], MACH[1], 50, 40, bp.NIGHT_MONITOR, 0.30),
             (MACH[0] - 50, MACH[1] + 40, 40, 30, (1.0, 0.35, 0.30), 0.26)] + _machine_glow()   # v3: pools at sources only
    lights = [(MON[0], MON[1], 200, 1.0), (MACH[0], MACH[1], 180, 0.8)]
    _frame(cam, draw, glows, lights, out, cast=LOCK_CAST)


def n3(out=EP + "rv_night_cast_N3_v6.png"):
    """6.4's light: Don close, his face lit cold by the robot's screen (HUMAN APPROVAL REQUIRED) at the frame's edge."""
    cam = (560, 805, 1.7)                                     # v2: the dark office glass in frame, the portrait out

    def draw(k):
        _room(k, pam_behind=False)
        _shadow(k, 480, F + 40, 34); o = dp.don(k, 480, F + 38, L.SC["don"], "stand", "neutral", look=(1, 0))
        r = rp.robot(k, 620, F + 20, L.SC["robot"], look=(-1, 0))
        _screen_text(k, r, ["HUMAN", "APPROVAL", "REQUIRED"], 1.0)
        n3.don = o; n3.robot = r
    draw_k = kit.Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
    c0 = draw_k.c; c0.save(); sbv.view(c0, *cam); draw(draw_k); c0.restore()
    hx, hy = n3.don["head"][:2]; sx, sy = n3.robot["screen"][:2]
    glows = [(sx, sy, 50, 44, bp.NIGHT_MONITOR, 0.50)]          # v3: the pool only at its source (the halos read as "behind
                                                                 # him"); the light on Don is the cast band
    lights = [(sx, sy, 170, 1.0)]
    _frame(cam, draw, glows, lights, out, cast=LOCK_CAST)


if __name__ == "__main__":
    {"all": lambda: (n1(), n2(), n3()), "n1": n1, "n2": n2, "n3": n3}[sys.argv[1]]()
