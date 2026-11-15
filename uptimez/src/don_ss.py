"""DON, "Secret Santa", v2 (don_ss_v1.py = v1, kept). v2 after the review: 80% incompetent agent, 20% Christmas.
No hat by default (hat=True brings back the v1 hat, for comparison only): the bald dome stays free for shot 6, where
POSE_SMOOTH now puts his palm on top of the dome and the glint sits on the crown. The card's TOP SECRET and SANTA are
bigger (HR-APPROVED stays small). beard="on": an obviously fake white Santa beard hooked over his ears on elastic,
a hole for the mouth; beard="slipped": it has slid down to his neck and he hasn't noticed (the optional shot 3 gag).
v1 notes: AGENT SECRET SANTA. He heard "Secret Santa" and took it as a mission.
His v4 office look (don_v4: open navy fleece vest, white shirt, khakis, the ketchup squiggle, staff badge) with no
police kit, plus props only, cheap on purpose (no tuxedo, no trench coat, nothing from any real spy franchise):
- a classic floppy Santa hat, red with white trim; the tip flops to his screen-left and the pompom bounces
  (hat_bounce = 0..1 phase of a small bounce, or (dx, dy) for the pompom offset);
- cheap black shades: shades="on" (entrance), "down" (slid down his nose, the eyes peek over: shot 6), None;
- a coiled earpiece wire from his screen-right ear down into the collar;
- his own laminated card: TOP SECRET · SANTA · HR-APPROVED, sealed with a ketchup thumbprint; card="hand"
  (flashed in his raised hand) | "vest" (clipped on the vest) | None.
Faces: everything in don_mf / don_tg ("hero" the entrance grin, "smug" the vain half-lids + one-sided smirk).
Poses: POSE_WIDE (3: arms wide, the showman), POSE_SMOOTH (6: his palm glides over the side of the bald dome under the
hat brim, with a glint).
Usage: o = don(k, x, feet, s, pose, face, look, shades="on", card="hand", hat_bounce=0.0, mouth=None, lean=0)"""
import math
import kit
import don_v4 as dv
import don_tg as dt
import don_mf as dm
from kit import INK, cut, rect, ellipse

SKIN = dt.SKIN
HY = dm.HY
BT = dm.BT
HAT_RED = (0.82, 0.13, 0.15)
HAT_DARK = (0.58, 0.07, 0.10)
FUR = (0.98, 0.97, 0.94)
FUR_SHADE = (0.86, 0.85, 0.82)
SHADES = (0.07, 0.07, 0.09)
KETCHUP = (0.80, 0.16, 0.10)
CARD = (0.99, 0.98, 0.95)
STAMP_RED = (0.78, 0.10, 0.12)
BIG_CARD = True
POSE_WIDE = (-112, -18, 112, 18)                       # 3: arms flung wide in the doorway
POSE_WIDE_CARD = (-112, -18) + dm.ik(1, 72, BT - 26)     # 3: one arm wide, the other up flashing the card
POSE_SMOOTH = dm.ik(-1, -50, BT + 126) + dm.ik(1, 26, HY - 30)   # 6 (v2): palm on top of the dome


def santa_hat(k, x, y, s=1.0, bounce=0.0, seed=0):
    """(x, y) = the middle of the fur band, in screen units; the tip flops over to screen left."""
    c = k.c
    if isinstance(bounce, tuple):
        pdx, pdy = bounce
    else:
        pdx, pdy = 4 * math.sin(bounce * 2 * math.pi), -9 * abs(math.sin(bounce * 2 * math.pi))
    c.save(); c.translate(x, y); c.scale(s, s)
    tip = (-62 + pdx, -6 + pdy)
    c.move_to(-36, -4)                                                    # the floppy cone
    c.curve_to(-30, -52, 20, -64, 32, -6)
    c.line_to(18, -10)
    c.curve_to(6, -40, -30, -40, tip[0] + 10, tip[1] - 4)
    c.curve_to(tip[0] + 4, tip[1] + 6, -44, 0, -36, -4); c.close_path()
    c.set_source_rgb(*HAT_RED); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_join(1); c.stroke()
    c.set_source_rgba(*HAT_DARK, 0.6); c.set_line_width(3)               # a fold shadow
    c.move_to(-10, -40); c.curve_to(-24, -36, -38, -24, tip[0] + 12, tip[1]); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.25)
    c.save(); c.translate(6, -38); c.rotate(-0.4); c.scale(12, 4); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    for i in range(7):                                                    # the fur band, lumpy
        bx = -36 + i * 12
        ellipse(k, bx, -2 + (i % 2) * 1.5, 9, 8, FUR, seed + i, shadow=False, lw=1.8)
    c.set_source_rgb(*FUR); c.rectangle(-38, -7, 76, 10); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.8)
    c.move_to(-40, -9); c.curve_to(-14, -12, 14, -12, 40, -9); c.stroke()
    c.move_to(-40, 6); c.curve_to(-14, 9, 14, 9, 40, 6); c.stroke()
    ellipse(k, tip[0], tip[1], 11, 11, FUR, seed + 9, shadow=False, lw=2)  # the pompom
    c.set_source_rgb(*FUR_SHADE); c.arc(tip[0] + 3, tip[1] + 3, 5, 0, 2 * math.pi); c.fill()
    c.restore()


