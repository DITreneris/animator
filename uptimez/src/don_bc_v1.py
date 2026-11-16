"""v1, pinned (the current file is v2). DON, "The Best Candidate", v1: self-appointed HEAD OF TALENT. His v4 office look (don_v4: open navy fleece
vest, white shirt, khakis, the ketchup squiggle) under a grey-blue blazer two sizes too big: shoulder pads past his
shoulders, sleeves down to his knuckles, the hem below his belt. Round his neck a VISITOR pass on a green lanyard,
VISITOR struck through, HEAD OF TALENT in marker; it hangs high on his chest, so the stain stays in view.
In his hand a clipboard with his "notes" (a doodle of himself with a crown), which he hides when Mom walks in.
New faces: "sheepish" (Mom is in the room: eyes down and aside, a small crooked mouth, a blush) and "mortified"
(the reveal: eyes squeezed shut, brows up in the middle, a flat wide grimace, a blush); every don_mf / don_tg
face still works. New poses: POSE_BOARD (clipboard up, writing), POSE_HIDE (clipboard flat against his chest, back
out), POSE_STRAIGHT (hands on his knees, upright, the way she taught him), POSE_HIRED (one arm thrown up).
don_v4, don_tg, don_mf, kit and every earlier Don are untouched.
Usage: o = don(k, x, feet, s, pose, face, look, board=None | "front" | "back", mouth=None, lean=0, stain=True)"""
import math
import kit
import don_v4 as dv
import don_tg as dt
import don_mf as dm
import iwry_mouths as im
import props_bc_v1 as props
from kit import INK, cut, rect, ellipse

SKIN = dt.SKIN
BLAZER = (0.47, 0.53, 0.63)
BLAZER_DARK = (0.34, 0.40, 0.50)
BT, HY, WAIST = dm.BT, dm.HY, dm.WAIST
BLUSH = (0.95, 0.45, 0.45)

POSE_BOARD = dm.ik(-1, -60, BT + 96) + (8, 0)                     # the clipboard held up at his side (screen left)
POSE_HIDE = dm.ik(-1, -8, BT + 70) + dm.ik(1, 14, BT + 84)        # the clipboard pressed to his chest, back out
POSE_STRAIGHT = dm.ik(-1, -28, BT + 138) + dm.ik(1, 28, BT + 138)  # bolt upright, hands on his knees
POSE_HIRED = (-10, 0, 160, 14)                                    # "Hired!": an arm straight up, far too fast


