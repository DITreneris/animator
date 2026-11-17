"""v1, pinned. Automatic checks for "The Onboarding" (the animation, ob_anim.py), by the series' render standard (uptimez/CLAUDE.md,
G3 and G5) and the bubble rules of docs/lessons.md. Every drawing that has a bubble is checked at three moments of its
line (after the pop-in, the middle, the end), drawn plain (no light, no grain) at 540 x 960.
  safe zone   the bubble's box is inside (20, 96, 475, 816): out of the title bar, the caption area and the button rail
  text        22 px or more
  faces       the box does not touch anybody's face (a disc on every face drawn in that frame, the robot's screen too)
  tail        where the tail ends there is the speaker, on rendered pixels: six pixels on from the tip, toward the
              face (deeper on a larger face: past the outline), the frame WITHOUT bubbles shows the speaker's skin (a person), or something that is not wall (the
              robot's antenna). A tail drawn from a wrong number therefore fails: nothing here trusts typed head sizes
  speaker     the speaker's face is whole in the frame and under the title bar
  title bar   in every third of a second of the film, no face's eye line is above y = 96 (the insert of the strand in
              3.7 shows her mouth and her hand, not her eyes: it is registered as an insert and skipped)
The self-test plants three faults (a box in the title bar, a tail that ends in the air, a box on a face) and fails
the run if any of them gets through.
Not checked here: Whisper on the mix (the model is not installed in this environment), the loudness and the format of
the delivered file (measured by ffmpeg after the render).
Usage: python3 qa_ob.py      exit code 1 if anything fails"""
import math
import sys
import cairo
import numpy as np
import kit
import ob_anim_v5 as A

W, H = 540, 960
SKIN_TOL = 0.17


def render(t, bubbles=True):
    A.OPT.update(bubbles=bubbles, plain=True)
    try:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        A.draw(cairo.Context(surf), t, W)
        surf.flush()
        px = np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4)[:, :, :3][:, :, ::-1].astype(float) / 255.0
        return px.copy(), [dict(b) for b in A.QA["bubbles"]], list(A.QA["faces"]), {k: dict(v) for k, v in A.ANCH.items()}
    finally:
        A.OPT.update(bubbles=True, plain=False)


def patch(px, x, y, r=2):
    x, y = int(round(x)), int(round(y))
    if not (r <= x < W - r and r <= y < H - r):
        return None
    return np.median(px[y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3), axis=0)


def check(t):
    """The misses of the drawing at film time t, as text lines."""
    out = []
    _, bubbles, faces, anch = render(t, True)
    if not bubbles:
        return out
    bare, _, _, _ = render(t, False)
    for b in bubbles:
        x0, y0, x1, y1 = b["box"]
        if x0 < A.SAFE[0] - 0.5 or y0 < A.SAFE[1] - 0.5 or x1 > A.SAFE[2] + 0.5 or y1 > A.SAFE[3] + 0.5:
            out.append("safe zone: box (%d, %d, %d, %d)" % (x0, y0, x1, y1))
        if b["size"] < 22:
            out.append("text: %d px" % b["size"])
        for who, (cx, cy), r in faces:
            nx, ny = max(x0, min(x1, cx)), max(y0, min(y1, cy))
            if math.hypot(cx - nx, cy - ny) < r - 1.0:
                out.append("faces: the box is on %s's face" % who)
        if b["tip"] is not None:
            sp_r = next((r for who, _, r in faces if who == b["who"]), 30.0)
            deep = max(8.0, 0.22 * sp_r)                    # past the outline, onto the cheek (or the scalp, or the screen)
            tx, ty = b["tip"][0] + b["inward"][0] * deep, b["tip"][1] + b["inward"][1] * deep
            col = patch(bare, tx, ty)
            skin = anch.get(b["who"], {}).get("skin")
            if col is None:
                out.append("tail: it ends outside the frame")
            elif skin is not None:
                if float(np.abs(col - np.array(skin)).max()) > SKIN_TOL:
                    out.append("tail: no skin of %s where it ends (%.2f %.2f %.2f)" % ((b["who"],) + tuple(col)))
            elif float(np.abs(col - np.array(kit.WALL)).max()) < 0.05:
                out.append("tail: it ends on the wall, not on %s" % b["who"])
        sp = [f for f in faces if f[0] == b["who"]]
        if sp and b["form"] != "off":
            _, (cx, cy), r = sp[0]
            if cx - r < -2 or cx + r > W + 2 or cy - r < A.SAFE[1] - 2 or cy + r > H + 2:
                out.append("speaker: %s's face is not whole in the frame, under the title bar" % b["who"])
    return out


def line_times():
    for s in A.T["shots"]:
        ln = s.get("line")
        if ln:
            n = int(round((ln["t1"] - ln["t0"]) * 12))
            for i in sorted({2, n // 2, max(2, n)}):
                yield s["shot"], ln["t0"] + i / 12.0


def self_test():
    """Each planted fault must be caught on a line that is clean without it."""
    shot, t = next((sh, t) for sh, t in line_times() if sh == "1.3")
    missed = []
    for fault, word in (("box", "safe zone"), ("tip", "tail")):
        A.OPT["fault"] = fault
        try:
            got = check(t)
        finally:
            A.OPT["fault"] = None
        if not any(g.startswith(word) for g in got):
            missed.append(fault)
    old = A.SAFE                                            # a box on a face: pull the speaker's bubble onto him
    px, bubbles, faces, anch = render(t, True)
    b = bubbles[0]
    cx, cy = [f for f in faces if f[0] == b["who"]][0][1]
    hit = max(b["box"][0], min(b["box"][2], cx)) == cx and max(b["box"][1], min(b["box"][3], cy)) == cy
    b2 = dict(b); w, h = b["box"][2] - b["box"][0], b["box"][3] - b["box"][1]
    b2["box"] = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    r = [f for f in faces if f[0] == b["who"]][0][2]
    nx, ny = max(b2["box"][0], min(b2["box"][2], cx)), max(b2["box"][1], min(b2["box"][3], cy))
    if not (math.hypot(cx - nx, cy - ny) < r - 1.0) or hit:
        missed.append("face")
    return missed


def title_bar():
    out, t = [], 0.0
    while t < A.T["total"] - 1e-6:
        _, _, faces, _ = render(t, False)
        for who, (cx, cy), r in faces:
            if who != "ROBOT" and not who.startswith("-") and cy - 0.2 * r < A.SAFE[1]:
                out.append("%6.2f s  %-5s title bar: %s's eyes are at y = %d" % (t, A.shot_at(t)["shot"], who, cy - 0.2 * r))
        t += 1 / 3.0
    return out


def main():
    bad = 0
    missed = self_test()
    if missed:
        print("SELF-TEST FAILED: these planted faults got through:", ", ".join(missed)); bad += 1
    else:
        print("self-test: the three planted faults were caught")
    n = 0
    for shot, t in line_times():
        n += 1
        for miss in check(t):
            bad += 1
            print("%6.2f s  %-5s %s" % (t, shot, miss))
    for miss in title_bar():
        bad += 1
        print(miss)
    print("checked %d drawings with bubbles and a frame every 1/3 s of %.1f s: %s" % (
        n, A.T["total"], "%d problems" % bad if bad else "clean"))
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
