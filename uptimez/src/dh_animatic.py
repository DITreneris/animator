"""Daddy's Home: animatic v1. One held key frame a shot (the layout and blocking frames, plus the inserts), the 37 recorded
lines in place, the line as a caption at the top. No motion, no music, no effects: it is for timing and order.
A shot lasts as long as the shot list says, or as long as its lines need, whichever is longer.
  python3 dh_animatic.py  -> ../daddys-home/daddys_home_animatic_v1.mp4 (540x960), dh_animatic_v1.json (the timing)"""
import os
import sys
import json
import math
import subprocess
import numpy as np
import cairo
import soundfile as sf
import kit
import fs_storyboard as sb
import cs_frame as cf
import dh_cast as dc
import dh_props as dp
import dh_poses as dq
import dh_layout as dl
import dh_voices as dv
import pam_bc as pb
import sofia_cs as scs
from kit import Ctx, INK

SR = 48000
F = sb.F
OUT = "../daddys-home/dh_animatic"
GS, SS, PS, MS = dl.GS, dl.SS, dl.PS, dl.MS
RB = (dl.RX, sb.FOOT["robot"], sb.SC["robot"])
RH = (dl.RX, 708.8, 20.0)                                 # where dq.robot_state really puts its face (measured)


def _rb(state):
    return lambda k, o: dq.robot_state(k, RB[0], RB[1], RB[2], state)


def _pose(p):
    return kit.ARM_POSES[p] if isinstance(p, str) and p not in ("stand", "vest") else p


def _don(face, pose="stand", look=(0, 0), zipped=False, filt=False):
    def f(k, o):
        d = (dq.don_zipped if zipped else sb.don)(k, 452, F + 26, 0.60, _pose(pose), face, look=look)
        if filt:
            dp.coffee_run(k, d["head"], 0.60); dp.wet_filter(k, d["head"][0], d["head"][1] - 29, 0.80, -0.12)
    return f


def s7_1a2(k, o):
    sb.mfs.mom(k, 408, F + 8, MS, "stand", "sweet", look=(1, 0))
    sb.don(k, 548, F + 26, 0.60, _pose("panic"), "panic", look=(1, 0))
    scs.sofia(k, 486, F + 4, SS, "hold", "caught", look=(1, 0))


def s7_4(k, o):
    dc.repairman(k, 648, F + 14, GS, case=False, look=(-0.4, 0))


def s10_6(k, o):
    dq.don_block(k, 440, F + 30, 0.60)


EXTRA = [
    dl.shot("0.4", [dl.hd(452, F + 26, 0.60)], _don("happy", (-8, 0, 150, 118)), "", chair=True),
    dl.shot("0.6", [dl.hd(452, F + 26, 0.60)], _don("confused", (-8, 0, 150, 118)), "", chair=True),
    dl.shot("2.2", [dl.hd(452, F + 26, 0.60)], _don("panic", "shock"), "", chair=True),
    dl.shot("3.2", [RH], _rb("idle"), "", zmax=3.6, chair=False),
    dl.shot("4.2", [dl.hp(476, F + 10, SS)], lambda k, o: scs.sofia(k, 476, F + 10, SS, "hold", "caught", look=(-1, 0)), "", chair=True),
    dl.shot("4.3", [dl.hm(384, F + 8, MS)], lambda k, o: sb.mfs.mom(k, 384, F + 8, MS, "wipe", "sweet", look=(0.6, 0.8)), "", chair=True),
    dl.shot("6.3", [dl.hd(408, F + 26, 0.60)], lambda k, o: sb.don(k, 408, F + 26, 0.60, "vest", "smug", look=(-1, 0)), "", chair=False),
    dl.shot("7.1a2", [dl.hm(408, F + 8, MS), dl.hp(486, F + 4, SS), dl.hd(548, F + 26, 0.60)], s7_1a2, "", chair=False, cam=(478, 678, 2.05)),
    dl.shot("7.1c", [dl.hc(648, F + 14, GS)], lambda k, o: dq.visitor_brush(k, 648, F + 14, GS), "", chair=False, cam=(700, 650, 2.2)),
    dl.shot("7.3b", [RH], _rb("rec"), "", zmax=3.6, chair=False),
    dl.shot("7.4", [dl.hc(648, F + 14, GS)], s7_4, "", chair=False, machine="ok", cam=(730, 650, 2.2)),
    dl.shot("7.5", [dl.hd(452, F + 26, 0.60)], _don("confused", filt=True), "", chair=True),
    dl.shot("7.6", [dl.hc(645, F + 14, GS)], lambda k, o: dq.visitor_invoice(k, 645, F + 14, GS), "", chair=False, machine="ok", cam=(730, 650, 2.2)),
    dl.shot("7.8", [dl.hp(652, F + 6, PS)], lambda k, o: pb.pam(k, 652, F + 6, PS, (-8, 0, 60, 118), "neutral", look=(0, 0.6), glasses="up"), "", chair=False, machine="ok"),
    dl.shot("9.5", [RH], _rb("tick"), "", zmax=3.6, chair=False),
    dl.shot("10.3", [dl.hd(452, F + 26, 0.60)], _don("confused", zipped=True, look=(-1, 0)), "", chair=True),
    dl.shot("10.5a", [RH], _rb("turn"), "", zmax=3.6, chair=False),
    dl.shot("10.6", [dl.hd(440, F + 30, 0.60)], s10_6, "", cam=(470, 724, 2.3)),
    dl.shot("10.6b", [RH], _rb("lean_l"), "", zmax=3.6, chair=False),
    dl.shot("10.6c", [RH], _rb("lean_r"), "", zmax=3.6, chair=False),
]


