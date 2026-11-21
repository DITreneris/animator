"""ONE STAR (episode 11): the animation pass, scene 1 "The post" (script v13, beat 01, 0:00-0:09), timed to the voice
takes (cs_voices/film_v3) on animatic v3's clock. Drawn natively at 1080 (2x), 12 drawings a second, out at 30 fps.

Tomas chose (20 Nov, /grill-me):
  1.1  every phone IN a hand (lesson 70): heads down on the phones, then they turn to Don one after another
  1.4  the portrait and OUR FIRST CLIENT whole behind Don and the robot (close shots stay in the dressed room)
  1.4b the reply posts while we watch (the change happens on screen)
  the robot: its visor blinks, REPLY types out while it speaks, a green tick on "Approved."

The day's rules, per shot: canon sizes (fs_storyboard._norm), arms from the shoulders, props in hands, everyone
breathes (no frozen holds), signs whole and under the bar, nobody cut by the frame.
  python3 cs_scene1.py [out_dir] [lo]  ->  cs_scene1_v1.mp4, cs_scene1_v1_strip.png  (lo: 540, for a quick look)"""
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
import pam_bc as pb
import mom_fs as mf
import mom_on as mo
import sofia_fs
import cs_props as cp
import cs_anim as A
from cs_board import S, at, base, calendar_on
from kit import Ctx, INK, ellipse, rect

V = "v7"                                                   # v2: Don's reach by IK; v3: the reply "Our AI does not lose files."
                                                           # (script v14). v1, v2 kept in cs_scene1_v1.py, cs_scene1_v2.py
DPS = 12
SR = 48000
TAKES = "cs_voices/film_v4"                                # v5: + the post (Client) and the reply (robot), read aloud
HI = [2]

# the pose with the phone in the right hand at the chest (kit's convention; Mom's own IK, her left on the bag side)
kit.ARM_POSES.setdefault("phone_r", (-8, 0, -12, -112))
mf._body.__globals__["POSES"].setdefault("phone_r", mo.ik(-1, -30, mf.WAIST + 2) + mo.ik(1, 6, mf.BT + 52))

WIDE1 = (487, 565, 1.20)                                   # the calendar, the portrait and Mom all whole, no strip of void below
TWO14 = (455, 410, 2.6)                                    # v7: opens on the portrait and its plaque, whole
TWO14_IN = (412, 707, 2.6)                                 # v7: tilts down to Don and the robot at the series' face
                                                           # scale (r 78, faces about y 400), the robot above the apps' bottom quarter                                # the push-in's end: Don, the robot's visor and his thumb on it
PUSH = (0.3, 1.6)                                          # the camera eases in while the robot speaks (s): the portrait
                                                           # watches first, then we land on the unread approval
                                  # Don and the robot, the portrait and its plaque whole above them
PHONE = (0.10, 0.11, 0.14)
GLOW = (0.6, 0.9, 1.0)


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Breath:
    """Scales a draw function a hair taller about the feet (module attribute patched for one drawing)."""
    def __init__(self, mod, name, sy):
        self.mod, self.name, self.sy = mod, name, sy

    def __enter__(self):
        self.orig = getattr(self.mod, self.name)
        orig, sy = self.orig, self.sy

        def w(k, x, feet, *a, **kw):
            c = k.c
            c.save(); c.translate(x, feet); c.scale(1.0, sy); c.translate(-x, -feet)
            try:
                return orig(k, x, feet, *a, **kw)
            finally:
                c.restore()
        setattr(self.mod, self.name, w)
        return self

    def __exit__(self, *e):
        setattr(self.mod, self.name, self.orig)


def br(d, phase=0.0, amp=0.008):
    return 1.0 + amp * math.sin(2 * math.pi * (d / float(DPS) / A.BREATH + phase))


