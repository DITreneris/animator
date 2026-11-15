"""v2 (v1 pinned in ss_set_sheet_v1.py), after the director's audit: 5 re-staged (Pam left, Don turned to Sofia
at the right edge, the heart rises on Pam's side); 6 gets a target for Don's look (Sofia's earring at the frame edge);
12 becomes a high angle from Pam's point of view; 14 becomes Pam's silent ECU (the robot's pride moves into 15);
15 keeps the red present in Pam's hands, the tag still tied on; 1 and 16 show Pam's purple sleeve and her gold bead
chain, so the loop is hers; bigger handwritten names on the tag; a bigger alert icon; 4 a small head lift.
v1: Set sheet for "Secret Santa" (ss_set.py) with the four locked looks (sofia_ss, pam_ss v2, don_ss v2 option C,
robot_ss) and the camera plan: one 9:16 frame for each of the 16 shots. Writes ss_set_sheet_v1.png at 2400x1800
(drawn at 1200x900, 2x)."""
import sys
import math
import cairo
import kit
import brand
import ss_set as S
import sofia_ss as so
import pam_ss as ps
import don_ss as ds
import robot_ss as rs
import props_ss as props
import pam_sheet_ss as pss
import sofia_sheet_ss as sfs
import emoji as _emoji
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush
from sofia_sheet_mf import HY as SHY

W2, H2 = 1200, 900
GREY = (0.35, 0.40, 0.50)
U = 540 / 98.0              # screen-space frames are drawn in 98 x 174 units (the sheets' crop boxes)
X = S.POS


def tag(k, x, y, s, bars=(), rot=-0.05, blank=False, style=2):
    pss.k = k
    pss.gift_tag(k.c, x, y, s, rot=rot, bars=bars, blank=blank, bar_style=style, big=True)


def pop(k, x, y, r):
    c = k.c
    c.set_source_rgba(0, 0, 0, 0.12); c.arc(x + 3, y + 4, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(1.0, 0.91, 0.93); c.arc(x, y, r, 0, 2 * math.pi); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
    _emoji.draw_emoji(c, "\U0001F497", x, y, r * 1.25)


def sofia_seated(k, pose="stand", face="neutral", **kw):
    o = {}
    S.seated(k, lambda: o.update(so.sofia(k, X["sofia"], S.SEAT, 1.0, pose, face, seed=95, **kw)))
    return o


# ---------------------------------------------------------------- world-space shots
def wide(k, t=0.3):
    S.backdrop(k, t=t)
    sofia_seated(k, "stand", "unimpressed", look=(-1, 0.1))
    S.desk(k)
    rs.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "eager")
    ds.don(k, X["don"] - 20, S.FEET - 30, 1.0, "stand", "smug", look=(1, 0))
    ps.pam(k, X["pam"], S.FEET, 1.0, ps.POSE_SHY, "hopeful", look=(-1, -0.1), glasses="chain")
    S.santa_table(k)


def shot2(k):               # tight over the shoulder into the compact: Pam puts it on, Sofia's knowing smile
    S.backdrop(k, t=0.2)
    sofia_seated(k, "compact", "knowing", look=(-0.8, 0.1), compact_open=1.0, sparkle=0.3)
    S.desk(k)
    ps.pam(k, X["pam"] + 40, S.FEET, 1.0, "stand", "neutral", look=(0.6, 0.2), apply=True)


def shot3(k):               # LOW + DUTCH: the door bangs open, Agent Santa, the robot THUNKs APPROVED
    S.backdrop(k, door_open=1.0)
    rs.robot(k, X["robot"], S.FEET_BACK, 1.0, rs.POSE_CLIP, "tick", clip=True)
    ds.don(k, X["door"] + 40, S.FEET, 1.0, ds.POSE_WIDE_CARD, "showman", card="hand")
    S.santa_table(k)


