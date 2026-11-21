"""ONE STAR (episode 11): the animation pass, scene 3 "The AI's blueprint" (script v16, beat 03), after layout v2
(one-star-layout-v2.md), timed to cs_voices/film_v4. Native 1080, 12 drawings a second, out at 30 fps.

Layout v2 for this scene:
  3.1  the robot PRINTS (the sheet rolls out of its chest slot); Don's pointing arm by IK; the wall dressed
  3.2  2.0 s: the Client already walking as the shot opens, past Sofía (lapel, earring, into his eyeline)
  3.3  "Recovered.": Don sure of himself; both whole in frame; the AI sheet in both his hands
  3.4  SITE PLAN / RECOVERED BY AI / 99% CONFIDENT; his finger counts the bays round the silhouette (Tomas)
  3.5  "Is this a joke?": tilt, tilt, red; his pocket shows only the blue edge (no readable 7 before 4.3c)
  3.5b the boom swings loose; the plaque whole behind him
  python3 cs_scene3.py [out_dir] [lo]  ->  cs_scene3_v1.mp4, _strip.png, cs_scene3_timing_v1.json"""
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
import cs_board3 as b3
from cs_cal import calendar2
from cs_board import S, at, base
from cs_board2 import blue_sheet
from kit import Ctx, INK, ellipse, rect

V = "v1"
DPS = 12
SR = 48000
TAKES = s1.TAKES
HI = s1.HI
ease, br, Breath = s1.ease, s1.br, s1.Breath
BLUE = (0.18, 0.42, 0.85)
SKIN_CL = sb.SKIN_CL


class Client:
    """For one drawing: the Client's mouth (talking), a lean about his feet (the head tilt reads in the whole
    figure), and his pocket strip as only its blue edge (layout v2: no readable 7 before 4.3c)."""
    def __init__(self, mouth=None, lean=0.0, edge=True):
        self.mouth, self.lean, self.edge = mouth, lean, edge

    def __enter__(self):
        self.oc, self.op = sb.co.client, sb.pocket_strip
        oc, mouth, lean = self.oc, self.mouth, self.lean

        def cl(k, x, feet, s=1.0, pose="arrive", face="confident", look=(0, 0), **kw):
            c = k.c
            c.save(); c.translate(x, feet); c.rotate(math.radians(lean)); c.translate(-x, -feet)
            try:
                return oc(k, x, feet, s, pose, face, look, mouth=mouth, **kw)
            finally:
                c.restore()
        sb.co.client = cl
        if self.edge:
            def edge(k, o, s, x=None, feet=None):
                hx, hy = o["hands"][-1]
                c = k.c
                c.save(); c.translate(hx - 4 * s, hy - 26 * s); c.rotate(-0.35); c.scale(s, s)
                rect(k, -5, -8, 10, 12, BLUE, 771, shadow=False, lw=1.4)            # just the edge above the pocket
                c.restore()
            sb.pocket_strip = edge
        return self

    def __exit__(self, *e):
        sb.co.client, sb.pocket_strip = self.oc, self.op


def talk_code(t, t0, t1):
    if not (t0 <= t <= t1):
        return None
    return ("A", "E", "O", "M", "A", "C")[int((t - t0) * DPS / 2) % 6]


# ---- 3.1 "Blueprint generated." the robot prints ----------------------------------------------------------------------

N31 = 48                                                   # 4.0 s: the two lines hold it
CAM31 = (410, 575, 1.95)                                   # the portrait and its plaque whole above Don and the robot
LINE31R = (0.25, 0.25 + 2.439)
LINE31D = (2.889, 2.889 + 0.718)
PRINT = (0.3, 2.6)                                         # the sheet rolls out (s)
DON_SH_L = (428.0, 679.6)
LN = 48 * 0.60
POINT_AT = (392.0, 690.0)                                  # his finger toward the robot (not touching)


