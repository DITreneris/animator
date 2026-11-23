"""DON in "Pick a Side" (episode 14): his look as ever (fleece vest, the ketchup stain, the headset, the one hair); this
episode's poses and props. Tomas, 23 Nov, /grill-me:
- under the fallen blind his face pokes out through a bent gap in the slats (1.2-1.3); then he wears it as a cape (1.4);
- the selfie: chin up, double thumbs-up (3.1); one thumb onto the pad without looking (3.4);
- the office gag (5.4): a knee up, the foot hovering over the tape, arms a little out, then back down;
- the last frame (6.1): thumbs in the vest, elbows wide, a warm, satisfied smile.
Nothing in his rig changes: fs_storyboard.don draws him, with arm poses passed by angle; the blind, the tape roll, the
thumbs and the raised leg are drawn over him (the leg: his trousers clipped at the knee and redrawn).
  don(k, x, feet, s, pose, face, look, knee=0.0, lean=0.0, chin=False)
  python3 don_ps.py [out_dir]  ->  ps_don_v1.png (sheet), ps_don_phone_v1.png (phone check)"""
import math
import os
import sys
import cairo
import kit
import fs_storyboard as sb
import don_v4 as dv
from kit import Ctx, INK, cut, rect, ellipse

TAPE = (0.95, 0.78, 0.15)
SLAT, SLAT_D = (0.86, 0.86, 0.82), (0.55, 0.55, 0.52)
KNEE_Y = -62                                              # the knee, in his own units (feet at 0)
POSES = {"cord": (-8, 0, 168, 8), "salute": (-8, 0, 128, 118), "thumbs": (-48, -118, 48, 118), "point_roll": (-8, 0, 92, 4),
         "balance": (-40, 10, 40, -10), "vest": "vest", "push": (-60, 40, 60, -40), "lift_roll": (-8, 0, 120, 60)}


def don(k, x, feet, s=0.60, pose="stand", face="neutral", look=(0, 0), knee=0.0, lean=0.0, chin=False):
    """knee 0..1: his screen-right knee comes up and the foot hovers (5.4). lean: radians, tipping about his feet."""
    c = k.c
    p = POSES.get(pose, pose)
    c.save(); c.translate(x, feet); c.rotate(lean); c.translate(-x, -feet)
    if knee > 0:
        c.save(); c.rectangle(x - 400, feet - 2000, 800, 2000 + KNEE_Y * s); c.clip()
    sb.DON_STATE[0] = ("up", "up")
    try:
        if chin:
            o = _don_chin(k, x, feet, s, p, face, look)
        else:
            o = sb.don(k, x, feet, s, p, face, look)
    finally:
        sb.DON_STATE[0] = None
    if knee > 0:
        c.restore()
        _legs(k, x, feet, s, knee)
    c.restore()
    return o


def _don_chin(k, x, feet, s, p, face, look):
    kit.ARM_POSES["_ps"] = p if isinstance(p, tuple) else sb.don.__defaults__ and p
    import acts_ob as ac
    if not isinstance(p, tuple):
        return sb.don(k, x, feet, s, p, face, look)
    kit.ARM_POSES["_ps"] = p
    try:
        with ac.arms():
            return dv.don(k, x, feet, s, "_ps", face, look=look, seed=500, chin=1)
    finally:
        del kit.ARM_POSES["_ps"]


