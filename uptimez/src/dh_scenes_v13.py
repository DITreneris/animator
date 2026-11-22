"""Daddy's Home: the scene sheets. One scene at a time, every shot as a real camera frame with its time, its length and
what happens in it, for review BEFORE anything is animated (Tomas, 21 Nov: "detail scenes with shots to review ... one by
one, until we succeed"). Eight scenes; the times are the 95-second plan's.
  python3 dh_scenes.py 1  -> ../daddys-home/dh_scene1_v1.png"""
import os
import sys
import cairo
import kit
import fs_storyboard as sb
import dh_cast as dc
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_animatic as da
from kit import Ctx, INK

F = sb.F
CH = dp.CHAIR
SCENES = {1: "THE CALL", 2: "GOOD NEWS", 3: "THE GREEN STAR", 4: "THE WRONG MAN", 5: "THE FILTER", 6: "MOM", 7: "THE ARRIVAL",
          8: "FIND MY MONEY"}


def _phone_in_hand(k, d, lit=True, side=1, at_ear=False):
    hx, hy = d["hands"][1 if side > 0 else 0]
    c = k.c
    if at_ear:                                             # flat against the side of his head, the hand over it
        hx, hy = d["head"][0] + 31, d["head"][1] + 2
        kit.ellipse(k, hx + 3, hy + 9, 8, 9, kit.PEOPLE["DON"]["skin"], 3402, shadow=False, lw=1.6)
    c.save(); c.translate(hx - 4 if not at_ear else hx, hy - 8 if not at_ear else hy - 6); c.rotate(-0.25 if not at_ear else 0.12)
    kit.rect(k, -7, -14, 14, 27, (0.06, 0.06, 0.08), 3401, lw=1.6)
    if lit:
        c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-5, -11, 3, 21); c.fill()
    c.restore()


def _don_call(face, lit=True, lowered=False, sunk_chair=True):
    def f(k, o):
        dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0 if sunk_chair else 0.0)
        pose = (-8, 0, 128, 124) if not lowered else (-8, 0, 40, 70)
        d = sb.don(k, 452, F + 26, 0.60, pose, face, look=(0.3, 0) if not lowered else (0.6, 0.6))
        _phone_in_hand(k, d, lit, at_ear=not lowered)
    return f


SEAT = [1.0]                                               # v2: after 0.2b only the seat is down; the crown is where it was


def _ring_on_arm(k):
    ax, ay = CH[0] + 94 * CH[2], CH[1] - 180 * CH[2]
    c = k.c
    c.save(); c.translate(ax, ay - 3 * CH[2]); c.rotate(-0.12)
    kit.rect(k, -9, -4, 18, 7, (0.06, 0.06, 0.08), 3290, shadow=False, lw=1.6)
    c.set_source_rgb(0.55, 0.80, 1.0); c.rectangle(-7, -4, 14, 2.2); c.fill()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.8); c.set_line_cap(1)
    for sx in (-1, 1):
        for i in (0, 1):
            c.new_path(); c.arc(ax, ay - 2, 17 + i * 6, (0 if sx > 0 else 3.14159) - 0.5, (0 if sx > 0 else 3.14159) + 0.5); c.stroke()


def _don_up(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    _ring_on_arm(k)
    sb.don(k, 452, F + 26, 0.60, "vest", "smug", look=(0.4, 0))


H = dl.hd(452, F + 26, 0.60)
def _seat(**kw):
    def f(k, o):
        import acts_ob as ac
        dq.don_seated(k, CH[0], dl.FLOOR, CH[2], phone="ring", **kw)
        if not kw.get("sunk"):
            ac.shredder(k, CH[0] + 190 * CH[2], dl.FLOOR, 0.62, fill=0.4)
    return f


HS = dl.h_seat()
S1 = [   # id, seconds, frame (an insert name or a shot dict), what happens, the line
    ("0.1", 0.45, "0.1", "INSERT. The phone on the throne's gold arm, already buzzing: DAD. A low, ugly ring.", ""),
    ("0.2a", 0.25, dl.shot("0.2a", [HS], _seat(look=(1, 0.2)), "", chair=False), "MEDIUM. Don in the throne, feet on the shredder, hands behind his head, smiling. His eyes go to the phone.", ""),
    ("0.2a'", 0.35, dl.shot("0.2a2", [HS], _seat(look=(1, 0.2), freeze=True), "", chair=False), "SAME FRAME, the second drawing: THE FREEZE. The smile sticks; the eyes go wide, the pupils small; one drop of sweat. All sound stops.", ""),
    ("0.2b", 0.70, dl.shot("0.2b", [HS], _seat(sunk=True, hang=True, puff=True), "", chair=False), "SAME FRAME. PSSSH: the SEAT drops to the floor. The back, the crown and the arms stay up. He hangs by his elbows, knees at his chin. The king went down; the crown didn't.", ""),
    ("0.2c", 0.45, dl.shot("0.2c", [H], _don_up, "", chair=False), "SAME FRAME. He is up, straight, vest pulled down: nobody saw that. The phone is still ringing on the arm.", ""),
    ("0.3", 1.2, "0.3", "THE BOOTH. A bodyguard's sleeve holds the phone with the one-star post up to him. The ring. No face.", "FATHER: \"Donnie.\""),
    ("0.4", 1.65, dl.shot("0.4", [H], _don_call("happy"), "", chair=False), "CLOSE. The phone at his ear, the sales smile, the first sweat.", "DON: \"Dad! Great timing!\""),
    ("0.5a", 2.0, "0.5", "THE BOOTH. One finger taps the post, once, on \"first\". Nothing else moves.", "FATHER: \"My men go in first.\""),
    ("0.5b", 2.15, dl.shot("0.5b", [H], _don_call("neutral"), "", chair=False), "CLOSE, Don listening. The smile drains off his face while Father's voice goes on, off screen.", "FATHER (off): \"I arrive at five.\""),
    ("0.6", 1.1, dl.shot("0.6", [H], _don_call("confused"), "", chair=False), "CLOSE. The smile is gone. Small.", "DON: \"Tomorrow?\""),
    ("0.7a", 1.2, "0.7", "THE BOOTH. The hand turns the phone face down on the table.", "FATHER: \"Today.\""),
    ("0.7b", 0.45, dl.shot("0.7b", [H], _don_call("panic", lit=False, lowered=True), "", chair=False), "CLOSE. He lowers the phone. The screen is dark. He looks at it.", ""),
]


# ---------------------------------------------------------------- scene 2: GOOD NEWS (beats 1 and 2)
import pam_bc as pb
import sofia_cs as scs
SS, PS = dl.SS, dl.PS
SOF, PAM = (566, F + 4), (652, F + 6)                      # right of Don: every look at him goes left


def _sweat(k, d, n=2):
    c = k.c
    hx, hy = d["head"]
    for dx, dy in ((-16, -34), (20, -30), (30, -6))[:n]:
        c.save(); c.translate(hx + dx, hy + dy); c.scale(0.7, 0.7)
        c.move_to(0, -8); c.curve_to(6, 0, 5, 6, 0, 6); c.curve_to(-5, 6, -6, 0, 0, -8); c.close_path()
        c.set_source_rgb(0.62, 0.84, 0.95); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.5); c.stroke()
        c.restore()


def _lines(k, pts):
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
    for x0, y0, x1, y1 in pts:
        c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()


def s2_stare(k, o):
    scs.sofia(k, SOF[0], SOF[1], SS, "hold", "interested", look=(-1, 0))
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, 0), glasses="up")


