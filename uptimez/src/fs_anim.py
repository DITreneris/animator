"""FIRST SEARCH (episode 10): the animation test, act 7 (7.1 "Young man." to 8.1 "Pam has a plan."), limited animation
at both pacings, to choose between the long (animatic v26, 46.5 s) and the short (animatic v27, 36.6 s) film.

Picked by /grill-me (19 Nov): one test act in both pacings; limited animation as in earlier episodes; 540 previews,
1080 only for the chosen version; the voices and effects plus a quiet music bed, ducked under the voices.

What moves (on twos, 15 drawings a second):
- a slow push-in on every shot (3%), the bubbles pop in over two drawings and leave 0.25 s after the line;
- Mom's mouth flaps on her lines (open, A / E / O, from the voice's loudness), her mouth corner in 7.1;
- 7.1 the hearts rise; 7.2 she comes round mid-stride (a bob), the two men step back; 7.3 the bust shudders on the lick;
  7.4 the thumb scrubs his one hair, Sofía shudders; 7.5 Mom pats Pam, the hearts rise; 8.1 Pam walks in with the plan.

The board's cameras are worked out once per shot and then held, so nothing jitters.

  python3 fs_anim.py [dir]            -> fs_anim_act7_long.mp4, fs_anim_act7_short.mp4 (540 x 960, 30 fps, BT.709)
  python3 fs_anim.py [dir] film540    -> fs_film_long_540.mp4  (the whole film, long pacing; picked 19 Nov)
  python3 fs_anim.py [dir] film1080   -> fs_film_long_1080.mp4 (native 1080: drawn at 2x with set_device_scale)
"""
import os
import sys
import json
import math
import shutil
import subprocess
import numpy as np
import soundfile as sf
import cairo
import kit
from kit import Ctx
import fs_storyboard as sb
import fs_animatic as an
import mom_fs as mfs
import sound_bc_mix as bm
import sound_iwry as si
import sound_xmas as sx

HERE = os.path.dirname(os.path.abspath(__file__))
ACT = ["7.1", "7.2", "7.3", "7.4", "7.5", "8.1"]
W, H, DR = 540, 960, 15                                  # drawings a second (on twos at 30 fps)
SR = an.SR
PACE = {"long": ("fs_timing_v26.json", 0.15), "short": ("fs_timing_v27.json", 0.05)}
MOUTH = [None]


def envelope(wav):
    a, sr = sf.read(wav)
    if a.ndim > 1:
        a = a.mean(1)
    hop = sr // DR
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    return e / max(1e-6, e.max())


def mouth_at(env, i):
    if i < 0 or i >= len(env) or env[i] < 0.18:
        return None
    return ("A", "E", "O", "A")[i % 4] if env[i] > 0.45 else "E"


class _talking:
    """Mom's mouth from MOUTH, wherever she is drawn."""
    def __enter__(self):
        self.f = mfs.mom
        orig = self.f
        def mom(k, x, feet, s=1.0, pose="bag", face="sweet", *a, **kw):
            if MOUTH[0] and kw.get("mouth") is None and face in ("sweet",):
                kw["mouth"] = MOUTH[0]
            return orig(k, x, feet, s, pose, face, *a, **kw)
        mfs.mom = mom
    def __exit__(self, *e):
        mfs.mom = self.f


class _held_camera:
    """The board's camera for a shot, worked out on its first drawing and then held."""
    def __init__(self):
        self.cache = {}
    def __enter__(self):
        self.af, self.br = sb._autoframe, sb._banner_rule
        cache = self.cache
        def af(cam4, heads):
            key = ("af", SHOT[0], cam4)
            if key not in cache:
                cache[key] = self.af(cam4, heads)
            return cache[key]
        def br(cam4, heads, cam0):
            key = ("br", SHOT[0])
            if key not in cache:
                cache[key] = self.br(cam4, heads, cam0)
            return cache[key]
        sb._autoframe, sb._banner_rule = af, br
        return self
    def __exit__(self, *e):
        sb._autoframe, sb._banner_rule = self.af, self.br


