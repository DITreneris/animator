"""ONE STAR (episode 11): the animation pass, scene 5 "The number" (script v16, beat 05), after layout v2 and Tomas's
answers (20 Nov, /grill-me). Native 1080, 12 drawings a second, out at 30 fps.

  5.1  two beats in one shot, a pan: Sofía steps into his path, smiling; he turns his back on her and the camera
       goes with him to Pam: "Your number."; Sofía's smile left behind at the frame's edge              (Tomas)
  5.2a Pam alone, very big: she freezes; her eyes go off to Don and back                               (Tomas)
  5.2  top shot: her pen writes PAM / 555 0142 on the tape across bay 7; his phone slides in beside it  (Tomas)
  5.3  his phone: his thumb types the note, "finds things"; then SAVE -> SAVED                         (Tomas)
  5.4b Pam straightens Don's mic (motion test v10, cold-tested)
  5.4c "Customer success." (motion test v10)
  python3 cs_scene5.py [out_dir] [lo]  ->  cs_scene5_v1.mp4, _strip.png, cs_scene5_timing_v1.json"""
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
import acts_ob as ac
import cs_props as cp
import cs_anim as A
import cs_scene1 as s1
import cs_scene3 as s3
import cs_scene4 as s4
from cand_bc import ik
from cs_board import S, at, base
from kit import Ctx, INK, ellipse, rect

V = "v4"
DPS = 12
SR = 48000
TAKES = s1.TAKES
HI = s1.HI
ease, br, Breath = s1.ease, s1.br, s1.Breath
lerp = s4.lerp
SKIN_CL = sb.SKIN_CL
PEN = (0.10, 0.15, 0.55)

# ---- 5.1 "Your number." --------------------------------------------------------------------------------------------------

N51 = 27
PAM_X, CL_X = 195, 300
CAM51 = ((342, 662, 2.45), (258, 665, 2.45))                # on Sofía and him; then on him and Pam
PAN51 = (6, 13)
LINE51 = (1.0, 1.0 + 0.813)
CL_SH_L = (-46.8, 651.72)                                   # his screen-left shoulder (x from his x)


def s5_1(k, d):
    """27 drawings (2.25 s). Sofía steps into his path, smoothing her lapel, smiling. He looks at her, flat; turns
    his back on her; the camera goes with him to Pam; his phone comes up in his hand: "Your number." Sofía's smile,
    left at the frame's edge, drops."""
    t = d / float(DPS)
    sx = 418 - (418 - 376) * ease(d / 4.0)
    turned = d >= 5
    up = ease((d - 6) / 4.0)                                                       # the phone comes up
    hand = lerp((CL_X - 46.8, 715.7), (CL_X - 60, 688), up)
    a1, a2 = ik(CL_X + CL_SH_L[0], CL_SH_L[1], hand[0], hand[1], s4.CL_LN, s4.CL_LN, 1)
    u = ease((d - PAN51[0]) / float(PAN51[1] - PAN51[0]))
    cam = lerp(CAM51[0], CAM51[1], u)
    code = s3.talk_code(t, *LINE51)

    def pre(k_):
        s4.pam(k_, PAM_X, "stand", "neutral", (1, -0.4), glasses="up", d=d)

    def ex(k_, o):
        if up > 0.3:
            hx, hy = min(o["client"]["hands"])
            s1.phone_held(k_, hx, hy, sb.SC["client"], ang=0.15, seed=961)
            s1.fist(k_, hx, hy, sb.SC["client"], SKIN_CL, 965)

    with s4.Strip(None), s3.Client(mouth=code, edge=False), Breath(sb, "client", br(d, 0.4)), \
            Breath(s1.sofia_fs, "sofia", br(d, 0.6)):
        S(k, cam, auto=False, portrait=False, pre=pre, extra=ex,
          **base(door=0.0, rb=False, dn=False, pm=False, mm=False,
                 sf=at("sofia", x=sx, pose="lapel" if d < 8 else "hold", face="knowing" if d < 8 else "caught",
                       look=(-1, -0.2)),
                 cl=at("client", x=CL_X, pose=(a1, a2, 8, 0), face="plain", look=(-1, 0.3) if turned else (1, 0.3))))


# ---- 5.2a Pam, very big ---------------------------------------------------------------------------------------------------

N52a = 11
CAM52a = (197, 671, 5.0)
EYE_X, EYE_Y = (215, 307), 431                              # her lenses in this framing (frame)
EYES = [(1, -0.6)] * 3 + [(-1, 0.2)] * 4 + [(1, -0.6)] * 4   # up at the Client beside her / away, across the room to Don / back


