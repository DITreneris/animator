"""ONE STAR (episode 11): the animation pass, scene 2 "The call" (script v16, beat 02), timed to cs_voices/film_v4.
Drawn natively at 1080 (2x), 12 drawings a second, out at 30 fps. Same rules as scene 1 (cs_scene1.py).

Tomas chose (20 Nov, /grill-me):
  2.1  the FRI calendar behind Don, and the calendar redrawn (cs_cal.calendar2: "like a stupid stick, not a calendar")
  2.2  the calendar fills in on Don's phone as the Client says it; then the call ends (he hung up)
  python3 cs_scene2.py [out_dir] [lo]  ->  cs_scene2_v1.mp4, cs_scene2_v1_strip.png, cs_scene2_timing_v1.json"""
import json
import math
import os
import subprocess
import sys
import cairo
import numpy as np
import soundfile as sf
import kit
import fs_storyboard as sb
import cs_props as cp
import cs_anim as A
import cs_scene1 as s1
from cs_cal import calendar2, CAL_AT
from cs_board import S, at, base
from kit import Ctx, INK, ellipse, rect

V = "v3"                                                   # v2: the series' face scale (Tomas); v1 kept in cs_scene2_v1.py
DPS = 12
SR = 48000
TAKES = s1.TAKES
HI = s1.HI
ease, br, Breath = s1.ease, s1.br, s1.Breath

# ---- 2.1a the call goes out --------------------------------------------------------------------------------------------

N21a = 6


def s2_1a(k, d):
    """6 drawings: CALLING 10 GARAGES; the rings pulse out of his avatar, the dots of "calling..." count up."""
    c = k.c
    old = cp.GARAGE_LOGO[0]; cp.GARAGE_LOGO[0] = True
    try:
        cp.phone2(k, "calling")
    finally:
        cp.GARAGE_LOGO[0] = old
    cx, cy = 270, 70 + 230
    for i in range(2):                                                          # two rings going out
        r = 120 + ((d * 14 + i * 40) % 80)
        c.set_source_rgba(*cp.GRN, max(0.0, 0.5 - (r - 120) / 160.0)); c.set_line_width(5)
        c.new_path(); c.arc(cx, cy, r, 0, 6.3); c.stroke()
    c.set_source_rgb(*cp.LIGHT); c.rectangle(150, 70 + 455, 240, 50); c.fill()   # "calling" with its dots counting
    cp.T(c, "calling" + "." * (1 + d % 3), 270, 70 + 490, 36, col=cp.GREY, bold=False)


# ---- 2.1 "Let's fix this together." ------------------------------------------------------------------------------------

N21 = 26
CAM21 = (404, 693, 3.1)                                     # v2: Don's face r 78 at y ~375, the plaque out of frame
CAL21 = (252, 470, 2.62)                                   # v2: the shot opens on the FRI calendar, whole (Tomas's 2.1 choice),
PAN21 = (5, 13)                                            # and pans down to Don as he talks (v1: Don small and low, to fit both)
LINE21 = 0.25                                              # his line in the shot (s)
SH_R = (476.0, 679.6)                                      # his screen-right shoulder (measured)
LN = 48 * 0.60
HEAD = (452.0, 644.8)
PHONE_ARM = (-150, -40)                                    # his screen-left hand at his ear (the mirror of "thumb")
HEART = (462.0, 704.0)                                     # his hand on his heart (on his vest, under the badge)
REST_R = (484.0, 736.6)
FLICK = [0.0, 0.0, 0.0, 0.35, 0.85, 1.12, 0.95, 1.0]        # the boom: UP to his mouth, a small bounce


FLICK_AT = 9                                               # v2: he flicks the mic as the pan lands on him


def _boom(d):
    d = max(0, d - FLICK_AT)
    t = FLICK[min(d, len(FLICK) - 1)]
    return A.lerp(A.UP, A.MOUTH, t)


