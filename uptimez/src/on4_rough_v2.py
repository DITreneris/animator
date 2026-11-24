"""OFFICE NOIR 4: the moving rough, v2 (24 Nov; v1 pinned as on4_rough_v1.py). Tomas's picks: 3.3-3.5 in the side camera
(on4_motion T6), 2 s moved from the stage to the office (on4_scenes DUR), every line voiced (seven new takes with the
series' voices, checked by the recognizer), effects, and the Office Noir band (sound_on_jazz.groove) cut by the story's
silences (lesson 107): dead on the bump, dead on "Well?"; no music awake. Voices dry. No bubbles yet.

  python3 on4_motion.py && python3 on4_rough.py  ->  ../office-noir-4/on4_rough_v2.mp4 (540x960, 24 fps, AAC, -15 LUFS)"""
import json
import os
import shutil
import subprocess
import numpy as np
import soundfile as sf
import on4_scenes as sc
import on4_voices as vo

FPS = 12
SR = 48000
MOT = {("1.1", "1.2"): ("T1", 0, 31), ("2.2", "2.3"): ("T2", 0, None), ("3.1", "3.2"): ("T3", 0, None),
       ("3.3", "3.3b", "3.4", "3.5"): ("T6", 0, None), ("6.3", "6.6"): ("T4", 0, -8), ("8.1", "8.2"): ("T5", 0, -7)}
OUT = os.path.join(sc.OUT, "on4_rough_v2.mp4")
NEW = {   # key: (shot, seconds into the shot, who, text)
    "c1": ("2.2", 1.3, "CLIENT", "Mine until it's done."),
    "d1": ("3.1", 1.5, "DON", "Traffic flows."),
    "d2": ("3.3", 1.9, "DON", "Not a scratch."),
    "f1": ("3.4", 1.0, "FATHER", "For the boys."),
    "p1": ("4.1", 0.9, "PAM", "There you are."),
    "p2": ("5.3", 2.6, "PAM", "Easy."),
    "p3": ("6.3", 0.9, "PAM", "Well?"),
}


def new_takes():
    """the seven lines, cached in on4_voices/takes_v2 with what the recognizer heard"""
    import sound_on as so
    import sound_fs as sfs
    import dh_voices as dv
    d = os.path.join(vo.OUT, "takes_v2"); os.makedirs(d, exist_ok=True)
    logp = os.path.join(d, "takes.json")
    log = json.load(open(logp)) if os.path.exists(logp) else {}
    for key, (shot, lead, who, txt) in NEW.items():
        p = os.path.join(d, key + ".wav")
        if os.path.exists(p) and key in log:
            continue
        if who == "DON":
            a = so.dry(txt, "am_onyx", 1.0)
        elif who == "CLIENT":
            a = so.pitch(so.dry(txt, "am_fenrir", 1.0), -4.0)
        elif who == "FATHER":
            v = dv.FATHER[dv.FATHER_VOICE][0]       # Father voice B, but 0.8 speed and -1.5 semitones: at -3 a three-word line is not recognized
            a = so.pitch(so.dry(txt.rstrip(".") + "...", so.blend(*v), 0.8), -1.5)
        else:
            a = so.dry(txt, vo.PAM_AWAKE[0], vo.PAM_AWAKE[2], vo.PAM_AWAKE[1])
        a = np.asarray(a, dtype=np.float64); a = a / (np.sqrt(np.mean(a ** 2)) + 1e-9) * 0.11
        h = vo.heard3(a); want = " ".join(sfs._words(txt))
        log[key] = dict(shot=shot, who=who, text=txt, asr=h, ok=sum(1 for x in h if sfs._match(x, want)), len=round(len(a) / vo.SR, 2))
        sf.write(p, a.astype(np.float32), vo.SR)
        print("take", key, log[key]["ok"], h[0])
    json.dump(log, open(logp, "w"), indent=1)
    return d, log


def load(p):
    a, sr = sf.read(p)
    if a.ndim > 1:
        a = a.mean(1)
    if sr != SR:
        a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    return a.astype(np.float64)


