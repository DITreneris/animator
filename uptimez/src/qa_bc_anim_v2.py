"""The checks as they ran on animation v2, pinned.
Automatic checks for the storyboard of "The Best Candidate" (bc_sb.py), by the series' rules for bubbles
(docs/lessons.md; the same thresholds as qa_dlx.py where it has one). Every panel is drawn twice at 540 x 960,
with and without its bubbles; the difference is what the bubbles cover.
  safe zone   a bubble's box stays out of the top 10 %, the bottom 15 % and the right 12 % (and 20 px off the left)
  text        22 px or more
  speaker     at most one spoken bubble in a panel
  tail        beside the face: the tip is at the cheek, at mouth height; above the head: the tip is just over the
              speaker's own head; either way the tail is short (40 px or less)
  faces       no bubble pixel on any face (eyes to mouth), the speaker's included
  signs       no bubble pixel on the poster, the notice, the monitor, the sign or the nameplate
  overlap     bubbles do not overlap each other
  cropping    every sign is whole in the frame or absent from it; the speaker's face is whole in the frame
Usage: python3 qa_bc.py [shot ids ...]      exit code 1 if anything fails"""
import sys
import cairo
import numpy as np
import bc_sb_anim_v2 as B

W, H = 540, 960
TOL = 3


def render(shot, bubbles):
    B.BUBBLES = bubbles
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    B.frame(cairo.Context(surf), 0, 0, W, shot[4])
    surf.flush()
    qa = {k: list(v) for k, v in B.QA.items()}
    return np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4)[:, :, :3].astype(int).copy(), qa


def clip(b):
    return max(0, int(b[0])), max(0, int(b[1])), min(W, int(b[2] + 1)), min(H, int(b[3] + 1))


def check(shot):
    out = []
    a, qa = render(shot, True)
    b, _ = render(shot, False)
    B.BUBBLES = True
    mask = np.abs(a - b).sum(axis=2) > 24
    bubbles, faces, labels = qa["bubbles"], qa["faces"], qa["labels"]
    spoken = [u for u in bubbles if u["form"] != "off"]
    if len(spoken) > 1:
        out.append("%d speakers in one panel" % len(spoken))
    for u in bubbles:
        x0, y0, x1, y1 = u["box"]
        t = '"%s"' % u["text"]
        if x0 < B.SAFE[0] - 0.5 or y0 < B.SAFE[1] - 0.5 or x1 > B.SAFE[2] + 0.5 or y1 > B.SAFE[3] + 0.5:
            out.append("%s outside the safe zone (%d, %d, %d, %d)" % (t, x0, y0, x1, y1))
        if u["size"] < 22:
            out.append("%s text %d px" % (t, u["size"]))
        if u["tail"] > 40 and u["form"] != "off":
            out.append("%s tail %d px long" % (t, u["tail"]))
        h = u["head"]
        if h:
            (mx, my), R, top = h["m"], h["R"], h["top"]
            tx, ty = u["tip"]
            if u["form"] in ("R", "L"):
                sd = 1 if u["form"] == "R" else -1
                if abs(tx - (mx + sd * R)) > 8 or abs(ty - my) > 4:
                    out.append("%s tail not at the cheek" % t)
                if not (y0 - 2 <= my <= y1 + 2):
                    out.append("%s not level with the mouth (mouth %d, box %d-%d)" % (t, my, y0, y1))
                if (sd > 0 and x0 < mx + R) or (sd < 0 and x1 > mx - R):
                    out.append("%s box over the speaker's face" % t)
            else:
                if abs(tx - mx) > 0.7 * R or not (-12 <= top - ty <= 12):
                    out.append("%s tail not over the speaker's head (off by %d, %d)" % (t, tx - mx, top - ty))
                if y1 > top - 6:
                    out.append("%s box on the speaker's head (box bottom %d, head top %d)" % (t, y1, top))
            name = u["who"]
            for n, fb in faces:
                if n == name and (fb[0] < -TOL or fb[2] > W + TOL or fb[1] < -TOL or fb[3] > H + TOL):
                    out.append("%s the speaker's face is cut by the frame" % t)
    for i, u in enumerate(bubbles):
        for v in bubbles[i + 1:]:
            p, q = u["box"], v["box"]
            if min(p[2], q[2]) > max(p[0], q[0]) and min(p[3], q[3]) > max(p[1], q[1]):
                out.append("bubbles overlap")
    for n, fb in faces:
        x0, y0, x1, y1 = clip(fb)
        if x1 > x0 and y1 > y0 and mask[y0:y1, x0:x1].sum() > 6:
            out.append("a bubble covers %s's face (%d px)" % (n, mask[y0:y1, x0:x1].sum()))
    for n, lb in labels:
        x0, y0, x1, y1 = clip(lb)
        if x1 <= x0 or y1 <= y0:
            continue                                       # not in the frame
        if lb[0] < -TOL or lb[1] < -TOL or lb[2] > W + TOL or lb[3] > H + TOL:
            out.append("the %s is cut by the frame (%d, %d, %d, %d)" % (n, lb[0], lb[1], lb[2], lb[3]))
        if mask[y0:y1, x0:x1].sum() > 6:
            out.append("a bubble covers the %s" % n)
    return out


def selftest():
    """Break four panels on purpose: each fault must be reported, or the checks prove nothing."""
    def over_face(k):
        B.world(k, "don", lambda: B.panel(k, "idle"))
        B.bubble(k, "First candidate.", "don", "T", 32, dy=170)

    def long_tail(k):
        B.world(k, "don", lambda: B.panel(k, "idle"))
        B.bubble(k, "First", "don", "T", 30, gap=90)

    def cut_sign(k):
        B.world(k, (335, 470, 1.7), lambda: B.S.backdrop(k, 0.0, "idle"))

    def two_voices(k):
        B.world(k, "sofia_don", lambda: B.panel(k, "idle"))
        B.bubble(k, "One.", "sofia", "T", 30); B.bubble(k, "Two.", "don", "T", 30)

    want = [(over_face, "covers don's face"), (long_tail, "tail"), (cut_sign, "is cut by the frame"), (two_voices, "speakers")]
    ok = 0
    for fn, word in want:
        found = any(word in line for line in check(("--", 0, 0, 0, fn)))
        ok += found
        print("self-test %-10s %s" % (fn.__name__, "caught" if found else "MISSED"))
    return ok == len(want)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    good = selftest()
    want = set(args)
    bad, nb = 0, 0
    for shot in B.SHOTS:
        if want and shot[0] not in want:
            continue
        for line in check(shot):
            bad += 1
            print("%s %-16s %s" % (shot[0], shot[4].__name__, line))
        nb += len(B.QA["bubbles"])
    n = len([s for s in B.SHOTS if not want or s[0] in want])
    print("checked %d panels, %d bubbles: %s" % (n, nb, "%d problems" % bad if bad else "clean"))
    sys.exit(1 if bad or not good else 0)