def phone_held(k, hx, hy, s, ang=-0.15, lit=True, buzz=False, d=0, seed=900):
    """A phone in a right hand, its back to us and its screen to its owner (the light on their face): the phone first,
    then the fist over its lower edge and the thumb round its side."""
    c = k.c
    sc = s / 0.55
    j = (0.9 if d % 2 else -0.9) if buzz else 0.0
    c.save(); c.translate(hx + j, hy - 8 * sc); c.rotate(ang); c.scale(sc, sc)
    if lit:                                                                       # the screen's light, up toward the face
        g = cairo.RadialGradient(0, -14, 0, 0, -14, 26)
        g.add_color_stop_rgba(0, *GLOW, 0.35); g.add_color_stop_rgba(1, *GLOW, 0.0)
        c.set_source(g); c.arc(0, -14, 26, 0, 6.3); c.fill()
    rect(k, -7, -12, 14, 24, PHONE, seed, lw=1.4)
    c.set_source_rgb(0.30, 0.32, 0.38); c.arc(-3.2, -8.2, 1.6, 0, 6.3); c.fill()   # its camera
    c.restore()
    if buzz:                                                                      # the buzz: two short zig-zags beside it
        c.set_source_rgb(*cp.RED); c.set_line_width(1.6); c.set_line_cap(1)
        for sx in (-1, 1):
            x0 = hx + sx * 12 * sc
            c.move_to(x0, hy - 18 * sc)
            for i in range(4):
                c.line_to(x0 + sx * (2.5 if i % 2 == 0 else 0) * sc, hy - (18 - 4 * (i + 1)) * sc)
            c.stroke()


def fist(k, hx, hy, s, skin, seed):
    sc = s / 0.55
    ellipse(k, hx, hy, 6 * sc, 6.5 * sc, skin, seed, shadow=False, lw=1.4)
    ellipse(k, hx - 6.5 * sc, hy - 7 * sc, 2.2 * sc, 3.4 * sc, skin, seed + 1, shadow=False, lw=1.0)  # the thumb round its side


# ---- 1.1 frame 0: every phone buzzes; heads down; then every head turns to Don ---------------------------------------------

N11 = 17
TURN = {"sofia": 6, "pam": 8, "mom": 9, "don_up": 11}       # the drawing each one turns (a ripple, not all at once)


def s1_1(k, d):
    """17 drawings (0-1.4 s). d 0-5: every phone buzzing in its owner's hand, every head down on it; the robot's visor
    lit. From d6 the heads come up and turn to Don, one after another; Don, last, looks up from his phone, grinning."""
    buzz = d <= 12
    lk = {n: ((-1, 0.05) if d >= t else (0.1, 1.0)) for n, t in TURN.items()}
    don_face = "grin" if d >= TURN["don_up"] else "neutral"
    don_look = (0.15, 0.1) if d >= TURN["don_up"] else (0.1, 1.0)
    sofia_face = "caught" if d >= TURN["sofia"] else "smile"
    got = {}

    def back(k_):
        from cs_cal import calendar2, CAL_AT
        calendar2(k_, *CAL_AT)                                                    # v7: its new place (cs_cal.CAL_AT)
        c_ = k_.c
        feet = sb.F + 6
        c_.save(); c_.translate(575, feet); c_.scale(1.0, br(d, 0.3)); c_.translate(-575, -feet)
        got["pam"] = pb.pam(k_, 575, feet, sb.SC["pam"], kit.ARM_POSES["phone_r"], "neutral", lk["pam"], glasses="up")
        c_.restore()
        (lx, ly), (rx, ry) = got["pam"]["hands"]
        phone_held(k_, rx, ry, sb.SC["pam"], ang=-0.2, buzz=buzz, d=d, seed=931)
        fist(k_, rx, ry, sb.SC["pam"], A.SKIN_PAM, 935)

    def ex(k_, o):
        for who, skin, sd, ang in (("don", kit.PEOPLE["DON"]["skin"], 941, -0.25), ("sofia", None, 951, -0.15)):
            (lx, ly), (rx, ry) = o[who]["hands"]
            hx, hy = (lx, ly) if who == "don" and lx > rx else (rx, ry)
            hx, hy = max((lx, ly), (rx, ry), key=lambda p: -p[1])                    # the raised hand: the higher one
            phone_held(k_, hx, hy, sb.SC[who], ang=ang, buzz=buzz, d=d + sd, seed=sd)
            fist(k_, hx, hy, sb.SC[who], skin or kit.PEOPLE.get("SOFIA", {}).get("skin", (0.98, 0.84, 0.74)), sd + 4)
        if "mom" in got:
            (lx, ly), (rx, ry) = got["mom"]["hands"]
            hx, hy = max((lx, ly), (rx, ry), key=lambda p: -p[1])
            phone_held(k_, hx, hy, sb.SC["mom"], ang=-0.1, buzz=buzz, d=d + 3, seed=961)
            fist(k_, hx, hy, sb.SC["mom"], kit.PEOPLE.get("MOM", {}).get("skin", (0.95, 0.80, 0.70)), 965)
        sx_, sy_ = o["robot"]["screen"]                                          # its visor lit by the buzz
        if buzz:
            c_ = k_.c
            c_.set_source_rgba(*GLOW, 0.35 if d % 2 else 0.2); c_.arc(sx_, sy_, 50 * sb.SC["robot"] * 0.9, 0, 6.3); c_.fill()

    om = sb.mfs.mom

    def mw(*a_, **kw):
        r = om(*a_, **kw); got["mom"] = r; return r
    sb.mfs.mom = mw
    try:
        with Breath(sb, "don", br(d)), Breath(sofia_fs, "sofia", br(d, 0.6)), Breath(sb.mfs, "mom", br(d, 0.15)):
            S(k, WIDE1, auto=False, back=back, extra=ex,
              **base(cl=False, door=0.0, rb=at("robot", arm="none"),
                     dn=at("don", pose=kit.ARM_POSES["phone_r"], face=don_face, look=don_look),
                     sf=at("sofia", pose="phone_r", face=sofia_face, look=lk["sofia"]),
                     pm=False, mm=dict(x=650, x4=True, pose="phone_r", face="sweet", look=lk["mom"])))
    finally:
        sb.mfs.mom = om


