"""v1 (pinned). HR ROBOT model sheet for "Secret Santa" (robot_ss.py). Writes robot_sheet_ss_v1.png at 2400x2260 (drawn at
1200x1130, 2x): the canonical robot, its screens by shot (the magnifier-over-a-heart alert, the thinking dots, the
proud face, the tick), poses with the big rubber stamp, the three stamps and their weights, details, 9:16 camera
crops on the drawings and the timing of shots 10-15."""
import sys
import math
import cairo
import kit
import brand
import waiter_kit as w
import robot_ss as rs
import pam_ss as ps
import pam_sheet_ss as pss
import props_ss as props
from kit import Ctx, INK, ellipse
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.95, 0.96)
RED = (0.72, 0.12, 0.16)
k = None


def tag(x, y, s, bars=(), rot=-0.05):
    pss.k = k
    pss.gift_tag(k.c, x, y, s, rot=rot, bars=bars)


BAR_C = {"from": (2.5, 7), "to": (0.5, -9), "kiss": (22.5, 8)}


def hit(x, y, s, bar, wt, lift=16):
    """The stamp just lifting off the bar it printed, impact lines at the bar (tag at x, y, scale s)."""
    bx, by = x + BAR_C[bar][0] * s, y + BAR_C[bar][1] * s
    rs.stamp_prop(k, bx, by - lift * s / 1.15, 0.42 * s, "up", 0.0, 7)
    rs.impact_lines(k.c, bx, by, wt, 0.42 * s)


def table_top(c, x, y, w):
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(x, y, w, 400); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(1.6); c.move_to(x, y); c.line_to(x + w, y); c.stroke()


