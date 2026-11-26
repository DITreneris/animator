"""The hand class sheet v4 as an opt-in film module (Tomas 26 Nov, series hands/phones audit v1, /grill-me: "yes, an
opt-in module"). The canon is DITreneris/uptimez: docs/rules-hands-and-phones.md and the sheet
the-blueprint/rough_work/pic_hands/bp_hand_classes_v4.png, whose ACCEPTED table says grab v2, pinch v2, phone_grip v4b.
The drawings below are copied (phone_grip v4b only behind PHONE_V4B, off by default: films keep the old grip) from that repo's src/bp_hand_sheet_v2.py (_grab, _pinch, _fist) and
src/bp_hand_sheet_v4.py (_phone_b), changed only to sit at a film's hand point and forearm direction.

Nothing changes until a film calls enable(): hands_ps.draw and of_cast.phone_grip are the old functions again after
disable(), and a film that never imports this module draws byte for byte as before.

New rows (to be added to the canon page, written before any film draws them):
  board_two(k, cx, cy, w, h, ang, s, skin_l, skin_r, draw_board)  a board, tablet, card or printout in two hands: one
                                                                 clutch at each upper corner, the board drawn first
  tap_insert(k, x, y, edge, w, skin, cuff)                      an insert's tap: point_t with a wrist stub out of the
                                                                 nearest frame edge (rules: "at the frame's edge")
"""
import math
import cairo
import kit
import hands_ps as hp
import of_cast as oc

INK = hp.INK
ROWS = ("grab", "pinch", "fist")
_ORIG = {}


def _side(arm):
    return -1 if arm < 0 else 1


def _round_block(c, x0, y0, x1, y1, r, skin):
    c.new_path()
    c.move_to(x0 + r, y0); c.line_to(x1 - r, y0); c.arc(x1 - r, y0 + r, r, -math.pi / 2, 0)
    c.line_to(x1, y1 - r); c.arc(x1 - r, y1 - r, r, 0, math.pi / 2); c.line_to(x0 + r, y1)
    c.arc(x0 + r, y1 - r, r, math.pi / 2, math.pi); c.line_to(x0, y0 + r); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
    c.close_path()
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(hp.LW); c.stroke()


def _grab(c, w, skin, arm):
    """sheet v2: one C, index longest, little finger shortest, the thumb clear"""
    s_ = _side(arm); t = 0.22 * w
    hp._wrist(c, w, skin)
    hp._blob(c, 0.22 * w, 0, 0.40 * w, 0.38 * w, skin)
    for reach, fy in ((0.66, 0.46), (0.80, 0.36), (0.92, 0.24), (1.02, 0.10)):
        yr = -s_ * fy * w
        hp._cap(c, [(0.36 * w, yr), (reach * w, yr * 0.35), (reach * 0.78 * w, s_ * 0.02 * w)], t, skin)
    hp._cap(c, [(0.10 * w, s_ * 0.32 * w), (0.48 * w, s_ * 0.50 * w), (0.70 * w, s_ * 0.28 * w)], t * 1.15, skin)


def _pinch(c, w, skin, arm):
    """sheet v2: thumb and index meet at one point, the other three one mass"""
    s_ = _side(arm); t = 0.26 * w; tip = (1.02 * w, s_ * 0.02 * w)
    hp._wrist(c, w, skin)
    hp._blob(c, 0.24 * w, 0, 0.40 * w, 0.36 * w, skin)
    hp._blob(c, 0.46 * w, -s_ * 0.14 * w, 0.20 * w, 0.16 * w, skin)
    hp._crease(c, [(0.34 * w, -s_ * 0.10 * w), (0.58 * w, -s_ * 0.10 * w)])
    hp._crease(c, [(0.36 * w, -s_ * 0.20 * w), (0.56 * w, -s_ * 0.18 * w)])
    hp._cap(c, [(0.42 * w, -s_ * 0.16 * w), (0.78 * w, -s_ * 0.10 * w), tip], t, skin)
    hp._cap(c, [(0.16 * w, s_ * 0.34 * w), (0.62 * w, s_ * 0.26 * w), tip], t * 1.05, skin)


def _fist(c, w, skin, arm):
    """sheet v2: one closed block, the thumb across the front"""
    s_ = _side(arm)
    hp._wrist(c, w, skin)
    x1 = 0.78 * w
    _round_block(c, 0.02 * w, -0.36 * w, x1, 0.36 * w, 0.20 * w, skin)
    hp._crease(c, [(0.22 * w, -0.12 * w), (x1 - 0.06 * w, -0.12 * w)])
    hp._crease(c, [(0.22 * w, 0.12 * w), (x1 - 0.06 * w, 0.12 * w)])
    hp._cap(c, [(0.08 * w, s_ * 0.22 * w), (0.55 * w, s_ * 0.08 * w)], 0.28 * w, skin)
    c.set_source_rgb(*skin)
    c.rectangle(0.04 * w, 0.04 * w if s_ > 0 else -0.22 * w, 0.26 * w, 0.18 * w); c.fill()