# ---- 1.2 the post -------------------------------------------------------------------------------------------------------

N12 = 58                                                   # v5: he reads it: his voice from 0.5 s (under 1.1) to 5.9 s
POST_AT = 0.5
PUSH12 = (40, 54)                                          # drawings: the push in on "My lawyer will call." as he says it


def s1_2(k, d):
    """29 drawings (1.4-3.8 s). The post; the reactions climb (0.3K to 2.4K, fast then slowing); the phone drifts in a
    hand at the breathing rhythm (lesson 72)."""
    c = k.c
    ph = 2 * math.pi * d / float(DPS) / A.BREATH
    c.set_source_rgb(0.24, 0.22, 0.20); c.paint()
    c.save(); c.translate(270, 480); c.rotate(math.radians(0.35 * math.sin(ph))); c.translate(-270, -480 + 2.0 * math.sin(ph))
    old = cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0]
    cp.REPLY_BIG[0] = cp.SAME_LAYOUT[0] = cp.GARAGE_LOGO[0] = True
    try:
        cp.phone2(k, "crisis")
    finally:
        cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0] = old
    react(k, 0.3 + 2.1 * (1 - (1 - d / float(N12 - 1)) ** 2))
    c.restore()
    z = 1.0 + 0.22 * ease((d - PUSH12[0]) / float(PUSH12[1] - PUSH12[0]))
    if z > 1.0:                                                                    # the red line fills the frame
        img = c.get_target()
        snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, img.get_width(), img.get_height())
        snap.set_device_scale(*img.get_device_scale())
        cs = cairo.Context(snap); cs.set_source_surface(img, 0, 0); cs.paint()
        c.save(); c.identity_matrix()
        cx, cy = 200, 515
        c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        c.set_source_surface(snap, 0, 0); c.paint(); c.restore()


def react(k, n):
    """Over the post's reaction count: the number now."""
    c = k.c
    c.set_source_rgb(*cp.LIGHT); c.rectangle(170, 646, 200, 46); c.fill()
    cp.T(c, "%.1fK" % n, 178, 678, 32, col=cp.GREY, bold=False, center=False)


# ---- 1.4 the reply, approved unread -------------------------------------------------------------------------------------

N14 = 47
LINE_R = (0.25, 2.618)                                     # the robot's line in the shot (s), from animatic v3
LINE_D = (2.818, 3.536)                                    # Don's "Approved."
REACH = (2.45, 2.95)                                       # his arm goes out to its pad (s): it lands on "Approved."
TYPE = "REPLY"


