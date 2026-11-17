"""v2, pinned. v2 (qa_ob_v1.py = v1, kept, for ob_anim_v5). Automatic checks for "The Onboarding" (the animation, ob_anim.py), by the series' render standard (uptimez/CLAUDE.md,
G3 and G5) and the bubble rules of docs/lessons.md. Every drawing that has a bubble is checked at three moments of its
line (after the pop-in, the middle, the end), drawn plain (no light, no grain) at 540 x 960.
  safe zone   the bubble's box is inside (20, 96, 475, 816): out of the title bar, the caption area and the button rail
  text        22 px or more
  faces       the box does not touch anybody's face (a disc on every face drawn in that frame, the robot's screen too)
  tail        (v2) a person's tail ends on the cheek RIGHT BESIDE THE MOUTH, on rendered pixels of the frame WITHOUT
              bubbles: at the tip there is the speaker's skin, and walking on from the tip toward the middle of the
              face the mouth begins within 0.40 of the face's radius (v1 only asked for skin, so a tail that stopped at
              the edge of the face, on Sofia's earring, passed). The robot has no mouth: its tail must end on it, not
              on the wall. A tail drawn from a wrong number fails: nothing here trusts typed head sizes
  badges      (v2) every third of a second and at every bubble: a name badge (SOFÍA, DON, PAM, HR, VISITOR) that is in
              the frame is whole or not seen at all. Each drawing is rendered twice, the second time with the names in
              magenta: the pixels that differ are the letters actually seen. Under 5 % seen: hidden, fine. Otherwise
              the name must not touch the edge of the frame, and, where it is 28 px wide or more (readable on a
              phone), 90 % of its letters must show: not under a hand, a sleeve, a prop or a bubble
  speaker     the speaker's face is whole in the frame and under the title bar
  title bar   in every third of a second of the film, no face's eye line is above y = 96 (the insert of the strand in
              3.7 shows her mouth and her hand, not her eyes: it is registered as an insert and skipped)
The self-test plants five faults (a box in the title bar, a tail that ends in the air, a box on a face, a badge half
out of the frame, a badge half under a patch of skin) and fails the run if any of them gets through.
Not checked here: Whisper on the mix (the model is not installed in this environment), the loudness and the format of
the delivered file (measured by ffmpeg after the render).
Usage: python3 qa_ob.py      exit code 1 if anything fails"""
import math
import sys
import cairo
import numpy as np
import kit
import ob_anim_v6 as A

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
            skin = anch.get(b["who"], {}).get("skin")
            if skin is None:                                # the robot: on it, not on the wall
                deep = max(8.0, 0.22 * sp_r)
                col = patch(bare, b["tip"][0] + b["inward"][0] * deep, b["tip"][1] + b["inward"][1] * deep)
                if col is None:
                    out.append("tail: it ends outside the frame")
                elif float(np.abs(col - np.array(kit.WALL)).max()) < 0.05:
                    out.append("tail: it ends on the wall, not on %s" % b["who"])
            else:
                miss = beside_mouth(bare, b["tip"], b["inward"], sp_r, np.array(skin))
                if miss:
                    out.append("tail: %s (%s)" % (miss, b["who"]))
        sp = [f for f in faces if f[0] == b["who"]]
        if sp and b["form"] != "off":
            _, (cx, cy), r = sp[0]
            if cx - r < -2 or cx + r > W + 2 or cy - r < A.SAFE[1] - 2 or cy + r > H + 2:
                out.append("speaker: %s's face is not whole in the frame, under the title bar" % b["who"])
    return out


def beside_mouth(bare, tip, inward, r, skin):
    """None if the tail ends on skin right beside the mouth; else what is wrong. Rendered pixels only."""
    is_skin = lambda x, y: (lambda c: c is not None and float(np.abs(c - skin).max()) <= SKIN_TOL)(patch(bare, x, y, 1))
    if patch(bare, tip[0], tip[1], 1) is None:
        return "it ends outside the frame"
    if not is_skin(tip[0] + inward[0] * 3, tip[1] + inward[1] * 3):
        c = patch(bare, tip[0] + inward[0] * 3, tip[1] + inward[1] * 3, 1)
        return "no skin where it ends (%.2f %.2f %.2f)" % tuple(c)
    band = max(2, int(round(0.10 * r)))                     # the mouth may sit a little above or below the tip's row
    d = 3.0
    while d <= 0.40 * r + 1e-6:
        x, y = tip[0] + inward[0] * d, tip[1] + inward[1] * d
        if any(not is_skin(x - inward[1] * o, y + inward[0] * o) for o in range(-band, band + 1, 2)) and \
           any(not is_skin(x + inward[0] * 2 - inward[1] * o, y + inward[1] * 2 + inward[0] * o) for o in range(-band, band + 1, 2)):
            return None
        d += 1.0
    return "the mouth is more than 0.40 of the face from where it ends"


