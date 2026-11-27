"""The Blueprint, the rough with sound. Budget: bp_sound_v1 to bp_sound_v5.

The picture is bp_rough_v5 (and its no-night cut), stream-copied: no frame is redrawn.
A later call can name another picture. The default stays v5, so a bare mix still writes the v1 sound files.
The sound is the dry takes of src/bp_voices/ at the times in the-blueprint/bp_sound_v1_timing.json (bp_scenes.timeline),
over cs_film's room tone at TONE 0.3. No reflections (voices stay dry, Tomas 23 Nov 2026), no music, no pink noise.
A picture pass passes its own timing file. That call does not rewrite bp_sound_v1_timing.json.
Loudness is measured on the AAC that ships: -15 +-1 LUFS, true peak at most -1 dBTP. The limiter starts at 0.50
because AAC overshoots the WAV's peak.

  python3 bp_sound.py mix nonight   -> ../the-blueprint/bp_sound_v1_nonight.mp4 (360 s, no night lines)
  python3 bp_sound.py mix full      -> ../the-blueprint/bp_sound_v1.mp4 (400 s, the night lines are local only)
  python3 bp_sound.py mix full 2    -> bp_sound_v2.mp4 on bp_pic_v2 and bp_pic_v2_timing.json
  python3 bp_sound.py check [path]  -> Whisper on every line inside the mix, 3 windows; exit 1 under 2 of 3
  python3 bp_sound.py plant         -> the check on known bad mixes; exit 1 unless the muted line fails
Needs ASR_DIR."""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

import bp_scenes as bs
import bp_voices as bv

SOUND_BUDGET = 5
VERSION = 1
SR = 48000
TONE = 0.3                    # cs_film: 0.3 kept 14 of 14 lines
TARGET = -15.0
PEAK = -1.0
# Each is tried; the highest that holds the target under the peak wins, because it limits the voices least.
# 26 Nov: at 0.50 the voices (19.6 dB peak over loudness) needed over 10 dB of limiting and still fell short of -15.
LIMITS = (0.50, 0.60, 0.70, 0.80, 0.85)
EP = bs.EP
PICTURE = {"full": "bp_rough_v5.mp4", "nonight": "bp_rough_v5_nonight.mp4"}
SECONDS = {"full": 400, "nonight": 360}
FADE = int(0.005 * SR)        # 5 ms on each take's ends: no click where a trimmed take starts


def out_path(cut, version=VERSION):
    return os.path.join(EP, "bp_sound_v%d%s.mp4" % (version, "_nonight" if cut == "nonight" else ""))


def placed(cut, path=None):
    """(row, start in seconds) for the lines in this cut.
    No path rebuilds bp_sound_v1_timing.json. A picture pass passes its own file and leaves that one alone."""
    path = path or bs.write_timing()
    rows = json.load(open(path, encoding="utf-8"))["lines"]
    return [(r, r[cut]) for r in rows if r[cut] is not None]


def room_tone(n):
    """cs_film.py lines 109-114: the lows of a noise, a slow drift, and a faint 100/200 Hz hum."""
    rs = np.random.RandomState(5)
    tone = rs.standard_normal(n)
    for k_ in (400, 200, 100):
        tone = np.convolve(tone, np.ones(k_) / k_, mode="same")
    tt = np.arange(n) / float(SR)
    tone = tone / np.abs(tone).max() * 0.006 * (1 + 0.15 * np.sin(2 * np.pi * 0.21 * tt))
    tone += 0.0012 * np.sin(2 * np.pi * 100 * tt) + 0.0006 * np.sin(2 * np.pi * 200 * tt)
    return tone


def audio(cut, tone=TONE, mute=(), timing=None):
    n = SECONDS[cut] * SR
    voice = np.zeros(n)
    for r, t in placed(cut, timing):
        if r["key"] in mute:
            continue
        x, sr = sf.read(os.path.join(bv.OUT, r["key"] + ".wav"))
        if sr != SR:
            raise SystemExit("%s is %d Hz, not %d" % (r["key"], sr, SR))
        x = np.asarray(x, dtype=np.float64)
        if x.ndim > 1:
            x = x.mean(axis=1)
        ramp = np.linspace(0, 1, FADE)
        x[:FADE] *= ramp
        x[-FADE:] *= ramp[::-1]
        p = int(round(t * SR))
        voice[p:p + len(x)] += x[:n - p]
    return voice / max(1e-9, np.abs(voice).max()) * 0.7 + room_tone(n) * tone


