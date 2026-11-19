"""FIRST SEARCH (episode 10): the set map v1. The front desk drawn wider (940 units, not 540), the cast spread out in
three zones instead of stacked in one frame, and every shot's camera frame laid over it, so we can see where each shot
is, what it shows and what the set still lacks. A planning drawing: the storyboard is untouched.
Zones: A the door and the screen (the Client comes in, the search, the robot); B the floor under OUR FIRST CLIENT (the
sale, the bonk, the payoff, Mom's lick); C the counter (Pam and her plan, Mom's desk, the shredder at its end).
python3 fs_setmap.py [out_dir] -> fs_setmap_v1.png"""
import os
import sys
import cairo
import kit
import brand
import set_ob as st
import acts_ob as ac
import fs_set as fs
import fs_storyboard as sb
import mom_fs as mfs
import sofia_fs as sfs
import pam_fs
from charsheets import corp, wrap

F = st.FLOOR
WW = 940                                                   # the wider set
DX = 330                                                   # the counter moved this far right
X = {"client": 110, "robot": 236, "sofia": 372, "don": 470, "shred": 596, "pam": 368 + DX, "mom": 470 + DX}
PORT = (470, 404)                                          # OUR FIRST CLIENT, over Don
SCR = (26, 286, 162, 100)                                  # the screen, over the door

ZONES = [("A", "the door and the screen", 0, 300, (0.20, 0.45, 0.85)),
         ("B", "the floor under OUR FIRST CLIENT", 300, 580, (0.85, 0.30, 0.25)),
         ("C", "the counter: Pam, Mom, the shredder", 580, WW, (0.20, 0.60, 0.35))]

# shot, zone, centre x, centre y, zoom (540/z units wide), what it shows
SHOTS = [("1.1a", "AB", 280, 560, 1.0, "the master: red zero, the portrait jumps"),
         ("1.1b", "AB", 280, 560, 1.0, "the bonk on Don"),
         ("1.2", "A", 200, 580, 1.6, "the Client comes in; Sofía flirts"),
         ("1.3", "B", 330, 600, 2.0, "Don turns: the sales smile"),
         ("2.1", "B", 470, 520, 3.4, "Don close: the calendar"),
         ("2.2", "AB", 300, 600, 1.9, "the tablet in Don's hand"),
         ("3.1", "B", 460, 560, 1.8, "red again: the duck; Mom licks behind"),
         ("3.3", "B", 420, 590, 2.3, "Sofía: It found nothing."),
         ("3.4", "B", 470, 410, 4.0, "the plaster on the portrait"),
         ("4.1", "B", 470, 560, 2.4, "Don: make the zero green?"),
         ("4.2", "A", 236, 690, 3.0, "the robot: approval required"),
         ("4.5", "A", 107, 336, 3.0, "the screen: the sweep to green"),
         ("5.1", "AB", 230, 540, 1.6, "the Client at the green zero"),
         ("5.2", "B", 420, 520, 2.0, "low angle: Where's my blueprint?"),
         ("5.3", "B", 470, 600, 2.0, "The zero's green.; Pam's plan held up"),
         ("6.1", "AB", 200, 560, 1.45, "the photo by the green zero"),
         ("6.1b", "C", 800, 630, 3.4, "Mom: Machines."),
         ("7.1", "C", 800, 630, 3.4, "Mom: Young man."),
         ("7.2", "B", 470, 600, 1.8, "two men step back; the thumb"),
         ("7.4", "B", 480, 600, 1.9, "the lick on his hair: Eww."),
         ("7.5", "B", 440, 600, 2.0, "Mom on Sofía: That hussy."),
         ("8.1", "BC", 560, 560, 1.0, "Pam brings the plan: Pam has a plan."),
         ("8.2", "C", 620, 620, 2.0, "the near-shred"),
         ("9.1", "A", 100, 600, 3.0, "the doorway: 100% COMPLETE"),
         ("9.2", "A", 160, 420, 2.4, "RETRY UNTIL FRIDAY; the robot"),
         ("9.3", "B", 470, 410, 4.0, "the plaster drops"),
         ("9.4", "AB", 280, 560, 1.0, "frame 0")]
