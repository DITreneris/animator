"""The HR robot, "Secret Santa", v1. The canonical robot of robot_mf (untouched), no costume, plus:
New screens (robot_mf's style: full-screen colour, a bold icon, a glow):
- "personal" (shot 10, red): a magnifier over a heart, PERSONAL DATA / DETECTED: it has found Pam's heart, as data;
- "thinking" (shot 13, the hover): the idle screen with three glowing dots, a considered professional decision;
- "proud" (shot 14, silent): soft content eyes, two happy arcs, a faint warm glow: sincerely proud, no text;
- "tick" (shots 6 and 15): just the green tick (robot_mf "approved"); "approved" in shot 3 is the same tick.
The stamp: a big rubber stamp (red knob, wooden handle, a black rubber base that prints a plain black bar).
stamp="up" (raised high), "down" (pressed on the tag, squashed), "hover" (still above the kiss), None.
impact=0..3: the weight of the hit, drawn as impact lines (1 ordinary, 2 heavier, 3 the kiss).
Poses: POSE_STAMP_UP, POSE_STAMP_DOWN, POSE_HOVER, POSE_CLIP (3: the clipboard held up, stamped APPROVED).
Usage: o = robot(k, x, feet, s, pose, state, look, stamp=None, impact=0, head_rot=None, clip=False, ...)"""
import math
import cairo
import kit
import waiter_kit as w
import robot_mf as rm
from kit import INK, ellipse, rect

RED, GREEN, AMBER = rm.RED, rm.GREEN, rm.AMBER
SRX, SRY = rm.SRX, rm.SRY
WOOD = (0.62, 0.42, 0.24)
WOOD_DARK = (0.42, 0.27, 0.14)
KNOB = (0.80, 0.14, 0.14)
RUBBER = (0.08, 0.08, 0.10)
STAMP_S = 1.7
POSE_STAMP_UP = (0.0, -6, 0, (-20, 0), (150, 24))      # the stamp raised high
POSE_STAMP_DOWN = (0.08, 0, 2, (-20, 0), (48, 40))     # pressed down onto the tag in front
POSE_HOVER = (0.02, 0, 0, (-20, 0), (70, 40))          # 13: held still in the air over the kiss
POSE_CLIP = (0.0, 0, 0, (-24, 10), (80, 40))           # 3: the clipboard held out


def magnifier_heart(c, x, y, r, col):
    """The alert icon: a heart, a magnifier over it."""
    c.save(); c.translate(x, y)
    def heart():
        hr = r * 0.85
        c.move_to(-r * 0.2, hr * 0.9)
        c.curve_to(-r * 0.2 - hr * 1.5, -hr * 0.1, -r * 0.2 - hr * 0.6, -hr * 1.3, -r * 0.2, -hr * 0.45)
        c.curve_to(-r * 0.2 + hr * 0.6, -hr * 1.3, -r * 0.2 + hr * 1.5, -hr * 0.1, -r * 0.2, hr * 0.9)
        c.close_path()
    heart(); c.set_source_rgba(*col, 0.35); c.set_line_width(r * 0.5); c.stroke()
    heart(); c.set_source_rgb(*col); c.fill_preserve()
    c.set_source_rgb(0.02, 0.04, 0.08); c.set_line_width(r * 0.16); c.stroke()
    lx, ly, lr = r * 0.42, -r * 0.05, r * 0.5                            # the lens over the heart
    for wd, cl in ((r * 0.5, (*col, 0.35)), (r * 0.32, (0.02, 0.04, 0.08, 1)), (r * 0.2, (*col, 1))):
        c.arc(lx, ly, lr, 0, 2 * math.pi); c.set_source_rgba(*cl); c.set_line_width(wd); c.stroke()
        c.move_to(lx + lr * 0.72, ly + lr * 0.72); c.line_to(lx + lr * 1.6, ly + lr * 1.6)
        c.set_line_cap(1); c.set_line_width(wd * 1.3); c.stroke()
    c.restore()


