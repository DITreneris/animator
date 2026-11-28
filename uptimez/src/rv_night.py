"""Approved. (episode 16): the canon night grade on the 9:16 front desk, opt-in (stage 3, Tomas /grill-me 28 Nov:
"Night grade test still" first; the throne keeps a warm rim only).

The canon night is The Blueprint's (bp_frame._night, the still bp_still_night.png, approved 25 Nov): the wall and the
floor go flat night blue-grey, every shape keeps its day colours (restored from the day frame), the screens are the
light (NIGHT_MONITOR pools), a warm pool where a lamp would be. The palette is bp_frame's, imported, never copied.
Here the same rule is applied to the 9:16 front desk v4 (fs_set4 / ps_set) after the frame is drawn:
  - wall and floor pixels (the stage's flat WALL and floor colours, matched with a soft tolerance so edges blend)
    become NIGHT_WALL / NIGHT_FLOOR;
  - the glass door goes dark (the street at night);
  - glow pools: Pam's monitor, the coffee machine's front (its panel), the robot's face;
  - the gold throne keeps a thin warm rim (NIGHT_WARM) on its upper-left edges so it reads at 270 px.
Nothing in fs_set4, ps_set, dh_props or bp_frame changes; a frame that does not call grade() draws as before.
  python3 rv_night.py still   -> ../the-review/rv_night_test_v2.png (+ _270.png, the feed size); v1 kept
"""
import os
import sys
import math
import numpy as np
import cairo
import kit
import fs_set4 as s4
import ps_set
import dh_props as dp
import fs_storyboard_v17 as sb
import bp_frame as bp

EP = "../the-review/"
NIGHT_WALL = (0x59 / 255.0, 0x67 / 255.0, 0x80 / 255.0)     # bp_frame._night's wall
NIGHT_FLOOR = (0x3E / 255.0, 0x4B / 255.0, 0x63 / 255.0)    # bp_frame._night's floor
DAY_FLOOR = (0.72, 0.63, 0.50)                              # stage_ob.stage's floor
S1W = (505, 575, 0.86)
S1M = (300, 575, 0.86)                                      # v3: the master (A+B), the door in frame                                      # the episode's S1 wide: throne (B) to the machine (C)


def _arr(s):
    s.flush()
    h, w = s.get_height(), s.get_width()
    return np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())[:, :w, :]


def _rgb(a):
    return a[:, :, 2::-1].astype(np.float64) / 255.0          # cairo ARGB32 is BGRA in memory


def _near(rgb, col, tol=0.10):
    d = np.sqrt(((rgb - np.array(col)) ** 2).sum(axis=2))
    return np.clip(1.0 - d / tol, 0.0, 1.0)


def _pool(c, x, y, rx, ry, col, a):
    bp._pool(c, x, y, rx, ry, ((0.0, col + (a,)), (1.0, col + (0.0,))))


BARS = [False]      # v2 (off in v3: read as rain / a glitch, 3 of 4) (cold check v1, 2 of 2 could not tell the time: "no window, no dark sky, no lamp")
VIGNETTE = [True]


def _bars(c, y0, h, slope, pitch, y_shift, n, gain):
    """Pale diagonal bands of street light on one plane (bp_frame._night_bars' widths and alphas, a touch stronger at
    9:16 feed size); clipped to the plane so a band never crosses wall and floor."""
    c.save(); c.rectangle(0, y0, 540, h); c.clip()
    for i in range(n):
        y = y_shift + i * pitch
        for thick, al in ((16, 0.070 * gain), (8, 0.110 * gain)):
            c.set_source_rgba(0.80, 0.86, 1.0, al)
            c.move_to(-20, y); c.line_to(560, y + 580 * slope); c.line_to(560, y + 580 * slope + thick)
            c.line_to(-20, y + thick); c.close_path(); c.fill()
    c.restore()


