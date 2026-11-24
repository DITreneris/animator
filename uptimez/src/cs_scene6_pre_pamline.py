"""ONE STAR (episode 11): the animation pass, scene 6 "The UPDATE" (script v16, beat 06), after layout v2.
Native 1080, 12 drawings a second, out at 30 fps.

  6.1  at the door: the plan rolled under his arm, his phone in both hands, eyes down, grudging
  6.2  his UPDATE (motion test v10's insert, cold-tested): the strike, UPDATE:, "Pam found it."; the reply above it
       is now "Shut off! Our AI does not lose files!"
  6.3  Pam at the counter, close: her phone lights up ON THE COUNTER (Tomas); she flips it face down; checks
       nobody saw; lifts one corner, peeks; almost smiles
  6.3b under his UPDATE, her line arrives: PAM: "Some post. Others find."
  6.5  Sofía holds her phone up to us, a real phone, the one star big: "Still one star." Dry, no anger
  6.6  the wide = frame 0: every phone buzzing; Don reads his, puffs up (praise!). Hard cut to 1.1
  python3 cs_scene6.py [out_dir] [lo]  ->  cs_scene6_v1.mp4, _strip.png, cs_scene6_timing_v1.json"""
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
import cs_scene3 as s3
import cs_scene4 as s4
from cs_board import S, at, base
from kit import Ctx, INK, ellipse, rect, cut

V = "v4"                                                   # v4: the reply under his UPDATE is "Stupid human." (script v18)
DPS = 12
SR = 48000
TAKES = s1.TAKES
HI = s1.HI
ease, br, Breath = s1.ease, s1.br, s1.Breath
lerp = s4.lerp
SKIN_CL = sb.SKIN_CL
kit.ARM_POSES.setdefault("phone_l", (12, 112, 8, 0))

# ---- 6.1 at the door ---------------------------------------------------------------------------------------------------

N61 = 12
CAM61 = (236, 660, 2.9)


def s6_1(k, d):
    """12 drawings. The door behind him. The plan, rolled, under his arm; his phone in both hands (fists on its
    sides, thumbs on its face); eyes down on it, heavy-lidded: grudging (cold test v9; Tomas kept it)."""
    up = 4 <= d <= 8
    look, face = ((0.45, 1.0) if up else (0.0, 1.0)), ("tired" if d >= 4 else "plain")
    lift = (0, 0, 0, 0, -3, -5, -5, -5, -4, -2, 0, 0)[d]
    x = 232

    def pre(k_):                                                                   # the roll under his arm: behind him,
        c = k_.c                                                                   # its ends out in front and behind
        c.save(); c.translate(x - 44, 688); c.rotate(-0.42)
        rect(k_, -46, -7, 92, 14, s4.BLUE, 995, lw=1.6)
        ellipse(k_, -46, 0, 3, 7, (0.30, 0.52, 0.92), 996, shadow=False, lw=1.2)
        c.set_source_rgba(0.98, 0.96, 0.86, 0.9); c.rectangle(-30, -7.5, 7, 15); c.fill()
        c.restore()

    def ex(k_, o):
        (lx, ly), (rx, ry) = sorted(o["client"]["hands"])
        mx, my = (lx + rx) / 2, (ly + ry) / 2 + lift
        c = k_.c
        c.save(); c.translate(mx, my - 14); c.rotate(-0.04)
        rect(k_, -13, -22, 26, 40, s1.PHONE, 997, lw=1.6)
        c.set_source_rgb(*cp.LIGHT); c.rectangle(-10.5, -19, 21, 33); c.fill()
        c.restore()
        for i, (hx, sgn) in enumerate(((lx, 1), (rx, -1))):
            ellipse(k_, hx, my, 9, 10, SKIN_CL, 980 + i, lw=1.6)
            ellipse(k_, hx + sgn * 6, my - 12, 3.6, 5.5, SKIN_CL, 984 + i, lw=1.3)

    with s4.Strip(None), Breath(sb, "client", br(d, 0.4)):
        S(k, CAM61, auto=False, portrait=False, pre=pre, extra=ex,
          **base(rb=False, sf=False, dn=False, pm=False, mm=False,
                 cl=at("client", x=x, pose=(22, 62, -22, -62), face=face, look=look)))