def _grip(pts):
    q = pts
    gx = 0.125 * q[0] + 0.375 * q[2] + 0.375 * q[4] + 0.125 * q[6]
    gy = 0.125 * q[1] + 0.375 * q[3] + 0.375 * q[5] + 0.125 * q[7]
    s = sb.SC["don"]
    return HEAD[0] + gx * s, HEAD[1] + gy * s


def _right_arm(d, pts):
    """d 0-2 up to the boom; 3-6 riding it down; 7-12 to his heart; held there. IK from the shoulder, elbow out."""
    from cand_bc import ik
    g = _grip(pts)
    d = d - FLICK_AT + 2                                                          # v2: the same moves, later
    if d < 0:
        tx, ty = REST_R
        a1, a2 = ik(SH_R[0], SH_R[1], tx, ty, LN, LN, -1)
        return a1, a2
    if d <= 2:
        tx, ty = s1.A.lerp(REST_R, g, ease(d / 2.0))
    elif d <= 6:
        tx, ty = g
    else:
        tx, ty = s1.A.lerp(g, HEART, ease((d - 6) / 6.0))
    a1, a2 = ik(SH_R[0], SH_R[1], tx, ty, LN, LN, -1)
    return a1, a2


def s2_1(k, d):
    """26 drawings (2.17 s). On the phone to the Client, the new calendar behind him: he flicks his mic down to his
    mouth (sales mode), then lays his hand on his heart; the sales smile, eyes shut, talking on twos."""
    t = d / float(DPS)
    pts = _boom(d)
    a1, a2 = _right_arm(d, pts)
    talk = 0.0
    if LINE21 <= t <= LINE21 + 1.5:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - LINE21) * DPS / 2) % 4]

    def back(k_):
        calendar2(k_, *CAL_AT)

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["don"]["hands"]
        hx, hy = (lx, ly) if lx < rx else (rx, ry)                                # the phone hand: screen-left, at his ear
        c = k_.c
        c.save(); c.translate(hx + 3, hy + 14); c.rotate(-0.12)
        rect(k_, -6, -12, 12, 24, s1.PHONE, 971, lw=1.3)
        c.restore()
        sk = kit.PEOPLE["DON"]["skin"]
        ellipse(k_, hx, hy + 8, 5.2, 5.6, sk, 972, shadow=False, lw=1.2)          # his fingers round it
        if 0 <= d - FLICK_AT + 2 <= 6:                                             # his other hand on the boom, over it
            gx, gy = _grip(pts)
            ellipse(k_, gx, gy, 5.0, 5.4, sk, 973, shadow=False, lw=1.2)

    with A.Don(pts, talk), Breath(sb, "don", br(d, 0.0, 0.010)):
        u = ease((d - PAN21[0]) / float(PAN21[1] - PAN21[0]))
        cam = tuple(a_ + (b_ - a_) * u for a_, b_ in zip(CAL21, CAM21))
        S(k, cam, auto=False, portrait="hang", back=back, extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, rb=False, door=0.0,
                 dn=at("don", pose=PHONE_ARM + (a1, a2), face="happy", look=(1, 0))))


# ---- 2.2 "Nine o'clock. Your office." -----------------------------------------------------------------------------------

N22 = 32                                                   # CALL ENDED held half a second
LINE22 = (0.25, 1.946)