def s2_news(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    d = sb.don(k, 452, F + 26, 0.60, (-100, -30, 100, 30), "happy", look=(0.6, 0))
    _sweat(k, d, 2)


def s2_alone(k, o):
    scs.sofia(k, SOF[0], SOF[1], SS, "hold", "interested", look=(-0.8, -0.35))


def s2_dead(k, o):                                        # v2: the smile is gone at once; then the sleeve
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    d = sb.don(k, 452, F + 26, 0.60, (-100, -30, 100, 30), "neutral", look=(0.6, 0))
    _sweat(k, d, 3)


def s2_wipe(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    d = sb.don(k, 452, F + 26, 0.60, (-8, 0, 152, 96), "confused", look=(0.4, 0.5))
    _sweat(k, d, 1)


def s2_reports(k, o):
    q = scs.sofia(k, SOF[0], SOF[1], SS, "chest", "deadpan", look=(-1, 0))
    c = k.c
    hx, hy = min(q["hands"], key=lambda h_: h_[1])
    c.save(); c.translate(hx, hy - 6); c.rotate(-0.06)
    kit.rect(k, -36, -32, 72, 50, (0.86, 0.72, 0.36), 3301, lw=2)
    kit.text(k, "EXPENSES", 0, -3, 11.5, INK)
    c.restore()


def s2_jump(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    sb.don(k, 452, F + 12, 0.60, kit.ARM_POSES["shock"], "panic", look=(1, 0.3))    # off the floor, eyes on the folder
    _lines(k, [(424, F + 22, 414, F + 30), (452, F + 24, 452, F + 34), (480, F + 22, 490, F + 30)])


def s2_hand(k, o):                                        # v2: no lever. Chin up, one hand lands on the throne's arm
    dp.ceo_chair(k, 400, CH[1], CH[2], seat_drop=1.0)
    sb.don(k, 486, F + 26, 0.60, (-78, -16, 8, 0), "smug", look=(1, -0.3))


def s2_push(k, o):                                        # the shove, on purpose: the arm straight, the throne leaving left
    dp.ceo_chair(k, 318, CH[1], CH[2], lean=-0.10, seat_drop=1.0)
    _lines(k, [(392, F - 170, 426, F - 170), (398, F - 130, 432, F - 130), (392, F - 90, 426, F - 90), (396, F - 20, 420, F - 20)])
    sb.don(k, 486, F + 26, 0.60, (-92, 0, 8, 0), "smug", look=(1, 0))


def s2_what(k, o):
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, 0.25), glasses="up")


def s2_peek(k, o):                                        # the button, first drawing: he smiles at Pam; a crown point at the frame's edge
    dp.ceo_chair(k, 318, CH[1], CH[2], lean=0.06, seat_drop=1.0)
    _lines(k, [(240, F - 150, 262, F - 150), (236, F - 110, 258, F - 110)])
    sb.don(k, 486, F + 26, 0.60, "vest", "happy", look=(1, 0))


def s2_caught(k, o):                                      # second drawing: all of it, beside him. The smile is dead
    dp.ceo_chair(k, 404, CH[1], CH[2], seat_drop=1.0)
    _lines(k, [(300, F - 150, 322, F - 150), (296, F - 110, 318, F - 110), (300, F - 30, 322, F - 30)])
    sb.don(k, 486, F + 26, 0.60, "vest", "neutral", look=(-1, 0.2))


HD = dl.hd(452, F + 26, 0.60)
HD2 = dl.hd(486, F + 26, 0.60)
TWO = (430, 694, 2.2)                                      # Don and the throne, the throne to his left
S2 = [
    ("1.2", 2.4, dl.shot("s2b", [HD], s2_news, "", chair=False),
     "MEDIUM. The scene opens on him: arms wide, a grin slightly too big, two drops of sweat. The throne behind him still has its seat on the floor.",
     "DON: \"Good news, everyone! My father's coming!\""),
    ("1.1", 0.4, dl.shot("s2a", [dl.hp(SOF[0], SOF[1], SS), dl.hp(PAM[0], PAM[1], PS)], s2_stare, "", chair=False),
     "TWO-SHOT. Sofía and Pam. Zero enthusiasm. Nobody moves.", ""),
    ("1.3", 1.15, dl.shot("s2c", [dl.hp(SOF[0], SOF[1], SS)], s2_alone, "", chair=False),
     "CLOSE. Her eyes are on the sweat, above his face.", "SOFÍA: \"Is he coming alone?\""),
    ("1.3b", 0.2, dl.shot("s2d0", [HD], s2_dead, "", chair=False),
     "MEDIUM, first drawing. The grin is gone in one frame: a dead stare, arms still out. Silence.", ""),
    ("1.3b'", 0.35, dl.shot("s2d", [HD], s2_wipe, "", chair=False),
     "Second drawing. He wipes his head with his sleeve and looks at the floor. No answer.", ""),
    ("2.1", 0.6, dl.shot("s2e", [dl.hp(SOF[0], SOF[1], SS)], s2_reports, "", chair=False),
     "MEDIUM. She lifts a folder to her chest: EXPENSES. Says nothing.", ""),
    ("2.2", 1.45, dl.shot("s2f", [dl.hd(452, F + 12, 0.60)], s2_jump, "", chair=False),
     "CLOSE. His eyes hit the folder; he is off the floor before she has said a word.", "DON: \"I didn't steal anything!\""),
    ("2.3a", 0.6, dl.shot("s2g", [HD2], s2_hand, "", chair=False, cam=TWO),
     "TWO-SHOT, Don and the throne. Fake confidence, chin up. His hand lands on the throne's arm.", "DON: \"The money...\""),
    ("2.3b", 1.2, dl.shot("s2h", [HD2], s2_push, "", chair=False, cam=TWO),
     "SAME FRAME. Eyes on Sofía, he shoves it, arm straight: it rolls out of frame to the left on a squeaking wheel.", "DON: \"...was invested.\""),
    ("2.4", 1.0, dl.shot("s2i", [dl.hp(PAM[0], PAM[1], PS)], s2_what, "", chair=False, cam=(628, 686.8, 2.889)),
     "CLOSE. Pam, three looks, her eyebrows hardly moving: at Don, at where the throne went, back at Don.", "PAM: \"Into what?\""),
    ("2.5", 0.6, dl.shot("s2j", [HD2], s2_peek, "", chair=False, cam=TWO),
     "TWO-SHOT, first drawing. He gives Pam the confident smile. Behind him, a squeak: the crown slides back into the edge of the frame.", ""),
    ("2.5'", 0.8, dl.shot("s2k", [HD2], s2_caught, "", chair=False, cam=TWO),
     "Second drawing. The whole throne is beside him and bumps his hip. The smile dies; his eyes go to it. HARD CUT.", ""),
]
# ---------------------------------------------------------------- scene 3: THE GREEN STAR (beats 3 and 4)
MS = dl.MS
THR = 404                                                  # where scene 2 left the throne
DON3 = (330, F + 26)                                       # he has walked to the robot's wall screen by the door


def s3_point(k, o):
    rx, ry = o["robot"]["screen"]
    dp.star_screen(k, rx + 6, ry - 92, 124, green=False)
    sb.don(k, DON3[0], DON3[1], 0.60, (-148, -14, 8, 0), "smug", look=(-1, -0.6))


def s3_thumb(k, c):
    c.set_source_rgb(0.86, 0.88, 0.90); c.paint()                                           # the robot's chest plate
    kit.rect(k, 110, 300, 320, 380, (0.10, 0.13, 0.18), 3501, lw=4)
    for r_ in (40, 62, 84, 106):
        c.set_source_rgb(0.30, 0.75, 0.95); c.set_line_width(5); c.new_path(); c.arc(270, 470, r_, 0.4, 2.74); c.stroke()
    da.dp._T(c, "APPROVE", 270, 640, 34, col=(0.80, 0.88, 0.95))
    skin = kit.PEOPLE["DON"]["skin"]
    kit.cut(k, [(560, 520), (420, 470), (300, 430), (262, 446), (270, 500), (400, 560), (560, 640)], skin, lw=4)     # his thumb, from the right
    kit.cut(k, [(280, 436), (306, 430), (316, 458), (288, 468)], (0.98, 0.93, 0.88), shadow=False, lw=2)                # the nail
    kit.cut(k, [(470, 470), (560, 500), (560, 660), (450, 600)], (0.98, 0.98, 0.96), lw=4)                             # the cuff
    for dx, dy in ((500, 540), (520, 566), (486, 572)):                                                                 # the ketchup on it
        kit.ellipse(k, dx, dy, 12, 9, (0.85, 0.16, 0.10), 3510 + dx, shadow=False, lw=1.6)


def s3_green(k, c):                                       # v2: a triumph. One huge green star, four small grey ones; the robot nods
    c.set_source_rgb(0.05, 0.07, 0.10); c.paint()
    da.dp._T(c, "CUSTOMER SATISFACTION", 270, 190, 30, col=(0.80, 0.88, 0.95))
    import math as _m
    def star(cx, cy, r_, col, fill):
        c.new_path()
        for j in range(10):
            a_ = -_m.pi / 2 + j * _m.pi / 5
            rr = r_ if j % 2 == 0 else r_ * 0.45
            (c.move_to if j == 0 else c.line_to)(cx + _m.cos(a_) * rr, cy + _m.sin(a_) * rr)
        c.close_path()
        if fill:
            c.set_source_rgb(*col); c.fill_preserve()
        c.set_source_rgb(*col); c.set_line_width(4); c.stroke()
    star(270, 400, 150, dp.GRN, True)
    for i in range(4):
        star(132 + i * 92, 610, 30, (0.45, 0.50, 0.58), False)
    c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.set_line_cap(1)                  # the chime
    for a_ in (-2.5, -2.1, -1.0, -0.6):
        c.move_to(270 + _m.cos(a_) * 176, 400 + _m.sin(a_) * 176); c.line_to(270 + _m.cos(a_) * 210, 400 + _m.sin(a_) * 210); c.stroke()
    c.save(); c.translate(270, 1400); c.rotate(0.07)                                    # the robot's head at the bottom edge, nodding
    dq.robot_state(k, 0, 0, 2.0, "idle")
    c.restore()


def s3_pam(k, o):
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, -0.35), glasses="up")


def s3_proud(k, o):                                       # v2: a victory pose: one fist up
    sb.don(k, DON3[0], DON3[1], 0.60, (-8, 0, 172, 6), "smug", look=(1, 0))


def _sofia_seated(k, x, floor, cs, face, look):
    """Sofía in the throne (its seat up): the rig cut off at the seat, her skirt over her knees, her shins and heels."""
    c = k.c
    seat_y = floor - 110 * cs + 3
    feet = seat_y + 122 * SS
    c.save(); c.rectangle(x - 150, seat_y - 400, 300, 400 + 2); c.clip()
    q = scs.sofia(k, x, feet, SS, "hold", face, look=look)
    c.restore()
    kit.cut(k, [(x - 30, seat_y - 2), (x + 30, seat_y - 2), (x + 34, seat_y + 22), (x - 34, seat_y + 22)], scs.WINE, shadow=False, lw=2)
    for sx in (-1, 1):
        kit.cut(k, [(x + sx * 14 - 7, seat_y + 22), (x + sx * 14 + 7, seat_y + 22), (x + sx * 13 + 5, floor - 4), (x + sx * 13 - 5, floor - 4)],
                (0.16, 0.15, 0.18), shadow=False, lw=1.8)
        kit.cut(k, [(x + sx * 13 - 9, floor - 6), (x + sx * 13 + 11, floor - 6), (x + sx * 13 + 13, floor + 2), (x + sx * 13 - 9, floor + 2)],
                (0.08, 0.07, 0.08), shadow=False, lw=1.6)
    return q