# ---- 6.2 the UPDATE (the motion test's insert) ------------------------------------------------------------------------------

N62 = 25                                                   # cold test: the hold after the text was long (1.5 -> 1.0 s)


def s6_2(k, d):
    old = A.SWAY8[0]; A.SWAY8[0] = True
    try:
        A.m6_1b7(k, d)
    finally:
        A.SWAY8[0] = old


# ---- 6.3 Pam's phone on the counter --------------------------------------------------------------------------------------

N63 = 30
CAM63 = (300, 698, 4.0)
PX63 = 300
PH = (350, 603)                                             # her phone on the counter top (frame)
FLIP63 = (5, 8)                                             # drawings: she turns it face down
PEEK63 = (16, 20)                                           # she lifts a corner


def _fr2sc(p):
    return (CAM63[0] + (p[0] - 270) / CAM63[2], CAM63[1] + (p[1] - 480) / CAM63[2])


def _arm_over(k, px, a1, a2):
    """Her screen-right arm again, over what was drawn after her (4.2b's way): from her shoulder, sleeve shoved up."""
    c = k.c
    cx, cy, z = CAM63
    c.save(); c.translate(270, 480); c.scale(z, z); c.translate(-cx, -cy)
    c.translate(px, s4.PAM_FEET); c.scale(s4.PAM_S, s4.PAM_S)
    dd = lambda a: (math.sin(math.radians(a)), math.cos(math.radians(a)))
    sx_, sy_ = s4.PAM_SH_R
    ex_, ey_ = sx_ + dd(a1)[0] * s4.LN, sy_ + dd(a1)[1] * s4.LN
    wx, wy = ex_ + dd(a1 + a2)[0] * s4.LN, ey_ + dd(a1 + a2)[1] * s4.LN
    for (ax, ay, bx, by), col in (((sx_, sy_, ex_, ey_), s4.PURPLE), ((ex_, ey_, wx, wy), s4.SKIN_PAM)):
        an = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(an) * 8.5, math.cos(an) * 8.5
        cut(k, [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], col, shadow=False, lw=2)
    ellipse(k, ex_, ey_, 9, 9, s4.PURPLE, 997, shadow=False, lw=2)
    ellipse(k, wx, wy, 10.5, 9.5, s4.SKIN_PAM, 999, shadow=False, lw=2)
    c.restore()