SHOT = [None]
BUB = {}


def motion(shot, t, ln):
    """The moving parts of `shot` at t seconds into it (ln long)."""
    u = t / ln
    ease = lambda x: x * x * (3 - 2 * x)
    a = {}
    if shot == "7.1":
        a["hearts"] = 70 * u
    elif shot == "7.2":
        a["m72_dx"] = 50 * (1 - ease(min(1, u * 1.4)))
        a["m72_bob"] = -6 * abs(math.sin(math.pi * 4 * t))
        a["m72_back"] = 14 * ease(min(1, u * 1.6))
    elif shot == "7.4":
        a["scrub"] = 7 * math.sin(2 * math.pi * 5 * t)
        a["shudder"] = 2.5 * math.sin(2 * math.pi * 9 * t) if t > 0.25 else 0
    elif shot == "7.5":
        a["pat"] = -7 * abs(math.sin(2 * math.pi * 2.5 * t))
        a["hearts"] = 50 * u
    elif shot == "8.1":
        a["pam_dx"] = -60 * (1 - ease(min(1, u * 1.8)))
        a["pam_bob"] = -5 * abs(math.sin(math.pi * 4 * t)) if u < 0.55 else 0
    return a


def frame(shot, fn, t, ln, line, lead, env, surf):
    """One drawing: the shot, pushed in, its bubble popped."""
    c0 = cairo.Context(surf)
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(tmp); k = Ctx(c, 0)
    sb.bg(c)
    sb.ANIM.clear(); sb.ANIM.update(motion(shot, t, ln))
    i = int(round((t - lead) * DR))
    MOUTH[0] = mouth_at(env, i) if env is not None else None
    if shot == "7.1" and MOUTH[0]:
        sb.ANIM["talk"] = {"A": 1.0, "E": 0.6, "O": 0.9}[MOUTH[0]]
    sb.HEADS.clear(); sb.AVOID.clear()
    with sb._norm(record_only=True):
        fn(k)
    heads, avoid = dict(sb.HEADS), list(sb.AVOID)
    z = 1 + 0.03 * (t / ln)                                # the push-in
    if shot == "7.3" and 0.1 < t < 0.45:                   # the lick: a shudder
        dx, dy = 3 * math.sin(2 * math.pi * 11 * t), 2 * math.sin(2 * math.pi * 7 * t)
    else:
        dx = dy = 0
    c0.save(); c0.translate(270 + dx, 480 + dy); c0.scale(z, z); c0.translate(-270, -480)
    c0.set_source_surface(tmp, 0, 0); c0.paint(); c0.restore()
    heads = {n: ((x - 270) * z + 270, (y - 480) * z + 480, r * z) for n, (x, y, r) in heads.items()}
    if line:
        who, text, t0, t1 = line
        if t0 <= t < t1 + 0.25:
            if BUB.get(shot) is None:                      # the bubble is placed once, where the line starts
                BUB[shot] = (heads, avoid, z)
            heads, avoid, z = BUB[shot]
            heads = dict(heads)
            n = int(round((t - t0) * DR))
            pop = (0.82, 1.05)[n] if n < 2 else 1.0
            sb.AVOID[:] = [(x0 * z + 270 * (1 - z), y0 * z + 480 * (1 - z), x1 * z + 270 * (1 - z), y1 * z + 480 * (1 - z))
                           for x0, y0, x1, y1 in avoid]
            dry = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            dc = cairo.Context(dry)
            box = _say_box(dc, Ctx(dc, 0), who, text, heads)
            cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            c0.save(); c0.translate(cx, cy); c0.scale(pop, pop); c0.translate(-cx, -cy)
            an.say(c0, Ctx(c0, 0), who, text, heads)
            c0.restore()


def _say_box(c, k, who, text, heads):
    names = an.SPEAKER.get(who, [])
    n = names[0] if names else None
    others = [h for m, h in heads.items() if m != n]
    mono = who == "ROBOT"
    return an.speech(c, k, text.upper() if mono else text, heads.get(n), others, mono=mono, size=24 if mono else 30)


