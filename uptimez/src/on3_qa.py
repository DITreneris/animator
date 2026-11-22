"""OFFICE NOIR 3: the G5 worker (uptimez/CLAUDE.md). Exit code 1 on any miss.
  python3 on3_qa.py FILM.mp4 timing.json [540.mp4 to compare a 1080 file with]
Checks: format (size, 30 fps, frame count, BT.709), loudness on the final AAC (-14..-16 LUFS, true peak <= -1 dBTP),
speech recognition on every line inside the final mix (three windows, a short line with the line before it), frame 0
against the last frame, and (for a scaled file) PSNR per frame against the 540 master.
Not checked here: text boxes in the safe area and tails (no worker for this film's bubbles yet); the report says so."""
import json
import re
import subprocess
import sys
import numpy as np
import on_qa as oq

SELF = "--self-test" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]


def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=width,height,r_frame_rate,nb_read_frames,color_space,color_primaries,color_transfer", "-of", "json", f], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]


def loud(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rindex("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1))


def frame(f, n, w=540, h=960):
    r = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", f, "-vf", "select=eq(n\\,%d),scale=%d:%d" % (n, w, h), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).astype(int)


def NUM(s):
    """Whisper writes numbers as digits ("100 bucks", "Round 1"): the script spells them."""
    return re.sub(r"\b100\b", "one hundred", re.sub(r"\b1\b", "one", re.sub(r"\b10\b", "ten", s)))


def speech(film, T, garble=False):
    rec = oq._recognizer(); a = oq._audio(film)
    if garble:
        a = a[::-1].copy()                                    # the known failure: the mix backwards
    L = T["lines"]; rows = []
    for i, (t0, t1, who, text, key) in enumerate(L):
        e = t1 + 0.45
        if i + 1 < len(L):
            e = min(e, L[i + 1][0] - 0.02) if L[i + 1][0] > t1 else e
        w0 = t0 - 0.10
        if t1 - t0 < 1.2 and i and t0 - L[i - 1][0] < 4.5:
            w0 = L[i - 1][0] - 0.10
        want = oq._words(text); res = []
        wins = [(w0 + d0, e + d1) for d0, d1 in ((0.0, 0.0), (-0.05, 0.15), (0.05, -0.10))]
        if w0 < t0 - 0.2:                                     # a short line is also heard on its own: the line before can eat its window
            wins += [(t0 - 0.10 + d0, e + d1) for d0, d1 in ((0.0, 0.0), (-0.05, 0.15), (0.05, -0.10))]
        for wa, wb in wins:
            got = oq.transcribe(rec, a, wa, wb)
            g_ = oq._words(got)
            if len(g_) >= 6 and len(set(zip(g_, g_[1:]))) <= 2:   # the recognizer looped ("I always I always I always"): void, hear a longer window
                got = oq.transcribe(rec, a, wa, wb + 0.45)
            have = oq._words(NUM(got))
            w0 = wa
            if w0 < t0 - 0.2:
                have = have[-(len(want) + 2):]
            ws = oq._lcs(want, have) / len(want)
            cw, ch = "".join(want), "".join(have)
            cs = 1 - oq._lev(cw, ch) / max(1, len(cw))
            res.append((max(ws, cs if cs >= 0.85 else 0.0), got))
        rows.append((sum(sc >= 0.75 for sc, _ in res) >= 2, who, text, max(res)[1]))                # two windows of all that were tried
    return rows


def main(film, timing, ref=None):
    T = json.load(open(timing)); bad = []
    p = probe(film); n = int(p["nb_read_frames"]); want_n = round(T["length"] * 30)
    fmt = (p["r_frame_rate"] == "30/1" and n == want_n and p.get("color_space") == "bt709" and p.get("color_primaries") == "bt709" and p.get("color_transfer") == "bt709")
    print("FORMAT  %s  %sx%s %s fps, %d frames (expected %d), %s/%s/%s" % ("PASS" if fmt else "FAIL", p["width"], p["height"], p["r_frame_rate"], n, want_n, p.get("color_space"), p.get("color_primaries"), p.get("color_transfer")))
    bad += [] if fmt else ["format"]
    print("SIZE    %s  1080x1920" % ("PASS" if (p["width"], p["height"]) == (1080, 1920) else "FAIL (%sx%s)" % (p["width"], p["height"])))
    i_, tp = loud(film); ok = -16 <= i_ <= -14 and tp <= -1.0
    print("LOUD    %s  %.1f LUFS, true peak %.1f dBTP" % ("PASS" if ok else "FAIL", i_, tp)); bad += [] if ok else ["loudness"]
    d = int(np.abs(frame(film, 0) - frame(film, n - 1)).mean() * 100) / 100
    ok = d < 1.5
    print("LOOP    %s  frame 0 against the last frame: mean difference %.2f of 255" % ("PASS" if ok else "FAIL", d)); bad += [] if ok else ["loop"]
    rows = speech(film, T)
    miss = [r for r in rows if not r[0]]
    print("SPEECH  %s  %d of %d lines heard" % ("PASS" if not miss else "FAIL", len(rows) - len(miss), len(rows)))
    for ok, who, text, got in miss:
        print("          %s: \"%s\" heard as \"%s\"" % (who, text, got))
    bad += ["speech"] if miss else []
    if SELF:
        g = speech(film, T, garble=True)
        print("SELF    %s  the mix played backwards: %d of %d lines heard (must be near 0)" % ("PASS" if sum(r[0] for r in g) <= 2 else "FAIL", sum(r[0] for r in g), len(g)))
    if ref:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", film, "-i", ref, "-lavfi", "[0:v]scale=540:960:flags=area[a];[a][1:v]psnr=stats_file=/tmp/on3_psnr.log", "-an", "-f", "null", "-"], capture_output=True, text=True)
        ps = [float(re.search(r"psnr_avg:([\d.inf]+)", l).group(1).replace("inf", "99")) for l in open("/tmp/on3_psnr.log")]
        ok = min(ps) >= 30
        print("SCALE   %s  against the 540 master: PSNR mean %.1f dB, lowest %.1f dB (frame %d)" % ("PASS" if ok else "FAIL", sum(ps) / len(ps), min(ps), ps.index(min(ps)))); bad += [] if ok else ["scale"]
    print("NOT CHECKED: text boxes in the safe area, tails, bubbles on faces (no worker for this film yet)")
    return bad


if __name__ == "__main__":
    b = main(*args)
    print("RESULT:", "PASS" if not b else "FAIL: " + ", ".join(b)); sys.exit(1 if b else 0)
