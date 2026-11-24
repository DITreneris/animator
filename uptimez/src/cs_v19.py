"""ONE STAR v19 (shot list v19, 23 Nov, R2): five close-ups, two over-the-shoulder shots, a foreground layer from the
set's own edges (with parallax on moves), the 7 insert back (4.3s), Pam's STOP palm with in-betweens. Opt-in:
install() wraps cs_board.S in every scene module; with it off, every scene draws as v7.
  CAMS19     shot -> the new static camera (from the v7 log: the subject's face in set coordinates, its size wanted)
  OTS19      shot -> (who leaves the cast, the back's frame x, y, scale)
  FG19       shot -> the foreground pieces, in frame coordinates, drawn after the people"""
import sys
import math
import kit
from kit import INK, ellipse, rect, cut

# camera = (x, y, zoom) in set coordinates: zoom = wanted face radius / the face's set radius;
# y puts the face at the wanted frame height (480 is the centre)
def _cam(fx, fy, r_set, r_want, face_y):
    z = r_want / r_set
    return (round(fx, 1), round(fy - (face_y - 480) / z, 1), round(z, 3))


CAMS19 = {
    "2.1": _cam(452.0, 643.6, 30.0, 110, 380),          # MCU, Don on the phone
    "3.5": _cam(247.9, 608.2, 26.0, 140, 420),          # CU, "Is this a joke?"
    "3.5b": _cam(452.0, 643.2, 30.0, 140, 420),         # CU, Don's panic
    "4.3a": _cam(277.9, 608.6, 26.0, 105, 330),         # MCU, the 7 at his chest
    "6.6a": _cam(452.0, 639.2, 30.0, 110, 360),         # MCU, Don proud
    "3.3": (428.8, 673.1, 2.83),                         # OTS onto Don and the sheet
    "4.1": (190.0, 677.5, 3.33),                         # OTS onto Pam
}
PAN19 = {"2.1": ((622, 474, 2.62), (404, 693, 3.1))}      # (start, the v7 end): v19 ends on the MCU instead
OTS19 = {"3.3": ("cl", 100, 740, 1.8, -1), "4.1": ("cl", 505, 790, 1.6, 1)}   # 4.1: air between her palm and his back
N42_19 = 32                                                 # 4.2 at 2.7 s (was 2.0): "MY GARAGES" hard to read (cold test v8)   # the Client's back: x, y, scale, side
FG19 = {
    "1.4": [("desk", "left")], "3.1": [("sheet",)], "3.2": [("door", "left")], "4.2b": [("door", "left")],
    "4.4": [("plant", "left")], "5.1": [("plant", "right")], "5.4c": [("counter",)], "6.5": [("counter",)],
    "6.6a": [("counter",)], "2.1": [("plant", "right")], "4.3a": [("door", "left")],
}
COUNTER_Y = {"5.4c": 690, "6.5": 700, "6.6a": 800}                  # the counter top per shot: over the legs, so they stand behind it
PARALLAX = 0.3                                              # the foreground moves 1.3x the set on a camera move
ON = [False]
LAST = [None]                                               # the camera the last S drew with (the gates read it)
CAM0 = {}                                                   # shot -> its first drawing's camera (for parallax)


def _shot():
    import cs_hands as ch
    return ch.SHOT[0]


def _d():
    import cs_scene1 as s1
    return s1.CUR_D[0]


# ---- the foreground pieces (frame coordinates, 540 x 960) ----------------------------------------------------------------

def bezel(k, side, dx=0):
    """a monitor's edge, close to the lens: a dark rounded frame, its glass catching the room's light."""
    c = k.c
    x = -60 + dx if side == "left" else 490 + dx
    rect(k, x, 650, 110, 330, (0.10, 0.11, 0.14), 1901, shadow=False, lw=3)                 # the bezel's corner
    c.set_source_rgb(0.16, 0.20, 0.28); c.rectangle(x + (16 if side == "left" else 14), 668, 76, 330); c.fill()   # its glass
    c.set_source_rgba(0.55, 0.75, 0.95, 0.45); c.set_line_width(6)
    c.move_to(x + 30, 700); c.line_to(x + 80, 660); c.stroke()                               # a glint
    rect(k, x - 30 if side == "left" else x - 20, 940, 160, 40, (0.10, 0.11, 0.14), 1902, shadow=False, lw=3)   # its stand


