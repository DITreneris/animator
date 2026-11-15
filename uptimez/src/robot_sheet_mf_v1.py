"""v1 (pinned; robot_sheet_mf.py writes v2). HR ROBOT model sheet for "Mandatory Fun" (robot_mf.py). Writes robot_sheet_mf_v1.png at 2400x1560 (drawn at
1200x780, 2x): no costume, the five screen states plus the approval flash, the scan beam (6 on Don, 12 on Pam), the
cuffs, the turn and nod to Pam, and a phone-size check in the film's seating (robot by the slide, Don, Pam)."""
import sys
import math
import cairo
import kit
import brand
import waiter_kit as w
import robot_tg as rt
import robot_mf_v1 as rm
import don_mf as dm
import pam_mf as pm
import props_mf as pr
from kit import Ctx, INK
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.93, 0.95)
LABELS = []


def boxed(c, x, y, w_, h, label=None, fill=(1, 1, 1)):
    c.set_source_rgb(*fill); c.rectangle(x, y, w_, h); c.fill()
    c.set_source_rgb(0.85, 0.83, 0.78); c.set_line_width(1); c.rectangle(x, y, w_, h); c.stroke()
    LABELS.append((x, y, w_, h, label))


def flush(c):
    for x, y, w_, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 17, w_ - 2, 16); c.fill()
            corp(c, label, x + 6, y + h - 5, 9, col=GREY)
    LABELS.clear()


def table(c, x, y, w_, h=60):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w_, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w_, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w_, h); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w_, h); c.stroke()


_SY = None


def head_only(k, cx, cy, s, state, **kw):
    """The robot with its screen centred on (cx, cy); the caller clips away the body."""
    global _SY
    if _SY is None:                                       # screen height above the feet, measured once off-screen
        ds = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
        _SY = rm.robot(Ctx(cairo.Context(ds), 0), 0, 0, 1.0, "stand", "eager")["screen"][1]
    rm.robot(k, cx, cy - _SY * s, s, "stand", state, **kw)


