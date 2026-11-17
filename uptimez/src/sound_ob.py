"""Voices for "The Onboarding": the Client's auditions (the rest of the cast keep their series voices: Don am_onyx,
Sofia af_bella, Pam bf_emma, the robot voice B).
The Client is a solid, warm man in his fifties who owns ten garages. His three lines are short and all of them are
said next to Don, so the voice is chosen by measurement first (docs/lessons.md: "Pick takes by measurement first ...
then ask the person to confirm by ear"):
  - the pitch gap to Don (am_onyx, about 92 Hz) and to the robot (about 120 Hz, but robotized);
  - the pace: unhurried, slower than Don, not as slow as Pam's deadpan;
  - the body: warmth (200-1000 Hz) against presence (2-6 kHz); a big chest is the lower formants of a take that was
    spoken a little fast and then lowered (the lowering slows it back down).
  python3 sound_ob.py measure    -> ob_voices/audition/*.wav and a table (raw takes are cached, so pitch can be retuned)
  python3 sound_ob.py audition   -> ../the-onboarding/ob_client_voices_v1.mp4: three finalists, each with his three
                                    lines and then two exchanges in context (with Pam, with Don)
CHOSEN (17 Nov, by ear, from ob_client_voices_v1.mp4): voice B = "fenrir": am_fenrir at speed 1.0, then four semitones
down: gruff, a big chest, about 124 Hz against Don's 94. client_line(txt) is that voice for any line.
  python3 sound_ob.py new        -> measures the three lines added in concept v5 (beat 03)
Needs the Kokoro model (KOKORO_DIR), like every sound module of the series."""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import sound_iwry as si
import sound_xmas as sx
import sound_on as so
import sound_bc as bc

SR = 48000
OUT = "ob_voices/audition"
LINES = [("hi", "Hi. I'd like to sign up."), ("ten", "Ten garages. And I keep losing this."),
         ("mine", "Mine takes a minute.")]
# key -> (voice or (voice, voice, share of the second), speed of the take, semitones afterwards, note)
CANDS = {
    "liam": ("am_liam", 1.00, -2.0, "even and warm"),
    "liam_low": ("am_liam", 1.06, -3.5, "the same man, lower and broader"),
    "fenrir": ("am_fenrir", 1.00, -4.0, "gruff, a big chest"),
    "adam": ("am_adam", 1.00, -2.0, "dry and direct"),
    "liam_george": (("am_liam", "bm_george", 0.40), 1.00, -2.0, "older grain, still American"),
    "fenrir_michael": (("am_fenrir", "am_michael", 0.50), 1.05, -3.0, "gruff, softened"),
}
CLIENT = "fenrir"                                         # voice B of the audition


def raw(key, tag, txt):
    """The untreated take, cached: retuning the pitch must not need the model again."""
    os.makedirs(OUT, exist_ok=True)
    p = "%s/raw_%s_%s.wav" % (OUT, key, tag)
    if os.path.exists(p):
        return sf.read(p)[0]
    v, sp, _, _ = CANDS[key]
    voice = so.blend(v[0], v[1], v[2]) if isinstance(v, tuple) else v
    a = so.dry(txt, voice, sp)
    sf.write(p, a, SR)
    return a


def warm(a):
    return a * 0.82 + si.lp(a, 5) * 0.18


def client(key, tag, txt, semis=None):
    s = CANDS[key][2] if semis is None else semis
    return bc.norm(warm(so.pitch(raw(key, tag, txt), s)))


def client_line(txt):
    """Any line in the chosen voice (not cached: the film's takes are made by its own sound stage)."""
    v, sp, semis, _ = CANDS[CLIENT]
    return bc.norm(warm(so.pitch(so.dry(txt, v, sp), semis)))


