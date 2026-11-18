"""G5 QA worker for "Office Noir: The Secret of a Stolen Heart". Exits non-zero on any failure.
  python3 on_qa.py [video] [film_module]     defaults: on_film_1080.mp4 on_film
Checks:
  1 format     1080x1920, 30 fps, the expected frame count, BT.709 tags
  2 loudness   true peak <= -1 dBTP, integrated -16..-14 LUFS (ebur128 on the final AAC)
  3 speech     every voice line inside the final mix, windowed with its tail (three windows; a lone word gets
               the line before as context), transcribed (Whisper base.en), compared with the script word by word (>= 75 %) or letter by
               letter (>= 85 %, for words Whisper runs together: "Pamahart");
               a line passes in 2 of 3 windows ("borderline") or 3 of 3
  4 frame 0    complete: not a flash, nothing scaling in; the last frame leads back (the heart in the same place)
  5 text       every bubble, caption card and shout inside the series safe area (18, 96, 522, 820 at 540x960),
               30 px (1080) from the edges and off the right-hand button rail
  6 tails      every bubble tail ends on the speaker's mouth drawn in that frame (no off-screen tails)
  7 grid       on_qa_grid.png: one frame every 2 s at 270 px wide, for a human legibility pass
Every check was first run on a known failure (on_qa.py --selftest)."""
import sys
import json
import math
import re
import subprocess
import numpy as np

SAFE = (18, 96, 522, 820)
EDGE = 15                                     # 30 px at 1080
RAIL = (460, 480, 540, 820)                    # TikTok's right-hand buttons (540 units)
ASR_DIR = "/home/claude/models/asr/sherpa-onnx-whisper-base.en"
SCRIPT = {                                     # take -> the words as written
    "vo1": "Monday. Somebody left Pam a heart. Unsigned.",
    "vo_drink": "One drink.", "vo_inf": "One informant.", "vo_boss": "One boss.",
    "don_sofia": "Sofia. Did you steal my heart?",
    "sofia": "I sign my work... darling.",
    "vo_partner": "My partner. Never blinks.",
    "robot": "Suspect identified.",
    "robot_you": "You.",
    "pam": "You left me your heart.",
    "don_framed": "I was framed!",
    "vo6": "Nobody tells me what to do. Whiskey. Money. Women.",
    "mom_F_donnie": "Donnie!",
    "mom_F_up": "Up. Time for work.",
}
ALIAS = {"vo1": "vo1p"}
SAME = {"donny": "donnie", "danny": "donnie", "sophia": "sofia", "sofía": "sofia", "framed": "framed",
        "pan": "pam", "palm": "pam"}
FAILS = []