def ding(c, x, y, s=1.0):
    c.set_source_rgb(*rm.GREEN); c.set_line_width(2 * s); c.set_line_cap(1)
    for a in (-1.0, -0.5, 0.0, 0.5, 1.0):
        c.move_to(x + 30 * s * math.sin(a), y - 30 * s * math.cos(a))
        c.line_to(x + 38 * s * math.sin(a), y - 38 * s * math.cos(a)); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "HR ROBOT", 68, 44, 28, bold=True)
    corp(c, "\"Mandatory Fun\"  ·  treats fun as an auditable requirement  ·  one flat tone", 218, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · MANDATORY FUN v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    rm.robot(k, 144, 500, 1.12, "stand", "eager", seed=71)
    corp(c, "FRONT · NO COSTUME, HR BADGE ONLY", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. lineage
    corp(c, "WAITER (IWRY)  ·  HR PILGRIM (TG)  ·  MANDATORY FUN", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    w.robot(k, 345, 296, 0.52, "stand", "eager", seed=72)
    rt.robot(k, 449, 296, 0.52, "stand", "eager", seed=72)
    rm.robot(k, 553, 296, 0.52, "stand", "eager", seed=72)
    c.restore()
    corp(c, "Same shell, wheel, bow tie, big HR badge. The hat is gone: the screens and the slide are the jokes.", 290,
         322, 9, col=GREY)

    # 3. screen states
    corp(c, "SCREEN STATES  (colour, icon, two words, glow)", 284, 348, 10, bold=True)
    states = [("eager", "idle"), ("scan", "scan"), ("insufficient", "6: red"), ("approval", "8: amber"),
              ("detected", "12: green")]
    for i, (st, lab) in enumerate(states):
        x, y = 284 + i * 66, 354
        boxed(c, x, y, 63, 92, lab)
        c.save(); c.rectangle(x, y, 63, 92); c.clip()
        head_only(k, x + 31, y + 38, 0.56, st, t=0.45)
        c.restore()
    corp(c, "9: ACCEPTS PAM  ·  PHONE SIZE: the three words at two-shot size", 284, 466, 9, col=GREY, bold=True)
    boxed(c, 284, 472, 63, 60, "9: green")
    c.save(); c.rectangle(284, 472, 63, 60); c.clip()
    head_only(k, 315, 500, 0.5, "approved")
    c.restore()
    c.set_source_rgb(*kit.WALL); c.rectangle(351, 472, 263, 60); c.fill()
    c.save(); c.rectangle(351, 472, 263, 60); c.clip()
    for j, st in enumerate(("insufficient", "approval", "detected")):
        head_only(k, 395 + j * 88, 496, 0.3, st)
    c.restore()

    # 4. beats
    corp(c, "BEATS  (robot by the slide on the left; the beam crosses Don to reach Pam)", 634, 92, 10, bold=True)
    beats = ["6: scans Don's sulk", "8: lifts the cuffs, freezes", "9: turns to Pam, nods, DING", "12: scans Pam, skips Don"]
    for i, lab in enumerate(beats):
        x = 634 + i * 137
        boxed(c, x, 98, 133, 210, lab, fill=(1, 1, 1))
        c.save(); c.rectangle(x, 98, 133, 210); c.clip()
        if i == 0:
            d = dm.don(k, x + 104, 300, 0.34, dm.POSE_CROSS, "pout", look=(-1, 0), seed=81)
            o = rm.robot(k, x + 34, 290, 0.5, "stand", "scan", t=0.6, seed=82)
            rm.scan_beam(k, o["screen"], d["head"], 50 * 0.34, 0.55)
        elif i == 1:
            o = rm.robot(k, x + 60, 290, 0.5, rm.POSE_CUFFS, "approval", cuffs=True, seed=83)
        elif i == 2:
            p_ = pm.pam(k, x + 108, 300, 0.34, pm.POSE_APPROVE, "approve", glasses="flash", seed=84)
            o = rm.robot(k, x + 40, 290, 0.5, "stand", "approved", head_rot=0.16, head_dx=4, seed=85)
            ding(c, o["screen"][0], o["screen"][1], 0.5)
        else:
            d = dm.don(k, x + 70, 300, 0.3, dm.POSE_STIFF, "panic", belt_cuffs_on=False, seed=86)
            p_ = pm.pam(k, x + 112, 300, 0.3, "stand", "happy", seed=87)
            o = rm.robot(k, x + 24, 290, 0.44, "stand", "detected", seed=88)
            rm.scan_beam(k, o["screen"], p_["head"], 50 * 0.3, 0.6, col=rm.GREEN)
        c.restore()

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    boxed(c, 634, 354, 170, 178, "icons: thick, outlined, one per state")
    for j, (ic, col) in enumerate((("x", rm.RED), ("warn", rm.AMBER), ("tick", rm.GREEN))):
        c.set_source_rgb(0.08, 0.12, 0.22); c.arc(667 + j * 52, 432, 22, 0, 2 * math.pi); c.fill()
        rm.icon(c, ic, 667 + j * 52, 432, 12, col)
    boxed(c, 812, 354, 170, 178, "one beam: 6 (Don, fail) = 12 (Pam)")
    c.save(); c.rectangle(812, 354, 170, 160); c.clip()
    o = rm.robot(k, 846, 600, 0.75, "stand", "scan", t=0.3, seed=89)
    pm.pam(k, 950, 600, 0.6, "stand", "happy", seed=90)
    hy_ = 600 + pm.HY * 0.6
    rm.scan_beam(k, o["screen"], (950, hy_), 50 * 0.6, 0.62)
    c.restore()
    boxed(c, 990, 354, 186, 178, "the nod: head dips, screen ticks, DING")
    c.save(); c.rectangle(990, 354, 186, 160); c.clip()
    rm.robot(k, 1040, 640, 0.8, "stand", "approval", seed=91)
    o = rm.robot(k, 1126, 640, 0.8, "stand", "approved", head_rot=0.16, head_dx=4, seed=92)
    ding(c, o["screen"][0], o["screen"][1], 0.8)
    c.set_source_rgb(*GREY); c.set_line_width(1.6); c.move_to(1074, 438); c.line_to(1092, 438); c.stroke()
    c.move_to(1092, 438); c.line_to(1086, 434); c.move_to(1092, 438); c.line_to(1086, 442); c.stroke()
    c.restore()

    # 6. phone-size check
    corp(c, "PHONE-SIZE CHECK  (6: scan on Don  ·  8-9: turns to Pam, APPROVED  ·  12: scans Pam, FUN DETECTED)", 24, 556,
         10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    o = rm.robot(k, 64, 740, 0.42, "stand", "insufficient", seed=95)
    d = dm.don(k, 150, 770, 0.38, dm.POSE_CROSS, "pout", look=(-1, 0), seed=96)
    o2 = rm.robot(k, 240, 740, 0.42, "stand", "approved", head_rot=0.16, head_dx=4, seed=97)
    pm.pam(k, 330, 760, 0.42, pm.POSE_APPROVE, "approve", glasses="flash", seed=98)
    o3 = rm.robot(k, 420, 740, 0.42, "stand", "detected", seed=99)
    d3 = dm.don(k, 494, 770, 0.38, dm.POSE_STIFF, "panic", belt_cuffs_on=False, seed=100)
    p3 = pm.pam(k, 574, 760, 0.42, pm.POSE_TABLE, "happy", seed=101)
    rm.scan_beam(k, o3["screen"], p3["head"], 50 * 0.42, 0.6, col=rm.GREEN)
    c.restore()
    table(c, 24, 700, 590)
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    dhx, phx = 494 + 22, 574 - 22
    for hx_ in (dhx, phx):
        kit.ellipse(k, hx_, 703, 4.2, 4.2, pm.SKIN, 7, shadow=False, lw=1.2)
    a_ = pr.cuff(k, dhx - 3, 697, 0.45, 0.0, loop_side=1)
    b_ = pr.cuff(k, phx + 3, 697, 0.45, 0.0, loop_side=-1)
    pr.chain(k, a_[0], a_[1], b_[0], b_[1], 0.45, sag=0.15)
    c.restore()

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["The robot from the last three films, no costume: shell, wheel, bow tie, big HR badge.",
             "Each verdict fills the screen: colour, a thick icon, two words, a glow. Then it speaks.",
             "6: the beam sweeps Don's sulk, then red. 12: the same beam on Pam, then green.",
             "8: it lifts Don's cuffs and freezes amber. It can't act alone; it turns to Pam.",
             "9: Pam shouts, its screen ticks green, APPROVER: PAM, a small nod, DING.",
             "One flat tone for everything, in every shot. It is never unkind, only thorough."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "robot_sheet_mf_v1.png")
