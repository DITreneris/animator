"""16:9 drawing audit for The Blueprint. Opt-in. Exits 1 on a miss.

A camera is (cx, cy, zoom). view() centres it on the 960x540 frame.
A head or a motion mark outside that visible world fails the shot.

Marks are read from bp_scenes, so the audit follows the drawing.
--plant puts back the coordinates and cameras of 25 Nov 2026, before the geometry pass.
It must fail with the same eight rows:
  shot 03 the shred sheet and Pam's finger below SHRED
  shot 05 SHRED does not hold Pam
  shot 11 COUNTER does not hold the Client, and the pocket is below the frame
  shot 13 the stamp page below S0

frame_fall stays inside S0. A change that fails shot 01 is a bad check.
This file does not draw, and it does not edit the set.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bp_frame as fr
import bp_set as room

W, H = fr.W, fr.H

# Feet minus this is the head point layouts() already uses for Sofía and Pam.
HEAD_DROP = {
    "client": 70,
    "robot": 70,
    "sofia": 70,
    "don": 80,
    "pam": 80,
    "mom": 80,
}

# Who the shot is about. Their heads must land inside the assigned camera.
REQUIRE = {
    "05": ("sofia", "pam"),
    "11": ("client", "pam"),
    "13": ("robot",),
}

# The room before the geometry pass. Only --plant uses these.
OLD_MARKS = {
    "01": ((440, 250), (440, 392)),
    "03": ((514, 705), (514, 741), (532, 724)),
    "11": ((140, 640), (756, 600)),
    "13": ((196, 748),),
}
OLD_CAMS = {"05": "SHRED", "11": "COUNTER"}

# Pam is outside SHRED. The shot does not draw her finger.
OPEN = ("03 finger: not drawn. Pam is outside SHRED, and a finger with no arm is a stray.",)


def live_marks(bp_scenes):
    return {
        "01": ((440, 250), (440, 392)),
        "03": (bp_scenes.SHEET_FROM, bp_scenes.SHEET_TO),
        "11": (bp_scenes.POCKET_FROM, bp_scenes.POCKET_TO),
        "13": (bp_scenes.STAMP_PAGE,
               (bp_scenes.STAMP_PAGE[0], bp_scenes.STAMP_PAGE[1] - bp_scenes.STAMP_DROP)),
    }


def span(cam):
    cx, cy, z = cam
    hw, hh = (W / 2.0) / z, (H / 2.0) / z
    return cx - hw, cy - hh, cx + hw, cy + hh


def inside(rect, x, y):
    x0, y0, x1, y1 = rect
    return x0 <= x <= x1 and y0 <= y <= y1


def homes():
    return {
        "client": room.CLIENT,
        "robot": room.ROBOT,
        "sofia": room.SOFIA,
        "don": room.DON,
        "pam": room.PAM,
        "mom": room.MOM,
    }


def head(name, place):
    x, feet, _scale = place
    return x, feet - HEAD_DROP[name]


def main(argv):
    import bp_scenes

    plant = "--plant" in argv
    marks = OLD_MARKS if plant else live_marks(bp_scenes)
    require = {k: v for k, v in REQUIRE.items() if not (plant and k == "13")}

    fails = []
    print("mode     %s" % ("plant (25 Nov coordinates)" if plant else "live"))
    print("camera   x0     x1     y0     y1")
    rects = {}
    for name, cam in bp_scenes.CAM.items():
        rects[name] = span(cam)
        x0, y0, x1, y1 = rects[name]
        print("%-8s %6.0f %6.0f %6.0f %6.0f" % (name, x0, x1, y0, y1))

    print("")
    if not plant:
        plate = ((300, 78), (400, 78), (300, 196), (400, 196))
        for i, (x, y) in enumerate(plate):
            if not inside(rects["ZERO"], x, y):
                fails.append("ZERO poster corner %d (%.0f, %.0f) outside the plate camera" % (i, x, y))
        page = bp_scenes.STAMP_PAGE
        for i, (x, y) in enumerate(((page[0] - 26, page[1] - 33), (page[0] + 26, page[1] - 33),
                                    (page[0] - 26, page[1] + 33), (page[0] + 26, page[1] + 33))):
            if not inside(rects["STAMP"], x, y):
                fails.append("STAMP page corner %d (%.0f, %.0f) outside the stamp camera" % (i, x, y))
        hx, hy = head("robot", homes()["robot"])
        if not inside(rects["STAMP"], hx, hy):
            fails.append("STAMP robot head (%.0f, %.0f) outside the stamp camera" % (hx, hy))
        for i, (x, y) in enumerate(((698, 318), (718, 318), (698, 336), (718, 336))):
            if not inside(rects["PLAN"], x, y):
                fails.append("PLAN strip corner %d (%.0f, %.0f) outside the plan camera" % (i, x, y))

    for shot in bp_scenes.SHOTS:
        cam_name = OLD_CAMS.get(shot["id"], shot["cam"]) if plant else shot["cam"]
        rect = rects.get(cam_name)
        if rect is None:
            fails.append("%s camera %s is not in CAM" % (shot["id"], cam_name))
            continue
        for who in require.get(shot["id"], ()):
            x, y = head(who, homes()[who])
            if not inside(rect, x, y):
                fails.append(
                    "%s %s %s head (%.0f, %.0f) outside x %.0f..%.0f y %.0f..%.0f"
                    % (shot["id"], cam_name, who, x, y, rect[0], rect[2], rect[1], rect[3])
                )
        for i, (x, y) in enumerate(marks.get(shot["id"], ())):
            if not inside(rect, x, y):
                fails.append(
                    "%s %s mark %d (%.0f, %.0f) outside x %.0f..%.0f y %.0f..%.0f"
                    % (shot["id"], cam_name, i, x, y, rect[0], rect[2], rect[1], rect[3])
                )

    print("fails %d" % len(fails))
    for row in fails:
        print("FAIL " + row)
    if not plant:
        for row in OPEN:
            print("OPEN " + row)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