def shot4(k):               # MCU Pam: glasses off, one step forward
    S.backdrop(k)
    ps.pam(k, X["pam"] - 40, S.FEET, 1.0, ps.POSE_GLASSES_OUT, "hopeful", look=(-1, -0.35), glasses="hand", lean=2)


def shot5(k):               # two-shot Pam and Don: one heart; his eyes already past her
    S.backdrop(k)
    sofia_seated(k, "stand", "neutral", look=(-1, 0.1))
    S.desk(k)
    o = ps.pam(k, X["don"] + 30, S.FEET, 1.0, ps.POSE_SHY, "hopeful", look=(1, -0.1), glasses="chain", lean=4)
    ds.don(k, X["pam"] + 20, S.FEET, 1.0, "stand", "neutral", look=(1, -0.1), lean=4)   # turned to Sofia, past Pam
    hx, hy = o["head"]
    pop(k, hx - 18, hy - 78, 22)                     # her heart, on her side, away from him


def shot10(k):              # CU robot, level, centred: PERSONAL DATA DETECTED
    S.backdrop(k)
    rs.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "personal")


def shot14(k):              # v2: ECU Pam, silent: eyes on the barred tag, a twitch, then nothing (music gone)
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
    ps.pam(k, 49, 78 - ps.HY * 1.5, 1.5, "stand", "pressed", look=(0.1, 1.0), glasses="chain")
    tag(k, 50, 166, 1.3, ("from", "to", "kiss"), rot=0.03)


def shot15(k):              # two-shot Pam and the robot, still; behind: Don preens at Sofia, she turns away
    S.backdrop(k)
    sofia_seated(k, "stand", "unimpressed", look=(1, 0.1), lean=4, lag=(-5, 0))
    S.desk(k)
    ds.don(k, X["sofia"] - 120, S.FEET - 40, 0.9, "stand", "smug", look=(1, -0.2), lean=6)
    rs.robot(k, X["robot"] + 30, S.FEET_BACK, 1.0, "stand", "tick")
    ps.pam(k, X["don"], S.FEET, 1.0, ps.POSE_SHY, "incredulous", look=(-0.6, 0.5))
    S.santa_table(k, pams=False)
    S.present(k, X["don"] + 2, S.FEET - 112, 64, 50, S.RED, S.GOLD, 966)         # her present, in her hands
    tag(k, X["don"] + 30, S.FEET - 150, 1.0, ("from", "to", "kiss"), rot=0.18)


# ---------------------------------------------------------------- screen-space shots (98 x 174 units)
def soft_sofia(k, x, face="eyebrow", look=(0.8, 0)):
    def bg(lc):
        so.sofia(Ctx(lc, 0), x + 82, 52 - SHY * 0.8, 0.8, "stand", face, look=look, badge=False, seed=95)
    props.soft(k.c, bg, 1.8)


def wall_bg(k):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()


def pam_hand(k, uncap=0.0):
    """v2: Pam's hand, bigger purple sleeve with a button cuff, and her gold bead glasses chain swinging into the
    frame from the top left: whose hand it is reads at once."""
    c = k.c
    import pam_mf as pm
    x, y = 98 * 0.24, 174 * 0.74
    kit.cut(k, [(x - 34, 190), (x + 30, 190), (x + 24, y + 20), (x - 26, y + 20)], pm.PURPLE, shadow=False, lw=2)
    kit.rect(k, x - 25, y + 20, 49, 9, pm.PURPLE_DARK, 4, shadow=False, lw=1.6)
    kit.ellipse(k, x + 14, y + 25, 3.2, 3.2, pm.BUTTON, 5, shadow=False, lw=1.2)
    c.set_source_rgb(*pm.GOLD)
    for i in range(22):                              # the bead chain swinging in from the top-left edge
        t = i / 21
        bx, by = -3 + 40 * t, 18 + 96 * t + 22 * math.sin(math.pi * t)
        c.set_source_rgb(*INK); c.arc(bx, by, 2.9, 0, 2 * math.pi); c.fill()
        c.set_source_rgb(*pm.GOLD); c.arc(bx, by, 2.2, 0, 2 * math.pi); c.fill()
    sfs.pam_hand_lipstick(k, x, y, 1.0, uncap)


