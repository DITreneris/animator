"""Automatic checks for "The Best Candidate" (the storyboard bc_sb.py, and the animation through bc_anim.py), by the
series' rules for bubbles (docs/lessons.md). v2: every tail is judged on rendered pixels.

v1 compared a tail's tip with the head numbers the tail had been drawn from, so a wrong number passed itself: tails
on Sofia's hair, on Mom's hat, on a collar and in the air above Don's scalp all went through (animation v2). Now
nothing is taken from typed head sizes. A frame is drawn several times at 540 x 960 and the drawings are compared:
  with / without its bubbles          what the bubbles cover
  without the speaker                 the speaker's silhouette, as the frame shows it
  the speaker's mouth open / shut     where the mouth is
  everybody's skin in a marker colour where skin is (faces, ears, hands), as against hair, hats and cloth

  safe zone   a bubble's box stays out of the top 10 %, the bottom 15 % and the right 12 % (and 20 px off the left)
  text        22 px or more
  speaker     at most one spoken bubble in a frame; on the board the speaker's mouth is open
  mouth       the speaker's mouth is in the frame
  side tail   (beside the face) the tip is level with the mouth, touches the speaker, and from the tip to the mouth
              there is skin: not hair, a hat, a collar or a shoulder; the box is level with the mouth; no more than
              26 px of the tail crosses the wall (it may run on over the speaker's own hair to the cheek)
  top tail    (above the head) the tip touches the speaker over the mouth, with no gap; on a person it lands on bare
              skin (so only Don's scalp can take one); the robot's lands on its antenna
  skin        no bubble pixel on anybody's skin (faces, ears and hands), but for the tip of a tail on its cheek
  signs       no bubble pixel on the poster, the notice, the monitor, the sign or the nameplate
  overlap     bubbles do not overlap each other
  cropping    every sign is whole in the frame or absent from it; the speaker's face is whole in the frame
Usage: python3 qa_bc.py [shot ids ...]      exit code 1 if anything fails, or if the self-test misses a planted fault"""
import math
import sys
import cairo
import numpy as np
import bc_sb as B

W, H = 540, 960
TOL = 3


def render(shot, bubbles, who=None, mode=None):
    B.BUBBLES = bubbles
    B.PROBE.update(who=who, mode=mode)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    try:
        B.frame(cairo.Context(surf), 0, 0, W, shot[4])
    finally:
        B.BUBBLES = True
        B.PROBE.update(who=None, mode=None)
    surf.flush()
    qa = {k: list(v) for k, v in B.QA.items()}
    return np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4)[:, :, :3].astype(int).copy(), qa


def diff(a, b, thr):
    return np.abs(a - b).sum(axis=2) > thr


def clip(b):
    return max(0, int(b[0])), max(0, int(b[1])), min(W, int(b[2] + 1)), min(H, int(b[3] + 1))


def at(m, x, y, r=1):
    """Is any pixel of mask m set within r of (x, y)?"""
    x, y = int(round(x)), int(round(y))
    return bool(m[max(0, y - r):min(H, y + r + 1), max(0, x - r):min(W, x + r + 1)].any())


