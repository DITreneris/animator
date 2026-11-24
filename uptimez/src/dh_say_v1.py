"""Daddy's Home speech bubbles, the way The Best Candidate drew them (bc_sb.bubble, approved in Tomas's reviews), on
this episode's rigs. Replaces the bubble of animation v2 (dh_speech.py), which is no longer used.

What comes from bc_sb.bubble, unchanged:
- form "R" / "L": the box beside the face, level with the mouth, on clear wall; a short straight tail (a triangle
  22 px at the box) whose tip lands on the cheek's outline at mouth height, 1.5 px over it;
- form "T": the box just above the speaker and the tail down onto the crown: only the robot (its antenna) and Don's
  bare scalp;
- hair beside the cheek: the box stands clear of the hair and the tail runs over it to the cheek;
- the box is kept off ears and hands in its own rows, inside the safe area, and held still through its shot (only the
  tail follows the head);
- the tail is drawn as its own triangle, filled after the box's outline, so nothing is cut out where it meets the box.
What is this episode's own:
- the measuring (mouth, cheek, crown) uses the rigs redrawn alone at the moment they are drawn (dh_speech's log);
- the box keeps the episode's look (white rounded box, Father's dark red, the font at 31 px);
- the safe area is the episode's: under the top bar (y 96), out of the bottom quarter (y 720) and the right rail.
A line whose speaker has no clear wall beside the face and no bare top is listed in NEEDS_FRAME (it needs a new framing,
lessons.md 358) and, until it gets one, drawn with the side that fits best and flagged by the check.

install() is opt-in."""
import math
import numpy as np
import kit
import dh_speech as SP

INK = (0.13, 0.11, 0.12)
SAFE = (20, 96, 470, 716)                  # x0, y0, x1, y1 for a box (top bar; bottom quarter; the right rail's edge)
LOCK = {}                                  # (text, shot key) -> (bx, by, form, side): the box held still through its shot
LAST = SP.LAST
NEEDS_FRAME = {}                           # text -> why no side bubble or overhead fits
# Lines placed by hand, as The Best Candidate's SAY table did (form, dx, dy, maxw); measured on the frames, 22 Nov
SAY = {
    "Find. My money.": dict(form="L", maxw=110),                 # on the left, clear of his ear, where "Good." sits
    "Of course.": dict(form="R", dx=40),                         # level with his mouth, right of the headset, over his sleeve (not skin)
    "Make it green.": dict(form="T", maxw=130, dx=22),           # over his bare scalp, clear of the screen on his left
    "Donnie.": dict(form="L", maxw=140),                         # the booth: left of his chin, off the neon sign
    "My men go in first.": dict(form="L", maxw=140),
    "Today.": dict(form="L", maxw=140),
}
CARD = dict(SP.CARD)
CARD.pop("I didn't steal anything!", None)  # a card is only for a speaker off the frame (lessons 551)


def install():
    SP.install()                           # the rigs' log, the redraw-alone, the tag keep-out
    import dh_anim1 as A, dh_anim2, dh_anim3
    A.bubble = bubble
    dh_anim3.SPEECH_SHIFT[0] = False       # dh_speech's step back for Mom is not used
    for m in (dh_anim2, dh_anim3):
        m.SPEECH_SHIFT[0] = True
    dh_anim2.SHIFT2["1.3"] = (72, 0)       # Sofía's "Is he coming alone?": wall on her right; the shredder's sign wholly out
    dh_anim3.SHIFT3["3.5"] = (-8, 0)       # "Green is all he sees.": wall on his left
    dh_anim2.SHIFT2["2.2"] = (-16, 0)      # "I didn't steal anything!": wall on his left, clear of his raised hands
    dh_anim3.SHIFT3["4.3"] = (-75, 0)      # "Different chair.": wall on Mom's left
    import dh_anim7
    dh_anim7.sc.SHIFT["9.4'"] = (-60, 0)   # Father's "Approved.": wall on his left


def _lines(c, text, maxw):
    return SP._lines(c, text, maxw)