def _clip(k, x, y, ang):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    kit.rect(k, -13, -17, 26, 34, (0.62, 0.42, 0.24), 3520, lw=1.6)
    kit.rect(k, -10, -13, 20, 27, (0.99, 0.98, 0.95), 3521, shadow=False, lw=1.2)
    c.restore()


def s3_thump(k, o):                                       # Mom knows this chair: one thump on the arm and the seat is back up
    dp.ceo_chair(k, THR, CH[1], CH[2], seat_drop=0.2)
    _lines(k, [(THR - 34, CH[1] - 128 * CH[2], THR - 34, CH[1] - 146 * CH[2]), (THR + 34, CH[1] - 128 * CH[2], THR + 34, CH[1] - 146 * CH[2]),
               (THR - 70, CH[1] - 196 * CH[2], THR - 84, CH[1] - 208 * CH[2]), (THR - 58, CH[1] - 202 * CH[2], THR - 62, CH[1] - 218 * CH[2])])
    sb.mfs.mom(k, 318, F + 8, MS, "wipe", "sweet", look=(0.6, 0.6))


def s3_sits(k, o):
    dp.ceo_chair(k, THR, CH[1], CH[2])
    _sofia_seated(k, THR, CH[1], CH[2], "smile", (-0.6, 0))
    sb.mfs.mom(k, 318, F + 8, MS, "wipe", "sweet", look=(0.6, 0.8))


def s3_up(k, o):                                          # v2: she explodes out of it. She goes up, the clipboard goes left, the throne rolls right
    dp.ceo_chair(k, THR + 62, CH[1], CH[2], lean=0.10)
    _lines(k, [(THR + 2, F - 150, THR + 26, F - 150), (THR - 2, F - 100, THR + 22, F - 100), (THR + 2, F - 40, THR + 26, F - 40)])
    scs.sofia(k, 392, F - 58, SS, "show", "caught", look=(0.4, -0.6), lean=-0.2, tablet_kind="none")
    _clip(k, 318, F - 262, -0.7)
    _lines(k, [(366, F - 8, 356, F + 4), (392, F - 6, 392, F + 8), (418, F - 8, 428, F + 4), (338, F - 240, 350, F - 228)])


def s3_mom(k, o):                                         # v2: the punchline lands on her: frozen where she landed, behind Mom
    dp.ceo_chair(k, 448, CH[1], CH[2])
    scs.sofia(k, 524, F + 4, SS, "show", "caught", look=(-1, 0), lean=0.14, tablet_kind="none")
    _clip(k, 300, F - 6, 1.35)                            # her clipboard, on the floor
    sb.mfs.mom(k, 372, F + 8, MS, "wipe", "sweet", look=(0.5, 0.9))


HM3 = dl.hm(318, F + 8, MS)
HSEAT = (THR, CH[1] - 110 * CH[2] + 3 + 122 * dl.SS - 272 * dl.SS, 50 * dl.SS)
S3 = [
    ("3.1", 1.3, dl.shot("s3a", [dl.hd(DON3[0], DON3[1], 0.60), dl.ROBOT], s3_point, "", rb=True, chair=False),
     "TWO-SHOT. Don has walked to the robot's wall screen by the door: CUSTOMER SATISFACTION, one red star. He points up at it, pleased with his idea.",
     "DON: \"Make it green.\""),
    ("3.2", 1.3, dl.shot("s3b", [da.RH], da._rb("idle"), "", zmax=3.6, chair=False),
     "CLOSE, the robot. The same polite face as always. We cut away before it has finished.", "ROBOT: \"Human approval required.\""),
    ("3.3", 0.5, {"insert": s3_thumb},
     "INSERT. His thumb is on the pad before the robot's last word, the ketchup cuff behind it. He isn't looking.", "DON: \"Approved.\""),
    ("3.3'", 0.8, {"insert": s3_green},
     "INSERT, second drawing. A TRIUMPH: one huge green star, a chime far too happy, the robot's small nod. Four small grey stars beside it. Still one.", ""),
    ("3.4", 1.2, dl.shot("s3c", [dl.hp(PAM[0], PAM[1], PS)], s3_pam, "", chair=False, cam=(628, 686.8, 2.889)),
     "CLOSE. Pam, looking up and left at the screen. Flat.", "PAM: \"It's still one.\""),
    ("3.5", 1.75, dl.shot("s3d", [dl.hd(DON3[0], DON3[1], 0.60)], s3_proud, "", chair=False),
     "CLOSE. Don, one fist up: victory. He means it kindly.", "DON: \"Green is all he sees.\""),
    ("4.1", 0.9, dl.shot("s3e", [HM3], s3_thump, "", chair=False, cam=(366, 700, 2.3)),
     "TWO-SHOT, Mom and the throne. She comes in with her cloth and thumps the gold arm once: PFFT, the seat is back up. She starts to scrub.",
     "MOM: \"He once fired a man...\""),
    ("4.1'", 1.3, dl.shot("s3f", [HM3, HSEAT], s3_sits, "", chair=False, cam=(366, 700, 2.3)),
     "SAME FRAME, second drawing. Sofía walks in and sits down in it to wait, smoothing her skirt. Mom scrubs on without looking up.",
     "MOM: \"...for sitting in that chair.\""),
    ("4.2", 0.9, dl.shot("s3g", [dl.hp(392, F - 58, SS)], s3_up, "", chair=False, cam=(400, 714, 2.3)),
     "SAME FRAME. She EXPLODES out of it: Sofía straight up, the clipboard one way, the throne rolling the other. Real terror.", ""),
    ("4.3", 1.5, dl.shot("s3h", [dl.hm(372, F + 8, MS), dl.hp(524, F + 4, SS)], s3_mom, "", chair=False, cam=(448, 742, 2.2)),
     "TWO-SHOT. Mom has stepped after the throne and is still scrubbing it, eyes on the arm. Behind her Sofía is frozen where she landed. Hold on both.",
     "MOM: \"Different chair.\""),
]
# ---------------------------------------------------------------- scene 4: THE WRONG MAN (beats 5 and 6)
GS = dl.GS
THR4 = 448                                                 # where scene 3 left the throne
LINE = ((400, F + 8), (470, F + 26), (542, F + 4))         # Mom, Don, Sofía, v3: apart, so no face touches another; Don in front of the throne


def s4_door(k, o):
    dc.repairman(k, 128, F + 8, GS, look=(0.6, 0))
    _lines(k, [(86, F - 6, 74, F - 6), (88, F + 4, 72, F + 4)])


def s4_line(k, o):
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    sb.mfs.mom(k, LINE[0][0], LINE[0][1], MS, "stand", "sweet", look=(-1, 0))
    scs.sofia(k, LINE[2][0], LINE[2][1], SS, "hold", "smile", look=(-1, 0))
    sb.don(k, LINE[1][0], LINE[1][1], 0.60, "vest", "happy", look=(-1, 0))
    _lines(k, [(LINE[1][0] - 40, F - 190, LINE[1][0] - 52, F - 198), (LINE[1][0] + 40, F - 190, LINE[1][0] + 52, F - 198)])


def s4_don(k, o):                                         # v3: not the arms-wide of scene 2: one arm sweeps the room open to him
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    sb.don(k, LINE[1][0], LINE[1][1], 0.60, (-104, -24, 30, 10), "happy", look=(-1, 0))


def s4_pam_look(k, o):
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, 0.3), glasses="up")


def s4_pam_cup(k, o):
    q = pb.pam(k, PAM[0], PAM[1], PS, (-8, 0, 60, 110), "neutral", look=(0.2, 0.9), glasses="up")
    c = k.c
    hx, hy = q["hands"][1]
    c.save(); c.translate(hx + 4, hy - 14); c.rotate(2.75)                    # her mug, upside down: nothing comes out
    c.set_source_rgb(*INK); c.set_line_width(3); c.new_path(); c.arc(11, 0, 7, -1.3, 1.3); c.stroke()
    kit.cut(k, [(-10, -12), (10, -12), (9, 12), (-9, 12)], (0.36, 0.62, 0.80), shadow=False, lw=2)
    kit.ellipse(k, 0, -12, 10, 3.2, (0.15, 0.12, 0.10), 3551, shadow=False, lw=1.6)
    c.restore()


TOUR = ((474, F + 26), (378, F + 8))                       # v2: Don in front of the shredder (and the throne); the visitor facing them
SHRED_X = 514


def _sticker(k, x, feet, s_=None):
    """The PREMIUM sticker Don slaps on him: gold, big, over his COFFEE SERVICE pass. It stays on to the end."""
    import math as _m
    s_ = s_ or GS
    c = k.c
    cx, cy = x - 10 * s_, feet + (co_BT + 80) * s_
    pts = []
    for i in range(24):
        a_ = 2 * _m.pi * i / 24
        r_ = (46 if i % 2 else 39) * s_
        pts.append((cx + _m.cos(a_) * r_, cy + _m.sin(a_) * r_))
    kit.cut(k, pts, dp.GOLD, lw=2)
    kit.text(k, "PREMIUM", cx, cy + 5 * s_, 16.5 * s_, INK)


import client_ob as _co
co_BT = _co.BT


