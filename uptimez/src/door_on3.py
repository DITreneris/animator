"""OFFICE NOIR 3: the arena's back door, 4.1 and 4.2 (20 Nov). v2 (v1 is door_on3_v1.py): in 4.2 the look is an action:
one glove pushes the folder down out of the frame as his eyes go up to the roll. react(): 4.4c, his face over the card.
v1: From behind him: a doorway in a black wall; through
it, small and far, the ring under its lamp, his plan hung over it, the robot under the plan. Then his face: up at
the roll, down at the folder, up again. The ring in the doorway is the ring set itself (ring_on3), drawn small.
frames() -> 4.1, 4.2 (up), 4.2 (down), 4.2 (up, the glove half raised)."""
import cairo
import kit
import client_on3 as b
import client_sheet_on3 as csh
import ring_on3 as rg
import robot_on3 as r
import street_on3 as st
from kit import Ctx, cut, rect, INK

TRACK = (0.20, 0.20, 0.23)
DOOR = (118, 150, 304, 560)                                 # the opening: x, y, w, h


def _robot(k):
    x, y, s = rg.HOME["robot"]
    rg.shadow(k, 352, y, 40); r.robot(k, 352, y, s, "r_wait", "furious", side=-1)


RIM = [False]


def behind(tip=1.0, door_light=True):
    """4.1. tip 0..1: his head goes back."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(0.05, 0.05, 0.06); c.paint()
    x, y, w, h = DOOR
    ring = rg.frame((332, 1090, 1.0), [_robot], [], noir=False, hats=False, folder=False)
    c.save(); c.rectangle(x, y, w, h); c.clip()
    z = 1.04
    c.translate(x + w / 2 - 270 * z, y - 330 * z); c.scale(z, z); c.set_source_surface(ring, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(0.02, 0.02, 0.03); c.set_line_width(14); c.rectangle(x - 7, y - 7, w + 14, h + 14); c.stroke()   # the frame
    rect(k, x - 30, y - 62, 150, 40, (0.86, 0.86, 0.82), 3, shadow=False, lw=3)                 # a plate over the door
    kit.text(k, "FIGHTERS", x + 45, y - 34, 24, INK, bold=True)
    c.set_source_rgba(1, 1, 1, 0.16); c.new_path()                                              # the ring's light, out across the ground
    c.move_to(x, y + h + 7); c.line_to(x + w, y + h + 7); c.line_to(x + w + 150, 960); c.line_to(x - 150, 960); c.close_path(); c.fill()
    dy = 14 * tip
    c.save(); c.translate(-96, 96)
    cut(k, [(120, 990), (128, 690), (176, 560 + dy), (270, 506 + dy * 2), (364, 560 + dy), (412, 690), (420, 990)], TRACK, shadow=False, lw=4)   # his back, hood up
    c.set_source_rgb(0.12, 0.12, 0.14); c.set_line_width(4); c.set_line_cap(1)
    c.move_to(196, 640 + dy); c.curve_to(236, 566 + dy * 2, 304, 566 + dy * 2, 344, 640 + dy); c.stroke()
    c.move_to(270, 690); c.line_to(270, 960); c.stroke(); c.set_line_cap(0)
    if RIM[0]:                                              # v5, opt-in: the ring's light on the edge of his hood and shoulders (he was dark on dark)
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(6); c.set_line_cap(1); c.set_line_join(1)
        c.new_path(); c.move_to(128, 700); c.line_to(176, 560 + dy); c.line_to(270, 506 + dy * 2); c.line_to(364, 560 + dy); c.line_to(412, 700); c.stroke(); c.set_line_cap(0)
    st.folder(k, 440, 800, 1.5, 1.42)                                                           # the folder, under his arm
    cut(k, [(396, 720), (446, 740), (452, 990), (400, 990)], TRACK, shadow=False, lw=3.4)
    c.restore()
    csh.noir(s)
    return s


def face(look=(0.2, -0.9), glove=0.0, push=0.0, expr="hard", folder=True, pocket=None):
    """4.2: his face, the ring's lamp on it; the folder under his arm at the bottom of the frame."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    g = cairo.RadialGradient(270, 60, 40, 270, 300, 900)
    g.add_color_stop_rgba(0, 0.74, 0.74, 0.76, 1); g.add_color_stop_rgba(1, 0.08, 0.08, 0.10, 1); c.set_source(g); c.paint()
    sc = 3.0 * b.REL
    pose = "b_walk" if glove < 0.5 else (-9, 6, 150, 22)
    b.boxer(k, 262, 500 - b.HY * sc + 30, sc, pose, expr, look, outfit="street")
    if not folder:
        csh.noir(s)
        return s
    if pocket is not None:                                   # v4 (Tomas, /grill-me): one glove shoves the folder into the hoodie's front pocket; her photograph's corner stays out
        u = pocket
        fx, fy, fa, fs = 120 + 150 * u, 800 - 60 * u + 150 * u * u, -0.16 + 0.26 * u, 1.0 - 0.22 * u
        c.save(); c.translate(fx, fy); c.rotate(fa); c.scale(fs, fs)
        rect(k, -84, -150, 150, 200, (0.98, 0.98, 0.96), 3, shadow=True, lw=3)
        c.save(); c.rectangle(-76, -142, 134, 150); c.clip(); c.set_source_rgb(0.62, 0.62, 0.64); c.paint()
        st.her(k, -6, -142 + 300, 1.15, (0.6, 0.0)); c.restore()
        cut(k, [(-120, -40), (110, -40), (110, 190), (-120, 190)], (0.86, 0.80, 0.62), shadow=True, lw=3.4)
        cut(k, [(30, -66), (104, -66), (110, -40), (30, -40)], (0.86, 0.80, 0.62), shadow=False, lw=3)
        c.restore()
        if u > 0.55:                                         # the pocket's lip, over it
            cut(k, [(96, 838), (440, 838), (470, 990), (70, 990)], TRACK, shadow=False, lw=4)
            c.set_source_rgb(0.12, 0.12, 0.14); c.set_line_width(4); c.move_to(100, 846); c.line_to(436, 846); c.stroke()
        gx, gy = fx + 150 * fs, fy + 70 * fs                 # his glove on the folder's far edge, pushing it in
        c.save(); c.translate(gx, gy); c.scale(3.0, 3.0); c.translate(-gx, -gy)
        b._glove(k, gx, gy, -0.7, 0.7, 1, 73)
        c.restore()
        csh.noir(s)
        return s
    c.save(); c.translate(120 - 30 * push, 800 + 250 * push); c.rotate(-0.16 - 0.5 * push)                                            # the folder under his arm, her photograph out of the top of it
    rect(k, -84, -150, 150, 200, (0.98, 0.98, 0.96), 3, shadow=True, lw=3)
    c.save(); c.rectangle(-76, -142, 134, 150); c.clip(); c.set_source_rgb(0.62, 0.62, 0.64); c.paint()
    st.her(k, -6, -142 + 300, 1.15, (0.6, 0.0)); c.restore()
    cut(k, [(-120, -40), (110, -40), (110, 190), (-120, 190)], (0.86, 0.80, 0.62), shadow=True, lw=3.4)
    cut(k, [(30, -66), (104, -66), (110, -40), (30, -40)], (0.86, 0.80, 0.62), shadow=False, lw=3)
    c.restore()
    if push > 0:                                             # his glove, flat on top of it, shoving it down; marks where it was
        gx, gy = 150 - 10 * push, 640 + 250 * push
        c.set_source_rgb(0.92, 0.92, 0.92); c.set_line_width(6); c.set_line_cap(1)
        for dx in (-70, -20, 34):
            c.move_to(120 + dx, 640); c.line_to(120 + dx - 6, 740); c.stroke()
        c.set_line_cap(0)
        cut(k, [(gx + 150, gy - 190), (gx + 40, gy - 30), (gx + 96, gy + 20), (gx + 230, gy - 150)], TRACK, shadow=False, lw=4)
        c.save(); c.translate(gx, gy); c.scale(3.0, 3.0); c.translate(-gx, -gy)
        b._glove(k, gx, gy, -0.5, 0.86, -1, 73)
        c.restore()
    csh.noir(s)
    return s


def react(up=False):
    """4.4c: his face over her desk. He looks down at the card (suspicious: one long squint); then up, as before."""
    return face((0.2, -0.2) if up else (-0.3, 0.95), expr="hard" if up else "suspicious", folder=False)


def frames():
    return [behind(1.0), face((0.2, -0.9)), face((-0.7, 0.9)), face((0.2, -0.9), glove=1.0, push=0.45)]
