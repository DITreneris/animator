"""OFFICE NOIR 3: the arena's back door, 4.1 and 4.2 (20 Nov). From behind him: a doorway in a black wall; through
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
    st.folder(k, 440, 800, 1.5, 1.42)                                                           # the folder, under his arm
    cut(k, [(396, 720), (446, 740), (452, 990), (400, 990)], TRACK, shadow=False, lw=3.4)
    c.restore()
    csh.noir(s)
    return s


def face(look=(0.2, -0.9), glove=0.0):
    """4.2: his face, the ring's lamp on it; the folder under his arm at the bottom of the frame."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s); k = Ctx(c, 0)
    g = cairo.RadialGradient(270, 60, 40, 270, 300, 900)
    g.add_color_stop_rgba(0, 0.74, 0.74, 0.76, 1); g.add_color_stop_rgba(1, 0.08, 0.08, 0.10, 1); c.set_source(g); c.paint()
    sc = 3.0 * b.REL
    pose = "b_walk" if glove < 0.5 else (-9, 6, 150, 22)
    b.boxer(k, 262, 500 - b.HY * sc + 30, sc, pose, "hard", look, outfit="street")
    c.save(); c.translate(120, 800); c.rotate(-0.16)                                            # the folder under his arm, her photograph out of the top of it
    rect(k, -84, -150, 150, 200, (0.98, 0.98, 0.96), 3, shadow=True, lw=3)
    c.save(); c.rectangle(-76, -142, 134, 150); c.clip(); c.set_source_rgb(0.62, 0.62, 0.64); c.paint()
    st.star(k, -6, -142 + 300, 1.15, "g_stand", "interested", (0.6, 0.0)); c.restore()
    cut(k, [(-120, -40), (110, -40), (110, 190), (-120, 190)], (0.86, 0.80, 0.62), shadow=True, lw=3.4)
    cut(k, [(30, -66), (104, -66), (110, -40), (30, -40)], (0.86, 0.80, 0.62), shadow=False, lw=3)
    c.restore()
    csh.noir(s)
    return s


def frames():
    return [behind(1.0), face((0.2, -0.9)), face((-0.7, 0.9)), face((0.2, -0.9), glove=1.0)]