def _shredding(k):
    """The shredder is running: a sheet going in, shreds jumping."""
    c = k.c
    top = F - 96
    c.save(); c.translate(SHRED_X + 2, top - 20); c.rotate(0.06)
    kit.rect(k, -17, -30, 34, 44, (0.99, 0.98, 0.95), 3560, lw=1.8)
    c.set_source_rgb(*INK); c.set_line_width(1.3)
    for yy in (-20, -12, -4):
        c.move_to(-11, yy); c.line_to(11, yy); c.stroke()
    c.restore()
    _lines(k, [(SHRED_X - 30, top - 6, SHRED_X - 42, top - 16), (SHRED_X + 34, top - 6, SHRED_X + 46, top - 16),
               (SHRED_X - 34, top + 14, SHRED_X - 48, top + 14), (SHRED_X + 38, top + 14, SHRED_X + 52, top + 14)])


def s4_shred(k, o):                                       # v3, first drawing: the shredder in plain view, eating a page; he is looking at it
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    _shredding(k)
    dc.repairman(k, TOUR[1][0] - 14, TOUR[1][1], GS, case=True, look=(1, 0.4))
    sb.don(k, 440, F + 26, 0.60, "vest", "happy", look=(-1, 0))


def s4_tour(k, o):                                        # second drawing: one step sideways and he is in front of it
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    _shredding(k)
    dc.repairman(k, TOUR[1][0] - 14, TOUR[1][1], GS, case=True, look=(1, 0.1))
    sb.don(k, 506, F + 26, 0.60, (-52, -8, 52, 8), "happy", look=(-1, 0))
    _lines(k, [(452, F - 4, 470, F - 4), (448, F + 10, 468, F + 10)])


def s4_card(k, o):                                        # v2: not a card: a big gold sticker, slapped over his pass
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    dc.repairman(k, TOUR[1][0] - 14, TOUR[1][1], GS, case=True, look=(0.2, 1))
    _sticker(k, TOUR[1][0] - 14, TOUR[1][1])
    sb.don(k, 480, F + 26, 0.60, (-88, -4, 8, 0), "happy", look=(-1, 0))
    _lines(k, [(TOUR[1][0], F - 150, TOUR[1][0] + 12, F - 160), (TOUR[1][0] + 4, F - 128, TOUR[1][0] + 18, F - 128)])


def s4_life(k, o):
    dp.ceo_chair(k, THR4 - 30, CH[1], CH[2])
    sb.don(k, 480, F + 26, 0.60, "vest", "happy", look=(-1, 0))


def s4_blank(k, o):                                       # v2: the button. He looks down at the sticker, then at Don. Nothing on his face
    dc.repairman(k, TOUR[1][0] - 14, TOUR[1][1], GS, case=True, look=(0.15, 1))
    _sticker(k, TOUR[1][0] - 14, TOUR[1][1])


def s4_line(k, o):                                        # v2: Sofía's smile is fear with teeth
    dp.ceo_chair(k, THR4, CH[1], CH[2])
    sb.mfs.mom(k, LINE[0][0], LINE[0][1], MS, "stand", "sweet", look=(-1, 0))
    scs.sofia(k, LINE[2][0], LINE[2][1], SS, "hold", "recover", look=(-1, 0))
    sb.don(k, LINE[1][0], LINE[1][1], 0.60, "vest", "happy", look=(-1, 0))
    _lines(k, [(LINE[1][0] - 40, F - 190, LINE[1][0] - 52, F - 198), (LINE[1][0] + 40, F - 190, LINE[1][0] + 52, F - 198)])


HV = dl.hc(TOUR[1][0] - 14, TOUR[1][1], GS)
TWO4 = (438, 720, 2.25)                                    # the visitor, Don and the shredder in one frame
S4 = [
    ("5.1", 1.9, dl.shot("s4a", [dl.hc(128, F + 8, GS)], s4_door, "", chair=False),
     "MEDIUM, the door. A knock, and he is already in: a big man in a black service jacket, a metal case low in his hand, caught mid-step. He says it to the room, plainly.",
     "VISITOR: \"I'm here to inspect the machine.\""),
    ("5.2", 0.6, dl.shot("s4b", [dl.hm(*LINE[0], MS), dl.hd(*LINE[1], 0.60), dl.hp(*LINE[2], SS)], s4_line, "", chair=False, ymin=240),
     "THREE-SHOT. They snap into a line, a step apart: Mom, Don, Sofía. Don is in front of the throne, pulling his vest straight. Sofía's smile is pure fear. All eyes left, on the door.", ""),
    ("5.3", 2.05, dl.shot("s4c", [dl.hd(*LINE[1], 0.60)], s4_don, "", chair=False),
     "CLOSE. One arm sweeps the room open to him, the salesman at full power. The crown of the throne he is hiding stands behind his head.",
     "DON: \"Of course. We've been expecting you.\""),
    ("5.4", 0.4, dl.shot("s4d", [dl.hp(PAM[0], PAM[1], PS)], s4_pam_look, "", chair=False, cam=(628, 686.8, 2.889)),
     "CLOSE. Pam, at the end of the counter. Her eyes go down to what he is carrying.", ""),
    ("5.4'", 0.7, "5.4i",
     "INSERT, what she sees: the coffee cup on the case, and his pass. COFFEE SERVICE.", ""),
    ("5.4''", 1.0, dl.shot("s4e", [dl.hp(PAM[0], PAM[1], PS)], s4_pam_cup, "", chair=False, cam=(628, 686.8, 2.889)),
     "CLOSE. She tips her mug upside down: nothing. She peers into it. Her mouth opens; she looks at the mug again; it closes. She says nothing to anyone.", ""),
    ("6.1", 0.6, dl.shot("s4f0", [dl.hd(440, F + 26, 0.60), HV], s4_shred, "", chair=False, cam=TWO4),
     "THREE THINGS IN FRAME: the visitor, Don, and to Don's right the shredder, running loudly, a page going in. The visitor's eyes are on it.",
     "DON: \"Complete...\""),
    ("6.1'", 1.3, dl.shot("s4f", [dl.hd(506, F + 26, 0.60), HV], s4_tour, "", chair=False, cam=TWO4),
     "SAME FRAME, second drawing. Without losing the smile Don takes one step sideways and is standing in front of it, arms a little out. The noise goes on behind him.",
     "DON: \"...transparency.\""),
    ("6.1''", 2.05, dl.shot("s4g", [dl.hd(480, F + 26, 0.60), HV], s4_card, "", chair=False, cam=TWO4),
     "SAME FRAME, third drawing. He slaps a big gold sticker on the man's chest, right over his COFFEE SERVICE pass: PREMIUM. The visitor looks down at it.",
     "DON: \"Lifetime Premium. On us.\""),
    ("6.2", 1.85, dl.shot("s4h", [da.RH], da._rb("idle"), "", zmax=3.6, chair=False),
     "CLOSE, the robot at its station by the door. Helpful. We cut away before it has finished.", "ROBOT: \"Premium search is non-functional.\""),
    ("6.3", 1.75, dl.shot("s4i", [dl.hd(480, F + 26, 0.60)], s4_life, "", chair=False),
     "CLOSE. He doesn't turn his head or lose the smile. His eyes stay on the visitor.", "DON: \"Then make it lifetime.\""),
    ("6.4", 0.7, dl.shot("s4j", [HV], s4_blank, "", chair=False),
     "CLOSE, the visitor. He looks down at the gold sticker on his chest, then up at Don. Nothing on his face at all. HOLD. Cut.", ""),
]
# ---------------------------------------------------------------- scene 5: THE FILTER (beat 7)
import math as _m5
VIS = (722, F + 14)                                        # the visitor, at the counter in front of the machine
THR5 = THR4 - 30                                           # the throne, where scene 4 left it
DON5 = (THR5 + 12, F + 26)                                 # v2: Don has not followed him. He stands in front of the throne, hiding it
MX, MY, MZ = dp.MACHINE
PAM5 = (828, F + 6)                                        # Pam has come round to the machine's other side, mug ready
SOF5, MOM5 = (570, F + 4), (636, F + 8)                    # Sofía and Mom, between Don and the counter


def _vis(k, look=(0.4, 0), fn=None, **kw):
    o = (fn or dc.repairman)(k, VIS[0], VIS[1], GS, look=look, **kw)
    _sticker(k, VIS[0], VIS[1])
    return o


def _don5(k, face, filt=False, look=(1, 0), pose="stand", flat=False, drop=False):
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    d = sb.don(k, DON5[0], DON5[1], 0.60, pose, face, look=look)
    if filt:
        dp.coffee_run(k, d["head"], 0.60)
        dp.wet_filter(k, d["head"][0] + (0 if flat else 4), d["head"][1] - (22 if flat else 25), 0.80, 0.0 if flat else -0.16)
    if drop:
        c = k.c
        hx, hy = d["head"]
        c.save(); c.translate(hx - 25, hy + 58); c.scale(0.8, 0.8)
        c.move_to(0, -9); c.curve_to(7, 0, 6, 7, 0, 7); c.curve_to(-6, 7, -7, 0, 0, -9); c.close_path()
        c.set_source_rgb(*dp.COFFEE); c.fill(); c.restore()
    return d


def s5_bang(k, o):
    dc.repairman(k, 648, VIS[1], GS, case=False, look=(1, 0.2)); _sticker(k, 648, VIS[1])
    dc.tool_case(k, 716, F - 216, 0.62)
    _lines(k, [(716 + _m5.cos(a_) * 44, F - 196 + _m5.sin(a_) * 30, 716 + _m5.cos(a_) * 66, F - 196 + _m5.sin(a_) * 48) for a_ in (-2.6, -2.1, -1.0, -0.5)])


JUMP5 = 46


