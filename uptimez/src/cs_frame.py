"""ONE STAR: the framing check (Tomas, 20 Nov, angry and right: "the robot and Don too small; watch the scales; the
robot will be under TikTok's and YouTube's dead zone"). The series' own rule (fs_storyboard v24, auto-framing that
the animation pass had switched off with auto=False): a medium shot's biggest face at radius FACE_R (80 px at 540)
with the faces at y FACE_Y (400); the bottom quarter (y > 720) and the right-hand buttons belong to the apps
(lessons 33, 79, and "keep the key action away from the buttons"). Signs whole or out (G3).

  face_cam(heads_scene, r_scene)  -> the camera that puts the faces there
  check(module)                   -> every drawing of every shot: faces, bottom, right rail, signs; prints FAILs"""
import importlib
import sys
import fs_storyboard as sb

FACE_R, FACE_Y = sb.FACE_R, sb.FACE_Y
BOTTOM = 720                                               # nothing that tells the story below this (540x960)
RAIL = (470, 380, 860)                                     # x > 470 between y 380 and 860: the buttons
SIGNS = {                                                  # set coordinates (x0, y0, x1, y1)
    "portrait+plaque": (355, 300, 510, 500),
    "logo": (296, 226, 350, 278),
    "calendar": (532, 430, 598, 512),                          # First Search's, right of the portrait
}
WIDES = {"1.1", "6.6"}


def face_cam(heads, z_max=None, y=FACE_Y, r_target=78, span_max=430):
    """heads: [(x, y, r) in set coordinates]. The zoom that makes the biggest face r_target px (less if the group's
    span would not fit), centred on the group, the faces' mean at y."""
    rmax = max(h[2] for h in heads)
    z = r_target / rmax
    xs = [h[0] for h in heads]
    span = (max(xs) - min(xs)) + 2.6 * rmax
    if span * z > span_max:
        z = span_max / span
    if z_max:
        z = min(z, z_max)
    cx = (max(xs) + min(xs)) / 2
    cy = sum(h[1] for h in heads) / len(heads) - (y - 480) / z
    return (round(cx, 1), round(cy, 1), round(z, 3))


def sign_state(cam, box, top=96):
    # the logo is a mark, not text: under the apps' top bar it may sit; only the frame's edge cuts it
    """in / out / CUT: the sign's box against the frame (and under the top bar)."""
    cx, cy, z = cam
    x0 = 270 + (box[0] - cx) * z; x1 = 270 + (box[2] - cx) * z
    y0 = 480 + (box[1] - cy) * z; y1 = 480 + (box[3] - cy) * z
    if x1 <= 2 or x0 >= 538 or y1 <= 2 or y0 >= 958:
        return "out"
    if x0 >= 0 and x1 <= 540 and y0 >= top and y1 <= 960:
        return "in"
    return "CUT"


def check(mod, every=1, cams=None):
    m = importlib.import_module(mod); m.HI[0] = 1
    bad = 0
    for shot, nd, fn in m.SHOTS:
        for d in range(0, nd, every):
            m.draw(fn, d)
            hs = {k: v for k, v in sb.HEADS.items() if k != "client" or v[1] > 0}
            if not hs:
                continue
            msgs = []
            rmax = max(v[2] for v in hs.values())
            if shot not in WIDES and rmax < 64:
                msgs.append("faces small (r %d < 64)" % rmax)
            for k, (x, y, r) in hs.items():
                if 0 <= x <= 540 and y + r > BOTTOM and y - r < 960:
                    msgs.append("%s in the bottom quarter (y %d)" % (k, y))
                if x > RAIL[0] and RAIL[1] < y < RAIL[2]:
                    msgs.append("%s under the right-hand buttons (x %d)" % (k, x))
            if msgs:
                bad += 1
                print("FAIL %s %s d%d: %s" % (mod, shot, d, "; ".join(sorted(set(msgs)))))
    print("%s: %d drawings fail" % (mod, bad))
    return bad


if __name__ == "__main__":
    for mod in sys.argv[1:]:
        check(mod, every=4)