def report(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'}  {name:10s} {detail}")
    if not ok:
        FAILS.append(name)
    return ok


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,nb_frames,color_space,color_primaries,color_transfer",
                        "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]


def check_format(path, frames):
    s = probe(path)
    ok = (s["width"], s["height"], s["r_frame_rate"], int(s["nb_frames"])) == (1080, 1920, "30/1", frames)
    tags = (s.get("color_space"), s.get("color_primaries"), s.get("color_transfer"))
    ok = ok and tags == ("bt709", "bt709", "bt709")
    return report("format", ok, f"{s['width']}x{s['height']} {s['r_frame_rate']} {s['nb_frames']} frames "
                                f"(want {frames}) tags {tags}")


def check_loudness(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
    return report("loudness", tp <= -1.0 and -16.0 <= I <= -14.0, f"{I:.1f} LUFS, true peak {tp:+.1f} dBTP")


def _words(s):
    return [SAME.get(w, w) for w in re.findall(r"[a-zà-ÿ']+", s.lower().replace("…", " "))]


def _lcs(a, b):
    m = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            m[i + 1][j + 1] = m[i][j] + 1 if a[i] == b[j] else max(m[i][j + 1], m[i + 1][j])
    return m[-1][-1]


def _lev(a, b):
    p = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        q = [i]
        for j, y in enumerate(b, 1):
            q.append(min(p[j] + 1, q[j - 1] + 1, p[j - 1] + (x != y)))
        p = q
    return p[-1]


def _recognizer():
    import sherpa_onnx
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{ASR_DIR}/base.en-encoder.int8.onnx", decoder=f"{ASR_DIR}/base.en-decoder.int8.onnx",
        tokens=f"{ASR_DIR}/base.en-tokens.txt", language="en", task="transcribe", num_threads=4)


def _audio(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, np.float32)


def transcribe(rec, a, t0, t1):
    seg = a[max(0, int(t0 * 16000)):int(t1 * 16000)]
    s = rec.create_stream(); s.accept_waveform(16000, seg); rec.decode_stream(s)
    return s.result.text.strip()


def check_speech(path, T, shift=0.0):
    rec = _recognizer(); a = _audio(path)
    lens = json.load(open("on_voices/takes.json"))
    cues = {n: t0 for n, t0, g in T["cues"]}
    ok_all = True; rows = []
    for name, text in SCRIPT.items():
        if name not in cues:                                     # v9c: the narration with its pause
            lens[name] = lens[ALIAS[name]]; cues[name] = cues[ALIAS[name]]
        t0 = cues[name] + shift
        t1 = t0 + lens[name] + 0.45
        if name == "vo6":
            t1 = min(t1, cues["mom_F_donnie"] + 0.05)              # cut off by DONNIE! by design
        w0 = t0 - 0.10
        if lens[name] < 1.2:                                       # Whisper is unreliable on a lone word: give it the
            prev = [cues[n] + shift for n in SCRIPT if cues[n] < cues[name] and cues[name] - cues[n] < 2.5]
            w0 = min(prev) - 0.10 if prev else w0                   # line before as context, judge the end of it
        want = _words(text); res = []
        for d0, d1 in ((0.0, 0.0), (-0.05, 0.15), (0.05, -0.10)):   # three windows: Whisper flips on the edges
            got = transcribe(rec, a, w0 + d0, t1 + d1)
            have = _words(got)
            if w0 < t0 - 0.2:
                have = have[-(len(want) + 2):]
            ws = _lcs(want, have) / len(want)                      # words
            cw, ch = "".join(want), "".join(have)                   # characters: "Pam a heart" heard as "Pamahart"
            cs = 1 - _lev(cw, ch) / len(cw)
            res.append((max(ws, cs if cs >= 0.85 else 0.0), got))
        n_ok = sum(sc >= 0.75 for sc, _ in res)
        ok = n_ok >= 2
        ok_all &= ok
        score, got = min(res) if not ok else max(res)
        tag = "ok " if n_ok == 3 else ("ok~" if ok else "MISS")
        rows.append(f"    {tag} {name:13s} {n_ok}/3 {score:4.0%}  want \"{text}\"  heard \"{got}\"")
    report("speech", ok_all, f"{sum(r.strip().startswith('ok') for r in rows)}/{len(rows)} lines "
                             f"({sum(r.strip().startswith('ok~') for r in rows)} borderline: 2 of 3 windows)")
    print("\n".join(rows))
    return ok_all


def frame(path, n, w=270):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"select=eq(n\\,{n}),scale={w}:-1",
                        "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    h = len(r.stdout) // (w * 3)
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3).astype(np.float32) / 255


def _heart(f):
    m = (f[..., 0] > 0.6) & (f[..., 1] < 0.3) & (f[..., 2] < 0.3)
    if m.sum() < 15:
        return None
    ys, xs = np.nonzero(m)
    return xs.mean(), ys.mean(), int(m.sum())


def check_frame0(path, frames, first=0):
    f0, f2, fl = frame(path, first), frame(path, first + 2), frame(path, frames - 1)
    bright = f0.mean()
    still = np.abs(f0 - f2).mean()
    h0, hl = _heart(f0), _heart(fl)
    loop = h0 is not None and hl is not None and math.hypot(h0[0] - hl[0], h0[1] - hl[1]) <= 20
    ok = bright < 0.6 and still < 0.05 and loop
    return report("frame 0", ok, f"mean {bright:.2f} (flash > 0.6), change to frame 2 {still:.3f} (< 0.05), "
                                 f"heart frame 0 {tuple(round(v) for v in h0[:2]) if h0 else None} "
                                 f"last {tuple(round(v) for v in hl[:2]) if hl else None} (<= 20 px at 270 wide)")


def sweep(modname, T):
    """Draw every drawing of the film (no encode) and collect text boxes and tails."""
    import importlib
    import cairo
    F = importlib.import_module(modname)
    import props_sheet_on as psh
    import on_sb as sb
    boxes = []
    cap0 = psh.caption

    def cap(c, s, x, y, size=34):
        c.select_font_face(psh.TYPE, 0, 0); c.set_font_size(size)
        boxes.append(("card", s, x, y, c.text_extents(s).x_advance + 34 + 6, size * 1.7 + 6))
        return cap0(c, s, x, y, size)
    psh.caption = cap
    shout0 = sb.shout

    def shout(sf, text, size=64):
        c = cairo.Context(sf); c.select_font_face(psh.TYPE, 0, 0); c.set_font_size(size)
        rx = c.text_extents(text).x_advance / 2 + 50
        boxes.append(("shout", text, 270 - rx, getattr(sb, "SHOUT_CY", 150) - 70, 2 * rx, 140))
        return shout0(sf, text, size)
    sb.shout = shout
    F.patch()
    fm = F.Film(T)
    if getattr(sb, "SUSPECT_HUD", False):
        boxes.append(("hud", "> SUSPECT IDENTIFIED.", 34, 742, 300, 50))
    n_draw = int(round(T["total"] * F.DRAW))
    for n in range(n_draw):
        t = n / F.DRAW
        i = max(k for k in range(len(fm.st)) if fm.st[k] <= t + 1e-9)
        fm.beat(i, t)
    F.unpatch(); psh.caption = cap0; sb.shout = shout0
    for q in fm.qa:
        if len(q) > 4:
            boxes.append(("bubble", q[1], *q[4]))
    return boxes, fm.qa