def s5_2a(k, d):
    """11 drawings (0.9 s). Only Pam. She freezes (no breath for three drawings); her eyes slide off to Don and come
    back; a small swallow (her head dips a hair)."""
    dip = 2.0 * math.sin(math.pi * max(0, d - 7) / 3.0) if d >= 7 else 0.0

    def pre(k_):
        c = k_.c
        c.save(); c.translate(0, dip / 4.0)
        s4.pam(k_, PAM_X, "stand", "neutral", EYES[d], glasses="up", d=0 if d < 3 else d)
        c.restore()

    S(k, CAM52a, auto=False, portrait=False, pre=pre,
      **base(door=0.0, cl=False, sf=False, rb=False, dn=False, pm=False, mm=False))
    # her eyes, drawn again in the lenses: the kit's grey pupils behind glass do not read as a look (checked at 1080)
    c = k.c
    lx, ly = EYES[d]
    wide = 1.25 if d < 3 else 1.0                                                  # the freeze: wide
    for ex_ in EYE_X:
        ellipse(k, ex_, EYE_Y + dip, 26, 16 * wide, (1, 1, 1), 985, shadow=False, lw=2.6)
        c.set_source_rgb(0.12, 0.10, 0.10); c.new_path()
        c.arc(ex_ + lx * 12.5, EYE_Y + dip + ly * 6, 10.5, 0, 6.3); c.fill()
        c.set_source_rgb(1, 1, 1); c.new_path(); c.arc(ex_ + lx * 12.5 + 4, EYE_Y + dip + ly * 6 - 4, 3, 0, 6.3); c.fill()


# ---- 5.2 her number ------------------------------------------------------------------------------------------------------

N52 = 30
TAPE = (270, 371)                                           # the tape across 7 in the close-up (frame)
WRITE = (("PAM", 3, 7), ("555 0142", 8, 17))                # the line, the drawings it is written over


SLEEVE52 = [0.40, 190]                                      # (sleeve share, the arm's entry x past the pen); v19: whose hand


def s5_2(k, d):
    """30 drawings (2.5 s). Close on bay 7, the tape across it. Her pen writes PAM, then 555 0142 (her hand, the
    sleeve shoved up, moving with it). She lifts off; his phone slides in from below, beside her number."""
    c = k.c
    sb.bg(c, (0.30, 0.26, 0.22))
    c.set_source_surface(s4._plan_surface("number"), 0, 0); c.paint()
    n_, bx, by, bw, bh = [b for b in ac._bays() if b[0] == 7][0]
    W = (bw + 8) * 11.0
    c.save(); c.translate(*TAPE); c.rotate(-0.06)
    c.set_source_rgb(0.98, 0.96, 0.86); c.rectangle(-W / 2 + 4, -60, W - 8, 120); c.fill()     # the tape, blank
    c.select_font_face("Comic Neue", 0, 1); c.set_font_size(46.2); c.set_source_rgb(*PEN)
    tip = None
    for j, (txt, d0, d1) in enumerate(WRITE):
        e = c.text_extents(txt)
        x0, y0 = -e.x_advance / 2, -6.6 + j * 48.4
        f = min(1.0, max(0.0, (d - d0) / float(d1 - d0)))
        n = int(round(f * len(txt)))
        if n:
            c.move_to(x0, y0); c.show_text(txt[:n])
        if d0 <= d <= d1:
            tip = (x0 + c.text_extents(txt[:n]).x_advance + 4, y0 - 6 + (4 if d % 2 else 0))
    if tip is None and d < WRITE[0][1]:
        tip = (-W / 2 + 40, -80 - (WRITE[0][1] - d) * 60)                          # the pen coming down
    tx_ = c.user_to_device(*tip) if tip else None
    c.restore()
    if tip:
        sc = HI[0]
        px, py = tx_[0] / sc, tx_[1] / sc
        s4.limb(k, px + SLEEVE52[1], -80, px + 78, py - 96, 84, SLEEVE52[0], s4.PURPLE, s4.SKIN_PAM, seed=911, thumb=1)
        c.set_source_rgb(*INK); c.set_line_width(15); c.set_line_cap(1)            # the pen in her fingers
        c.move_to(px, py); c.line_to(px + 96, py - 122); c.stroke()
        c.set_source_rgb(*PEN); c.set_line_width(10); c.move_to(px + 8, py - 10); c.line_to(px + 96, py - 122); c.stroke()
    if d >= 20:                                                                    # his phone slides in, beside it
        u = ease((d - 20) / 6.0)
        x, y = 372, 640 + (1 - u) * 420
        s4.limb(k, 560, 1060 + (1 - u) * 300, x + 60, y + 150, 64, 0.55, s4.OLIVE, SKIN_CL, cuff=s4.CUFF, seed=931, oil=True)
        c.save(); c.translate(x, y); c.rotate(0.10)
        rect(k, -70, -120, 140, 250, s1.PHONE, 971, lw=3)
        c.set_source_rgb(*cp.LIGHT); c.rectangle(-60, -106, 120, 222); c.fill()
        cp.T(c, "NEW", 0, -60, 26, col=cp.GREY); cp.T(c, "CONTACT", 0, -30, 26, col=cp.GREY)
        c.set_source_rgb(0.80, 0.82, 0.86)
        for i in range(2):
            c.rectangle(-44, 4 + i * 36, 88, 22); c.fill()
        c.restore()
        ellipse(k, x + 66, y + 110, 20, 26, SKIN_CL, 973, shadow=False, lw=2.4)      # his oily thumb on its edge