def s3_1(k, d):
    """48 drawings. Don points at the robot (recover it) and looks away to the door; the robot speaks, its visor
    PRINTING, and a long glossy blue sheet rolls out of its chest slot, curling on the floor; "Approved." unread."""
    from cand_bc import ik
    t = d / float(DPS)
    p = ease(t / 0.4)
    if t > LINE31R[1]:
        p = 1 - ease((t - LINE31R[1]) / 0.4)                                       # the arm drops as it finishes
    tx, ty = A.lerp((420.0, 736.6), POINT_AT, p)
    a1, a2 = ik(DON_SH_L[0], DON_SH_L[1], tx, ty, LN, LN, 1)
    talk = 0.0
    if LINE31D[0] <= t <= LINE31D[1]:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - LINE31D[0]) * DPS / 2) % 4]
    L = ease((t - PRINT[0]) / (PRINT[1] - PRINT[0]))

    def ex(k_, o):
        c = k_.c
        sx, sy = o["robot"]["screen"]
        r = 50 * sb.SC["robot"]
        ellipse(k_, sx, sy, 0.80 * r, 0.62 * r, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        if L < 1:                                                                  # the visor: PRINTING and a bar
            cp.T(c, "PRINT", sx, sy - 0.02 * r, 0.30 * r, col=cp.CYAN)
            c.set_source_rgb(*cp.CYAN); c.rectangle(sx - 0.45 * r, sy + 0.14 * r, 0.9 * r * L, 0.12 * r); c.fill()
        else:
            c.set_source_rgb(*cp.GRN); c.set_line_width(0.12 * r); c.set_line_cap(1)
            c.move_to(sx - 0.3 * r, sy); c.line_to(sx - 0.08 * r, sy + 0.22 * r); c.line_to(sx + 0.34 * r, sy - 0.25 * r); c.stroke()
        if L > 0:                                                                  # the sheet out of the chest slot,
            bx, by = sx - 0.35 * r, sy + 1.45 * r                                   # out to its left and down to the
            w = 1.3 * r                                                             # floor, like a receipt
            floor = sb.F + 4
            reach = 0.9 * r * min(1.0, L * 3)                                      # first it comes out sideways
            c.set_source_rgb(*BLUE); c.rectangle(bx - reach, by - 0.2 * r, reach + 0.3 * r, 0.4 * r); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(bx - reach, by - 0.2 * r, reach + 0.3 * r, 0.4 * r); c.stroke()
            if L > 0.33:                                                           # then it hangs and grows to the floor
                drop = (floor - by) * min(1.0, (L - 0.33) / 0.6)
                x0 = bx - 0.9 * r - w / 2
                c.save(); c.rectangle(x0, by - 0.2 * r, w, drop + 0.2 * r); c.clip()
                blue_sheet(k_, x0 + w / 2, by + (floor - by) / 2, w, floor - by + 0.4 * r, 0.0)
                c.restore()
                if L >= 0.93:                                                      # it curls on the floor
                    ellipse(k_, x0 + w / 2 - 0.3 * r, floor - 0.12 * r, w * 0.65, 0.18 * r, (0.20, 0.45, 0.85), 992, shadow=False, lw=1.3)

    with A.Don(A.MOUTH, talk), Breath(sb, "don", br(d)), Breath(sb, "robot", br(d, 0.5, 0.006)):
        S(k, CAM31, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm="none"),
                 dn=at("don", pose=(a1, a2, 8, 0), face="smug", look=(-1, -0.1))))


# ---- 3.2 9:00: he walks in, past her -----------------------------------------------------------------------------------

N32 = 24
CAM32 = (372, 590, 1.9)                                    # the plaque whole (v1 test: cut at the right)
WALK = (215.0, 430.0)                                      # his x across the shot
SOF = (392.0, 370.0)                                       # she steps into his line


def s3_2(k, d):
    """24 drawings (2.0 s). The door at 9:00. He is already walking (a bob each step), eyes on Don off right; Sofía
    smooths her lapel, steps into his eyeline; he walks straight past her; her smile at his back."""
    u = d / float(N32 - 1)
    x = WALK[0] + (WALK[1] - WALK[0]) * u
    bob = abs(math.sin(math.pi * d / 3.0)) * 3.0                                   # a step every 3 drawings
    sx = SOF[0] + (SOF[1] - SOF[0]) * ease((d - 4) / 5.0)
    past = x > sx + 10
    sface = "knowing" if not past else "caught"
    spose = "lapel" if d < 12 else "hold"

    def back(k_):
        calendar2(k_)

    with Client(lean=1.5 if d % 3 else 0.5), Breath(s1.sofia_fs, "sofia", br(d, 0.6)):
        S(k, CAM32, auto=False, portrait="hang", back=back,
          **base(door=0.85, rb=False, dn=False, pm=False, mm=False,
                 sf=at("sofia", x=sx, pose=spose, face=sface, look=(-1, 0) if not past else (1, 0)),
                 cl=at("client", x=x, feet=sb.FOOT["client"] - bob, face="plain", look=(1, 0))))