def head_screen(x, y, s, state, t=0.0, rot=0.0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ellipse(k, 0, 0, 50, 44, w.BODY, 3, shadow=False, lw=2.4)
    rs.screen(k, state, t=t)
    c.restore()


def clip_box(x, y, w_, h, draw, fill=None, label=None, frame=False):
    c = k.c
    if frame:
        c.save(); c.rectangle(x, y, w_, h); c.clip()
        c.set_source_rgb(*(fill or kit.WALL)); c.rectangle(x, y, w_, h); c.fill()
        draw()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w_, h); c.stroke()
        if label:
            corp(c, label, x, y + h + 12, 8.5, col=GREY, bold=True)
    else:
        boxed(c, x, y, w_, h, label, fill=fill or (1, 1, 1))
        c.save(); c.rectangle(x, y, w_, h); c.clip(); draw(); c.restore()


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "HR ROBOT", 68, 44, 28, bold=True)
    corp(c, "\"Secret Santa\"  ·  sincerely helpful, catastrophically confident, proud of its work", 232, 44, 13,
         col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · SECRET SANTA v1"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    rs.robot(k, 144, 500, 1.35, "stand", "eager", seed=71)
    corp(c, "FRONT · CANONICAL, NO COSTUME", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. screens
    corp(c, "SCREENS, BY SHOT  (the icon leads; words only where they must)", 284, 92, 10, bold=True)
    screens = [("tick", "3: APPROVED"), ("tick", "6: soft, behind Don"), ("personal", "10: the alert"),
               ("thinking", "13: the hover"), ("proud", "14: pride"), ("tick", "15: You're welcome.")]
    for i, (st, lab) in enumerate(screens):
        x, y = 284 + (i % 3) * 111, 98 + (i // 3) * 106
        clip_box(x, y, 107, 102, lambda x=x, y=y, st=st, i=i: head_screen(x + 53, y + 42, 0.92, st, t=0.4),
                 fill=(1.0, 0.94, 0.94) if st == "personal" else None, label=lab)

    # 3. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(rs.POSE_CLIP, "tick", dict(clip=True), "3: THUNK, APPROVED"),
             ("stand", "personal", dict(), "10: detected"),
             (rs.POSE_STAMP_UP, "eager", dict(stamp="up"), "11–13: stamp up"),
             (rs.POSE_HOVER, "thinking", dict(stamp="hover", head_rot=-0.18, t=0.4), "13: hover"),
             ("stand", "proud", dict(head_rot=0.12), "14: the nod")]
    for i, (pose, st, kw, lab) in enumerate(poses):
        x = 634 + i * 109
        clip_box(x, 98, 105, 210, lambda x=x, pose=pose, st=st, kw=kw, i=i: rs.robot(k, x + 48, 292, 0.55, pose, st,
                                                                                    seed=80 + i, **kw),
                 fill=(1.0, 0.94, 0.94) if i == 1 else None, label=lab)

    # 4. the three stamps
    corp(c, "THE THREE STAMPS  (correct, absurd, cruel: three weights)", 284, 348, 10, bold=True)
    hits = [((), ("from",), 1, "11: sender · THUNK", "ordinary: that's Secret Santa"),
            (("from",), ("from", "to"), 2, "12: recipient · THUNK!", "heavier, a 0.4 s beat"),
            (("from", "to"), ("from", "to", "kiss"), 3, "13: the kiss · THUNK.", "a hover, then the biggest")]
    for i, (before, after, wt, lab, sub) in enumerate(hits):
        x, y = 284 + i * 111, 354
        def d(x=x, y=y, after=after, wt=wt):
            table_top(c, x, y + 58, 107)
            tag(x + 50, y + 92, 1.15, after, rot=0)
            hit(x + 50, y + 92, 1.15, after[-1], wt)
        clip_box(x, y, 107, 150, d, label=lab)
        corp(c, sub, x + 2, y + 164, 8, col=GREY)

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    def stamp_detail():
        rs.stamp_prop(k, 690, 474, 1.9, "up", 0.0, 5)
        c.set_source_rgb(0.08, 0.08, 0.10); c.rectangle(744, 456, 46, 14); c.fill()
        corp(c, "the print:", 744, 448, 8, col=GREY); corp(c, "a plain bar", 744, 484, 8, col=GREY)
    clip_box(634, 354, 170, 160, stamp_detail, label="the big rubber stamp")
    def icon_detail():
        c.save(); c.translate(897, 428)
        c.set_source_rgb(0.04, 0.06, 0.12); c.arc(0, 0, 58, 0, 2 * math.pi); c.fill()
        rs.magnifier_heart(c, 0, 0, 34, rs.RED)
        c.restore()
    clip_box(812, 354, 170, 160, icon_detail, label="alert: her heart, found as data")
    def clip_detail():
        rs.clipboard(k, 1040, 430, 1.9, True, 5)
        corp(c, "plants the", 1092, 418, 9, col=GREY); corp(c, "THUNK (3)", 1092, 432, 9, col=GREY)
    clip_box(990, 354, 186, 160, clip_detail, label="clipboard, shot 3")

    # 6. 9:16 crops
    y0 = 562
    corp(c, "9:16 CROPS ON THE DRAWINGS", 24, y0 - 6, 10, bold=True)
    W, H, G = 98, 174, 104

    def c10():
        x = 24
        rs.robot(k, x + 49, y0 + 330, 1.2, "stand", "personal", seed=91)
    clip_box(24, y0, W, H, c10, frame=True, fill=(1.0, 0.94, 0.94), label="10: CU, level, centred")

    def ins(x, bars, wt, sc, dx, label, beat=False):
        def d():
            table_top(c, x, y0 + 40, W)
            tag(x + 49 + dx, y0 + 112, sc, bars, rot=0)
            hit(x + 49 + dx, y0 + 112, sc, bars[-1], wt)
            if beat:
                corp(c, "(0.4 s beat)", x + 20, y0 + 166, 8, col=GREY, bold=True)
        clip_box(x, y0, W, H, d, frame=True, label=label)
    ins(24 + G, ("from",), 1, 2.0, 0, "11: tight insert")
    ins(24 + 2 * G, ("from", "to"), 2, 2.5, 8, "12: tighter, shifted", beat=True)

    def c13():
        x = 24 + 3 * G
        table_top(c, x, y0 + 70, W)
        tag(x + 60, y0 + 128, 1.8, ("from", "to"))
        rs.stamp_prop(k, x + 74, y0 + 96, 1.1, "up", 0.0, 9)
        def bg(lc):
            rs.robot(Ctx(lc, 0), x - 10, y0 + 300, 1.2, rs.POSE_HOVER, "thinking", head_rot=-0.18, t=0.4, seed=92)
        props.soft(c, bg, 2.0)
    clip_box(24 + 3 * G, y0, W, H, c13, frame=True, label="13: over its shoulder")

    def c14():
        x = 24 + 4 * G
        rs.robot(k, x + 49, y0 + 330, 1.2, "stand", "proud", head_rot=0.10, seed=93)
    clip_box(24 + 4 * G, y0, W, H, c14, frame=True, label="14: pride, still")

    def c15():
        x = 24 + 5 * G
        rs.robot(k, x + 72, y0 + 236, 0.62, "stand", "tick", seed=94)
        ps.pam(k, x + 26, y0 + 236, 0.62, "stand", "incredulous", look=(0.4, 0.6), seed=95)
        tag(x + 30, y0 + 154, 0.7, ("from", "to", "kiss"))
    clip_box(24 + 5 * G, y0, W, H, c15, frame=True, label="15: still, no zoom")

    # 7. timing
    x1 = 660
    corp(c, "SHOTS 10–15: TIME FOR EVERY DECISION", x1, y0 - 6, 10, bold=True)
    boxed(c, x1, y0, 516, 174)
    segs = [("10", 2.5, "BZZT red"), ("11", 0.9, "THUNK"), ("12", 1.7, "THUNK! + beat"), ("13", 2.3, "… THUNK."),
            ("14", 0.7, "still"), ("15", 4.4, "DING")]
    tot = sum(d for _, d, _ in segs)
    sx, bx = 488 / tot, x1 + 14
    cols = [(0.85, 0.30, 0.30), (0.45, 0.45, 0.50), (0.35, 0.35, 0.40), (0.20, 0.20, 0.25), (0.55, 0.70, 0.85),
            (0.25, 0.65, 0.40)]
    for (sh, d, snd), col in zip(segs, cols):
        wd = d * sx
        c.set_source_rgb(*col); c.rectangle(bx, y0 + 20, wd - 2, 26); c.fill()
        corp(c, sh, bx + 3, y0 + 37, 9, col=(1, 1, 1), bold=True)
        corp(c, "%.1f s" % d, bx + 1, y0 + 60, 8, col=GREY)
        corp(c, snd, bx + 1, y0 + 74, 8, col=INK)
        bx += wd
    lines = ["The order is the joke: sender (sensible), recipient (absurd), a hover, the kiss (cruel).",
             "Each stamp is heavier: sound, impact lines and camera tightness grow; never rushed.",
             "13: head tilt + thinking dots while the stamp hangs still: a considered professional decision.",
             "14: at least 0.6 s of stillness: soft content eyes, one slow nod. Sincerely proud, never sarcastic.",
             "15: the green tick and a warm DING on \"You're welcome.\" No zoom, no sticker."]
    for i, l in enumerate(lines):
        corp(c, "·  " + l, x1 + 14, y0 + 98 + i * 15, 9, col=INK)

    # 8. the line: what HR sees vs what Pam wrote
    y1 = 790
    corp(c, "WHAT PAM WROTE, THEN WHAT HR APPROVED", 24, y1 - 6, 10, bold=True)
    boxed(c, 24, y1, 1152, 180)
    seq = [((), "8: her courage"), (("from",), "11: correct"), (("from", "to"), "12: absurd"),
           (("from", "to", "kiss"), "13: cruel"), (("from", "to", "kiss"), "15: \"You're welcome.\"")]
    for i, (b, lab) in enumerate(seq):
        x = 130 + i * 228
        tag(x, y1 + 80, 2.0, b)
        corp(c, lab, x - 60, y1 + 150, 11, col=brand.NAVY, bold=True)
        if i < len(seq) - 1:
            c.set_source_rgb(*GREY); c.set_line_width(1.8)
            c.move_to(x + 92, y1 + 80); c.line_to(x + 130, y1 + 80); c.stroke()
            c.move_to(x + 123, y1 + 74); c.line_to(x + 130, y1 + 80); c.line_to(x + 123, y1 + 86); c.stroke()
    head_screen(130 + 4 * 228 + 70, y1 + 64, 0.45, "tick")

    # 9. notes
    y2 = 996
    corp(c, "NOTES", 24, y2, 10, bold=True)
    notes = ["The canonical robot, no costume: bow tie, HR badge, wheel. Christmas is the set's job.",
             "New screens: PERSONAL DATA DETECTED (a magnifier over a heart), thinking dots, proud, the tick.",
             "The stamp is big and plain: red knob, wooden handle, a black rubber face that prints a plain bar.",
             "Printed TO: and FROM: stay readable under the bars: you see exactly what was removed.",
             "It is sincerely helpful: literal, confident, proud. Never sarcastic, never cruel on purpose.",
             "The green tick behind Don in 6 is the plant for the tick on \"You're welcome.\" in 15.",
             "Shot 3: the same stamp THUNKs APPROVED on its clipboard: the plant for the three stamps.",
             "Voice: Robot B, flat and professional in 10, warm and satisfied in 15."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 24 + (i % 2) * 588, y2 + 24 + (i // 2) * 30, 10, col=INK)
    flush(c)
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "robot_sheet_ss_v1.png")
