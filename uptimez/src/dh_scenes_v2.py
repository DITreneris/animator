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


def s2_wipe(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    d = sb.don(k, 452, F + 26, 0.60, (-8, 0, 152, 96), "confused", look=(0.4, 0.5))
    _sweat(k, d, 1)


def s2_reports(k, o):
    q = scs.sofia(k, SOF[0], SOF[1], SS, "chest", "deadpan", look=(-1, 0))
    c = k.c
    hx, hy = min(q["hands"], key=lambda h_: h_[1])
    c.save(); c.translate(hx, hy - 6); c.rotate(-0.06)
    kit.rect(k, -32, -30, 64, 46, (0.86, 0.72, 0.36), 3301, lw=2)
    kit.text(k, "REPORTS", 0, -4, 11, INK)
    c.restore()


def s2_jump(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=1.0)
    sb.don(k, 452, F + 12, 0.60, kit.ARM_POSES["shock"], "panic", look=(1, 0))      # off the floor
    _lines(k, [(424, F + 22, 414, F + 30), (452, F + 24, 452, F + 34), (480, F + 22, 490, F + 30)])


def s2_kick(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], seat_drop=0.25)
    kx, ky = CH[0] + 122 * CH[2], CH[1] - 69 * CH[2]                                  # the lever's knob
    _lines(k, [(kx + 10, ky - 8, kx + 22, ky - 16), (kx + 12, ky, kx + 26, ky), (kx + 10, ky + 8, kx + 22, ky + 16),
               (CH[0] - 30, CH[1] - 124 * CH[2], CH[0] - 30, CH[1] - 140 * CH[2]), (CH[0] + 30, CH[1] - 124 * CH[2], CH[0] + 30, CH[1] - 140 * CH[2])])
    sb.don(k, 440, F + 26, 0.60, "vest", "smug", look=(1, 0))


def s2_push(k, o):
    dp.ceo_chair(k, 352, CH[1], CH[2], lean=-0.07)
    _lines(k, [(420, F - 150, 446, F - 150), (424, F - 110, 450, F - 110), (420, F - 70, 446, F - 70)])
    sb.don(k, 478, F + 26, 0.60, (-96, -8, 8, 0), "smug", look=(1, 0))


def s2_what(k, o):
    pb.pam(k, PAM[0], PAM[1], PS, "stand", "neutral", look=(-1, 0.15), glasses="up")


def s2_back(k, o):
    dp.ceo_chair(k, 404, CH[1], CH[2], lean=0.05)
    _lines(k, [(300, F - 150, 326, F - 150), (296, F - 110, 322, F - 110), (300, F - 70, 326, F - 70)])
    sb.don(k, 478, F + 26, 0.60, (-50, -10, 8, 0), "smug", look=(1, 0))


HD = dl.hd(452, F + 26, 0.60)
TWO = (420, 694, 2.1)                                      # Don and the throne, the throne to his left
S2 = [
    ("1.1", 0.5, dl.shot("s2a", [dl.hp(SOF[0], SOF[1], SS), dl.hp(PAM[0], PAM[1], PS)], s2_stare, "", chair=False),
     "TWO-SHOT. Sofía and Pam, both looking left at him. Nobody moves.", ""),
    ("1.2", 2.5, dl.shot("s2b", [HD], s2_news, "", chair=False),
     "MEDIUM. Arms wide, the salesman's smile. Two drops of sweat on his bald head; one runs down. The throne behind him still has its seat on the floor.",
     "DON: \"Good news, everyone! My father's coming!\""),
    ("1.3", 1.25, dl.shot("s2c", [dl.hp(SOF[0], SOF[1], SS)], s2_alone, "", chair=False),
     "CLOSE. Her eyes are on the sweat, above his face. A real question.", "SOFÍA: \"Is he coming alone?\""),
    ("1.3b", 0.6, dl.shot("s2d", [HD], s2_wipe, "", chair=False),
     "CLOSE. He wipes his head with his sleeve and looks at the floor. No answer: that is the answer.", ""),
    ("2.1", 0.7, dl.shot("s2e", [dl.hp(SOF[0], SOF[1], SS)], s2_reports, "", chair=False),
     "MEDIUM. She lifts a folder to her chest: REPORTS. Says nothing.", ""),
    ("2.2", 1.5, dl.shot("s2f", [dl.hd(452, F + 12, 0.60)], s2_jump, "", chair=False),
     "CLOSE. He jumps off the floor as if she had pulled a gun.", "DON: \"I didn't steal anything!\""),
    ("2.3a", 0.5, dl.shot("s2g", [dl.hd(440, F + 26, 0.60)], s2_kick, "", chair=False, cam=TWO),
     "TWO-SHOT, Don and the throne. Chin up again. Without looking he heels the lever: PFFT, the seat pops back up.", "DON: \"The money...\""),
    ("2.3b", 1.2, dl.shot("s2h", [dl.hd(478, F + 26, 0.60)], s2_push, "", chair=False, cam=TWO),
     "SAME FRAME. Eyes on Sofía, he shoves the throne away to the left with one hand. It rolls out of frame.", "DON: \"...was invested.\""),
    ("2.4", 1.0, dl.shot("s2i", [dl.hp(PAM[0], PAM[1], PS)], s2_what, "", chair=False),
     "CLOSE. Pam at the end of the counter. Her eyes follow something moving back from the left.", "PAM: \"Into what?\""),
    ("2.5", 1.3, dl.shot("s2j", [dl.hd(478, F + 26, 0.60)], s2_back, "", chair=False, cam=TWO),
     "TWO-SHOT. The throne rolls slowly back in and bumps his legs. Still smiling at Sofía, he pushes it off again without looking. It starts back at once.", ""),
]
VER = {1: 2, 2: 1}


def sheet(n, rows, out):
    cols = 6 if len(rows) > 10 else 5; tw, th = 324, 576
    nrow = (len(rows) + cols - 1) // cols
    Wd, Hd = cols * (tw + 24) + 24, 96 + nrow * (th + 150)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(0.97, 0.95, 0.90); c.paint()
    total = sum(r[1] for r in rows)
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(30)
    c.move_to(24, 44); c.show_text("DADDY'S HOME · SCENE %d of 8 · %s · v%d · %.1f s · %d shots" % (n, SCENES[n], VER[n], total, len(rows)))
    c.select_font_face("Inter", 0, 0); c.set_font_size(17)
    c.move_to(24, 72); c.show_text("every frame is the real camera; the red dashes are the bottom line (y 720) and the app's button rail. Nothing is animated yet.")
    t = 0.0
    for i, (sid, dur, fr, what, line) in enumerate(rows):
        big = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); bc_ = cairo.Context(big); bc_.scale(2, 2)
        if isinstance(fr, str) and fr in da.INSERTS:
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
    sheet(n, {1: S1, 2: S2}[n], "../daddys-home/dh_scene%d_v%d.png" % (n, VER[n]))
