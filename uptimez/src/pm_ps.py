"""PAM and MOM in "Pick a Side" (episode 14): their looks as ever (Pam: pam_bc, the berry lips, the brooch; Mom: mom_fs,
the teal suit, the curler), this episode's poses and props, with the one hand (hands_ps). Tomas, 23 Nov, /grill-me:
- Pam's half salute (2.5): two fingers lift off her cup toward her brow, halfway; then the cup hides her smile;
- Pam on the step stool (5.6): both hands frozen on the blind's rail, half hung; only her head turns to the door;
- Mom on the tape (2.6, 6.1): both feet together square on the stripe, arms folded, chin up, a flat, final look;
- the hand: hands_ps for all of episode 14 from now.
Pam's cup is her blue mug from episode 12 (the same evening).
v2 (23 Nov, after the hands audit): the mug sits past the fingers, so the forearm shows and the fingers wrap it; the
two fingers 25 % smaller; Mom's arms cross (one hand hidden under the top forearm, which grips her other arm); Pam's
fists drawn over the blind's rail; her reach for the phone is an open grab; the idle thumb pressed in (Pam, Mom).
  python3 pm_ps.py [out_dir]  ->  ps_pam_mom_v2.png (sheet), ps_pam_mom_phone_v2.png (phone check)"""
import math
import os
import sys
import cairo
import kit
import pam_bc as pb
import pam_mf as pm
import mom_fs as mf
import mom_on as mo
import hands_ps as hp
import don_ps as dp
from kit import Ctx, INK, cut, rect, ellipse

MUG = (0.36, 0.62, 0.80)
MUG_RING = [False]
MUG_THUMB = [False]
MUG_ART = [None]                                          # (28 Nov, Office Noir 4's mug ending) f(k, x, y, s, tilt): another mug in her hand, drawn by mug_at's rules
TAPE = dp.TAPE
STOOL = (0.55, 0.58, 0.62)
PHY, PBT = pm.HY, pm.BT
P_POSES = {"cup_mid": (-8, 0) + pm.ik(1, 40, PBT + 70), "cup_chin": (-8, 0) + pm.ik(1, 24, PHY + 68),
           "half_salute": (-8, 0) + pm.ik(1, 72, PHY + 62), "cross": (-20, 10) + pm.ik(1, 46, PBT + 64),
           "rail": pm.ik(-1, -78, PHY - 58) + pm.ik(1, 78, PHY - 58), "reach": (-8, 0) + pm.ik(1, 150, PBT + 130),
           "stand": (-8, 0, 8, 0)}
P_HANDS = {"cup_mid": ("relax_s", "cup"), "cup_chin": ("relax_s", "cup"), "half_salute": ("relax_s", "two_s"),
           "cross": ("relax_s", "cup"), "rail": ("cup", "cup"), "reach": ("relax_s", "grab"), "stand": ("relax_s", "relax_s")}
M_POSES = {"folded": mo.ik(-1, 40, mo.BT + 70) + mo.ik(1, -50, mo.BT + 46)}      # v2: the under arm lower, the top one gripping


def pam(k, x, feet, s=0.54, pose="stand", face="neutral", look=(0, 0), mug=True, late=True, **kw):
    """Pam with the one hand; a held mug is drawn under her fingers (the hand drawn again over it)."""
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset(*P_HANDS.get(pose, ("relax", "relax")))
    try:
        o = pb.pam(k, x, feet, s, P_POSES.get(pose, pose), face, look, **kw)
        g = P_HANDS.get(pose, ("", ""))[1]
        if mug and pose != "rail" and g in ("cup", "two_s"):
            hx, hy = o["hands"][1]
            (dx, dy), _ = hp.DIRS[1]
            if g == "two_s":
                mug_at(k, hx + dx * 6 * s, hy + dy * 6 * s + 22 * s, s)       # under the fist: it holds the rim
            else:
                mug_at(k, hx + dx * 14 * s, hy + dy * 14 * s + 4 * s, s)      # past the fingers: the forearm shows
        if late:
            hp.redraw_late(k)
        if MUG_THUMB[0] and MUG_RING[0] and mug and g == "cup":   # its thumb over the mug's front (26 Nov audit: off, a second
                                                             # thumb beside the rig hand's own: "two fingers", read as a phone)
            hx, hy = o["hands"][1]
            (dx, dy), _ = hp.DIRS[1]
            c = k.c; c.set_line_cap(1)
            for col, lw in ((INK, 9.5 * s), (pb.SKIN if hasattr(pb, "SKIN") else (0.98, 0.84, 0.70), 6.5 * s)):
                c.set_source_rgb(*col); c.set_line_width(lw); c.new_path()
                c.move_to(hx + dx * 2 * s, hy - 5 * s); c.line_to(hx + dx * 13 * s, hy - 12 * s); c.stroke()
            c.set_line_cap(0)
    finally:
        kit.HAND[0] = old
    return o


