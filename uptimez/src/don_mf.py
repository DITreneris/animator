"""v2 (don_mf_v1.py = v1, kept), acting fixes after the review: "panic" (12: wide uneven eyes, tiny pupils, brows
up, a crooked open mouth, no smile) with POSE_STIFF (rigid arms held out); "pout" (5) with less lid and a bigger
lower lip, POSE_CROSS higher and overlapping; "indignant" (7) offended rather than angry (brows up in the middle,
chin up, mouth open in protest, no teeth); POSE_CLUTCH hugs the star to his chest with both hands.
DON, "Mandatory Fun", v1. His v4 office look (don_v4: open navy fleece vest, white shirt, no tie, khakis,
belt, ketchup squiggle, staff badge) plus the self-appointed AI Police kit, cheap on purpose:
- a shiny navy plastic police cap a size too small, perched on the dome, a gold shield on the front;
- a giant gold plastic sheriff star pinned on his vest: "AI" in the middle, a "POLICE" scroll across the bottom;
- Don's bright-yellow toy handcuffs (props_mf) clipped to his belt on the hip, until the robot takes them.
New faces: "hero" (3, the entrance grin), "wink" (4, "you're under arrest"), "pout" (5, the sulk the robot scans:
lower lip out, brows down, eyes on Sofia), "indignant" (7, "You can't arrest a cop!"), "snap" (11, the yank:
tiny pupils, mouth O); "freeze" (12) and "smug" come from don_tg.
New poses: POSE_HERO, POSE_LEAN, POSE_CROSS, POSE_CLUTCH, POSE_LUNGE, POSE_SNAP. Options: cap=True | False |
(dx, dy, deg) flying off; belt_cuffs; cuff="R" (his wrist cuff, loop toward Pam); lean (degrees, - = screen left).
don_v4, don_tg, kit and every earlier Don are untouched.
Usage: o = don(k, x, feet, s, pose, face, look, cap=True, belt_cuffs=True, cuff=None, lean=0, mouth=None)"""
import math
import cairo
import kit
import brand
import don_v4 as dv
import don_tg as dt
import iwry_mouths as im
import props_mf as pr
from kit import INK, cut, rect, ellipse

SKIN = dt.SKIN
CAP = (0.13, 0.17, 0.32)
CAP_DARK = (0.07, 0.09, 0.18)
GOLD = (0.93, 0.72, 0.16)
GOLD_LIGHT = (0.99, 0.86, 0.38)
GOLD_DARK = (0.66, 0.46, 0.06)
H = kit.PEOPLE["DON"]["h"]
BT = -300 * H + 78
HY = BT - 44
WAIST = BT + 150


def ik(side, tx, ty, ln=48):
    sx, sy = side * 40, BT + 14
    vx, vy = tx - sx, ty - sy
    D = min(math.hypot(vx, vy), 2 * ln - 0.5)
    angD = math.degrees(math.atan2(vx, vy))
    al = math.degrees(math.acos(D / (2 * ln)))
    best = None
    for sg in (1, -1):
        a1 = angD + sg * al
        ex = sx + math.sin(math.radians(a1)) * ln
        if best is None or ex * side > best[0]:
            best = (ex * side, a1, -2 * sg * al)
    return best[1], best[2]


POSE_HERO = ik(-1, -6, BT + 30) + ik(1, 50, BT + 126)        # 3: taps the star's top point, other fist on the hip
POSE_LEAN = ik(-1, -44, BT + 132) + ik(1, 50, BT + 126)      # 4: leaning over her notebook, hand on the table
POSE_CROSS = ik(-1, 30, BT + 46) + ik(1, -30, BT + 38)       # 5 (v2): arms folded high, overlapping
POSE_CLUTCH = ik(-1, -36, BT + 74) + ik(1, -4, BT + 40)      # 7 (v2): both hands hug the star to his chest
POSE_CLUTCH_CLEAR = ik(-1, -58, BT + 90) + ik(1, -2, BT + 26)  # 7-8 (animatic): the hug, hands clear of the scroll
POSE_STIFF = (-24, 6, 24, -6)                                # 12: rigid, arms held out from his sides
POSE_LUNGE = (-128, 14, 70, 12)                              # 11: reaching after Sofia, cuffed arm trailing
POSE_SNAP = (-160, -24, 150, 30)                             # 11: yanked back, arms flung up


