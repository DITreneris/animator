"""Daddy's Home, animatic v2: built from the eight approved scene sheets (dh_scenes.S1..S8), not from the old SEQ.
Every row of a sheet is one held frame for its own length; the takes in dh_voices/film_v1 are laid under the rows that
speak them. A take is found by its text, so a line split over two or three drawings ("The money..." / "...was invested.")
starts once, on the first of them. Nothing moves: this is the board with sound, to judge order, length and the lines.
  KOKORO_DIR=/tmp/kokoro python3 dh_animatic2.py            -> ../daddys-home/daddys_home_animatic_v2.mp4, dh_animatic_v2.json
  python3 dh_animatic2.py script                            -> ../daddys-home/daddys-home-script-v2.md (the sheets as a script)"""
import os
import re
import sys
import json
import subprocess
import numpy as np
import cairo
import soundfile as sf
from kit import Ctx, INK
import dh_layout as dl
import dh_animatic as da
import dh_voices as dv
import dh_scenes as ds

SR = 48000
OUT = "../daddys-home/dh_animatic2"
WHO = {"FATHER": "FATHER", "DON": "DON", "SOFÍA": "SOFÍA", "PAM": "PAM", "MOM": "MOM", "ROBOT": "ROBOT", "VISITOR": "VISITOR"}


def _norm(t):
    return re.sub(r"[^a-z]", "", t.lower())


def _said(line):
    """'DON: "The money..."' -> ('DON', 'The money...')"""
    m = re.match(r'\s*([A-ZÍ]+)[^:]*:\s*"(.*)"', line)
    return (m.group(1), m.group(2)) if m else (None, "")


def plan():
    meta = json.load(open(dv.FILM_OUT + "/takes.json"))
    left = {k: _norm(v["text"]) for k, v in meta.items()}
    rows = []
    cur = None                                              # (key, the part of its text not yet shown)
    for n, S in sorted(ds.ALL().items()):
        for sid, dur, fr, what, line in S:
            who, txt = _said(line) if line else (None, "")
            key = None
            if txt:
                t = _norm(txt)
                if cur and cur[1].startswith(t):            # the next piece of a take that is already running
                    cur = (cur[0], cur[1][len(t):])
                else:
                    key = next((k for k, v in left.items() if v.startswith(t)), None)
                    if key is None:
                        raise SystemExit("no take for %s %s: %r" % (n, sid, txt))
                    cur = (key, left.pop(key)[len(t):])
            rows.append(dict(scene=n, shot=sid, dur=dur, frame=fr, what=what, who=who, text=txt, key=key))
    if left:
        print("takes not used:", sorted(left))
    return rows, meta


def _frame(r):
    ds.ARM_PHONE[0] = r["scene"] >= 2
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960); c = cairo.Context(surf)
    fr = r["frame"]
    if isinstance(fr, dict) and "insert" in fr:
        fr["insert"](Ctx(c, 0), c)
    elif isinstance(fr, str) and fr in da.INSERTS:
        da.INSERTS[fr](Ctx(c, 0), c)
    else:
        sh = fr if isinstance(fr, dict) else {s_["name"]: s_ for s_ in dl.SHOTS_BLOCKING + dl.SHOTS_NEW + da.EXTRA}[fr]
        dl.draw(sh, Ctx(c, 0))
    c.identity_matrix()
    c.set_source_rgba(0, 0, 0, 0.55); c.rectangle(0, 0, 112, 30); c.fill()
    c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.move_to(8, 21); c.show_text("%d · %s" % (r["scene"], r["shot"]))
    if r["text"]:                                           # the line, at the top (y 96), never in the bottom quarter
        c.select_font_face("Inter", 0, 1); c.set_font_size(21)
        lines = [""]
        for w_ in r["text"].split():
            if c.text_extents((lines[-1] + " " + w_).strip()).x_advance > 440:
                lines.append(w_)
            else:
                lines[-1] = (lines[-1] + " " + w_).strip()
        h = 30 + 27 * len(lines)
        c.set_source_rgba(1, 1, 1, 0.94); c.rectangle(30, 96, 480, h); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(30, 96, 480, h); c.stroke()
        c.set_source_rgb(0.75, 0.15, 0.15); c.set_font_size(13); c.move_to(42, 114); c.show_text(WHO.get(r["who"], r["who"] or ""))
        c.set_source_rgb(*INK); c.set_font_size(21)
        for i, row in enumerate(lines):
            c.move_to(42, 138 + 27 * i); c.show_text(row)
    return surf