def _insert(fn):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
    fn(Ctx(c, 0), c)
    return surf


def _star(green):
    def f(k, c):
        c.set_source_rgb(0.05, 0.07, 0.10); c.paint()
        dp.star_screen(k, 270, 470, 500, green=green)
    return f


def _pam_sees(k, c):
    c.set_source_rgb(*dc.SUIT); c.paint()
    dc.pass_card(k, 170, 470, 2.6); dc.tool_case(k, 400, 520, 2.4)


def _case(k, c):
    c.set_source_rgb(0.55, 0.38, 0.24); c.paint()
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 540, 420); c.fill()
    dc.case_open(k, 270, 640, 3.6)


def _clock(k, c):
    c.set_source_rgb(0.05, 0.07, 0.10); c.paint()
    c.set_source_rgb(0.45, 0.95, 1.0); c.select_font_face("Inter", 0, 1); c.set_font_size(150)
    e = c.text_extents("16:59"); c.move_to(270 - e.x_advance / 2, 520); c.show_text("16:59")


def _eur(k, c):
    c.set_source_rgb(0.05, 0.07, 0.10); c.paint()
    for txt, size, y, col in (("COFFEE MACHINE", 44, 420, (0.80, 0.88, 0.95)), ("REPAIRED", 60, 500, (0.25, 0.90, 0.40)), ("$80", 110, 640, (1, 1, 1))):
        c.set_source_rgb(*col); c.select_font_face("Inter", 0, 1); c.set_font_size(size)
        e = c.text_extents(txt); c.move_to(270 - e.x_advance / 2, y); c.show_text(txt)


INSERTS = {
    "0.1": lambda k, c: dp.dad_phone(k, True), "11.7": lambda k, c: dp.dad_phone(k, True, buzz=1.0),
    "0.3": lambda k, c: dp.booth(k), "0.5": lambda k, c: dp.booth(k, tap=1.0), "0.7": lambda k, c: dp.booth(k, face_down=True),
    "3.3": _star(True), "10.1": _star(True), "5.4i": _pam_sees, "7.1b": _case, "8.1": _clock, "7.6i": _eur,
}

