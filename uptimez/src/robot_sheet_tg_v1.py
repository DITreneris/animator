"""HR ROBOT model sheet for the Thanksgiving film "Raises for Everyone" (robot_tg.py). Writes robot_sheet_tg_v1.png
at 2400x1560 (drawn at 1200x780, 2x)."""
import sys
import cairo
import kit
import brand
import waiter_kit as w
import santa_robot as sr
import robot_tg_v1 as rt
import don_tg as dt
import pam_tg as pt
from kit import Ctx, INK, ellipse
from charsheets import corp

W2, H2 = 1200, 780
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.86, 0.90, 0.92)
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


def table(c, x, y, w_):
    c.set_source_rgb(0.55, 0.36, 0.22); c.rectangle(x, y, w_, 14); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y, w_, 14); c.stroke()
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y + 14, w_, 60); c.fill()
    c.set_source_rgb(*INK); c.rectangle(x, y + 14, w_, 60); c.stroke()


def head_at(k, cx, cy, s, state, look=(0, 0), t=0.0):
    return rt.robot(k, cx, cy - w.HEAD_Y * s, s, "stand", state, look=look, t=t, badge=False)


def leg_over(k, sx, sy, s, ls, bites=3):
    """Turkey leg held flat with the meat centred on the screen at (sx, sy); s = character scale."""
    L = s * ls
    hx = sx - 47 * L
    dt.turkey_leg(k, hx, sy, L, 0, bites, 620)
    ellipse(k, hx, sy, 10.5 * s, 10.5 * s, dt.SKIN, 621, shadow=False, lw=2 * s)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "HR ROBOT", 68, 44, 28, bold=True)
    corp(c, "Thanksgiving film \"Raises for Everyone\"  ·  judges truth, not loyalty", 222, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · THANKSGIVING v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    rt.robot(k, 144, 505, 1.12, "stand", "eager", seed=71)
    corp(c, "FRONT · PAPER PILGRIM HAT", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. lineage
    corp(c, "WAITER (IWRY)  ·  HR SANTA (XMAS)  ·  HR PILGRIM", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    w.robot(k, 345, 290, 0.5, "stand", "eager", seed=72)
    sr.robot(k, 449, 290, 0.5, "stand", "eager", seed=72)
    rt.robot(k, 553, 290, 0.5, "stand", "eager", seed=72)
    c.restore()
    corp(c, "Same robot, HR badge; the suit is off, the hat is folded paper.", 290, 322, 9, col=GREY)

    # 3. screen states
    corp(c, "SCREEN STATES  (the verdict IS the screen)", 284, 348, 10, bold=True)
    states = [("eager", "idle"), ("scan", "scanning"), ("violation", "shot 5"), ("accurate", "shot 10"),
              ("blocked", "shot 11: blocked")]
    for i, (st_, lab) in enumerate(states):
        x, y = 284 + i * 66, 354
        boxed(c, x, y, 63, 92, lab)
        c.save(); c.rectangle(x, y, 63, 76); c.clip()
        o = head_at(k, x + 31, y + 46, 0.55, "accurate" if st_ == "blocked" else st_, (0.6, 0), t=0.35)
        if st_ == "blocked":
            sx_, sy_ = o["screen"]
            leg_over(k, sx_, sy_, 0.55, 1.5)
        c.restore()
    corp(c, "PHONE-SIZE: the words at the smallest two-shot size", 284, 466, 9, col=GREY, bold=True)
    boxed(c, 284, 472, 330, 60)
    c.set_source_rgb(*kit.WALL); c.rectangle(285, 473, 328, 58); c.fill()
    c.save(); c.rectangle(285, 473, 328, 58); c.clip()
    for i, st_ in enumerate(("eager", "violation", "accurate")):
        head_at(k, 330 + i * 110, 500, 0.3, st_)
    c.restore()

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [("stand", "eager", 0, None, "behind Don"), ("stand", "violation", 6, 0.14, "5: snaps to Don"),
             ("stand", "scan", -6, -0.12, "10: scans Pam..."), ("stand", "scan", 6, 0.12, "...then Don"),
             ("stand", "accurate", 0, 0, "10: ACCURATE."), ("stand", "accurate", 0, 0, "11: blocked")]
    for i, (p, st_, hdx, hrot, lab) in enumerate(poses):
        x = 634 + i * 91
        boxed(c, x, 98, 87, 210, lab)
        c.save(); c.rectangle(x, 98, 87, 210); c.clip()
        o = rt.robot(k, x + 46, 284, 0.42, p, st_, look=(0.8 if hdx >= 0 else -0.8, 0), seed=80 + i,
                     head_dx=hdx, head_rot=hrot, t=0.4, side=-1 if p == "lock" else 1)
        if lab.startswith("11"):
            sx_, sy_ = o["screen"]
            leg_over(k, sx_, sy_, 0.42, 1.5)
        c.restore()

    # 5. size check with Don: the real leg vs the cheated leg
    corp(c, "SIZE CHECK WITH DON  (shot 11: his raised leg against the real screen)", 634, 348, 10, bold=True)
    for i, (ls, lab) in enumerate(((1.0, "real size: the word's ends peek out"), (1.5, "cheat 1.5x: the word is gone"))):
        bx = 634 + i * 274
        boxed(c, bx, 354, 268, 178, lab)
        c.save(); c.rectangle(bx, 354, 268, 160); c.clip()
        s = 0.48
        scratch = Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0)
        dx_, dy_ = bx + 90, 590
        hx, hy = dt.don(scratch, dx_, dy_, s, dt.POSE_BLOCK, "grin", seed=88)["hands"][1]
        sx_, sy_ = hx + 47 * s * ls, hy
        rt.robot(k, sx_, sy_ - w.HEAD_Y * s, s, "stand", "accurate", seed=89)
        dt.don(k, dx_, dy_, s, dt.POSE_BLOCK, "grin", look=(-0.6, 0.3), seed=88, leg=(3, 0, 1, ls))
        c.restore()

    # 6. phone-size two-shot behind the table
    corp(c, "PHONE-SIZE CHECK  (behind Don at the head of the table, as in shots 5, 10, 11)", 24, 556, 10, bold=True)
    c.set_source_rgb(*kit.WALL); c.rectangle(24, 562, 590, 190); c.fill()
    c.save(); c.rectangle(24, 562, 590, 190); c.clip()
    pt.pam(k, 80, 760, 0.42, "stand", "stare", look=(0.8, 0), seed=96)
    rt.robot(k, 250, 720, 0.42, "stand", "violation", seed=97, head_dx=6, head_rot=0.14)
    dt.don(k, 200, 770, 0.42, dt.POSE_LAUGH, "laugh", seed=98)
    rt.robot(k, 470, 720, 0.42, "stand", "accurate", seed=99)
    dt.don(k, 420, 770, 0.42, dt.POSE_FREEZE_BITE, "bite_freeze", look=(0.8, -0.2), seed=100, leg=(2, -110, 1))
    c.restore()
    table(c, 24, 700, 590)

    # 7. notes
    corp(c, "NOTES", 634, 556, 10, bold=True)
    notes = ["The robot from the last two films: shell, wheel, bow tie, big HR badge. No Santa suit.",
             "One costume piece: a pilgrim hat folded from black paper, gold paper buckle, crooked, taped.",
             "Verdicts are the screen: the face goes, one word fills it, with a glow round the screen.",
             "Red \"POLICY VIOLATION.\" and green \"ACCURATE.\" in the same flat voice.",
             "Shot 10: scans Pam, then Don, a beat of silence, then the green word.",
             "Shot 11: the leg covers the word; the green glow leaks round the edges."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 634, 580 + i * 24, 11, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "robot_sheet_tg_v1.png")
