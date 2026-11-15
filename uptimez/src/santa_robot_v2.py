"""v2 (santa_robot_v1.py = v1, kept), after review: a big HR badge that reads in the wide shot; red lines
radiating from the pompom when alarmed; a "smug" screen face for "Violation resolved."; a "detect" pose
(the rigid point from the last episode, tipped slightly toward the target).

v1 notes: The robot, Christmas special ("Happy Compliance"): the waiter robot from "I Will Replace You", promoted.
Same body, wheel, screen faces and bow tie (waiter_kit.py, untouched); the costume is drawn on top:
- a Santa hat over the screen; the antenna light now sits in the pompom (yellow, or red when alarmed),
- a cotton beard hooked under the screen, stopping above the bow tie so the tie still shows,
- the staff badge now reads HR (Don "Approved." it last episode),
- censor bars: flat black bars with CENSORED in white, held for slapping onto ornaments.
Usage: robot(k, x, feet, s, pose, face, look, side, talk, alarm=False, bar=None, seed=900)
Extra poses: "slap_up" (front arm raised with a bar), "slap" (arm out, bar pressed on), "present" (to camera)."""
import math
import kit
import waiter_kit as w
from kit import INK, cut, rect, ellipse, text

HAT = (0.82, 0.10, 0.14)
HAT_DARK = (0.60, 0.05, 0.09)
FUR = (0.99, 0.99, 0.97)
FUR_SHADE = (0.80, 0.85, 0.92)
LIGHT_ON = (1.0, 0.82, 0.25)
LIGHT_ALARM = (1.0, 0.25, 0.20)
BAR = (0.06, 0.06, 0.07)

POSES = {
    "slap_up": (0.04, -4, 0, (-20, 0), (160, 10)),     # front arm high, a bar in the hand, about to slap
    "slap":    (0.08, 0, 2, (-20, 0), (100, -10)),     # arm out, the bar pressed onto the ornament
    "present": (0.00, -6, -4, (-60, -40), (60, 40)),   # both hands out to the sides: "Happy compliance!"
    "detect":  (-0.07, -12, -8, (-90, 0), (20, 0)),    # v2: the rigid "lock" point, tipped toward the target
    "pull":    (0.02, 0, 0, (-20, 0), (40, 30)),       # v2: hand pulled back after the slap; the bar stays on
}
for _k, _v in POSES.items():
    w.POSES.setdefault(_k, _v)


def censor_bar(k, x, y, wd=60, ht=18, rot=0.0, label=True, seed=0):
    """A flat black bar with CENSORED in white. (x, y) = its centre."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot)
    rect(k, -wd / 2, -ht / 2, wd, ht, BAR, seed, shadow=True, lw=1.8)
    if label and wd >= 34:
        text(k, "CENSORED", 0, ht * 0.22, ht * 0.46, (1, 1, 1), font="Inter", bold=True)
    c.restore()


def _hat(k, alarm, seed):
    """Head-local units (screen centre at 0, 0; head r 50 x 44)."""
    c = k.c
    cone = [(-46, -36), (46, -36)]
    c.move_to(-46, -36); c.curve_to(-40, -78, -6, -104, 22, -102)
    c.curve_to(48, -100, 64, -86, 68, -66)                     # the tip flops over to the side
    c.curve_to(52, -80, 34, -84, 26, -78)
    c.curve_to(40, -64, 46, -48, 46, -36); c.close_path()
    c.set_source_rgb(*HAT); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    c.set_source_rgb(*HAT_DARK); c.set_line_width(2.4)
    c.move_to(-18, -46); c.curve_to(-14, -70, 0, -88, 18, -94); c.stroke()
    # fur rim: a lumpy band across the top of the screen
    blobs = [(-46, -36), (-30, -40), (-14, -42), (2, -42), (18, -41), (34, -39), (48, -35)]
    c.set_source_rgb(*INK)
    for bx, by in blobs:
        c.arc(bx, by, 10.5, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*FUR)
    for bx, by in blobs:
        c.arc(bx, by, 9, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*FUR_SHADE)
    for bx, by in blobs[1::2]:
        c.arc(bx + 3, by + 3, 4, 0, 2 * math.pi); c.fill()
    # the pompom is the antenna light
    col = LIGHT_ALARM if alarm else LIGHT_ON
    if alarm:                                                   # glow ring + v2 radiating lines
        c.set_source_rgba(*LIGHT_ALARM, 0.25); c.arc(70, -64, 20, 0, 2 * math.pi); c.fill()
        c.set_line_cap(1)
        for i in range(7):
            a_ = -math.pi * 0.95 + i * math.pi * 1.25 / 6
            x0, y0 = 70 + math.cos(a_) * 17, -64 + math.sin(a_) * 17
            x1, y1 = 70 + math.cos(a_) * 29, -64 + math.sin(a_) * 29
            c.set_source_rgb(*INK); c.set_line_width(5.6); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
            c.set_source_rgb(*LIGHT_ALARM); c.set_line_width(3.4); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    ellipse(k, 70, -64, 11, 11, col, seed, shadow=False, lw=2.2)
    c.set_source_rgb(1, 1, 1); c.arc(66, -68, 3, 0, 2 * math.pi); c.fill()


def _beard(k, seed):
    """Cotton beard under the screen (head-local units), hooked over the head's sides; stops above the tie."""
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(1.6)               # elastic hooks
    c.move_to(-36, 30); c.line_to(-49, 6); c.stroke(); c.move_to(36, 30); c.line_to(49, 6); c.stroke()
    blobs = [(-32, 34, 9), (-24, 46, 11), (-12, 55, 11), (0, 60, 12), (12, 55, 11), (24, 46, 11), (32, 34, 9),
             (-14, 42, 9), (14, 42, 9), (0, 46, 9), (-7, 70, 8), (7, 70, 8), (0, 78, 6)]   # narrower, hangs lower
    c.set_source_rgb(*INK)
    for bx, by, r in blobs:
        c.arc(bx, by, r + 1.8, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*FUR)
    for bx, by, r in blobs:
        c.arc(bx, by, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*FUR_SHADE)
    for bx, by, r in blobs[::2]:
        c.arc(bx + r * 0.3, by + r * 0.35, r * 0.4, 0, 2 * math.pi); c.fill()