# the film: (shot, frame, seconds from the shot list, [line keys])
SEQ = [
    ("0.1", "0.1", 1.0, []), ("0.2", "0.2a", 1.0, []), ("0.2", "0.2b", 1.0, []), ("0.3", "0.3", 1.6, ["0.3"]),
    ("0.4", "0.4", 1.4, ["0.4"]), ("0.5", "0.5", 3.0, ["0.5"]), ("0.6", "0.6", 0.9, ["0.6"]), ("0.7", "0.7", 1.6, ["0.7"]),
    ("1.1", "1.1", 1.0, []), ("1.2", "1.2", 2.6, ["1.2"]), ("1.3", "1.3", 1.3, ["1.3"]),
    ("2.1", "2.1", 0.9, []), ("2.2", "2.2", 1.5, ["2.2"]), ("2.3", "2.3", 2.4, ["2.3"]), ("2.4", "2.4", 1.0, ["2.4"]), ("2.5", "2.3", 1.4, []),
    ("3.1", "3.1", 1.6, ["3.1"]), ("3.2", "3.2", 1.5, ["3.2"]), ("3.3", "3.3", 1.6, ["3.3"]), ("3.4", "2.4", 1.0, ["3.4"]), ("3.5", "3.5", 1.2, ["3.5"]),
    ("4.1", "4.1", 2.8, ["4.1"]), ("4.2", "4.2", 0.7, []), ("4.3", "4.3", 1.2, ["4.3"]),
    ("5.1", "5.1", 1.4, []), ("5.2", "5.2", 1.8, ["5.2"]), ("5.3", "0.4", 1.8, ["5.3"]), ("5.4", "5.4", 1.2, []), ("5.4", "5.4i", 1.0, []),
    ("6.1", "6.1", 3.2, ["6.1a", "6.1b"]), ("6.2", "3.2", 1.8, ["6.2"]), ("6.3", "6.3", 1.3, ["6.3"]),
    ("7.1a", "7.1a", 0.9, []), ("7.1a2", "7.1a2", 0.8, []), ("7.1b", "7.1b", 1.8, []), ("7.1c", "7.1c", 1.0, []),
    ("7.2", "7.2", 1.3, []), ("7.3", "7.3", 1.4, []), ("7.3b", "7.3b", 2.4, ["7.3b"]), ("7.4", "7.4", 0.9, ["7.4"]),
    ("7.5", "7.5", 1.0, ["7.5"]), ("7.6", "7.6", 1.0, ["7.6"]), ("7.6", "7.6i", 0.8, []), ("7.8", "7.8", 1.2, ["7.8"]),
    ("8.1", "8.1", 0.6, []), ("8.2", "8.2", 2.6, ["8.2"]), ("8.3", "8.3", 1.8, ["8.3"]), ("8.4", "8.4a", 1.0, []), ("8.4", "8.4b", 1.2, []),
    ("9.1", "9.1", 2.0, []), ("9.2", "9.2", 2.2, []), ("9.3", "9.3", 2.6, ["9.3"]), ("9.4", "9.4", 1.8, ["9.4"]), ("9.5", "9.5", 1.6, ["9.5"]),
    ("9.6", "9.6", 1.4, []),
    ("10.1", "10.1", 2.0, ["10.1"]), ("10.2", "9.2", 2.8, ["10.2"]), ("10.3", "10.3", 0.7, []), ("10.4a", "10.4a", 1.8, ["10.4a"]),
    ("10.4b", "10.4b", 0.4, []), ("10.5a", "10.5a", 1.0, []), ("10.5b", "10.5b", 1.0, []),
    ("10.6", "10.6", 0.6, []), ("10.6", "10.6b", 0.35, []), ("10.6", "10.6", 0.3, []), ("10.6", "10.6c", 0.35, []),
    ("11.1", "9.2", 0.3, []), ("11.2", "10.6", 0.3, []), ("11.3", "4.3", 0.3, []), ("11.4", "7.8", 0.3, []), ("11.5", "7.6", 0.3, []),
    ("11.6", "9.4", 1.6, ["11.6"]), ("11.7", "11.7", 0.8, []),
]
WHO = {"FATHER": "FATHER", "DON": "DON", "SOFIA": "SOFÍA", "PAM": "PAM", "MOM": "MOM", "ROBOT": "ROBOT", "VISITOR": "VISITOR"}