DRAW = {"grab": _grab, "pinch": _pinch, "fist": _fist}


def draw(k, g, hx, hy, w, skin, d, arm):
    """hands_ps.draw with the sheet's rows; every other shape is hands_ps's own"""
    if g not in DRAW or hp.GLOVE[0] is not None:
        return _ORIG["draw"](k, g, hx, hy, w, skin, d, arm)
    c = k.c
    a = math.atan2(d[1], d[0])
    arm_eff = arm if math.cos(a) >= 0 else -arm              # the film's thumb side (hands_ps: mirrored per arm)
    c.save(); c.translate(hx, hy); c.rotate(a)
    DRAW[g](c, w, skin, arm_eff)
    c.restore()


def phone_grip(k, x, y, s, screen=None, ang=0.0, skin=oc.SKIN_LIGHT, thumb=None, wrist=None, body_x=None, back=False,
               part="all", ink=1.0, thumb_tip=None):
    """sheet v4b: forearm, palm, the side of the hand and the thumb one silhouette; three fingers of unequal length
    round the far edge. Falls back to the old grip for what v4b does not draw (a tilted phone, parts, a pressing thumb,
    the phone's back)."""
    if ang and abs(ang) < 0.35 and part == "all" and thumb_tip is None and not back:   # a small tilt: the same grip, turned
        c = k.c; c.save(); c.translate(x, y); c.rotate(ang)
        try:
            return phone_grip(k, 0, 0, s, screen=screen, skin=skin, thumb=thumb, body_x=None if body_x is None else body_x - x,
                              ink=ink)
        finally:
            c.restore()
    if ang or part != "all" or thumb_tip is not None or back:
        return _ORIG["phone_grip"](k, x, y, s, screen=screen, ang=ang, skin=skin, thumb=thumb, wrist=wrist, body_x=body_x,
                                   back=back, part=part, ink=ink, thumb_tip=thumb_tip)
    c = k.c
    w = 26.0 * s
    thumb_ = oc.inner_thumb(x, body_x, False) if body_x is not None else (thumb if thumb is not None else -1)
    oc.log_grip(c, "phone", x, y, thumb_, None if body_x is None else oc.inner_thumb(x, body_x, False))
    far = -thumb_
    py = y - 22.0 * s
    oc.phone(k, x, py, s, screen)
    edge = 22.0 * s
    lw = hp.LW
    bend = math.radians(12.0)

    def outside_phone():
        pts = kit.rough_rect_pts(k, -22, -38, 44, 76, 3501)
        c.new_path(); c.rectangle(x - 10 * w, y - 10 * w, 20 * w, 20 * w)
        c.move_to(x + pts[0][0] * s, py + pts[0][1] * s)
        for px_, py_ in pts[1:]:
            c.line_to(x + px_ * s, py + py_ * s)
        c.close_path(); c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.clip(); c.set_fill_rule(cairo.FILL_RULE_WINDING)

    def stroke(pts, t, col):
        c.set_source_rgb(*col); c.set_line_width(t)
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.stroke()

    def oval(cx, cy, rx, ry, col):
        c.save(); c.translate(cx, cy); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*col); c.fill()

    fingers = []
    for fy, ln in ((-34.0, 9.0), (-23.0, 10.5), (-12.0, 8.0)):
        root = (x + far * (edge + 4.0 * s), y + fy * s - 1.5 * s)
        knuckle = (x + far * (edge - 1.0 * s), y + fy * s)
        tip = (knuckle[0] - far * ln * s * math.cos(bend), knuckle[1] + ln * s * math.sin(bend))
        fingers.append([root, knuckle, tip])
    thumb_pts = [(x + thumb_ * 0.40 * w, y + 0.62 * w), (x + thumb_ * (edge - 4.0 * s), y + 12.0 * s),
                 (x + thumb_ * (edge - 10.0 * s), y + 5.0 * s)]
    arm_pts = [(x, y + 1.55 * w), (x, y + 0.40 * w)]
    side_pts = [(x + far * 0.40 * w, y + 0.66 * w), (x + far * (edge + 1.5 * s), y + 0.22 * w),
                (x + far * (edge + 1.5 * s), y - 34.0 * s)]
    tf, tt = 0.27 * w, 0.30 * w
    for inked in (True, False):
        col = INK if inked else skin
        grow = 2 * lw * ink if inked else 0.0
        c.save(); outside_phone()
        stroke(arm_pts, 0.60 * w + grow, col)
        oval(x, y + 0.44 * w, 0.62 * w + grow / 2, 0.42 * w + grow / 2, col)
        stroke(side_pts, 8.0 * s + grow, col)
        c.restore()
        for pts in fingers:
            stroke(pts, tf + grow, col)
        stroke(thumb_pts, tt + grow, col)
    c.set_line_cap(cairo.LINE_CAP_BUTT); c.set_line_join(cairo.LINE_JOIN_MITER)