# ---- 3.3 "Recovered." ---------------------------------------------------------------------------------------------------

N33 = 17
CAM33 = (372, 562, 1.75)                                   # both whole; the logo out of frame, the plaque whole
LINE33 = (0.25, 0.25 + 0.835)
HOLD = (25, 100, -25, -100)                                  # both his hands in front of his chest


def s3_3(k, d):
    """17 drawings (1.4 s). Don, sure of himself, unrolls the AI's sheet with a flourish to the Client: the sheet
    drops open from his two fists; "Recovered."; the Client looks at it, flat."""
    t = d / float(DPS)
    talk = 0.0
    if LINE33[0] <= t <= LINE33[1]:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - LINE33[0]) * DPS / 2) % 4]
    U = ease(d / 5.0)

    def ex(k_, o):
        (lx, ly), (rx, ry) = o["don"]["hands"]
        top = min(ly, ry) - 4
        w = abs(rx - lx) + 30
        h = 20 + 100 * U
        cx = (lx + rx) / 2
        c = k_.c
        c.save(); c.rectangle(cx - w / 2, top, w, h); c.clip()
        blue_sheet(k_, cx, top + 60, w, 120, 0.0)
        c.restore()
        if U < 1:                                                                  # the roll still at its foot
            ellipse(k_, cx, top + h, w / 2 + 2, 5, (0.16, 0.38, 0.78), 993, shadow=False, lw=1.4)
        sk = kit.PEOPLE["DON"]["skin"]
        for hx, hy, sd in ((lx, ly, 994), (rx, ry, 995)):                          # his fists over its top corners
            ellipse(k_, hx, hy, 5.2, 5.6, sk, sd, shadow=False, lw=1.2)

    with A.Don(A.MOUTH, talk), Breath(sb, "don", br(d, 0.0, 0.010)), Client(), Breath(sb, "client", br(d, 0.4)):
        S(k, CAM33, auto=False, portrait="hang",  extra=ex,
          **base(rb=False, sf=False, pm=False, mm=False, door=0.0,
                 cl=at("client", x=280, face="plain", look=(1, 0.5)),
                 dn=at("don", x=450, pose=HOLD, face="grin" if talk == 0 else "happy", look=(-1, 0))))


# ---- 3.4 the AI's site plan -------------------------------------------------------------------------------------------

N34 = 24


def _bays():
    """The twelve bays' centres, in ai_site's order (unscaled layout)."""
    out = []
    for cx_, cy_, a0 in ((206, 690, 2.2), (334, 690, -0.6)):
        for i in range(3):
            a_ = a0 + i * 0.95
            out.append((cx_ + math.cos(a_) * 100, cy_ + math.sin(a_) * 100))
    for i in range(3):
        for sx in (-1, 1):
            out.append((270 + sx * 74, 600 - i * 104))
    return out


def finger(k, x, y, ang=0.15):
    """His thick oily finger from below, the olive sleeve behind it."""
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(k, -40, 120, 80, 400, (0.42, 0.44, 0.24), 951, lw=3)                       # the sleeve
    rect(k, -32, 100, 64, 30, (0.98, 0.97, 0.94), 952, shadow=False, lw=2.5)       # the cuff
    rect(k, -26, 0, 52, 110, SKIN_CL, 953, shadow=False, lw=3)                       # the finger
    ellipse(k, 0, 2, 26, 22, SKIN_CL, 954, shadow=False, lw=3)
    ellipse(k, 0, -2, 13, 11, (0.95, 0.86, 0.80), 955, shadow=False, lw=1.5)       # the nail
    c.set_source_rgba(0.15, 0.13, 0.10, 0.35)                                      # oil in the creases
    for yy in (38, 62):
        c.set_line_width(3); c.move_to(-18, yy); c.line_to(18, yy + 2); c.stroke()
    c.restore()