def s1_4(k, d):
    """47 drawings (3.8-7.7 s). Don smug, looking off; the robot speaks, its visor typing REPLY, blinking as it talks.
    His arm goes out without a look; his thumb lands on its pad on "Approved." (thumb 1); a green tick."""
    t = d / float(DPS)
    r = ease((t - REACH[0]) / (REACH[1] - REACH[0]))
    if t > LINE_D[1] + 0.15:
        r = 1 - ease((t - LINE_D[1] - 0.15) / 0.4)
    pose = don_reach(r, press=LINE_D[0] <= t <= LINE_D[0] + 0.25)
    talk = 0.0
    if LINE_D[0] <= t <= LINE_D[1]:
        talk = (1.0, 0.5, 1.0, 0.0)[int((t - LINE_D[0]) * DPS / 2) % 4]          # on twos
    tick = t >= LINE_D[0] + 0.15
    speaking = LINE_R[0] <= t <= LINE_R[1]

    def ex(k_, o):
        c_ = k_.c
        sx, sy = o["robot"]["screen"]
        rr = 50 * sb.SC["robot"]
        lit = 0.6 if (speaking and (d // 2) % 3 == 0) else 1.0                    # the visor blinks as it talks
        ellipse(k_, sx, sy, 0.80 * rr, 0.62 * rr, (0.06, 0.08, 0.12), 990, shadow=False, lw=1.6)
        if tick:
            c_.set_source_rgb(*cp.GRN); c_.set_line_width(0.12 * rr); c_.set_line_cap(1)
            c_.move_to(sx - 0.3 * rr, sy); c_.line_to(sx - 0.08 * rr, sy + 0.22 * rr); c_.line_to(sx + 0.34 * rr, sy - 0.25 * rr); c_.stroke()
        else:
            n = min(len(TYPE), max(0, int((t - LINE_R[0]) * 6)))                  # types out while it speaks
            col = tuple(v * lit for v in cp.CYAN)
            if n:
                cp.T(c_, TYPE[:n], sx - 0.48 * rr, sy + 0.12 * rr, 0.36 * rr, col=col, center=False)
        if r > 0.6:                                                                # his hand over the visor's edge, thumb 1 on it
            (lx, ly), _ = o["don"]["hands"]
            sk = kit.PEOPLE["DON"]["skin"]
            ellipse(k_, lx + 1.5, ly, 5.2, 5.6, sk, 947, shadow=False, lw=1.2)
            ellipse(k_, lx - 3.5, ly - 2.5, 2.0, 3.0, sk, 948, shadow=False, lw=0.9)

    with A.Don(A.UP, talk), Breath(sb, "don", br(d)), Breath(sb, "robot", br(d, 0.5, 0.006)):
        u = ease((t - PUSH[0]) / (PUSH[1] - PUSH[0]))
        cam = tuple(a_ + (b_ - a_) * u for a_, b_ in zip(TWO14, TWO14_IN))
        S(k, cam, auto=False, portrait="hang", extra=ex,
          **base(cl=False, sf=False, pm=False, mm=False, door=0.0, rb=at("robot", arm="none"),
                 dn=at("don", pose=pose, face="smug", look=(1, -0.3))))


DON_SH = (428.0, 679.6)                                    # his screen-left shoulder in 1.4 (measured: the hand at -90 deg)
DON_LN = 48 * 0.60                                         # kit.arm's segments at his canon scale
DON_REST = (420.0, 736.6)                                  # the hand hanging ("stand")
VISOR_HIT = (384.0, 709.0)                                 # the visor's near edge: where his thumb lands


def don_reach(r, press=False):
    """v2 (Tomas: "Don's arm moves wrong"): the arm by IK from his shoulder, elbow down, fixed segments; the hand
    travels on a small arc (up, then in) and lands on the visor's edge; a press pushes it in 2 units. (v1 blended two
    poses' angles: the arm swung up stiff like a lever and the hand landed beside the visor.)"""
    from cand_bc import ik
    e = r
    tx = DON_REST[0] + (VISOR_HIT[0] - DON_REST[0]) * e - (2.0 if press else 0.0)
    ty = DON_REST[1] + (VISOR_HIT[1] - DON_REST[1]) * e - 10.0 * math.sin(math.pi * e)
    a1, a2 = ik(DON_SH[0], DON_SH[1], tx, ty, DON_LN, DON_LN, 1)
    return (a1, a2, 8, 0)


# ---- 1.4b the reply posts ----------------------------------------------------------------------------------------------

N14b = 35                                                  # v5: the robot reads it as it lands (2.15 s)
REPLY_AT = 5 / 12.0


def _phone_surface(kind, d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * HI[0], 960 * HI[0])
    if HI[0] > 1:
        s.set_device_scale(HI[0], HI[0])
    k = Ctx(cairo.Context(s), 0)
    old = cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0]
    cp.REPLY_BIG[0] = cp.SAME_LAYOUT[0] = cp.GARAGE_LOGO[0] = True
    try:
        cp.phone2(k, kind)
        if kind == "crisis":
            react(k, 2.4)
    finally:
        cp.REPLY_BIG[0], cp.SAME_LAYOUT[0], cp.GARAGE_LOGO[0] = old
    return s


def s1_4b(k, d):
    """16 drawings (7.7-9.0 s). The post (2.4K), then the company's reply slides up into place under it and settles;
    held, the phone drifting."""
    c = k.c
    ph = 2 * math.pi * (d + N12) / float(DPS) / A.BREATH
    c.set_source_rgb(0.24, 0.22, 0.20); c.paint()
    c.save(); c.translate(270, 480); c.rotate(math.radians(0.35 * math.sin(ph))); c.translate(-270, -480 + 2.0 * math.sin(ph))
    c.set_source_surface(_phone_surface("crisis", d), 0, 0); c.paint()
    e = ease((d - 2) / 5.0)
    if e > 0:
        ry = 650
        c.save(); c.rectangle(60, ry - 4, 420, 886 - ry); c.clip()
        c.set_source_rgb(*cp.LIGHT); c.rectangle(60, ry - 4, 420, 886 - ry); c.fill()
        c.set_source_surface(_phone_surface("reply", d), 0, (1 - e) * 120); c.paint_with_alpha(e)
        c.restore()
    c.restore()


SHOTS = [("1.1", N11, s1_1), ("1.2", N12, s1_2), ("1.4", N14, s1_4), ("1.4b", N14b, s1_4b)]


def draw(fn, d):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540 * HI[0], 960 * HI[0])
    if HI[0] > 1:
        s.set_device_scale(HI[0], HI[0])
    c = cairo.Context(s); k = Ctx(c, 0)
    sb.bg(c); sb.HEADS.clear(); sb.AVOID.clear()
    old = cp.PROPS4[0], cp.REAL_PAM[0], cp.REPLY_TXT[0]
    cp.PROPS4[0] = cp.REAL_PAM[0] = True; cp.REPLY_TXT[0] = cp.REPLY_V15                 # v4: "Shut off!" (script v15)
    try:
        with A.b3._ep11v3():
            fn(k, d)
    finally:
        cp.PROPS4[0], cp.REAL_PAM[0], cp.REPLY_TXT[0] = old
    return s