def shades_draw(k, x, y, state):
    """Cheap black shades. "on": over the eyes; "down": slid down the nose, the eyes peek over the top."""
    if not state:
        return
    c = k.c
    top = y - 9 if state == "on" else y + 8
    sc = 1.0 if state == "on" else 0.6
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
    for sx in (-1, 1):                                                    # the arms, out to the ears
        c.move_to(x + sx * 31, top + 4); c.line_to(x + sx * 46, top + 1); c.stroke()
    for sx in (-17, 17):
        c.move_to(x + sx - 15, top); c.line_to(x + sx + 15, top); c.line_to(x + sx + 13, top + 12 * sc)
        c.curve_to(x + sx + 8, top + 19 * sc, x + sx - 8, top + 19 * sc, x + sx - 13, top + 12 * sc); c.close_path()
        c.set_source_rgb(*SHADES); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(2.2)          # the cheap shine
        c.move_to(x + sx - 9, top + 4); c.line_to(x + sx - 3, top + 4); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(3.2)
    c.move_to(x - 3, top + 3); c.line_to(x + 3, top + 3); c.stroke()


CARD_FIX = False   # full animation: the vest card sits clear of his arm (v1 read "P SECRET / ANTA" when clipped)
CLEAN = False   # animatic v2: a tidy earpiece wire and his forearm drawn over the head in POSE_SMOOTH (off: v1 looks)


def earpiece(k, x, y):
    """A coiled wire from the screen-right ear down into the collar."""
    c = k.c
    ellipse(k, x + 44, y + 8, 4.5, 4.5, (0.15, 0.15, 0.17), 3, shadow=False, lw=1.4)
    if CLEAN:                                    # v2: one thin, softly curled wire (the v1 rings were joined by
        c.new_path()                             # stray lines, which read as a tangle in close-up)
        c.set_source_rgb(0.22, 0.22, 0.25); c.set_line_width(1.6); c.set_line_cap(1)
        for i in range(41):
            t = i / 40
            px_ = x + 44 - 9 * t + 1.6 * math.sin(t * 30)
            py_ = y + 12 + 46 * t
            (c.move_to if i == 0 else c.line_to)(px_, py_)
        c.stroke()
        return
    c.set_source_rgb(0.25, 0.25, 0.28); c.set_line_width(1.8)
    for i in range(11):
        t = i / 10
        cx = x + 44 - 8 * t + 3 * math.sin(i * 1.7)
        cy = y + 12 + 46 * t
        c.arc(cx, cy, 2.6, 0, 2 * math.pi); c.stroke()


def secret_card(k, x, y, s=1.0, rot=0.0, seed=0):
    """His laminated card: TOP SECRET (red stamp), SANTA, HR-APPROVED, a ketchup thumbprint. (x, y) = its centre."""
    import charsheets
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(k, -24, -16, 48, 32, CARD, seed, shadow=False, lw=2)
    c.set_source_rgba(1, 1, 1, 0.5); c.move_to(-20, -14); c.line_to(-4, -14); c.line_to(-14, 14)
    c.line_to(-22, 14); c.close_path(); c.fill()                         # laminate shine
    if BIG_CARD:                                                         # v2: the words that matter, big
        c.set_source_rgb(*STAMP_RED); c.rectangle(-22, -14, 44, 14); c.fill()
        charsheets.corp(c, "TOP SECRET", -20.2, -4.2, 6.6, col=(1, 1, 1), bold=True)
        charsheets.corp(c, "SANTA", -19, 9.6, 8.6, col=INK, bold=True)
        charsheets.corp(c, "HR-APPROVED", -19, 14.6, 3.2, col=(0.35, 0.40, 0.50), bold=True)
    else:
        c.set_source_rgb(*STAMP_RED); c.set_line_width(1.6); c.rectangle(-20, -12, 40, 11); c.stroke()
        charsheets.corp(c, "TOP SECRET", -18.6, -3.8, 5.4, col=STAMP_RED, bold=True)
        charsheets.corp(c, "SANTA", -18, 6.5, 6.5, col=INK, bold=True)
        charsheets.corp(c, "HR-APPROVED", -18, 13, 3.6, col=(0.35, 0.40, 0.50), bold=True)
    tx, ty = (17, 11) if BIG_CARD else (14, 8)
    c.save(); c.translate(tx, ty); c.rotate(0.4); c.scale(5.2, 4.2)       # the ketchup thumbprint
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*KETCHUP, 0.9); c.fill()
    c.set_source_rgba(0.55, 0.08, 0.05, 0.7); c.set_line_width(0.7)
    for r in (1.6, 3.0, 4.2):
        c.save(); c.translate(tx, ty); c.rotate(0.4); c.scale(r * 1.2, r); c.arc(0, 0, 1, 0.3, 5.6); c.restore(); c.stroke()
    c.restore()