def tail_checks(u, t, sil, mo, skin, out):
    tx, ty = u["tip"]
    ys, xs = np.nonzero(mo)
    if not len(xs):
        out.append("%s the speaker's mouth is not in the frame" % t)
        return
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    bx0, by0, bx1, by1 = u["box"]
    if u["form"] in ("R", "L"):
        sd = 1 if u["form"] == "R" else -1
        if not (y0 - 3 <= ty <= y1 + 3):
            out.append("%s tail not level with the mouth (tip %d, mouth %d-%d)" % (t, ty, y0, y1))
        if not (by0 - 2 <= cy <= by1 + 2):
            out.append("%s box not level with the mouth (mouth %d, box %d-%d)" % (t, cy, by0, by1))
        if (sd > 0 and tx <= x1) or (sd < 0 and tx >= x0):
            out.append("%s tail runs onto the mouth" % t)
            return
        gap = next((d for d in range(0, 40) if at(sil, tx - sd * d, ty)), None)      # walking in from the tip
        if gap is None or gap > 4:
            out.append("%s tail stops short of the speaker (%s)" % (t, "nobody within 40 px" if gap is None else
                                                                    "a %d px gap" % gap))
            return
        first = next((d for d in range(gap, gap + 60) if at(skin, tx - sd * d, ty)), None)
        if first is None or first - gap > 12:
            out.append("%s tail ends on hair, a hat or cloth, not on the cheek (%s)" %
                       (t, "no skin within 60 px" if first is None else "skin is %d px further in" % (first - gap)))
            return
        end = (x1 if sd > 0 else x0)
        n = int(abs(tx - sd * first - end))
        if n > 4:
            on = sum(at(skin, tx - sd * (first + i), ty) or at(mo, tx - sd * (first + i), ty) for i in range(n))
            if on < 0.75 * n:
                out.append("%s between the tail and the mouth is not cheek (%d of %d px are skin)" % (t, on, n))
        bxm, bym = u["base"]
        steps = max(1, int(math.hypot(tx - bxm, ty - bym)))
        wall = sum(not at(sil, bxm + (tx - bxm) * i / steps, bym + (ty - bym) * i / steps, 0) for i in range(steps))
        if wall > 26:
            out.append("%s tail crosses %d px of wall" % (t, wall))
        if u["tail"] > 110:
            out.append("%s tail %d px long" % (t, u["tail"]))
    else:
        row = np.nonzero(sil[int(cy)])[0]
        half = (row.max() - row.min()) / 2.0 if len(row) else 40
        if abs(tx - cx) > 0.35 * half + 6:
            out.append("%s tail not over the speaker's mouth (off by %d px)" % (t, tx - cx))
        gap = next((d for d in range(0, 40) if at(sil, tx, ty + d)), None)
        if gap is None or gap > 3:
            out.append("%s tail stops short of the head (%s)" % (t, "nobody within 40 px" if gap is None else
                                                                 "a %d px gap" % gap))
            return
        if at(sil, tx, ty - 8, 0):
            out.append("%s tail runs into the head" % t)
        if u["who"] != "robot" and not any(at(skin, tx, ty + d, 2) for d in range(4, 22)):
            out.append("%s tail lands on hair or a hat, not on the head" % t)
        if by1 > ty - 6:
            out.append("%s box on the speaker's head" % t)
        if u["tail"] > 40:
            out.append("%s tail %d px long" % (t, u["tail"]))


