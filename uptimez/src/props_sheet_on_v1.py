"""Props sheet for "Office Noir", v1. Writes props_sheet_on_v1.png (2400x2260, drawn at 1200x1130, 2x) and
props_phone_on_v1.png. Noir frames as rendered (accent pass, tone v2, then the CCTV overlay on top).
Sections: shot 5 as five frames (the lean, the catch, the peel, the stick with the 0.3 s freeze and punch-in,
Don walking off), shot 4 (the robot in its watchman's cap, the footage on its screen), the robot alone, the heart's
four states close up, the props (flask and milk, the bunny in grey and pink, the mug), and the type (Special
Elite) on a caption card and a bubble."""
import sys
import math
import cairo
import kit
import brand
import don_on as d
import robot_on_v1 as ro
import props_on_v1 as pr
import mom_on as mo
import engine_on as eng
from kit import Ctx, INK, rect, ellipse
from charsheets import corp, wrap
from pam_sheet_mf import boxed, LABELS

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
PAPER = (0.82, 0.80, 0.77)
ACC = [(d.HEART, 1.0), (d.TIE, 0.4)]
TYPE = "Special Elite"


def flush(c):
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 22, w - 2, 21); c.fill()
            corp(c, label, x + 5, y + h - 7, 11, col=(0.25, 0.28, 0.36))
    LABELS.clear()


def caption(c, s, x, y, size=34):
    c.select_font_face(TYPE, 0, 0); c.set_font_size(size)
    w = c.text_extents(s).x_advance + 34
    h = size * 1.7
    c.set_source_rgba(0, 0, 0, 0.8); c.rectangle(x + 6, y + 6, w, h); c.fill()
    c.set_source_rgb(0.97, 0.95, 0.90); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0, 0, 0); c.set_line_width(3); c.rectangle(x, y, w, h); c.stroke()
    c.move_to(x + 17, y + h * 0.68); c.show_text(s)


def bubble(c, txt, x, y, tail=(0, 0), size=34):
    c.select_font_face(TYPE, 0, 0); c.set_font_size(size)
    lines = txt.split("\n")
    w = max(c.text_extents(t).x_advance for t in lines) + 40
    h = size * 1.25 * len(lines) + 30

    def shape(dx=0, dy=0):
        c.new_path(); r = 14; x0, y0 = x + dx, y + dy
        c.arc(x0 + w - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, math.pi / 2)
        c.line_to(x0 + w * 0.36, y0 + h); c.line_to(x0 + tail[0] + dx, y0 + h + tail[1]); c.line_to(x0 + w * 0.22, y0 + h)
        c.arc(x0 + r, y0 + h - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi); c.close_path()
    shape(7, 7); c.set_source_rgb(0, 0, 0); c.fill()
    shape(); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(0, 0, 0); c.set_line_width(4); c.stroke()
    c.set_source_rgb(0, 0, 0)
    for i, t in enumerate(lines):
        c.move_to(x + 20, y + 15 + size * 0.95 + i * size * 1.25); c.show_text(t)


def rot_about(px, py, cx, cy, deg):
    a = math.radians(deg)
    dx, dy = px - cx, py - cy
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


DX, FEET, S, LEAN = 196, 1000, 1.5, 14
LIFT = 190
MON = (420, 760, 1.2)


def office_top(kk):
    """High angle on Pam's desk: dark floor, the desk slab, the monitor."""
    c = kk.c
    c.set_source_rgb(0.30, 0.29, 0.28); c.rectangle(0, 0, 540, 960); c.fill()
    c.set_source_rgba(0, 0, 0, 0.18); c.set_line_width(2)
    for i in range(-10, 20):                                                    # floor tiles in perspective
        c.move_to(i * 60, 960); c.line_to(270 + (i * 60 - 270) * 0.55, 0); c.stroke()
    for j in range(12):
        y = 960 - (j ** 1.4) * 22
        c.move_to(0, y); c.line_to(540, y); c.stroke()
    g = cairo.RadialGradient(360, 660, 30, 360, 660, 460)                      # the overhead light on her desk
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.55); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    c.save(); c.translate(0, -LIFT)                                             # frame the action higher
    kit.cut(kk, [(250, 740), (560, 740), (560, 920), (220, 920)], (0.46, 0.38, 0.30))          # the desk
    pr.monitor(kk, *MON)
    c.restore()