def night_street(k, seed=4310):
    """v3 (Tomas 28 Nov, after two cold rounds, 0 of 4 sure it was night: "Night in the glass door"). The shut glass
    door shows the street at night: a navy sky, the building across the road with one lit window, a streetlamp with a
    warm pool, the glass tint and its highlights over it. Drawn after ps_set.room, before the blinds go back on top."""
    import set_ob as st
    c = k.c
    x, y, w, h = st.DOOR
    c.save(); c.rectangle(x, y, w, h); c.clip()
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, 0.07, 0.09, 0.18); g.add_color_stop_rgb(1, 0.14, 0.17, 0.28)
    c.set_source(g); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.98, 0.96, 0.84); c.arc(x + w * 0.70, y + h * 0.15, 15, 0, 2 * math.pi); c.fill()    # the moon (v3: 15, cold round 3 "a tiny dot at 270")
    c.set_source_rgb(0.05, 0.06, 0.11)                                                                   # across the road
    c.rectangle(x - 4, y + h * 0.40, w * 0.62, h * 0.60); c.fill()
    c.rectangle(x + w * 0.56, y + h * 0.52, w * 0.50, h * 0.48); c.fill()
    c.set_source_rgb(*bp.NIGHT_WARM); c.rectangle(x + w * 0.20, y + h * 0.50, 16, 20); c.fill()        # one lit window
    lx = x + w * 0.84                                                                                    # the streetlamp
    c.set_source_rgb(0.03, 0.03, 0.06); c.set_line_width(4); c.move_to(lx, y + h); c.line_to(lx, y + h * 0.30); c.stroke()
    c.rectangle(lx - 12, y + h * 0.28, 16, 6); c.fill()
    _pool(c, lx - 4, y + h * 0.33, 46, 60, bp.NIGHT_WARM, 0.55)
    _pool(c, lx - 4, y + h * 0.96, 52, 14, bp.NIGHT_WARM, 0.40)
    c.set_source_rgba(0.55, 0.65, 0.80, 0.16); c.rectangle(x, y, w, h); c.fill()                          # the glass
    c.set_source_rgba(1, 1, 1, GLASS_HI[0]); c.set_line_width(7)
    for dx in (26, 44):
        c.move_to(x + dx, y + h - 20); c.line_to(x + dx + 54, y + 20); c.stroke()
    c.restore()
    c.set_source_rgb(*kit.INK); c.set_line_width(2.2); c.rectangle(x, y, w, h); c.stroke()