def slope(a):
    """Pitch at the start and at the end of a take (Hz): falling is settled or interested, rising is a question."""
    n = int(0.04 * SR); f = []
    for i in range(0, len(a) - n, n // 2):
        x = a[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(x ** 2)) < 0.02:
            continue
        r = np.correlate(x, x, "full")[n - 1:]
        lo, hi = int(SR / 420), int(SR / 70)
        j = lo + int(np.argmax(r[lo:hi]))
        if r[j] > 0.35 * r[0]:
            f.append(SR / float(j))
    if len(f) < 4:
        return 0.0, 0.0
    k = max(1, len(f) // 3)
    return float(np.median(f[:k])), float(np.median(f[-k:]))


def new_lines():
    rows = [("CLIENT", "I live alone.", client_line("I live alone."))]
    rows.append(("SOFIA", "Does your missus love your garages?", bc.sofia("Does your missus love your garages?")))
    for txt, sp in (("Oh...", 1.0), ("Oh...", 0.8), ("Ohh.", 0.8), ("Oooh.", 0.85)):
        rows.append(("SOFIA", "%s (x%.2f)" % (txt, sp), bc.sofia(txt, sp)))
    for who, txt, a in rows:
        a0, a1 = slope(a)
        print("%-7s %-40s %.2f s  f0 %3.0f Hz  start %3.0f -> end %3.0f Hz" % (who, txt, span(a), bc.f0(a), a0, a1), flush=True)
    print("phonemes:", si.K.tokenizer.phonemize("Does your missus love your garages? I live alone.", "en-us"))


def bands(a):
    S = np.abs(np.fft.rfft(a * np.hanning(len(a)))); f = np.fft.rfftfreq(len(a), 1.0 / SR)
    lo = (f > 200) & (f < 1000); hi = (f > 2000) & (f < 6000)
    return 20 * np.log10(np.sqrt((S[hi] ** 2).mean()) / np.sqrt((S[lo] ** 2).mean()))


def span(a):
    i = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]
    return (i[-1] - i[0]) / float(SR)


def measure():
    don = [bc.don(t) for t in ("Don. CEO.", "Zero results. In 0.2 seconds.")]
    fd = float(np.median([bc.f0(a) for a in don]))
    rows = {}
    for key, (v, sp, semis, note) in CANDS.items():
        takes = [client(key, tag, txt) for tag, txt in LINES]
        f = float(np.median([bc.f0(a) for a in takes]))
        rows[key] = dict(f0=round(f, 1), st_vs_don=round(12 * np.log2(f / fd), 1), seconds=round(sum(span(a) for a in takes), 2),
                         presence_db=round(float(np.mean([bands(a) for a in takes])), 1),
                         click=round(max(float(np.abs(np.diff(a)).max()) for a in takes), 3), note=note)
        print("%-15s f0 %5.1f Hz  %+4.1f st vs Don  3 lines %.2f s  presence %+5.1f dB  max jump %.3f  %s" % (
            key, f, rows[key]["st_vs_don"], rows[key]["seconds"], rows[key]["presence_db"], rows[key]["click"], note), flush=True)
    rows["_don_f0"] = round(fd, 1)
    json.dump(rows, open(OUT + "/measure.json", "w"), indent=1)
    return rows


def audition(picks, out="../the-onboarding/ob_client_voices_v1.mp4"):
    """picks: [(letter, key, semitones or None)]. One card per voice; the pictures are stills, the sound is the test."""
    import cairo
    import kit
    import client_ob as co
    from kit import Ctx
    Wd, Hd, FPS = 540, 540, 10
    rows = json.load(open(OUT + "/measure.json"))
    pam = bc.norm(sx.pam_line("On purpose?", "A"))
    don = bc.don("Zero results. In 0.2 seconds.")
    gap = lambda s: np.zeros(int(s * SR))
    parts = []
    for n, (letter, key, semis) in enumerate(picks):
        t = {tag: client(key, tag, txt, semis) for tag, txt in LINES}
        f = float(np.median([bc.f0(a) for a in t.values()]))
        a = np.concatenate([gap(0.5), t["hi"], gap(0.45), t["ten"], gap(0.45), t["mine"], gap(0.9),
                            t["hi"], gap(0.30), pam, gap(0.8), don, gap(0.55), t["mine"], gap(0.9)])
        nfr = int(np.ceil(len(a) / float(SR) * FPS)); a = np.concatenate([a, np.zeros(nfr * SR // FPS - len(a))])
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd)
        c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
        co.client(Ctx(c, 0), 150, 300 - co.HY * 1.5, 1.5, "open", "confident", look=(0.6, 0.0))
        c.set_source_rgb(0.12, 0.16, 0.27); c.select_font_face("Inter", 0, 1)
        v = CANDS[key][0]
        name = v if isinstance(v, str) else "%s + %d%% %s" % (v[0], round(v[2] * 100), v[1])
        s = CANDS[key][2] if semis is None else semis
        for txt, size, y, bold in (("VOICE " + letter, 46, 86, 1), (name, 19, 122, 0), ("%+.1f semitones" % s, 15, 146, 0),
                                   ("%d Hz  ·  Don %d Hz" % (round(f), round(rows["_don_f0"])), 15, 168, 0),
                                   (CANDS[key][3], 15, 190, 0), ("his three lines,", 14, 250, 0),
                                   ("then with Pam, then with Don", 14, 270, 0)):
            c.select_font_face("Inter", 0, bold); c.set_font_size(size)
            e = c.text_extents(txt); c.move_to(400 - e.x_advance / 2, y); c.show_text(txt)
        png = "/tmp/ob_aud_%s.png" % letter; wav = "/tmp/ob_aud_%s.wav" % letter; tmp = "/tmp/ob_aud_%s.tmp.mp4" % letter
        surf.write_to_png(png); sf.write(wav, a, SR)
        d = len(a) / float(SR)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % d, "-af", "loudnorm=I=-16:TP=-2,aresample=48000",
                               "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                               "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % d, tmp])
        os.rename(tmp, "/tmp/ob_aud_%s.mp4" % letter)
        parts.append("/tmp/ob_aud_%s.mp4" % letter)
        sf.write("%s/final_%s.wav" % (OUT, letter), a, SR)
        print("voice", letter, key, "%+.1f st" % s, round(f), "Hz", round(d, 1), "s", flush=True)
    open("/tmp/ob_aud.txt", "w").write("".join("file '%s'\n" % p for p in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/ob_aud.txt", "-c", "copy",
                           out + ".tmp.mp4"])
    os.rename(out + ".tmp.mp4", out)
    print("wrote", out)


if __name__ == "__main__":
    if sys.argv[1] == "measure":
        measure()
    elif sys.argv[1] == "new":
        new_lines()
    elif sys.argv[1] == "audition":
        audition([(a.split(":")[0], a.split(":")[1], float(a.split(":")[2]) if a.count(":") > 1 else None) for a in sys.argv[2:]])


# ---------------------------------------------------------------- Sofia's "Oh..." (17 Nov): three built takes
OH = {   # letter -> (text, speed of the take, semitones lower overall, semitones it falls across the take, note)
    "A": ("Ohh.", 0.70, 0.0, 3.0, "light: a short fall"),
    "B": ("Ohhh.", 0.60, 1.0, 5.0, "lower, a longer fall"),
    "C": ("Ohhh.", 0.55, 2.0, 7.0, "lowest and longest: it settles"),
}


def fall(a, semis):
    """Read the take at a rate that slows from 1 to 2^(-semis/12): the pitch slides down and the sound draws out."""
    n = len(a)
    rate = np.linspace(1.0, 2 ** (-semis / 12.0), int(n * 1.6))
    pos = np.cumsum(rate); pos = pos[pos < n - 1]
    return np.interp(pos, np.arange(n), a)


def oh_take(letter):
    txt, sp, low, drop, _ = OH[letter]
    a = bc.sofia(txt, sp)
    a = fall(so.pitch(a, -low) if low else a, drop)
    f = int(0.06 * SR); a[-f:] *= np.linspace(1, 0, f)
    return bc.norm(a)


def audition_oh(out="../the-onboarding/ob_sofia_oh_v1.mp4"):
    """Each take alone, twice, then in the exchange: her question, his answer, "Oh..."."""
    import cairo
    import kit
    import sofia_ob as sob
    from kit import Ctx
    Wd, Hd, FPS = 540, 540, 10
    q = bc.sofia("Does your missus love your garages?")
    ans = client_line("I live alone.")
    gap = lambda s: np.zeros(int(s * SR))
    parts = []
    for letter in "ABC":
        t = oh_take(letter)
        a0, a1 = slope(t)
        a = np.concatenate([gap(0.5), t, gap(0.7), t, gap(1.0), q, gap(0.35), ans, gap(0.75), t, gap(1.0)])
        nfr = int(np.ceil(len(a) / float(SR) * FPS)); a = np.concatenate([a, np.zeros(nfr * SR // FPS - len(a))])
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, Wd, Hd)
        c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
        sob.sofia(Ctx(c, 0), 150, 250 - sob.HY * 1.5, 1.5, "pearl", "oh", look=(-0.9, -0.2))
        c.set_source_rgb(0.12, 0.16, 0.27)
        for txt, size, y, bold in (("\"OH...\"  " + letter, 40, 86, 1), ("%.2f s" % span(t), 19, 122, 0),
                                   ("%d Hz falling to %d Hz" % (round(a0), round(a1)), 15, 146, 0), (OH[letter][4], 15, 168, 0),
                                   ("twice alone,", 14, 230, 0), ("then after his answer", 14, 250, 0)):
            c.select_font_face("Inter", 0, bold); c.set_font_size(size)
            e = c.text_extents(txt); c.move_to(400 - e.x_advance / 2, y); c.show_text(txt)
        png = "/tmp/ob_oh_%s.png" % letter; wav = "/tmp/ob_oh_%s.wav" % letter; tmp = "/tmp/ob_oh_%s.tmp.mp4" % letter
        surf.write_to_png(png); sf.write(wav, a, SR)
        d = len(a) / float(SR)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", png, "-i", wav, "-vf",
                               "format=yuv420p,loop=-1:1,trim=duration=%.3f" % d, "-af", "loudnorm=I=-16:TP=-2,aresample=48000",
                               "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                               "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % d, tmp])
        os.rename(tmp, "/tmp/ob_oh_%s.mp4" % letter)
        parts.append("/tmp/ob_oh_%s.mp4" % letter)
        os.makedirs("ob_voices/oh", exist_ok=True); sf.write("ob_voices/oh/oh_%s.wav" % letter, t, SR)
        print("Oh", letter, "%.2f s" % span(t), "%d -> %d Hz" % (round(a0), round(a1)),
              "max jump %.3f" % float(np.abs(np.diff(t)).max()), flush=True)
    open("/tmp/ob_oh.txt", "w").write("".join("file '%s'\n" % p for p in parts))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/ob_oh.txt", "-c", "copy",
                           out + ".tmp.mp4"])
    os.rename(out + ".tmp.mp4", out)
    print("wrote", out)