def _legs(k, x, feet, s, u):
    """Below the knee: the screen-left leg straight to the floor; the screen-right one lifted, the foot hovering."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    ky = KNEE_Y
    lift = 120 * u
    cut(k, [(-45, ky - 2), (0, ky - 2), (0, 0), (-47, 0)], dv.KHAKI, shadow=False, lw=2)
    cut(k, [(-49, -10), (2, -10), (4, 2), (-51, 2)], (0.24, 0.18, 0.13), shadow=False, lw=2)     # the planted shoe
    c.set_source_rgba(0, 0, 0, 0.20); c.save(); c.translate(30, 4); c.scale(1, 0.22); c.arc(0, 0, 30 * (1 - 0.4 * u), 0, 2 * math.pi)
    c.restore(); c.fill()                                                            # the shadow under the hovering foot
    kx, kyy = 26, ky - 22 * u                                                        # the knee, up and toward us
    cut(k, [(0, ky - 2), (45, ky - 2), (kx + 30, kyy + 6), (kx - 26, kyy + 10)], dv.KHAKI, shadow=False, lw=2)   # thigh
    cut(k, [(kx - 24, kyy + 6), (kx + 28, kyy + 2), (kx + 30, -lift), (kx - 18, -lift)], dv.KHAKI, shadow=False, lw=2)  # shin
    ellipse(k, kx + 2, kyy + 4, 30, 20, dv.KHAKI, 4700, shadow=False, lw=2)                                    # the kneecap
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.new_path(); c.arc(kx + 2, kyy + 8, 12, 0.3, math.pi - 0.3); c.stroke()
    cut(k, [(kx - 24, -lift), (kx + 36, -lift), (kx + 40, -lift + 14), (kx - 26, -lift + 14)], (0.24, 0.18, 0.13), shadow=False, lw=2)
    for i in (-1, 1):                                                                  # wobble lines: he's balancing
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.new_path()
        c.arc(kx + 6 + i * 58, -lift + 4, 10, -0.9 if i > 0 else math.pi - 0.9, 0.9 if i > 0 else math.pi + 0.9); c.stroke()
    c.restore()


def blind_over(k, head, s, seed=4800):
    """1.2-1.3: the whole blind over him, his face through a bent gap in the slats, the cord dangling."""
    c = k.c
    hx, hy = head
    w, top, bot = 150 * s, hy - 70 * s, hy + 230 * s
    c.save()
    c.new_path(); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(hx - w / 2, top, w, bot - top)
    c.save(); c.translate(hx, hy + 6 * s); c.scale(44 * s, 40 * s); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*SLAT); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.2); c.stroke()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_source_rgb(*SLAT_D); c.set_line_width(1.4)
    yy = top + 10 * s
    while yy < bot:
        dy = abs(yy - (hy + 6 * s))
        if dy < 40 * s:                                                               # the slats bend round his face
            half = 44 * s * math.sqrt(max(0.0, 1 - (dy / (40 * s)) ** 2))
            c.move_to(hx - w / 2, yy); c.line_to(hx - half - 3, yy); c.stroke()
            c.move_to(hx + half + 3, yy); c.line_to(hx + w / 2, yy); c.stroke()
        else:
            c.move_to(hx - w / 2, yy); c.line_to(hx + w / 2, yy); c.stroke()
        yy += 11 * s
    c.restore()
    rect(k, hx - w / 2 - 6 * s, top - 10 * s, w + 12 * s, 12 * s, (0.70, 0.70, 0.66), seed, shadow=False, lw=2)   # the rail, askew
    c.set_source_rgb(0.30, 0.30, 0.30); c.set_line_width(2.2)
    c.move_to(hx + w / 2 - 8 * s, top); c.curve_to(hx + w / 2 + 6 * s, hy + 60 * s, hx + w / 2 - 4 * s, hy + 140 * s, hx + w / 2 + 10 * s, hy + 200 * s)
    c.stroke()
    ellipse(k, hx + w / 2 + 10 * s, hy + 204 * s, 4 * s, 6 * s, (0.92, 0.88, 0.70), seed + 1, shadow=False, lw=1.4)


def blind_cape(k, head, s, seed=4810):
    """1.4: the blind over his shoulders like a cape (drawn before him: behind), its rail across his shoulders."""
    c = k.c
    hx, hy = head
    top, bot = hy + 56 * s, hy + 300 * s
    cut(k, [(hx - 70 * s, top), (hx + 70 * s, top), (hx + 96 * s, bot), (hx - 96 * s, bot)], SLAT, lw=2.2)
    c.set_source_rgb(*SLAT_D); c.set_line_width(1.4)
    yy = top + 10 * s
    while yy < bot:
        t = (yy - top) / (bot - top)
        hw = 70 * s + 26 * s * t
        c.move_to(hx - hw, yy); c.line_to(hx + hw, yy); c.stroke(); yy += 11 * s


def cape_rail(k, head, s, seed=4811):
    hx, hy = head
    c = k.c
    c.save(); c.translate(hx, hy + 60 * s); c.rotate(-0.08)
    rect(k, -78 * s, -6 * s, 156 * s, 12 * s, (0.70, 0.70, 0.66), seed, shadow=False, lw=2)
    c.restore()


def tape_roll(k, x, y, s, ang=0.0):
    """The roll of yellow tape: a fat ring, a tongue of tape hanging off it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(10, 8), (30, 10), (34, 60), (22, 64), (14, 56)], TAPE, lw=1.8)
    for col, lw in ((INK, 30), (TAPE, 25)):
        c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.80, 0.62, 0.10); c.set_line_width(3); c.new_path(); c.arc(0, 0, 16, 0, 2 * math.pi); c.stroke()
    c.restore()


def thumb(k, x, y, s, up=True):
    """A thumbs-up over his ball hand."""
    c = k.c
    c.save(); c.translate(x, y); c.scale(s, s)
    cut(k, [(-6, -4), (-8, -30), (-2, -36), (6, -32), (8, -4)], (0.96, 0.80, 0.68), lw=2)
    c.restore()