def s6_3(k, d):
    """30 drawings (2.5 s). Pam at the counter, close. Her phone, on the counter, lights up: her name. Her hand comes
    down and turns it face down (d5-8). Her eyes go left, right: nobody saw. She lifts one corner (d16-20), the light
    leaks out; she peeks; almost smiles."""
    c = k.c
    f = ease((d - FLIP63[0]) / float(FLIP63[1] - FLIP63[0]))                       # 0 lit, face up; 1 face down
    pk = ease((d - PEEK63[0]) / float(PEEK63[1] - PEEK63[0]))
    rest = (PX63 + 22, s4.PAM_FEET - 64)
    tgt = _fr2sc((PH[0] + 26, PH[1] - 6))
    if d < 3:
        hand = rest
    elif d < 12:
        hand = lerp(rest, tgt, ease((d - 3) / 3.0) * (1 - ease((d - 9) / 3.0)))
    else:
        hand = lerp(rest, _fr2sc((PH[0] + 44, PH[1] - 2)), ease((d - 13) / 3.0))
    a1, a2 = s4.pam_reach(PX63, 0.0, hand)
    if d < 3:
        look = (0, 0.2)
    elif d < 9:
        look = (0.4, 1.0)
    elif d < 12:
        look = (-1, 0.0)
    elif d < 15:
        look = (1, 0.0)
    else:
        look = (0.4, 1.0)
    face = "pleased" if d >= 24 else "neutral"

    def pre(k_):
        s4.pam(k_, PX63, (-8, 0, a1, a2), face, look, glasses="up", d=d)

    S(k, CAM63, auto=False, portrait=False, pre=pre,
      **base(door=0.0, cl=False, sf=False, rb=False, dn=False, pm=False, mm=False))
    # the counter in front of her: its top, seen a little from above, and its face
    cut(k, [(-10, 562), (550, 562), (550, 644), (-10, 644)], (0.80, 0.70, 0.55), shadow=False, lw=3)
    cut(k, [(-10, 644), (550, 644), (550, 970), (-10, 970)], (0.70, 0.60, 0.46), shadow=False, lw=3)
    # the phone on it
    lit = 1 - f
    if lit > 0.05 or pk > 0:
        g = cairo.RadialGradient(PH[0], PH[1], 0, PH[0], PH[1], 120)
        g.add_color_stop_rgba(0, 0.6, 0.9, 1.0, 0.45 * max(lit, pk * 0.6)); g.add_color_stop_rgba(1, 0.6, 0.9, 1.0, 0)
        c.set_source(g); c.arc(PH[0], PH[1], 120, 0, 6.3); c.fill()
    buzz = (2.0 if d % 2 else -2.0) if d < 4 else 0.0
    c.save(); c.translate(PH[0] + buzz, PH[1] - pk * 6); c.rotate(-0.10 - pk * 0.10)
    w = 150 * max(0.12, abs(math.cos(math.pi * f)))                                # it turns over. Cold test: read as a
    cut(k, [(-w / 2 + 12, -34), (w / 2 + 12, -34), (w / 2 - 12, 34), (-w / 2 - 12, 34)], s1.PHONE, lw=3)   # nameplate:
    if f < 0.5:                                                                    # bigger, a bezel, a notification, buzz marks
        c.set_source_rgb(*cp.LIGHT); c.move_to(-w / 2 + 22, -27); c.line_to(w / 2 + 2, -27); c.line_to(w / 2 - 22, 27)
        c.line_to(-w / 2 - 2, 27); c.close_path(); c.fill()
        if f < 0.2:
            c.set_source_rgb(*cp.GRN); c.rectangle(-52, -20, 60, 9); c.fill()
            cp.T(c, "Pam found it.", 0, 14, 19, col=(0.55, 0.16, 0.46))
        c.set_source_rgb(0.30, 0.32, 0.38); c.new_path(); c.arc(w / 2 - 6, 0, 3, 0, 6.3); c.fill()   # its button
    else:
        c.set_source_rgb(0.30, 0.32, 0.38); c.new_path(); c.arc(-w / 2 + 22, -14, 6, 0, 6.3); c.fill()   # its back: the camera
        c.set_source_rgb(0.20, 0.22, 0.27); c.new_path(); c.arc(-w / 2 + 22, -14, 3, 0, 6.3); c.fill()
    c.restore()
    if d < 4 or 9 <= d < 12:                                                       # it buzzes; and again, face down
        c.set_source_rgb(*cp.RED); c.set_line_width(3); c.set_line_cap(1)
        for sx in (-1, 1):
            x0 = PH[0] + sx * 98
            c.move_to(x0, PH[1] - 22)
            for i in range(4):
                c.line_to(x0 + sx * (7 if i % 2 == 0 else 0), PH[1] - 22 + 11 * (i + 1))
            c.stroke()
    if d >= 3:
        _arm_over(k, PX63, a1, a2)


# ---- 6.3b her line ---------------------------------------------------------------------------------------------------------

N63b = 20