def desk(k, side, dx=0):
    """the corner of a desk, near the lens, and a mug on it with the company's mark: a room, not a block."""
    c = k.c
    sg = 1 if side == "left" else -1
    x0 = (-20 if sg > 0 else 560) + dx
    pts = [(x0, 780), (x0 + sg * 190, 800), (x0 + sg * 230, 980), (x0, 980)]
    cut(k, pts, (0.56, 0.40, 0.26), shadow=False, lw=3)                                     # the desk top, wood
    c.set_source_rgb(0.66, 0.50, 0.34); c.new_path(); c.move_to(x0, 784); c.line_to(x0 + sg * 190, 804)
    c.line_to(x0 + sg * 192, 816); c.line_to(x0, 798); c.close_path(); c.fill()                # its lit edge
    mx = x0 + sg * 100                                                                       # the mug
    rect(k, mx - 34, 700, 68, 92, (0.97, 0.97, 0.95), 1906, shadow=False, lw=3)
    c.set_source_rgb(*INK); c.set_line_width(3); c.new_path(); c.arc(mx + sg * 40, 744, 18, -1.3, 1.3) if sg > 0 else c.arc_negative(mx - 40, 744, 18, math.pi + 1.3, math.pi - 1.3); c.stroke()
    c.set_source_rgb(0.20, 0.70, 0.45); c.set_line_width(5); c.set_line_cap(1)               # its green tick mark
    c.move_to(mx - 14, 744); c.line_to(mx - 4, 756); c.line_to(mx + 16, 728); c.stroke(); c.set_line_cap(0)
    ellipse(k, mx, 702, 34, 8, (0.36, 0.22, 0.12), 1907, shadow=False, lw=2.5)              # coffee


def door(k, side, dx=0):
    """the door frame, near: a tall strip at the frame's edge, its shadow side toward the room."""
    c = k.c
    x = -30 + dx if side == "left" else 480 + dx
    cut(k, [(x, -20), (x + 80, -20), (x + 80, 980), (x, 980)], (0.38, 0.42, 0.48), shadow=False, lw=3)
    c.set_source_rgba(0, 0, 0, 0.25); c.rectangle(x + (62 if side == "left" else 0), -20, 18, 1000); c.fill()


def plant(k, side, dx=0):
    """a desk plant's leaves rising from the bottom corner, out of focus by being big and simple."""
    c = k.c
    bx = (-10 if side == "left" else 550) + dx
    sgn = 1 if side == "left" else -1
    for i, (ang, ln, w) in enumerate(((-1.25, 300, 54), (-0.85, 340, 60), (-0.45, 250, 50), (-1.6, 230, 44))):
        a = ang if sgn > 0 else math.pi - ang
        tx, ty = bx + math.cos(a) * ln, 980 + math.sin(a) * ln
        nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
        mx, my = (bx + tx) / 2, (980 + ty) / 2
        c.new_path(); c.move_to(bx, 980)
        c.curve_to(mx + nx, my + ny, tx + nx * 0.3, ty + ny * 0.3, tx, ty)
        c.curve_to(tx - nx * 0.3, ty - ny * 0.3, mx - nx, my - ny, bx, 980); c.close_path()
        c.set_source_rgb(*((0.20, 0.42, 0.26) if i % 2 else (0.26, 0.50, 0.30))); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        c.set_source_rgba(0, 0, 0, 0.25); c.set_line_width(2); c.move_to(bx, 980); c.line_to(tx, ty); c.stroke()


def counter(k, dx=0):
    """the front desk's top edge, near: a band across the bottom."""
    c = k.c
    y = COUNTER_Y.get(_shot(), 760)
    rect(k, -20 + dx, y, 580, 980 - y, (0.62, 0.48, 0.34), 1903, shadow=False, lw=3)          # over their legs: near
    c.set_source_rgb(0.74, 0.60, 0.44); c.rectangle(-20 + dx, y + 4, 580, 18); c.fill()
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(-20 + dx, y + 22, 580, 10); c.fill()


