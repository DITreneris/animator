"""OFFICE NOIR 2: voices and sound, v1. 17 Nov.
  narr(txt, kind)   Sofia's narration, three ways for the audition (Tomas chooses):
                      "A"  as in the animatic: her voice two semitones down, pace 0.95
                      "B"  quicker and drier: pace 1.08, no added darkness
                      "C"  slower and close: pace 0.84, darker, quieter, a longer breath between sentences
  takes()           every line of script v2, written to on2_voices/takes_v1 (narration in all three kinds),
                    and each take given to Whisper on its own: what a listener with no picture hears
  audition()        on2_narration_audition_v1.mp4: two lines, A then B then C, the letter on screen
  motion_mix()      the sound of the motion test (beats 01 and 02): the first film's jazz, rain, the narration, her heels
  KOKORO_DIR=/tmp/kokoro python3 on2_sound.py"""
import json
import os
import subprocess
import sys
import numpy as np
import soundfile as sf

os.environ.setdefault("KOKORO_DIR", "/tmp/kokoro")
import sound_on as so
import sound_on_jazz as oj
import sound_bc as bc
import sound_ob as sob
import sound_xmas as sx
import sound_iwry as si

SR = so.SR
TAKES = "on2_voices/takes_v1"
NARR = [("n1", "New Year's Eve."), ("n2", "A woman like me doesn't walk alone."), ("n3", "I don't run. I give them something to chase."),
        ("n4", "He sent a note. They always send a note."), ("n5", "Everybody had lost it. I found it in one drawer.")]
NARR2 = [("n6", "The whole city was celebrating."), ("n7", "The law was always one step behind me."),          # 18 Nov: six more lines
         ("n8", "Every door in this town opens for me."), ("n9", "I never hide. I let them look."), ("n10", "I gave him my number."),
         ("n11", "Let him come.")]
KINDS = {"A": "as in the animatic", "B": "quicker and drier", "C": "slower and close",
         "A2": "A, a touch lower and slower"}                 # Tomas, 17 Nov: "I like A; barely lower, barely slower"


def trim(a):
    idx = np.where(np.abs(a) > 0.012)[0]
    return a if not len(idx) else a[max(0, idx[0] - int(0.02 * SR)):min(len(a), idx[-1] + int(0.10 * SR))]


def _one(txt, speed, semis, dark):
    v = si.K.get_voice_style(so.SOF)
    a = np.asarray(si.K.create(txt, voice=v, speed=speed, lang="en-us")[0], dtype=np.float64)
    a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * SR / 24000)), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.01)[0]
    a = so.pitch(a[max(0, idx[0] - 600):idx[-1] + 2400], semis)
    a = a * (1 - dark) + si.lp(a, 4) * dark
    return a / np.sqrt(np.mean(a ** 2)) * 0.11


def narr(txt, kind="A"):
    if kind == "A":
        return _one(txt, 0.95, -2.0, 0.2)
    if kind == "A2":                                       # half a semitone down, three per cent slower
        return _one(txt, 0.92, -2.5, 0.2)
    if kind == "B":
        return _one(txt, 1.08, -2.0, 0.0)
    parts = [p.strip() for p in txt.replace("?", "?|").replace(".", ".|").split("|") if p.strip()]      # C: sentence by sentence
    out = []
    for i, p in enumerate(parts):
        out.append(_one(p, 0.84, -2.0, 0.45) * 0.86)
        if i + 1 < len(parts):
            out.append(np.zeros(int(0.22 * SR)))
    return np.concatenate(out)


def others():
    pv, psp, _ = sx.PAMS["A"]
    m1 = np.asarray(bc.mom_shout("You! Not near Donnie's desk!"), dtype=np.float64)
    m1 = m1 / np.sqrt(np.mean(m1 ** 2)) * 0.15
    c1 = trim(np.asarray(sob.client_line("I only want my"), dtype=np.float64))
    return {
        "s1": ("SOFÍA", "The usual.", bc.sofia("The usual.")),
        "m1": ("MOM", "You! Not near Donnie's desk!", m1),
        "c1": ("THE SHADOW", "I only want my", so.cut_off(c1, len(c1) / SR - 0.06)),
        "m2": ("MOM", "Happy New Year, dear.", bc.mom("Happy New Year, dear.")),
        "p1": ("PAM", "Some dream. Others sweep.", bc.norm(so.dry("Some dream. Others sweep.", pv, 1.0))),
    }