def s5_flinch(k, o):                                      # v2: his feet are a long way off the floor
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    sb.mfs.mom(k, MOM5[0], MOM5[1], MS, "stand", "sweet", look=(1, 0))
    scs.sofia(k, SOF5[0], SOF5[1], SS, "hold", "caught", look=(1, 0))
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.20); c.save(); c.translate(DON5[0], F + 30); c.scale(1, 0.22); c.arc(0, 0, 34, 0, 6.2832); c.fill(); c.restore()
    sb.don(k, DON5[0], DON5[1] - JUMP5, 0.60, kit.ARM_POSES["shock"], "panic", look=(1, 0))
    _lines(k, [(DON5[0] - 26, F - 4, DON5[0] - 26, F + 16), (DON5[0], F, DON5[0], F + 20), (DON5[0] + 26, F - 4, DON5[0] + 26, F + 16)])


def s5_brush(k, o):
    dq.visitor_brush(k, VIS[0] - 30, VIS[1], GS); _sticker(k, VIS[0] - 30, VIS[1])


def _brush_hand(k, touch):
    """In the machine's close-up: his hand comes in from the left with the brush. touch: its tip is on the machine."""
    hx = MX - 62 * MZ - (0 if touch else 22)
    hy = MY - 92 * MZ
    kit.cut(k, [(hx - 90, hy), (hx - 40, hy - 4), (hx - 38, hy + 22), (hx - 90, hy + 30)], dc.SUIT, shadow=False, lw=2)
    kit.ellipse(k, hx - 30, hy + 9, 13, 11, _co.SKIN, 3570, shadow=False, lw=2)
    dc.brush(k, hx - 14, hy + 4, 0.8, 0.0)
    if touch:
        _lines(k, [(hx + 14, hy - 10, hx + 24, hy - 20), (hx + 18, hy + 4, hx + 30, hy + 4), (hx + 14, hy + 18, hx + 24, hy + 28)])


def s5_track(k, o):                                       # v2: we don't follow the filter; we watch them watch it cross the room
    scs.sofia(k, SOF5[0], SOF5[1], SS, "hold", "caught", look=(-0.6, -0.9))
    sb.mfs.mom(k, MOM5[0], MOM5[1], MS, "stand", "sweet", look=(-0.3, -0.9))
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_dash([7, 6])
    c.move_to(690, F - 310); c.curve_to(640, F - 352, 560, F - 356, 500, F - 326); c.stroke(); c.set_dash([])
    dp.wet_filter(k, 574, F - 348, 0.5, 2.6, drips=False)


def s5_land(k, o):
    _don5(k, "neutral", filt=True, look=(0, 0), flat=True)
    hx, hy = DON5[0], DON5[1] - 302 * 0.60
    _lines(k, [(hx - 42, hy - 40, hx - 58, hy - 50), (hx + 42, hy - 40, hx + 58, hy - 50), (hx - 48, hy - 22, hx - 66, hy - 24), (hx + 48, hy - 22, hx + 66, hy - 24)])


def s5_clear(k, o):
    _vis(k, look=(-0.6, 0), case=False)


def s5_hope(k, o):
    _don5(k, "happy", filt=True, look=(1, 0), pose=(-30, -10, 30, 10))


def s5_inv(k, o):
    dq.visitor_invoice(k, VIS[0] - 70, VIS[1], GS, big=True)
    _sticker(k, VIS[0] - 70, VIS[1])


def s5_dead(k, o):
    _don5(k, "neutral", filt=True, look=(1, 0.2), drop=True)


def s5_pam(k, o):
    q = pb.pam(k, PAM5[0], PAM5[1], PS, (-8, 0, 150, 96), "neutral", look=(-0.2, 0.6), glasses="up")
    c = k.c
    hx, hy = q["head"][0] + 14, q["head"][1] + 36
    c.save(); c.translate(hx, hy); c.rotate(-0.42); c.scale(1.45, 1.45)     # a mug: a handle, a rim, at her mouth
    c.set_source_rgb(*INK); c.set_line_width(5); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    c.set_source_rgb(0.36, 0.62, 0.80); c.set_line_width(2.4); c.new_path(); c.arc(12, 1, 7.5, -1.3, 1.3); c.stroke()
    kit.cut(k, [(-10, -12), (10, -12), (9, 12), (-9, 12)], (0.36, 0.62, 0.80), shadow=False, lw=2)
    kit.ellipse(k, 0, -12, 10, 3.2, (0.97, 0.96, 0.92), 3580, shadow=False, lw=1.6)
    c.restore()
    c.set_source_rgba(1, 1, 1, 0.85); c.set_line_width(3); c.set_line_cap(1)
    for dx in (-10, 4):
        c.move_to(hx + dx, hy - 26); c.curve_to(hx + dx + 6, hy - 36, hx + dx - 6, hy - 44, hx + dx + 2, hy - 54); c.stroke()


HD5 = dl.hd(DON5[0], DON5[1], 0.60)
HV5 = dl.hc(VIS[0], VIS[1], GS)
MCAM = (MX - 16, 560, 2.8)
DCAM = (DON5[0] - 20, 604, 3.2)                            # Don close: his face big, the crown whole above it
S5 = [
    ("7.1a", 0.7, dl.shot("s5a", [dl.hc(648, VIS[1], GS)], s5_bang, "", chair=False, cam=(728, 650, 2.2)),
     "MEDIUM, the counter. He walks past the robot and drops the metal case on the counter beside the dead coffee machine. BANG. The gold PREMIUM sticker is on his chest.", ""),
    ("7.1a'", 0.5, dl.shot("s5b", [dl.hd(DON5[0], DON5[1] - JUMP5, 0.60), dl.hp(SOF5[0], SOF5[1], SS), dl.hm(MOM5[0], MOM5[1], MS)], s5_flinch, "", chair=False, cam=(528, 800, 1.6), ymin=150),
     "THREE-SHOT. Mom and Sofía flinch. Don, in front of the throne he is hiding, leaves the floor altogether.", ""),
    ("7.1b", 1.4, "7.1b",
     "INSERT. His thumbs on the latches: click, click. The lid comes up slowly. Inside, in pale foam, with room for a rifle: one small brush.", ""),
    ("7.1c", 0.6, dl.shot("s5c", [dl.hc(VIS[0] - 30, VIS[1], GS)], s5_brush, "", chair=False, cam=(724, 650, 2.2)),
     "MEDIUM. He lifts it out between two fingers, like a surgeon, and turns to the machine.", ""),
    ("7.2a", 0.4, dl.shot("s5d", [], lambda k, o: _brush_hand(k, False), "", chair=False, machine="broken", cam=MCAM),
     "CLOSE, the machine. His hand comes in from the left with the brush, slowly.", ""),
    ("7.2a'", 0.4, dl.shot("s5e", [], lambda k, o: _brush_hand(k, True), "", chair=False, machine="rattle", cam=MCAM),
     "SAME FRAME, second drawing. ONE touch. The machine shakes and the needle jumps into the red. The repair is the fault.", ""),
    ("7.2a''", 0.4, dl.shot("s5f", [], lambda k, o: None, "", chair=False, machine="pop", cam=MCAM),
     "Third drawing. ONE big POP: the lid jumps and the filter leaves the top of the frame, going left.", ""),
    ("7.2b", 0.45, dl.shot("s5t", [dl.hp(SOF5[0], SOF5[1], SS), dl.hm(MOM5[0], MOM5[1], MS)], s5_track, "", chair=False, cam=(604, 668, 2.3)),
     "TWO-SHOT, Sofía and Mom. Their heads and eyes follow something across the room over them, right to left. We don't see where it is going.", ""),
    ("7.3", 1.2, dl.shot("s5g", [HD5], s5_land, "", chair=False, cam=DCAM),
     "CLOSE, Don, the throne's crown behind his head. It comes in from the top: SLAP, flat on his bald head for one drawing. Coffee runs past his eye. He does not move. HELD IN SILENCE.", ""),
    ("7.3b", 1.7, dl.shot("s5h", [da.RH], da._rb("rec"), "", zmax=3.6, chair=False),
     "CLOSE, the robot, cheerful. A red REC dot, a shutter click.", "ROBOT: \"CEO responsible.\""),
    ("7.4", 1.0, dl.shot("s5i", [HV5], s5_clear, "", chair=False, machine="ok", cam=(736, 650, 2.2)),
     "MEDIUM. The machine has a green light and steam. He wipes his hands, satisfied, and says it across the room.", "VISITOR: \"All clear.\""),
    ("7.5", 1.05, dl.shot("s5j", [HD5], s5_hope, "", chair=False, cam=DCAM),
     "CLOSE, Don, the filter crooked on his head, the crown behind it. He dares to smile: he thinks he has passed.", "DON: \"The company?\""),
    ("7.6", 1.4, dl.shot("s5k", [dl.hc(VIS[0] - 70, VIS[1], GS)], s5_inv, "", chair=False, machine="ok", cam=(724, 650, 2.2)),
     "MEDIUM. A little puzzled by the question, he holds out an invoice. One thing on it you can read: $80.", "VISITOR: \"The coffee machine.\""),
    ("7.7", 0.6, dl.shot("s5l", [HD5], s5_dead, "", chair=False, cam=DCAM),
     "CLOSE, Don. The smile is gone in one drawing. The filter is still on his head. One fat drop of coffee falls off his jaw.", ""),
    ("7.8", 2.15, dl.shot("s5m", [dl.hp(PAM5[0], PAM5[1], PS)], s5_pam, "", chair=False, machine="ok", cam=(792, 648, 2.6)),
     "TWO THINGS IN FRAME: the steaming machine and Pam, who has come round to it with her mug. A sip, eyes down. Then, into the mug, to nobody.",
     "PAM: \"Some inspect. Others drink.\""),
]
# ---------------------------------------------------------------- scene 6: MOM (beat 8), v2 (after the scene review)
import sofia_dh as sdh
import mom_bc as _mb
DON6 = DON5                                                # he hasn't moved: in front of the throne, the filter on his head
MOM6 = (DON6[0] - 84, F + 8)                               # Mom has marched across the room to him
HD6 = dl.hd(DON6[0], DON6[1], 0.60)
HM6 = dl.hm(MOM6[0], MOM6[1], MS)
LINE6 = ((DON6[0], F + 26), (DON6[0] + 72, F + 6), (DON6[0] + 162, F + 8))
CAM6B = (DON6[0] + 92, 762, 1.95)    # Don, Pam, Mom (8.4b)
SOF6 = (636, F + 4)                                        # where Sofía is left standing
SKIN_M = (0.93, 0.76, 0.65)


