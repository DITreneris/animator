"""Animatics for "Office Noir: The Secret of a Stolen Heart" from storyboard v4 (the robot as Don's partner) (on_sb.py) and the measured voice takes
(on_voices/takes.json from sound_on.py takes). Every beat is a held storyboard panel with a slow push-in; the
lightning beat flashes and decays. The beat lengths come from the takes: a voiced beat is never shorter than its
line plus its pad (on_timing.json).
  python3 on_anim.py MOMKEY   -> on_animatic_silent.mp4 (no captions, no bubbles, no sound: the audit's test)
                                 on_animatic_voiced.mp4 (captions, voices, the jazz-noir cue, thunder, rain, stings, sfx)"""
import sys
import json
import subprocess
import numpy as np
import cairo
import on_sb as sb
import props_sheet_on as psh
import sound_on as so

FPS = 30
VO_LEAD = 0.05
OPEN = 1.47                             # v9 (18 Nov): the cold open, the black cat, before "Monday."
CAT_HISS = 0.58
LOOP = 1.0                              # v9d: he falls back asleep: bedroom -> grey -> the office of frame 0
TRIM = {6: 0.8, 10: 0.8}               # silent beats tightened for the measured cut: the eye, CCTV wide                         # a montage line starts this much before its cut (a small J-cut)


def panels(captions):
    if captions:
        return sb.build()
    keep = (psh.caption, psh.bubble, sb.say, sb.two_cards, sb.shout, sb.vo)
    psh.caption = psh.bubble = lambda *a, **k: None
    sb.say = sb.two_cards = sb.shout = sb.vo = lambda sf, *a, **k: sf
    try:
        return sb.build()
    finally:
        psh.caption, psh.bubble, sb.say, sb.two_cards, sb.shout, sb.vo = keep


def retime(P, tk, mom, open_=0.0):
    """open_: v9 cold open (seconds before the first line: the black cat). 0 = exactly as before."""
    d = [round(t1 - t0, 3) for t0, t1, *_ in P]
    for i, x in TRIM.items():
        d[i] = x
    d[0] = round(d[0] + open_, 3)
    V1 = "vo1p" if open_ else "vo1"                # v9c: a 0.4 s pause before "Unsigned." (vo1p.wav)

    def need(i, x):
        d[i] = max(d[i], round(x, 2))
    need(1, open_ + 0.25 + tk[V1] + 0.25 - d[0])
    d[2], d[3], d[4] = (round(tk["vo_drink"] + 0.05, 2), round(tk["vo_inf"] + 0.05, 2),
                        round(tk["vo_boss"] + 0.15, 2))                 # the montage runs on the voice
    d[7] = round(0.35 + tk["don_sofia"] + 0.15, 2)            # v3: his whole question over the lens POV
    need(8, 0.1 + tk["sofia"] + 0.45)
    d[9] = round(0.2 + tk["vo_partner"] + 0.25, 2)              # v4: the partner, introduced by Don's VO
    need(14, 0.1 + tk["robot"] * 0.6)                        # the robot finishes over the exit wide
    d[16] = round(0.15 + tk["robot_you"] + 0.3, 2)           # v4: "You."
    need(21, 0.3 + tk["pam"] + 0.4)
    d[26] = round(0.2 + tk["don_framed"] + 0.45 + 0.15, 2)    # "I was framed!" then 0.45 s of silence (Pam smiles)
    d[27] = round(0.1 + tk["vo6_split"], 2)                  # "Nobody tells me what to do."
    d[28] = round(tk["vo6_end"] - tk["vo6_split"], 2)        # "Whiskey. Cards. Money.": DONNIE! on the end
    d[29] = round(tk[f"mom_{mom}_donnie"] + 0.25, 2)
    need(30, 0.15 + tk[f"mom_{mom}_up"] + 0.35)
    d[33] = 1.8                                                     # v5: the slide, then the brim down
    loop = LOOP if open_ else 0.0
    d[33] = round(d[33] + loop, 3)
    st = [round(float(x), 3) for x in np.concatenate([[0], np.cumsum(d)[:-1]])]
    total = round(float(sum(d)), 3)
    cues = [
        ("sfx:thunder_soft" if open_ else "sfx:thunder", open_ + 2 / 15, 1.0),   # v9b: the rumble ducked under the first line                                    # v6: with the flash, after frame 0
        (V1, open_ + 0.25, 1.0),
        ("sfx:sting", open_ + 0.25 + (1.80 if open_ else tk["vo1"] - 0.85), 0.3 if open_ else 0.45),   # v9c: in the pause, before "Unsigned."                  # on "Unsigned." (v8: 0.8 masked the word)
        ("vo_drink", st[2] - VO_LEAD, 1.0), ("sfx:flask", st[2] + 0.05, 0.9),
        ("vo_inf", st[3] - VO_LEAD, 1.0),
        ("vo_boss", st[4] - VO_LEAD, 1.0), ("sfx:sting_low", st[4] - VO_LEAD + tk["vo_boss"] + (0.06 if open_ else -0.06), 0.7),   # v8: right after "boss"; v9: 0.12 s later still (the AAC turned "boss" into "buff")
        ("sfx:gun", st[5] + 0.3, 1.0),
        ("don_sofia", st[7] + 0.35, 1.0),
        ("sofia", st[8] + 0.1, 1.0),
        ("vo_partner", st[9] + 0.2, 1.0),
        ("sfx:snag", st[12] + 0.1, 1.0), ("sfx:pop", st[13] + 0.05, 2.4),
        ("robot", st[14] + 0.1, 1.0),
        ("robot_you", st[16] + 0.15, 1.1),
        ("sfx:dry", st[19], 1.0),
        ("pam", st[21] + 0.3, 1.0),
        ("don_framed", st[26] + 0.2, 1.0),
        ("vo6", st[27] + 0.1, 1.0),
        (f"mom_{mom}_donnie", st[29], 1.0),
        (f"mom_{mom}_up", st[30] + 0.15, 1.0),
        ("sfx:chirp", st[31] + 0.4, 1.0), ("sfx:chirp", st[31] + 0.55, 0.8),
        ("sfx:swish", st[33] + 0.3, 1.0),
    ]
    if loop:                                                           # v9d: the rain comes back with the dream
        cues += [("sfx:rain_in", round(total - loop + 0.05, 3), 1.0)]
    if open_:                                                          # v9: the cat's hiss, Don's hat
        cues += [("sfx:paws", 0.22, 0.8), ("sfx:hiss", CAT_HISS, 1.0), ("sfx:swish", CAT_HISS + 0.05, 0.7),
                 ("sfx:thump", 0.92, 0.6)]
    return {"open": open_, "loop": loop, "mom": mom, "durations": d, "starts": st, "total": total, "cues": cues,
            "labels": [p[3] for p in P]}