def shot1(k):               # ECU: Pam's hand uncaps the lipstick, Sofia soft behind, the earring's glint
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
    def bg(lc):
        so.sofia(Ctx(lc, 0), 98 * 0.40, 174 * 0.34 - SHY * 1.0, 1.0, "stand", "neutral", look=(-0.6, 0.1),
                 lag=(3, 0), badge=False, sparkle=1.0)
    props.soft(c, bg, 1.5)
    pam_hand(k, 0.0)


def shot6(k):               # CU Don over Pam's shoulder: shades down, the dome, the robot's tick soft behind
    wall_bg(k)
    def bg(lc):
        rs.robot(Ctx(lc, 0), 90, 150, 0.42, "stand", "tick", seed=93)
    props.soft(k.c, bg, 1.8)
    def tgt(lc):                                     # Sofia at the right edge: blonde hair and her earring
        so.sofia(Ctx(lc, 0), 132, 60 - SHY * 0.9, 0.9, "stand", "unimpressed", look=(-1, 0.1), badge=False, seed=96)
    props.soft(k.c, tgt, 1.6)
    props.sparkle(k.c, 92, 74, 7, 1.0)
    ds.don(k, 40, 300, 0.85, ds.POSE_SMOOTH, "smug", look=(1, 0), shades="down", glint=True, mouth="E", seed=95)
    def fg(lc):
        ps.pam(Ctx(lc, 0), -26, 330, 1.1, "stand", "hopeful", look=(1, 0), glasses="chain", seed=94)
    props.soft(k.c, fg, 2.4)


def shot7(k):               # CU Pam, Sofia soft behind: 7A hurt, then 7B decides
    wall_bg(k)
    soft_sofia(k, 0)
    ps.pam(k, 40, 112 - ps.HY * 1.05, 1.05, "stand", "hurt", glasses="chain")


def shot8(k):               # ECU the tag: TO: DON, FROM: PAM, the kiss
    c = k.c
    c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(0, 0, 98, 174); c.fill()
    c.set_source_rgb(*S.RED); c.rectangle(-10, 118, 120, 70); c.fill()            # the present under it
    c.set_source_rgb(*S.GOLD); c.rectangle(40, 118, 14, 70); c.fill()
    tag(k, 50, 88, 2.2, rot=-0.04)


def shot9(k):               # CU Pam: proud, eyes on the tag
    c = k.c
    c.set_source_rgb(1.0, 0.94, 0.95); c.rectangle(0, 0, 98, 174); c.fill()
    ps.pam(k, 49, 84 - ps.HY * 1.12, 1.12, "stand", "proud", glasses="chain")
    tag(k, 52, 168, 1.25, rot=-0.04)


def hit(k, x, y, s, bar, wt, lift=16):
    bc = {"from": (3, 8), "to": (1, -10), "kiss": (23, 8)}[bar]
    bx, by = x + bc[0] * s, y + bc[1] * s
    rs.stamp_prop(k, bx, by - lift * s / 1.15, 0.42 * s, "up", 0.0, 7)
    rs.impact_lines(k.c, bx, by, wt, 0.42 * s)


def table_top(c, y):
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, y); c.fill()
    c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(0, y, 98, 200); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(0, y); c.line_to(98, y); c.stroke()


def shot11(k):
    table_top(k.c, 40); tag(k, 49, 112, 2.0, ("from",), rot=0); hit(k, 49, 112, 2.0, "from", 1)