INSERTS = ["2.3 the Client's thumb on the tablet", "3.2 his phone: PAID $999", "4.3 Don's thumb: APPROVED",
           "4.4 Pam's thumb: the tape", "6.2 his phone: the post", "7.3 the lick"]

PRESENT = ["the glass door (A)", "the screen UPTIMEZ FIND, over the door (A)", "OUR FIRST CLIENT and its plate (B)",
           "the brand mark on the wall", "the counter with its in-tray (C)", "ASSISTANT TO DON plate, the baby photo (C)",
           "Mom's mug, candy dish, knitting (C)", "Pam's patched plan and tape (C)", "the shredder, SHRED (C)",
           "the HR robot, its paddle and ENTER (A)"]
MISSING = ["Pam's monitor: in the switch test, not on the set; she needs a screen to turn to (C)",
           "episode 9's confetti cannon, or blue confetti left in the corners: the set forgets episode 9",
           "where Mom stands when she comes out front (7.2-7.5): a clear path from C to B",
           "a door to Don's office, or his own corner: he has no place of his own",
           "the ficus (set_ob has it; it is off in this episode)",
           "a wall clock or calendar: Friday is said, never shown on the set"]


def draw_set(k):
    c = k.c
    oldW = st.W
    st.W = WW
    try:
        st.stage(k, open_=0.85, decor=False, back=False)
    finally:
        st.W = oldW
    brand.mark(c, 760, 300, 64, zzz=False)                 # the brand mark over the counter, clear of the portrait
    fs.screen(k, "query", *SCR)
    fs.PSTATE[0] = "clean"
    try:
        fs.portrait(k, *PORT, fs.PORTRAIT_S)
    finally:
        fs.PSTATE[0] = None
    with pam_fs.look(False):
        c.save(); c.translate(DX, 0)
        sb.pam_taping(k, 368, F - 72, 0.50)
        mfs.mom(k, 470, F - 70, 0.50, "bag", "sweet", look=(-0.8, 0))
        st.desk(k, terminal=False, shred=None)
        fs.PLAN_V2[0] = True
        try:
            fs.plan_taped(k, 352, F - 190, 0.36)
        finally:
            fs.PLAN_V2[0] = False
        fs.counter_plate(k, 398, F - 176)
        mfs.knitting(k, 452, F - 160, 0.36); mfs.mug(k, 502, F - 192, 0.5); mfs.candy(k, 410, F - 170, 0.55)
        c.restore()
        ac.shredder(k, X["shred"], F, 0.9, fill=0.4)
        sb.client(k, X["client"], F - 14, 0.52, "stand", "confident", (0.9, 0))
        fs.robot_finger(k, X["robot"], F + 4, 0.48)
        sfs.sofia(k, X["sofia"], F - 8, 0.50, "hold", "charm", look=(-0.9, -0.2))
        sb.DON_STATE[0] = ("up", "up")
        try:
            sb.don(k, X["don"], F + 4, 0.56, "stand", "neutral", (-1, 0))
        finally:
            sb.DON_STATE[0] = None