def takes():
    import on_qa as oq
    os.makedirs(TAKES, exist_ok=True)
    rec = oq._recognizer()
    meta, rows = {}, []

    def keep(key, who, want, a):
        a = trim(np.asarray(a, dtype=np.float64))
        path = "%s/%s.wav" % (TAKES, key)
        sf.write(path, a.astype(np.float32), SR)
        b = np.concatenate([np.zeros(4800), np.interp(np.arange(0, len(a), SR / 16000.0), np.arange(len(a)), a), np.zeros(6400)]).astype(np.float32)
        got = oq.transcribe(rec, b, 0, len(b) / 16000.0)
        w, h = oq._words(want), oq._words(got)
        score = oq._lcs(w, h) / max(1, len(w))
        meta[key] = {"who": who, "text": want, "len": round(len(a) / SR, 3), "heard": got, "score": round(score, 2)}
        rows.append("  %-4s %-5s %-10s %.2fs  %3.0f%%  want \"%s\"  heard \"%s\"" % ("ok" if score >= 0.75 else "MISS", key, who, len(a) / SR, score * 100, want, got))

    for kind in "ABC":
        for key, txt in NARR:
            keep("%s_%s" % (key, kind), "N (" + kind + ")", txt, narr(txt, kind))
    for key, (who, txt, a) in others().items():
        keep(key, who, txt, a)
    json.dump(meta, open(TAKES + "/takes.json", "w"), indent=1, ensure_ascii=False)
    print("\n".join(rows))
    for kind in "ABC":
        print("  narration %s: %.2f s for the five lines" % (kind, sum(meta["%s_%s" % (k, kind)]["len"] for k, _ in NARR)))
    return meta


def take_kind(kind, lines=None):
    """Record the five narration lines in one more kind, check each alone, and add them to takes.json.
    lines (18 Nov): other (key, text) pairs to record instead, such as NARR2; the takes already made are not touched."""
    import on_qa as oq
    meta = json.load(open(TAKES + "/takes.json"))
    rec = oq._recognizer()
    for key, txt in (lines or NARR):
        a = trim(np.asarray(narr(txt, kind), dtype=np.float64))
        sf.write("%s/%s_%s.wav" % (TAKES, key, kind), a.astype(np.float32), SR)
        b = np.concatenate([np.zeros(4800), np.interp(np.arange(0, len(a), SR / 16000.0), np.arange(len(a)), a), np.zeros(6400)]).astype(np.float32)
        got = oq.transcribe(rec, b, 0, len(b) / 16000.0)
        w, h = oq._words(txt), oq._words(got)
        score = oq._lcs(w, h) / max(1, len(w))
        meta["%s_%s" % (key, kind)] = {"who": "N (%s)" % kind, "text": txt, "len": round(len(a) / SR, 3), "heard": got, "score": round(score, 2)}
        print("  %-4s %-6s %.2fs  %3.0f%%  heard \"%s\"" % ("ok" if score >= 0.75 else "MISS", key + "_" + kind, len(a) / SR, score * 100, got))
    json.dump(meta, open(TAKES + "/takes.json", "w"), indent=1, ensure_ascii=False)
    print("  narration %s: %.2f s for these lines" % (kind, sum(meta["%s_%s" % (k, kind)]["len"] for k, _ in (lines or NARR))))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-2000:])


def audition(out="../office-noir-2/on2_narration_audition_v1.mp4"):
    """Two lines in each of the three ways, the letter and what it is on the picture."""
    import cairo
    import on2_board as b
    meta = json.load(open(TAKES + "/takes.json"))
    tmp = "/tmp/on2/aud"; os.makedirs(tmp, exist_ok=True)
    base = [b.render(2), b.render(7)]                                    # 2.1 and 2.6: where these two lines are said
    segs, audio, t = [], [], 0.0
    for kind in "ABC":
        for j, key in enumerate(("n2", "n3")):
            m = meta["%s_%s" % (key, kind)]
            dur = round((0.35 + m["len"] + 0.55) * 30) / 30.0
            s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(s2)
            c.set_source_surface(base[j], 0, 0); c.paint()
            c.set_source_rgba(0.04, 0.04, 0.06, 0.86); c.rectangle(18, 110, 504, 120); c.fill()
            c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(74); c.move_to(40, 200); c.show_text(kind)
            c.set_font_size(24); c.move_to(120, 168); c.show_text(KINDS[kind])
            c.select_font_face("Inter", 0, 0); c.set_font_size(20); c.move_to(120, 204)
            c.show_text("%.1f s for this line" % m["len"])
            c.set_source_rgba(0.04, 0.04, 0.06, 0.82); c.rectangle(18, 736, 504, 84); c.fill()
            c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD); c.set_font_size(23)
            words, line, yy = m["text"].split(), "", 770
            for wd in words:
                trial = (line + " " + wd).strip()
                if c.text_extents(trial).x_advance > 470 and line:
                    e = c.text_extents(line); c.move_to((540 - e.x_advance) / 2, yy); c.show_text(line); line = wd; yy += 30
                else:
                    line = trial
            e = c.text_extents(line); c.move_to((540 - e.x_advance) / 2, yy); c.show_text(line)
            png = "%s/a_%s_%d.png" % (tmp, kind, j); s2.write_to_png(png)
            seg, part = "%s/a_%s_%d.mp4" % (tmp, kind, j), "%s/a_%s_%d.part.mp4" % (tmp, kind, j)
            run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", png, "-vf", "format=yuv420p,loop=-1:1,trim=duration=%.5f" % dur,
                 "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", part])
            os.replace(part, seg); segs.append("file '%s'" % seg)
            a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind))
            audio.append((t + 0.35, a)); t += dur
    open(tmp + "/list.txt", "w").write("\n".join(segs) + "\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "/list.txt", "-c", "copy", tmp + "/v.mp4"])
    mix = np.zeros(int((t + 0.3) * SR))
    for t0, a in audio:
        p = int(t0 * SR); mix[p:p + len(a)] += a[:len(mix) - p]
    sf.write(tmp + "/a.wav", (np.tanh(mix * 2.2) / 2.2 * 1.6).astype(np.float32), SR)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp + "/v.mp4", "-i", tmp + "/a.wav", "-map", "0:v", "-map", "1:a", "-af",
         "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", tmp + "/out.part.mp4"])
    os.replace(tmp + "/out.part.mp4", out)
    return out, t


