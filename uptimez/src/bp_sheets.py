"""Blueprint 16:9 character sheets. One figure each, on one ruler.

Don is drawn with legs="cuffs". The other sheets turn on one opt-in each.
Pam and Sofia get a nose, Sofia a heel that reads, Mom a joined elbow,
the Client an elbow disc plus a quieter head beside the room face.
Off, every film draws as before. The room is not painted here.
Scales are the locked homes. The tick marked DON is his height at 0.60.
This file does not paint the room and does not move a home.
"""
import os

import cairo

import bp_set as room
import don_v4 as dv
import fs_set as fs
import fs_storyboard as sb
import kit
import mom_fs as mfs
import sofia_fs as sfs
from kit import Ctx, INK

EP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "the-blueprint", "sheets"))
W, H = 960, 1100
GAIN = 2.0
FEET_Y = 980
INK_SOFT = (0.35, 0.32, 0.28)
# kit person height is 300 * h. Don's h is 1.12. The tick uses the locked scale 0.60.
DON_H = 300 * kit.PEOPLE["DON"]["h"] * room.DON[2] * GAIN


def _label(c, text, x, y, size, bold=False):
    c.set_source_rgb(*(INK if bold else INK_SOFT))
    c.select_font_face("Inter", 0, 1 if bold else 0)
    c.set_font_size(size)
    c.move_to(x, y)
    c.show_text(text)


def _ruler(c):
    c.set_source_rgb(0.55, 0.48, 0.40)
    c.set_line_width(1.2)
    c.move_to(70, FEET_Y)
    c.line_to(70, FEET_Y - DON_H)
    c.stroke()
    c.move_to(62, FEET_Y)
    c.line_to(78, FEET_Y)
    c.stroke()
    c.move_to(62, FEET_Y - DON_H)
    c.line_to(86, FEET_Y - DON_H)
    c.stroke()
    _label(c, "DON  0.60", 92, FEET_Y - DON_H + 4, 14, bold=True)
    c.set_source_rgb(0.45, 0.38, 0.30)
    c.set_line_width(2)
    c.move_to(160, FEET_Y)
    c.line_to(800, FEET_Y)
    c.stroke()


def _sheet(name, scale, note, draw):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2)
    surf.set_device_scale(2, 2)
    c = cairo.Context(surf)
    c.set_source_rgb(0.93, 0.89, 0.82)
    c.paint()
    _label(c, "UPTIMEZ  ·  16:9  ·  " + name, 48, 54, 22, bold=True)
    _label(c, "scale %0.2f    %s" % (scale, note), 48, 82, 16)
    _ruler(c)
    k = Ctx(c, 0)
    draw(k, 480, FEET_Y, scale * GAIN)
    return surf


def _don(k, x, feet, s):
    kit.ARM_POSES["_fs"] = (-8, 0, 8, 0)
    try:
        import acts_ob as ac
        with ac.arms():
            o = dv.don(k, x, feet, s, "_fs", "neutral", look=(-1, 0), seed=500, legs="cuffs")
    finally:
        kit.ARM_POSES.pop("_fs", None)
    sb.don_signs(k, o["head"], s, "up", "up")


def _client(k, x, feet, s):
    import client_ob as co
    co.ELBOW[0] = True
    try:
        sb.client(k, x - 70, feet, s, "stand", "confident", (0.9, 0))
        co.QUIET[0] = True
        co.client(k, x + 270, feet, s * 0.62, "stand", "confident", (0.9, 0))
    finally:
        co.ELBOW[0] = False
        co.QUIET[0] = False
    _label(k.c, "QUIET", x + 220, feet - 400, 16, bold=True)


def _robot(k, x, feet, s):
    fs.robot_finger(k, x, feet, s)


def _sofia(k, x, feet, s):
    sfs.NOSE[0] = True
    sfs.HEEL[0] = True
    try:
        sfs.sofia(k, x, feet, s, "hold", "charm", look=(0.6, -0.2))
    finally:
        sfs.NOSE[0] = False
        sfs.HEEL[0] = False


def _pam(k, x, feet, s):
    import pam_mf as pm
    pm.NOSE[0] = True
    try:
        sb.pam_taping(k, x, feet, s)
    finally:
        pm.NOSE[0] = False


def _mom(k, x, feet, s):
    import acts_ob as ac
    with ac.arms():
        mfs.mom(k, x, feet, s, "fists", "unimpressed", look=(-0.9, 0.3), chin=True)


CAST = (
    ("don", room.DON[2], "two cuffs, two shoes. The room still uses the old block.", _don),
    ("client", room.CLIENT[2], "elbow disc. QUIET keeps the broken nose and drops the forehead lines.", _client),
    ("robot", room.ROBOT[2], "the room drawing, remote up", _robot),
    ("sofia", room.SOFIA[2], "a small J, a heel and a sole. The room face is unchanged.", _sofia),
    ("pam", room.PAM[2], "a small nose under the glasses. The room face is unchanged.", _pam),
    ("mom", room.MOM[2], "one sleeve through the elbow. The room still uses two segments.", _mom),
)


def main(directory=None):
    directory = directory or EP
    os.makedirs(directory, exist_ok=True)
    paths = []
    for name, scale, note, draw in CAST:
        path = os.path.join(directory, "bp_sheet_%s.png" % name)
        _sheet(name.upper(), scale, note, draw).write_to_png(path)
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in main():
        print(p)
