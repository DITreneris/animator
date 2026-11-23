"""ONE STAR: the layout pass (Tomas, 20 Nov: "lay each scene out in detail first, so we see where, when and what we
show, and can look at the props"). Scenes 3-6, one sheet each: every shot's frame as the board draws it now (the
same drawing code the animation builds on; the shots already in the motion tests from cs_anim, v10), at feed size, with its time on the film_v4 clock, its lines, and the
rule check: OK (green), FIX (amber: what changes before animating), ASK (red: a decision for Tomas).
The notes behind each verdict are in customer-success/one-star-layout-v1.md.
  python3 cs_layout.py [out_dir]  ->  cs_layout_v1_scene3.png ... scene6.png"""
import json
import os
import sys
import cairo

BOARD = "cs_board_v7"
V = "v2"                                                   # v2: the outside audit's correlating points; the real clock
OK, FIX, ASK = (0.20, 0.62, 0.32), (0.90, 0.58, 0.10), (0.85, 0.20, 0.20)

# shot, scene, verdict, three short lines for the tile (the md has the rest)
SHOTS = [
    ("3.1", 3, FIX, ["Robot prints the AI plan", "ROBOT: Blueprint generated...", "DON: Approved.  | wall bare"]),
    ("3.2", 3, FIX, ["9:00 he walks in past Sofía", "1.0 s too short for a walk", "7 strip in his pocket"]),
    ("3.3", 3, FIX, ["DON: Recovered.", "Client cut by the frame", "the sheet: in both hands"]),
    ("3.4", 3, ASK, ["The AI site plan, held 2 s", "the silhouette: platforms", "SITE PLAN title missing"]),
    ("3.5", 3, OK, ["CLIENT: Is this a joke?", "tilt, tilt, red, turns", "the 7 strip shows"]),
    ("3.5b", 3, FIX, ["Don: panic, the boom", "swings loose (set-up)", "wall bare"]),
    ("4.1", 4, FIX, ["Pam steps into his way", "glasses up, sleeves up", "the roll: whose hand"]),
    ("4.2", 4, FIX, ["Her hands unroll it", "MY GARAGES unreadable", "the hole at 7"]),
    ("4.2b", 4, FIX, ["Pam points at his pocket", "her arm: stretched", "stand closer, IK"]),
    ("4.3a", 4, FIX, ["He freezes, 0.5 s", "the strip floats on his", "jacket: in his hand"]),
    ("4.3c", 4, FIX, ["The 7 in his hand", "the hand: a block", "redraw the fist"]),
    ("4.3b", 4, FIX, ["9 turned to 6, 7 in", "her finger reads as", "pointing: show the tape"]),
    ("4.4", 4, FIX, ["ROBOT: ...a h-human.", "paddle not in its hand", "closer, wall dressed"]),
    ("5.1", 5, FIX, ["CLIENT: Your number.", "his back to Sofía", "phone: in his hand"]),
    ("5.2", 5, ASK, ["Pam writes PAM 555 0142", "her close (freeze, eyes", "to Don): add a shot?"]),
    ("5.3", 5, OK, ["Contact saved", "= motion test v10", "sleeve first"]),
    ("5.4b", 5, OK, ["Pam fixes the mic", "= motion test v10", "close, 2.1 s"]),
    ("5.4c", 5, OK, ["DON: Customer success.", "= motion test v10", "plaque whole"]),
    ("6.1", 6, FIX, ["At the door, typing", "the plan under his arm", "missing in test v10"]),
    ("6.2", 6, FIX, ["UPDATE: Pam found it.", "= test v10 insert", "reply -> Shut off! (v15)"]),
    ("6.3", 6, ASK, ["Pam: phone face down,", "the peek; small, far:", "on the counter or hand?"]),
    ("6.3b", 6, FIX, ["PAM: Some post.", "Others find.", "reply -> Shut off! (v15)"]),
    ("6.5", 6, FIX, ["SOFÍA: Still one star.", "her phone, not a tablet", "1 star readable"]),
    ("6.6", 6, FIX, ["The wide = frame 0", "match scene 1's 1.1", "phones in hands"]),
]


TEST = {"5.3": ("m5_3", 8), "5.4b": ("m5_4b7", 12), "5.4c": ("m5_4c", 8), "6.1": ("m6_1_7", 6), "6.2": ("m6_1b7", 20)}