def measure(path):
    log = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr.split("Summary:")[-1]
    return float(log.split("I:")[1].split("LUFS")[0]), float(log.split("Peak:")[1].split("dBFS")[0])


def _encode(picture, wav, out, gain, limit):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", picture, "-i", wav, "-map", "0:v", "-map", "1:a",
        "-af", "volume=%.2fdB,alimiter=limit=%.2f:attack=1:release=60:level=disabled" % (gain, limit),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest",
        "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact", "-movflags", "+faststart", out],
        check=True)


def master(cut, a, out, picture=None):
    """Gain to the target on the AAC itself. Returns (lufs, peak, gain, limit)."""
    tmp = "/tmp/bp_sound"
    os.makedirs(tmp, exist_ok=True)
    wav = os.path.join(tmp, "%s.wav" % os.path.basename(out))
    sf.write(wav, a.astype(np.float32), SR)
    pic = picture or os.path.join(EP, PICTURE[cut])
    i0, _ = measure(wav)
    part = out + ".part.mp4"
    best = None
    for limit in sorted(LIMITS, reverse=True):
        if best:
            break
        gain = TARGET - i0
        for _ in range(4):
            _encode(pic, wav, part, gain, limit)
            i, p = measure(part)
            if abs(i - TARGET) <= 0.3:
                break
            gain += TARGET - i
        ok = abs(i - TARGET) <= 0.3 and p <= PEAK
        print("  limit %.2f gain %+.2f dB -> %.1f LUFS, %.1f dBTP %s" % (limit, gain, i, p, "ok" if ok else ""), flush=True)
        if ok:
            best = (i, p, gain, limit)
    if not best:
        os.remove(part)
        raise SystemExit("no limit in %s holds %.0f LUFS under %.0f dBTP" % (LIMITS, TARGET, PEAK))
    i, p, gain, limit = best
    _encode(pic, wav, part, gain, limit)
    if measure(part) != (i, p):
        raise SystemExit("the re-encode at limit %.2f measured differently" % limit)
    os.replace(part, out)
    return best


def _picture_file(cut, version, picture):
    """v1 is the rough. A later version copies bp_pic_vN unless a picture stem is named."""
    if version <= 1 and picture is None:
        return os.path.join(EP, PICTURE[cut])
    stem = picture or ("bp_pic_v%d" % version)
    if stem.endswith(".mp4"):
        stem = stem[:-4]
    if stem.endswith("_nonight"):
        stem = stem[:-len("_nonight")]
    name = stem + ("_nonight.mp4" if cut == "nonight" else ".mp4")
    return os.path.join(EP, name)


def _stem_timing(stem):
    """Timing JSON that belongs to a picture stem (bp_pic_v5 → bp_pic_v5_timing.json)."""
    if stem.endswith(".mp4"):
        stem = stem[:-4]
    if stem.endswith("_nonight"):
        stem = stem[:-len("_nonight")]
    return os.path.join(EP, stem + "_timing.json")


def _timing_file(path, picture=None):
    """bp_sound_vN defaults to bp_pic_vN_timing.json. A named picture stem wins."""
    if picture is not None:
        return _stem_timing(picture)
    base = os.path.basename(path)
    if not base.startswith("bp_sound_v"):
        return None
    num = ""
    for ch in base[len("bp_sound_v"):]:
        if ch.isdigit():
            num += ch
        else:
            break
    if num and int(num) >= 2:
        return os.path.join(EP, "bp_pic_v%s_timing.json" % num)
    return None


def mix(cut, version=VERSION, out=None, picture=None, timing=None, **kw):
    if not 1 <= version <= SOUND_BUDGET:
        raise SystemExit("the rough with sound has a budget of %d versions; refused %d" % (SOUND_BUDGET, version))
    out = out or out_path(cut, version)
    if os.path.isfile(out):
        raise SystemExit("refusing to overwrite %s" % os.path.basename(out))
    if version >= 2 and os.path.basename(out).startswith("bp_sound_v1"):
        raise SystemExit("refusing to overwrite bp_sound_v1")
    pic = _picture_file(cut, version, picture)
    if not os.path.isfile(pic):
        raise SystemExit("no picture %s" % pic)
    if version >= 2 and timing is None:
        timing = _timing_file(out, picture=picture or ("bp_pic_v%d" % version))
    if timing is not None and not os.path.isfile(timing):
        raise SystemExit("no timing %s" % timing)
    i, p, gain, limit = master(cut, audio(cut, timing=timing, **kw), out, picture=pic)
    print("%s  %.1f LUFS  %.1f dBTP  gain %+.2f dB  limit %.2f  %d lines" % (
        out, i, p, gain, limit, len(placed(cut, timing))))
    return out