def bed(total):
    l, r, bar = bm.bed(total + 2.0, max(2, int(round((total + 2.0) / 2.4))))
    n = int(total * SR)
    return (l[:n] + r[:n]) / 2


def build(d, pace):
    tfile, lead = PACE[pace]
    rows = {r["shot"]: r for r in json.load(open(os.path.join(d, tfile)))}
    fns = {s: fn for s, _, fn, _ in sb.SHOTS}
    t0 = rows[ACT[0]]["start"]
    total = sum(rows[s]["len"] for s in ACT)
    out_dir = "/tmp/fs_anim_%s" % pace
    shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    voice = np.zeros(int((total + 1) * SR))
    lines, envs = {}, {}
    for s in ACT:
        if s in an.LINE_OF:
            m = an.TAKES[an.LINE_OF[s]]
            wav = os.path.join(HERE, an.VOICES, "%s.wav" % an.LINE_OF[s])
            a, _ = sf.read(wav)
            a = a.mean(1) if a.ndim > 1 else a
            st = rows[s]["start"] - t0 + lead
            an._at(voice, a, st, 1.0)
            lines[s] = (m["who"], m["text"], lead, lead + m["len"])
            envs[s] = envelope(wav) if m["who"] == "MOM" else None
    n = 0
    BUB.clear()
    with _talking(), _held_camera():
        for s in ACT:
            SHOT[0] = s
            ln = rows[s]["len"]
            pre = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)     # the held camera: where everyone ends up
            frame(s, fns[s], ln, ln, None, lead, None, pre)
            for j in range(int(round(ln * DR))):
                t = j / DR
                surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
                frame(s, fns[s], t, ln, lines.get(s), lead, envs.get(s), surf)
                surf.write_to_png("%s/f%05d.png" % (out_dir, n)); n += 1
    sb.ANIM.clear(); MOUTH[0] = None
    fx = np.zeros_like(voice)                              # the effects
    at = {s: rows[s]["start"] - t0 for s in ACT}
    an._at(fx, an.slurp(), at["7.3"] + 0.05, 0.35)
    an._at(fx, an.squeak(), at["7.4"] + 0.05, 0.10)
    an._at(fx, an.squeak(), at["7.4"] + 0.30, 0.10)
    for i in range(3):                                     # her heels, coming round the counter
        an._at(fx, sx.thunk(0.04, 700), at["7.2"] + 0.05 + i * 0.25, 0.10)
    env = si.lp(np.abs(voice), int(SR * 0.08))             # the bed, ducked under the voices
    env = env / max(1e-6, env.max())
    b = bed(len(voice) / SR)
    b = b[:len(voice)] if len(b) >= len(voice) else np.pad(b, (0, len(voice) - len(b)))
    mix = voice + fx + b * (0.16 - 0.10 * np.clip(env * 3, 0, 1))
    mix = mix[:int(total * SR)]
    mix *= 0.5 / max(1e-6, np.abs(mix).max())
    wav = os.path.join(out_dir, "mix.wav")
    sf.write(wav, np.stack([mix, mix], 1).astype(np.float32), SR)
    out = os.path.join(d, "fs_anim_act7_%s.mp4" % pace)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(DR), "-i", "%s/f%%05d.png" % out_dir, "-i", wav,
                    "-vf", "fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "18", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-color_range", "tv",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    print("wrote", out, "%.2f s" % total)
    return out




# ---------------------------------------------------------------- the whole film (picked 19 Nov: the long pacing)
OTS = {"2.3", "5.2"}                                       # the speaker seen from behind: no mouth on the back of a head
SHAKE = {"1.1a": (0.35, 99, 3.0), "1.1b": (0.0, 0.2, 6.0), "3.4": (0.0, 99, 1.2), "9.5": (0.0, 99, 2.5)}


def motion_all(shot, t, ln):
    a = motion(shot, t, ln)
    u = t / ln
    if shot == "9.3":
        a["plaster_up"] = 160 * (1 - min(1, u * 1.6)) ** 2
        a["plaster_spin"] = -0.6 * (1 - min(1, u * 1.6))
        a["twinkle"] = math.sin(2 * math.pi * 3 * t)
    return a


