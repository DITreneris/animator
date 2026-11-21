"""FIRST SEARCH (episode 10): the animatic v27 (fs_animatic_v26.py = v26, kept): storyboard v32; cut to about 36 s from
the same drawings and the same lines (every line whole: the holds trimmed to what it takes to read a shot, a line's lead
0.05 s and its tail 0.10 s, the ending RETRY-first); the bubbles' tails go beside the speaker's mouth on the side away
from anyone else, never with the tip inside the bubble; an off-screen speaker's bubble sits at the frame's edge on their
side, never on the portrait; the file is tagged BT.709, TV range.
FIRST SEARCH (episode 10): the animatic v26 (fs_animatic_v25.py = v25, kept): storyboard v28 (5.1 restaged; the
promise and the post's small print legible).
FIRST SEARCH (episode 10): the animatic v25 (fs_animatic_v24.py = v24, kept): storyboard v27 (frame 0 and the loop:
Don under the portrait, which smiles whenever it is whole).
FIRST SEARCH (episode 10): the animatic v24 (fs_animatic_v23.py = v23, kept): storyboard v26 (frame 0 closer, Pam out
front, 8.2 the rescue).
FIRST SEARCH (episode 10): the animatic v23 (fs_animatic_v22.py = v22, kept): storyboard v25 (staged for 9:16: groups
in depth, the faces bigger, frame 0 a medium-wide).
FIRST SEARCH (episode 10): the animatic v22 (fs_animatic_v21.py = v21, kept): storyboard v23 (the low angles pushed;
8.1 a medium shot).
FIRST SEARCH (episode 10): the animatic v21 (fs_animatic_v20.py = v20, kept): storyboard v22 (shot design v1: angles,
over-the-shoulders, the bank card as an insert, Pam behind Don, over Mom's shoulder).
FIRST SEARCH (episode 10): the animatic v20 (fs_animatic_v19.py = v19, kept): storyboard v21 (canon proportions, feet
on the floor) and the lines in speech bubbles again, as in every episode: each tail ends beside the speaker's mouth,
outside the head; an off-screen speaker gets a bubble with no tail; no bubble covers a face.
FIRST SEARCH (episode 10): the animatic v19 (fs_animatic_v18.py = v18, kept): storyboard v20 (the healed portrait
smiles under gold glints; Mom's arm round Pam; Pam's avatar).
FIRST SEARCH (episode 10): the animatic v18 (fs_animatic_v17.py = v17, kept): storyboard v19 (the v18 cold test's
fixes: 6.1 cut, the whoosh now on the hard cut to Mom; 9.5, the shake into frame 0).
FIRST SEARCH (episode 10): the animatic v17 (fs_animatic_v16.py = v16, kept): storyboard v18 (every shot on set v4:
the wider room, the counter's left end, Mom's way out round it; Don's hair bigger).
FIRST SEARCH (episode 10): the animatic v16 (fs_animatic_v15.py = v15, kept): storyboard v17 (Don's guilty glance,
the micro flashback to episode 9, a rewind zip on it; the post in LinkedIn's manner).
FIRST SEARCH (episode 10): the animatic v15 (fs_animatic_v14.py = v14, kept): storyboard v16 (6.2 in two beats).
FIRST SEARCH (episode 10): the animatic v14 (fs_animatic_v13.py = v13, kept): storyboard v15 (the blueprint's
line true to episodes 9 and 11; Sofía's comment; no nail on any thumb).
FIRST SEARCH (episode 10): the animatic v13 (fs_animatic_v12.py = v12, kept): storyboard v14 (the thumbs' owners,
pad side, no nail); fs_voices/film_v9 (Mom's deliveries picked by ear; every line 3/3 with Whisper).
FIRST SEARCH (episode 10): the animatic v12 (fs_animatic_v11.py = v11, kept): storyboard v13 (3.1b cut).
FIRST SEARCH (episode 10): the animatic v11 (fs_animatic_v10.py = v10, kept): storyboard v12 (the full cold
test's fixes; frame 0 matches frame 1).
FIRST SEARCH (episode 10): the animatic v10 (fs_animatic_v9.py = v9, kept): storyboard v11, Don's signs.
FIRST SEARCH (episode 10): the animatic v9 (fs_animatic_v8.py = v8, kept): storyboard v10, Pam's look.
FIRST SEARCH (episode 10): the animatic v8 (fs_animatic_v7.py = v7, kept): storyboard v9, Mom in her look v2.
FIRST SEARCH (episode 10): the animatic v7 (fs_animatic_v6.py = v6, kept): storyboard v8, Mom's three remarks
(fs_voices/film_v8: "Machines.", "That hussy.", "Pam has a plan.").
FIRST SEARCH (episode 10): the animatic v6 (fs_animatic_v5.py = v5, kept): storyboard v7, Mom's line; the takes
of fs_voices/film_v7 (the women's "Eww." in 7.4); a wet slurp on the lick (7.3), a squeak on the scrub (7.4).
FIRST SEARCH (episode 10): the animatic v5 (fs_animatic_v4.py = v4, kept): storyboard v6 (the tail pressed, Don's
glances, Pam's plan blocked by his thumb in 5.3).
FIRST SEARCH (episode 10): the animatic v4 (fs_animatic_v3.py = v3, kept): storyboard v5, Sofía's flirt in 1.2.
FIRST SEARCH (episode 10): the animatic v3 (fs_animatic_v2.py = v2, kept): storyboard v4, the plaster told whole
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
import fs_storyboard as sb
import sound_bc_mix as bm
import sound_xmas as sx
import sound_iwry as si
from kit import Ctx, INK

V = "v27"
W, H, FPS, SR = 540, 960, 30, 48000
HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = "fs_voices/film_v9"
TAKES = json.load(open(os.path.join(HERE, VOICES, "takes.json")))
LEAD, TAIL = 0.15, 0.30
RETIME = [True]                                            # v27: the ~36 s cut (False: v26's timing)
if RETIME[0]:
    LEAD, TAIL = 0.05, 0.10
CUT27 = {"1.1a": 0.8, "1.1b": 0.7, "1.2": 1.3, "1.3": 1.25, "2.1": 0.4, "2.2": 2.64, "2.3": 0.5, "3.1": 1.0, "3.2": 0.7,
         "3.3": 1.0, "3.4": 0.6, "4.1": 1.92, "4.2": 2.40, "4.3": 0.82, "4.4": 0.4, "4.5": 0.8, "5.1": 1.0, "5.2": 1.54,
         "5.2b": 0.4, "5.2c": 0.45, "5.3": 1.51, "6.1b": 1.12, "6.2a": 0.9, "6.2b": 1.0, "7.1": 1.39, "7.2": 0.6,
         "7.3": 0.5, "7.4": 1.09, "7.5": 1.05, "8.1": 1.51, "8.2": 0.8, "9.1": 0.8, "9.2": 1.6, "9.3": 0.7, "9.4": 0.6,
         "9.5": 0.3}
LINE_OF = {"1.2": "1.2", "2.2": "2.2", "3.3": "3.3", "4.1": "4.1", "4.2": "4.2", "4.3": "4.3", "5.2": "5.2",
           "5.3": "5.3", "7.1": "7.1", "7.4": "7.4",
           "6.1b": "6.1b", "7.5": "7.5", "8.1": "8.1"}
SPAN = {"1.2": ("1.2", "1.3")}                             # his line runs on into 1.3
WHO = {"CLIENT": "CLIENT", "DON": "DON", "SOFIA": "SOFÍA", "ROBOT": "ROBOT", "MOM": "MOM", "PAM+SOFIA": "PAM & SOFÍA"}


def timing():
    """Shot lengths: a spoken shot holds lead + take + tail (or the board's hold, if longer); a line that runs on
    (SPAN) is spread over its shots."""
    rows, t = [], 0.0
    span_left = 0.0
    for shot, hold, fn, note in sb.SHOTS:
        ln = hold
        if RETIME[0] and shot in CUT27:
            ln = CUT27[shot]
            if shot in LINE_OF and shot not in SPAN:
                ln = max(ln, LEAD + TAKES[LINE_OF[shot]]["len"] + TAIL)
            if shot in SPAN:
                span_left = max(0.0, LEAD + TAKES[LINE_OF[shot]]["len"] + TAIL - ln)
            elif span_left > 0:
                ln = max(ln, span_left); span_left = 0.0
            rows.append(dict(shot=shot, start=round(t, 3), len=round(ln, 3)))
            t += ln
            continue
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


BUBBLES = [True]                                           # v20: speech bubbles (canon); False = v19's caption boxes
SPEAKER = {"CLIENT": ["client"], "DON": ["don"], "SOFIA": ["sofia"], "ROBOT": ["robot"], "MOM": ["mom"],
           "PAM+SOFIA": ["sofia", "pam"]}
SAFE = (18, 96, 522, 720)                                  # bubbles stay out of the bottom quarter (the platforms' captions)


def _rows(c, text, width):
    words, rows, cur = text.split(), [], ""
    for w_ in words:
        t_ = (cur + " " + w_).strip()
        if c.text_extents(t_).x_advance > width and cur:
            rows.append(cur); cur = w_
        else:
            cur = t_
    rows.append(cur)
    return rows


def _hits(box, heads):
    x0, y0, x1, y1 = box
    for hx, hy, r in heads:
        if x0 < hx + r * 0.9 and x1 > hx - r * 0.9 and y0 < hy + r * 1.15 and y1 > hy - r:
            return True
    return False


def speech(c, k, text, head, others, mono=False, size=30, taken=()):
    """A canon speech bubble (episode 9's): white, rough-edged, Lilita One (the robot in mono caps). head (x, y, r) on
    the canvas or None (off screen: no tail). Placed just above the speaker if it fits, else beside, else below;
    never over a face or another bubble; inside the safe area."""
    face = kit.MONO if mono else kit.FONT
    c.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    rows = _rows(c, text, 360)
    ws = [c.text_extents(r_).x_advance for r_ in rows]
    lh = size * 1.14
    bw, bh = max(ws) + 44, len(rows) * lh + 26
    on = head is not None and 0 <= head[0] <= 540 and 60 <= head[1] <= 960
    heads = [h for h in others if 0 <= h[0] <= 540]
    if on:
        heads.append(head)
    L, T, R, B = SAFE

    def free(bx, by):
        box = (bx, by, bx + bw, by + bh)
        if _hits(box, heads):
            return False
        return not any(bx < q[2] and bx + bw > q[0] and by < q[3] and by + bh > q[1] for q in list(taken) + list(sb.AVOID))

    place = None
    if on:
        hx, hy, r = head
        side = 1 if hx < 270 else -1
        others_on = [h for h in others if 0 <= h[0] <= 540 and 0 <= h[1] <= 960]
        def clear(sd):                                     # how far a tip on side sd is from anyone else's face
            tx_, ty_ = hx + sd * (r * 0.95 + 8), hy + r * 0.35
            if not (8 <= tx_ <= 532):
                return -1
            return min([((tx_ - ox) ** 2 + (ty_ - oy) ** 2) ** 0.5 - orr for ox, oy, orr in others_on] or [999])
        side = max((side, -side), key=clear)
        top_tip = clear(side) < r * 0.4                    # both sides crowded or off the frame: the tail comes down
                                                           # onto the top of the speaker's head instead
        bx = max(L, min(R - bw, hx + side * r * 0.9 - bw / 2))
        xs = [bx] + [max(L, min(R - bw, bx + d_)) for d_ in (-40, 40, -80, 80, -120, 120, -160, 160, -220, 220)]
        for by in range(int(hy - r - bh - 30), T + 7, -8):                          # just above, then higher
            for bx_ in xs:                                                          # ... sliding sideways if needed
                if free(bx_, by):
                    place = (bx_, by); break
            if place:
                break
        if place is None:                                                           # beside, at head height
            for bx_ in (hx + r + 20, hx - r - 20 - bw):
                bx_ = max(L, min(R - bw, bx_))
                by = max(T + 8, min(B - bh, hy - r * 0.8))
                if free(bx_, by):
                    place = (bx_, by); break
        if place is None:                                                           # below
            for by in range(int(hy + r * 1.3 + 24), int(B - bh), 8):
                if free(bx, by):
                    place = (bx, by); break
    if place is None:                                                               # off screen: at the frame's edge on
        ax = R - bw if head is None else (L if head[0] < 0 else R - bw if head[0] > 540 else head[0] - bw / 2)   # their side,
        bx = max(L, min(R - bw, ax))                                                # in the top band
        for by in range(T + 8, 380, 8):
            if free(bx, by):
                place = (bx, by); break
        if place is None:
            place = (bx, T + 8)
    bx, by = place
    tail = None
    if on:
        hx, hy, r = head
        tip = (hx + side * (r * 0.95 + 8), hy + r * 0.35)                             # beside the mouth, outside the head
        if top_tip:
            tip = (hx, hy - r - 8)
        if bx - 8 <= tip[0] <= bx + bw + 8 and by - 8 <= tip[1] <= by + bh + 8:       # the tip inside the bubble: move it off
            if side > 0:
                bx = min(R - bw, tip[0] + 44)
            else:
                bx = max(L, tip[0] - 44 - bw)
            if bx - 8 <= tip[0] <= bx + bw + 8:                                       # no room beside: above it then
                by = max(T + 8, tip[1] - r * 1.6 - bh)
        if tip[1] > by + bh:                                                         # the speaker below
            cx = max(bx + 30, min(bx + bw - 30, tip[0]))
            tail = [(cx - 13, by + bh - 3), tip, (cx + 13, by + bh - 3)]
        elif tip[1] < by:
            cx = max(bx + 30, min(bx + bw - 30, tip[0]))
            tail = [(cx - 13, by + 3), tip, (cx + 13, by + 3)]
        else:
            ex = bx + 3 if tip[0] < bx else bx + bw - 3
            yy = max(by + 16, min(by + bh - 16, tip[1]))
            tail = [(ex, yy - 11), tip, (ex, yy + 11)]
        kit.cut(k, tail, (1, 1, 1))
    kit.cut(k, kit.rough_rect_pts(k, bx, by, bw, bh, 900 + len(text), j=1.6), (1, 1, 1))
    if tail:
        c.set_source_rgb(1, 1, 1); c.move_to(*tail[0]); c.line_to(*tail[1]); c.line_to(*tail[2]); c.close_path(); c.fill()
    c.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if mono else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size); c.set_source_rgb(*INK)
    for i, (r_, w_) in enumerate(zip(rows, ws)):
        c.move_to(bx + (bw - w_) / 2, by + 13 + lh * (i + 0.80)); c.show_text(r_)
    return bx, by, bx + bw, by + bh


def say(c, k, who, text, heads):
    names = SPEAKER.get(who, [])
    if len(names) == 2:                                    # both of them: one "Eww." each
        taken = []
        for n in names:
            others = [h for m, h in heads.items() if m != n]
            taken.append(speech(c, k, text, heads.get(n), others, size=30, taken=taken))
        return
    n = names[0] if names else None
    others = [h for m, h in heads.items() if m != n]
    mono = who == "ROBOT"
    speech(c, k, text.upper() if mono else text, heads.get(n), others, mono=mono, size=24 if mono else 30)


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
                sb.bg(c)
                sb.HEADS.clear(); sb.AVOID.clear()
                with sb._norm(record_only=True):
                    fn(k)
                if cap:
                    key = "1.2" if shot == "1.3" else LINE_OF[shot]
                    m = TAKES[key]
                    if BUBBLES[0]:
                        say(c, k, m["who"], m["text"], dict(sb.HEADS))
                    else:
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


def slurp(d=0.42, seed=3):
    """Wet: band-passed noise, fluttering, with a falling suck at the end."""
    r = np.random.default_rng(seed)
    n = int(d * SR); t = np.arange(n) / SR
    x = r.standard_normal(n)
    y = np.zeros(n); f0 = 900.0
    for i in range(1, n):                                  # a one-pole low-pass that closes as it goes
        a_ = min(0.6, 2 * np.pi * (f0 * (1 - 0.6 * i / n)) / SR)
        y[i] = y[i - 1] + a_ * (x[i] - y[i - 1])
    env = np.sin(np.pi * t / d) ** 0.7 * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t))
    suck = 0.5 * np.sin(2 * np.pi * np.cumsum(np.linspace(520, 160, n)) / SR) * np.clip((t - d * 0.6) / (d * 0.4), 0, 1)
    out = y * env + suck * np.sin(np.pi * t / d)
    return out / np.abs(out).max()


def squeak(d=0.22):
    t = np.arange(int(d * SR)) / SR
    f = 1500 + 400 * np.sin(2 * np.pi * 9 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2


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
        (at["6.1b"] if "6.1" not in at else at["6.1"] + 0.4, sx.whoosh(0.08), 0.45), (at["6.2a"] + 0.3, bm.chime([1760, 2349], 0.07, 0.3), 0.14),
        (at["8.2"] + 0.2, buzz(0.35) * 0.4, 0.4), (at["9.1"] + 0.3, bm.chime([1047, 1319, 1568], 0.09, 0.7), 0.20),
    ]
    for t, a, g in fx:
        _at(m, a, t, g)
    for i in range(9):                                     # the robot's keys
        _at(m, sx.thunk(0.03, 1400), at["9.2"] + 0.9 + i * 0.09, 0.08)
    _at(m, sx.whoosh(0.05), at["9.3"] + 0.15, 0.25)                   # the plaster flutters down
    _at(m, sx.whoosh(0.08)[::-1].copy(), at["5.2c"], 0.35)              # the rewind zip into the memory
    _at(m, slurp(), at["7.3"] + 0.05, 0.35)                            # the lick
    _at(m, squeak(), at["7.4"] + 0.05, 0.10)                           # the scrub, twice
    _at(m, squeak(), at["7.4"] + 0.30, 0.10)
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
                    "-vf", "fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-color_range", "tv",
                    "-c:a", "aac", "-b:a", "192k", "-t", "%.3f" % total, "-movflags", "+faststart", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