def sound(tm, d, total):
    import sound_on as so
    import sound_on_jazz as jz
    import sound_iwry as iw
    n = int((total + 0.2) * SR)
    def put(buf, a, t, g=1.0):
        a = np.asarray(a, dtype=np.float64); j = int(t * SR)
        if j >= len(buf):
            return
        a = a[:len(buf) - j]; buf[j:j + len(a)] += a * g
    def rs(a, sr):
        return a if sr == SR else np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    st_ = lambda s: tm[s]["start"]
    voice = np.zeros(n); fx = np.zeros(n); mus = np.zeros(n)
    marks = []
    for key, ln in d["lines"].items():
        t = st_(ln["shot"]) + vo.LEAD.get(ln["shot"], 0.3)
        put(voice, load(os.path.join(vo.OUT, "takes_v1", key + ".wav")), t); marks.append((key, round(t, 2)))
    d2, _ = new_takes()
    for key, (shot, lead, who, txt) in NEW.items():
        t = st_(shot) + lead
        put(voice, load(os.path.join(d2, key + ".wav")), t); marks.append((key, round(t, 2)))
    span31 = tm["3.1"]["dur"] + tm["3.2"]["dur"]
    bump = st_("3.1") + span31 * 21.0 / 32.0                 # T3's hit drawing
    toot = st_("3.1") + span31 * 12.0 / 32.0
    put(fx, rs(so.swish(0.3), so.SR), 0.72, 0.9); put(fx, rs(so.thump(), so.SR), 0.85, 1.6)       # the punch
    put(fx, rs(so.swish(0.9), so.SR), 1.0, 0.5)                                                     # the shadow runs down the wall
    t_ = np.arange(int(0.5 * SR)) / SR                                                             # the whistle's toot
    put(fx, np.sin(2 * np.pi * (2300 + 60 * np.sin(2 * np.pi * 38 * t_)) * t_) * np.minimum(t_ / 0.02, 1) * np.exp(-np.maximum(t_ - 0.35, 0) / 0.05) * 0.12, toot)
    put(fx, rs(so.hiss(0.5), so.SR), bump - 0.45, 0.5)                                              # the tyres
    put(fx, rs(so.thump(), so.SR), bump, 2.0)
    put(fx, rs(so.swish(0.6), so.SR), st_("3.4") + 0.9, 0.35)                                       # the bills
    put(fx, rs(iw.clink(), getattr(iw, "SR", SR)), st_("7.2") + 2.4, 0.8)                           # her mug set down
    r0 = st_("8.2") - 0.8
    rain = rs(so.rain(total - r0 + 0.1), so.SR); rain[:int(0.8 * SR)] *= np.linspace(0, 1, int(0.8 * SR))
    put(fx, rain, r0, 1.2)
    put(fx, rs(so.rain(1.2), so.SR) * np.linspace(1, 0, len(rs(so.rain(1.2), so.SR))), 0.0, 1.2)    # the rain runs through the loop's seam
    # the band: in the dream only; dead on the bump (back when she sits up), dead on "Well?"; nothing awake
    for t0, t1 in ((0.3, bump), (st_("3.6") + 0.4, st_("6.3") + 0.9)):
        jz.groove(mus, t0, t1, level=0.8)
        j = int(t1 * SR); mus[j:] = 0.0                                                             # cut dead
    mus_end = int((st_("6.3") + 0.9) * SR); mus[mus_end:] = 0.0
    mix = voice * 1.0 + fx * 0.7 + mus * 0.22
    return mix[:int(total * SR)], marks, dict(bump=round(bump, 2), toot=round(toot, 2))


def main():
    tm, d = sc._timing()
    shots = [x for _, ss in sc.SCENES for x in ss]
    ids = [x["id"] for x in shots]
    tmp = "/tmp/on4_rough"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    n = 0
    def put(path, count):
        nonlocal n
        for _ in range(count):
            os.symlink(path, "%s/%05d.png" % (tmp, n)); n += 1
    i = 0
    while i < len(ids):
        grp = next((g for g in MOT if g[0] == ids[i]), None)
        span = grp if grp else (ids[i],)
        end = tm[span[-1]]["start"] + tm[span[-1]]["dur"]
        count = int(round(end * FPS)) - n
        if grp:
            t, a, b = MOT[grp]
            files = sorted(os.listdir("/tmp/on4_mot/" + t))[a:b]
            if len(files) >= count:
                pick = files[:count]
            else:
                pick = [files[min(len(files) - 1, int(j * len(files) / count))] for j in range(count)]
            for f in pick:
                put("/tmp/on4_mot/%s/%s" % (t, f), 1)
        else:
            s, _ = sc.render(shots[i], 1)
            p = "%s/key_%s.png" % (tmp, ids[i]); s.write_to_png(p); put(p, count)
        i += len(span)
    total = n / FPS
    mix, marks, ev = sound(tm, d, total)
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.5
    sf.write(tmp + "/a0.wav", mix.astype(np.float32), SR)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp + "/a0.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    I = float([l for l in r.stderr.splitlines() if "I:" in l][-1].split("I:")[1].split("LUFS")[0])
    g = 10 ** ((-15.0 - I) / 20.0)
    for _ in range(4):                                                                              # a soft ceiling at 0.7, then measured again
        out = np.tanh(mix * g / 0.7) * 0.7
        sf.write(tmp + "/a.wav", out.astype(np.float32), SR)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp + "/a.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
        I2 = float([l for l in r.stderr.splitlines() if "I:" in l][-1].split("I:")[1].split("LUFS")[0])
        if abs(I2 + 15.0) < 0.3:
            break
        g *= 10 ** ((-15.0 - I2) / 20.0)
    print("lines", marks, ev, "gain %.1f dB" % (20 * np.log10(g)))
    t_ = OUT[:-4] + "_tmp.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", tmp + "/%05d.png", "-i", tmp + "/a.wav",
                        "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                        "-c:a", "aac", "-b:a", "128k", "-t", "%.3f" % total, t_])
    if r.returncode == 0:
        os.replace(t_, OUT)
    print(OUT, n, "drawings", round(total, 2), "s")


if __name__ == "__main__":
    main()