def salute_hand(k, x, y, s):
    """The flat hand at his brow, fingers together."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(-0.45); c.scale(s, s)
    cut(k, [(-6, -14), (34, -18), (40, -10), (34, -2), (-6, 6)], (0.96, 0.80, 0.68), lw=2)
    c.set_source_rgb(*INK); c.set_line_width(1.2)
    for yy in (-10, -5):
        c.move_to(12, yy); c.line_to(34, yy - 2); c.stroke()
    c.restore()


def _label(c, s, x, y, size=16, col=INK):
    c.select_font_face("Inter", 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - e.x_advance / 2, y); c.show_text(s)


def sheet(out):
    W, H = 2400, 1300
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
    F = 860
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, F, W, 200); c.fill()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(30); c.set_source_rgb(*INK); c.move_to(40, 50)
    c.show_text("PICK A SIDE · DON · his look as ever, this episode's poses and props · v1")
    c.select_font_face("Inter", 0, 0); c.set_font_size(18); c.move_to(40, 84)
    c.show_text("the blind (face through the slats, then a cape) · the tape roll · the salute · double thumbs-up · the knee over the line · thumbs in the vest")
    S = 0.60 * 1.5
    xs = [140, 400, 660, 920, 1180, 1440, 1700, 1960, 2220]
    o = don(k, xs[0], F, S, "cord", "squint", (1, -0.4))                                             # 1.1
    hx, hy = o["hands"][1]
    c.set_source_rgb(0.3, 0.3, 0.3); c.set_line_width(2.4); c.move_to(hx, hy - 180); c.line_to(hx, hy + 10); c.stroke()
    o = don(k, xs[1], F, S, "stand", "squint", (0, 0))                                                # 1.3
    blind_over(k, o["head"], S)
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
    h0 = sb.don(Ctx(cairo.Context(tmp), 0), xs[2], F, S, "stand", "neutral", (0, 0))["head"]
    blind_cape(k, h0, S)                                                                            # 1.4, behind him
    o = don(k, xs[2], F, S, "lift_roll", "hollow", (0, 0))
    cape_rail(k, o["head"], S)
    tape_roll(k, *o["hands"][1], S * 0.9)
    o = don(k, xs[3], F, S, "point_roll", "smug", (1, 0))                                             # 2.3
    tape_roll(k, o["hands"][1][0] + 10, o["hands"][1][1], S * 0.9, ang=0.6)
    o = don(k, xs[4], F, S, "salute", "pleased", (0.6, 0))                                            # 2.5
    salute_hand(k, *o["hands"][1], S)
    don(k, xs[5], F, S, "push", "shock", (1, 0), lean=-0.20)                                           # 2.11: bumped
    o = don(k, xs[6], F, S, "thumbs", "pleased", (0, -0.3))                                            # 3.1
    for hx_, hy_ in o["hands"]:
        thumb(k, hx_, hy_ - 4 * S, S)
    c.set_source_rgb(*TAPE); c.move_to(xs[7] + 22, F); c.line_to(xs[7] + 44, F); c.line_to(xs[7] + 70, F + 110)
    c.line_to(xs[7] + 44, F + 110); c.fill()                                                         # 5.4: the line under his foot
    don(k, xs[7], F, S, "balance", "smug", (1, 0), knee=1.0)
    don(k, xs[8], F, S, "vest", "pleased", (0, 0))                                                   # 6.1
    for x, n, note in zip(xs, ("1.1", "1.3", "1.4", "2.3", "2.5", "2.11", "3.1", "5.4", "6.1"),
                          ("the cord", "through the slats", "the cape, the roll", "\"Pick a side.\"", "\"Pam. My general.\"",
                           "bumped by the robot", "chin up, thumbs up", "knee over the line", "\"Everyone's with me.\"")):
        _label(c, n, x, F + 140, 20); _label(c, note, x, F + 166, 14, (0.3, 0.3, 0.3))
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    frames = []
    for name, txt in (("medium", "1.3: the first line, through the slats"), ("medium ", "5.4: the knee over the line"),
                      ("close", "6.1: \"Everyone's with me.\"")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "medium":
            o = don(k, 270, 1120, 0.60 * 2.4, "stand", "squint", (0, 0))
            blind_over(k, o["head"], 0.60 * 2.4)
        elif name == "medium ":
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 820, 540, 140); c.fill()
            c.set_source_rgb(*TAPE); c.move_to(278, 820); c.line_to(300, 820); c.line_to(350, 960); c.line_to(320, 960); c.fill()
            don(k, 250, 880, 0.60 * 1.7, "balance", "smug", (1, 0), knee=1.0)
        else:
            don(k, 270, 1330, 0.60 * 3.0, "vest", "pleased", (0, 0))
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.strip().upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_don_v1.png"))
    phone(os.path.join(d, "ps_don_phone_v1.png"))
