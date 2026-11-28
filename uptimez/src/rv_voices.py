"""Approved. (episode 16): the film's 11 lines, stage 2 of series/production-process.md (script v3, 28 Nov; Tomas,
/grill-me: "Script + reuse"). Built from da_voices.py (episode 15, branch uptimez-double-agent), which is untouched:
the same takes, Whisper and pick rules. The series' own voices, no auditions: Don am_onyx (sound_bc.don), Pam voice A
bf_emma (as in 15), Father voice B (dh_voices, as in 12-15), Sofia (sound_bc.sofia, low and flat, as in 14), the robot
voice B (sound_bc.robot, as in 14), the machine panel in the robot's family, flat (script v2).
Four takes per line, A-D, at 0.90 / 0.96 / 1.02 / 1.08 of the voice's own speed (the robot and the panel: one take,
their voice has no speed). Each take gets Whisper in three windows; a short line also with the line before as context
(lesson 121). The pick per line: the most windows heard word for word, then the most heard at all, then B, then the
nearest speed to B. Tomas can overrule any pick in PICK.
REUSE: Don's "Approved." (3.4) is episode 15's take 7.2 B, copied to rv_voices/takes/3.4_B.wav: the same take every
episode, an audio callback. It is scored like the others but never re-recorded.
  python3 rv_voices.py takes      -> rv_voices/takes/<shot>_<A-D>.wav, takes.json, picks
  python3 rv_voices.py audition   -> ../the-review/rv_voices_audition_v1.mp4 (every take, a card each)
  python3 rv_voices.py timing     -> ../the-review/rv_timing_v1.json, rv_voices_v1.mp4 (the picks at their times)
Needs the Kokoro model (KOKORO_DIR) and the Whisper model (ASR_DIR). Run locally: this cloud session cannot fetch
the Kokoro weights."""
import os
import sys
import json
import re
import subprocess
import numpy as np
import soundfile as sf
import sound_ob as ob
import sound_bc as bc
import sound_on as so
import sound_xmas as sx
import sound_fs as sfs
import dh_voices as dv

SR = 48000
OUT = "rv_voices/takes"
EP = "../the-review/"
SCRIPT = EP + "the-review-script-v3.md"
# shot, who, the line, what the voice is given (None = the line), gain, note
LINES = [
    ("1.2", "DON", "Pam! Coffee.", None, 1.0, "an order, eyes shut, from the floor"),
    ("1.4", "FATHER", "Executive.", None, 1.0, "calm, looking at his folding chair"),
    ("2.5", "SOFIA", "We'll be in touch.", None, 1.0, "professional, an interviewer's close"),
    ("3.2", "DON", "I usually delegate.", None, 1.0, "proud, to Father"),
    ("3.3", "PANEL", "Human approval required.", None, 0.85, "flat, polite, the robot's family"),
    ("3.4", "DON", "Approved.", None, 1.0, "not looking (episode 15's take, reused)"),
    ("4.2", "FATHER", "Good hands.", None, 1.0, "quiet, a barely visible smile"),
    ("4.4", "PAM", "Did anyone review the business?", None, 0.85, "dry, to Father"),
    ("5.1", "ROBOT", "Yes.", None, 1.0, "from its station"),
    ("5.9", "FATHER", "There it is.", None, 1.0, "slow, quiet: he has found his money"),
    ("5.10", "DON", "It reclines.", None, 1.0, "sincerely proud, tilting the throne"),
]
SPEEDS = {"A": 0.90, "B": 0.96, "C": 1.02, "D": 1.08}
ONE_TAKE = ("ROBOT", "PANEL")  # the robot's voice has no speed: one take, B
REUSE = {"3.4": "B"}           # kept as copied, never re-recorded
PICK = {}                      # Tomas's overrides: shot -> letter
LEAD, TAIL = 0.15, 0.35        # a line starts 0.15 s into its shot and leaves 0.35 s after it
TAKES_OF = {}
GAP = {}
RUN_ON = {}
DUCK = {}
# where in its shot a line starts, from the script's action (the line lands after the action it follows, never on it)
AT = {"1.2": 0.6,        # the cup is up
      "1.4": 0.9,        # the chair unfolded
      "2.5": 0.9,        # pinned, checked, the point
      "3.2": 0.6,        # the filter in upside down
      "3.3": 0.3,        # the panel lights
      "3.4": 0.5,        # the jab
      "4.2": 0.6,        # the smile
      "4.4": 0.5,        # her eyes reach the corner
      "5.1": 0.3,        # the head up
      "5.9": 0.8,        # straightens, the eye up, 0.4 s hold
      "5.10": 0.6}       # the tilt


