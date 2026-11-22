"""Daddy's Home: the poses the script needs that no rig had (pose sheet v4). Designs are unchanged; these are new poses and
states, each drawn on the existing rigs.
- don_seated(k, x, floor, s, chair, sunk): Don in the throne. Up: leaning back, hands behind his head, feet crossed on
  the shredder. sunk: the seat on the floor, his knees at his chin, hands gripping the arms.
- don_zipped(k, x, feet, s, ...): the fleece vest zipped to his chin (8.3 to the end).
- don_block(k, x, feet, s): palms out, in front of the throne (10.6).
- Father "low": chin down, eyes up from under his brows (dh_cast.father, face="low").
- dh_cast.guard(pose=ATTENTION): the snap to attention (10.4b).
- visitor_brush(), visitor_invoice(): the repairman's two hand poses.
- robot_state(k, x, feet, s, state): "rec", "tick", "turn", "lean_l", "lean_r".
  python3 dh_poses.py -> ../daddys-home/dh_poses_v4.png"""
import math
import cairo
import kit
import don_v4 as dv
import client_ob as co
import robot_mf as rm
import fs_storyboard as sb
import dh_cast as dc
import dh_props as dp
from kit import Ctx, INK, cut, rect, ellipse
from cand_bc import ik

KHAKI = dv.KHAKI
SHOE = (0.36, 0.23, 0.14)
BT = -(300 * 1.12 - 78)                                    # Don's body top, from his feet
WAIST = BT + 150


def _leg(k, pts, w, seed):
    """A trouser leg along pts (hip, knee, ankle), w wide."""
    c = k.c
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        ang = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], KHAKI, shadow=False, lw=2)
    kx, ky = pts[1]
    ellipse(k, kx, ky, w / 2, w / 2, KHAKI, seed, shadow=False, lw=2)


def _shoe(k, x, y, s, ang, seed):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-9, -15), (9, -15), (12, 12), (-12, 12)], SHOE, shadow=False, lw=2)      # the sole, towards us
    c.set_source_rgb(0.20, 0.12, 0.07); c.set_line_width(1.6)
    for yy in (-6, 0, 6):
        c.move_to(-8, yy); c.line_to(8, yy); c.stroke()
    c.restore()