def s3_4(k, d):
    """24 drawings (2.0 s). SITE PLAN / RECOVERED BY AI / 99% CONFIDENT. His finger counts the bays round the
    outline, 1 to 12 (it traces the silhouette); then it stops and comes off: the whole shape, held; a slow pull
    back so it lands."""
    c = k.c
    z = 1.12 - 0.12 * ease((d - 12) / 10.0)
    c.save(); c.translate(270, 520); c.scale(z, z); c.translate(-270, -520)
    old = cp.PROPS4[0]; cp.PROPS4[0] = False
    try:
        cp.ai_site(k)
    finally:
        cp.PROPS4[0] = old
    c.set_source_rgb(0.20, 0.45, 0.85); c.rectangle(36, 126, 468, 128); c.fill()   # the three levels of the title
    cp.T(c, "SITE PLAN", 270, 172, 44, col=(1, 1, 1))
    cp.T(c, "RECOVERED BY AI", 270, 206, 22, col=(0.85, 0.92, 1.0))
    cp.T(c, "99% CONFIDENT", 270, 248, 38, col=(1, 0.9, 0.3))
    bays = _bays()
    order = [0, 1, 2, 7, 9, 11, 10, 8, 6, 3, 4, 5]                                # up one side, round, down the other
    if d < 16:
        i = min(len(order) - 1, int(d * 12 / 15.0))
        bx, by = bays[order[i]]
        finger(k, bx + 8, by + 20, 0.12)
    elif d < 19:
        bx, by = bays[order[-1]]
        finger(k, bx + 8, by + 20 + (d - 15) * 90, 0.12)                           # it comes off, down
    c.restore()


# ---- 3.5 "Is this a joke?" ---------------------------------------------------------------------------------------------

N35 = 20
CAM35 = (250, 640, 3.0)
LINE35 = (0.25, 0.25 + 1.074)
TILT = [0, 0, 3, 4, 4, 1, 0, 4, 6, 6, 6, 5, 3, 2, 1, 0, 0, -2, -3, -3]


def s3_5(k, d):
    """20 drawings (1.7 s). He tilts his head; again, more; he gets it: red from the collar up; "Is this a joke?" at
    Don; then he turns for the door."""
    t = d / float(DPS)
    code = talk_code(t, *LINE35)
    flush = min(0.45, max(0.0, (d - 6) / 6.0) * 0.45)
    look = (1, 0) if d < 16 else (-1, 0)
    with Client(mouth=code, lean=TILT[d]), Breath(sb, "client", br(d, 0.4, 0.012)):
        S(k, CAM35, auto=False, portrait=False,
          **base(rb=False, sf=False, dn=False, pm=False, mm=False, door=0.0,
                 cl=at("client", face="suspicious", look=look)))
    if flush > 0:
        b3.flush(k, "client", flush)


# ---- 3.5b Don's flash of panic; the boom swings loose -------------------------------------------------------------------

N35b = 8
CAM35b = (452, 590, 2.6)                                   # = 5.4c's framing: the plaque whole under the bar


def s3_5b(k, d):
    pts = A.lerp(A.MOUTH, A.CROOKED4, A.SWING[d])
    with A.Don(pts), Breath(sb, "don", br(d, 0.0, 0.012)):
        S(k, CAM35b, auto=False, mic="down", portrait="hang",
          **base(cl=False, sf=False, rb=False, pm=False, mm=False, door=0.0,
                 dn=at("don", face="panic" if d >= 2 else "smug", look=(-1, 0) if d < 2 else (-1, -0.3))))


SHOTS = [("3.1", N31, s3_1), ("3.2", N32, s3_2), ("3.3", N33, s3_3), ("3.4", N34, s3_4), ("3.5", N35, s3_5),
         ("3.5b", N35b, s3_5b)]


def starts():
    out, n = {}, 0
    for sh, nd, _ in SHOTS:
        out[sh] = n / float(DPS); n += nd
    return out


def schedule():
    st = starts()
    return [("3.1r", st["3.1"] + LINE31R[0]), ("3.1d", st["3.1"] + LINE31D[0]), ("3.3", st["3.3"] + LINE33[0]),
            ("3.5", st["3.5"] + LINE35[0])]


def draw(fn, d):
    return s1.draw(fn, d)


def main(out_dir):
    tmp = "/tmp/cs_s3"; os.makedirs(tmp, exist_ok=True)
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
    out = os.path.join(out_dir, "cs_scene3_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in schedule()]},
              open("cs_scene3_timing_%s.json" % V, "w"), indent=1)
    A.strip(tiles[::2], os.path.join(out_dir, "cs_scene3_%s_strip.png" % V), 160, 10)
    print("wrote", out, "%d drawings, %.2f s" % (n, total))


if __name__ == "__main__":
    if "lo" in sys.argv[1:]:
        HI[0] = 1
    args = [a for a in sys.argv[1:] if a != "lo"]
    main(args[0] if args else "../customer-success")