def take(who, txt, k):
    if who == "DON":
        return bc.don(txt, k)
    if who == "PAM":
        return bc.norm(sx.best_take(txt, "bf_emma", 0.92 * k, "en-gb"))
    if who == "SOFIA":
        return bc.sofia(txt, 0.95 * k, g=0.10)                     # low, flat (as in 14)
    if who == "FATHER":
        v, sp, semis, n = dv.FATHER[dv.FATHER_VOICE]
        return dv.one((v, sp * k, semis, n), txt)
    if who in ("ROBOT", "PANEL"):
        return bc.robot(txt)
    raise ValueError(who)


def recognizer():
    import sherpa_onnx as so_
    d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
    return so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx",
                                              tokens=d + "base.en-tokens.txt")


def _to16(a):
    return np.interp(np.linspace(0, len(a) - 1, int(len(a) * 16000 / SR)), np.arange(len(a)), a)


def _hear(r, w):
    s = r.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); r.decode_stream(s)
    return s.result.text.strip()


def score(r, a, line, prev):
    a16 = _to16(a); pad = np.zeros(4800)
    heard = [_hear(r, w) for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad]))]
    want = " ".join(sfs._words(line))
    good = sum(1 for h in heard if sfs._match(h, want))
    if good < 2 and prev is not None:                  # lesson 121: a short line gets the line before as context
        pw, ptxt = prev; p16 = _to16(pw)
        ctx = [_hear(r, np.concatenate([p16, np.zeros(int(g * 16000)), a16, pad])) for g in (0.3, 0.5, 0.8)]
        both = " ".join(sfs._words(ptxt + " " + line))
        cgood = sum(1 for h in ctx if sfs._match(h, want) or sfs._match(h, both))
        if cgood >= 2:
            heard += ["[with the line before] " + h for h in ctx]; good = cgood
    return good, heard


def takes(only=None):
    os.makedirs(OUT, exist_ok=True)
    r = recognizer()
    p = OUT + "/takes.json"
    meta = json.load(open(p)) if os.path.exists(p) else {}
    prev = None
    for shot, who, line, give, gain, note in LINES:
        if only and shot not in only:
            if shot in meta:
                w, _ = sf.read("%s/%s_%s.wav" % (OUT, shot, meta[shot]["pick"])); prev = (w, line)
            continue
        rows = {}
        letters = {REUSE[shot]: 1.0} if shot in REUSE else ({"B": SPEEDS["B"]} if who in ONE_TAKE else SPEEDS)
        for L, k in letters.items():
            if shot in REUSE:
                a, _ = sf.read("%s/%s_%s.wav" % (OUT, shot, L)); a = np.asarray(a, dtype=np.float64)
            else:
                a = ob.trim(np.asarray(take(who, give or line, k), dtype=np.float64)) * gain
                sf.write("%s/%s_%s.wav" % (OUT, shot, L), a.astype(np.float32), SR)
            good, heard = score(r, a, line, prev)
            want = sfs._words(line)                    # strict: every word as written ("rules" is not "rule")
            exact = sum(1 for h in heard[:3] if sfs._words(h) == want)
            rows[L] = dict(len=round(len(a) / float(SR), 2), ok=good, exact=exact, asr=heard)
            print("%-5s %-6s %s %4.2f s  %d/3 exact %d/3  %-36s | %s" % (shot, who, L, rows[L]["len"], good, exact, line,
                  " / ".join(heard[:3])), flush=True)
        best = PICK.get(shot) or sorted(rows, key=lambda L: (-rows[L]["exact"], -rows[L]["ok"], abs(SPEEDS.get(L, 0.96) - SPEEDS["B"]), L))[0]
        meta[shot] = dict(who=who, text=line, note=note, takes=rows, pick=best, len=rows[best]["len"], ok=rows[best]["ok"])
        w, _ = sf.read("%s/%s_%s.wav" % (OUT, shot, best)); prev = (w, line)
    json.dump(meta, open(p, "w"), indent=1)
    bad = [k for k, m in meta.items() if m["ok"] < 2]
    print("picks: " + ", ".join("%s %s" % (k, m["pick"]) for k, m in meta.items()))
    print("spoken (picks): %.1f s; heard at least 2 of 3: %d of %d%s" % (sum(m["len"] for m in meta.values()),
          len(meta) - len(bad), len(meta), ("  FAILED: " + ", ".join(bad)) if bad else ""))
    if bad:
        sys.exit(1)