def don_seated(k, x, floor, s, sunk=False, face=None, look=(1, 0), chair=True, puff=False, hang=False, freeze=False,
               phone=None):
    """(x, floor): the middle of the throne's base. Draws the throne, then Don in it. Returns Don's kit points."""
    c = k.c
    cs = s                                                  # the throne at Don's scale
    # v5 (scene 1 v2): hang: only the SEAT has dropped; the back, the crown and the arms stay, and he hangs by his elbows.
    # freeze: the smile stuck, the eyes wide, the pupils small (0.2a, second drawing). phone: "ring" draws it on the arm.
    if chair:
        ch = dp.ceo_chair(k, x, floor, cs, sink=1.0 if (sunk and not hang) else 0.0, puff=puff, seat_drop=1.0 if hang else 0.0)
        if phone:
            ax, ay = x + 94 * cs, floor - 180 * cs
            c.save(); c.translate(ax, ay - 3 * cs); c.rotate(-0.12)
            rect(k, -9 * cs / 0.6, -4 * cs / 0.6, 18 * cs / 0.6, 7 * cs / 0.6, (0.06, 0.06, 0.08), 3290, shadow=False, lw=1.6)
            c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-7 * cs / 0.6, -4 * cs / 0.6, 14 * cs / 0.6, 2.2 * cs / 0.6); c.fill()
            c.restore()
            c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)
            for sx in (-1, 1):
                for i in (0, 1):
                    c.new_path(); c.arc(ax, ay - 2, (17 + i * 6) * cs / 0.6, (0 if sx > 0 else math.pi) - 0.5, (0 if sx > 0 else math.pi) + 0.5); c.stroke()
    seat_y = floor - (110 - (46 if sunk else 0)) * cs + 4 * s
    feet = seat_y - WAIST * s                               # where his feet would be if he stood: the waist lands on the seat
    c.save(); c.rectangle(x - 200 * s, seat_y - 400 * s, 400 * s, 400 * s + 2); c.clip()      # nothing of him below the seat
    if sunk and hang:
        pose, fc = (-96, 34, 96, -34), (face or "panic")     # elbows out on the armrests, the hands hanging
    elif sunk:
        pose, fc = (-38, -8, 38, 8), (face or "panic")
    else:
        pose, fc = (-150, -110, 150, 110), (face or "happy")   # hands behind his head
    o = sb.don(k, x, feet, s, pose, fc, look=look)
    if freeze:                                              # over the smile's closed eyes: wide, the pupils pin-small
        hx, hy = o["head"]
        for sx in (-17, 17):
            ellipse(k, hx + sx * s, hy + 4 * s, 12.5 * s, 12.5 * s, (1, 1, 1), 3280 + sx, shadow=False, lw=2)
            ellipse(k, hx + sx * s + 3 * s, hy + 5 * s, 2.4 * s, 2.4 * s, INK, 3283 + sx, shadow=False, outline=False)
        c.set_source_rgb(0.62, 0.84, 0.95)
        c.save(); c.translate(hx + 34 * s, hy - 26 * s); c.scale(s, s)
        c.move_to(0, -9); c.curve_to(7, 0, 6, 7, 0, 7); c.curve_to(-6, 7, -7, 0, 0, -9); c.close_path(); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke(); c.restore()
    c.restore()
    c.save(); c.translate(x, seat_y); c.scale(s, s)
    if sunk:                                                # knees up at his chin, feet flat on the floor in front
        fl = (floor - seat_y) / s
        for sx, sd in ((-1, 3201), (1, 3202)):
            _leg(k, [(sx * 20, -6), (sx * 34, -92 if not hang else -122), (sx * 40, fl - 10)], 30, sd)
            cut(k, [(sx * 40 - 18, fl - 14), (sx * 40 + 18, fl - 14), (sx * 40 + 22, fl), (sx * 40 - 22, fl)], SHOE, shadow=False, lw=2)
    else:                                                   # legs out to the right, ankles crossed on the shredder
        _leg(k, [(14, -8), (92, -22), (176, -58)], 30, 3203)
        _leg(k, [(-10, -8), (82, -6), (172, -40)], 30, 3204)
        _shoe(k, 186, -62, 1.5, 0.35, 3205); _shoe(k, 184, -36, 1.5, 0.20, 3206)
    c.restore()
    return o


def don_zipped(k, x, feet, s, pose="stand", face="neutral", look=(0, 0)):
    """The vest zipped to his chin: the collar stands up over his neck, the zip pull right under his mouth. The ketchup
    stain is under it now (Mom scrubbed it first)."""
    o = sb.don(k, x, feet, s, pose, face, look=look)
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    cut(k, [(-17, BT + 2), (17, BT + 2), (19, WAIST + 2), (-19, WAIST + 2)], dv.VEST, shadow=False, lw=2)     # closed over the shirt
    cut(k, [(-30, BT + 20), (-25, BT - 1), (25, BT - 1), (30, BT + 20)], dv.VEST, shadow=False, lw=2.2)      # the collar, up under his mouth
    c.set_source_rgb(*dv.ZIP); c.set_line_width(3.2); c.set_line_cap(1)
    c.move_to(0, BT + 1); c.line_to(0, WAIST); c.stroke()
    rect(k, -3.5, BT - 2, 7, 12, dv.ZIP, 3210, shadow=False, lw=1.4)                                         # the pull, at the top
    c.restore()
    return o


def don_block(k, x, feet, s, face="panic", look=(-1, 0), zipped=True):
    """Palms out at shoulder height: he is in the way. Not arms wide."""
    pose = (-74, -86, 74, 86)
    o = (don_zipped if zipped else sb.don)(k, x, feet, s, pose, face, look=look)
    skin = kit.PEOPLE["DON"]["skin"]
    c = k.c
    for hx, hy in o["hands"]:
        c.save(); c.translate(hx, hy); c.scale(s, s)
        cut(k, [(-13, -16), (13, -16), (15, 12), (-15, 12)], skin, shadow=False, lw=2)       # the palm, towards us
        for i in range(4):
            rect(k, -13 + i * 6.8, -30, 6, 16, skin, 3220 + i, shadow=False, lw=1.6)
        c.restore()
    return o


