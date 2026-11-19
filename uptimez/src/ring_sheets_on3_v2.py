"""OFFICE NOIR 3: the ring, the three planning sheets of gate G2b (set v2, 19 Nov; ring_sheets_on3_v1.py draws v1).
v2: the blocking sheet shows the frames of the second cold test (ring_casts_on3.py) and both tests' results; the set
sheet has the dark doorway and the lower hats; the plan sheet has 5.1 split, as script v12.
  on3_ring_set_v2.png       the clean set: zones, depth, home positions, ways in and out
  on3_ring_plan_v2.png      the ring from above: camera setups, and every shot of beats 05-07 by zone, setup, size, time
  on3_ring_blocking_v2.png  the hardest beat (5.1, 5.2) as real camera frames on the set, eyelines and moves marked
Usage: python3 ring_sheets_on3.py [out_dir]   (default ../office-noir-3)"""
import sys
import math
import cairo
import kit
import ring_on3_v2 as rg
import ring_casts_on3_v2 as rc
import cast_on3_v6 as ca
import client_on3 as b
import robot_on3 as r
import sofia_on3 as so3
from kit import Ctx, INK

F, SC = rg.F, rg.SC
PAPER = (0.95, 0.93, 0.88)
EYE, MOVE = (0.10, 0.45, 0.85), (0.90, 0.45, 0.10)


def T(c, s, x, y, size=20, bold=False, col=INK, center=False):
    c.select_font_face("Inter", 0, 1 if bold else 0); c.set_font_size(size); c.set_source_rgb(*col)
    if center:
        x -= c.text_extents(s).x_advance / 2
    c.move_to(x, y); c.show_text(s)


def arrow(c, x0, y0, x1, y1, col, dash=False, lw=4):
    c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
    if dash:
        c.set_dash([12, 8])
    c.move_to(x0, y0); c.line_to(x1, y1); c.stroke(); c.set_dash([])
    a = math.atan2(y1 - y0, x1 - x0)
    c.move_to(x1, y1); c.line_to(x1 - 16 * math.cos(a - 0.4), y1 - 16 * math.sin(a - 0.4))
    c.line_to(x1 - 16 * math.cos(a + 0.4), y1 - 16 * math.sin(a + 0.4)); c.close_path(); c.fill()


def probe(fn):
    """Draw on a scratch surface to learn where a figure's hands and head are."""
    return fn(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 8, 8)), 0))


# ------------------------------------------------------------------ the casts
def cast_home():
    H = rg.HOME

    def fig(name, fn):
        def d(k):
            x, y, s = H[name]
            rg.shadow(k, x, y, 34); fn(k, x, y, s)
        return d
    mid = [fig("referee", lambda k, x, y, s: ca.referee(k, x, y, s, "ref_stand", look=(-0.6, 0))),
           fig("robot_corner", lambda k, x, y, s: r.robot(k, x, y, s, "r_wait", "proud", side=-1)),
           fig("robot", lambda k, x, y, s: r.robot(k, x, y, s, "r_wait", "furious", side=-1)),
           fig("client", lambda k, x, y, s: b.boxer(k, x, y, s, "b_walk", "hard", (0.8, 0))),
           fig("pam", lambda k, x, y, s: ca.pam_corner(k, x, y, s, "p_stand", "neutral", (0.6, 0)))]
    front = [lambda k: so3.sofia(k, 694, F + 108, 0.92, "r_hips", "spotted", (-1, 0))]      # at the head of her lane
    return mid, front


CL51 = (212, F - 26)
PAM51 = (112, F - 14)