def beard_draw(k, x, y, state, seed=0):
    """An obviously fake white beard on elastic. "on": hooked over the ears, a hole for the mouth;
    "slipped": slid down round his neck."""
    if not state:
        return
    c = k.c
    dy = 0 if state == "on" else 46
    c.set_source_rgb(0.95, 0.95, 0.95); c.set_line_width(1.6)             # the elastic, ear to ear
    for sx in (-1, 1):
        c.move_to(x + sx * 44, y + 6); c.line_to(x + sx * 36, y + 16 + dy); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(0.8)
    for sx in (-1, 1):
        c.move_to(x + sx * 45, y + 6); c.line_to(x + sx * 37, y + 16 + dy); c.stroke()
    cy0, rx, ry = y + 20 + dy, 40, 38
    bumps = [(x + rx * math.cos(a), cy0 + ry * math.sin(a)) for a in [math.pi * (i / 10) for i in range(11)]]
    for (bx, by) in bumps:                                                # scalloped cotton-wool edge
        c.arc(bx, by, 8.5, 0, 2 * math.pi)
        c.set_source_rgb(0.98, 0.98, 0.97); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.save(); c.translate(x, cy0); c.scale(rx, ry); c.arc(0, 0, 1, 0, math.pi); c.restore(); c.close_path()
    c.set_source_rgb(0.98, 0.98, 0.97); c.fill()
    c.set_source_rgb(0.98, 0.98, 0.97); c.rectangle(x - rx, cy0 - 7, 2 * rx, 8); c.fill()
    c.set_source_rgb(0.86, 0.86, 0.84); c.set_line_width(1.4)            # cotton texture
    for (ax, ay) in ((-22, 34), (-6, 46), (12, 40), (26, 30), (0, 56)):
        c.arc(x + ax, y + ay + dy, 5, 0.3, 2.6); c.stroke()
    if state == "on":                                                     # the hole for the mouth
        c.save(); c.translate(x + 1, y + 28); c.scale(17, 8); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*SKIN); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke()


def _faces(inner, shades, mouth, beard=None):
    base = dm._mf_faces(inner, mouth)

    def face_draw(k, x, y, face, look, glasses=False, seed=0, _no_beard=False):
        c = k.c
        if face == "showman":                         # 3: the big open grin under the shades, brows up
            base(k, x, y, "neutral", look, glasses=glasses, seed=seed)
            my = y + 28
            ellipse(k, x + 1, my - 1, 20, 10, SKIN, seed + 90, shadow=False, outline=False)
            c.move_to(x - 16, my - 5); c.curve_to(x - 10, my + 14, x + 12, my + 14, x + 18, my - 5); c.close_path()
            c.set_source_rgb(0.35, 0.08, 0.08); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_join(1); c.stroke()
            c.save(); c.move_to(x - 16, my - 5); c.curve_to(x - 10, my + 14, x + 12, my + 14, x + 18, my - 5)
            c.close_path(); c.clip()
            c.set_source_rgb(1, 1, 1); c.rectangle(x - 16, my - 6, 34, 5); c.fill()
            c.set_source_rgb(0.85, 0.35, 0.38); c.arc(x + 1, my + 10, 6, 0, 2 * math.pi); c.fill()
            c.restore()
            c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(1)
            c.move_to(x - 26, y - 22); c.line_to(x - 9, y - 26); c.stroke()
            c.move_to(x + 9, y - 26); c.line_to(x + 26, y - 22); c.stroke()
        else:
            base(k, x, y, face, look, glasses=glasses, seed=seed)
        if _no_beard:
            return
        if beard:
            beard_draw(k, x, y, beard, seed)
            if beard == "on":                         # the mouth is redrawn inside its hole
                k.c.save()
                k.c.save(); k.c.translate(x + 1, y + 28); k.c.scale(17, 8); k.c.arc(0, 0, 1, 0, 2 * math.pi)
                k.c.restore(); k.c.clip()
                face_draw(k, x, y, face, look, glasses, seed, _no_beard=True)
                k.c.restore()
        shades_draw(k, x, y, shades)
        earpiece(k, x, y)
    return face_draw