def test_frame(shot, out):
    """Shots already animated in the motion tests: their frame from cs_anim (v10 flags), the reply as script v15."""
    import cs_anim as A
    import cs_props as cp
    A.HI[0] = 1
    A.CUT_HANDSHAKE[0] = A.V7[0] = A.SWAY8[0] = A.V9[0] = A.V10[0] = True
    old = cp.REPLY_TXT[0]; cp.REPLY_TXT[0] = cp.REPLY_V15
    try:
        fn, d = TEST[shot]
        A.draw(getattr(A, fn), d).write_to_png(out)
    finally:
        cp.REPLY_TXT[0] = old
    return out


SHOTS_V1 = list(SHOTS)
SHOTS = [                                                   # v2 (20 Nov, Tomas: "improve", not what contradicts the tests)
    ("3.1", 3, FIX, ["Robot PRINTS (a visible move)", "Don's arm by IK, wall dressed", "4 s = two voice lines"]),
    ("3.2", 3, FIX, ["2.0 s: he is already walking", "2-3 walk poses past Sofía", "calendar in shot"]),
    ("3.3", 3, FIX, ["DON: Recovered. (sure of it)", "both whole in frame", "the sheet in both hands"]),
    ("3.4", 3, FIX, ["SITE PLAN / RECOVERED BY AI", "/ 99% CONFIDENT: 3 levels", "his finger counts the bays"]),
    ("3.5", 3, FIX, ["CLIENT: Is this a joke?", "pocket: only the BLUE EDGE", "no readable 7 yet"]),
    ("3.5b", 3, OK, ["One jerk of panic,", "the boom swings loose", "(built: m3_5b), wall dressed"]),
    ("4.1", 4, FIX, ["2.0 s: Pam into his way,", "glasses up, sleeves up", "(kept: Tomas, v9)"]),
    ("4.2", 4, FIX, ["PROBLEM: a gap at 7", "torn-paper outline, no red 7", "MY GARAGES on one strip"]),
    ("4.2b", 4, FIX, ["SUSPICION: Pam points", "at the blue edge in his pocket", "closer, elbow bent (IK)"]),
    ("4.3a", 4, FIX, ["REACTION: strip in his hand", "(fingers round it), he freezes", "the 7 NOT readable yet"]),
    ("4.3c", 4, FIX, ["PROOF: the first readable 7", "a real fist: palm, thumb,", "fingers round the strip"]),
    ("4.3b", 4, FIX, ["EXPLANATION: one flip 9->6,", "7 in; her thumb on the tape", "stops beside it, never covers"]),
    ("4.4", 4, FIX, ["ROBOT: ...a h-human.", "the paddle IN its hands,", "the arrow aimed at Pam"]),
    ("5.1", 5, FIX, ["CLIENT: Your number.", "head and eyes to Pam,", "phone in hand, Sofía behind"]),
    ("5.2a", 5, FIX, ["NEW close, Pam (0.8 s):", "she freezes, eyes to Don", "and back (Tomas)"]),
    ("5.2", 5, FIX, ["Her pen writes PAM 555 0142", "on the tape across 7", "(kept: protect list #4)"]),
    ("5.3", 5, OK, ["Contact saved", "his sleeve first (v10)", "= his phone"]),
    ("5.4b", 5, OK, ["Pam fixes the mic", "cold test v9: read 2/2", "(motion test v10)"]),
    ("5.4c", 5, OK, ["DON: Customer success.", "plaque whole", "(motion test v10)"]),
    ("6.1", 6, FIX, ["Grudging, typing; the", "plan rolled under his", "left arm"]),
    ("6.2", 6, OK, ["UPDATE: kept as tested", "(4/4 cold viewers read it)", "reply = Shut off! (v15)"]),
    ("6.3", 6, FIX, ["Phone ON THE COUNTER,", "closer: flips it face down,", "peeks, almost smiles"]),
    ("6.3b", 6, OK, ["PAM: Some post.", "Others find.", "reply = Shut off! (v15)"]),
    ("6.5", 6, FIX, ["SOFÍA: Still one star.", "a real phone, 1/5 big,", "dry, exhausted, no anger"]),
    ("6.6", 6, FIX, ["= frame 0 (scene 1's 1.1)", "Don puffs up: praise", "(kept: the ending)"]),
]
REAL_LEN = {"3.2": 2.0, "4.1": 2.0, "5.2a": 0.8, "5.3": 1.0, "5.4b": 25 / 12.0, "5.4c": 16 / 12.0, "6.1": 1.0,
            "6.2": 31 / 12.0}