def frames():
    os.makedirs(OUT, exist_ok=True)
    have = {}
    shots = {s["name"]: s for s in dl.SHOTS_BLOCKING + dl.SHOTS_NEW}
    shots.update({s["name"]: s for s in EXTRA})
    need = sorted(set(f for _, f, _, _ in SEQ))
    for name in need:
        if name in INSERTS:
            surf = _insert(INSERTS[name])
        else:
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); c = cairo.Context(surf); c.scale(2, 2)
            dl.draw(shots[name], Ctx(c, 0))
        have[name] = surf
        print("frame", name, flush=True)
    return have


def main(out="../daddys-home/daddys_home_animatic_v1.mp4", fit=None):
    meta = json.load(open(dv.FILM_OUT + "/takes.json"))
    have = frames()
    t = 0.0; plan = []; audio = []
    for i, (shot, frame, est, keys) in enumerate(SEQ):
        need = 0.0; at = []
        for kq in keys:
            a, sr = sf.read("%s/%s.wav" % (dv.FILM_OUT, kq))
            at.append((kq, need + 0.12, a)); need += 0.12 + len(a) / float(SR) + 0.18
        dur = max(est * (fit or 1.0), need)
        dur = round(dur * 30) / 30.0
        for kq, off, a in at:
            audio.append((t + off, a))
        plan.append(dict(shot=shot, frame=frame, t=round(t, 3), dur=round(dur, 3), lines=[(kq, meta[kq]["who"], meta[kq]["text"]) for kq in keys]))
        t += dur
    total = t
    mix = np.zeros(int((total + 0.5) * SR))
    for at_, a in audio:
        i0 = int(at_ * SR); mix[i0:i0 + len(a)] += a[:len(mix) - i0]
    sf.write(OUT + "/voices.wav", mix, SR)
    lst = []
    for n, p in enumerate(plan):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(surf)
        c.scale(0.5, 0.5); c.set_source_surface(have[p["frame"]], 0, 0); c.paint(); c.identity_matrix()
        c.set_source_rgba(0, 0, 0, 0.55); c.rectangle(0, 0, 86, 30); c.fill()
        c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.move_to(8, 21); c.show_text(p["shot"])
        y = 100
        for kq, who, text in p["lines"]:                    # the line, at the top
            c.select_font_face("Inter", 0, 1); c.set_font_size(21)
            words = text.split(); rows = [""]
            for w_ in words:
                if c.text_extents((rows[-1] + " " + w_).strip()).x_advance > 440:
                    rows.append(w_)
                else:
                    rows[-1] = (rows[-1] + " " + w_).strip()
            h = 30 + 27 * len(rows)
            c.set_source_rgba(1, 1, 1, 0.94); c.rectangle(30, y, 480, h); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(30, y, 480, h); c.stroke()
            c.set_source_rgb(0.75, 0.15, 0.15); c.set_font_size(13); c.move_to(42, y + 18); c.show_text(WHO[who])
            c.set_source_rgb(*INK); c.set_font_size(21)
            for r_i, row in enumerate(rows):
                c.move_to(42, y + 42 + 27 * r_i); c.show_text(row)
            y += h + 8
        png = "%s/a_%03d.png" % (OUT, n); surf.write_to_png(png)
        lst.append("file '%s'\nduration %.4f\n" % (os.path.abspath(png), p["dur"]))
    lst.append("file '%s'\n" % os.path.abspath("%s/a_%03d.png" % (OUT, len(plan) - 1)))
    open(OUT + "/list.txt", "w").write("".join(lst))
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", OUT + "/list.txt", "-i", OUT + "/voices.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "20",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % total, tmp])
    os.rename(tmp, out)
    json.dump(dict(total=round(total, 2), plan=plan), open("../daddys-home/dh_animatic_v1.json", "w"), indent=1)
    by = {}
    for p in plan:
        b = p["shot"].split(".")[0]; by[b] = by.get(b, 0) + p["dur"]
    print("total %.1f s, %d frames held" % (total, len(plan)))
    print("by beat:", {k_: round(v, 1) for k_, v in by.items()})
    print("wrote", out)


if __name__ == "__main__":
    main(fit=float(sys.argv[1]) if len(sys.argv) > 1 else None)