def s2_2(k, d):
    """28 drawings (2.33 s). Don's phone, on the call: the Client's voice through it; the calendar entry fills in as he
    says it (FRI, then 9:00, then CLIENT · 10 GARAGES); then CALL ENDED: he hung up."""
    c = k.c
    t = d / float(DPS)
    ph = 2 * math.pi * d / float(DPS) / A.BREATH
    c.set_source_rgb(0.24, 0.22, 0.20); c.paint()
    c.save(); c.translate(270, 480); c.rotate(math.radians(0.35 * math.sin(ph))); c.translate(-270, -480 + 2.0 * math.sin(ph))
    x0, y0, w = cp._phone(k, 950)
    cx = x0 + w / 2
    u = (t - LINE22[0]) / (LINE22[1] - LINE22[0])                                 # how far through his line
    c.set_source_rgb(*cp.GRN); c.rectangle(x0, y0, w, 40); c.fill()                # on a call: the green bar
    cp.T(c, "10 GARAGES · 0:%02d" % (14 + int(t)), cx, y0 + 29, 24, col=(1, 1, 1))
    c.set_source_rgb(*cp.RED); c.rectangle(x0, y0 + 40, w, 140); c.fill()      # his calendar open on Friday, empty
    cp.T(c, "FRI", cx, y0 + 40 + 108, 90, col=(1, 1, 1))
    c.set_source_rgb(0.85, 0.86, 0.90); c.set_line_width(2)
    for i in range(3):                                                             # the rest of the day, empty, under it
        c.move_to(x0 + 30, y0 + 600 + i * 70); c.line_to(x0 + w - 30, y0 + 600 + i * 70); c.stroke()
    if u > 0.25:                                                                   # "Nine o'clock."
        cp.T(c, "9:00", cx, y0 + 340, 110)
    if u > 0.6:                                                                   # "Your office."
        cp.T(c, "CLIENT", cx, y0 + 450, 60, col=cp.RED)
        cp.T(c, "10 GARAGES", cx, y0 + 520, 36, col=cp.GREY, bold=False)
    if t > LINE22[1] + 0.15:                                                       # he hung up on Don
        c.set_source_rgb(*cp.RED); c.rectangle(x0, y0, w, 40); c.fill()
        cp.T(c, "CALL ENDED", cx, y0 + 29, 24, col=(1, 1, 1))
    c.restore()


SHOTS = [("2.1a", N21a, s2_1a), ("2.1", N21, s2_1), ("2.2", N22, s2_2)]


def schedule():
    t21 = N21a / float(DPS); t22 = (N21a + N21) / float(DPS)
    return [("2.1", t21 + LINE21), ("2.2", t22 + LINE22[0])]


def draw(fn, d):
    return s1.draw(fn, d)


def main(out_dir):
    tmp = "/tmp/cs_s2"; os.makedirs(tmp, exist_ok=True)
    lst, n, tiles = open(tmp + "/list.txt", "w"), 0, []
    for shot, nd, fn in SHOTS:
        for d in range(nd):
            f = draw(fn, d)
            p = "%s/d%03d.png" % (tmp, n); f.write_to_png(p)
            lst.write("file '%s'\nduration %.6f\n" % (p, 1.0 / DPS))
            tiles.append(("#%d %s %.2f s" % (n + 1, shot, n / float(DPS)), f)); n += 1
    lst.write("file '%s'\n" % p); lst.close()
    total = n / float(DPS)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp + "/v.mp4"], check=True)
    meta = json.load(open(TAKES + "/takes.json"))
    a = np.zeros(int((total + 0.3) * SR))
    for key, t0 in schedule():
        x, _ = sf.read("%s/%s.wav" % (TAKES, key))
        p_ = int(t0 * SR); a[p_:p_ + len(x)] += x[:len(a) - p_]
    sf.write(tmp + "/a.wav", (a / max(1e-9, np.abs(a).max()) * 0.7).astype(np.float32), SR)
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "cs_scene2_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in schedule()]},
              open("cs_scene2_timing_%s.json" % V, "w"), indent=1)
    A.strip(tiles, os.path.join(out_dir, "cs_scene2_%s_strip.png" % V), 160, 10)
    print("wrote", out, "%d drawings, %.2f s" % (n, total))


if __name__ == "__main__":
    if "lo" in sys.argv[1:]:
        HI[0] = 1
    args = [a for a in sys.argv[1:] if a != "lo"]
    main(args[0] if args else "../customer-success")