def _mouth_overlay(c, head, amt):
    """An open mouth over a face that has no mouth shapes of its own (Don, Sofía, the Client)."""
    x, y, r = head
    c.save(); c.translate(x, y + 0.40 * r); c.scale(0.20 * r, 0.13 * r * amt)
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(0.30, 0.10, 0.12); c.fill_preserve()
    c.set_source_rgb(*kit.INK); c.set_line_width(max(1.5, r * 0.035)); c.stroke()


def frame_full(shot, fn, t, ln, lines, surf, S):
    """One drawing of the film: the shot (its moving parts), pushed in, shaken where it shakes, its mouths and bubbles."""
    c0 = cairo.Context(surf)
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * S, H * S); tmp.set_device_scale(S, S)
    c = cairo.Context(tmp); k = Ctx(c, 0)
    sb.bg(c)
    sb.ANIM.clear(); sb.ANIM.update(motion_all(shot, t, ln))
    act = [ln_ for ln_ in lines if ln_[2] <= t < ln_[3]]                 # (who, text, t0, t1, env) in shot time
    MOUTH[0] = None
    for who, text, t0, t1, env in act:
        if who == "MOM" and env is not None:
            MOUTH[0] = mouth_at(env, int(round((t - t0) * DR)))
    sb.HEADS.clear(); sb.AVOID.clear()
    with sb._norm(record_only=True):
        fn(k)
    heads, avoid = dict(sb.HEADS), list(sb.AVOID)
    z = 1 + 0.03 * (t / ln)
    dx = dy = 0.0
    if shot in SHAKE:
        a0, a1, amp = SHAKE[shot]
        if a0 <= t <= a1:
            dx, dy = amp * math.sin(2 * math.pi * 13 * t), amp * 0.6 * math.sin(2 * math.pi * 9 * t + 1)
    if shot == "7.3" and 0.1 < t < 0.45:
        dx, dy = 3 * math.sin(2 * math.pi * 11 * t), 2 * math.sin(2 * math.pi * 7 * t)
    c0.save(); c0.translate(270 + dx, 480 + dy); c0.scale(z, z); c0.translate(-270, -480)
    c0.set_source_surface(tmp, 0, 0); c0.paint(); c0.restore()
    tz = lambda x, y: ((x - 270) * z + 270 + dx, (y - 480) * z + 480 + dy)
    heads = {n: tz(x, y) + (r * z,) for n, (x, y, r) in heads.items()}
    for who, text, t0, t1, env in act:                                   # the mouths that have no shapes of their own
        if who in ("DON", "SOFIA", "CLIENT", "PAM+SOFIA") and shot not in OTS and env is not None:
            i = int(round((t - t0) * DR))
            m = mouth_at(env, i)
            n = {"DON": "don", "SOFIA": "sofia", "CLIENT": "client", "PAM+SOFIA": "sofia"}[who]
            h = heads.get(n)
            if m and h and 0 <= h[0] <= 540 and 0 <= h[1] <= 960:
                _mouth_overlay(c0, h, {"A": 1.0, "E": 0.55, "O": 0.85}[m])
    for who, text, t0, t1, env in lines:                                 # the bubbles
        if t0 <= t < t1 + 0.25:
            key = (shot, text)
            if key not in BUB:
                BUB[key] = (heads, [tuple(list(tz(a_[0], a_[1])) + list(tz(a_[2], a_[3]))) for a_ in avoid])
            hh, av = BUB[key]
            sb.AVOID[:] = av
            n = int(round((t - max(t0, 0)) * DR))
            pop = (0.82, 1.05)[n] if (n < 2 and t0 >= 0) else 1.0
            dry = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            dc = cairo.Context(dry)
            box = _say_box(dc, Ctx(dc, 0), who, text, hh)
            cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            c0.save(); c0.translate(cx, cy); c0.scale(pop, pop); c0.translate(-cx, -cy)
            an.say(c0, Ctx(c0, 0), who, text, hh)
            c0.restore()