def _shape_alpha(cam, draw, day=None):
    """One shape alone on a transparent frame, for its rim. day (v4, opt-in): the finished day frame's rgb; then only
    the part of the shape still seen in it counts (v4's first stills: the rim was drawn over Don standing in front of
    the throne)."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.save(); sb.view(c, *cam); draw(k); c.restore()
    a = _arr(s)
    al = a[:, :, 3].astype(np.float64) / 255.0
    if day is None:
        return al
    rgb = _rgb(a) / np.maximum(al, 1e-6)[..., None]          # un-premultiply
    seen = np.sqrt(((rgb - day) ** 2).sum(axis=2)) < 0.06
    return al, seen


FALLOFF = [0.0]      # v4 (outside review 28 Nov, "flat": no fall-off): how dark the night wall and floor get away from
                     # their light sources, 0 = as v3 (the default, so v1-v3 rebuild); never applied to people or props
CAST_LIGHT = [None]  # v5 (Tomas 28 Nov, "Light the people", episode 16 only, opt-in): None = the canon (people and props in
                     # day colours, as v1-v4); or dict(shade=0..0.35, key=(dx, dy) toward the key light, rim=colour,
                     # rim_a=0..1): everything that is not wall or floor goes cooler and darker away from the lights,
                     # and keeps a thin rim of the key light's colour on its edges that face it
COOL = (0.62, 0.70, 0.88)
FLOOR_END = [True]   # the stage's last floor row filled flat (the empty-set stills); v4 frames with ds._floor_on: off
RIM_SEEN = [False]   # v4: the warm rim only where the throne is still seen (people in front of it keep theirs)
GLASS_HI = [0.22]    # v4: the door glass highlights (0.22 as v3; the review: "too bright and mechanical")


def _falloff(cam, lights, shape):
    """1 at a light source, falling to 1 - FALLOFF far from every one. lights: [(world x, world y, world radius, k)]."""
    fx, fy, z = cam
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    L = np.zeros((h, w))
    for x, y, r, kk in lights:
        sx, sy = 270 + (x - fx) * z, 480 + (y - fy) * z
        L = L + kk * np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * (r * z) ** 2)))
    return 1.0 - FALLOFF[0] * (1.0 - np.clip(L, 0, 1))


def moon_patch(c, cam, door=(22, 392, 150, 408), floor=800, length=260, col=(0.60, 0.72, 0.90), alpha=0.16):
    """v4: the street light through the shut glass door lands on the floor as one soft cold patch, in front of the door
    (motivated by the door: v2's free-floating bands read as rain and were removed)."""
    x, y, w, h = door
    c.save(); sb.view(c, *cam)
    c.rectangle(-2000, floor, 5000, 3000); c.clip()
    g = cairo.LinearGradient(0, floor, 0, floor + length)
    g.add_color_stop_rgba(0, *col, alpha); g.add_color_stop_rgba(1, *col, 0.0)
    c.set_source(g)
    c.move_to(x, floor); c.line_to(x + w, floor); c.line_to(x + w + 140, floor + length); c.line_to(x + 60, floor + length)
    c.close_path(); c.fill()
    c.restore()


def grade(s, cam, floor_y, glows=(), rim=None, lights=(), after=None, people=None):
    """The night grade on a finished 540x960 day frame (in place). floor_y: the floor line's y in this frame.
    glows: [(world x, world y, rx, ry, colour, alpha)]; rim: a draw(k) whose shape keeps a warm rim."""
    a = _arr(s)
    rgb = _rgb(a)
    rim_al = _shape_alpha(cam, rim, rgb) if (rim is not None and RIM_SEEN[0]) else None
    wall = _near(rgb, kit.WALL)
    yy = np.arange(rgb.shape[0])[:, None]
    floor = np.maximum(_near(rgb, DAY_FLOOR), wall * (yy >= floor_y + 2))   # below the stage's floor the paint is WALL
    wall = wall * (yy < floor_y)
    floor = floor * (yy >= floor_y - 1)
    out = rgb.copy()
    for m, col in ((wall, NIGHT_WALL), (floor, NIGHT_FLOOR)):
        out = out * (1 - m[..., None]) + np.array(col) * m[..., None]
    if FALLOFF[0] > 0 and lights:                            # v4: only the background (wall and floor) falls off
        bgm = np.clip(wall + floor, 0, 1)[..., None]
        f = _falloff(cam, lights, bgm.shape[:2])[..., None]
        out = out * (1 - bgm) + out * f * bgm
    if CAST_LIGHT[0] and lights:                             # v5: the people and props lit by the same sources
        cl = CAST_LIGHT[0]
        fg = np.clip(1 - wall - floor, 0, 1)
        keep = FALLOFF[0]; FALLOFF[0] = 1.0
        Lmap = 1 - _falloff(cam, [(x, y, r * 1.4, kk) for x, y, r, kk in lights], fg.shape)   # 0 at a light .. 1 far
        FALLOFF[0] = keep
        sh = (cl["shade"] * Lmap * fg)[..., None]
        out = out * (1 - sh) + out * np.array(COOL) * (1 - 0.35) * sh / (1 - 0.35) * 0.80 + 0 * sh
        dx, dy = cl["key"]                                   # the rim: fg edges whose neighbour toward the key is not fg

        def shifted(a, sx, sy):
            n = np.zeros_like(a)
            ys, xs = slice(max(0, -sy), a.shape[0] - max(0, sy)), slice(max(0, -sx), a.shape[1] - max(0, sx))
            yd, xd = slice(max(0, sy), a.shape[0] - max(0, -sy)), slice(max(0, sx), a.shape[1] - max(0, -sx))
            n[ys, xs] = a[yd, xd]
            return n
        if people is not None:                               # v5c: the rim and the band on the people only (v5b lit the
            fg = people * fg                                 # tape's and the DON mark's edges too)
        rim = np.clip(fg - shifted(fg, dx, dy), 0, 1) * cl.get("rim_a", 0.7)
        band = cl.get("band", 0)                             # v5b (Tomas: "one stronger pass"): a soft lit band, not
        if band:                                             # only a line: the light lands on the side that faces it
            acc = np.zeros_like(fg)
            for i in range(1, band + 1):
                acc = np.maximum(acc, np.clip(fg - shifted(fg, dx * i, dy * i), 0, 1) * (1 - (i - 1) / float(band)))
            near = (1 - Lmap) if cl.get("near", True) else 1.0           # stronger close to a source
            lit = (acc * cl.get("band_a", 0.45) * (0.35 + 0.65 * near))[..., None]
            col = np.array(cl["rim"])
            out = 1 - (1 - out) * (1 - col * lit)                # screen: it brightens, never darkens
        out = out * (1 - rim[..., None]) + np.array(cl["rim"]) * rim[..., None]
    end = int(round(480 + (s4.F + 160 - cam[1]) * cam[2]))   # below the stage's last floor row: plain night floor
    if FLOOR_END[0] and 0 < end < rgb.shape[0]:
        out[end - 2:] = np.array(NIGHT_FLOOR)
    a[:, :, 2] = (out[:, :, 0] * 255).round().astype(np.uint8)
    a[:, :, 1] = (out[:, :, 1] * 255).round().astype(np.uint8)
    a[:, :, 0] = (out[:, :, 2] * 255).round().astype(np.uint8)
    s.mark_dirty()
    c = cairo.Context(s)
    if BARS[0]:                                              # v2: the canon's street light through the blinds, two planes
        _bars(c, 0, floor_y, -0.36, 64, 40, 5, 1.0)          # (bp_frame._night_bars: the wall keeps the window's slope,
        _bars(c, floor_y, 960 - floor_y, -0.10, 92, floor_y + 30, 4, 0.8)   # the floor a flatter one; no bar crosses both)
    if VIGNETTE[0]:                                          # v2: the frame's edges fall off into the dark
        g = cairo.RadialGradient(270, 470, 260, 270, 470, 640)
        g.add_color_stop_rgba(0, *bp.NIGHT_SHADOW, 0.0); g.add_color_stop_rgba(1, *bp.NIGHT_SHADOW, 0.62)
        c.set_source(g); c.paint()
    c.save(); sb.view(c, *cam)
    c.restore()
    if after is not None:                                    # v4: the light that lands (the moon patch) before the glows
        after(c)
    c.save(); sb.view(c, *cam)
    c.set_operator(cairo.OPERATOR_SCREEN)
    for x, y, rx, ry, col, al in glows:
        _pool(c, x, y, rx, ry, col, al)
    c.set_operator(cairo.OPERATOR_OVER)
    c.restore()
    if rim is not None:
        al, seen = rim_al if rim_al is not None else (_shape_alpha(cam, rim), 1.0)
        sh = np.zeros_like(al); sh[3:, 3:] = al[:-3, :-3]
        edge = np.clip(al - sh, 0, 1) * 0.85 * seen             # the shape's own edge, kept only where it is seen
        r = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); ra = _arr(r)
        w = bp.NIGHT_WARM
        for i, v in ((2, w[0]), (1, w[1]), (0, w[2])):
            ra[:, :, i] = (edge * v * 255).round().astype(np.uint8)  # premultiplied
        ra[:, :, 3] = (edge * 255).round().astype(np.uint8)
        r.mark_dirty()
        c.set_source_surface(r, 0, 0); c.paint()
    return s