def main(out="../daddys-home/daddys_home_animatic_v2.mp4"):
    rows, meta = plan()
    os.makedirs(OUT, exist_ok=True)
    # The sheets' lengths are the approved ones: nothing is stretched. A take may run on under the next picture; where it
    # would run into the next take, it is cut off there with a short fade (the robot is interrupted on purpose in 6.2), and listed.
    t = 0.0; starts = []
    for r in rows:
        r["dur"] = round(r["dur"] * 30) / 30.0
        r["t"] = round(t, 3)
        if r["key"]:
            a, _ = sf.read("%s/%s.wav" % (dv.FILM_OUT, r["key"]))
            starts.append([t + 0.10, np.asarray(a, dtype=np.float64).copy(), r])
        t += r["dur"]
    audio = []; cuts = []
    for i, (at_, a, r) in enumerate(starts):
        end = at_ + len(a) / float(SR)
        nxt = starts[i + 1][0] if i + 1 < len(starts) else t
        if end > nxt - 0.02:
            keep = max(0, int((nxt - 0.02 - at_) * SR)); lost = end - (nxt - 0.02)
            a = a[:keep]; f = min(len(a), int(0.04 * SR))
            if f:
                a[-f:] *= np.linspace(1, 0, f)
            cuts.append((r["scene"], r["shot"], r["key"], round(lost, 2)))
        audio.append((at_, a))
    for cu in cuts:
        print("cut off by the next line: scene %d shot %s take %s, %.2f s lost" % cu)
    total = t
    mix = np.zeros(int((total + 0.5) * SR))
    for at_, a in audio:
        i0 = int(at_ * SR); mix[i0:i0 + len(a)] += a[:len(mix) - i0]
    sf.write(OUT + "/voices.wav", mix, SR)
    lst = []
    for n, r in enumerate(rows):
        png = "%s/a_%03d.png" % (OUT, n); _frame(r).write_to_png(png)
        lst.append("file '%s'\nduration %.4f\n" % (os.path.abspath(png), r["dur"]))
    lst.append("file '%s'\n" % os.path.abspath("%s/a_%03d.png" % (OUT, len(rows) - 1)))
    open(OUT + "/list.txt", "w").write("".join(lst))
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", OUT + "/list.txt", "-i", OUT + "/voices.wav",
                           "-vf", "fps=30,format=yuv420p", "-af", "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000", "-c:v", "libx264", "-crf", "20",
                           "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % total, tmp])
    os.rename(tmp, out)
    by = {}
    for r in rows:
        by[r["scene"]] = by.get(r["scene"], 0) + r["dur"]
    json.dump(dict(total=round(total, 2), by_scene={k: round(v, 2) for k, v in by.items()},
                   plan=[dict(scene=r["scene"], shot=r["shot"], t=r["t"], dur=round(r["dur"], 3), take=r["key"], who=r["who"], text=r["text"]) for r in rows]),
              open("../daddys-home/dh_animatic_v2.json", "w"), indent=1, ensure_ascii=False)
    print("total %.2f s, %d frames held, %d takes" % (total, len(rows), len(audio)))
    print("by scene:", {k: round(v, 2) for k, v in by.items()})
    print("wrote", out)


def script(out="../daddys-home/daddys-home-script-v2.md"):
    rows, meta = plan()
    tot = sum(r["dur"] for r in rows)
    o = ["# Daddy's Home: the script, v2 (from the eight scene sheets)\n",
         "UptimeZ Inc. · episode 12 · 22 Nov. Written out by `src/dh_animatic2.py script` from `src/dh_scenes.py`, so it cannot drift from the sheets. "
         "Script v1.6 and its beats are kept for the history; this is the running order now.\n",
         "**%.1f s, %d held drawings, %d spoken lines.** Scenes: %s.\n" % (
             tot, len(rows), len([r for r in rows if r["key"]]),
             ", ".join("%d %s (v%d)" % (n, ds.SCENES[n].title(), ds.VER[n]) for n in sorted(ds.SCENES))),
         "## What changed against script v1.6\n",
         "- **Scene 2:** Don's announcement is \"Brace yourselves. Dad is coming.\" His phone goes back on the throne's arm and stays there.",
         "- **Scene 3:** the folder says EXPENSES; \"Green is all he sees.\" replaces \"He won't count.\"",
         "- **Scene 4:** a gold PREMIUM sticker instead of a card; it stays on the repairman to the end.",
         "- **Scene 5:** the brush causes the POP; the filter flies across the room to Don at the throne; the robot says only \"CEO responsible.\"; the invoice is $80.",
         "- **Scene 6:** Don's protest is two drawings (recoil, surrender); Mom plants Pam beside Don and labels her HAND OF THE CEO; Sofía gets her own reaction shot.",
         "- **Scene 7:** the shut glass door with two shapes and a knocking fist; Father takes one step; Don's thumb stays up; the robot hops. The CV moved to scene 8.",
         "- **Scene 8:** the CV opens it; the second bodyguard posts himself on the far side; the robot's viewfinder finds the phone on the throne's arm (FOUND); "
         "Father's call makes the throne ring; the last frame is frame 0.",
         "- **Scene 1:** a neon motto in the booth, THE HOUSE ALWAYS COLLECTS.\n"]
    t = 0.0; cur = None
    for r in rows:
        if r["scene"] != cur:
            cur = r["scene"]
            o.append("\n## Scene %d · %s · %d:%04.1f · %.1f s\n" % (cur, ds.SCENES[cur].title(), int(t // 60), t % 60, sum(x["dur"] for x in rows if x["scene"] == cur)))
            o.append("| Shot | At | s | Picture | Line |\n|---|---|---|---|---|")
        line = ("%s: \"%s\"" % (r["who"], r["text"])) if r["text"] else ""
        o.append("| %s | %d:%04.1f | %.2f | %s | %s |" % (r["shot"], int(t // 60), t % 60, r["dur"], r["what"].replace("|", "/"), line))
        t += r["dur"]
    open(out, "w").write("\n".join(o) + "\n"); print("wrote", out, "%.1f s" % tot)


if __name__ == "__main__":
    script() if len(sys.argv) > 1 and sys.argv[1] == "script" else main()