# ---------------------------------------------------------------- the film's 20 lines (script v5), measured
OH_PICK = "A"                                             # chosen by ear on 17 Nov from ob_sofia_oh_v1.mp4 (B was the stand-in)
FILM = [  # shot, who, the caption (identical to the line), what the voice is given
    ("1.3", "CLIENT", "Hi. I'd like to sign up.", None),
    ("2.1", "DON", "Don. CEO.", None),
    ("2.2", "ROBOT", "CONTACT NOT VERIFIED.", "Contact not verified."),
    ("2.3", "DON", "Founder. And CEO.", None),
    ("3.1", "CLIENT", "Ten garages. And I keep losing this.", None),
    ("3.2", "SOFIA", "Does your missus love your garages?", None),
    ("3.3", "CLIENT", "I live alone.", None),
    ("3.7", "SOFIA", "Oh...", "oh"),
    ("3.12", "CLIENT", "Can it find this when I lose it?", None),
    ("4.1", "DON", "Here, you will never lose anything again.", None),
    ("4.3", "DON", "We'll take care of it.", None),
    ("5.4", "CLIENT", "One month. I ask, you find it.", None),
    ("5.5", "DON", "Approved.", None),
    ("6.2", "SOFIA", "Tap here.", None),
    ("6.5", "CLIENT", "That worked.", None),
    ("6.8", "SOFIA", "Everything you need is in there.", None),
    ("7.3", "ROBOT", "CONTACT APPROVED.", "Contact approved."),
    ("8.1", "ROBOT", "FIRST CUSTOMER. CELEBRATION REQUIRED.", "First customer. Celebration required."),
    ("8.3", "DON", "SOFÍA! WE HAVE A CUSTOMER!", "Sophia! We have a customer!"),      # this spelling stresses the i
    ("10.4", "ROBOT", "ONBOARDING COMPLETE.", "Onboarding complete."),
]
FILM_OUT = "ob_voices/film"


