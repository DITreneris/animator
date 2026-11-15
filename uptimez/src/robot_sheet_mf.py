"""v2 (robot_sheet_mf_v1.py writes v1 from robot_mf_v1.py). After the review: icon-first screens, the beats as
cause-and-effect pairs at one scale (6 sweep -> red, 8 cuffs insert -> turns to Pam, 9 Pam's thumbs-up -> tick +
DING, 12 the beam on Don does nothing -> on Pam, green), the lineage labelled, the robot visibly turned to Pam.
HR ROBOT model sheet for "Mandatory Fun" (robot_mf.py). Writes robot_sheet_mf_v2.png at 2400x1560 (drawn at
1200x780, 2x): no costume, the five screen states plus the approval flash, the scan beam (6 on Don, 12 on Pam), the
cuffs, the turn and nod to Pam, and a phone-size check in the film's seating (robot by the slide, Don, Pam)."""
import sys
import math
import cairo
import kit
import brand
import waiter_kit as w
import robot_tg as rt
import robot_mf as rm
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
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · MANDATORY FUN v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    rm.robot(k, 144, 500, 1.12, "stand", "eager", seed=71)
    corp(c, "FRONT · NO COSTUME, HR BADGE ONLY", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. lineage
    corp(c, "EARLIER: WAITER  ·  EARLIER: PILGRIM  ·  CURRENT", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    w.robot(k, 345, 296, 0.52, "stand", "eager", seed=72)
    rt.robot(k, 449, 296, 0.52, "stand", "eager", seed=72)
    rm.robot(k, 553, 296, 0.52, "stand", "eager", seed=72)
    c.restore()
    c.set_source_rgb(*brand.GREEN); c.set_line_width(2.4); c.rectangle(510, 104, 98, 198); c.stroke()
    corp(c, "PRODUCTION", 528, 118, 9, col=brand.GREEN, bold=True)
    corp(c, "Only the green-framed robot is the production model: no hat, HR badge only.", 290,
         322, 9, col=GREY)

    # 3. screen states
    corp(c, "SCREEN STATES  (icon first, words confirm)", 284, 348, 10, bold=True)
    states = [("eager", "idle"), ("scan", "scan"), ("insufficient", "6: red"), ("approval", "8: amber"),
              ("detected", "12: green")]
    for i, (st, lab) in enumerate(states):
        x, y = 284 + i * 66, 354
        boxed(c, x, y, 63, 92, lab)
        c.save(); c.rectangle(x, y, 63, 92); c.clip()
        head_only(k, x + 31, y + 38, 0.56, st, t=0.45)
        c.restore()
    corp(c, "9: JUST A TICK  ·  PHONE SIZE: colour and icon carry it", 284, 466, 9, col=GREY, bold=True)
    boxed(c, 284, 472, 63, 60, "9: green")
    c.save(); c.rectangle(284, 472, 63, 60); c.clip()
    head_only(k, 315, 500, 0.5, "approved")
    c.restore()
    c.set_source_rgb(*kit.WALL); c.rectangle(351, 472, 263, 60); c.fill()
    c.save(); c.rectangle(351, 472, 263, 60); c.clip()
    for j, st in enumerate(("insufficient", "approval", "detected")):
        head_only(k, 395 + j * 88, 496, 0.3, st)
    c.restore()

    # 4-5. the beats as cause -> effect, one scale (robot 0.42, Don 0.38, Pam 0.42), robot left, Pam right
    RS, DS, PS = 0.42, 0.38, 0.42
    corp(c, "CAUSE -> EFFECT  (6: sweep, then red  ·  8: Don's cuffs, then it turns to Pam)", 634, 92, 10, bold=True)
    corp(c, "CAUSE -> EFFECT  (9: Pam approves, then tick + DING  ·  12: nothing on Don, green on Pam)", 634, 348, 10,
         bold=True)
    frames = [("6a", "6a: the sweep on his sulk", None), ("6b", "6b: then red, held", (1.0, 0.93, 0.92)),
              ("8a", "8a: his cuffs, his empty belt", None), ("8b", "8b: freezes, turns to Pam", (1.0, 0.97, 0.88)),
              ("9a", "9a: Pam: thumbs up", None), ("9b", "9b: then tick, nod, DING", (0.93, 0.98, 0.93)),
              ("12a", "12a: beam on Don: nothing", None), ("12b", "12b: beam on Pam: FUN", (0.93, 0.98, 0.93))]
    for i, (key, lab, fill) in enumerate(frames):
        x = 634 + (i % 4) * 137
        y0 = 98 if i < 4 else 354
        hgt = 210 if i < 4 else 178
        boxed(c, x, y0, 133, hgt, lab, fill=fill or (1, 1, 1))
        c.save(); c.rectangle(x, y0, 133, hgt - 17); c.clip()
        fy = y0 + hgt - 10
        if key in ("6a", "6b"):
            d = dm.don(k, x + 100, fy + 20, DS, dm.POSE_CROSS, "pout", look=(-1, 0), seed=81)
            o = rm.robot(k, x + 34, fy, RS, "stand", "scan" if key == "6a" else "insufficient", t=0.6, seed=82)
            if key == "6a":
                rm.scan_beam(k, o["screen"], d["head"], 50 * DS, 0.55)
        elif key == "8a":                                   # insert: the toy cuffs big, Don's belt clip empty beside
            ds = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
            hx0, hy0 = rm.robot(Ctx(cairo.Context(ds), 0), 0, 0, 1.0, rm.POSE_CUFFS, "approval")["hands"][1]
            S8 = 1.0
            rm.robot(k, x + 46 - hx0 * S8, y0 + 46 - hy0 * S8, S8, rm.POSE_CUFFS, "approval", cuffs=True, seed=83)
            c.save(); c.translate(x + 100, y0 + 150)              # Don's belt, the clip empty (inset)
            c.set_source_rgb(0.78, 0.70, 0.52); c.rectangle(-34, -22, 68, 46); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(-34, -22, 68, 46); c.stroke()
            kit.rect(k, -34, -7, 68, 13, (0.30, 0.20, 0.12), 3, shadow=False, lw=1.6)
            c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(12, 6); c.line_to(12, 18); c.stroke()
            c.restore()
            corp(c, "Don's belt: empty", x + 68, y0 + 186, 8, col=GREY)
        elif key == "8b":
            p_ = pm.pam(k, x + 104, fy + 20, PS, "stand", "neutral", look=(-1, 0), seed=84)
            o = rm.robot(k, x + 38, fy, RS, rm.POSE_TURN_CUFFS, "approval", cuffs=True, seed=85, **rm.TURN_HEAD)
        elif key in ("9a", "9b"):
            p_ = pm.pam(k, x + 104, fy + 20, PS, pm.POSE_APPROVE, "approve", glasses="flash", thumb=True, seed=86)
            if key == "9a":
                o = rm.robot(k, x + 38, fy, RS, rm.POSE_TURN, "approval", seed=87, **rm.TURN_HEAD)
            else:
                o = rm.robot(k, x + 38, fy, RS, rm.POSE_TURN, "approved", seed=87, head_rot=0.0, head_dx=-10)
                ding(c, o["screen"][0], o["screen"][1], RS)
        else:
            d = dm.don(k, x + 72, fy + 20, DS * 0.9, dm.POSE_STIFF, "panic", belt_cuffs_on=False, seed=88)
            p_ = pm.pam(k, x + 114, fy + 20, PS * 0.9, "stand", "happy", seed=89)
            o = rm.robot(k, x + 24, fy, RS * 0.9, "stand", "scan" if key == "12a" else "detected", t=0.3, seed=90)
            tgt = d["head"] if key == "12a" else p_["head"]
            rm.scan_beam(k, o["screen"], tgt, 50 * DS * 0.9, 0.55, col=rm.CYAN if key == "12a" else rm.GREEN)
        c.restore()

    # 6. phone-size check
    corp(c, "PHONE-SIZE CHECK  (6: scan on Don  ·  8-9: turns to Pam, APPROVED  ·  12: scans Pam, FUN DETECTED)", 24, 556,
         10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    o = rm.robot(k, 64, 740, 0.42, "stand", "insufficient", seed=95)
    d = dm.don(k, 150, 770, 0.38, dm.POSE_CROSS, "pout", look=(-1, 0), seed=96)
    o2 = rm.robot(k, 240, 740, 0.42, rm.POSE_TURN, "approved", seed=97, **rm.TURN_HEAD)
    pm.pam(k, 330, 760, 0.42, pm.POSE_APPROVE, "approve", glasses="flash", thumb=True, seed=98)
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
    notes = ["Its rule: it never breaks HR policy; it applies it so literally that everyone else suffers.",
             "Screens: icon first (big), words small under it; colour carries it at phone size.",
             "Every verdict is an effect with a visible cause: sweep -> red, Pam's thumbs-up -> tick.",
             "9 is only a tick, so the one big green is 12: FUN DETECTED next to miserable Don.",
             "12: the same beam crosses Don (nothing happens), lands on Pam, flips green.",
             "No eyebrows, no tears, no legs, no extra screens. One flat tone for everything."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "robot_sheet_mf_v2.png")