def schedule():
    """v5: the lines on this scene's own clock (drawings), not animatic v3's."""
    t12 = N11 / float(DPS); t14 = (N11 + N12) / float(DPS); t14b = (N11 + N12 + N14) / float(DPS)
    return [("1.2", POST_AT), ("1.4r", t14 + LINE_R[0]), ("1.4d", t14 + LINE_D[0]), ("1.4b", t14b + REPLY_AT)]


def sound(total, out):
    """The lines on the scene's clock, the buzz under 1.1; to about -15 LUFS like the animatic."""
    import cs_animatic as an
    meta = json.load(open(TAKES + "/takes.json"))
    a = np.zeros(int((total + 0.3) * SR))
    for key, t0 in schedule():
        x, _ = sf.read("%s/%s.wav" % (TAKES, key))
        p = int(t0 * SR); a[p:p + len(x)] += x[:len(a) - p]
    z = an.buzz(1.15) * 0.7; p = int(0.05 * SR); a[p:p + len(z)] += z
    sf.write(out, (a / max(1e-9, np.abs(a).max()) * 0.7).astype(np.float32), SR)
    json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in schedule()]},
              open("cs_scene1_timing_%s.json" % V, "w"), indent=1)


def main(out_dir):
    tmp = "/tmp/cs_s1"; os.makedirs(tmp, exist_ok=True)
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
    sound(total, tmp + "/a.wav")
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "cs_scene1_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    A.strip(tiles[::2], os.path.join(out_dir, "cs_scene1_%s_strip.png" % V), 160, 9)
    print("wrote", out, "%d drawings, %.2f s" % (n, total))


if __name__ == "__main__":
    if "lo" in sys.argv[1:]:
        HI[0] = 1
    args = [a for a in sys.argv[1:] if a != "lo"]
    main(args[0] if args else "../customer-success")
