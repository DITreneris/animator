"""v1 (pinned). Set sheet for "Secret Santa" (ss_set.py) with the four locked looks (sofia_ss, pam_ss v2, don_ss v2 option C,
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
    pss.gift_tag(k.c, x, y, s, rot=rot, bars=bars, blank=blank, bar_style=style)


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
    ps.pam(k, X["pam"] - 40, S.FEET, 1.0, ps.POSE_GLASSES_OUT, "hopeful", look=(-1, 0), glasses="hand")


def shot5(k):               # two-shot Pam and Don: one heart; his eyes already past her
    S.backdrop(k)
    sofia_seated(k, "stand", "neutral", look=(-1, 0.1))
    S.desk(k)
    ds.don(k, X["don"] + 40, S.FEET, 1.0, "stand", "neutral", look=(1, 0))
    o = ps.pam(k, X["pam"], S.FEET, 1.0, ps.POSE_SHY, "hopeful", look=(-1, -0.1), glasses="chain", lean=-4)
    hx, hy = o["head"]
    pop(k, hx + 50, hy - 70, 22)


def shot10(k):              # CU robot, level, centred: PERSONAL DATA DETECTED
    S.backdrop(k)
    rs.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "personal")


def shot14(k):              # CU robot: pride, still
    S.backdrop(k)
    rs.robot(k, X["robot"], S.FEET_BACK, 1.0, "stand", "proud", head_rot=0.10)


def shot15(k):              # two-shot Pam and the robot, still; behind: Don preens at Sofia, she turns away
    S.backdrop(k)
    sofia_seated(k, "stand", "unimpressed", look=(1, 0.1), lean=4, lag=(-5, 0))
    S.desk(k)
    ds.don(k, X["sofia"] - 120, S.FEET - 40, 0.9, "stand", "smug", look=(1, -0.2), lean=6)
    rs.robot(k, X["robot"] + 30, S.FEET_BACK, 1.0, "stand", "tick")
    ps.pam(k, X["don"], S.FEET, 1.0, "stand", "incredulous", look=(-0.6, 0.5))
    S.santa_table(k, pams=False)
    tag(k, X["don"] - 4, S.FEET - 150, 1.2, ("from", "to", "kiss"), rot=0.04)


# ---------------------------------------------------------------- screen-space shots (98 x 174 units)
def soft_sofia(k, x, face="eyebrow", look=(0.8, 0)):
    def bg(lc):
        so.sofia(Ctx(lc, 0), x + 82, 52 - SHY * 0.8, 0.8, "stand", face, look=look, badge=False, seed=95)
    props.soft(k.c, bg, 1.8)


def wall_bg(k):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(0, 0, 98, 174); c.fill()


def shot1(k):               # ECU: Pam's hand uncaps the lipstick, Sofia soft behind, the earring's glint
    sfs.frame0(k, 0, 0, 98, 174, 0.0, 1.0, "")


def shot6(k):               # CU Don over Pam's shoulder: shades down, the dome, the robot's tick soft behind
    wall_bg(k)
    def bg(lc):
        rs.robot(Ctx(lc, 0), 90, 150, 0.42, "stand", "tick", seed=93)
    props.soft(k.c, bg, 1.8)
    ds.don(k, 44, 300, 0.85, ds.POSE_SMOOTH, "smug", look=(1, 0), shades="down", glint=True, mouth="E", seed=95)
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


def shot12(k):
    table_top(k.c, 40); tag(k, 57, 112, 2.5, ("from", "to"), rot=0); hit(k, 57, 112, 2.5, "to", 2)


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
    sfs.pam_hand_lipstick(k, 98 * 0.24, 174 * 0.74, 1.0, 0.0)


FRAMES = [("1 frame 0", shot1, None, "ECU, the uncap"),
          ("2 \"mirrors\"", shot2, (700, 470, 1.9), "tight OTS, compact"),
          ("3 Agent Santa", shot3, (150, 460, 1.55, -0.12), "LOW + DUTCH"),
          ("4 glasses off", shot4, (560, 470, 2.4), "MCU Pam"),
          ("5 one heart", shot5, (560, 480, 1.6), "2-shot"),
          ("6 \"a mirror\"", shot6, None, "CU Don, OTS Pam"),
          ("7 hurt / decides", shot7, None, "CU Pam, Sofía soft"),
          ("8 the tag", shot8, None, "ECU insert"),
          ("9 proud", shot9, None, "CU Pam + tag"),
          ("10 detected", shot10, (S.POS["robot"], 418, 3.6), "CU robot, level"),
          ("11 sender", shot11, None, "insert, THUNK"),
          ("12 recipient", shot12, None, "tighter, THUNK!"),
          ("13 the kiss", shot13, None, "OTS robot, hover"),
          ("14 pride", shot14, (S.POS["robot"], 418, 3.6), "CU robot, still"),
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
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE OFFICE AT CHRISTMAS", 68, 44, 28, bold=True)
    corp(c, "\"Secret Santa\"  ·  door, Secret Santa table, Sofía's desk  ·  no tree", 470, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · SET SHEET · SECRET SANTA v1"
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
             "The sign's little HR-APPROVED stamp plants the robot's stamp; the clipboard THUNK in 3 plants it again.",
             "Pam's present: red paper, gold ribbon, the big cream tag; two plainer gifts beside it so it stands out.",
             "Faces in close-up (6 Don, 7 and 9 Pam, 10 and 14 the robot); the tag in inserts (8, 11, 12, 13).",
             "One dutch angle only: 3, Don's entrance, low. The robot is always level and centred: deadpan.",
             "15 holds still (five beats inside one frame); 1 and 16 are the same ECU: the match cut of the loop.",
             "Normal office light; the fairy lights twinkle softly behind Sofía."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 24, 702 + i * 22, 10, col=INK)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ss_set_sheet_v1.png")