def sheet(k, dx=0):
    """the printed sheet's curl, close: its glossy blue edge rolled at the bottom."""
    c = k.c
    c.save(); c.translate(150 + dx, 930); c.rotate(-0.12)
    rect(k, -230, -40, 460, 110, (0.22, 0.46, 0.86), 1904, shadow=False, lw=3)
    ellipse(k, -230, 15, 22, 55, (0.30, 0.56, 0.94), 1905, shadow=False, lw=3)
    c.set_source_rgba(1, 1, 1, 0.35); c.rectangle(-200, -28, 400, 8); c.fill()
    c.restore()


PIECES = {"desk": desk, "bezel": bezel, "door": door, "plant": plant, "counter": counter, "sheet": sheet}


def _fg(k, shot, cam):
    dx = 0.0
    if shot in CAM0 and cam and CAM0[shot] != tuple(cam):
        dx = -(cam[0] - CAM0[shot][0]) * cam[2] * PARALLAX                       # parallax: 0.3 more than the set
        dx = max(-20.0, min(20.0, dx))                                              # (and it never leaves the frame)
    for p in FG19.get(shot, ()):
        k.c.save(); k.c.identity_matrix()                                   # (the device scale stays: lesson 162)
        PIECES[p[0]](k, *p[1:], dx=dx)
        k.c.restore()


def _back(k, x, y, s, side):
    import fs_storyboard as sb
    c = k.c
    c.save(); c.identity_matrix()
    if side < 0:
        c.translate(x, 0); c.scale(-1, 1); c.translate(-x, 0)
    sb._client_back(k, x, y, s)
    c.restore()


def install():
    import importlib
    import cs_board
    real = getattr(cs_board, "_S_real", cs_board.S)
    cs_board._S_real = real

    def S(k, cam, *a, **kw):
        shot = _shot()
        if not ON[0] or shot is None:
            return real(k, cam, *a, **kw)
        if shot in PAN19:                                                           # the move kept, its end moved in
            a_, b_ = PAN19[shot]
            u = (cam[0] - a_[0]) / float(b_[0] - a_[0]) if b_[0] != a_[0] else 1.0
            u = max(0.0, min(1.0, u))
            cam = tuple(x + (y - x) * u for x, y in zip(a_, CAMS19[shot]))
        elif shot in CAMS19:
            cam = CAMS19[shot]
        if _d() == 0 or shot not in CAM0:
            CAM0.setdefault(shot, tuple(cam))
            if _d() == 0:
                CAM0[shot] = tuple(cam)
        LAST[0] = tuple(cam)
        if shot in OTS19:
            kw[OTS19[shot][0]] = False                                             # he is the shoulder, not a person in it
        out = real(k, cam, *a, **kw)
        if shot in OTS19:
            _, x, y, s, side = OTS19[shot]
            _back(k, x, y, s, side)
        _fg(k, shot, cam)
        return out
    for i in range(1, 7):
        importlib.import_module("cs_scene%d" % i)
    import cs_scene4 as s4
    import cs_hands as ch
    if not any(x[0] == "4.3s" for x in s4.SHOTS):                                     # the 7 insert, after his freeze
        i = [x[0] for x in s4.SHOTS].index("4.3a") + 1
        s4.SHOTS.insert(i, ("4.3s", s4.N43s, s4.s4_3s))
    ch._BYFN.clear()
    s4.FACE43A[0] = "puzzled"                                                          # 4.3a: "...oh", not fear
    import cs_scene5 as s5
    s5.SLEEVE52[:] = [0.72, 230]                                                      # 5.2: her purple sleeve in frame (cold test v8)
    if not any(x[0] == "4.2" and x[1] == N42_19 for x in s4.SHOTS):                    # 4.2: the plan held longer to be read
        i = [x[0] for x in s4.SHOTS].index("4.2")
        s4.SHOTS[i] = ("4.2", N42_19, s4.SHOTS[i][2])
    for m in list(sys.modules.values()):
        if getattr(m, "S", None) is real:
            m.S = S
    ON[0] = True