def shot12(k):              # v2: high angle, Pam's point of view: the tag on the cloth, her cuffs at the bottom
    import pam_mf as pm
    c = k.c
    c.set_source_rgb(0.97, 0.97, 0.95); c.rectangle(0, 0, 98, 174); c.fill()
    c.set_source_rgb(0.86, 0.86, 0.83); c.set_line_width(1.2)
    for gx in range(-20, 120, 16):                   # the cloth's folds, converging: we look down
        c.move_to(gx, 0); c.line_to(49 + (gx - 49) * 1.4, 174); c.stroke()
    c.save(); c.translate(49, 92); c.scale(1, 0.82); c.translate(-49, -92)
    tag(k, 49, 92, 2.4, ("from", "to"), rot=0.08)
    c.restore()
    for sx in (-1, 1):                               # her purple cuffs and hands at the bottom of the frame
        cx_ = 49 + sx * 34
        kit.cut(k, [(cx_ - 16, 180), (cx_ + 16, 180), (cx_ + 12, 150), (cx_ - 12, 150)], pm.PURPLE, shadow=False, lw=2)
        kit.ellipse(k, cx_ - sx * 2, 146, 11, 9, pm.SKIN, 6, shadow=False, lw=2)
    c.save(); c.translate(52, 28); c.scale(1, 0.62)  # the stamp from above: knob, block, coming down at the top
    rs.stamp_prop(k, 0, 0, 1.1, "up", 0.0, 7)
    c.restore()
    rs.impact_lines(c, 50, 72, 2, 1.1)


def shot13(k):              # over the robot's shoulder: the stamp hangs still over the kiss
    table_top(k.c, 70)
    tag(k, 60, 128, 1.8, ("from", "to"), rot=0)
    rs.stamp_prop(k, 74, 96, 1.1, "up", 0.0, 9)
    def bg(lc):
        rs.robot(Ctx(lc, 0), -10, 300, 1.2, rs.POSE_HOVER, "thinking", head_rot=-0.18, t=0.4, seed=92)
    props.soft(k.c, bg, 2.0)


def shot16(k):              # ECU: the same framing as frame 0: a fresh blank tag, the uncap
    c = k.c
    def bg(lc):
        k2 = Ctx(lc, 0)
        lc.save(); lc.scale(1 / U, 1 / U); lc.translate(270, 480); lc.scale(2.2, 2.2); lc.translate(-760, -470)
        S.wall(k2); S.fairy_lights(k2, t=0.8); S.desk(k2)
        lc.restore()
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()
    props.soft(c, bg, 1.5)
    tag(k, 60, 120, 1.15, blank=True, rot=0.06)
    pam_hand(k, 0.0)


FRAMES = [("1 frame 0", shot1, None, "ECU, the uncap"),
          ("2 \"mirrors\"", shot2, (700, 470, 1.9), "tight OTS, compact"),
          ("3 Agent Santa", shot3, (150, 460, 1.55, -0.12), "LOW + DUTCH"),
          ("4 glasses off", shot4, (560, 470, 2.4), "MCU Pam"),
          ("5 one heart", shot5, (585, 480, 1.55), "2-shot, Don past her"),
          ("6 \"a mirror\"", shot6, None, "CU Don, OTS Pam"),
          ("7 hurt / decides", shot7, None, "CU Pam, Sofía soft"),
          ("8 the tag", shot8, None, "ECU insert"),
          ("9 proud", shot9, None, "CU Pam + tag"),
          ("10 detected", shot10, (S.POS["robot"], 418, 3.6), "CU robot, level"),
          ("11 sender", shot11, None, "insert, THUNK"),
          ("12 recipient", shot12, None, "HIGH, Pam POV"),
          ("13 the kiss", shot13, None, "OTS robot, hover"),
          ("14 silence", shot14, None, "ECU Pam, no music"),
          ("15 You're welcome", shot15, (380, 500, 1.65), "2-shot, still"),
          ("16 attempt two", shot16, None, "ECU = frame 0")]


def frame(c, k, x, y, sc, cam, draw):
    c.save(); c.rectangle(x, y, 540 * sc, 960 * sc); c.clip()
    c.translate(x, y); c.scale(sc, sc)
    if cam is None:
        c.scale(U, U)
    else:
        S.with_cam(c, cam)
    draw(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, 540 * sc, 960 * sc); c.stroke()