# ---- the check: Whisper inside the mix
def _pcm16k(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32).astype(np.float64)


def check(path, cut=None, quiet=False, timing=None):
    """Every line in at least 2 of 3 windows. A one-word line is heard with the line before it."""
    cut = cut or ("nonight" if path.endswith("_nonight.mp4") else "full")
    a = _pcm16k(path)
    rows = placed(cut, timing or _timing_file(path))
    bad, report = [], []
    for i, (r, t) in enumerate(rows):
        if r["text"] == "Oh...":
            report.append((r, None, ["(a vowel: no ASR)"]))
            continue
        t0, want = t, r["text"]
        prev = rows[i - 1] if i and rows[i - 1][0]["shot"] == r["shot"] else None
        if len(bv.words(r["text"])) == 1 and prev:
            t0, want = prev[1], prev[0]["text"] + " " + r["text"]
        t1 = t + (r["t1"] - r["t0"])
        heard = []
        for pre, post in ((0.05, 0.05), (0.3, 0.05), (0.05, 0.3)):
            seg = a[max(0, int((t0 - pre) * 16000)):int((t1 + post) * 16000)]
            heard.append(bv.hear(seg, 16000))
        word = json.load(open(os.path.join(bv.OUT, "takes.json"), encoding="utf-8"))[r["key"]].get("word")
        ok = sum(1 for h in heard if bv.match(h, want, word))
        report.append((r, ok, heard))
        if ok < 2:
            bad.append(r["key"])
    if not quiet:
        for r, ok, heard in report:
            print("%s %-8s %s  %s" % (r["shot"], r["key"], "-  " if ok is None else "%d/3" % ok, " | ".join(heard)),
                  flush=True)
        print("FAIL" if bad else "PASS", "(%d of %d lines under 2 of 3)%s" % (len(bad), len(rows),
                                                                            (": " + ", ".join(bad)) if bad else ""))
    return bad


def plant(version=1):
    """The check must lose a line that is not there. Room tone x5 is the plan's plant; its result is reported.
    version 2 mutes the same two lines on the picture-pass timeline and does not rebuild the v1 file."""
    tmp = "/tmp/bp_sound"
    os.makedirs(tmp, exist_ok=True)
    if version >= 2:
        timing = os.path.join(EP, "bp_pic_v%d_timing.json" % version)
        muted = mix("nonight", version, out=os.path.join(tmp, "plant_mute_v%d.mp4" % version), mute=("cs_6.5", "fs_4.1"))
        lost = check(muted, "nonight", quiet=True, timing=timing)
        caught = set(lost) == {"cs_6.5", "fs_4.1"}
        print("plant muted cs_6.5 and fs_4.1: lost %s -> %s" % (lost, "caught" if caught else "MISSED"))
        return caught
    loud = mix("nonight", out=os.path.join(tmp, "plant_tone5.mp4"), tone=TONE * 5)
    lost = check(loud, "nonight", quiet=True)
    print("plant tone x5: %d lines lost %s" % (len(lost), lost))
    muted = mix("nonight", out=os.path.join(tmp, "plant_mute.mp4"), mute=("cs_6.5", "fs_4.1"))
    lost = check(muted, "nonight", quiet=True)
    caught = set(lost) == {"cs_6.5", "fs_4.1"}
    print("plant muted cs_6.5 and fs_4.1: lost %s -> %s" % (lost, "caught" if caught else "MISSED"))
    return caught


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "mix"
    if cmd == "mix":
        cut = sys.argv[2] if len(sys.argv) > 2 else "nonight"
        version = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        picture = sys.argv[4] if len(sys.argv) > 4 else None
        mix(cut, version, picture=picture)
    elif cmd == "check":
        p = sys.argv[2] if len(sys.argv) > 2 else out_path("nonight")
        sys.exit(1 if check(p) else 0)
    elif cmd == "plant":
        version = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        sys.exit(0 if plant(version) else 1)
    else:
        raise SystemExit("mix nonight|full | check [path] | plant")