def board_two(k, cx, cy, bw, bh, ang, w, skin_l, skin_r, draw_board):
    """row board_two: the board (card, tablet, printout) drawn by draw_board(k) centred at (cx, cy), then one clutch at
    each upper corner (the back of the hand on top, four fingers down over its front, the thumb behind)"""
    c = k.c
    draw_board(k)
    ca, sa = math.cos(ang), math.sin(ang)
    for side, skin in ((-1, skin_l), (1, skin_r)):
        lx, ly = side * (bw / 2 - 0.42 * w), -bh / 2
        oc.clutch(k, cx + lx * ca - ly * sa, cy + lx * sa + ly * ca, w, skin)


def tap_insert(k, x, y, edge, w, skin, cuff=(0.20, 0.22, 0.30)):
    """row tap_insert: point_t whose fingertip is at (x, y), its forearm and a short cuffed wrist stub running out of
    the nearest frame edge ("bottom", "right", "left")"""
    d = {"bottom": (0.0, -1.0), "right": (-1.0, 0.0), "left": (1.0, 0.0)}[edge]
    hx, hy = x - d[0] * 0.95 * w, y - d[1] * 0.95 * w
    c = k.c
    ex, ey = {"bottom": (hx, 1100), "right": (700, hy), "left": (-200, hy)}[edge]
    for col, lw_ in ((INK, 0.62 * w + 2 * hp.LW), (skin, 0.62 * w)):                 # the wrist and forearm to the edge
        c.set_source_rgb(*col); c.set_line_width(lw_); c.set_line_cap(1)
        c.move_to(hx - d[0] * 0.3 * w, hy - d[1] * 0.3 * w); c.line_to(ex, ey); c.stroke()
    cx0, cy0 = hx - d[0] * 0.9 * w, hy - d[1] * 0.9 * w                                 # the cuff
    for col, lw_ in ((INK, 0.90 * w + 2 * hp.LW), (cuff, 0.90 * w)):
        c.set_source_rgb(*col); c.set_line_width(lw_); c.set_line_cap(0)
        c.move_to(cx0, cy0); c.line_to(ex, ey); c.stroke()
    _ORIG.get("draw", hp.draw)(k, "point_t", hx, hy, w, skin, d, 1)


PHONE_V4B = [False]          # Tomas 26 Nov: films keep the old phone grip (v3). v4b's thumb and fingers cover the screen's
                             # edge words (One Star v27, 1:04: "1/5" and "Pam"); the rule is "the thumb off the words"


def enable(phone=None):
    if _ORIG:
        return
    _ORIG["draw"], _ORIG["phone_grip"] = hp.draw, oc.phone_grip
    hp.draw = draw
    if PHONE_V4B[0] if phone is None else phone:
        oc.phone_grip = phone_grip


def disable():
    if not _ORIG:
        return
    hp.draw, oc.phone_grip = _ORIG.pop("draw"), _ORIG.pop("phone_grip")


def sheet(path="/tmp/hands_v4_check.png"):
    """the three rows and the phone, old vs new, at 100 % and a 270-px-scale copy, both arms, two directions"""
    import kit as kit_
    W, H = 1100, 520
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf); c.set_source_rgb(0.97, 0.95, 0.90); c.paint()
    k = kit_.Ctx(c, 0)
    skin = oc.SKIN_LIGHT
    for row, label in enumerate(("hands_ps (old)", "hands_v4 (sheet)")):
        if row == 1:
            enable()
        y = 80 + row * 230
        c.set_source_rgb(0, 0, 0); c.select_font_face("Inter"); c.set_font_size(15); c.move_to(10, y - 50); c.show_text(label)
        x = 60
        for g in ROWS:
            for arm, d in ((-1, (1, 0)), (1, (-1, 0)), (1, (0.3, -1))):
                hp.draw(k, g, x, y, 34, skin, d, arm); x += 70
        oc.phone_grip(k, x + 30, y + 40, 1.1, body_x=x - 40)
        if row == 1:
            disable()
    surf.write_to_png(path)
    return path


if __name__ == "__main__":
    print(sheet())