def shots():
    """The shots from the script's tables (stage 2; from stage 4 the scene file rv_scenes is the one source):
    act, shot, script length, picture, line."""
    out, act = [], ""
    for ln in open(SCRIPT):
        if ln.startswith("### Act"):
            act = ln[4:].split("(")[0].strip()
        m = re.match(r"\| (\d\.\d+) \| \d:\d+\.\d \| (\d\.\d\d) \|", ln)
        if m and act:
            c = [x.strip() for x in ln.split("|")]
            line = c[7] if len(c) > 7 and c[7] not in ("—", "") and not c[7].startswith("— *") else None
            out.append(dict(scene=act, shot=m.group(1), script=float(m.group(2)), picture=c[5], line=line))
    return out


def _card(path, head, big, rest, small):
    import cairo
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(s)
    c.set_source_rgb(0.12, 0.13, 0.16); c.paint()
    def txt(x, y, size, s_, col=(0.95, 0.93, 0.88), bold=0):
        c.set_source_rgb(*col); c.select_font_face("Inter", 0, bold); c.set_font_size(size); c.move_to(x, y); c.show_text(s_)
    txt(30, 140, 18, head, (0.75, 0.75, 0.80))
    txt(30, 200, 44, big, bold=1)
    txt(30, 240, 22, small, (0.75, 0.75, 0.80))
    y = 300
    for i, (part, col, size) in enumerate(rest):
        txt(30, y, size, part, col, 1 if size >= 28 else 0); y += size + 10
    s.write_to_png(path)


def _render(cards, a, t, out_mp4, tag):
    wav = "/tmp/%s.wav" % tag; sf.write(wav, a, SR)
    lst = ["file '%s'\nduration %.3f\n" % (png, d) for png, d in cards] + ["file '%s'\n" % cards[-1][0]]
    open("/tmp/%s_list.txt" % tag, "w").write("".join(lst))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "/tmp/%s_list.txt" % tag,
                           "-i", wav, "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2,aresample=48000",
                           "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k",
                           "-t", "%.3f" % t, out_mp4])
    print("wrote", out_mp4)


def audition(out_mp4=EP + "rv_voices_audition_v1.mp4"):
    meta = json.load(open(OUT + "/takes.json"))
    fr = "/tmp/rv_aud"; os.makedirs(fr, exist_ok=True)
    cards, parts, t = [], [], 0.0
    for shot, who, line, _, _, note in LINES:
        m = meta[shot]
        for L in [x for x in SPEEDS if x in m["takes"]]:
            w, _ = sf.read("%s/%s_%s.wav" % (OUT, shot, L))
            d = 0.3 + len(w) / SR + 0.6
            buf = np.zeros(int(d * SR)); buf[int(0.3 * SR):int(0.3 * SR) + len(w)] = w; parts.append(buf)
            png = "%s/%s_%s.png" % (fr, shot, L)
            r = m["takes"][L]
            _card(png, "APPROVED. · voices v1 · audition", "%s  %s  %s" % (shot, who, L),
                  [(s_, (1.0, 0.86, 0.35), 30) for s_ in _wrap(line, 26)] + [("", (0, 0, 0), 10), (note, (0.95, 0.93, 0.88), 20)]
                  + [("heard: " + h, (0.70, 0.80, 0.70), 16) for h in r["asr"][:3]],
                  "speed x%.2f  ·  %.2f s  ·  Whisper %d/3%s" % (SPEEDS.get(L, 1.0), r["len"], r["ok"], "  ·  PICK" if L == m["pick"] else ""))
            cards.append((png, d)); t += d
    _render(cards, np.concatenate(parts), t, out_mp4, "rv_aud")