READ = 28                                                   # a name narrower than this is not read at phone size


def badge_misses(marks, seen):
    """The badges of one drawing. marks: what ob_anim noted for each name (its box, its letters as a mask); seen: a
    frame-sized mask of the pixels where a name's letters are actually visible. Whole, or not there at all."""
    out = []
    for m in marks:
        xs, ys = [q[0] for q in m["quad"]], [q[1] for q in m["quad"]]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x1 < 0 or x0 > W or y1 < 0 or y0 > H:
            continue                                        # not in this frame at all
        mask = m["mask"]; mx, my = m["x0"], m["y0"]
        h, w = mask.shape
        vis = np.zeros_like(mask)
        ax0, ay0, ax1, ay1 = max(0, mx), max(0, my), min(W, mx + w), min(H, my + h)
        if ax1 > ax0 and ay1 > ay0:
            vis[ay0 - my:ay1 - my, ax0 - mx:ax1 - mx] = seen[ay0:ay1, ax0:ax1]
        share = float((vis & mask).sum()) / max(1, int(mask.sum()))
        if share <= 0.05:
            continue                                        # hidden altogether: not a cropped word
        if x0 < 3 or x1 > W - 3 or y0 < 3 or y1 > H - 3:
            out.append("badge: %s is cut by the edge of the frame" % m["name"])
        elif x1 - x0 >= READ and share < 0.90:
            out.append("badge: %s is partly covered (%d %% of its letters show)" % (m["name"], round(share * 100)))
    return out


def badge_frames(t):
    """(marks, seen) for film time t: the same drawing rendered twice, the second time with the names in magenta."""
    px, _, _, _ = render(t, True)
    A.OPT["mark"] = True
    try:
        px2, _, _, _ = render(t, True)
        marks = [dict(m) for m in A.QA["badges"]]
    finally:
        A.OPT["mark"] = False
    return marks, np.abs(px2 - px).max(axis=2) > 0.2


def badges_at(t):
    return badge_misses(*badge_frames(t))


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
    marks, seen = badge_frames(t)
    big = [m for m in marks if max(q[0] for q in m["quad"]) - min(q[0] for q in m["quad"]) >= READ]
    if not big or badge_misses(big, seen):
        missed.append("badge (the test frame has no clean badge to plant a fault on)")
    else:
        m = big[0]
        dx = int(W - 12 - min(q[0] for q in m["quad"]))      # push it half out of the right edge
        moved = dict(m, quad=[(x + dx, y) for x, y in m["quad"]], x0=m["x0"] + dx)
        seen2 = np.zeros_like(seen); seen2[:, dx:] = seen[:, :W - dx]
        if not badge_misses([moved], seen2):
            missed.append("badge out of the frame")
        seen3 = seen.copy(); seen3[:, :int(sum(q[0] for q in m["quad"]) / 4)] = False      # a hand over its first half
        if not badge_misses([m], seen3):
            missed.append("badge covered")
    return missed


def title_bar():
    out, t, seen = [], 0.0, set()
    while t < A.T["total"] - 1e-6:
        for miss in badges_at(t):
            key = (A.shot_at(t)["shot"], miss)
            if key not in seen:
                seen.add(key); out.append("%6.2f s  %-5s %s" % (t, key[0], miss))
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
        print("self-test: the five planted faults were caught")
    n = 0
    for shot, t in line_times():
        n += 1
        for miss in check(t) + badges_at(t):
            bad += 1
            print("%6.2f s  %-5s %s" % (t, shot, miss))
    for miss in title_bar():
        bad += 1
        print(miss)
    print("checked %d drawings with bubbles and a frame every 1/3 s of %.1f s (bubbles, tails, faces, badges): %s" % (
        n, A.T["total"], "%d problems" % bad if bad else "clean"))
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