def build_full(d, pace="long", S=1):
    tfile, lead = PACE[pace]
    rows = json.load(open(os.path.join(d, tfile)))
    fns = {s: fn for s, _, fn, _ in sb.SHOTS}
    order = [r["shot"] for r in rows]
    assert order == [s for s, _, _, _ in sb.SHOTS], "the timing and the board disagree on the shots"
    at = {r["shot"]: r["start"] for r in rows}
    total = rows[-1]["start"] + rows[-1]["len"]
    lines_abs = []                                                       # (who, text, t0, t1, env) in film time
    voice = np.zeros(int((total + 1) * SR))
    for s in order:
        if s in an.LINE_OF:
            key = an.LINE_OF[s]
            m = an.TAKES[key]
            wav = os.path.join(HERE, an.VOICES, "%s.wav" % key)
            a, _ = sf.read(wav)
            a = a.mean(1) if a.ndim > 1 else a
            t0 = at[s] + lead
            an._at(voice, a, t0, 1.0)
            lines_abs.append((m["who"], m["text"], t0, t0 + m["len"], envelope(wav)))
    tag = "%s_%d" % (pace, 540 * S)
    out_dir = "/tmp/fs_film_%s" % tag
    shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    n = 0
    BUB.clear()
    with _talking(), _held_camera():
        for r in rows:
            s, ln = r["shot"], r["len"]
            SHOT[0] = s
            local = [(w, tx, a - r["start"], b - r["start"], e) for w, tx, a, b, e in lines_abs
                     if a < r["start"] + ln and b + 0.25 > r["start"]]
            pre = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
            frame_full(s, fns[s], ln, ln, [], pre, 1)
            BUB.clear()
            for j in range(int(round(ln * DR))):
                surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * S, H * S); surf.set_device_scale(S, S)
                frame_full(s, fns[s], j / DR, ln, local, surf, S)
                surf.write_to_png("%s/f%05d.png" % (out_dir, n)); n += 1
    sb.ANIM.clear(); MOUTH[0] = None
    old = an.LEAD
    an.LEAD = lead
    try:
        m = an.mix(rows, total)                                          # the animatic's voices and effects
    finally:
        an.LEAD = old
    m = m[:len(voice)] if len(m) >= len(voice) else np.pad(m, (0, len(voice) - len(m)))
    for i in range(3):                                                   # her heels, round the counter
        an._at(m, sx.thunk(0.04, 700), at["7.2"] + 0.05 + i * 0.25, 0.05)
    env = (np.abs(voice) > 0.01).astype(float)                           # the bed ducks a beat before a line and comes
    env = si.lp(env, int(SR * 0.35)); env = env / max(1e-6, env.max())   # back after it (Whisper hears through it)
    b = bed(len(voice) / SR)
    b = b[:len(voice)] if len(b) >= len(voice) else np.pad(b, (0, len(voice) - len(b)))
    mix = m + b * (0.10 - 0.085 * np.clip(env * 4, 0, 1))
    mix = mix[:int(total * SR)]
    mix *= 0.5 / max(1e-6, np.abs(mix).max())
    wav = os.path.join(out_dir, "mix.wav")
    sf.write(wav, np.stack([mix, mix], 1).astype(np.float32), SR)
    out = os.path.join(d, "fs_film_%s.mp4" % tag)
    nf = int(round(total * 30))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(DR), "-i", "%s/f%%05d.png" % out_dir, "-i", wav,
                    "-vf", "fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "18", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-color_range", "tv", "-frames:v", str(nf),
                    "-af", "loudnorm=I=-14.5:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    print("wrote", out, "%.2f s" % total)
    return out


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../first-search"
    what = sys.argv[2] if len(sys.argv) > 2 else "act"
    if what == "act":
        for p in ("long", "short"):
            build(d, p)
    else:                                                  # film540 / film1080
        build_full(d, "long", 2 if what == "film1080" else 1)