def police_star(k, x, y, r, seed=0):
    """The giant toy sheriff star: gold plastic, a lighter inner star, "AI" and a "POLICE" scroll."""
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.18); dt.star(c, x + 2, y + 3, r); c.fill()
    dt.star(c, x, y, r); c.set_source_rgb(*GOLD); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_join(1); c.stroke()
    for i in range(5):                                            # ball tips
        a = -math.pi / 2 + i * 2 * math.pi / 5
        ellipse(k, x + math.cos(a) * r, y + math.sin(a) * r, r * 0.12, r * 0.12, GOLD, seed + i, shadow=False, lw=1.6)
    dt.star(c, x, y, r * 0.66); c.set_source_rgb(*GOLD_LIGHT); c.fill()
    c.select_font_face("Lilita One", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(r * 0.62); e = c.text_extents("AI")
    c.move_to(x - e.x_advance / 2, y + r * 0.12); c.set_source_rgb(*CAP); c.show_text("AI")
    w, h = r * 1.5, r * 0.36                                      # the scroll
    yy = y + r * 0.28
    c.move_to(x - w / 2, yy); c.line_to(x + w / 2, yy); c.line_to(x + w / 2 - h * 0.35, yy + h / 2)
    c.line_to(x + w / 2, yy + h); c.line_to(x - w / 2, yy + h); c.line_to(x - w / 2 + h * 0.35, yy + h / 2); c.close_path()
    c.set_source_rgb(*CAP); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    c.set_font_size(h * 0.78); e = c.text_extents("POLICE")
    c.move_to(x - e.x_advance / 2, yy + h * 0.78); c.set_source_rgb(1, 1, 1); c.show_text("POLICE")


def police_cap(k, x, y, s=1.0, rot=0.0, seed=0):
    """The toy cap, a size too small; (x, y) = the middle of its band; drawn in the head's frame."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(s, s)
    cut(k, [(-31, 0), (-36, -26), (-24, -34), (24, -34), (36, -26), (31, 0)], CAP, shadow=False, lw=2.2)  # crown
    c.set_source_rgba(1, 1, 1, 0.35)                                                     # plastic shine
    c.save(); c.translate(-14, -24); c.rotate(-0.3); c.scale(10, 3); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    rect(k, -31, -7, 62, 9, CAP_DARK, seed + 1, shadow=False, lw=1.8)                    # band
    c.move_to(-34, 1); c.curve_to(-20, 12, 20, 12, 34, 1); c.close_path()                # visor
    c.set_source_rgb(0.05, 0.05, 0.08); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(1.6)
    c.move_to(-22, 4); c.curve_to(-12, 8, 0, 8, 8, 7); c.stroke()
    c.move_to(0, -27); c.line_to(9, -23); c.line_to(8, -13); c.line_to(0, -8); c.line_to(-8, -13); c.line_to(-9, -23)
    c.close_path(); c.set_source_rgb(*GOLD); c.fill_preserve()                           # the shield
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
    c.restore()


def belt_cuffs(k, seed=0):
    """The pair of toy cuffs hanging from his belt on the hip (body units)."""
    c = k.c
    x, y = 36, WAIST + 4
    c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(x, y - 4); c.line_to(x, y + 6); c.stroke()
    for i, (cx, cy) in enumerate(((x - 6, y + 22), (x + 9, y + 30))):
        c.set_source_rgb(*INK); c.set_line_width(6.2); c.arc(cx, cy, 9, 0, 2 * math.pi); c.stroke()
        c.set_source_rgb(*pr.TOY_YELLOW); c.set_line_width(3.6); c.arc(cx, cy, 9, 0, 2 * math.pi); c.stroke()
    pr.chain(k, x, y + 6, x + 1, y + 14, 1.0, sag=0.0, links=2)


def _mf_faces(inner, mouth):
    own = ("hero", "wink", "pout", "indignant", "snap", "panic")

    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        my = y + 28
        if face not in own:
            inner(k, x, y, face, look, glasses=glasses, seed=seed)
        elif face in ("hero", "wink"):
            inner(k, x, y, "grin", look, glasses=glasses, seed=seed)
            if face == "wink":                                    # his left eye (screen right) shut
                ellipse(k, x + 17, y, 12.5, 12.5, SKIN, seed + 61, shadow=False, outline=False)
                c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
                c.arc(x + 17, y + 3, 9, math.pi * 1.15, math.pi * 1.85); c.stroke()
        elif face == "pout":                                      # v2: brows down at the inner ends, a light lid, big lip
            inner(k, x, y, "neutral", look, glasses=glasses, seed=seed)
            c.set_source_rgb(*SKIN)
            for sx in (-17, 17):
                c.rectangle(x + sx - 12, y - 13, 24, 5); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
            for sx in (-17, 17):
                c.move_to(x + sx - 11, y - 8); c.line_to(x + sx + 11, y - 8); c.stroke()
            c.set_line_width(4.4)
            c.move_to(x - 28, y - 22); c.line_to(x - 8, y - 13); c.stroke()
            c.move_to(x + 8, y - 13); c.line_to(x + 28, y - 22); c.stroke()
            ellipse(k, x + 1, my, 21, 12, SKIN, seed + 90, shadow=False, outline=False)
            c.save(); c.translate(x + 1, my + 5); c.scale(14, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgb(0.86, 0.48, 0.46); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.8); c.stroke()
            c.set_line_width(3.8); c.move_to(x - 15, my + 1); c.curve_to(x - 6, my - 5, x + 8, my - 5, x + 17, my + 1); c.stroke()
        elif face == "indignant":                                 # v2: offended, not angry: brows up in the middle
            yy = y - 3                                            # chin up: features lifted a touch
            inner(k, x, yy, "neutral", look, glasses=glasses, seed=seed)
            for sx in (-17, 17):
                ellipse(k, x + sx, yy, 12, 12, (1, 1, 1), seed + sx + 50, shadow=False, lw=2)
                ellipse(k, x + sx + look[0] * 3, yy - 1, 4.4, 4.4, INK, seed + sx + 51, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4.4); c.set_line_cap(1)
            c.move_to(x - 28, yy - 20); c.line_to(x - 9, yy - 28); c.stroke()
            c.move_to(x + 9, yy - 28); c.line_to(x + 28, yy - 20); c.stroke()
            ellipse(k, x + 1, yy + 28, 20, 12, SKIN, seed + 90, shadow=False, outline=False)
            ellipse(k, x + 1, yy + 30, 10, 8, (0.35, 0.08, 0.08), seed + 92, shadow=False, lw=2.4)
        elif face == "snap":                                      # the yank: tiny pupils, brows shot up, mouth O
            inner(k, x, y, "shock", (0, 0), glasses=glasses, seed=seed)
            for sx in (-17, 17):
                ellipse(k, x + sx, y, 13, 13, (1, 1, 1), seed + sx + 50, shadow=False, lw=2)
                ellipse(k, x + sx, y, 2.6, 2.6, INK, seed + sx + 51, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.move_to(x - 27, y - 28); c.line_to(x - 9, y - 32); c.stroke()
            c.move_to(x + 9, y - 32); c.line_to(x + 27, y - 28); c.stroke()
            ellipse(k, x + 1, my, 20, 12, SKIN, seed + 90, shadow=False, outline=False)
            ellipse(k, x + 1, my + 2, 8, 10, (0.35, 0.08, 0.08), seed + 92, shadow=False, lw=2.4)
        elif face == "panic":                                     # 12: he can't get out: no smile anywhere
            inner(k, x, y, "neutral", (0, 0), glasses=glasses, seed=seed)
            ellipse(k, x - 17, y - 1, 13.5, 13.5, (1, 1, 1), seed + 50, shadow=False, lw=2.2)
            ellipse(k, x + 17, y + 1, 10.5, 10.5, (1, 1, 1), seed + 52, shadow=False, lw=2.2)
            ellipse(k, x - 15, y - 1, 2.6, 2.6, INK, seed + 51, shadow=False, outline=False)
            ellipse(k, x + 18, y + 1, 2.4, 2.4, INK, seed + 53, shadow=False, outline=False)
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.move_to(x - 29, y - 22); c.line_to(x - 9, y - 31); c.stroke()
            c.move_to(x + 9, y - 25); c.line_to(x + 27, y - 21); c.stroke()
            ellipse(k, x + 1, my, 21, 12, SKIN, seed + 90, shadow=False, outline=False)
            c.move_to(x - 13, my - 2); c.line_to(x + 11, my - 6); c.curve_to(x + 13, my + 8, x - 6, my + 12, x - 13, my - 2)
            c.close_path(); c.set_source_rgb(0.35, 0.08, 0.08); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
            for sx_, sy_ in ((40, -18), (-42, -8)):
                import don_xmas
                don_xmas.sweat_drop(k, x + sx_, y + sy_, 0.8)
        if mouth and face in ("hero", "wink", "pout", "indignant", "neutral"):
            ellipse(k, x + 1, my, 20, 12, SKIN, seed + 97, shadow=False, outline=False)
            im.mouth(k, x, my, mouth, SKIN, erase=(1, 1), seed=seed + 96)
    return face_draw


def don(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=500, cap=True, belt_cuffs_on=True,
        cuff=None, lean=0.0, mouth=None, badge=True):
    c = k.c
    if lean:
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
        try:
            out = don(k, x, feet, s, pose, face, look, seed, cap, belt_cuffs_on, cuff, 0.0, mouth, badge)
            dev = {kk: ([c.user_to_device(*q) for q in out[kk]] if kk == "hands" else c.user_to_device(*out[kk]))
                   for kk in ("hands", "cuff", "head") if kk in out}
        finally:
            c.restore()
        for kk, v in dev.items():
            out[kk] = [c.device_to_user(*q) for q in v] if kk == "hands" else c.device_to_user(*v)
        return out
    old_p = dict(kit.PEOPLE["DON"])
    old_hook, old_face, old_fix = kit.BADGE_HOOK, kit.face_draw, dt.SMUG_FIX
    dt.SMUG_FIX = True
    kit.face_draw = _mf_faces(dt._faces(old_face), mouth)
    p = dict(old_p); p["body"] = dv.SHIRT; p.pop("tie", None)
    kit.PEOPLE["DON"] = p
    base = dv._costume(True, badge)

    def hook(k_, name_, p_, bt, seed_):
        base(k_, name_, p_, bt, seed_)
        if belt_cuffs_on:
            belt_cuffs(k_, seed_ + 70)
        police_star(k_, -20, bt + 54, 35, seed_ + 80)
    kit.BADGE_HOOK = hook
    try:
        if not isinstance(pose, str):
            kit.ARM_POSES["_mf"] = pose
            pose = "_mf"
        out = kit.person(k, "DON", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
        a = kit.ARM_POSES[pose]
    finally:
        kit.ARM_POSES.pop("_mf", None)
        kit.PEOPLE["DON"] = old_p
        kit.BADGE_HOOK, kit.face_draw, dt.SMUG_FIX = old_hook, old_face, old_fix
    if cap:
        dx, dy, rot = (0, 0, -4) if cap is True else cap
        police_cap(k, x + (4 + dx) * s, feet + (HY - 36 + dy) * s, s, rot, seed + 5)
    if cuff:
        i = 0 if cuff == "L" else 1
        hx, hy = out["hands"][i]
        f = math.radians(a[2 * i] + a[2 * i + 1])
        ddx, ddy = math.sin(f), math.cos(f)
        ang = math.atan2(ddy, ddx) + math.pi / 2
        ls = 1 if math.cos(ang) > 0 else -1                       # loop toward Pam (screen right)
        out["cuff"] = pr.cuff(k, hx - ddx * 13 * s, hy - ddy * 13 * s, s * 0.9, ang, loop_side=ls)
    return out