def cast51(sofia_x=585):
    """5.1: he is through the ropes; Pam has the robe off his shoulders and pulls at a sleeve; the Referee and the
    robot wait at centre; Sofia crosses the front with the card, her eyes on him; his are on the plan."""
    cl = lambda k: b.boxer(k, *CL51, SC * b.REL, "b_walk", "hard", (0.5, -0.9), strip=True)
    gx, gy = probe(cl)["hands"][0]; q = SC * b.REL
    px_, pf = PAM51

    def client(k):
        rg.shadow(k, CL51[0], CL51[1], 44); cl(k)

    def pam(k):
        rg.shadow(k, px_, pf, 34)
        ca.pam_corner(k, px_, pf, SC, ca.reach(px_, pf, SC, (gx - 26 * q, gy - 36 * q), (gx - 2 * q, gy - 64 * q), stance=(6.0, 12)),
                      "curious", (0.9, 0.4), stance=(6.0, 12))

    def ref(k):
        rg.shadow(k, 368, F - 88, 36); ca.referee(k, 368, F - 88, SC * ca.REL_REF, "ref_stand", look=(-0.8, 0))

    def robot(k):
        rg.shadow(k, 452, F - 46, 40); r.robot(k, 452, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def sofia(k):
        so3.sofia(k, sofia_x, F + 108, 0.92, "r_card", "spotted", (-1, 0), card_="ROUND 1")
    return [ref, robot, client, pam], [sofia]


def cast52():
    """5.2: the bell has gone and the Referee has stepped back to the robot's far side, his arm still up; he swings;
    the glove stops a hand short, with only the dark hall behind the gap; Pam's thumb is on the stopwatch."""
    def ref(k):
        rg.shadow(k, 545, F - 96, 36); ca.referee(k, 545, F - 96, SC * ca.REL_REF, "ref_bell", look=(-0.8, 0.2))

    def robot(k):
        rg.shadow(k, 462, F - 46, 40); r.robot(k, 462, F - 46, SC * r.REL, "r_wait", "furious", side=-1)

    def client(k):
        rg.shadow(k, 292, F - 40, 44); b.boxer(k, 292, F - 40, SC * b.REL, "b_swing", "hard", (0.9, 0))

    def pam(k):
        x, f = 172, F - 10
        ca.pam_corner(k, x, f, SC, ca.reach(x, f, SC, (228, F - 196), (196, F - 84), stance="stand"), "neutral", (0.9, 0.1),
                      watch="hand", stance="stand")
    return [ref, robot, client, pam], []


# ------------------------------------------------------------------ sheet 1: the set
def sheet_set(out):
    S = 1.25
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint(); k = Ctx(c, 0)
    T(c, "THE RING · Office Noir 3: The Last Round · set v2 · the room of beats 05 to 07", 50, 70, 40, True)
    T(c, "One lamp, his plan under it, two corners. Everyone at home; the robot is drawn twice (centre for the fight, its corner between rounds).", 50, 106, 22)
    X0, Y0 = 50, 150
    y_top = 660                                            # the world's rows shown: 660 .. 1650
    c.save(); c.rectangle(X0, Y0, rg.WW * S, 990 * S); c.clip()
    c.translate(X0, Y0); c.scale(S, S); c.translate(0, -y_top)
    mid, front = cast_home()
    rg.draw_ring(k, mid, front)
    c.restore()
    f = cairo.ImageSurface(cairo.FORMAT_RGB24, int(rg.WW * S), int(990 * S)); fc = cairo.Context(f)
    fc.set_source_surface(s, -X0, -Y0); fc.paint(); rg.csh.noir(f)
    c.set_source_surface(f, X0, Y0); c.paint()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(X0, Y0, rg.WW * S, 990 * S); c.stroke()
    wx = lambda x: X0 + x * S
    wy = lambda y: Y0 + (y - y_top) * S
    for z, name, x0, x1, col in rg.ZONES:                  # the zones, under the picture
        c.set_source_rgba(*col, 0.16); c.rectangle(wx(x0), Y0 + 990 * S + 8, (x1 - x0) * S, 64); c.fill()
        T(c, z, wx(x0) + 10, Y0 + 990 * S + 54, 40, True, col)
        T(c, name.split(":")[0].split(",")[0], wx(x0) + 50, Y0 + 990 * S + 50, 20, False, col)
        c.set_source_rgba(*col, 0.9); c.set_line_width(2); c.set_dash([8, 8])
        if x0:
            c.move_to(wx(x0), Y0); c.line_to(wx(x0), Y0 + 990 * S); c.stroke()
        c.set_dash([])
    # ways in and out
    arrow(c, wx(20), wy(F + 150), wx(140), wy(F - 20), MOVE, True)                 # Don, in to the stool
    arrow(c, wx(190), wy(F - 60), wx(560), wy(rg.FAR - 20), MOVE, True)            # Don, out under the plan
    arrow(c, wx(700), wy(F + 96), wx(60), wy(F + 96), EYE, True)                   # Sofia's lane
    arrow(c, wx(-6) + 30, wy(F - 150), wx(120), wy(F - 60), (0.75, 0.15, 0.15), True)   # the Client, through the ropes
    X1 = X0 + rg.WW * S + 50
    rows = [("Zones, each with one job", None),
            ("A  his corner: the pale-padded post, the stool with the folder, the bucket. Pam works here.", None),
            ("B  centre: the lamp, his plan on two cords, the fight. The Referee stands a step behind the line between them.", None),
            ("C  its corner: the post with the socket, the cable, the oil can. The robot goes home here between rounds.", None),
            ("", None),
            ("Depth, back to front", None),
            ("1 the hall, and the doorway behind C: dark until Don leaves by it", None),
            ("2 the far crowd: one dark mass, hats; cuffs with money in 5.1 only", None),
            ("3 the far posts and ropes (grey)", None),
            ("4 the canvas and the cast; the lamp's pool is brightest in B", None),
            ("5 the near ropes and posts (bright): in the master only; a camera inside the ropes leaves them out", None),
            ("6 the apron: Sofía's lane, right to left, in front of the ropes", None),
            ("7 the ringside hats: big, black, nearest us", None),
            ("", None),
            ("Home positions (world x, feet, scale)", None),
            ("Pam 88, F−16, 0.70 · Client on the stool 152, F−36 · Client, fighting 296, F−42, 0.49", None),
            ("Referee 368, F−88, 0.49 · robot, fighting 452, F−46, 0.57 · robot, its corner 600, F−52", None),
            ("Sofía, the lane 600 → 100, F+108, 0.92.  F = 1400; the canvas runs from F−110 to F+30.", None),
            ("", None),
            ("Ways in and out", None),
            ("The Client: through the ropes on A's side, once, in 5.1 (red).", (0.75, 0.15, 0.15)),
            ("Don: in from our side to the stool; out across B, under the plan, to the doorway (orange).", MOVE),
            ("Sofía: along the apron, never onto the canvas (blue).", EYE),
            ("Mom: never here. Her word arrives on the robot's screen.", None),
            ("", None),
            ("What hangs over B", None),
            ("The lamp, then his plan: level on two cords, one end let down so the ten bays show.", None),
            ("Its hung end is over the gap between them; a hat can touch it, a glove cannot hold it.", None),
            ("Only the Client looks up. Nobody else's eyeline ever rises above the ropes.", None)]
    y = Y0 + 30
    for t, col in rows:
        head = t and col is None and not t[0].isdigit() and t.split(" ")[0] not in ("A", "B", "C", "Pam", "Referee", "Sofía,", "The", "Its", "Only", "Mom:")
        T(c, t, X1, y, 22 if head else 19, bool(head), col or INK)
        y += 40 if head else 33
    s.write_to_png(out)


# ------------------------------------------------------------------ sheet 2: from above, and the shot table
SHOTS = [("5.1a", "A B C", "R1", "wide, the master", "0:34.0", 2.5, "the ring, the plan; Sofía walks ROUND 1"),
         ("5.1b", "A", "R3", "medium", "0:36.5", 2.0, "the robe off his shoulders; the sleeves stop at the gloves"),
         ("5.2", "B", "R2", "two-shot", "0:38.5", 1.5, "the bell; he swings; the glove stops short; Pam's thumb"),
         ("5.3", "B", "insert", "the screen", "0:40.0", 1.0, "HUMAN / APPROVAL / REQUIRED"),
         ("5.4", "office", "—", "close, Mom", "0:41.0", 2.0, "she reads the hundred; the button; \"Approved.\""),
         ("5.5", "B", "insert, R2", "two-shot", "0:43.0", 1.5, "the tick; one jab; he goes over"),
         ("5.6", "B", "R5", "from above", "0:44.5", 1.5, "the count; his wrist is a glove; Pam's stopwatch"),
         ("6.1", "A", "R3", "medium, square on", "0:46.0", 3.0, "the sponge, the tape; \"Some punch. Others patch.\""),
         ("6.2", "C | office", "R4 | —", "split frame", "0:49.0", 2.5, "the robot oiled at its post; her hand on the cash box"),
         ("6.3", "A", "R3, closer", "over his shoulder", "0:51.5", 2.0, "Don's tweezers take the folder; Sofía in his glass"),
         ("6.4", "A → B", "R2, one close", "medium", "0:53.5", 2.5, "CASE CLOSED; Don out under the plan; the eyebrow"),
         ("7.1", "A", "R3", "medium", "0:56.0", 1.5, "LAST ROUND goes past; he stands up"),
         ("7.2", "B", "closes", "three closes", "0:57.5", 1.5, "the dent; the crack; it rocks back"),
         ("7.2b", "B", "R2", "three-shot", "0:59.0", 1.5, "\"Break!\"; a bare palm; he steps back"),
         ("7.3", "B", "R6", "low, looking up", "1:00.5", 2.0, "he reaches; the plan swings; the glove cannot grip"),
         ("7.4", "B | office", "inserts", "insert, desk, insert", "1:02.5", 1.5, "the ask; the gear card face down; \"Approved.\""),
         ("7.5", "B", "close", "the framing of 1.1", "1:04.0", 1.0, "the glove lands. White")]


def sheet_plan(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    T(c, "THE RING FROM ABOVE · camera setups and the shot plan · beats 05 to 07 · set v2", 50, 70, 40, True)
    T(c, "Every shot gets one zone and one setup. Times are the script's (about 31 s); 5.1 is two shots, as in script v12.", 50, 106, 22)
    # the plan view: the ring 720 wide maps to 560 px; depth (far to near) to 420 px
    X0, Y0, RW, RH = 150, 230, 560, 380
    c.set_source_rgb(0.86, 0.85, 0.82); c.rectangle(X0, Y0, RW, RH); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(4); c.rectangle(X0, Y0, RW, RH); c.stroke()
    c.set_line_width(1.6); c.rectangle(X0 + 10, Y0 + 10, RW - 20, RH - 20); c.stroke()
    mx = lambda x: X0 + x / 720 * RW
    for z, name, x0, x1, col in rg.ZONES:
        c.set_source_rgba(*col, 0.14); c.rectangle(mx(x0), Y0, mx(x1) - mx(x0), RH); c.fill()
        T(c, z, mx(x0) + 12, Y0 + 44, 40, True, col)
    for px_, py_ in ((X0, Y0), (X0 + RW, Y0), (X0, Y0 + RH), (X0 + RW, Y0 + RH)):
        c.set_source_rgb(0.30, 0.30, 0.33); c.arc(px_, py_, 13, 0, 2 * math.pi); c.fill()
    T(c, "his post", X0 - 96, Y0 + RH + 8, 16); T(c, "its post", X0 + RW + 22, Y0 + RH + 8, 16); T(c, "low, looking up", mx(300) + 34, Y0 + RH - 38, 15)

    def mark(x, depth, label, col=INK, r_=13, fill=True):
        px_, py_ = mx(x), Y0 + depth * RH
        c.new_path(); c.set_source_rgb(*col); c.arc(px_, py_, r_, 0, 2 * math.pi)
        c.fill() if fill else (c.set_line_width(3), c.set_dash([6, 5]), c.stroke(), c.set_dash([]))
        T(c, label, px_, py_ + r_ + 20, 16, True, col, center=True)
        return px_, py_
    mark(88, 0.90, "Pam"); mark(152, 0.76, "stool"); mark(296, 0.70, "Client", (0.75, 0.15, 0.15))
    mark(368, 0.36, "Referee"); mark(452, 0.66, "robot"); mark(600, 0.80, "robot, home", (0.35, 0.35, 0.38))
    mark(365, 0.52, "lamp · plan", (0.2, 0.2, 0.2), 60, False)
    c.set_source_rgb(0.80, 0.80, 0.78); c.rectangle(mx(548), Y0 - 70, 52, 30); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(mx(548), Y0 - 70, 52, 30); c.stroke()
    T(c, "the way out", mx(548) + 62, Y0 - 50, 16)
    arrow(c, mx(690), Y0 + RH + 80, mx(70), Y0 + RH + 80, EYE, True); T(c, "Sofía's lane (the apron)", mx(250), Y0 + RH + 106, 16, False, EYE)
    arrow(c, mx(40), Y0 + RH + 150, mx(140), Y0 + RH * 0.82, MOVE, True)
    arrow(c, mx(190), Y0 + RH * 0.66, mx(570), Y0 - 34, MOVE, True); T(c, "Don: in to the stool, then out under the plan", X0 - 120, Y0 + RH + 250, 16, False, MOVE)
    arrow(c, X0 - 70, Y0 + RH * 0.62, mx(120), Y0 + RH * 0.70, (0.75, 0.15, 0.15), True); T(c, "the Client, in", X0 - 100, Y0 + RH * 0.56, 16, False, (0.75, 0.15, 0.15))

    def cam(name, x, y, tx, ty, note):
        a = math.atan2(ty - y, tx - x)
        c.set_source_rgba(0.1, 0.1, 0.12, 0.10)
        c.move_to(x, y); c.line_to(tx + 60 * math.sin(a), ty - 60 * math.cos(a)); c.line_to(tx - 60 * math.sin(a), ty + 60 * math.cos(a)); c.close_path(); c.fill()
        c.set_source_rgb(0.12, 0.12, 0.14); c.rectangle(x - 26, y - 15, 52, 30); c.fill()
        T(c, name, x, y + 7, 18, True, (1, 1, 1), center=True)
        T(c, note, x, y + 38, 15, False, INK, center=True)
    cy_ = Y0 + RH
    cam("R1", mx(360), cy_ + 250, mx(360), cy_ - 120, "the master")
    cam("R2", mx(470), cy_ + 150, mx(380), cy_ - 160, "centre, two-shot")
    cam("R3", mx(150), cy_ + 150, mx(140), cy_ - 80, "his corner")
    cam("R4", mx(650), cy_ + 150, mx(600), cy_ - 80, "its corner")
    cam("R6", mx(300), cy_ - 44, mx(330), cy_ - 200, "")
    c.set_source_rgb(0.12, 0.12, 0.14); c.rectangle(mx(250) - 26, Y0 + RH * 0.30 - 15, 52, 30); c.fill()
    T(c, "R5", mx(250), Y0 + RH * 0.30 + 7, 18, True, (1, 1, 1), center=True); T(c, "straight down", mx(250), Y0 + RH * 0.30 + 38, 15, center=True)
    # the table
    TX, TY = 880, 190
    cols = (("shot", 0), ("zone", 80), ("setup", 210), ("size", 370), ("at", 590), ("s", 680), ("what it has to carry", 730))
    for h, dx in cols:
        T(c, h, TX + dx, TY, 19, True)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(TX, TY + 10); c.line_to(W - 50, TY + 10); c.stroke()
    zc = {z: col for z, _, _, _, col in rg.ZONES}
    for i, (sh, zone, setup, size, at, dur, what) in enumerate(SHOTS):
        y = TY + 44 + i * 38
        col = zc.get(zone[0], (0.35, 0.35, 0.38))
        c.set_source_rgba(*col, 0.12); c.rectangle(TX - 8, y - 24, W - 50 - TX + 8, 34); c.fill()
        for v, (h, dx) in zip((sh, zone, setup, size, at, "%.1f" % dur, what), cols):
            T(c, v, TX + dx, y, 18, h == "shot", col if h == "zone" else INK)
    # time by zone
    BY = 1010
    T(c, "Where the camera is, second by second", 120, BY, 24, True)
    t0, t1 = 34.0, 65.0
    bx = lambda t: 120 + (t - t0) / (t1 - t0) * 1960
    lanes = ["A", "B", "C", "office"]
    for j, ln in enumerate(lanes):
        y = BY + 40 + j * 62
        col = zc.get(ln, (0.35, 0.35, 0.38))
        T(c, ln, 60, y + 34, 26 if len(ln) == 1 else 15, True, col)
        c.set_source_rgba(*col, 0.07); c.rectangle(120, y, 1960, 50); c.fill()
    for sh, zone, setup, size, at, dur, what in SHOTS:
        m, sec = at.split(":"); t = int(m) * 60 + float(sec)
        parts = [z.strip() for z in zone.replace("→", " ").replace("|", " ").split()]
        for z in parts:
            j = lanes.index(z)
            col = zc.get(z, (0.35, 0.35, 0.38))
            w = (bx(t + dur) - bx(t)) - 3
            c.set_source_rgba(*col, 0.85 if len(parts) == 1 else 0.5); c.rectangle(bx(t), BY + 40 + j * 62, w, 50); c.fill()
            T(c, sh, bx(t) + w / 2, BY + 40 + j * 62 + 32, 16, True, (1, 1, 1), center=True)
    for t in range(34, 66, 2):
        T(c, "%d:%02d" % (t // 60, t % 60), bx(t), BY + 40 + 4 * 62 + 24, 15, center=True)
    notes = ["What the plan shows",
             "· B carries the film: 13 of the 31 seconds to itself and 5 more shared. That is right; the fight is the mechanism.",
             "· A is visited four times (5.1b, 6.1, 6.3, 7.1): until the last round, Pam's thread and the folder's are never away for more than 7.5 seconds.",
             "· C is visited once, in half a frame (6.2). The robot's corner has one job, one shot. If 6.2 is cut, C is only ever background",
             "  and the socket and oil can should come out of the set with it.",
             "· The office cuts in three times (5.4, 6.2, 7.4), always from B or C, never from A: Mom answers the machine, not him.",
             "· The plan is in frame in R1, R2 and R6: six shots. He looks up in 5.1 and 7.3 and points up in 6.4; nobody else looks.",
             "· R5 (from above) and the closes of 7.2 and 7.5 are their own drawings, not framings of this set."]
    for i, t in enumerate(notes):
        T(c, t, 120, 1400 + i * 34, 24 if i == 0 else 20, i == 0)
    s.write_to_png(out)


# ------------------------------------------------------------------ sheet 3: the hardest beat, as frames
def sheet_blocking(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    T(c, "THE RING · blocking 5.1a, 5.1b, 5.2 · the frames of the second cold test · set v2", 50, 70, 40, True)
    T(c, "Blue: where someone looks. These are the frames two fresh viewers saw, with nothing added but the arrows.", 50, 106, 22)
    Z = 1.0
    FW, FH = 540 * Z, 960 * Z
    titles = ("5.1a · R1, the master · 2.5 s", "5.1b · R3, his corner · 2.0 s", "5.2 · R2, centre · 1.5 s")
    plan = (rg.PLAN[0] + 50 * rg.PLAN[2], rg.PLAN[1] + 64 * rg.PLAN[2])
    Q = rc.Q
    for i, ((cam, cast, kw), title) in enumerate(zip(rc.SPECS, titles)):
        x0, y0 = 50 + i * (FW + 60), 140
        mid, front = cast()
        f = rg.frame(cam, mid, front, **kw)
        c.save(); c.translate(x0, y0); c.scale(Z, Z); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x0, y0, FW, FH); c.stroke()
        T(c, title, x0, y0 + FH + 36, 26, True)
        P = lambda x, y: (x0 + rg.to_frame(rg.CAMS[cam], x, y)[0] * Z, y0 + rg.to_frame(rg.CAMS[cam], x, y)[1] * Z)
        c.save(); c.rectangle(x0, y0, FW, FH); c.clip()
        if i == 0:
            hx, hy = 112, F - 44 + b.HY * Q
            arrow(c, *P(hx + 24, hy - 30), *P(plan[0] - 30, plan[1] + 40), EYE)
            arrow(c, *P(540, F - 150), *P(hx + 50, hy + 10), EYE)
        elif i == 1:
            hx, hy = rc.CL[0], rc.CL[1] + b.HY * Q
            arrow(c, *P(hx + 26, hy - 30), *P(plan[0] - 44, plan[1] + 50), EYE)
            arrow(c, *P(rc.PAM[0] - 14, F - 196), *P(rc.PAM[0] - 60, F - 150), EYE)
        else:
            arrow(c, *P(316, F - 232), *P(450, F - 200), EYE)
        c.restore()
    X1 = 1880
    rows = [("Cold test 1 (set v1): 2 of 5, 2 of 5", True), ("Cold test 2 (these frames): 4 of 5, 3 of 5", True), ("Pass is 4 of 5 for both: FAIL", True), ("", False),
            ("Read by both, both times", True), ("· the ring, the corners, ROUND 1", False), ("· the punch stops short; the robot", False), ("  does not move", False), ("", False),
            ("Fixed between the tests", True), ("· the robe gag: now read by both", False), ("  (the sleeve stretched to her hands)", False), ("· the robot's face is no longer", False), ("  behind the card", False), ("", False),
            ("Failed both times, the same way", True), ("· nobody sees him look at the plan.", False), ("  Eyes up read as \"fed up\"; the", False), ("  plan reads as decoration", False),
            ("· the Referee behind the robot", False), ("  reads as the robot's man (1 of 2)", False), ("", False),
            ("New faults in these frames", True), ("· the stop marks at the glove read", False), ("  as a hit on nothing", False), ("· the ropes across him in 5.1a read", False), ("  as a sash, not as arriving", False),
            ("· Sofía is cut by the frame's edge", False), ("· robe on, off, on: both worked it", False), ("  out; one first took it for a slip", False)]
    cx_, y = 0, 1200
    for t_, bold in rows:
        if bold and y > 1420 and not t_.startswith(("Cold", "Pass")):
            cx_ += 1; y = 1200
        T(c, t_, 50 + cx_ * 520, y, 22 if bold else 19, bold, (0.6, 0.15, 0.12) if "FAIL" in t_ else INK); y += 34 if bold else 28
    T(c, "What it means: a look cannot carry the plan in this drawing style. It needs a shot of its own (his view of it, from below) or a reach, as 7.3 has.", 50, 1610, 22, True)
    T(c, "The test cannot tell whether any of this is funny, or anything that needs sound (the bell, the click of the stopwatch).", 50, 1646, 20)
    s.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../office-noir-3"
    sheet_set(d + "/on3_ring_set_v2.png")
    sheet_plan(d + "/on3_ring_plan_v2.png")
    sheet_blocking(d + "/on3_ring_blocking_v2.png")