def hr_badge(k, x0, y0, seed, label="HR"):
    """v2: a bigger badge with big HR lettering, readable in the wide shot (the waiter badge is 50 x 25)."""
    c = k.c
    wd, ht = 58, 34
    x0 -= 4; y0 -= 4
    rect(k, x0 + wd / 2 - 5, y0 - 5, 10, 6, (0.45, 0.47, 0.52), seed + 1, shadow=False, lw=1.2)
    rect(k, x0, y0, wd, ht, (1, 1, 1), seed, shadow=False, lw=1.8)
    c.set_source_rgb(*kit_brand_green()); c.rectangle(x0 + 1.5, y0 + 1.5, wd - 3, 6); c.fill()
    text(k, label, x0 + wd / 2, y0 + 29, 22, INK, font="Inter", bold=True)


def kit_brand_green():
    import brand
    return brand.GREEN


def _screen_face_v2(orig):
    def screen_face(k, face, look=(0, 0), talk=0.0, side=1):
        if face != "smug":
            return orig(k, face, look, talk, side)
        c = k.c                                                  # v2: pleased with itself
        c.set_source_rgb(*w.GLOW); c.set_line_cap(1); c.set_line_width(4.5)
        c.arc(-15, 0, 8, math.pi * 1.15, math.pi * 1.85); c.stroke()      # one happy arc
        c.move_to(7, -2); c.line_to(23, -4); c.stroke()                    # one lowered lid
        c.set_line_width(3)
        c.move_to(9, -11); c.line_to(23, -15); c.stroke()                  # raised brow over it
        c.set_line_width(4)                                                # lopsided smirk
        c.move_to(-12, 14); c.curve_to(-4, 20, 8, 20, 16, 10); c.stroke()
        if talk > 0.05:
            c.rectangle(-6, 15, 14, 3 + 10 * talk); c.fill()
    return screen_face


def robot(k, x, feet, s=1.0, pose="stand", face="eager", look=(0, 0), wobble=0.0, side=1, talk=0.0,
          alarm=False, bar=None, seed=900, badge=True, locked=None, head_dx=None, head_rot=None, beard=True):
    """bar: None | "held" (in the front hand). Returns robot()'s points plus "bar" (centre) when held."""
    c = k.c
    old_badge, old_face = w._badge, w.screen_face
    w._badge = hr_badge
    w.screen_face = _screen_face_v2(old_face)
    if locked is None and pose == "detect":
        locked = True
    try:
        out = w.robot(k, x, feet, s, pose, face, look, wobble, side, talk, None, seed, badge, locked, head_dx, head_rot)
    finally:
        w._badge, w.screen_face = old_badge, old_face
    named = isinstance(pose, str)
    tilt = (w.POSES[pose] if named else pose)[0] + wobble
    hdx = head_dx if head_dx is not None else (w.HEAD_DX.get(pose, 0) if named else 0)
    hrot = head_rot if head_rot is not None else (w.HEAD_ROT.get(pose, 0) if named else 0)
    hx, hy = out["head"]
    # redraw the costume in the head's frame: same transform chain as waiter_kit (mirror, tilt, head offset)
    c.save(); c.translate(x, feet); c.scale(s * side, s); c.rotate(tilt)
    c.translate(hdx, (hy - feet) / s); c.rotate(hrot)
    if beard:
        _beard(k, seed + 70)
    _hat(k, alarm, seed + 71)
    c.restore()
    if bar == "on":                                       # v2 contact frame: the bar pressed onto an ornament
        bx, by = out["hands"][1]
        ox, oy = bx + 16 * s * side, by + 4 * s
        import sofia_xmas as sx
        sx.ornament(k, ox, oy, 20 * s, seed + 74)
        censor_bar(k, ox, oy, 56 * s, 17 * s, rot=-0.08 * side, seed=seed + 72)
        ellipse(k, bx, by, 6 * s, 6 * s, w.STEEL_DARK, seed + 73, shadow=False, lw=1.6)
        c.set_source_rgb(*INK); c.set_line_width(2 * s); c.set_line_cap(1)    # impact ticks
        for a_ in (-0.9, -0.3, 0.3):
            c.move_to(ox + math.cos(a_) * 34 * s * side, oy + math.sin(a_) * 34 * s)
            c.line_to(ox + math.cos(a_) * 44 * s * side, oy + math.sin(a_) * 44 * s); c.stroke()
        out["bar"] = (ox, oy)
    if bar == "held":
        bx, by = out["hands"][1]
        censor_bar(k, bx + 8 * s * side, by - 10 * s, 62 * s, 18 * s, rot=-0.2 * side, seed=seed + 72)
        ellipse(k, bx, by, 6 * s, 6 * s, w.STEEL_DARK, seed + 73, shadow=False, lw=1.6)     # fingers over the bar
        out["bar"] = (bx + 8 * s * side, by - 10 * s)
    return out
