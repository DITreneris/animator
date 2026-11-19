"""(pinned: animatic v3) FIRST SEARCH (episode 10): the animatic v3 (fs_animatic_v2.py = v2, kept): storyboard v4, the plaster told whole
(clean at frame 0, cracked by the bonk, plastered by Sofía, dropped and healed at the end).
FIRST SEARCH (episode 10): the animatic v2 (fs_animatic_v1.py = v1, kept): storyboard v3 in script v6's order,
the takes of fs_voices/film_v6 (two new lines). Below, the notes of v1.
FIRST SEARCH (episode 10): the animatic v1. Storyboard v2 (fs_storyboard.py) held shot by shot for the lengths
the measured takes need (fs_voices/film/takes.json, sound_fs.py), each line as a caption at the top under the app's bar
while it is said, the takes and the episode's key sounds in place (the buzz, the tonk, ka-ching, the click, the chime,
the shutter, the ping, the shredder, the keys). A timing test, 540 x 960 at 30 fps: stills, no movement, no lip-sync,
no music yet. The baby photo carries Don's markers here (fs_set.BABY_DON), after the mute test of board v2.
  python3 fs_animatic.py [out_dir]   -> fs_timing_v1.json, fs_animatic_mix_v1.wav, fs_animatic_v1.mp4"""
import os
import sys
import json
import subprocess
import numpy as np
import soundfile as sf
import cairo
import kit
import fs_set as fs
import fs_storyboard_v4 as sb                                 # pinned: animatic v3 is board v4
import sound_bc_mix as bm
import sound_xmas as sx
import sound_iwry as si
from kit import Ctx, INK

V = "v3"
W, H, FPS, SR = 540, 960, 30, 48000
HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = "fs_voices/film_v6"
TAKES = json.load(open(os.path.join(HERE, VOICES, "takes.json")))
LEAD, TAIL = 0.15, 0.30
LINE_OF = {"1.2": "1.2", "2.2": "2.2", "3.3": "3.3", "4.1": "4.1", "4.2": "4.2", "4.3": "4.3", "5.2": "5.2",
           "5.3": "5.3", "7.1": "7.1"}
SPAN = {"1.2": ("1.2", "1.3")}                             # his line runs on into 1.3
WHO = {"CLIENT": "CLIENT", "DON": "DON", "SOFIA": "SOFÍA", "ROBOT": "ROBOT", "MOM": "MOM"}


def timing():
    """Shot lengths: a spoken shot holds lead + take + tail (or the board's hold, if longer); a line that runs on
    (SPAN) is spread over its shots."""
    rows, t = [], 0.0
    span_left = 0.0
    for shot, hold, fn, note in sb.SHOTS:
        ln = hold
        if shot in LINE_OF:
            need = LEAD + TAKES[LINE_OF[shot]]["len"] + TAIL
            if shot in SPAN:
                span_left = need - hold
            else:
                ln = max(hold, need)
        elif span_left > 0:
            ln = max(hold, span_left)
            span_left = 0.0
        rows.append(dict(shot=shot, start=round(t, 3), len=round(ln, 3)))
        t += ln
    return rows


def caption(c, who, text):
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(24)
    words, lines_, cur = text.split(), [], ""
    for w_ in words:
        t_ = (cur + " " + w_).strip()
        if c.text_extents(t_).x_advance > 440 and cur:
            lines_.append(cur); cur = w_
        else:
            cur = t_
    lines_.append(cur)
    h = 40 + 30 * len(lines_)
    c.set_source_rgba(1, 1, 1, 0.94); c.rectangle(34, 104, 472, h); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(34, 104, 472, h); c.stroke()
    c.set_font_size(13); c.set_source_rgb(0.35, 0.40, 0.50); c.move_to(48, 124); c.show_text(who)
    c.set_font_size(24); c.set_source_rgb(*INK)
    for i, l_ in enumerate(lines_):
        c.move_to(48, 152 + i * 30); c.show_text(l_)


def stills(d):
    os.makedirs(d, exist_ok=True)
    fs.LAYOUT[0] = "v2"; fs.REMOTE_BIG[0] = True; fs.BABY_DON[0] = True
    out = {}
    try:
        for shot, hold, fn, note in sb.SHOTS:
            for cap in (False, True):
                if cap and shot not in LINE_OF and shot != "1.3":
                    continue
                s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
                c = cairo.Context(s); k = Ctx(c, 0)
                sb.bg(c); fn(k)
                if cap:
                    key = "1.2" if shot == "1.3" else LINE_OF[shot]
                    m = TAKES[key]
                    caption(c, WHO[m["who"]], m["text"].upper() if m["who"] == "ROBOT" else m["text"])
                p = "%s/%s%s.png" % (d, shot, "_cap" if cap else "")
                s.write_to_png(p)
                out[(shot, cap)] = p
    finally:
        fs.LAYOUT[0] = "v1"; fs.REMOTE_BIG[0] = False; fs.BABY_DON[0] = False
    return out