END = (MON[0] - 62 * MON[2], MON[1] - 112 * MON[2])                            # on the screen, near its left edge


def lapel_point():
    lx0, ly0 = DX + d.LAPEL_HEART[0] * S, FEET + d.LAPEL_HEART[1] * S
    return rot_about(lx0, ly0, DX, FEET, LEAN)


def shot5(kk, t, walk=False):
    c = kk.c
    office_top(kk)
    end = END
    c.save(); c.translate(0, -LIFT)
    if walk:
        d.don_noir(kk, 110, FEET, S, face="cynic", brim=1.0)
        d.heart(c, end[0], end[1], 13 * S * 0.9)
    else:
        d.don_noir(kk, DX, FEET, S, pose=d.POSE_LEAN, face="cynic", brim=1.0, lean=LEAN, outline=True)
        pr.heart_peel(c, lapel_point(), end, 13 * S * 0.9, t)
    c.restore()
    return end


def render5(t, walk=False, freeze=False):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(sf)
    if freeze:                                                                   # the punch-in on the transfer
        cc.translate(END[0], END[1] - LIFT); cc.scale(1.22, 1.22); cc.translate(-END[0], -END[1] + LIFT)
    shot5(Ctx(cc, 0), t, walk)
    eng.accent_pass(sf, ACC)
    pr.cctv_overlay(cairo.Context(sf), 540, 960, stamp="MON 08:59:%02d" % (14 + int(t * 3) + (5 if walk else 0)),
                    rec_on=not freeze)
    if freeze:
        c2 = cairo.Context(sf)
        c2.select_font_face("DejaVu Sans Mono", 0, 1); c2.set_font_size(26); c2.set_source_rgb(0.95, 0.95, 0.95)
        c2.move_to(400, 76); c2.show_text("II PAUSE")
    return sf