def heel():
    t = so.tt(0.09)
    n = np.random.default_rng(5).standard_normal(len(t))
    return (so.hp(n, 3) * np.exp(-t / 0.012) * 0.5 + np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.02) * 0.25)


def motion_mix(rows, total, kind="A", out="/tmp/on2/motion_mix.wav"):
    """rows: [(shot, start, length)] of the motion test. Music from 0.4 s, under everything; rain all through; the
    narration of beats 01 and 02 at lead 0.25; her heels; the compact on the stones."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    cues = {"1.1": "n1", "2.1": "n2", "2.6": "n3"}
    spans = []
    for shot, key in cues.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h = heel()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(9):                                                    # running, 2.6
        put(at["2.6"] + 0.10 + i * 0.25, h, 0.75 - i * 0.05)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def thud():
    """A man's shoe on wet stone, far softer than her heel."""
    t = so.tt(0.12)
    return np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.035) * 0.55 + so.hp(np.random.default_rng(9).standard_normal(len(t)), 2) * np.exp(-t / 0.02) * 0.06


def motion_mix3(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v3: beats 01 to 04. motion_mix is left as it was. The run is the smooth loop: a heel every third of
    a second. New: her run past the sweeper, the broom, the detective's steps, the coin in the cup, the robot."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(5):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + 0.1 + i * 0.44, th, 0.35 + i * 0.05)
    put(at["3.2"] + 1.0, so.swish(0.38), 0.8)                             # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(5):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 0.22, th, 0.75 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)
    put(at["4.1b"] + 2 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 3 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 5 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix4(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v4: motion_mix3 with the new timings. The detective walks: a heavy step every five drawings, coming
    (3.2) and going (3.4). The sweep has a lift before it. At the door she takes two steps before the arm comes out."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(6):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix5(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v5: motion_mix4 and beat 05, the bar. Indoors the rain is only heard through the wall and the
    band is nearer. Her spoken line and the fourth line of narration; glasses, banknotes, his steps, the napkin, her
    finger, the lipstick, the stamp."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(6):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27, 32):                                         # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 31), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (12, 14):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (0, 3):                                                     # 5.8: to the door
        put(at5("5.8", dr), h, 0.42)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    inside = np.clip((np.arange(n) / SR - b0) / 0.6, 0.0, 1.0)            # the door closes behind her
    rain = rain * (1.0 - 0.84 * inside)
    music = music * (1.0 + 0.30 * inside)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix6(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v7, the whole film: motion_mix5 and beats 06 to 08. The office: the door, the drawer, the lamp,
    keys. The wall: Mom's shout, his half sentence, one pop, and the jazz stops dead on it. The party: Auld Lang Syne
    on vibes, the blower, the broom; at the window the rain comes back, for the loop."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.2": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(6):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27, 32):                                         # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 31), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (12, 14):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (0, 3):                                                     # 5.8: to the door
        put(at5("5.8", dr), h, 0.42)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 0), so.swish(0.30), 0.4); put(at5("6.2", 12), so.swish(0.35), 0.35)   # 6.2: the drawer; the roll
    for dr in (24, 27):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.3", 10), so.metal_click(2200, 0.04), 0.6)                  # 6.3: the lamp
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 5), th, 0.5)
    for dr in (10, 14, 19):                                               # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 2), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix7(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v8, the cut film: motion_mix6 without the two set-ups that were dropped (5.8, 6.3) and with the
    cues moved to the trimmed shots. New: the cloth on the glass, the pour from the bottle, the door still swinging."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.2": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(4):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27, 32):                                         # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 31), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (11, 13):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 0), so.swish(0.30), 0.4); put(at5("6.2", 12), so.swish(0.35), 0.35)   # 6.2: the drawer; the roll
    for dr in (24, 27):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    for dr in (10, 14, 19):                                               # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 2), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix8(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v9: motion_mix7 with the cues moved for the two shots that changed length or order inside:
    6.2 (the drawer is pulled out first, then the roll) and 8.2 (she sleeps for half a second before she starts up)."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.2": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(4):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27, 32):                                         # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 31), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (11, 13):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2", 18), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    for dr in (10, 14, 19):                                               # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix9(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v13: motion_mix8 and the gang war behind her in 1.2: shots far off, low and dull, through the
    rain, each one quieter than her heel and far quieter than the pop in 7.3."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.2": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.22 if who < 2 else 0.17)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(4):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27, 32):                                         # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 31), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (11, 13):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2", 18), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    for dr in (10, 14, 19):                                               # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix10(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v15: motion_mix9 with her six new lines (the music ducks under them too), and the cues that
    fell past the end of the trimmed shots taken out."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.2": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.22 if who < 2 else 0.17)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(3):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 1.5 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (11, 13):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2", 18), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    for dr in (10, 14, 19):                                               # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix11(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v16: motion_mix10 with the cues moved for the trimmed shots, and the drawer line on 6.1."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.1": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.22 if who < 2 else 0.17)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(2):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 10 / 12.0 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (8, 9):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2", 18), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    for dr in (10, 14):                                                   # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix12(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v17: motion_mix11 and three more far-off shots in the close-up 1.2b."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.1": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.22 if who < 2 else 0.17)
    for dr in (1, 4, 7):                                                  # 1.2b: and while we are close on her
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); put(at["1.2b"] + dr / 12.0 + 0.03, np.convolve(crack, np.ones(k_) / k_, mode="same"), 0.2)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(2):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 10 / 12.0 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (8, 9):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2", 18), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    for dr in (10, 14):                                                   # 7.1: his shoes
        put(at5("7.1", dr), th, 0.6)
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - (total - 1.9)) / 1.6, 0.0, 1.0)                # at the window the rain comes back
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - tsec) / 2.0, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans



def motion_mix13(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v17: motion_mix11 and three more far-off shots in the close-up 1.2b."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.1": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.22 if who < 2 else 0.17)
    for dr in (1, 4, 7):                                                  # 1.2b: and while we are close on her
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); put(at["1.2b"] + dr / 12.0 + 0.03, np.convolve(crack, np.ones(k_) / k_, mode="same"), 0.2)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(2):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 10 / 12.0 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (8, 9):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2c", 6), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2c", dr - 12), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    put(at5("7.1c", 0), th, 0.6); put(at5("7.1c", 4), th, 0.6)          # 7.1: his shoes
    put(at5("6.2r", 4), so.sting(220.0, 0.6), 0.25)                       # v21: the drawer: her little win
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    put(at5("8.5", 17), so.metal_click(700, 0.05), 0.35); put(at5("8.5", 17), so.swish(0.30), 0.3)   # v21: into the pan; the puff
    tw = so.tt(0.75)                                                      # v21, 8.6: the blower again, and it gives up
    ph = 2 * np.pi * np.cumsum(330 - 120 * tw / 0.75 + 14 * np.sin(2 * np.pi * 7 * tw)) / SR
    fiz = (np.sin(ph) + np.sin(3 * ph) / 3) * np.minimum(1, tw / 0.03) * np.clip((0.75 - tw) / 0.35, 0, 1) * 0.08
    put(at5("8.6", 14), fiz, 1.0)
    tend = at5("8.6", 24)                                                 # black: everything stops
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.zeros(n)                                                    # v21: no window at the end
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((tend - tsec) / 0.03, 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = mix * np.clip((tend + 0.03 - tsec) / 0.03, 0.0, 1.0)          # v21: the sound cuts with the picture
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix14(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v17: motion_mix11 and three more far-off shots in the close-up 1.2b."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.1": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.22 if who < 2 else 0.17)
    for dr in (1, 4, 7):                                                  # 1.2b: and while we are close on her
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.004 * SR); put(at["1.2b"] + dr / 12.0 + 0.03, np.convolve(crack, np.ones(k_) / k_, mode="same"), 0.2)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(2):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 10 / 12.0 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (8, 9):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2c", 6), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2c", dr - 12), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    put(at5("7.1c", 0), th, 0.6); put(at5("7.1c", 4), th, 0.6)          # 7.1: his shoes
    put(at5("6.2r", 4), so.sting(220.0, 0.6), 0.25)                       # v21: the drawer: her little win
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    put(at5("8.5", 17), so.metal_click(700, 0.05), 0.35); put(at5("8.5", 17), so.swish(0.30), 0.3)   # v21: into the pan; the puff
    tw = so.tt(0.75)                                                      # v21, 8.6: the blower again, and it gives up
    ph = 2 * np.pi * np.cumsum(330 - 120 * tw / 0.75 + 14 * np.sin(2 * np.pi * 7 * tw)) / SR
    fiz = (np.sin(ph) + np.sin(3 * ph) / 3) * np.minimum(1, tw / 0.03) * np.clip((0.75 - tw) / 0.35, 0, 1) * 0.08
    put(at5("8.6", 14), fiz, 1.0)
    tend = at["8.7"]                                                      # v22: into the window
    tb_ = so.tt(0.95)                                                      # the taxi's brakes, ending on the seam
    sq = np.sin(2 * np.pi * np.cumsum(2300 - 500 * tb_ / 0.95 + 40 * np.sin(2 * np.pi * 9 * tb_)) / SR)
    hiss = np.random.default_rng(77).standard_normal(len(tb_))
    env_ = np.minimum(1, tb_ / 0.15) * np.clip((0.95 - tb_) / 0.12, 0, 1)
    put(total - 0.95, (sq * 0.05 + so.hp(hiss, 3) * 0.06) * env_, 1.0)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - tend) / (total - tend), 0.0, 1.0) / 0.9         # v22: the rain comes back to where the film starts
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - 0.15 - tsec) / (total - 0.15 - tend), 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans


def motion_mix15(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav"):
    """Motion test v17: motion_mix11 and three more far-off shots in the close-up 1.2b."""
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.1": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11"}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        p = int((at[shot] + 0.25) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + 0.25, at[shot] + 0.25 + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    put(at["1.1"] + 11 / 12.0, h, 1.0)                                    # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1)):      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.0015 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")       # v23: brighter, and louder
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.60 if who < 2 else 0.48)
        put(at["1.2"] + dr / 12.0 + 0.12, dull, 0.20 if who < 2 else 0.16)                  # the slap off the walls
    for dr in (1, 4, 7):                                                  # 1.2b: and while we are close on her
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.0015 * SR); a_ = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2b"] + dr / 12.0 + 0.03, a_, 0.50); put(at["1.2b"] + dr / 12.0 + 0.12, a_, 0.16)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(2):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 10 / 12.0 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (8, 9):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2c", 6), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2c", dr - 12), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    put(at5("7.1c", 0), th, 0.6); put(at5("7.1c", 4), th, 0.6)          # 7.1: his shoes
    put(at5("6.2r", 4), so.sting(220.0, 0.6), 0.25)                       # v21: the drawer: her little win
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    put(at5("8.5", 17), so.metal_click(700, 0.05), 0.35); put(at5("8.5", 17), so.swish(0.30), 0.3)   # v21: into the pan; the puff
    tw = so.tt(0.75)                                                      # v21, 8.6: the blower again, and it gives up
    ph = 2 * np.pi * np.cumsum(330 - 120 * tw / 0.75 + 14 * np.sin(2 * np.pi * 7 * tw)) / SR
    fiz = (np.sin(ph) + np.sin(3 * ph) / 3) * np.minimum(1, tw / 0.03) * np.clip((0.75 - tw) / 0.35, 0, 1) * 0.08
    put(at5("8.6", 14), fiz, 1.0)
    tend = at["8.7"]                                                      # v22: into the window
    tb_ = so.tt(0.95)                                                      # the taxi's brakes, ending on the seam
    sq = np.sin(2 * np.pi * np.cumsum(2300 - 500 * tb_ / 0.95 + 40 * np.sin(2 * np.pi * 9 * tb_)) / SR)
    hiss = np.random.default_rng(77).standard_normal(len(tb_))
    env_ = np.minimum(1, tb_ / 0.15) * np.clip((0.95 - tb_) / 0.12, 0, 1)
    put(total - 0.95, (sq * 0.05 + so.hp(hiss, 3) * 0.06) * env_, 1.0)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - tend) / (total - tend), 0.0, 1.0) / 0.9         # v22: the rain comes back to where the film starts
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - 0.15 - tsec) / (total - 0.15 - tend), 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans

if __name__ == "__main__":
    if len(sys.argv) > 1:
        take_kind(sys.argv[1])
    else:
        takes()
        o, t = audition()
        print("wrote", o, "%.1f s" % t)


def caw(d=0.30):
    """v29 (25 Nov): the raven, once: a harsh 'kraa', a buzzing saw with a nasal band, the pitch falling"""
    t = so.tt(d)
    f = 560 - 180 * t / d
    ph = 2 * np.pi * np.cumsum(f + 25 * np.sin(2 * np.pi * 31 * t)) / SR
    saw = sum(np.sin(k * ph) / k for k in range(1, 14))
    nz = np.random.default_rng(5).standard_normal(len(t))
    rough = so.hp(nz, 3) * 0.35 * (1 + np.sin(2 * np.pi * 70 * t))
    env = np.minimum(1, t / 0.012) * np.clip((d - t) / 0.12, 0, 1) * (1 + 0.4 * np.sin(2 * np.pi * 9 * t))
    return (saw * 0.22 + rough) * env * 0.5