def _map(k, frames):
    c = k.c
    c.rectangle(0, 0, WW, 960); c.clip()
    draw_set(k)
    for z, name, x0, x1, col in ZONES:
        c.set_source_rgba(*col, 0.12); c.rectangle(x0, F + 30, x1 - x0, 130); c.fill()
        c.set_source_rgb(*col); c.select_font_face("Inter", 0, 1); c.set_font_size(34)
        c.move_to(x0 + 12, F + 76); c.show_text(z)
        c.set_font_size(15); c.move_to(x0 + 48, F + 72); c.show_text(name)
    if not frames:
        return
    for i, (sh, zone, cx, cy, z, what) in enumerate(SHOTS):
        w, h = 540 / z, 960 / z
        col = [zz[4] for zz in ZONES if zz[0] == zone[0]][0]
        c.set_source_rgba(*col, 0.7); c.set_line_width(3.0)
        c.rectangle(cx - w / 2, cy - h / 2, w, h); c.stroke()
    for i, (sh, zone, cx, cy, z, what) in enumerate(SHOTS):
        w, h = 540 / z, 960 / z
        col = [zz[4] for zz in ZONES if zz[0] == zone[0]][0]
        c.select_font_face("Inter", 0, 1); c.set_font_size(22)
        e = c.text_extents(sh)
        lx, ly = cx - e.x_advance / 2, cy + (i % 4 - 1.5) * 26
        c.set_source_rgba(1, 1, 1, 0.9); c.rectangle(lx - 4, ly - 20, e.x_advance + 8, 26); c.fill()
        c.set_source_rgb(*col); c.move_to(lx, ly); c.show_text(sh)


def main(d):
    import json
    S1, S2 = 1.15, 0.62
    W1, H1 = int(WW * S1), int(960 * S1)
    W2, H2 = int(WW * S2), int(960 * S2)
    PANEL = 640
    TL = 230
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W1 + W2 + 50, 120 + H1 + TL + 40)
    c = cairo.Context(s); k = kit.Ctx(c, 0)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    corp(c, "FIRST SEARCH  ·  set map v1: three zones instead of one crowded frame", 30, 58, 34, brand.NAVY, True)
    wrap(c, "Left: the front desk drawn 940 wide (now 540), the cast spread out. Right: where each shot's camera "
            "looks (9:16 boxes, by zone). Below: the shots in time, by zone.", 30, 92, 18, W1 + W2)
    c.save(); c.translate(20, 120); c.scale(S1, S1); _map(k, False); c.restore()
    c.save(); c.translate(W1 + 30, 120); c.scale(S2, S2); _map(k, True); c.restore()
    px, y = W1 + 30, 120 + H2 + 30                         # the panel, under the small map
    corp(c, "ON THE SET", px, y, 20, brand.NAVY, True); y += 24
    for t in PRESENT:
        corp(c, "·  " + t, px, y, 13, (0.2, 0.2, 0.25)); y += 18
    y += 12
    corp(c, "MISSING OR UNCLEAR", px, y, 20, (0.75, 0.15, 0.15), True); y += 24
    for t in MISSING:
        n = wrap(c, "·  " + t, px, y, 13, W2 - 10, (0.2, 0.2, 0.25))
        y += 18 * (1 + len(t) // 78) + 4
    t = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../first-search/fs_timing_v14.json")))
    total = t[-1]["start"] + t[-1]["len"]
    x0, y0, wt = 30, 120 + H1 + 40, W1 + W2 - 20
    corp(c, "THE SHOTS IN TIME (animatic v14, %.1f s): the camera's zone" % total, x0, y0, 20, brand.NAVY, True)
    zone_of = {sh: z for sh, z, *_ in SHOTS}
    for r in t:
        sh = r["shot"]
        z = zone_of.get(sh)
        col = [zz[4] for zz in ZONES if zz[0] == z[0]][0] if z else (0.6, 0.6, 0.62)
        row = "ABC".index(z[0]) if z else 3
        xx = x0 + r["start"] / total * wt
        ww = r["len"] / total * wt
        c.set_source_rgba(*col, 0.85); c.rectangle(xx, y0 + 18 + row * 42, ww - 2, 36); c.fill()
        c.set_source_rgb(1, 1, 1); c.select_font_face("Inter", 0, 1); c.set_font_size(12)
        c.move_to(xx + 3, y0 + 40 + row * 42); c.show_text(sh)
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "fs_setmap_v1.png")
    s.write_to_png(out)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../first-search")