def film_take(shot, who, cap, give):
    txt = give or cap
    if give == "oh":
        return oh_take(OH_PICK)
    if who == "CLIENT":
        return client_line(txt)
    if who == "SOFIA":
        return bc.sofia(txt)
    if who == "ROBOT":
        return bc.robot(txt)
    if shot == "8.3":
        return si.don_shout(bc.don(txt))                  # raised, not clipped (the lesson of "WHAT IS THIS?!")
    return bc.don(txt)


def trim(a):
    """Cut to the voiced span, with 20 ms of air either side, so a take's length is the line's length."""
    i = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]
    p = int(0.02 * SR)
    b = a[max(0, i[0] - p):i[-1] + p].copy()
    f = int(0.008 * SR); b[:f] *= np.linspace(0, 1, f); b[-f:] *= np.linspace(1, 0, f)
    return b


def film_takes(only=None):
    os.makedirs(FILM_OUT, exist_ok=True)
    p = FILM_OUT + "/takes.json"
    meta = json.load(open(p)) if os.path.exists(p) else {}
    for shot, who, cap, give in FILM:
        if only and shot not in only:
            continue
        a = trim(np.asarray(film_take(shot, who, cap, give), dtype=np.float64))
        sf.write("%s/%s.wav" % (FILM_OUT, shot), a.astype(np.float32), SR)
        a0, a1 = slope(a)
        meta[shot] = dict(who=who, text=cap, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))), start=round(a0), end=round(a1),
                          rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3),
                          jump=round(float(np.abs(np.diff(a)).max()), 3))
        m = meta[shot]
        print("%-5s %-6s %5.2f s  f0 %3d Hz (%3d -> %3d)  rms %.3f  peak %.2f  jump %.3f  %s" % (
            shot, who, m["len"], m["f0"], m["start"], m["end"], m["rms"], m["peak"], m["jump"], cap), flush=True)
    json.dump(meta, open(p, "w"), indent=1)
    print("spoken in all: %.2f s" % sum(m["len"] for m in meta.values()))
    return meta