def _at(mix, a, t, g=1.0):
    i = int(t * SR)
    a = np.asarray(a, dtype=np.float64)[:max(0, len(mix) - i)]
    mix[i:i + len(a)] += a * g


def buzz(d=0.45):
    t = np.arange(int(d * SR)) / SR
    a = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.6 + np.sign(np.sin(2 * np.pi * 116 * t)) * 0.4
    rattle = np.random.default_rng(3).standard_normal(len(t)) * (np.sin(2 * np.pi * 12 * t) > 0.6) * 0.5
    return bm.fade(si.lp(a, 5) + si.lp(rattle, 3), 0.005, 0.08)


def mix(rows, total):
    m = np.zeros(int((total + 0.5) * SR))
    at = {r["shot"]: r["start"] for r in rows}
    for shot, key in LINE_OF.items():                     # the voices
        a, sr = sf.read(os.path.join(HERE, VOICES, "%s.wav" % key))
        _at(m, a, at[shot] + LEAD, 1.0)
    fx = [  # (time, sound, gain)
        (0.70, buzz(), 0.30), (1.25, sx.thunk(0.25, 140), 0.55), (1.27, bm.chime([2400, 3100], 0.03, 0.4), 0.10),
        (at["2.3"] + 0.15, bm.chime([1568, 2093], 0.08, 0.5), 0.16),
        (at["3.1"] + 0.3, buzz(), 0.30), (at["3.4"] + 0.3, sx.thunk(0.08, 300), 0.15),
        (at["4.3"] + 0.4, sx.thunk(0.05, 900), 0.20), (at["4.5"] + 0.6, bm.chime([1047, 1319, 1568], 0.09, 0.7), 0.20),
        (at["6.1"] + 0.4, sx.whoosh(0.08), 0.45), (at["6.2"] + 0.3, bm.chime([1760, 2349], 0.07, 0.3), 0.14),
        (at["8.2"] + 0.2, buzz(0.35) * 0.4, 0.4), (at["9.1"] + 0.3, bm.chime([1047, 1319, 1568], 0.09, 0.7), 0.20),
    ]
    for t, a, g in fx:
        _at(m, a, t, g)
    for i in range(9):                                     # the robot's keys
        _at(m, sx.thunk(0.03, 1400), at["9.2"] + 0.9 + i * 0.09, 0.08)
    _at(m, sx.whoosh(0.05), at["9.3"] + 0.15, 0.25)                   # the plaster flutters down
    room = si.lp(np.random.default_rng(5).standard_normal(len(m)), 160) * 0.006
    m += room
    m *= 0.5 / max(1e-6, np.abs(m).max())
    return m


def main(d):
    rows = timing()
    total = rows[-1]["start"] + rows[-1]["len"]
    json.dump(rows, open(os.path.join(d, "fs_timing_%s.json" % V), "w"), indent=1)
    for r in rows:
        print("%-5s %6.2f  %5.2f" % (r["shot"], r["start"], r["len"]))
    print("total %.2f s" % total)
    tmp = "/tmp/fs_animatic"
    st_ = stills(tmp)
    m = mix(rows, total)
    wav = os.path.join(d, "fs_animatic_mix_%s.wav" % V)
    sf.write(wav, np.stack([m, m], 1).astype(np.float32), SR)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for r in rows:
            shot = r["shot"]
            if shot in LINE_OF or shot == "1.3":
                if shot == "1.3":
                    cap_end = TAKES["1.2"]["len"] + LEAD - (r["start"] - rows[[x["shot"] for x in rows].index("1.2")]["start"])
                    cap_end = max(0.0, min(r["len"], cap_end + 0.1))
                else:
                    cap_end = min(r["len"], LEAD + TAKES[LINE_OF[shot]]["len"] + 0.1)
                f.write("file '%s'\nduration %.4f\n" % (st_[(shot, True)], cap_end))
                if r["len"] - cap_end > 0.01:
                    f.write("file '%s'\nduration %.4f\n" % (st_[(shot, False)], r["len"] - cap_end))
            else:
                f.write("file '%s'\nduration %.4f\n" % (st_[(shot, False)], r["len"]))
        f.write("file '%s'\n" % st_[(rows[-1]["shot"], False)])
    out = os.path.join(d, "fs_animatic_%s.mp4" % V)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-c:a", "aac", "-b:a", "192k", "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