def timing(out_json=EP + "rv_timing_v1.json", out_mp4=EP + "rv_voices_v1.mp4"):
    meta = json.load(open(OUT + "/takes.json"))
    rows, t = [], 0.0
    for r in shots():
        ks = [k for k in TAKES_OF.get(r["shot"], (r["shot"],)) if k in meta]
        gap = GAP.get(r["shot"], 0.25)
        at0 = AT.get(r["shot"], LEAD)
        need = at0 + sum(meta[k]["len"] for k in ks) + gap * max(0, len(ks) - 1) + TAIL if ks else 0.0
        if r["shot"] in RUN_ON:                                # the rest of the line is carried by the next shot
            nxt = [x for x in shots() if x["shot"] == RUN_ON[r["shot"]]][0]
            assert need <= r["script"] + nxt["script"], "%s: the run-on line is longer than the next shot" % r["shot"]
            need = 0.0
        ln = round(max(r["script"], need), 2)
        at, offs = at0, []
        for k in ks:
            offs.append(round(at, 2)); at += meta[k]["len"] + gap
        rows.append(dict(r, start=round(t, 2), len=ln, takes=ks, picks=[meta[k]["pick"] for k in ks], take_at=offs,
                         run_on=RUN_ON.get(r["shot"]), duck={k: DUCK[k] for k in ks if k in DUCK},
                         longer=round(ln - r["script"], 2)))
        t += ln
    json.dump(dict(total=round(t, 2), script_total=round(sum(r["script"] for r in rows), 2), shots=rows), open(out_json, "w"), indent=1)
    print("script %.1f s -> with the takes %.1f s" % (sum(r["script"] for r in rows), t))
    for r in rows:
        if r["longer"] > 0:
            print("  %-5s +%.2f s  (%s)" % (r["shot"], r["longer"], " / ".join(meta[k]["text"] for k in r["takes"])))
    n = int(np.ceil(t * SR)); a = np.zeros(n)
    for r in rows:
        for k, off in zip(r["takes"], r["take_at"]):
            w, _ = sf.read("%s/%s_%s.wav" % (OUT, k, meta[k]["pick"]))
            i = int((r["start"] + off) * SR); a[i:i + len(w)] += w[:max(0, n - i)]
    fr = "/tmp/rv_cards"; os.makedirs(fr, exist_ok=True)
    cards = []
    for i, r in enumerate(rows):
        png = "%s/%03d.png" % (fr, i)
        rest = []
        if r["line"]:
            rest += [(p, (1.0, 0.86, 0.35), 30) for p in _wrap(re.sub(r"\*\*|\(.*?\)", "", r["line"]).replace(" · ", " / "), 26)]
            rest.append(("", (0, 0, 0), 10))
        rest += [(p, (0.95, 0.93, 0.88), 19) for p in _wrap(r["picture"].replace("**", ""), 44)[:14]]
        _card(png, "APPROVED. · voices v1 · %s" % r["scene"], r["shot"], rest,
              "%d:%04.1f  ·  %.2f s%s" % (r["start"] // 60, r["start"] % 60, r["len"],
                                          ("  (+%.2f)" % r["longer"]) if r["longer"] > 0 else ""))
        cards.append((png, r["len"]))
    _render(cards, a, t, out_mp4, "rv_voices")


def _wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + ([cur] if cur else [])


if __name__ == "__main__":
    {"takes": lambda: takes(sys.argv[2:] or None), "audition": audition, "timing": timing}[sys.argv[1]]()