def don(k, x, feet, s=1.0, pose="stand", face="neutral", look=(0, 0), seed=500, shades="on", card="vest",
        hat_bounce=0.0, mouth=None, lean=0.0, badge=True, glint=False, hat=False, beard=None):
    c = k.c
    if lean:
        c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
        try:
            out = don(k, x, feet, s, pose, face, look, seed, shades, card, hat_bounce, mouth, 0.0, badge, glint, hat,
                      beard)
            dev = {kk: ([c.user_to_device(*q) for q in out[kk]] if kk == "hands" else c.user_to_device(*out[kk]))
                   for kk in ("hands", "head") if kk in out}
        finally:
            c.restore()
        for kk, v in dev.items():
            out[kk] = [c.device_to_user(*q) for q in v] if kk == "hands" else c.device_to_user(*v)
        return out
    pose_in = pose
    old_p = dict(kit.PEOPLE["DON"])
    old_hook, old_face, old_fix = kit.BADGE_HOOK, kit.face_draw, dt.SMUG_FIX
    dt.SMUG_FIX = True
    kit.face_draw = _faces(dt._faces(old_face), shades, mouth, beard)
    p = dict(old_p); p["body"] = dv.SHIRT; p.pop("tie", None)
    kit.PEOPLE["DON"] = p
    base = dv._costume(True, badge)

    def hook(k_, name_, p_, bt, seed_):
        base(k_, name_, p_, bt, seed_)
        if card == "vest" and CARD_FIX:
            secret_card(k_, -15, bt + 40, 0.66, -0.04, seed_ + 80)
        elif card == "vest":
            secret_card(k_, -24, bt + 44, 0.85, -0.06, seed_ + 80)
    kit.BADGE_HOOK = hook
    try:
        if not isinstance(pose, str):
            kit.ARM_POSES["_ss"] = pose
            pose = "_ss"
        out = kit.person(k, "DON", x, feet, s, pose=pose, face=face, seed=seed, look=look, badge=True)
    finally:
        kit.ARM_POSES.pop("_ss", None)
        kit.PEOPLE["DON"] = old_p
        kit.BADGE_HOOK, kit.face_draw, dt.SMUG_FIX = old_hook, old_face, old_fix
    if hat:
        santa_hat(k, x + 2 * s, feet + (HY - 32) * s, 1.12 * s, hat_bounce, seed + 5)
    if pose_in == POSE_SMOOTH and CLEAN:              # animatic v2: his forearm rises beside the head to the palm
        hx, hy = out["hands"][1]
        ex, ey = x + 58 * s, feet + (HY + 34) * s
        for wd, col in ((17 * s, INK), (13 * s, dv.SHIRT)):
            c.set_source_rgb(*col); c.set_line_width(wd); c.set_line_cap(1)
            c.move_to(ex, ey); c.line_to(hx + 6 * s, hy + 2 * s); c.stroke()
    if pose_in == POSE_SMOOTH:                        # v2: the palm lies flat on the dome, drawn over the head
        hx, hy = out["hands"][1]
        c.save(); c.translate(hx, hy); c.rotate(-0.25); c.scale(s, s)
        ellipse(k, 0, 0, 15, 8.5, SKIN, seed + 83, shadow=False, lw=2)
        c.set_source_rgb(*INK); c.set_line_width(1.2)
        for d in (-6, -1, 4):
            c.move_to(d - 8, -2); c.line_to(d - 1, -2); c.stroke()
        c.restore()
    if card == "hand":
        hx, hy = out["hands"][1]
        secret_card(k, hx + 4 * s, hy - 22 * s, 1.15 * s, 0.12, seed + 81)
        ellipse(k, hx, hy, 10 * s, 10 * s, SKIN, seed + 82, shadow=False, lw=2 * s)
    if glint:                                         # 6: the dome glints under his palm
        gx, gy = (x + 22 * s, feet + (HY - 14) * s) if hat else (x - 14 * s, feet + (HY - 40) * s)
        c.save(); c.translate(gx, gy); c.scale(s, s)
        c.move_to(0, -12); c.line_to(2.5, -2.5); c.line_to(12, 0); c.line_to(2.5, 2.5); c.line_to(0, 12)
        c.line_to(-2.5, 2.5); c.line_to(-12, 0); c.line_to(-2.5, -2.5); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.4); c.stroke()
        c.restore()
    out["head"] = (x, feet + HY * s)
    return out