def screen(k, state, look=(0, 0), talk=0.0, side=1, seed=0, t=0.0):
    c = k.c
    if state == "tick":
        state = "approved"
    if state not in ("personal", "thinking", "proud"):
        ORIG_SCREEN(k, state, look, talk, side, seed, t)
        return
    col = {"personal": RED, "thinking": w.GLOW, "proud": w.GLOW}[state]
    c.set_source_rgba(*col, 0.30 if state == "personal" else 0.16)
    c.save(); c.scale(SRX + 10, SRY + 10); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    ellipse(k, 0, 0, SRX, SRY, w.SCREEN, seed, shadow=False, lw=2)
    c.save(); c.scale(SRX - 3, SRY - 3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*col, 0.16 if state == "personal" else 0.08); c.fill()
    c.save(); c.scale(side, 1)
    if state == "personal":
        if BIG_ICON:                                             # set sheet v2: the icon leads harder
            magnifier_heart(c, 0, -10, 17, col)
            rm._lines(c, ("PERSONAL DATA", "DETECTED"), col, (21, 33), (10, 11))
        else:
            magnifier_heart(c, 0, -13, 13, col)
            rm._lines(c, ("PERSONAL DATA", "DETECTED"), col, (17, 30), (11, 12))
    elif state == "thinking":                                    # three dots, the middle one brightest
        for i, dx in enumerate((-16, 0, 16)):
            a = 1.0 if i == int(t * 3) % 3 else 0.55
            c.set_source_rgba(*col, a * 0.35); c.arc(dx, 2, 8, 0, 2 * math.pi); c.fill()
            c.set_source_rgba(*col, a); c.arc(dx, 2, 5, 0, 2 * math.pi); c.fill()
    else:                                                        # proud: two soft happy arcs, a little blush glow
        c.set_source_rgb(*col); c.set_line_cap(1); c.set_line_width(4.5)
        for sx in (-15, 15):
            c.arc(sx, 4, 9, math.pi * 1.12, math.pi * 1.88); c.stroke()
        c.set_source_rgba(1.0, 0.55, 0.55, 0.45)
        for sx in (-24, 24):
            c.save(); c.translate(sx, 14); c.scale(7, 3.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.set_source_rgb(*col); c.set_line_width(3.5)
        c.arc(0, 14, 7, math.pi * 0.2, math.pi * 0.8); c.stroke()
    c.restore()


ORIG_SCREEN = rm.screen
BIG_ICON = False


def stamp_prop(k, x, y, s=1.0, state="up", rot=0.0, seed=0):
    """(x, y) = the middle of the rubber face. 'down' squashes it a little on the hit."""
    c = k.c
    sq = 0.86 if state == "down" else 1.0
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    rect(k, -20, -7, 40, 7, RUBBER, seed, shadow=False, lw=1.8)                 # the rubber
    rect(k, -22, -17, 44, 11, WOOD, seed + 1, shadow=False, lw=2)                # the block
    c.set_source_rgb(*WOOD_DARK); c.set_line_width(1.2); c.move_to(-18, -11); c.line_to(18, -11); c.stroke()
    rect(k, -5, -40, 10, 24, WOOD, seed + 2, shadow=False, lw=2)                 # the handle
    ellipse(k, 0, -46, 11, 9, KNOB, seed + 3, shadow=False, lw=2)                # the knob
    c.set_source_rgba(1, 1, 1, 0.5); c.arc(-4, -49, 3, 0, 2 * math.pi); c.fill()
    c.restore()


def impact_lines(c, x, y, weight, s=1.0):
    """1: an ordinary THUNK, 2: heavier, 3: the kiss."""
    if not weight:
        return
    n, ln, wd = {1: (3, 10, 2.0), 2: (5, 16, 2.8), 3: (7, 24, 3.6)}[weight]
    c.set_source_rgb(*INK); c.set_line_cap(1); c.set_line_width(wd * s)
    for i in range(n):
        a = math.pi * (1.1 + 0.8 * i / (n - 1))
        r0 = 26 * s
        c.move_to(x + math.cos(a) * r0, y + math.sin(a) * r0 * 0.6)
        c.line_to(x + math.cos(a) * (r0 + ln * s), y + math.sin(a) * (r0 + ln * s) * 0.6); c.stroke()


def clipboard(k, x, y, s=1.0, approved=True, seed=0):
    import charsheets
    c = k.c
    c.save(); c.translate(x, y); c.rotate(-0.08); c.scale(s, s)
    rect(k, -20, -26, 40, 52, WOOD, seed, shadow=False, lw=2)
    rect(k, -16, -20, 32, 42, (0.99, 0.98, 0.95), seed + 1, shadow=False, lw=1.4)
    rect(k, -8, -30, 16, 8, (0.70, 0.72, 0.76), seed + 2, shadow=False, lw=1.6)
    c.set_source_rgb(0.75, 0.76, 0.80); c.set_line_width(1.2)
    for i in range(4):
        c.move_to(-12, -12 + i * 6); c.line_to(12, -12 + i * 6); c.stroke()
    if approved:
        c.save(); c.translate(0, 10); c.rotate(-0.18)
        c.set_source_rgb(*GREEN); c.set_line_width(1.8); c.rectangle(-15, -6, 30, 11); c.stroke()
        charsheets.corp(c, "APPROVED", -13.5, 2.6, 5.6, col=GREEN, bold=True)
        c.restore()
    c.restore()


def robot(k, x, feet, s=1.0, pose="stand", state="eager", look=(0, 0), side=1, talk=0.0, seed=900, badge=True,
          head_dx=None, head_rot=None, wobble=0.0, t=0.0, stamp=None, impact=0, clip=False):
    rm.screen = screen
    try:
        out = rm.robot(k, x, feet, s, pose, state, look, side, talk, seed, badge, head_dx, head_rot, wobble, t)
    finally:
        rm.screen = ORIG_SCREEN
    hx, hy = out["hands"][1]
    if stamp:                                         # the hand grips the knob; the stamp hangs below it, big
        ss_ = STAMP_S * s
        ry = hy + 46 * ss_
        stamp_prop(k, hx, ry, ss_, "down" if stamp == "down" else "up", 0.0, seed + 40)
        if stamp == "down":
            impact_lines(k.c, hx, ry, impact, ss_)
        ellipse(k, hx, hy, 8 * s, 8 * s, (0.6, 0.62, 0.66), seed + 41, shadow=False, lw=1.6 * s)
    out["stamp"] = (hx, hy + 46 * STAMP_S * s) if stamp else None
    if clip:
        clipboard(k, hx + 6 * s, hy - 4 * s, s * 1.2, True, seed + 42)
    return out