def motion_mix16(rows, total, kind="A2", out="/tmp/on2/motion_mix.wav", leads=None, heel_at=11 / 12.0, shots12=None, raven=False, swap=None):
    """Motion test v28: motion_mix15 with the opening re-timed (Tomas: a joke by 0:01). leads: a line's start after its
    shot, where it isn't 0.25 (the city line waits for New Year's Eve.); heel_at: the heel in 1.1; shots12: the drawings
    of 1.2's gang war. With the defaults it is motion_mix15."""
    leads = leads or {}
    shots12 = shots12 or ((12, 0), (14, 2), (16, 1), (17, 3), (19, 0), (21, 2), (22, 1))
    n = int((total + 0.4) * SR)
    music = np.zeros(n + SR)
    oj.groove(music, 0.40, total, level=0.85)
    music = music[:n]
    rain = so.rain(total + 0.4)[:n]
    voice = np.zeros(n)
    fx = np.zeros(n)
    at = {s: t0 for s, t0, d in rows}
    spans = []
    for shot, key in {"1.1": "n1", "2.1": "n2", "2.6": "n3", "5.3": "s1", "5.4": "n4", "6.1": "n5", "7.2a": "m1", "7.2b": "c1", "8.1": "m2", "8.5": "p1",
                     "1.2": "n6", "3.2": "n7", "4.1a": "n8", "5.2": "n9", "5.6": "n10", "6.4": "n11", **(swap or {})}.items():
        a, _ = sf.read("%s/%s_%s.wav" % (TAKES, key, kind) if key[0] == "n" else "%s/%s.wav" % (TAKES, key))
        ld = leads.get(shot, 0.25)
        p = int((at[shot] + ld) * SR); voice[p:p + len(a)] += a[:n - p]
        spans.append((shot, key, at[shot] + ld, at[shot] + ld + len(a) / SR))
    h, th = heel(), thud()

    def put(t, a, g=1.0):
        p = int(t * SR)
        if 0 <= p < n:
            fx[p:p + len(a)] += a[:n - p] * g
    if heel_at is not None:
        put(at["1.1"] + heel_at, h, 1.0)                                # the heel on the stones
    rg = np.random.default_rng(31)
    for dr, who in shots12:      # 1.2: far off, through the rain
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.0015 * SR); dull = np.convolve(crack, np.ones(k_) / k_, mode="same")       # v23: brighter, and louder
        put(at["1.2"] + dr / 12.0 + 0.03, dull, 0.60 if who < 2 else 0.48)
        put(at["1.2"] + dr / 12.0 + 0.12, dull, 0.20 if who < 2 else 0.16)                  # the slap off the walls
    for dr in (1, 4, 7):                                                  # 1.2b: and while we are close on her
        tt_ = so.tt(0.30)
        crack = rg.standard_normal(len(tt_)) * np.exp(-tt_ / 0.012) + np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ / 0.08) * 0.8
        k_ = int(0.0015 * SR); a_ = np.convolve(crack, np.ones(k_) / k_, mode="same")
        put(at["1.2b"] + dr / 12.0 + 0.03, a_, 0.50); put(at["1.2b"] + dr / 12.0 + 0.12, a_, 0.16)
    for i in range(6):                                                    # walking away, 2.1
        put(at["2.1"] + 0.15 + i * 0.42, h, 0.6 - i * 0.05)
    put(at["2.5"] + 3 / 12.0, so.metal_click(2400, 0.08), 0.9)            # the compact
    put(at["2.5"] + 3 / 12.0 + 0.07, so.metal_click(3100, 0.05), 0.5)
    for i in range(10):                                                   # running, 2.6: a contact every half cycle
        put(at["2.6"] + i / 3.0, h, 0.75 - i * 0.05)
    for i, g in enumerate((0.35, 0.7, 0.9, 0.6, 0.3)):                    # 3.1: she runs past, close
        put(at["3.1"] + 0.17 + i / 4.0, h, g)
    for i in range(6):                                                    # 3.2: he is coming, far off
        put(at["3.2"] + i * 5 / 12.0, th, 0.30 + i * 0.05)
    put(at["3.2"] + 10 / 12.0, so.swish(0.18), 0.3)                       # the broom lifted
    put(at["3.2"] + 12.5 / 12.0, so.swish(0.34), 0.9)                     # one sweep
    put(at["3.3"] + 0.45, so.swish(0.22), 0.35)
    for i in range(2):                                                    # 3.4: he walks off the wrong way
        put(at["3.4"] + 10 / 12.0 + i * 5 / 12.0, th, 0.85 - i * 0.12)
    for i in range(2):                                                    # 4.1: she walks up
        put(at["4.1a"] + 0.02 + i * 0.3, h, 0.5)
    put(at["4.1a"] + 10 / 12.0, so.metal_click(2600, 0.10), 1.0)          # the coin in the tin cup
    put(at["4.1a"] + 10 / 12.0 + 0.06, so.metal_click(3900, 0.07), 0.6)
    put(at["4.1a"] + 13 / 12.0, so.chirp(), 4.0)                          # the robot has noticed
    put(at["4.1b"] + 0.02, h, 0.5)                                        # two steps
    put(at["4.1b"] + 3 / 12.0, h, 0.5)
    put(at["4.1b"] + 6 / 12.0, so.swish(0.16), 0.9)                       # its arm, out
    put(at["4.1b"] + 7 / 12.0, so.metal_click(1500, 0.06), 0.8)
    put(at["4.1b"] + 9 / 12.0, so.chirp(), 4.0)
    put(at["4.2"] + 9 / 12.0, so.metal_click(2600, 0.06), 0.7)            # she takes it back
    put(at["4.2"] + 10 / 12.0, so.swish(0.14), 0.7)
    for i in range(3):
        put(at["4.2"] + 1.0 + i * 0.2, h, 0.55 - i * 0.12)
    b0 = at["5.1"]                                                        # beat 05: the bar

    def at5(shot, drawing):
        return at[shot] + drawing / 12.0
    for i in range(5):                                                    # 5.1: her heels on the boards
        put(b0 + i * 0.5, h, 0.42)
    for dr, a_ in ((2, so.swish(0.12)), (6, so.metal_click(4200, 0.05)), (11, so.metal_click(4600, 0.05)), (15, so.swish(0.12))):
        put(at5("5.1", dr), a_, 0.35)
    for dr in (2, 7, 22, 27):                                             # 5.2: his steps, in and out
        put(at5("5.2", dr), th, 0.55)
    put(at5("5.2", 6), so.swish(0.16), 0.5); put(at5("5.2", 28), so.swish(0.16), 0.4)
    put(at5("5.3", 20), so.metal_click(3600, 0.06), 0.5)                  # 5.3: a coupe set down, and filled
    for dr in (2, 6, 10, 14):                                             # the cloth on the glass
        put(at5("5.3", dr), so.swish(0.10), 0.14)
    put(at5("5.3", 22), so.swish(0.40), 0.25)
    put(at5("5.4", 0), so.swish(0.50), 0.5)                               # 5.4: the note along the bar; one tap
    put(at5("5.4", 11), th, 0.3)
    for dr in (0, 2, 4, 6, 8, 12, 15):                                    # 5.5: her finger on the bays
        put(at5("5.5", dr), so.metal_click(900, 0.03), 0.3)
    put(at5("5.6", 2), so.swish(0.20), 0.4)                               # 5.6: over; the lipstick
    for dr in (7, 10, 13, 17, 21):
        put(at5("5.6", dr), so.swish(0.28), 0.28)
    put(at5("5.7", 0), so.swish(0.40), 0.4)                               # 5.7: across the bar; her fingers, once
    for dr in (8, 9):
        put(at5("5.7", dr), so.metal_click(900, 0.03), 0.3)
    for dr in (6, 10, 14):                                                # 5.10: the door, still swinging
        put(at5("5.10", dr), so.swish(0.22), 0.22)
    put(at5("5.9", 11), so.sting(110.0, 1.6), 0.6)                        # 5.9: his eye
    put(at5("5.10", 8), th, 1.4); put(at5("5.10", 8), so.metal_click(700, 0.05), 0.5)   # 5.10: CASE CLOSED
    put(at5("5.10", 18), so.metal_click(3600, 0.06), 0.45)
    for dr in (0, 2):                                                     # 6.1: in, running; the door, shut with her back
        put(at5("6.1", dr), h, 0.5)
    put(at5("6.1", 4), th, 1.6); put(at5("6.1", 4), so.metal_click(500, 0.06), 0.5)
    put(at5("6.2", 3), so.swish(0.45), 0.5); put(at5("6.2c", 6), so.swish(0.35), 0.35)   # 6.2: the drawer, pulled; the roll
    put(at5("6.2", 9), th, 0.35)                                          # it stops against its runners
    for dr in (30, 33):
        put(at5("6.2c", dr - 12), so.metal_click(900, 0.03), 0.3)
    put(at5("6.4", 3), th, 0.25); put(at5("6.4", 8), so.swish(0.50), 0.35)               # 6.4: the roll laid down; the door
    put(at5("6.6", 6), so.swish(0.30), 0.3)                               # 6.6: his hand
    for dr in (1, 2, 4, 5, 7, 8, 10):                                     # 6.7: keys
        put(at5("6.7a", dr), so.metal_click(5200 + 300 * (dr % 3), 0.04), 0.35)
    put(at5("6.7", 2), so.swish(0.20), 0.6); put(at5("6.7", 4), th, 0.5)
    put(at5("7.1c", 0), th, 0.6); put(at5("7.1c", 4), th, 0.6)          # 7.1: his shoes
    put(at5("6.2r", 4), so.sting(220.0, 0.6), 0.25)                       # v21: the drawer: her little win
    for dr in (5, 7, 9):                                                  # 7.2: her slippers
        put(at5("7.2a", dr), th, 0.3)
    tpop = at5("7.3", 2)
    put(tpop, so.pop(), 1.6)                                              # 7.3: one pop
    put(at5("8.1", 12), so.metal_click(1200, 0.03), 0.2)                  # 8.1: the paper hat lands
    put(at5("8.2", 8), th, 0.5)                                           # 8.2: she jerks upright
    tb = so.tt(0.55)                                                      # 8.3: the blower toots
    ph = 2 * np.pi * np.cumsum(420 + 110 * tb) / SR
    toot = (np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5) * np.minimum(1, tb / 0.02) * np.minimum(1, (0.55 - tb) / 0.08) * 0.12
    put(at5("8.3", 7), toot, 1.0)
    for dr in (2, 12):                                                    # 8.5: the broom
        put(at5("8.5", dr), so.swish(0.40), 0.5)
    put(at5("8.5", 17), so.metal_click(700, 0.05), 0.35); put(at5("8.5", 17), so.swish(0.30), 0.3)   # v21: into the pan; the puff
    tw = so.tt(0.75)                                                      # v21, 8.6: the blower again, and it gives up
    ph = 2 * np.pi * np.cumsum(330 - 120 * tw / 0.75 + 14 * np.sin(2 * np.pi * 7 * tw)) / SR
    fiz = (np.sin(ph) + np.sin(3 * ph) / 3) * np.minimum(1, tw / 0.03) * np.clip((0.75 - tw) / 0.35, 0, 1) * 0.08
    put(at5("8.6", 14), fiz, 1.0)
    tend = at["8.7"]                                                      # v22: into the window
    tb_ = so.tt(0.95)                                                      # the taxi's brakes, ending on the seam
    sq = np.sin(2 * np.pi * np.cumsum(2300 - 500 * tb_ / 0.95 + 40 * np.sin(2 * np.pi * 9 * tb_)) / SR)
    hiss = np.random.default_rng(77).standard_normal(len(tb_))
    env_ = np.minimum(1, tb_ / 0.15) * np.clip((0.95 - tb_) / 0.12, 0, 1)
    put(total - 0.95, (sq * 0.05 + so.hp(hiss, 3) * 0.06) * env_, 1.0)
    tsec = np.arange(n) / SR
    inside = np.clip((tsec - b0) / 0.6, 0.0, 1.0)                         # the door closes behind her
    back = np.clip((tsec - tend) / (total - tend), 0.0, 1.0) / 0.9         # v22: the rain comes back to where the film starts
    rain = rain * np.maximum(np.where(tsec >= tpop, 0.0, 1.0 - 0.84 * inside), 0.9 * back)
    music = music * (1.0 + 0.30 * inside) * np.clip((tpop - tsec) / 0.02, 0.0, 1.0)     # the jazz stops dead on the pop
    beat = 60.0 / 104.0                                                   # Auld Lang Syne, vibes, from the cut to colour
    tune = [(60, 1), (65, 1.5), (65, .5), (65, 1), (69, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (65, .5), (69, 1), (72, 1),
            (74, 3), (74, 1), (72, 1.5), (69, .5), (69, 1), (65, 1), (67, 1.5), (65, .5), (67, 1), (69, 1), (65, 1.5), (62, .5), (62, 1),
            (60, 1), (65, 3)]
    als = np.zeros(n)
    t0 = at["8.1"]
    for mi, bt in tune:
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 1.6) * 2.4
        p = int(t0 * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
        t0 += bt * beat
    for i, mi in enumerate((53, 48, 53, 58, 53, 48, 58, 53)):             # a root under each bar
        v = oj.vibe(440.0 * 2 ** ((mi - 69) / 12.0), 2.2) * 1.6
        p = int((at["8.1"] + (1 + 4 * i) * beat) * SR)
        if p < n:
            als[p:p + len(v)] += v[:n - p]
    als *= np.clip((total - 0.15 - tsec) / (total - 0.15 - tend), 0.0, 1.0)
    if raven:                                                             # v29: the raven at 0:00 (on2_raven), opt-in
        put(0.0, caw(), 1.0)                                              # one caw
        t_ = so.tt(0.26)                                                  # its wings, coming at us faster
        sw = so.si.lp(np.random.default_rng(8).standard_normal(len(t_)), 20) * (t_ / 0.26) ** 2 * 0.9
        put(0.06, sw, 1.4)
        put(0.20, so.thump(), 1.2)                                        # the wing on the lens: low, full (v42: before "New", a little lower)
        put(0.25, so.swish(0.22), 1.0)
        put(total - 0.20, so.swish(0.16), 0.5)                            # on the lamp it opens its wings: the seam
        quiet = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((0.95 - tsec) / 0.05, 0, 1)
        quiet_m = 1.0 - 0.85 * np.clip((tsec - 0.33) / 0.02, 0, 1) * np.clip((1.55 - tsec) / 0.30, 0, 1)   # v42: the music back after "Eve", not under it
        music = music * quiet_m; rain = rain * quiet; fx[int(0.36 * SR):int(0.95 * SR)] *= 0.15     # then nothing until the first shot
    env = np.zeros(n)                                                     # duck the music under her voice
    for _, _, t0, t1 in spans:
        env[int((t0 - 0.25) * SR):int((t1 + 0.20) * SR)] = 1.0
    k = int(0.12 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    mix = voice * 1.0 + music * (0.26 - 0.15 * env) + als * (1.0 - 0.45 * env) + rain * 0.55 + fx * 0.5
    mix = np.tanh(mix * 2.0) / 2.0 * 1.5
    sf.write(out, mix.astype(np.float32), SR)
    return out, spans

if __name__ == "__main__":
    if len(sys.argv) > 1:
        take_kind(sys.argv[1])
    else:
        takes()
        o, t = audition()
        print("wrote", o, "%.1f s" % t)