def mom(k, x, feet, s=0.54, pose="folded", face="unimpressed", look=(0, 0), **kw):
    old = kit.HAND[0]; kit.HAND[0] = hp.hand; hp.reset(*(("tuck", "fist") if pose == "folded" else ("relax_s", "relax_s")))
    try:
        return mf.mom(k, x, feet, s, M_POSES.get(pose, pose), face, look, **kw)
    finally:
        kit.HAND[0] = old


def mug_at(k, x, y, s, tilt=0.0):
    """Her blue mug, held: the body behind her fingers, the handle on the far side."""
    if MUG_ART[0]:
        return MUG_ART[0](k, x, y, s, tilt)
    c = k.c
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    if MUG_RING[0]:                                          # opt-in (Pick a Side film, review 25 Nov: "the handle must
        for col, lw in ((INK, 10), (MUG, 5)):                # read"): a blue ring, outlined, not a dark line on her purple
            c.set_source_rgb(*col); c.set_line_width(lw); c.new_path(); c.arc(-22, 0, 10, 1.6, 4.7); c.stroke()
    else:
        c.set_source_rgb(*INK); c.set_line_width(4); c.new_path(); c.arc(-22, 0, 9, 1.8, 4.5); c.stroke()
    cut(k, [(-16, -22), (16, -22), (14, 22), (-14, 22)], MUG, shadow=False, lw=2.2)
    ellipse(k, 0, -22, 16, 4.5, (0.24, 0.16, 0.10), 3551, shadow=False, lw=1.6)
    c.restore()


def stool(k, x, feet, s, h=90):
    """A two-step stool, grey metal: the top at feet - h*s."""
    c = k.c
    c.save(); c.translate(x, feet); c.scale(s, s)
    for sx in (-1, 1):
        c.set_source_rgb(*INK); c.set_line_width(7); c.new_path(); c.move_to(sx * 44, 0); c.line_to(sx * 34, -h); c.stroke()
        c.set_source_rgb(*STOOL); c.set_line_width(4); c.new_path(); c.move_to(sx * 44, 0); c.line_to(sx * 34, -h); c.stroke()
    rect(k, -40, -h * 0.5 - 5, 80, 10, STOOL, 801, shadow=False, lw=1.8)
    rect(k, -46, -h - 8, 92, 12, STOOL, 802, shadow=False, lw=2)
    c.restore()


BLIND_STYLE = ["sheet"]                                     # "sheet" or "slats" (v2: separate slats, read as "a stack of paper" 2/2)
BLIND_W = [0.0]                                              # opt-in (film 5.6, review 26 Nov: "a grey bar"): the blind this much wider than
                                                             # her hands each side (rig units), darker slats, its pull cord: it reads a blind