def check_text(boxes):
    bad = set()
    for kind, s, x, y, w, h in boxes:
        why = []
        if x < max(SAFE[0], EDGE) or x + w > min(SAFE[2], 540 - EDGE):
            why.append("side")
        if y < SAFE[1]:
            why.append("top bar")
        if y + h > SAFE[3]:
            why.append("bottom captions")
        if x + w > RAIL[0] and y + h > RAIL[1] and y < RAIL[3]:
            why.append("button rail")
        if why:
            bad.add(f"    {kind:6s} {s!r:34s} x {x:.0f}-{x + w:.0f} y {y:.0f}-{y + h:.0f}: {', '.join(why)}")
    report("text", not bad, f"{len(set((b[0], b[1], round(b[2]), round(b[3])) for b in boxes))} distinct boxes, "
                            f"{len(bad)} outside the safe area")
    for b in sorted(bad):
        print(b)
    return not bad


def check_tails(qa):
    bad = []
    for q in qa:
        t, who, tip, mouth = q[:4]
        d = math.hypot(tip[0] - mouth[0], tip[1] - mouth[1]) if mouth else 1e9
        lim = q[5] + 6 if len(q) > 5 else 40                    # the lip corner: the mouth's own half-width
        if who in (None, "robot") or d > lim:
            bad.append((round(t, 2), who, round(d)))
    seen = sorted(set((b[1], b[2]) for b in bad))
    report("tails", not bad, f"{len(qa)} bubble drawings; misses {seen if seen else 'none'}")
    return not bad


def grid(path, frames, out="on_qa_grid.png"):
    sel = "+".join(f"eq(n\\,{n})" for n in range(0, frames, 60))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", f"select='{sel}',scale=270:-1,tile=7x3",
                    "-frames:v", "1", out], check=True)
    print(f"INFO  grid       {out}: one frame every 2 s at 270 px (human legibility pass)")


def main(path="on_film_1080.mp4", mod="on_film"):
    T = json.load(open("on_timing.json"))
    frames = int(round(T["total"] * 15)) * 2
    check_format(path, frames)
    check_loudness(path)
    check_speech(path, T)
    check_frame0(path, frames)
    boxes, qa = sweep(mod, T)
    check_text(boxes)
    check_tails(qa)
    grid(path, frames)
    print("\nG5 QA:", "PASS" if not FAILS else f"FAIL ({', '.join(FAILS)})")
    sys.exit(1 if FAILS else 0)


def selftest():
    """Each check on a known failure: it must fail."""
    T = json.load(open("on_timing.json"))
    frames = int(round(T["total"] * 15)) * 2
    print("-- known failures (each line must FAIL) --")
    a = check_format("on_film_preview.mp4", frames)                   # 540 wide, no BT.709 tags
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "on_film_1080.mp4", "-vn", "-af", "volume=4dB",
                    "-c:a", "aac", "-b:a", "192k", "/tmp/qa_loud.m4a"], check=True)
    b = check_loudness("/tmp/qa_loud.m4a")                            # 4 dB hot: over the peak and the range
    c = check_speech("on_film_1080.mp4", T, shift=2.5)                # every window 2.5 s late
    d = check_frame0("on_film_1080.mp4", frames, first=4)             # the lightning frame as frame 0
    boxes, qa = sweep("on_film_v2", T)                                 # 19:17 film: off-screen tail, robot "You."
    e = check_text([("bubble", "test", 40, 40, 200, 80)])             # a box under the top bar
    f = check_tails(qa)
    caught = [not x for x in (a, b, c, d, e, f)]
    FAILS.clear()
    print("\nselftest:", "every check caught its failure" if all(caught) else f"MISSED {caught}")
    sys.exit(0 if all(caught) else 1)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    main(*sys.argv[1:3])