def _mom_pose(name, pose):
    sb.mfs._body.__globals__["POSES"].setdefault(name, pose)     # the dict Mom's body looks poses up in
    return name


def s6_peel(k, o):                                        # first drawing: she lifts it off him between two fingers
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    d = sb.don(k, DON6[0], DON6[1], 0.60, "stand", "neutral", look=(-0.7, -0.5))
    dp.coffee_run(k, d["head"], 0.60)
    sb.mfs.mom(k, MOM6[0], MOM6[1], MS, _mom_pose("peel", _mb.wipe_at(96, _mb.HY - 40)), "glare", look=(0.8, -0.5), bag=False)
    dp.wet_filter(k, d["head"][0] - 40, d["head"][1] - 40, 0.66, -0.55, drips=True)
    _lines(k, [(d["head"][0] - 8, d["head"][1] - 40, d["head"][0] - 4, d["head"][1] - 52), (d["head"][0] + 10, d["head"][1] - 40, d["head"][0] + 14, d["head"][1] - 52)])


def s6_lick(k, o):                                        # v2, the recoil: he has gone a step back and sideways, palms up, head away
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    c = k.c
    c.save(); c.translate(DON6[0] + 4, DON6[1]); c.rotate(0.09); c.translate(-DON6[0] - 4, -DON6[1])
    d = sb.don(k, DON6[0] + 4, DON6[1], 0.60, (-50, -168, 50, 168), "panic", look=(-1, 0))
    dp.coffee_run(k, d["head"], 0.60)
    c.restore()
    sb.mfs.mom(k, MOM6[0], MOM6[1], MS, "lick", "sweet", look=(0.8, -0.3), bag=False)
    dp.wet_filter(k, MOM6[0] - 34, F - 86, 0.6, 0.4)


def s6_thumb(k, o):                                       # v2, the surrender: the thumb is on his scalp. His arms have dropped. It is over
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    d = sb.don(k, DON6[0], DON6[1], 0.60, "stand", "neutral", look=(0, -1))
    m = sb.mfs.mom(k, MOM6[0], MOM6[1], MS, _mom_pose("thumb", _mb.wipe_at(126, _mb.HY - 30)), "sweet", look=(0.8, -0.5), bag=False)
    hx, hy = d["head"][0] - 14, d["head"][1] - 28
    c = k.c
    c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(3.2); c.set_line_cap(1)           # the wet shine she leaves
    c.move_to(hx + 8, hy + 2); c.curve_to(hx + 16, hy - 4, hx + 26, hy - 4, hx + 34, hy + 2); c.stroke()
    _lines(k, [(hx - 4, hy - 12, hx - 10, hy - 22), (hx + 8, hy - 14, hx + 8, hy - 26)])
    dp.wet_filter(k, MOM6[0] - 34, F - 86, 0.6, 0.4)


def s6_scrub(k, o):                                       # v2: one big wipe at the stain; his eyes are on the ceiling
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    sb.don(k, DON6[0], DON6[1], 0.60, "stand", "neutral", look=(0, -1))
    m = sb.mfs.mom(k, MOM6[0], MOM6[1], MS, "wipe", "glare", look=(0.6, 0.5), bag=False)
    tx, ty = m["hands"][1]
    kit.cut(k, [(tx - 4, ty - 15), (tx + 18, ty - 12), (tx + 22, ty + 8), (tx + 6, ty + 16), (tx - 8, ty + 6)], (0.99, 0.99, 0.97), shadow=False, lw=2)   # the tissue
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(2.2); c.set_line_cap(1)
    for r_ in (26, 34):                                    # the scrub, one way
        c.new_path(); c.arc(tx + 6, ty, r_, -0.9, 0.9); c.stroke()


def s6_zip(k, o):
    """v2: the zip as a small act of violence. Her sleeve and fist are in the frame, the pull in her fist under his chin;
    his shoulders are up round his ears, the collar has eaten his neck and his mouth is a short flat line."""
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    d = dq.don_zipped(k, DON6[0], DON6[1], 0.60, pose=(-22, 6, 22, -6), face="neutral", look=(-0.5, 0.3))
    hx, hy = d["head"]
    c = k.c
    VEST = dq.dv.VEST
    for sg in (-1, 1):                                     # the shoulders, up
        kit.cut(k, [(hx + sg * 14, hy + 30), (hx + sg * 40, hy + 24), (hx + sg * 47, hy + 46), (hx + sg * 16, hy + 48)], VEST, shadow=False, lw=2.2)
    kit.cut(k, [(hx - 21, hy + 42), (hx - 18, hy + 25), (hx + 18, hy + 25), (hx + 21, hy + 42)], VEST, shadow=False, lw=2.2)        # the collar, over his chin
    c.set_source_rgb(*SKIN_M); c.rectangle(hx - 11, hy + 8, 22, 10); c.fill()                                                          # his mouth: one tight line
    c.set_source_rgb(*INK); c.set_line_width(3.2); c.set_line_cap(1); c.move_to(hx - 8, hy + 14); c.line_to(hx + 8, hy + 14); c.stroke()
    fx, fy = hx - 2, hy + 34                               # her fist, on the pull
    kit.cut(k, [(fx - 92, fy + 64), (fx - 24, fy + 6), (fx - 10, fy + 22), (fx - 78, fy + 82)], sb.mfs.TEAL, shadow=False, lw=2.4)   # her sleeve, from the bottom left
    kit.cut(k, [(fx - 30, fy + 10), (fx - 20, fy + 2), (fx - 6, fy + 18), (fx - 16, fy + 27)], sb.mfs.MUSTARD, shadow=False, lw=2)   # the cuff
    kit.ellipse(k, fx - 6, fy + 6, 12, 11, SKIN_M, 3600, shadow=False, lw=2.2)
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for i in (-4, 1, 6):
        c.move_to(fx - 6 + i, fy - 2); c.line_to(fx - 8 + i, fy + 6); c.stroke()
    kit.text(k, "eek!", hx - 44, hy - 40, 11, (1, 1, 1))


def s6_sofia(k, o):                                       # v2: surer of herself: the CV higher, carried like a ticket
    sdh.sofia(k, SOF6[0], SOF6[1], SS, "lapel", "interested", look=(-0.8, -0.3))
    sdh.cv(k, SOF6[0] - 50, F - 92, 0.62, -0.12)


def s6_place(k, o):
    """v3: Mom stands an arm's length from Pam, so the arm is the picture: straight out, her hand closed on Pam's
    elbow. Pam has landed with her fists on her hips, chin up; nothing of her is covered. Don hasn't moved. At the
    right edge, above the app's buttons: Sofía's cream sleeve, her hand and the CV, stopped."""
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    dq.don_zipped(k, LINE6[0][0], LINE6[0][1], 0.60, look=(0.6, 0))
    ex_, ey_ = LINE6[1][0] + 30, F - 78                                     # Pam's elbow, the one towards Mom
    tx = (ex_ + 6 - LINE6[2][0]) / MS
    m = sb.mfs.mom(k, LINE6[2][0], LINE6[2][1], MS, _mom_pose("steer4", _mb.mo.ik(-1, tx, (ey_ - LINE6[2][1]) / MS) + _mb.mo.ik(1, 11, _mb.WAIST - 2)),
                   "sweet", look=(-0.8, 0), bag=False)
    pb.pam(k, LINE6[1][0], LINE6[1][1], PS, (-35, 110, 35, -110), "neutral", look=(0, -0.3), glasses="up")
    gx, gy = m["hands"][0]
    kit.ellipse(k, gx, gy, 10, 9, SKIN_M, 3610, shadow=False, lw=2.4)                     # her hand, on top: it has the elbow
    c = k.c
    c.set_source_rgb(*INK); c.set_line_width(1.6)
    for i in (-4, 1, 6):
        c.move_to(gx + i, gy - 7); c.line_to(gx + i - 1, gy + 2); c.stroke()
    _lines(k, [(gx - 6, gy - 16, gx - 10, gy - 26), (gx + 6, gy - 16, gx + 10, gy - 26)])
    ex = CAM6B[0] + 270 / CAM6B[2]                           # the frame's right edge
    CREAM = (0.96, 0.93, 0.85)
    kit.cut(k, [(ex + 4, 676), (ex - 22, 680), (ex - 22, 696), (ex + 4, 700)], CREAM, shadow=False, lw=2)        # her sleeve
    sdh.cv(k, ex - 30, 684, 0.5, 0.06)
    kit.ellipse(k, ex - 24, 690, 7, 6, (0.80, 0.60, 0.45), 3620, shadow=False, lw=2)                             # her hand on it