def s6_3b(k, d):
    """20 drawings (1.7 s). The UPDATE's screen; her reply arrives under it: PAM: "Some post. Others find." """
    c = k.c
    ph = 2 * math.pi * d / float(DPS) / A.BREATH
    c.set_source_rgb(0.24, 0.22, 0.20); c.paint()
    c.save(); c.translate(270, 480); c.rotate(math.radians(0.35 * math.sin(ph))); c.translate(-270, -480 + 2.0 * math.sin(ph))
    c.set_source_surface(s1._phone_surface("update", d), 0, 0); c.paint()
    e = ease((d - 3) / 2.0)
    if e > 0:
        c.set_source_surface(s1._phone_surface("pam", d), 0, 0); c.paint_with_alpha(e)     # a fade: a slide ghosted the text
    c.restore()


# ---- 6.5 "Still one star." ---------------------------------------------------------------------------------------------------

N65 = 20
CAM65 = (330, 690, 3.2)
SX65 = 352
LINE65 = (0.3, 0.3 + 0.875)


def star(c, x, y, r, fill):
    c.new_path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (c.move_to if i == 0 else c.line_to)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path()
    if fill:
        c.set_source_rgb(0.98, 0.78, 0.10); c.fill_preserve()
    c.set_source_rgb(*(INK if fill else (0.72, 0.74, 0.78))); c.set_line_width(2.4); c.stroke()


def s6_5(k, d):
    """20 drawings (1.7 s). Sofía, close, dry. Her phone comes up, turned to us: a real phone in her hand, one
    star of five, big, under "Pam found it." "Still one star." No smile."""
    t = d / float(DPS)
    up = ease(d / 3.0)
    talk = LINE65[0] <= t <= LINE65[1]
    mouth = ("A", "E", "M", "O", "E", "M")[int((t - LINE65[0]) * DPS / 2) % 6] if talk else None
    got = {}
    of = s1.sofia_fs.sofia

    def sof(*a, **kw):
        try:
            return of(*a, mouth=mouth, **kw)
        except TypeError:
            return of(*a, **kw)
    s1.sofia_fs.sofia = sof
    try:
        with Breath(s1.sofia_fs, "sofia", br(d, 0.6)):
            S(k, CAM65, auto=False, portrait=False, extra=lambda k_, o: got.update(o=o),
              **base(door=0.0, cl=False, rb=False, dn=False, pm=False, mm=False,
                     sf=at("sofia", x=SX65, pose="phone_l", face="unimpressed", look=(-0.3, 0.1))))
    finally:
        s1.sofia_fs.sofia = of
    c = k.c
    px, py = 196, 556 + (1 - up) * 420                                             # her phone, thrust at us: beside her face,
                                                                                   # never over her mouth, above the apps' zone
    c.save(); c.translate(px, py); c.rotate(-0.06)
    c.scale(0.80, 0.80)                                                            # cold test: read as a tablet
    rect(k, -92, -160, 184, 330, s1.PHONE, 971, lw=3.5)
    c.set_source_rgb(*cp.LIGHT); c.rectangle(-80, -142, 160, 290); c.fill()
    c.set_source_rgb(0.30, 0.32, 0.38); c.rectangle(-22, -154, 44, 6); c.fill()    # its speaker slot
    cp.T(c, "UPDATE:", 0, -96, 24, col=cp.GRN)
    cp.T(c, "Pam found it.", 0, -62, 23, col=(0.55, 0.16, 0.46))
    star(c, 0, 0, 44, True)
    for i in range(4):
        star(c, -57 + i * 38, 70, 13, False)
    cp.T(c, "1/5", 0, 128, 40)
    c.restore()
    sk = (0.98, 0.84, 0.74)
    # (her arm is behind the phone: it sits against her shoulder)
    for i in range(4):                                                             # her fingers over its near edge, red nails
        ellipse(k, px + 70, py + 36 + i * 24, 14, 10, sk, 974 + i, shadow=False, lw=2.2)
        ellipse(k, px + 63, py + 36 + i * 24, 6, 5, (0.80, 0.12, 0.20), 978 + i, shadow=False, lw=1.2)