ORDER = [s[0] for s in SHOTS]
START3 = (157 + 64) / 12.0                                  # cs_scene1_v6 (157 drawings) + cs_scene2_v1 (64)


def clock():
    """v2: each shot's place on the film as built: scenes 1-2 animated, then animatic v3's lengths (they hold the
    voice lines) except where the layout changed a shot. v1 used animatic v3's clock, which still had the cut
    handshake (5.4a): an outside reviewer read its 2 s as a hole in the cut."""
    old = clock_v1()
    out, t = {}, START3
    for sh in ORDER:
        ln = REAL_LEN.get(sh, old.get(sh, (0, 1.0, []))[1])
        out[sh] = (t, ln, old.get(sh, (0, 0, []))[2]); t += ln
    return out


def clock_v1():

    """Each shot's place on animatic v3's clock (the film_v4 takes are the same for scenes 3-6)."""
    tm = json.load(open("cs_animatic_timing_v3.json"))
    return {r["shot"]: (r["start"], r["len"], [l["text"] for l in r["lines"]]) for r in tm["rows"]}


def tile(c, x, y, png, shot, verdict, lines, t):
    tw, th = 270, 480
    s = cairo.ImageSurface.create_from_png(png)
    c.save(); c.translate(x, y + 34); c.scale(tw / float(s.get_width()), th / float(s.get_height()))
    c.set_source_surface(s, 0, 0); c.paint(); c.restore()
    c.set_source_rgb(*verdict); c.rectangle(x, y, tw, 34); c.fill()
    c.select_font_face("Inter", 0, 1); c.set_font_size(19); c.set_source_rgb(1, 1, 1)
    tag = {OK: "OK", FIX: "FIX", ASK: "ASK"}[verdict]
    c.move_to(x + 8, y + 24); c.show_text("%s   %s" % (shot, tag))
    if t:
        c.set_font_size(15); e = c.text_extents("%.1f-%.1f s" % (t[0], t[0] + t[1]))
        c.move_to(x + tw - e.x_advance - 8, y + 23); c.show_text("%.1f-%.1f s" % (t[0], t[0] + t[1]))
    c.set_source_rgb(0.12, 0.12, 0.13); c.rectangle(x, y + 34 + th, tw, 78); c.fill()
    c.select_font_face("Inter", 0, 0); c.set_font_size(16); c.set_source_rgb(0.95, 0.95, 0.95)
    for i, ln in enumerate(lines):
        c.move_to(x + 8, y + 34 + th + 22 + i * 22); c.show_text(ln)


def main(out_dir):
    ck = clock()
    for scene in (3, 4, 5, 6):
        rows = [s for s in SHOTS if s[1] == scene]
        cols = min(6, len(rows)); nrow = (len(rows) + cols - 1) // cols
        W, H = 20 + cols * 290, 70 + nrow * (34 + 480 + 78 + 20)
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
        c.set_source_rgb(0.20, 0.20, 0.21); c.paint()
        t0 = min(ck[s[0]][0] for s in rows if s[0] in ck); t1 = max(ck[s[0]][0] + ck[s[0]][1] for s in rows if s[0] in ck)
        c.select_font_face("Inter", 0, 1); c.set_font_size(26); c.set_source_rgb(1, 1, 1)
        c.move_to(20, 44); c.show_text("ONE STAR · layout %s · scene %d · %.1f-%.1f s (the film's clock) · board v7 + motion test v10 frames" % (V, scene, t0, t1))
        for i, (shot, _, verdict, lines) in enumerate(rows):
            src = "5.2" if shot == "5.2a" else shot                      # 5.2a is new: its tile shows 5.2's board frame
            png = (test_frame(shot, "/tmp/cs_layout_%s.png" % shot) if shot in TEST
                   else os.path.join(out_dir, BOARD, "cs_board_%s.png" % src))
            tile(c, 20 + (i % cols) * 290, 70 + (i // cols) * (34 + 480 + 78 + 20), png, shot, verdict, lines, ck.get(shot))
        p = os.path.join(out_dir, "cs_layout_%s_scene%d.png" % (V, scene)); S.write_to_png(p); print("wrote", p)
    print("film: %.1f s" % (max(t + l for t, l, _ in ck.values())))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../customer-success")