ATTENTION = (-5, 2, 5, -2)


def visitor_brush(k, x, feet, s, look=(0.6, 0.2)):
    pose = (-6, 3) + ik(co.SH[0], co.BT + 26, 96, co.BT + 34, co.LN1, co.LN2, 1)
    o = dc.repairman(k, x, feet, s, pose=pose, case=False, look=look)
    hx, hy = o["hands"][1]
    dc.brush(k, hx + 24 * s, hy - 26 * s, 1.6 * s, -0.9)
    for dx, dy in ((8, -12), (16, -2)):                     # two fingers on it
        ellipse(k, hx + dx * s, hy + dy * s, 9 * s, 7 * s, co.SKIN, 3230 + dx, shadow=False, lw=1.8)
    return o


def visitor_invoice(k, x, feet, s, look=(1, 0)):
    pose = (-6, 3) + ik(co.SH[0], co.BT + 26, 150, co.BT + 96, co.LN1, co.LN2, 1)
    o = dc.repairman(k, x, feet, s, pose=pose, case=False, look=look)
    hx, hy = o["hands"][1]
    c = k.c
    c.save(); c.translate(hx + 30 * s, hy - 22 * s); c.rotate(0.10); c.scale(s, s)
    rect(k, -32, -44, 64, 88, (0.99, 0.98, 0.94), 3240, lw=2)
    kit.text(k, "INVOICE", 0, -26, 11.5, INK)
    dc.cup_logo(c, 0, -6, 7, col=(0.16, 0.16, 0.19))
    kit.text(k, "€80", 0, 28, 22, (0.80, 0.12, 0.12))
    c.restore()
    return o


def robot_state(k, x, feet, s, state="rec"):
    """rec: a red REC dot and a shutter flash (7.3b). tick: the green tick (9.5). turn: its head turned to the throne
    (10.5a). lean_l / lean_r: leaning to look past Don, still smiling (10.6)."""
    c = k.c
    tilt = {"lean_l": -0.24, "lean_r": 0.24}.get(state, 0.0)
    pose = (tilt, 0, 0, (-8, 0), (8, 0))
    look = {"turn": (1, 0), "lean_l": (0.6, 0), "lean_r": (0.6, 0)}.get(state, (0, 0))
    o = rm.robot(k, x, feet, s, pose, "eager", look, 1, head_dx=(14 if state == "turn" else None),
                 head_rot=(None if state != "turn" else 0.0))
    sx, sy = o["screen"]
    r = 50 * s
    if state == "rec":
        ellipse(k, sx + 1.25 * r, sy - 0.95 * r, 0.20 * r, 0.20 * r, (0.90, 0.10, 0.10), 3250, shadow=False, lw=1.6)
        c.set_source_rgb(0.90, 0.10, 0.10); c.select_font_face("Inter", 0, 1); c.set_font_size(0.36 * r)
        c.move_to(sx + 1.55 * r, sy - 0.82 * r); c.show_text("REC")
        c.set_source_rgb(*INK); c.set_line_width(max(1.6, 0.05 * r)); c.set_line_cap(1)        # the shutter's flash
        for a in (-2.6, -2.2, -1.8):
            c.move_to(sx + math.cos(a) * 1.25 * r, sy + math.sin(a) * 1.25 * r); c.line_to(sx + math.cos(a) * 1.6 * r, sy + math.sin(a) * 1.6 * r); c.stroke()
    if state == "tick":
        ellipse(k, sx, sy, 0.80 * r, 0.62 * r, (0.06, 0.20, 0.10), 3251, shadow=False, lw=1.6)
        c.set_source_rgb(0.25, 0.90, 0.40); c.set_line_width(0.16 * r); c.set_line_cap(1); c.set_line_join(1)
        c.move_to(sx - 0.34 * r, sy); c.line_to(sx - 0.08 * r, sy + 0.26 * r); c.line_to(sx + 0.38 * r, sy - 0.26 * r); c.stroke()
    return o