def _faces(inner, mouth):
    own = ("sheepish", "mortified")

    def face_draw(k, x, y, face, look, glasses=False, seed=0):
        c = k.c
        my = y + 28
        if face not in own:
            inner(k, x, y, face, look, glasses=glasses, seed=seed)
            return
        inner(k, x, y, "neutral", (0.7, 0.8) if face == "sheepish" else (0, 0), glasses=glasses, seed=seed)
        for sx in (-1, 1):                                          # the blush
            c.save(); c.translate(x + sx * 31, y + 17); c.scale(9, 5.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(*BLUSH, 0.55); c.fill()
        if face == "mortified":
            for sx in (-17, 17):                                    # eyes squeezed shut
                ellipse(k, x + sx, y, 12.5, 12.5, SKIN, seed + sx + 60, shadow=False, outline=False)
                c.set_source_rgb(*INK); c.set_line_width(3.8); c.set_line_cap(1)
                d = 1 if sx > 0 else -1
                c.move_to(x + sx - d * 8, y - 3); c.line_to(x + sx + d * 7, y + 2); c.stroke()
                c.move_to(x + sx - d * 8, y + 6); c.line_to(x + sx + d * 7, y + 2); c.stroke()
            c.set_source_rgb(*INK); c.set_line_width(4.2); c.set_line_cap(1)
            c.move_to(x - 28, y - 14); c.line_to(x - 9, y - 22); c.stroke()
            c.move_to(x + 9, y - 22); c.line_to(x + 28, y - 14); c.stroke()
            ellipse(k, x + 1, my, 22, 12, SKIN, seed + 90, shadow=False, outline=False)
            c.move_to(x - 16, my - 4); c.line_to(x + 16, my - 4); c.line_to(x + 13, my + 5); c.line_to(x - 13, my + 5)
            c.close_path(); c.set_source_rgb(1, 1, 1); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
            c.set_line_width(1.4)
            for d in (-8, 0, 8):
                c.move_to(x + d, my - 4); c.line_to(x + d, my + 5); c.stroke()
        else:
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.move_to(x - 27, y - 15); c.line_to(x - 9, y - 21); c.stroke()
            c.move_to(x + 9, y - 21); c.line_to(x + 27, y - 15); c.stroke()
            ellipse(k, x + 1, my, 20, 11, SKIN, seed + 90, shadow=False, outline=False)
            c.set_line_width(3.8)
            c.move_to(x - 9, my + 1); c.curve_to(x - 4, my - 4, x + 2, my + 5, x + 9, my - 1); c.stroke()
        if mouth:
            ellipse(k, x + 1, my, 22, 12, SKIN, seed + 97, shadow=False, outline=False)
            im.mouth(k, x, my, mouth, SKIN, erase=(1, 1), seed=seed + 96)
    return face_draw


def _blazer(k, bt, seed, card):
    c = k.c
    hem = WAIST + 34
    for sx in (-1, 1):
        cut(k, [(sx * 24, bt + 2), (sx * 44, bt - 2), (sx * 52, hem), (sx * 22, hem)], BLAZER, shadow=False, lw=2.2)
        cut(k, [(sx * 24, bt + 2), (sx * 38, bt - 1), (sx * 36, bt + 52), (sx * 22, bt + 78)], BLAZER, shadow=False,
            lw=1.8)                                                 # a long lapel
        c.set_source_rgb(*BLAZER_DARK); c.set_line_width(2)
        c.move_to(sx * 30, hem - 40); c.line_to(sx * 47, hem - 40); c.stroke()      # pocket flap
    ellipse(k, 24, bt + 96, 3.4, 3.4, BLAZER_DARK, seed + 71, shadow=False, lw=1.3)
    ellipse(k, 24.6, bt + 114, 3.4, 3.4, BLAZER_DARK, seed + 72, shadow=False, lw=1.3)
    if card:                                                        # the lanyard, swung to his right (screen left)
        cx, cy = -7, bt + 50
        for sx in (-1, 1):
            c.set_source_rgb(*INK); c.set_line_width(5.4); c.set_line_cap(1)
            c.move_to(sx * 13, bt + 3); c.line_to(cx + sx * 2, cy - 17); c.stroke()
            c.set_source_rgb(*props.LANYARD); c.set_line_width(3.2)
            c.move_to(sx * 13, bt + 3); c.line_to(cx + sx * 2, cy - 17); c.stroke()
        props.talent_card(k, cx, cy, 0.84, 0.09, seed + 75)


def don(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=500, board=None, mouth=None, lean=0.0,
        stain=True, card=True):
    c = k.c
    if lean:
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
        try:
            out = don(k, x, feet, s, pose, face, look, seed, board, mouth, 0.0, stain, card)
            dev = {kk: ([c.user_to_device(*q) for q in out[kk]] if kk == "hands" else c.user_to_device(*out[kk]))
                   for kk in ("hands", "head") if kk in out}
        finally:
            c.restore()
        for kk, v in dev.items():
            out[kk] = [c.device_to_user(*q) for q in v] if kk == "hands" else c.device_to_user(*v)
        return out
    old_p = dict(kit.PEOPLE["DON"])
    old_hook, old_face, old_fix = kit.BADGE_HOOK, kit.face_draw, dt.SMUG_FIX
    dt.SMUG_FIX = True
    kit.face_draw = _faces(dm._mf_faces(dt._faces(old_face), mouth), mouth)
    p = dict(old_p); p["body"] = BLAZER; p.pop("tie", None)            # the sleeves are the blazer's
    kit.PEOPLE["DON"] = p
    base = dv._costume(stain, False)

    def hook(k_, name_, p_, bt, seed_):
        cut(k_, [(-43, bt), (43, bt), (47, 0), (-47, 0)], dv.SHIRT, shadow=False, lw=2)   # the shirt, under the vest
        base(k_, name_, p_, bt, seed_)
        _blazer(k_, bt, seed_, card)
    kit.BADGE_HOOK = hook
    try:
        if not isinstance(pose, str):
            kit.ARM_POSES["_bc"] = pose
            pose = "_bc"
        out = kit.person(k, "DON", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
        a = kit.ARM_POSES[pose]
    finally:
        kit.ARM_POSES.pop("_bc", None)
        kit.PEOPLE["DON"] = old_p
        kit.BADGE_HOOK, kit.face_draw, dt.SMUG_FIX = old_hook, old_face, old_fix
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sx in (-1, 1):                                              # shoulder pads, wider than he is
        cut(k, [(sx * 26, BT - 3), (sx * 50, BT - 1), (sx * 60, BT + 12), (sx * 56, BT + 24), (sx * 30, BT + 20)], BLAZER,
            shadow=False, lw=2.2)
    c.restore()
    for i in (0, 1):                                                # sleeve ends over his knuckles
        hx, hy = out["hands"][i]
        f = math.radians(a[2 * i] + a[2 * i + 1])
        dx, dy = math.sin(f), math.cos(f)
        c.save(); c.translate(hx - dx * 7 * s, hy - dy * 7 * s); c.rotate(math.atan2(dy, dx) - math.pi / 2); c.scale(s, s)
        rect(k, -11.5, -8, 23, 14, BLAZER, seed + 85 + i, shadow=False, lw=2)
        c.restore()
    if board:
        hx, hy = out["hands"][0] if pose == "_bc" and a == POSE_BOARD else out["hands"][1]
        if a == POSE_HIDE:
            props.clipboard(k, x + 4 * s, feet + (BT + 74) * s, 0.92 * s, 0.05, seed + 90, side="back")
            for q in out["hands"]:
                ellipse(k, q[0], q[1], 10 * s, 10 * s, SKIN, seed + 92, shadow=False, lw=2 * s)
        else:
            props.clipboard(k, hx - 2 * s, hy - 22 * s, 0.92 * s, -0.10, seed + 90, side=board)
            ellipse(k, hx, hy + 12 * s, 10 * s, 10 * s, SKIN, seed + 92, shadow=False, lw=2 * s)
    out["head"] = (x, feet + HY * s)
    return out