def film_visemes():
    """Mouth shapes on the 12 fps drawing grid for every spoken take (bc.visemes: phonemes spread over the voiced span),
    written into takes.json as "vis". The robot has no mouth; "Oh..." is acted by her face, not by a viseme."""
    p = FILM_OUT + "/takes.json"
    meta = json.load(open(p))
    for shot, who, cap, give in FILM:
        if who == "ROBOT" or give == "oh":
            meta[shot]["vis"] = []
            continue
        a = sf.read("%s/%s.wav" % (FILM_OUT, shot))[0].astype(np.float64)
        meta[shot]["vis"] = bc.visemes(a, give or cap)
        print("%-5s %-6s %s" % (shot, who, "".join(v or "-" for v in meta[shot]["vis"])), flush=True)
    json.dump(meta, open(p, "w"), indent=1)


# ---------------------------------------------------------------- v6 of the film: "Oh...", without the breath
FILM_V6 = "ob_voices/film_v6"


def hiss_lead(a, sr=SR):
    """Seconds of unvoiced hiss before the first voiced 20 ms of a take (energy above 4 kHz, none below 1 kHz)."""
    hop = int(sr * 0.01); n = int(sr * 0.02)
    peak = np.sqrt(np.mean(a ** 2)) + 1e-9
    for i in range(0, len(a) - n, hop):
        w = a[i:i + n] * np.hanning(n)
        S = np.abs(np.fft.rfft(w)) ** 2; f = np.fft.rfftfreq(n, 1.0 / sr)
        if S[f < 1000].sum() > 0.5 * S.sum() and np.sqrt(np.mean(a[i:i + n] ** 2)) > 0.25 * peak:
            return i / float(sr)
    return 0.0


def oh_clean(a):
    """The take from its vowel: the breath in front of it (0.15 s of hiss) was heard as an s, "so". 12 ms of fade-in."""
    i0 = max(0, int((hiss_lead(a) - 0.004) * SR))
    b = a[i0:].copy()
    f = int(0.012 * SR); b[:f] *= np.linspace(0, 1, f) ** 2
    return b