def test_frame(cam=S1M):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    c.save(); sb.view(c, *cam)
    ps_set.room(k, blind="up", tape=True, phone=None)
    night_street(k)
    ps_set.blinds(k, "up")
    dp.coffee_machine(k, dp.MACHINE[0], dp.MACHINE[1], dp.MACHINE[2], "rattle", t=0.0)   # v2: no steam in an empty room
    c.restore()
    fx, fy, z = cam
    floor_y = 480 + (s4.F - fy) * z
    x, feet, sc = ps_set.THRONE
    glows = [(s4.HOME["pam"][0] - 10, s4.F - 210, 110, 80, bp.NIGHT_MONITOR, 0.55),   # Pam's monitor
             (dp.MACHINE[0], dp.MACHINE[1] - 70, 90, 70, bp.NIGHT_MONITOR, 0.40),  # the machine's panel
             (x, feet - 260 * sc, 130, 150, bp.NIGHT_WARM, 0.10)]                  # a faint warm halo on the throne
    return grade(s, cam, floor_y, glows, rim=lambda k_: ps_set.throne(k_))


def still(out=EP + "rv_night_test_v3.png"):
    s = test_frame()
    s.write_to_png(out)
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, 270, 480)
    c = cairo.Context(small); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    small.write_to_png(out.replace(".png", "_270.png"))
    print("wrote", out)


if __name__ == "__main__":
    {"still": still}[sys.argv[1]]()