def s6_left(k, o):                                        # the spot is taken. Sofía, mid-step, the CV still held out
    sdh.sofia(k, SOF6[0], SOF6[1], SS, "stand", "tight", look=(-1, 0))
    sdh.cv(k, SOF6[0] - 50, F - 84, 0.6, 0.1)


TWO6 = (DON6[0] - 62, 664, 2.3)
S6 = [
    ("8.1", 0.4, "8.1", "INSERT. The robot's visor: 16:59. One minute.", ""),
    ("8.2", 0.5, dl.shot("s6a", [HD6, HM6], s6_peel, "", chair=False, cam=TWO6),
     "TWO-SHOT at the throne. Mom has crossed the room. She lifts the filter off his head between two fingers, like something the cat brought in.", ""),
    ("8.2'", 0.7, dl.shot("s6b", [HD6, HM6], s6_lick, "", chair=False, cam=TWO6),
     "SAME FRAME, second drawing. She licks her thumb. He sees it and goes back on his heels: palms up at his shoulders, head away.", "DON: \"Mom! I'm...\""),
    ("8.2''", 0.9, dl.shot("s6b2", [HD6, HM6], s6_thumb, "", chair=False, cam=TWO6),
     "Third drawing, before he has finished the sentence. The thumb is on his scalp. His arms have dropped. Eyes on the ceiling. A wet shine where it went.", "DON: \"...the CEO!\""),
    ("8.2'''", 0.4, dl.shot("s6c", [HD6, HM6], s6_scrub, "", chair=False, cam=TWO6),
     "Fourth drawing. One pose: a tissue on the ketchup stain, one big wipe. He is still looking at the ceiling.", ""),
    ("8.3", 1.8, dl.shot("s6d", [HD6], s6_zip, "", chair=False, cam=DCAM),
     "CLOSE, Don, the crown behind his head. Her sleeve and fist run the zip up to his chin in one pull, as her line ends. His shoulders go up, his neck is gone, his mouth is a line. SOUND: ZZZIP, eek.",
     "MOM (off): \"Then stand like one, Donnie.\""),
    ("8.4a", 0.6, dl.shot("s6e", [dl.hp(SOF6[0], SOF6[1], SS)], s6_sofia, "", chair=False, cam=(SOF6[0] - 2, 690, 3.0)),
     "MEDIUM. Sofía walks back in, changed: the cream suit, the ponytail, the triangles. Chin up, a hand on her lapel, the CV carried high. The place beside Don is hers.", ""),
    ("8.4b", 0.8, dl.shot("s6f", [dl.hd(*LINE6[0], 0.60), dl.hp(*LINE6[1], PS), dl.hm(*LINE6[2], MS)], s6_place, "", chair=False, cam=CAM6B, ymin=150),
     "THREE-SHOT. Without a word, Mom takes Pam by the elbow and plants her beside Don. Pam lands with her fists on her hips. Don does not move. At the frame's edge: a cream sleeve and a CV, stopped.", ""),
    ("8.4c", 0.5, dl.shot("s6g", [dl.hp(SOF6[0], SOF6[1], SS)], s6_left, "", chair=False, cam=(SOF6[0] - 2, 690, 3.0)),
     "MEDIUM, Sofía. The same frame as 8.4a. The CV still held out to nobody. The smile stays on; the eyes have stopped.", ""),
]
# ---------------------------------------------------------------- scene 7: THE ARRIVAL (beat 9)
FS = dl.FS
FA1 = (130, F + 16)                                        # Father, just inside the door, by the robot
FA2 = (330, F + 20)                                        # Father, two steps in: facing Don
GU7 = (746, F - 2)                                         # the second bodyguard's post, on the far side, by Sofía
HF2 = dl.hd(FA2[0], FA2[1], FS)


def s7_thumb(up):
    """v2: the thumb never comes down. up: the offer, a big smile. not up: Father has said it; the smile is dead, he has
    sunk a little into his collar, and the thumb is still up there, forgotten, shaking."""
    def f(k, o):
        dp.ceo_chair(k, THR5, CH[1], CH[2])
        dc.father(k, FA2[0], FA2[1], FS, face="hard" if up else "talk", look=(1, 0))
        d = dq.don_zipped(k, DON6[0], DON6[1] + (0 if up else 9), 0.60, pose=(-150, -40, 10, 0) if up else (-146, -34, 4, 0),
                          face="happy" if up else "neutral", look=(-1, 0) if up else (-1, 0.5))
        hands = d.get("hands")
        if hands:
            hx, hy = hands[0]
            kit.cut(k, [(hx - 5, hy - 6), (hx - 4, hy - 25), (hx + 6, hy - 25), (hx + 7, hy - 6)], SKIN_M, shadow=False, lw=2.2)   # the thumb
            if up:
                _lines(k, [(hx - 16, hy - 28, hx - 22, hy - 36), (hx + 18, hy - 28, hx + 24, hy - 36)])
            else:                                           # it shakes
                c = k.c
                c.set_source_rgb(1, 1, 1); c.set_line_width(2.6); c.set_line_cap(1)     # white: it is in front of the throne's dark back
                for sx in (-1, 1):
                    for r_ in (15, 22):
                        c.new_path(); c.arc(hx + 1, hy - 14, r_, (-0.5 if sx > 0 else 3.14 - 0.5), (0.5 if sx > 0 else 3.14 + 0.5)); c.stroke()
        if not up:                                          # one drop of sweat
            hx, hy = d["head"]
            c = k.c
            c.save(); c.translate(hx + 24, hy - 4); c.scale(0.8, 0.8)
            c.move_to(0, -9); c.curve_to(7, 0, 6, 7, 0, 7); c.curve_to(-6, 7, -7, 0, 0, -9); c.close_path()
            c.set_source_rgb(0.55, 0.78, 0.92); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.6); c.stroke(); c.restore()
    return f


GAP7 = (22, 228)                                           # v3: the guards half in the frame on each side, faces and glasses readable


def s7_gap(k, o):
    dl._guards(k, GAP7[0], GAP7[1])
    dc.father(k, 125, F + 22, FS, look=(0.3, 0.1))


def s7_step(k, o):
    """v3: the same size, the same place, and one foot out in front of him: a black trouser leg and a shoe, a floor
    shadow under it. The bodyguards are the same drawing as before: nothing else has moved."""
    dl._guards(k, GAP7[0], GAP7[1])
    dc.father(k, 125, F + 22, FS, look=(0.3, 0.1))
    c = k.c
    BLACK = (0.10, 0.10, 0.12)
    lx = 125 + 13
    c.set_source_rgba(0, 0, 0, 0.22); c.save(); c.translate(lx + 4, F + 44); c.scale(1, 0.3); c.arc(0, 0, 26, 0, 6.2832); c.fill(); c.restore()
    c.set_source_rgb(*kit.FLOOR); c.rectangle(lx - 12, F + 13, 44, 16); c.fill()                                               # the foot he has lifted
    kit.cut(k, [(lx - 11, F - 40), (lx + 11, F - 40), (lx + 14, F + 32), (lx - 9, F + 32)], BLACK, shadow=False, lw=2.2)        # the leg, forward
    kit.cut(k, [(lx - 12, F + 30), (lx + 18, F + 30), (lx + 24, F + 42), (lx - 12, F + 42)], BLACK, shadow=False, lw=2.2)       # the shoe
    c.set_source_rgba(1, 1, 1, 0.75); c.set_line_width(2); c.set_line_cap(1); c.move_to(lx + 6, F + 34); c.line_to(lx + 14, F + 34); c.stroke()
    _lines(k, [(lx + 30, F + 42, lx + 46, F + 42)])


def s7_hop(k, o):                                         # v2: the robot is the only happy thing in the room
    c = k.c
    c.save(); c.translate(0, -15)
    da._rb("tick")(k, o)
    c.restore()
    rx, ry = da.RB[0], da.RB[1]
    _lines(k, [(rx - 26, ry + 6, rx - 40, ry + 6), (rx + 26, ry + 6, rx + 40, ry + 6), (rx - 10, ry + 12, rx - 10, ry + 2), (rx + 10, ry + 12, rx + 10, ry + 2)])


def s7_cv(taken):
    def f(k, o):
        g = dc.guard(k, GU7[0], GU7[1], GS, flip=True)
        if not taken:                                       # she is on him before he has finished arriving
            sdh.sofia(k, SOF6[0], SOF6[1], SS, "stand", "interested", look=(1, -0.2))
            sdh.cv(k, SOF6[0] + 44, F - 100, 0.62, 0.1)
            _lines(k, [(GU7[0] + 34, F - 6, GU7[0] + 50, F - 6), (GU7[0] + 36, F + 6, GU7[0] + 54, F + 6)])
        else:                                               # one bare hand; the CV is half in his breast pocket already
            sdh.sofia(k, SOF6[0], SOF6[1], SS, "stand", "tight", look=(1, 0))
            px, py = GU7[0] - 20, F - 128
            sdh.cv(k, px, py - 14, 0.5, 0.0)
            kit.cut(k, [(px - 17, py - 2), (px + 17, py - 2), (px + 15, py + 24), (px - 15, py + 24)], dc.SUIT, shadow=False, lw=2)     # the pocket, over it
            kit.ellipse(k, px + 2, py - 34, 12, 9, _co.SKIN, 3700, shadow=False, lw=2.2)
            k.c.set_source_rgb(0.85, 0.85, 0.88); k.c.set_line_width(1.8); k.c.move_to(px - 16, py - 1); k.c.line_to(px + 16, py - 1); k.c.stroke()   # the pocket's edge                                              # his hand, pushing it in
            _lines(k, [(SOF6[0] + 30, F - 110, SOF6[0] + 42, F - 114), (SOF6[0] + 30, F - 96, SOF6[0] + 44, F - 94)])
    return f