def shot4(kk, footage):
    c = kk.c
    c.set_source_rgb(0.16, 0.16, 0.17); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(270, 330, 20, 270, 330, 420)                          # the screen's own glow
    g.add_color_stop_rgba(0, 0.85, 0.88, 0.92, 0.55); g.add_color_stop_rgba(1, 0.85, 0.88, 0.92, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    ro.robot_noir(kk, 270, 1080, 2.3, state="cctv", footage=footage)


def main(out, phone_out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PROPS + THE CCTV", 68, 44, 26, bold=True)
    corp(c, "\"Office Noir\"  ·  the evidence, the witness, the twins", 330, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · PROPS SHEET · OFFICE NOIR v1", 920, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    corp(c, "SHOT 5: THE CCTV (catch, peel, stick, 0.3 s freeze + punch-in, walk off)", 28, 92, 10.5, bold=True)
    seq = [(render5(0.0), "1 · the lean"), (render5(0.35), "2 · the corner catches"),
           (render5(0.66), "3 · the peel"), (render5(1.0, freeze=True), "4 · stuck: freeze 0.3 s"),
           (render5(1.0, walk=True), "5 · he walks off")]
    for i, (sf, lab) in enumerate(seq):
        x0, w = 28 + i * 230, 220
        c.save(); c.translate(x0, 100); c.scale(w / 540, w / 540)
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 100, w, w * 960 / 540); c.stroke()
        corp(c, lab, x0, 100 + w * 960 / 540 + 16, 11, col=(0.25, 0.28, 0.36))

    y2 = 528
    corp(c, "SHOT 4: THE WITNESS", 28, y2, 10.5, bold=True)
    s4 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot4(Ctx(cairo.Context(s4), 0), seq[0][0]); eng.accent_pass(s4, ACC)
    w4 = 170
    c.save(); c.translate(28, y2 + 8); c.scale(w4 / 540, w4 / 540)
    c.set_source_surface(s4, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(28, y2 + 8, w4, w4 * 960 / 540); c.stroke()

    def robot_box(kk):
        ro.robot_noir(kk, 85, 300, 0.8, state="eager")
    boxed(c, 210, y2 + 8, 170, 302, "the robot: a watchman's cap")
    c.save(); c.rectangle(210, y2 + 8, 170, 302); c.clip(); c.translate(210, y2 + 8)
    robot_box(Ctx(c, 0)); c.restore()

    corp(c, "THE HEART, CLOSE UP", 400, y2, 10.5, bold=True)
    for i, (t, lab) in enumerate(((0.0, "on the lapel"), (0.35, "catches"), (0.66, "peeling"),
                                  (1.0, "stuck"))):
        x0 = 400 + i * 100
        boxed(c, x0, y2 + 8, 94, 110, lab, fill=PAPER)
        c.save(); c.rectangle(x0, y2 + 8, 94, 110); c.clip()
        c.set_source_rgb(*d.TRENCH_SHADE); c.rectangle(x0, y2 + 8, 40, 110); c.fill()
        c.set_source_rgb(*pr.MON_BEZEL); c.rectangle(x0 + 62, y2 + 8, 32, 110); c.fill()
        pr.heart_peel(c, (x0 + 24, y2 + 50), (x0 + 74, y2 + 46), 15, t)
        c.restore()

    corp(c, "PROPS: EVERY NOIR PROP HAS A TWIN", 400, y2 + 146, 10.5, bold=True)
    props = [(lambda kk: pr.flask(kk, 47, 52, 0.9), "flask"), (lambda kk: pr.milk(kk, 47, 86, 0.9), "milk"),
             (lambda kk: pr.bunny(kk, 47, 88, 0.6, mode="noir"), "informant"),
             (lambda kk: pr.bunny(kk, 47, 88, 0.6, mode="pink"), "bunny"),
             (lambda kk: mo._mug(kk, 47, 52, 1.4), "mug"),
             (lambda kk: pr.monitor(kk, 47, 96, 0.45), "monitor")]
    for i, (fn, lab) in enumerate(props):
        x0 = 400 + i * 66 + (0 if i < 6 else 0)
        boxed(c, x0, y2 + 154, 62, 120, lab, fill=PAPER if i in (0, 2) else (1, 1, 1))
        c.save(); c.rectangle(x0, y2 + 154, 62, 120); c.clip(); c.translate(x0 - 16, y2 + 154)
        c.scale(1.0, 1.0); fn(Ctx(c, 0)); c.restore()

    corp(c, "TYPE: SPECIAL ELITE (Apache 2.0)", 820, y2, 10.5, bold=True)
    ts = cairo.ImageSurface(cairo.FORMAT_ARGB32, 700, 520)
    tc = cairo.Context(ts); tc.set_source_rgb(0.18, 0.18, 0.19); tc.paint()
    caption(tc, "ONE DRINK.", 30, 30)
    caption(tc, "Monday. Unsigned.", 30, 130, 30)
    bubble(tc, "You left me\nyour heart.", 300, 250, tail=(60, 70), size=36)
    boxed(c, 820, y2 + 8, 350, 260, None)
    c.save(); c.translate(820, y2 + 8); c.scale(0.5, 0.5); c.set_source_surface(ts, 0, 0); c.paint(); c.restore()

    notes = [
        "Shot 5 reads with the sound off: he leans over Pam's desk to peek at her screen, the heart's curled corner "
        "catches the monitor edge, peels (its white back showing) and sticks. Freeze 0.3 s on the stick, a small "
        "punch-in, the pop; then he walks off, the faint outline on his lapel.",
        "The CCTV look: grey, scanlines, a vignette, corner brackets, \"MON 08:59:14\", \"CAM 3\", and a white REC "
        "(red is the heart's). The overlay goes on after the accent pass.",
        "The robot wears a night-watchman's cap, antenna through the crown. Its bow tie is not the key red, so it is "
        "grey in noir. In shot 4 its screen shows the footage.",
        "Type: Special Elite for every caption card and bubble (license checked: Apache 2.0, keep the notice).",
    ]
    corp(c, "NOTES", 820, y2 + 290, 10.5, bold=True)
    y = y2 + 310
    for n in notes:
        y = wrap(c, "· " + n, 820, y, 9.5, 350, col=(0.2, 0.22, 0.28)) + 12
    flush(c)
    surf.write_to_png(out)

    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for i, (sf, lab) in enumerate(((seq[2][0], "shot 5, the peel"), (s4, "shot 4, the witness"))):
        x = 20 + i * 410
        cp.save(); cp.translate(x, 20); sc = 390 / 540; cp.scale(sc, sc)
        cp.set_source_surface(sf, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab + ", phone width", x, 20 + 390 * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "props_sheet_on_v1.png",
         sys.argv[2] if len(sys.argv) > 2 else "props_phone_on_v1.png")