def blind_rail(k, a, b, s, drop=230):
    """The blind half hung: its rail between her hands, the slats hanging (drawn before her: behind)."""
    c = k.c
    (ax, ay), (bx, by) = a, b
    if BLIND_W[0] and BLIND_STYLE[0] == "sheet":      # v1: one sheet of slats, strings, the cord ("a bar or shelf" 2/2)
        e = BLIND_W[0] * s
        ax, bx = ax - e, bx + e
        top = min(ay, by) + 4 * s
        cut(k, [(ax - 6 * s, top), (bx + 6 * s, top), (bx + 4 * s, top + drop * s), (ax - 4 * s, top + drop * s)], dp.SLAT, shadow=False, lw=2.2)
        c.set_source_rgb(*dp.SLAT_D); c.set_line_width(2.2)
        yy = top + 12 * s
        while yy < top + drop * s - 6 * s:
            c.move_to(ax - 4 * s, yy); c.line_to(bx + 4 * s, yy); c.stroke(); yy += 12 * s
        c.set_source_rgb(*INK); c.set_line_width(1.6)                       # the ladder strings and the pull cord with its knob
        for fx in (0.22, 0.78):
            xx = ax + (bx - ax) * fx; c.move_to(xx, top); c.line_to(xx, top + drop * s); c.stroke()
        c.move_to(bx - 2 * s, top); c.line_to(bx + 14 * s, top + drop * s * 0.62); c.stroke()
        c.new_path(); c.arc(bx + 14 * s, top + drop * s * 0.62 + 5 * s, 5 * s, 0, 2 * math.pi); c.set_source_rgb(0.92, 0.92, 0.88); c.fill_preserve()
        c.set_source_rgb(*INK); c.stroke()
        return
    if BLIND_W[0]:                                           # v2 (cold test: "a grey bar or shelf" 2/2, the sheet of slats not seen as
        e = BLIND_W[0] * s                                   # a blind): separate slats with the wall between, a few crooked, a bottom
        ax, bx = ax - e, bx + e                              # rail, ladder strings and the pull cord
        top = min(ay, by) + 8 * s
        r_ = k.rng(4830)
        n = int(drop / 13)
        for xx in (ax + (bx - ax) * 0.2, ax + (bx - ax) * 0.8):
            c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(xx, top - 6 * s); c.line_to(xx, top + n * 13 * s); c.stroke()
        for i in range(n):
            yy = top + i * 13 * s
            a_ = (r_.random() - 0.5) * (0.10 if i % 5 == 3 else 0.02)
            c.save(); c.translate((ax + bx) / 2, yy + 3.5 * s); c.rotate(a_)
            rect(k, -(bx - ax) / 2, -3.5 * s, bx - ax, 7 * s, dp.SLAT, 4840 + i, shadow=False, lw=1.5)
            c.restore()
        rect(k, ax - 2 * s, top + n * 13 * s, bx - ax + 4 * s, 9 * s, (0.70, 0.70, 0.66), 4839, shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        c.move_to(bx - 2 * s, top - 6 * s); c.line_to(bx + 14 * s, top + drop * s * 0.62); c.stroke()
        c.new_path(); c.arc(bx + 14 * s, top + drop * s * 0.62 + 5 * s, 5 * s, 0, 2 * math.pi); c.set_source_rgb(0.92, 0.92, 0.88); c.fill_preserve()
        c.set_source_rgb(*INK); c.stroke()
        return
    top = min(ay, by) + 4 * s
    cut(k, [(ax - 6 * s, top), (bx + 6 * s, top), (bx + 2 * s, top + drop * s), (ax + 10 * s, top + drop * s - 20 * s)],
        dp.SLAT, shadow=False, lw=2)
    c.set_source_rgb(*dp.SLAT_D); c.set_line_width(1.3)
    yy = top + 10 * s
    while yy < top + drop * s - 22 * s:
        c.move_to(ax - 4 * s, yy); c.line_to(bx + 4 * s, yy); c.stroke(); yy += 10 * s


def rail_bar(k, a, b, s):
    c = k.c
    (ax, ay), (bx, by) = a, b
    ang = math.atan2(by - ay, bx - ax)
    c.save(); c.translate((ax + bx) / 2, (ay + by) / 2); c.rotate(ang)
    L = math.hypot(bx - ax, by - ay) + 40 * s + 2 * BLIND_W[0] * s
    if BLIND_W[0]:                                           # a few slats gathered under the head rail, in front (a raised blind's stack)
        for i in range(3):
            rect(k, -L / 2 + 6 * s, (6 + i * 5.5) * s, L - 12 * s, 5.5 * s, dp.SLAT, 4820 + i, shadow=False, lw=1.6)
    rect(k, -L / 2, -6 * s, L, 12 * s, (0.70, 0.70, 0.66), 4813, shadow=False, lw=2)
    c.restore()


def phone_lit(k, x, y, s):
    rect(k, x - 22 * s, y - 6 * s, 44 * s, 12 * s, (0.15, 0.15, 0.17), 811, shadow=False, lw=1.6)
    c = k.c; c.set_source_rgba(1.0, 0.95, 0.70, 0.9); c.rectangle(x - 18 * s, y - 4 * s, 36 * s, 6 * s); c.fill()


def tape_floor(c, x, F, w=26, lean=30, h=110):
    c.set_source_rgb(*TAPE); c.new_path(); c.move_to(x - w / 2, F); c.line_to(x + w / 2, F)
    c.line_to(x + w / 2 + lean, F + h); c.line_to(x - w / 2 + lean, F + h); c.close_path(); c.fill()


def _label(c, s, x, y, size=16, col=INK):
    c.select_font_face("Inter", 0, 1); c.set_font_size(size); c.set_source_rgb(*col)
    e = c.text_extents(s); c.move_to(x - e.x_advance / 2, y); c.show_text(s)


def sheet(out):
    W, H = 2400, 1300
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H * 2); surf.set_device_scale(2, 2)
    c = cairo.Context(surf); c.set_source_rgb(*kit.WALL); c.paint()
    F = 900
    c.set_source_rgb(*kit.FLOOR); c.rectangle(0, F, W, 200); c.fill()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(30); c.set_source_rgb(*INK); c.move_to(40, 50)
    c.show_text("PICK A SIDE · PAM & MOM · their looks as ever, this episode's poses and props · v2")
    c.select_font_face("Inter", 0, 0); c.set_font_size(18); c.move_to(40, 84)
    c.show_text("Pam: her blue mug (12) · the half salute off the cup · the cup at her chin · frozen on the stool · the reach to her phone   "
                "Mom: feet together on the tape, arms folded, chin up · the one hand (hands_ps)")
    S = 0.54 * 1.5
    xs = [150, 390, 630, 870, 1130, 1420, 1720, 1980, 2240]
    T = F                                                                                            # the floor's back edge
    F = F + 40                                                                                       # feet on the floor, not on its edge
    pam(k, xs[0], F, S, "cup_mid", "frozen", (0, -0.2))                                              # 1.2
    pam(k, xs[1], F, S, "cross", "neutral", (1, 0), lean=8)                                          # 2.4
    pam(k, xs[2], F, S, "half_salute", "quiet", (-0.6, 0))                                           # 2.5a
    pam(k, xs[3], F, S, "cup_chin", "happy", (-0.6, 0.2))                                            # 2.5b
    pam(k, xs[4], F, S, "cup_chin", "doubt", (-1, 0))                                                # 3.7
    stool(k, xs[5], F, S)                                                                            # 5.6
    st = F - 98 * S
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4); kt = Ctx(cairo.Context(tmp), 0)
    hh = pam(kt, xs[5], st, S, "rail", "frozen", (1, -0.1))["hands"]
    blind_rail(k, hh[0], hh[1], S)
    o = pam(k, xs[5], st, S, "rail", "frozen", (1, -0.1), late=False)
    rail_bar(k, o["hands"][0], o["hands"][1], S)
    hp.redraw_late(k)                                                                                # the fists round the rail
    tape_floor(c, xs[6] + 60, T, lean=30, h=150)                                                                    # 6.1: across the line
    o = pam(k, xs[6] - 30, F, S, "reach", "avert", (1, 0.4), mug=False)
    phone_lit(k, o["hands"][1][0] + 40, o["hands"][1][1] + 18, S)
    tape_floor(c, xs[7] - 24, T, w=46, lean=50, h=150)                                                           # 2.6 Mom
    mom(k, xs[7], F, S, "folded", "unimpressed", (-1, 0), chin=True)
    tape_floor(c, xs[8] - 24, T, w=46, lean=50, h=150)                                                           # 6.1 Mom, turned away
    mom(k, xs[8], F, S, "folded", "stern", (1, -0.2), chin=True)
    for x, n, note in zip(xs, ("1.2", "2.4", "2.5", "2.5", "3.7", "5.6", "6.1", "2.6", "6.1"),
                          ("the cup stops halfway", "first across, to Don", "two fingers off the cup", "the smile into the cup",
                           "\"Some pose. Others notice.\"", "frozen on the blind", "the reach for her phone",
                           "\"I don't pick sides, Donnie.\"", "on the tape, her eyes away")):
        _label(c, n, x, F + 110, 20); _label(c, note, x, F + 136, 14, (0.3, 0.3, 0.3))
    surf.write_to_png(out); print("wrote", out)