def s7_door(k, o):
    """The door, shut. Two shapes fill the glass from the other side; three knocks on it."""
    c = k.c
    c.push_group()
    dl.s9_1(k, o)
    pat = c.pop_group()
    c.set_source_rgba(0.16, 0.20, 0.27, 0.62); c.mask(pat)   # only their shapes, through the glass
    import math as _m
    fx, fy = 128, 618                                        # one of them has a fist on the glass
    c.set_source_rgba(0.10, 0.13, 0.19, 0.80)
    c.set_line_width(22); c.set_line_cap(1); c.move_to(92, 668); c.line_to(fx - 4, fy + 6); c.stroke()      # his forearm, up from his shoulder
    c.arc(fx, fy, 17, 0, 2 * _m.pi); c.fill()
    c.set_source_rgb(*INK); c.set_line_cap(1)
    for (kx, ky, r0, r1, lw) in ((fx, fy, 22, 38, 3.6), (fx + 46, fy - 40, 9, 19, 2.8), (fx + 74, fy - 74, 6, 13, 2.2)):   # knock, knock, knock
        c.set_line_width(lw)
        for j in range(10):
            a_ = 2 * _m.pi * j / 10 + 0.2
            c.move_to(kx + _m.cos(a_) * r0, ky + _m.sin(a_) * r0); c.line_to(kx + _m.cos(a_) * r1, ky + _m.sin(a_) * r1); c.stroke()


def s7_line(k, o):                                        # the line-up has heard it. Nobody breathes
    dp.ceo_chair(k, THR5, CH[1], CH[2])
    dq.don_zipped(k, LINE6[0][0], LINE6[0][1], 0.60, face="panic", look=(-1, 0))
    pb.pam(k, LINE6[1][0], LINE6[1][1], PS, "stand", "neutral", look=(-1, 0), glasses="up")
    sb.mfs.mom(k, LINE6[2][0], LINE6[2][1], MS, "stand", "sweet", look=(-1, 0), bag=False)


CAM7C = ((SOF6[0] + GU7[0]) / 2 + 2, 690, 2.2)
S7 = [
    ("9.1", 0.7, dl.shot("s7k", [dl.hc(70, F - 6, GS), dl.hc(180, F - 6, GS)], s7_door, "", chair=False),
     "THE DOOR, tight, shut. Two big shapes fill the glass from outside. THREE SLOW KNOCKS. THE MUSIC STOPS.", ""),
    ("9.1r", 0.5, dl.shot("s7a", [dl.hd(*LINE6[0], 0.60), dl.hp(*LINE6[1], PS), dl.hm(*LINE6[2], MS)], s7_line, "", chair=False, cam=CAM6B, ymin=150),
     "THREE-SHOT, the line-up from scene 6: Don, Pam, Mom. Three pairs of eyes on the door. Don has stopped breathing.", ""),
    ("9.1b", 0.9, dl.shot("9s7b", [dl.hc(70, F - 6, GS), dl.hc(180, F - 6, GS)], dl.s9_1, "", chair=False),
     "THE DOOR again, the same frame, open. Two bodyguards, shoulder to shoulder, bare hands folded. The frame crops their shoulders. HELD IN SILENCE.", ""),
    ("9.2", 1.0, dl.shot("9s7c", [dl.hd(125, F + 22, FS)], s7_gap, "", chair=False),
     "THE SAME FRAME, pushing in. They step apart together. In the gap, smaller than either: FATHER. His face for the first time: Don's face, older and harder, chin down, eyes up from under his brows. He isn't looking at anyone.", ""),
    ("9.2'", 0.7, dl.shot("9s7c2", [dl.hd(125, F + 22, FS)], s7_step, "", chair=False),
     "SAME FRAME, second drawing. One foot forward: one slow step into the room. The bodyguards do not move. Nothing else in the film moves. HELD IN SILENCE.", ""),
    ("9.3", 2.45, dl.shot("9s7d", [dl.hd(FA1[0], FA1[1], FS), dl.ROBOT], dl.s9_3, "", rb=True, chair=False),
     "TWO-SHOT, Father and the robot at its station by the door. Its red scanner beam crosses his chest. He lets it.", "ROBOT: \"Visitor detected. Human approval required.\""),
    ("9.4", 0.7, dl.shot("s7e", [HF2, HD6], s7_thumb(True), "", chair=False, ymin=200),
     "TWO-SHOT, Father and Don. Father has walked in; Don is still in front of the throne. Don opens his mouth and puts a thumb up: approved, obviously. Father looks at him.", ""),
    ("9.4'", 1.4, dl.shot("s7f", [HF2, HD6], s7_thumb(False), "", chair=False, ymin=200),
     "SAME FRAME, second drawing. Father says it to the robot without turning his head. Don's smile dies; he sinks into his collar. THE THUMB STAYS UP, forgotten, shaking. Hold it after the word.", "FATHER: \"Approved.\""),
    ("9.5", 0.9, dl.shot("s7g", [da.RH], da._rb("tick"), "", zmax=3.6, chair=False),
     "CLOSE, the robot. A green tick. It is delighted.", "ROBOT: \"Welcome...\""),
    ("9.5'", 0.8, dl.shot("s7g2", [da.RH], s7_hop, "", zmax=3.6, chair=False),
     "SAME FRAME, second drawing. A happy little hop on its wheel. It is the only thing in the room that is pleased. (Sofía's CV has moved to scene 8.)", "ROBOT: \"...majority shareholder.\""),
]
VER = {1: 2, 2: 2, 3: 2, 4: 3, 5: 2, 6: 3, 7: 3}


def sheet(n, rows, out):
    cols = 6 if len(rows) > 10 else 5; tw, th = 324, 576
    shots_n = len([r for r in rows if "'" not in r[0]])
    cols = 5 if len(rows) <= 10 else (6 if len(rows) <= 12 else (7 if len(rows) <= 14 else 8))
    nrow = (len(rows) + cols - 1) // cols
    Wd, Hd = cols * (tw + 24) + 24, 96 + nrow * (th + 150)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(0.97, 0.95, 0.90); c.paint()
    total = sum(r[1] for r in rows)
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(30)
    c.move_to(24, 44); c.show_text("DADDY'S HOME · SCENE %d of 8 · %s · v%d · %.1f s · %d shots" % (n, SCENES[n], VER[n], total, shots_n))
    c.select_font_face("Inter", 0, 0); c.set_font_size(17)
    c.move_to(24, 72); c.show_text("every frame is the real camera; the red dashes are the bottom line (y 720) and the app's button rail. Nothing is animated yet.")
    t = 0.0
    for i, (sid, dur, fr, what, line) in enumerate(rows):
        big = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); bc_ = cairo.Context(big); bc_.scale(2, 2)
        if isinstance(fr, dict) and "insert" in fr:
            fr["insert"](Ctx(bc_, 0), bc_)
        elif isinstance(fr, str) and fr in da.INSERTS:
            da.INSERTS[fr](Ctx(bc_, 0), bc_)
        else:
            sh = fr if isinstance(fr, dict) else {s_["name"]: s_ for s_ in dl.SHOTS_BLOCKING + dl.SHOTS_NEW + da.EXTRA}[fr]
            dl.draw(sh, Ctx(bc_, 0))
        x0, y0 = 24 + (i % cols) * (tw + 24), 96 + (i // cols) * (th + 150)
        c.save(); c.translate(x0, y0); c.scale(tw / 1080.0, th / 1920.0); c.set_source_surface(big, 0, 0); c.paint(); c.restore()
        c.set_source_rgba(0.9, 0.1, 0.1, 0.55); c.set_line_width(1.5); c.set_dash([6, 4])
        c.move_to(x0, y0 + 720 * th / 960.0); c.line_to(x0 + tw, y0 + 720 * th / 960.0); c.stroke()
        c.rectangle(x0 + 470 * tw / 540.0, y0 + 380 * th / 960.0, 70 * tw / 540.0, 480 * th / 960.0); c.stroke(); c.set_dash([])
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(x0, y0, tw, th); c.stroke()
        c.select_font_face("Inter", 0, 1); c.set_font_size(18)
        c.move_to(x0, y0 + th + 24); c.show_text("%s   %d:%04.1f   %.2f s" % (sid, int(t // 60), t % 60, dur))
        yy = y0 + th + 46
        for txt, bold, col in ((line, 1, (0.72, 0.12, 0.12)), (what, 0, INK)):
            if not txt:
                continue
            c.select_font_face("Inter", 0, bold); c.set_font_size(14); c.set_source_rgb(*col)
            row = ""
            for w_ in txt.split():
                if c.text_extents((row + " " + w_).strip()).x_advance > tw:
                    c.move_to(x0, yy); c.show_text(row); yy += 18; row = w_
                else:
                    row = (row + " " + w_).strip()
            c.move_to(x0, yy); c.show_text(row); yy += 22
        t += dur
    surf.write_to_png(out); print("wrote", out, "%.2f s" % total)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    sheet(n, {1: S1, 2: S2, 3: S3, 4: S4, 5: S5, 6: S6, 7: S7}[n], "../daddys-home/dh_scene%d_v%d.png" % (n, VER[n]))
