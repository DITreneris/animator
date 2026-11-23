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
        dp.ceo_chair(k, CH[0], CH[1], CH[2], sink=1.0 if sunk_chair else 0.0)
        pose = (-8, 0, 128, 124) if not lowered else (-8, 0, 40, 70)
        d = sb.don(k, 452, F + 26, 0.60, pose, face, look=(0.3, 0) if not lowered else (0.6, 0.6))
        _phone_in_hand(k, d, lit, at_ear=not lowered)
    return f


def _don_up(k, o):
    dp.ceo_chair(k, CH[0], CH[1], CH[2], sink=1.0)
    sb.don(k, 452, F + 26, 0.60, "vest", "confused", look=(1, 0.4))


H = dl.hd(452, F + 26, 0.60)
S1 = [   # id, seconds, frame (an insert name or a shot dict), what happens, the line
    ("0.1", 0.75, "0.1", "INSERT. The phone on the throne's gold arm lights up: DAD. It buzzes and slides.", ""),
    ("0.2a", 0.5, "0.2a", "MEDIUM. Don in the throne, feet on the shredder, hands behind his head. His eyes go to the phone; the smile stops.", ""),
    ("0.2b", 0.6, "0.2b", "SAME FRAME. He jolts; PSSSH: the seat drops to the floor under him, knees at his chin.", ""),
    ("0.2c", 0.4, dl.shot("0.2c", [H], _don_up, "", chair=False), "SAME FRAME. He scrambles out, stands straight, pulls his vest down. The throne stays sunk behind him.", ""),
    ("0.3", 1.2, "0.3", "THE BOOTH. A bodyguard's sleeve holds the phone with the one-star post up to him. The ring. No face.", "FATHER: \"Donnie.\""),
    ("0.4", 1.65, dl.shot("0.4", [H], _don_call("happy"), "", chair=False), "CLOSE. The phone at his ear, the sales smile, the first sweat.", "DON: \"Dad! Great timing!\""),
    ("0.5a", 2.0, "0.5", "THE BOOTH. One finger taps the post, once, on \"first\". Nothing else moves.", "FATHER: \"My men go in first.\""),
    ("0.5b", 2.15, dl.shot("0.5b", [H], _don_call("neutral"), "", chair=False), "CLOSE, Don listening. The smile drains off his face while Father's voice goes on, off screen.", "FATHER (off): \"I arrive at five.\""),
    ("0.6", 1.1, dl.shot("0.6", [H], _don_call("confused"), "", chair=False), "CLOSE. The smile is gone. Small.", "DON: \"Tomorrow?\""),
    ("0.7a", 1.2, "0.7", "THE BOOTH. The hand turns the phone face down on the table.", "FATHER: \"Today.\""),
    ("0.7b", 0.45, dl.shot("0.7b", [H], _don_call("panic", lit=False, lowered=True), "", chair=False), "CLOSE. He lowers the phone. The screen is dark. He looks at it.", ""),
]


def sheet(n, rows, out):
    cols = 5; tw, th = 324, 576
    nrow = (len(rows) + cols - 1) // cols
    Wd, Hd = cols * (tw + 24) + 24, 96 + nrow * (th + 150)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd); c = cairo.Context(surf)
    c.set_source_rgb(0.97, 0.95, 0.90); c.paint()
    total = sum(r[1] for r in rows)
    c.set_source_rgb(*INK); c.select_font_face("Inter", 0, 1); c.set_font_size(30)
    c.move_to(24, 44); c.show_text("DADDY'S HOME · SCENE %d of 8 · %s · v1 · %.1f s · %d shots" % (n, SCENES[n], total, len(rows)))
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
    sheet(n, {1: S1}[n], "../daddys-home/dh_scene%d_v1.png" % n)
