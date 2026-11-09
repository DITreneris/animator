"""Shared timing for both animatics. Frames at 30 fps, 450 per loop."""
FPS = 30
N = 450

# measured voice lengths (s) from voices.py
VOICE = {"L1": 0.92, "L2": 1.02, "L3": 0.63, "L4": 1.30, "L5": 1.23, "L6": 1.01}

SHARED = {
    "ding1": 45, "ding2": 120, "ding3": 180,
    "L1": 0.067, "L2": 2.05, "L3": 3.30, "L4": 4.50, "L5": 6.40,
}

VARIANTS = {
    # A: slow reveal (4.3 s glow -> punchline)
    "A": {"glow": 240, "hatch": 285, "thunk": 300, "turn": 330, "cu": 360,
          "L6": 12.3, "pounce": 420, "music_back": 14.0},
    # B: fast reveal (3.0 s glow -> punchline)
    "B": {"glow": 240, "hatch": 270, "thunk": 285, "turn": 300, "cu": 330,
          "L6": 11.3, "pounce": 381, "music_back": 12.5},
}


def bubbles(v):
    """(start_frame, end_frame, speaker, text). Bubbles vanish 0.2 s after the line,
    except L1 (visible from frame 0) and L6 (held until the pounce)."""
    T = VARIANTS[v]
    def end(key, start):
        return int(round((start + VOICE[key] + 0.2) * FPS))
    return [
        (0, end("L1", SHARED["L1"]), "SAVI", "Your file is saved."),
        (int(SHARED["L2"] * FPS), end("L2", SHARED["L2"]), "USER", "Cool. Where is it?"),
        (int(SHARED["L3"] * FPS), end("L3", SHARED["L3"]), "SAVI", "Locally."),
        (int(SHARED["L4"] * FPS), end("L4", SHARED["L4"]), "DEAD", "Not in Downloads!"),
        (int(SHARED["L5"] * FPS), end("L5", SHARED["L5"]), "PM", "Not on ANY of ours!"),
        (int(T["L6"] * FPS), T["pounce"] - 1, "SAVI", "...On MY machine."),
    ]