def film_v6():
    """The takes of v5 (ob_voices/film, untouched) with "Oh..." cleaned, in ob_voices/film_v6."""
    import shutil
    os.makedirs(FILM_V6, exist_ok=True)
    meta = json.load(open(FILM_OUT + "/takes.json"))
    for shot in meta:
        shutil.copyfile("%s/%s.wav" % (FILM_OUT, shot), "%s/%s.wav" % (FILM_V6, shot))
    a = oh_clean(sf.read(FILM_OUT + "/3.7.wav")[0].astype(np.float64))
    sf.write(FILM_V6 + "/3.7.wav", a.astype(np.float32), SR)
    a0, a1 = slope(a)
    meta["3.7"].update(len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))), start=round(a0), end=round(a1),
                       rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3))
    json.dump(meta, open(FILM_V6 + "/takes.json", "w"), indent=1)
    return meta


# ---------------------------------------------------------------- v7 of the film: Pam's one remark
FILM_V7 = "ob_voices/film_v7"
PAM_LINE = ("9.1", "PAM", "Some shit, others scoop.")


def film_v7():
    """The takes of v6 (ob_voices/film_v6, untouched) and Pam's line, in ob_voices/film_v7. Her voice is the one she
    had in The Best Candidate (sound_xmas.pam_line, key A: bf_emma, dry, flat, unimpressed)."""
    import shutil
    os.makedirs(FILM_V7, exist_ok=True)
    meta = json.load(open(FILM_V6 + "/takes.json"))
    for shot in meta:
        shutil.copyfile("%s/%s.wav" % (FILM_V6, shot), "%s/%s.wav" % (FILM_V7, shot))
    shot, who, cap = PAM_LINE
    a = trim(np.asarray(bc.norm(sx.pam_line(cap, "A")), dtype=np.float64))
    sf.write("%s/%s.wav" % (FILM_V7, shot), a.astype(np.float32), SR)
    a0, a1 = slope(a)
    meta[shot] = dict(who=who, text=cap, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))), start=round(a0), end=round(a1),
                      rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3),
                      jump=round(float(np.abs(np.diff(a)).max()), 3), vis=bc.visemes(a, cap))
    json.dump(meta, open(FILM_V7 + "/takes.json", "w"), indent=1)
    return meta


# ---------------------------------------------------------------- v10 of the film: Pam's line, as the recogniser hears it
FILM_V10 = "ob_voices/film_v10"


def film_v10():
    """The takes of v7 with Pam's line recorded again. In the final mix Whisper heard the first take as "Some shit other
    scooper" (0 of 3 windows): given "Some shit, others scoop." at her usual pace (0.92) the voice let the last p go
    with a vowel, and the room and the master's knee made it a syllable. Tried through the mix's own chain (room, room
    tone, gain, knee), the same four words given as two sentences at pace 1.0 are heard "Some shit other scoop." in 3
    of 3; at 0.92 and at 0.84 they are not. The caption keeps the comma."""
    import shutil
    os.makedirs(FILM_V10, exist_ok=True)
    meta = json.load(open(FILM_V7 + "/takes.json"))
    for shot in meta:
        shutil.copyfile("%s/%s.wav" % (FILM_V7, shot), "%s/%s.wav" % (FILM_V10, shot))
    shot, who, cap = PAM_LINE
    v, sp, _ = sx.PAMS["A"]
    a = trim(np.asarray(bc.norm(so.dry("Some shit. Others scoop.", v, 1.0)), dtype=np.float64))
    sf.write("%s/%s.wav" % (FILM_V10, shot), a.astype(np.float32), SR)
    a0, a1 = slope(a)
    meta[shot] = dict(who=who, text=cap, len=round(len(a) / float(SR), 3), f0=round(float(bc.f0(a))), start=round(a0), end=round(a1),
                      rms=round(float(np.sqrt(np.mean(a ** 2))), 3), peak=round(float(np.abs(a).max()), 3),
                      jump=round(float(np.abs(np.diff(a)).max()), 3), vis=bc.visemes(a, cap))
    json.dump(meta, open(FILM_V10 + "/takes.json", "w"), indent=1)
    return meta