def sheet(out="../daddys-home/dh_poses_v4.png"):
    Wd, Hd = 2000, 1560
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(*kit.WALL); c.paint()
    k = Ctx(c, 0)
    kit.text(k, "DADDY'S HOME · POSES · v4 · new poses on the existing rigs; no design changed", Wd / 2, 44, 32, INK)
    Z = 1.6
    S = 0.60 * Z

    def cap(x, y, a, b):
        kit.text(k, a, x, y, 21, INK); kit.text(k, b, x, y + 26, 15, INK, font=kit.MONO)
    for fy in (700, 1440):
        c.set_source_rgb(*kit.FLOOR); c.rectangle(0, fy - 20, Wd, 60); c.fill()
    F1 = 700
    # --- Don
    don_seated(k, 240, F1, S)
    c.save(); c.translate(240 + 186 * S * 0.98, F1); c.scale(S * 1.1, S * 1.1)             # the shredder under his feet
    import acts_ob as ac
    c.restore()
    sh = sb.fd.SHRED
    ac.shredder(k, 240 + 190 * S, F1, 0.88 * Z * 0.72, fill=0.4)
    cap(300, 760, "0.2  DON IN THE THRONE", "feet on the shredder, hands behind his head")
    don_seated(k, 760, F1, S, sunk=True, puff=True)
    cap(760, 760, "0.2  PSSSH", "the seat on the floor, knees at his chin")
    don_zipped(k, 1120, F1, S, face="neutral", look=(-1, 0))
    cap(1120, 760, "8.3 to the end", "the vest zipped to his chin")
    dp.ceo_chair(k, 1470, F1, S)
    don_block(k, 1470, F1 + 14, S)
    cap(1470, 760, "10.6  IN THE WAY", "palms out, not arms wide")
    for i, (fc, lab) in enumerate((("happy", "the fake smile"), ("panic", "panic"), ("neutral", "frozen (the filter)"))):
        x0 = 1730 + (i % 2) * 150; y0 = 300 + (i // 2) * 250
        c.save(); c.rectangle(x0 - 66, y0 - 150, 132, 150); c.clip()
        o = sb.don(k, x0, y0 + 250, 1.1, "stand", fc, look=(0, 0))
        if fc == "neutral":
            dp.coffee_run(k, o["head"], 1.1); dp.wet_filter(k, o["head"][0], o["head"][1] - 53, 1.5, -0.12)
        c.restore()
        kit.text(k, lab, x0, y0 + 22, 15, INK, font=kit.MONO)
    # --- Father, the bodyguards, the repairman, the robot
    F2 = 1440
    G = 0.56 * Z
    for i, (fc, lab) in enumerate((("hard", "hard"), ("low", "9.2: chin down, eyes up"), ("brow", "10.4a: the eyebrow"))):
        x0 = 120 + i * 190
        dc.father(k, x0, F2, 0.62 * Z, face=fc, look=(0, 0))
        kit.text(k, lab, x0, F2 + 60, 15, INK, font=kit.MONO)
    kit.text(k, "FATHER: three faces, no fourth", 310, F2 + 92, 21, INK)
    dc.guard(k, 760, F2, G); dc.guard(k, 990, F2, G, pose=ATTENTION)
    c.set_source_rgb(*INK); c.set_line_width(3); c.set_line_cap(1)
    for dx in (-22, 22):
        c.move_to(990 + dx, F2 - 452 * G); c.line_to(990 + dx * 1.3, F2 - 482 * G); c.stroke()
    cap(875, F2 + 66, "BODYGUARD: at rest, and the snap (10.4b)", "bare hands; both do it at the same instant")
    visitor_brush(k, 1230, F2, G); visitor_invoice(k, 1470, F2, G)
    cap(1360, F2 + 66, "REPAIRMAN: 7.1c the brush, 7.6 the invoice", "two fingers; €80, unpaid to the end")
    for i, (st_, lab) in enumerate((("rec", "7.3b REC"), ("tick", "9.5 tick"), ("turn", "10.5a turns"), ("lean_l", "10.6 leans"))):
        x0 = 1790 + (i % 2) * 140; y0 = F2 - 300 + (i // 2) * 300
        robot_state(k, x0, y0, 0.40 * Z * 1.1, st_)
        kit.text(k, lab, x0, y0 + 34, 15, INK, font=kit.MONO)
    surf.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    sheet()
