"""Secret Santa: the voice takes (Kokoro, the series cast), made once and kept in ss_takes/ so the timing, the mix
and the visemes all use the same audio. Pam bf_emma (Christmas audition A), her opening line a soft breathy whisper
(sound_iwry.whisper2); Sofia af_bella; Don am_onyx, his reflection line a slower, warmer purr; the robot voice B
(am_echo, robotized), "You're welcome." a touch slower and warmer. Writes ss_takes/NN.npy and ss_takes_v1.json:
[{id, who, text, panel, at (storyboard seconds into the panel), dur}]."""
import json
import numpy as np
import sound_iwry as si
import sound_xmas as sx

SR = si.SR
LINES = [  # id, who, text (spelled for the voice), panel, at, how
    (1, "PAM", "Sofia... do you think I could pull off nude?", "s1", 1.35, "whisper"),
    (2, "SOF", "On your lips, Pam.", "s1", 2.6, ("af_bella", 1.0)),
    (3, "PAM", "Would Don notice?", "s2b", 0.1, "pam"),
    (4, "SOF", "Don notices mirrors.", "s2b", 1.15, ("af_bella", 1.0)),
    (5, "DON", "Secret Santa! H.R. approved!", "s3b", 0.3, ("am_onyx", 1.05)),
    (6, "DON", "Agent Santa. Licensed to gift.", "s4b", 1.25, "purr"),
    (7, "PAM", "Don... what would you like Santa to bring?", "s5b", 0.15, "pam"),
    (8, "DON", "Sofia.", "s6b", 0.15, ("am_onyx", 0.95)),
    (9, "DON", "Or a full-length mirror.", "s6b", 1.5, ("am_onyx", 1.0)),
    (10, "ROB", "Personal data detected. Anonymizing.", "s10b", 0.5, "robot"),
    (11, "PAM", "Will Don get it?", "s15b", 1.0, "pam"),
    (12, "ROB", "He won't.", "s15b", 2.4, "robot"),
    (13, "ROB", "You're welcome.", "s15b", 3.3, "warm"),
]


def make(txt, how):
    if how == "whisper":
        return si.whisper2(sx.pam_line(txt, "A"))
    if how == "pam":
        return sx.pam_line(txt, "A")
    if how == "purr":
        a = sx.best_take(txt, "am_onyx", 0.95, "en-us")
        a = si.lp(a, 2) * 0.6 + a * 0.4                       # warmer: a little of the top taken off
        return a / np.sqrt(np.mean(a ** 2)) * 0.11
    if how == "robot":
        return si.robot_line(txt, "B", "normal")
    if how == "warm":
        v, sp, semis, ring, comb, _ = si.ROBOTS["B"]
        a = si.robotize(si.say(txt, v, sp * 0.92), semis, ring * 0.6, comb * 0.7)
        return a / np.sqrt(np.mean(a ** 2)) * 0.11
    v, sp = how
    return sx.best_take(txt, v, sp, "en-us")


if __name__ == "__main__":
    meta = []
    for i, who, txt, panel, at, how in LINES:
        a = make(txt, how)
        np.save("ss_takes/%02d.npy" % i, a)
        meta.append({"id": i, "who": who, "text": txt, "panel": panel, "at": at, "dur": round(len(a) / SR, 3)})
        print(f"{i:2d} {who} {txt:46s} {len(a) / SR:5.2f} s")
    json.dump(meta, open("ss_takes_v1.json", "w"), indent=1)