def frames(P, T):
    total, st, d = T["total"], T["starts"], T["durations"]
    n = int(round(total * FPS))
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    c = cairo.Context(out)
    for f in range(n):
        t = f / FPS
        i = max(k for k in range(len(st)) if st[k] <= t + 1e-9)
        u = (t - st[i]) / d[i]
        z = 1.0 + 0.035 * u if i not in (0, 1) else 1.0 + 0.05 * (t / (st[1] + d[1]))     # shot 1: one push over both
        c.save(); c.set_source_rgb(0, 0, 0); c.paint()
        c.translate(270, 480); c.scale(z, z); c.translate(-270, -480)
        c.set_source_surface(P[i][5], 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
        c.restore()
        if i == 0:                                                     # the flash: two bright frames, then it decays
            a = 0.85 if f < 2 else 0.85 * np.exp(-(t - 2 / FPS) / 0.12)
            c.set_source_rgba(1, 1, 1, a); c.paint()
        out.flush()
        yield bytes(out.get_data())


def encode(P, T, path, audio=None):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "540x960", "-r", str(FPS),
           "-i", "-"]
    if audio:
        cmd += ["-i", audio, "-af", "loudnorm=I=-16:TP=-2:LRA=11", "-c:a", "aac", "-b:a", "160k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-shortest" if audio else "-an",
            path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fr in frames(P, T):
        p.stdin.write(fr)
    p.stdin.close(); p.wait()


def main(mom):
    tk = json.load(open(f"{so.OUT}/takes.json"))
    Pv = panels(True)
    T = retime(Pv, tk, mom, OPEN)
    json.dump(T, open("on_timing.json", "w"), indent=1)
    so.mix(T, mom, "on_mix.wav")
    encode(Pv, T, "on_animatic_voiced.mp4", "on_mix.wav")
    Ps = panels(False)
    encode(Ps, T, "on_animatic_silent.mp4")
    print("total", T["total"], "s,", len(T["durations"]), "beats")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "F")              # Mom F (bf_alice + bm_lewis, aged, shouting), chosen 16 Nov