def check(shot, board=False):
    """The problems in one drawing. board: a storyboard panel, where the speaker's mouth must be drawn open."""
    out = []
    a, qa = render(shot, True)
    b, _ = render(shot, False)
    mask = diff(a, b, 24)
    bubbles, labels = qa["bubbles"], qa["labels"]
    spoken = [u for u in bubbles if u["form"] != "off"]
    if len(spoken) > 1:
        out.append("%d speakers in one panel" % len(spoken))
    skin_all = diff(b, render(shot, False, "*", "skin")[0], 60) if bubbles else None
    for u in bubbles:
        x0, y0, x1, y1 = u["box"]
        t = '"%s"' % u["text"]
        if x0 < B.SAFE[0] - 0.5 or y0 < B.SAFE[1] - 0.5 or x1 > B.SAFE[2] + 0.5 or y1 > B.SAFE[3] + 0.5:
            out.append("%s outside the safe zone (%d, %d, %d, %d)" % (t, x0, y0, x1, y1))
        if u["size"] < 22:
            out.append("%s text %d px" % (t, u["size"]))
        if u["form"] == "off":
            continue
        who = u["who"]
        if board and not u["mouth"]:
            out.append("%s the speaker's mouth is shut" % t)
        sil = diff(b, render(shot, False, who, "hide")[0], 24)
        mo = diff(render(shot, False, who, "open")[0], render(shot, False, who, "shut")[0], 40)
        tail_checks(u, t, sil, mo, skin_all & sil, out)
        tx, ty = u["tip"]
        yy, xx = np.ogrid[:H, :W]
        far = (xx - tx) ** 2 + (yy - ty) ** 2 > 10 ** 2
        n = int((mask & skin_all & far).sum())
        if n > 6:
            out.append("%s covers skin: a face or a hand (%d px)" % (t, n))
        e = u["edges"]                                      # the cheeks either side of the mouth, as measured
        if e and (e[0] < -TOL or e[1] > W + TOL):
            out.append("%s the speaker's face is cut by the frame" % t)
    for i, u in enumerate(bubbles):
        for v in bubbles[i + 1:]:
            p, q = u["box"], v["box"]
            if min(p[2], q[2]) > max(p[0], q[0]) and min(p[3], q[3]) > max(p[1], q[1]):
                out.append("bubbles overlap")
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
    """Break panels on purpose: each fault must be reported, or the checks prove nothing. The last six are the
    faults animation v2 shipped with: tails that the old check, reading its own numbers, called correct."""
    def over_face(k):
        B.world(k, "don", lambda: B.panel(k, "idle", do=dict(mouth="E")))
        B.bubble(k, "First candidate.", "don", "T", 32, dy=170)

    def long_tail(k):
        B.world(k, "don", lambda: B.panel(k, "idle", do=dict(mouth="E")))
        B.bubble(k, "First", "don", "T", 30, gap=90)

    def cut_sign(k):
        B.world(k, (335, 470, 1.7), lambda: B.S.backdrop(k, 0.0, "idle"))

    def two_voices(k):
        B.world(k, "sofia_don", lambda: B.panel(k, "idle", so=dict(mouth="E"), do=dict(mouth="E")))
        B.bubble(k, "One.", "sofia", "T", 30); B.bubble(k, "Two.", "don", "T", 30)

    def shut_mouth(k):
        B.world(k, "don", lambda: B.panel(k, "idle"))
        B.bubble(k, "First candidate.", "don", "T", 32)

    def on_hair(k):                                         # 7 s, 32 s, 50 s: above Sofia's head, the tip on her hair
        B.world(k, "sofia_say", lambda: B.panel(k, "idle", so=dict(mouth="E")))
        B.bubble(k, "For whom?", "sofia", "T", 30)

    def on_hat(k):                                          # 71 s, 80 s, 86 s, 90 s: above Mom, the tip on her hat
        B._mom(k, "mom", pose="bag", face="sweet", mouth="E")
        B.bubble(k, "Good boy.", "mom", "T", 36)

    def air_gap(k):                                         # 3 s, 13 s, 26 s, 78 s: the tip stops above Don's scalp
        B.world(k, "don", lambda: B.panel(k, "idle", do=dict(mouth="E")))
        B.bubble(k, "First candidate.", "don", "T", 32, fault=(0, -9))

    def on_collar(k):                                       # 8 s, 11 s: the tip out on the small one's shoulder
        def d():
            B.S.backdrop(k, 0.0, "idle")
            B.small(k, "finger", "proud", look=(0.7, -0.1), mouth="E")
        B.world(k, "small_say", d)
        B.bubble(k, ["And", "a half."], "small", "R", 34, dy=34, fault=(40, 0))

    def on_ear(k):                                          # 21 s: the tip up by the macho's ear
        def d():
            B.S.backdrop(k, 0.0, "idle")
            B.macho(k, "pinch_near", "warm", look=(0.9, 0.3), pen=True, mouth="E")
        B.world(k, "loom_say", d)
        B.bubble(k, ["You dropped", "this."], "macho", "R", 26, dy=-44, fault=(8, -70))

    def short_of_antenna(k):                                # 73 s: the robot's tail stops short of its antenna
        def d():
            B.S.backdrop(k, 0.0, "clear")
            B.robot(k, "slap_up", talk=0.8)
            B.S.table(k, phone=None)
        B.world(k, "robot", d)
        B.bubble(k, ["Hired."], "robot", "T", 22, mono=True, fault=(0, -12))

    want = [(over_face, "covers"), (long_tail, "tail"), (cut_sign, "is cut by the frame"), (two_voices, "speakers"),
            (shut_mouth, "mouth is shut"), (on_hair, "hair or a hat"), (on_hat, "hair or a hat"),
            (air_gap, "stops short"), (on_collar, "not on the cheek"), (on_ear, "not level with the mouth"),
            (short_of_antenna, "stops short")]
    ok = 0
    for fn, word in want:
        found = any(word in line for line in check(("--", 0, 0, 0, fn), board=True))
        ok += found
        print("self-test %-16s %s" % (fn.__name__, "caught" if found else "MISSED"))
    return ok == len(want)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    good = selftest()
    want = set(args)
    bad, nb = 0, 0
    for shot in B.SHOTS:
        if want and shot[0] not in want:
            continue
        for line in check(shot, board=True):
            bad += 1
            print("%s %-16s %s" % (shot[0], shot[4].__name__, line))
        nb += len(B.QA["bubbles"])
    n = len([s for s in B.SHOTS if not want or s[0] in want])
    print("checked %d panels, %d bubbles: %s" % (n, nb, "%d problems" % bad if bad else "clean"))
    sys.exit(1 if bad or not good else 0)