def measure(rec):
    """bc_sb.measure on a logged rig: the mouth, the cheek edge either side at mouth height (the last skin walking out
    from the mouth, stepping over a line or a string of pearls), the crown over the mouth, and how far the figure runs
    on beside the cheek (hair)."""
    if "meas" in rec:
        return rec["meas"]
    fc = SP.read_booth(rec) if rec.get("kind") == "booth" else SP.read_face(rec)
    N, S = fc["N"], fc["S"]
    mx, my = fc["mouth"]; mw = fc["mw"]; z = fc["s"]
    cx, cy = int(round(mx)), int(round(my))
    gmax = int(5 * z + 2)
    edge = {}
    for sd in (-1, 1):
        ends = []
        for row in range(cy - 2, cy + 3):
            x = last = int(round(mx + sd * mw))
            gap = 0
            while 0 < x + sd < 539 and gap <= gmax:
                x += sd
                if S[row, x]:
                    last, gap = x, 0
                else:
                    gap += 1
            ends.append(last)
        edge[sd] = sorted(ends)[len(ends) // 2]
    band = int(round(16 * z))
    cols = N[:cy, max(0, cx - band):cx + band + 1]
    rows = np.nonzero(cols.any(axis=1))[0]
    ty = int(rows.min()) if len(rows) else cy
    tx = float(np.nonzero(cols[ty])[0].mean()) + max(0, cx - band) if len(rows) else cx
    reach = {}
    for sd in (-1, 1):
        x = edge[sd]
        while 0 < x + sd < 539 and N[cy - 2:cy + 3, x + sd].any():
            x += sd
        reach[sd] = x
    bald = False
    for off in (0, -0.15, 0.15, -0.3, 0.3):                 # a bare-scalp column, clear of a curl or the headset above
        x = int(mx + off * fc["r"])
        ks = np.nonzero(S[:cy, x])[0] if 0 <= x < 540 else []
        if len(ks) and not N[max(0, ks.min() - 30):max(0, ks.min() - 6), max(0, x - 8):x + 9].any() \
                and S[ks.min() + 2:ks.min() + 10, x - 3:x + 4].mean() > 0.6:
            tx, ty, bald = float(x), int(ks.min()) - 3, True
            break
    out = dict(m=(mx, my), eL=edge[-1], eR=edge[1], top=(tx, ty), sL=reach[-1], sR=reach[1], z=z, N=N, S=S, r=fc["r"],
               bald=bald, fc=fc)
    rec["meas"] = out
    return out


def _free(M, bx, by, bw, bh, pad=6):
    y0, y1, x0, x1 = int(max(0, by - pad)), int(min(960, by + bh + pad)), int(max(0, bx - pad)), int(min(540, bx + bw + pad))
    return not M[y0:y1, x0:x1].any()


def _inside(bx, by, bw, bh):
    return bx >= SAFE[0] and by >= SAFE[1] and bx + bw <= SAFE[2] + (70 if by + bh < 380 else 0) and by + bh <= SAFE[3]


def _place(ms, form, bw, bh, gap=20, hair=False):
    (mx, my), eL, eR, top = ms["m"], ms["eL"], ms["eR"], ms["top"]
    oL, oR = (ms["sL"] - 4 + gap, ms["sR"] + 4 - gap) if hair else (eL, eR)
    if form in ("R", "L"):
        sd = 1 if form == "R" else -1
        bx = oR + gap if sd > 0 else oL - gap - bw
        by = my - bh / 2
    else:
        bx, by = top[0] - bw / 2, top[1] - gap - bh
    by = max(SAFE[1], min(SAFE[3] - bh, by))
    if form in ("R", "L"):                                  # an ear or a hand beside the box's own rows: stand clear
        r0, r1 = int(by) - 4, int(by + bh) + 4
        e = int(eR if sd > 0 else eL)
        span = ms["N"][max(0, r0):r1, e:e + int(34 * ms["z"])] if sd > 0 else \
            ms["N"][max(0, r0):r1, max(0, e - int(34 * ms["z"])):e + 1][:, ::-1]
        cols = np.nonzero(span.any(axis=0))[0]
        if len(cols) and not hair:
            far = e + sd * int(cols.max())
            bx = max(bx, far + 7) if sd > 0 else min(bx, far - 7 - bw)
    bx = max(SAFE[0], min(SAFE[2] + (70 if by + bh < 380 else 0) - bw, bx))
    return bx, by


def _tail(ms, form, bx, by, bw, bh):
    (mx, my), eL, eR, top = ms["m"], ms["eL"], ms["eR"], ms["top"]
    if form in ("R", "L"):
        sd = 1 if form == "R" else -1
        ex = bx + 3 if sd > 0 else bx + bw - 3
        ty = max(by + 15, min(by + bh - 15, my))
        tip = ((eR if sd > 0 else eL) + sd * 1.5, my)
        return [(ex, ty - 11), tip, (ex, ty + 11)], tip
    rx = max(bx + 28, min(bx + bw - 28, top[0]))
    tip = (top[0], top[1] + 1.5)
    return [(rx - 12, by + bh - 3), tip, (rx + 12, by + bh - 3)], tip


def _wall(ms, tail, tip):
    """How much of the tail crosses open wall (not the speaker): the straight run from the box to the first pixel of
    the figure."""
    bxm = ((tail[0][0] + tail[2][0]) / 2, (tail[0][1] + tail[2][1]) / 2)
    L = math.hypot(tip[0] - bxm[0], tip[1] - bxm[1])
    n = max(2, int(L))
    for i in range(n + 1):
        x = bxm[0] + (tip[0] - bxm[0]) * i / n; y = bxm[1] + (tip[1] - bxm[1]) * i / n
        if ms["N"][int(min(959, max(0, y))), int(min(539, max(0, x)))]:
            return L * i / n
    return L


def _draw(c, lines, bx, by, bw, bh, tail, dark):
    fill = (0.16, 0.05, 0.08) if dark else (1, 1, 1)
    edge = (0.93, 0.25, 0.35) if dark else INK
    c.set_line_join(1)
    SP._box_path(c, bx, by, bw, bh)                         # the outlines first
    c.set_source_rgb(*edge); c.set_line_width(7); c.stroke()
    c.move_to(*tail[0]); c.line_to(*tail[1]); c.line_to(*tail[2]); c.close_path()
    c.set_source_rgb(*edge); c.set_line_width(7); c.stroke()
    SP._box_path(c, bx, by, bw, bh); c.set_source_rgb(*fill); c.fill()   # then the fills: the tail's over the box's edge
    c.move_to(*tail[0]); c.line_to(*tail[1]); c.line_to(*tail[2]); c.close_path(); c.set_source_rgb(*fill); c.fill()
    c.select_font_face(kit.FONT); c.set_font_size(31)
    c.set_source_rgb(*((1, 1, 1) if dark else INK))
    for i, l in enumerate(lines):
        c.move_to(bx + (bw - c.text_extents(l).x_advance) / 2, by + 42 + 37 * i); c.show_text(l)


def bubble(c, text, tip, y=128, up=False, side=0, maxw=372, dark=False, shift=0):
    """Same call as dh_anim1.bubble; tip only names the speaker (the nearest head)."""
    if SP.PLANT[0] is not None:
        return SP.PLANT[0](c, text, tip, y, up, side, maxw, dark, shift)
    if text in CARD:
        return SP.card(c, text, CARD[text], side, maxw)
    rec = SP.pick(tip)
    if rec is None:
        return SP.card(c, text, "", side, maxw)
    if rec["kind"] == "antenna":
        ms = _antenna_meas(rec)
    else:
        ms = measure(rec)
    M = SP._dilate(SP.others_mask(rec), 4) | (ms["fc"]["S"] if "fc" in ms else np.zeros((960, 540), bool))
    if SP.KEEP:
        M |= SP._dilate(SP.keep_mask(), 4)
    if "fc" in ms and "K" in ms["fc"]:                      # the booth: its neon motto is a sign too
        M |= ms["fc"]["K"]
    hx = ms["m"][0]
    pref = side if side else (1 if hx < 270 else -1)
    key = (text, int(round(ms["m"][0] / 40)), int(round(ms["m"][1] / 40)))
    held = LOCK.get(text)
    tries = []
    if rec["kind"] == "antenna":
        tries = ["T"]
    else:
        tries = ["R" if pref > 0 else "L", "L" if pref > 0 else "R"]
        if ms.get("bald") and rec.get("kind") == "face":
            tries.append("T")
    ov = SAY.get(text)
    if ov:
        tries = [ov["form"]]
    best = None
    for mw in ([ov["maxw"]] if ov and "maxw" in ov else sorted({maxw, 220, 170, 130}, reverse=True)):
        lines, bw, bh = _lines(c, text, mw)
        for form in tries:
            for hair in ((False, True) if form != "T" else (False,)):
                if held and held[2] == form and held[4] == (bw, bh) and abs(held[5][0] - ms["m"][0]) < 0.6 * ms["r"] \
                        and abs(held[5][1] - ms["m"][1]) < 0.6 * ms["r"]:
                    bx, by = held[0], held[1]
                else:
                    bx, by = _place(ms, form, bw, bh, hair=hair)
                    if ov:
                        bx = max(SAFE[0], min(540 - 24 - bw, bx + ov.get("dx", 0)))
                        by = max(SAFE[1], by + ov.get("dy", 0))
                tail, tp = _tail(ms, form, bx, by, bw, bh)
                ok_box = _inside(bx, by, bw, bh) and _free(M, bx, by, bw, bh)
                wall = _wall(ms, tail, tp) if form != "T" else 0
                level = form == "T" or (by + 10 <= ms["m"][1] <= by + bh - 10) or bool(ov and ov.get("dy"))
                score = (0 if ok_box else 1000) + (0 if level else 300) + max(0, wall - 26) * 10 + 40 * (len(lines) - 1) \
                    + (0 if form == tries[0] else 60) + (30 if hair else 0) + (0 if form != "T" else 80)
                if best is None or score < best[0]:
                    best = (score, form, bx, by, bw, bh, lines, tail, tp, ok_box and level and wall <= 26 + 4)
    score, form, bx, by, bw, bh, lines, tail, tp, clean = best
    if not clean:
        NEEDS_FRAME[text] = "no clear wall beside the face (form %s, score %d)" % (form, score)
    LOCK[text] = (bx, by, form, 0, (bw, bh), ms["m"])
    _draw(c, lines, bx, by, bw, bh, tail, dark)
    LAST.append(dict(kind="face" if form != "T" else ("antenna" if rec["kind"] == "antenna" else "overhead"), text=text,
                     tip=tp, mouth=ms["m"], r=ms["r"], box=(bx, by, bw, bh), side=form, rec=rec, clean=clean))


def _antenna_meas(rec):
    an = SP.read_antenna(rec)
    ax, ay = an["tip"]
    return dict(m=an["head"], top=(ax, ay - 2.5), eL=ax, eR=ax, sL=ax, sR=ax, z=an["s"], N=an["N"], r=an["r"])