# ---- 5.3 the contact, saved -------------------------------------------------------------------------------------------------

N53 = 22
NOTE = "finds things"
NOTE_COL = (0.55, 0.16, 0.46)                               # cold test: small and grey, and it is the punchline
TYPE53 = (3, 11)                                           # drawings the note is typed over
TAP53 = 15


def s5_3(k, d):
    """22 drawings (1.8 s). His phone: Pam, 555 0142, an empty note. His olive sleeve and oily thumb come in and type
    it: "finds things". Then the thumb goes up to SAVE: SAVED."""
    c = k.c
    cp.phone(k, "contact3")
    x0, y0, w = 58, 70, 424
    c.set_source_rgb(*cp.LIGHT); c.rectangle(x0 + 8, y0 + 468, w - 16, 46); c.fill()
    n = int(round(len(NOTE) * min(1.0, max(0.0, (d - TYPE53[0]) / float(TYPE53[1] - TYPE53[0])))))
    scratch = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 8, 8))
    full = cp.T(scratch, "note: " + NOTE, 0, 0, 38, col=NOTE_COL, center=False)
    lx = 270 - (full if isinstance(full, (int, float)) else 250) / 2.0
    cur = "|" if (d < TAP53 and d % 2 == 0) else ""
    cp.T(c, "note: " + NOTE[:n] + cur, lx, y0 + 503, 38, col=NOTE_COL, center=False)
    if d < TAP53:
        rect(k, 118, 650, 304, 90, (0.72, 0.74, 0.78) if d < TAP53 - 1 else (0.55, 0.80, 0.60), 990, shadow=False, lw=2)
        cp.T(c, "SAVE", 270, 710, 42, col=(1, 1, 1))
    if d <= 2:
        p = lerp((560, 900), (330, 842), ease(d / 2.0))
    elif d <= TYPE53[1]:
        p = ((300, 330, 280, 320)[d % 4], 842 - (8 if d % 2 else 0))               # typing
    elif d <= TAP53:
        p = lerp((310, 842), (300, 692), ease((d - TYPE53[1]) / float(TAP53 - 1 - TYPE53[1])))
    else:
        p = lerp((300, 692), (560, 900), ease((d - TAP53) / 4.0))
    if d <= TAP53 + 4:
        sb.thumb(k, p[0], p[1], 1.15, SKIN_CL, oil=True, ang=2.3, who="client")


# ---- 5.4b, 5.4c: from the motion test (v10 flags) ---------------------------------------------------------------------------

CAM54c = (474, 692, 2.6)                                    # the two at the series' face scale (the test's framing kept the
                                                           # plaque whole and left them small and low: Tomas, on scale)


def _test(fn, cam=None):
    def w(k, d):
        old = A.V7[0], A.V9[0], A.CUT_HANDSHAKE[0], A.MIC_CAM7
        A.V7[0] = A.V9[0] = A.CUT_HANDSHAKE[0] = True
        if cam:
            A.MIC_CAM7 = cam
        try:
            fn(k, d)
        finally:
            A.V7[0], A.V9[0], A.CUT_HANDSHAKE[0], A.MIC_CAM7 = old
    return w


N54b, N54c = 25, 16
LINE54 = 0.25
# 5.4b (Pam straightens Don's mic) is CUT: three cold rounds read the gesture but not its aim (lesson 52; Tomas, 21 Nov)
SHOTS = [("5.1", N51, s5_1), ("5.2a", N52a, s5_2a), ("5.2", N52, s5_2), ("5.3", N53, s5_3),
         ("5.4c", N54c, _test(A.m5_4c, CAM54c))]


def schedule():
    st, n = {}, 0
    for sh, nd, _ in SHOTS:
        st[sh] = n / float(DPS); n += nd
    return [("5.1", st["5.1"] + LINE51[0]), ("5.4d", st["5.4c"] + LINE54)]


def draw(fn, d):
    return s1.draw(fn, d)


def main(out_dir):
    tmp = "/tmp/cs_s5"; os.makedirs(tmp, exist_ok=True)
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
    out = os.path.join(out_dir, "cs_scene5_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a",
                    "-af", "volume=%.2fdB,alimiter=limit=0.60:attack=2:release=40:level=disabled" % (-11.5 - cur),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", tmp + "/o.part.mp4"], check=True)
    os.replace(tmp + "/o.part.mp4", out)
    json.dump({"shots": [{"shot": k, "line": {"key": k, "who": meta[k]["who"], "text": meta[k]["text"], "t0": round(t0, 3),
                                                "t1": round(t0 + meta[k]["len"], 3)}} for k, t0 in schedule()]},
              open("cs_scene5_timing_%s.json" % V, "w"), indent=1)
    A.strip(tiles[::2], os.path.join(out_dir, "cs_scene5_%s_strip.png" % V), 160, 10)
    print("wrote", out, "%d drawings, %.2f s" % (n, total))


if __name__ == "__main__":
    if "lo" in sys.argv[1:]:
        HI[0] = 1
    args = [a for a in sys.argv[1:] if a != "lo"]
    main(args[0] if args else "../customer-success")