def main(out):
    rs.BIG_ICON = True
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE OFFICE AT CHRISTMAS", 68, 44, 28, bold=True)
    corp(c, "\"Secret Santa\"  ·  door, Secret Santa table, Sofía's desk  ·  no tree", 470, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · SET SHEET · SECRET SANTA v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. world view
    corp(c, "THE SET (WORLD VIEW)  ·  shot 5 as staged", 24, 92, 10, bold=True)
    c.save(); c.rectangle(24, 98, 590, 330); c.clip()
    c.translate(24, 98); c.scale(0.58, 0.58); c.translate(-10, -190)
    wide(k)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(24, 98, 590, 330); c.stroke()
    corp(c, "Door far left · the robot · the Secret Santa table (Pam's present + 2) · Sofía's desk under the lights.",
         24, 444, 9, col=GREY)

    # 2. details
    corp(c, "DETAILS", 24, 476, 10, bold=True)
    def det(x, w, h, draw, label):
        c.save(); c.rectangle(x, 482, w, h); c.clip()
        c.set_source_rgb(*kit.WALL); c.paint()
        draw()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, 482, w, h); c.stroke()
        corp(c, label, x, 482 + h + 12, 8.5, col=GREY, bold=True)
    def d1():
        c.save(); c.translate(24 + 95, 482 + 75); c.scale(0.95, 0.95); c.translate(-330, -318)
        S.santa_sign(k); c.restore()
    det(24, 190, 150, d1, "the sign: marker, tape, HR-APPROVED")
    def d2():
        c.save(); c.translate(222 + 100, 482 + 60); c.scale(1.05, 1.05); c.translate(-430, -S.TABLE_TOP - 20)
        S.santa_table(k); c.restore()
    det(222, 200, 150, d2, "the table: hers is the big red one")
    def d3():
        c.save(); c.translate(430 + 92, 482 + 70); c.scale(0.62, 0.62); c.translate(-560, -300)
        S.paper_chains(k, 380, 760, 260); S.fairy_lights(k, 380, 760, 360, t=0.5); c.restore()
    det(430, 184, 150, d3, "chains (one sags) · fairy lights")

    # 3. the camera plan
    corp(c, "THE CAMERA PLAN  (16 shots, about 36 s; close-ups carry faces, inserts carry the tag; one dutch angle)",
         634, 92, 10, bold=True)
    sc = 0.158
    for i, (lab, fn, cam, kind) in enumerate(FRAMES):
        x, y = 634 + (i % 6) * 91, 98 + (i // 6) * 196
        frame(c, k, x, y, sc, cam, fn)
        corp(c, lab, x, y + 960 * sc + 11, 8, col=INK, bold=True)
        corp(c, kind, x, y + 960 * sc + 22, 8, col=GREY)

    # 4. notes
    corp(c, "NOTES", 24, 680, 10, bold=True)
    notes = ["Festive but not Happy Compliance: red/green paper chains (one sags), the hand-drawn sign, fairy lights. No tree.",
             "Eye-lines carry the triangle: Pam looks at Don (5), Don looks past her to Sofía (5, 6: her earring at the edge).",
             "Pam's red present stays with her tag through the payoff: on the table (8-13), in her hands (15).",
             "12 is the one high angle, from Pam's eyes: the second bar lands on the name she wrote. One dutch: 3.",
             "14 is Pam's silent ECU: music gone after the last stamp, eyes on the tag, a twitch, then nothing.",
             "15 holds still: glasses back on (the payoff of 4), the robot beams on \"He won't.\", the tick on \"You're welcome.\"",
             "1 and 16 are the same ECU with Pam's purple sleeve and her bead chain: the loop is visibly hers."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 24, 702 + i * 22, 10, col=INK)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ss_set_sheet_v2.png")