# ---- 6.6 the wide = frame 0 -------------------------------------------------------------------------------------------------

N66a = 14
CAM66a = (452, 687, 3.05)


def s6_6a(k, d):
    """14 drawings (1.2 s). Cold test: in the wide nobody saw Don react (it read as a plain repeat of the opening).
    So first Don alone, big: his phone buzzing in his hand; he reads it, grins, swells, a thumb in his vest, eyes
    shut: praise."""
    p = ease((d - 5) / 3.0)
    pose = tuple(a + (b - a) * p for a, b in zip(kit.ARM_POSES["phone_r"], (25, 100, -12, -112)))
    face = "neutral" if d < 4 else ("grin" if d < 9 else "happy")

    def ex(k_, o):
        hx, hy = min(o["don"]["hands"], key=lambda q: q[1])
        s1.phone_held(k_, hx, hy, sb.SC["don"], ang=-0.25, buzz=d < 5, d=d, seed=941)
        s1.fist(k_, hx, hy, sb.SC["don"], kit.PEOPLE["DON"]["skin"], 945)

    with A.Don(A.MOUTH), Breath(sb, "don", br(d) + 0.05 * p):
        S(k, CAM66a, auto=False, mic="down", portrait=False, extra=ex,
          **base(cl=False, sf=False, rb=False, pm=False, mm=False, door=0.0,
                 dn=at("don", pose=pose, face=face, look=(0.1, 1.0))))


N66 = 10


def s6_6(k, d):
    """16 drawings (1.3 s). Scene 1's wide, by the same code (the loop's seam): every phone buzzing in its hand,
    every head down. Don reads his, grins, puffs up, a thumb in his vest: praise. Hard cut to 1.1."""
    old = s1.END66[0]; s1.END66[0] = True
    try:
        s1.s1_1(k, d + 6)                                                          # Don already puffed up (6.6a)
    finally:
        s1.END66[0] = old


SHOTS = [("6.1", N61, s6_1), ("6.2", N62, s6_2), ("6.3", N63, s6_3), ("6.3b", N63b, s6_3b), ("6.5", N65, s6_5),
         ("6.6a", N66a, s6_6a), ("6.6", N66, s6_6)]


def schedule():
    st, n = {}, 0
    for sh, nd, _ in SHOTS:
        st[sh] = n / float(DPS); n += nd
    return [("6.5", st["6.5"] + LINE65[0])]


def draw(fn, d):
    return s1.draw(fn, d)


def main(out_dir):
    import cs_animatic as an
    tmp = "/tmp/cs_s6"; os.makedirs(tmp, exist_ok=True)
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
    st = dict((sh, i) for sh, i in zip([s[0] for s in SHOTS], np.cumsum([0] + [s[1] for s in SHOTS])))
    for sh, ln in (("6.3", 0.35), ("6.6a", 1.6)):                                   # the buzz: her phone; then everyone's
        z = an.buzz(ln) * 0.35; p_ = int(st[sh] / float(DPS) * SR); a[p_:p_ + len(z)] += z[:len(a) - p_]
    sf.write(tmp + "/a.wav", (a / max(1e-9, np.abs(a).max()) * 0.7).astype(np.float32), SR)
    r_ = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"],
                        capture_output=True, text=True)
    cur = float([x for x in r_.stderr.split("\n") if "I:" in x][-1].split("I:")[1].split("LUFS")[0])
    out = os.path.join(out_dir, "cs_scene6_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in schedule()]},
              open("cs_scene6_timing_%s.json" % V, "w"), indent=1)
    A.strip(tiles[::2], os.path.join(out_dir, "cs_scene6_%s_strip.png" % V), 160, 10)
    print("wrote", out, "%d drawings, %.2f s" % (n, total))


if __name__ == "__main__":
    if "lo" in sys.argv[1:]:
        HI[0] = 1
    args = [a for a in sys.argv[1:] if a != "lo"]
    main(args[0] if args else "../customer-success")