def phone(out):
    frames = []
    for name, txt in (("two-shot", "2.5: \"Pam. My general.\""), ("close", "3.7: \"Some pose. Others notice.\""),
                      ("medium", "2.6: \"I don't pick sides, Donnie.\"")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        c.set_source_rgb(*kit.WALL); c.paint()
        if name == "two-shot":
            dp.don(k, 150, 860, 0.60 * 1.9, "salute", "pleased", (0.6, 0), chin=1)
            pam(k, 390, 860, 0.54 * 1.9, "half_salute", "quiet", (-0.6, 0))
        elif name == "close":
            pam(k, 270, 1130, 0.54 * 4.5, "cup_chin", "doubt", (-1, 0))
        else:
            c.set_source_rgb(*kit.FLOOR); c.rectangle(0, 800, 540, 160); c.fill()
            tape_floor(c, 250, 800, w=70, lean=60, h=160)
            mom(k, 270, 860, 0.54 * 1.8, "folded", "unimpressed", (-1, 0), chin=True)
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s_ = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s_); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s_.write_to_png(out); print("wrote", out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../pick-a-side"
    os.makedirs(d, exist_ok=True)
    sheet(os.path.join(d, "ps_pam_mom_v2.png"))
    phone(os.path.join(d, "ps_pam_mom_phone_v2.png"))
