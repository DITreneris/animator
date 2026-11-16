"""Props + CCTV sheet for "Office Noir", v2 (props_sheet_on_v1.py = v1, kept). v2 after the CCTV review: the monitor
stays fully visible and its corner hooks the heart (caught, stretched sideways with a white peel line, snapped
onto the monitor); the camera never moves, the robot zooms into the footage instead (ENHANCE x2, x4 pixelated);
the freeze is 0.6 s with a punch-in, a playback click and the robot's "Suspect identified."; Don walks off
unaware, timestamps matching the real elapsed time; shot 4 with a brighter, closer playback screen; shot 6 opens
with his eyes dropping to the empty lapel; the flashback's drink (his gloved hand flips the flask open) and the
informant (lit from below, eyes in shadow); a thin grey hatband. Writes props_sheet_on_v2.png and
props_phone_on_v2.png."""
import sys
import math
import cairo
import kit
import brand
import don_on as d
import robot_on as ro
import props_on as pr
import engine_on as eng
from kit import Ctx, INK, rect
from charsheets import corp, wrap
from pam_sheet_mf import boxed, LABELS

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
PAPER = (0.82, 0.80, 0.77)
ACC = [(d.HEART, 1.0), (d.TIE, 0.4)]
TYPE = "Special Elite"
HBAND = (0.42, 0.42, 0.44)


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
        c.line_to(x0 + w * 0.80, y0 + h); c.line_to(x0 + tail[0] + dx, y0 + h + tail[1]); c.line_to(x0 + w * 0.64, y0 + h)
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


DX, FEET, S = 150, 1000, 1.5
SIZE = 13 * S * 0.9


def lapel_at(lean):
    lx0, ly0 = DX + d.LAPEL_HEART[0] * S, FEET + d.LAPEL_HEART[1] * S
    return rot_about(lx0, ly0, DX, FEET, lean)


L0 = lapel_at(12)
CORNER = (L0[0] + 0.95 * SIZE + 6, L0[1] - 0.55 * SIZE - 3)            # the monitor's top-left corner: the hook
MS = 1.2
MON = (CORNER[0] + 88 * MS, CORNER[1] + 150 * MS, MS)
END = (CORNER[0] + 50, CORNER[1] + 44)                                 # stuck on the screen, right by the corner


def office_top(kk):
    c = kk.c
    c.set_source_rgb(0.30, 0.29, 0.28); c.rectangle(0, 0, 540, 960); c.fill()
    c.set_source_rgba(0, 0, 0, 0.18); c.set_line_width(2)
    for i in range(-10, 20):
        c.move_to(i * 60, 960); c.line_to(270 + (i * 60 - 270) * 0.55, 0); c.stroke()
    for j in range(12):
        y = 960 - (j ** 1.4) * 22
        c.move_to(0, y); c.line_to(540, y); c.stroke()
    g = cairo.RadialGradient(CORNER[0] + 60, CORNER[1] + 60, 30, CORNER[0] + 60, CORNER[1] + 60, 460)
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.6); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    kit.cut(kk, [(CORNER[0] - 30, MON[1] - 10), (560, MON[1] - 10), (560, MON[1] + 170), (CORNER[0] - 70, MON[1] + 170)],
            (0.46, 0.38, 0.30))                                                          # the desk


def shot5(kk, t, lean=12, walk=False):
    c = kk.c
    office_top(kk)
    if walk:
        d.don_noir(kk, 80, FEET + 30, S, face="cynic", brim=1.0)
        pr.monitor(kk, *MON)
        d.heart(c, END[0], END[1], SIZE)
        return
    d.don_noir(kk, DX, FEET, S, pose=d.POSE_LEAN, face="cynic", brim=1.0, lean=lean, outline=True)
    pr.monitor(kk, *MON)                                                   # in front of him: its corner meets his lapel
    pr.hook_peel(c, lapel_at(lean), CORNER, END, SIZE, t)


def frame5(t, lean=12, walk=False):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot5(Ctx(cairo.Context(sf), 0), t, lean, walk)
    eng.accent_pass(sf, ACC)
    return sf


def cctv(sf, stamp, rec=True):
    pr.cctv_overlay(cairo.Context(sf), 540, 960, stamp=stamp, rec_on=rec)
    return sf


def shot4(kk, footage):
    c = kk.c
    c.set_source_rgb(0.16, 0.16, 0.17); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(270, 300, 20, 270, 300, 460)
    g.add_color_stop_rgba(0, 0.90, 0.92, 0.95, 0.75); g.add_color_stop_rgba(1, 0.90, 0.92, 0.95, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    ro.robot_noir(kk, 270, 1120, 2.9, state="cctv", footage=footage)


def shot6(kk, beat):
    """ECU on Don after the footage. a: his eyes drop to the empty lapel (the outline); b: the tilt, the brim down."""
    c = kk.c
    c.set_source_rgb(0.20, 0.20, 0.21); c.rectangle(0, 0, 540, 960); c.fill()
    c.save()
    if beat == "b":
        c.translate(270, 480); c.rotate(math.radians(9)); c.translate(-270, -480)
    s, x, feet = 4.0, 290, 1560
    if beat == "a":
        d.don_noir(kk, x, feet, s, face="neutral", look=(0.3, 0.95), brim=0.4, outline=True)
    else:
        d.don_noir(kk, x, feet, s, face="drop", look=(0, 0.2), brim=1.0, outline=True)
    c.restore()


def drink(kk):
    c = kk.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(200, 420, 20, 200, 420, 420)
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.9); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    rect(kk, -20, 640, 580, 400, (0.20, 0.17, 0.15), 901)
    pr.flask(kk, 270, 540, 3.2, open_=True, glove=True)
    caption(c, "ONE DRINK.", 24, 40)


def informant(kk):
    c = kk.c
    c.set_source_rgb(0.04, 0.04, 0.05); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.LinearGradient(0, 960, 0, 300)                                        # the light from below
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.9); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0.0)
    c.set_source(g); c.move_to(120, 960); c.line_to(420, 960); c.line_to(330, 300); c.line_to(210, 300); c.close_path()
    c.fill()
    rect(kk, -20, 760, 580, 300, (0.18, 0.16, 0.15), 902)
    pr.bunny(kk, 270, 770, 3.0, mode="noir", menace=True)
    caption(c, "ONE INFORMANT.", 24, 40)


def paste(c, sf, x0, y0, w, lab=None):
    c.save(); c.translate(x0, y0); c.scale(w / 540, w / 540)
    c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, y0, w, w * 960 / 540); c.stroke()
    if lab:
        wrap(c, lab, x0, y0 + w * 960 / 540 + 16, 10.5, w, col=(0.25, 0.28, 0.36))


def main(out, phone_out):
    d.FEDORA_BAND, d.FEDORA_RIM = HBAND, True
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PROPS + THE CCTV", 68, 44, 26, bold=True)
    corp(c, "\"Office Noir\"  ·  the hook, the zoom, the evidence", 330, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · PROPS SHEET · OFFICE NOIR v2", 920, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    corp(c, "SHOT 5: THE CAMERA NEVER MOVES; THE ROBOT ZOOMS INTO THE FOOTAGE", 28, 92, 10.5, bold=True)
    wide = cctv(frame5(0.0), "MON 08:59:14")
    catch = cctv(pr.enhance(frame5(0.33), CORNER, 2.0, 1, "ENHANCE x2"), "MON 08:59:15")
    peel = cctv(pr.enhance(frame5(0.66, lean=7), CORNER, 4.0, 5, "ENHANCE x4"), "MON 08:59:15")
    stuck = pr.enhance(frame5(1.0, lean=4), (END[0] - 20, END[1] + 60), 1.25, 1, None)
    cctv(stuck, "MON 08:59:16", rec=False)
    cs = cairo.Context(stuck)
    cs.select_font_face("DejaVu Sans Mono", 0, 1); cs.set_font_size(26); cs.set_source_rgb(0.95, 0.95, 0.95)
    cs.move_to(380, 112); cs.show_text("II 0.6 s")
    bubble(cs, "Suspect\nidentified.", 250, 640, tail=(300, 120), size=36)
    exitf = cctv(frame5(1.0, walk=True), "MON 08:59:17")
    seq = [(wide, "1 · wide: the lean, lapel at the corner"), (catch, "2 · ENHANCE x2: the corner hooks it"),
           (peel, "3 · ENHANCE x4: the peel, sideways"), (stuck, "4 · snapped on. Freeze 0.6 s, click"),
           (exitf, "5 · wide: he walks off, unaware")]
    for i, (sf, lab) in enumerate(seq):
        paste(c, sf, 28 + i * 230, 100, 220, lab)

    y2 = 548
    corp(c, "SHOT 4: THE WITNESS", 28, y2, 10.5, bold=True)
    s4 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot4(Ctx(cairo.Context(s4), 0), wide); eng.accent_pass(s4, ACC)
    paste(c, s4, 28, y2 + 8, 160)

    corp(c, "SHOT 6: THE EMPTY LAPEL", 206, y2, 10.5, bold=True)
    for i, (b, lab) in enumerate((("a", "a · eyes drop to the lapel"), ("b", "b · the tilt, brim down"))):
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        shot6(Ctx(cairo.Context(sf), 0), b); eng.accent_pass(sf, ACC)
        paste(c, sf, 206 + i * 120, y2 + 8, 112, lab)

    corp(c, "FLASHBACK INSERTS", 456, y2, 10.5, bold=True)
    for i, (fn, lab) in enumerate(((drink, "the drink: he flips it open"), (informant, "the informant, lit from below"))):
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        fn(Ctx(cairo.Context(sf), 0)); eng.accent_pass(sf, ACC)
        paste(c, sf, 456 + i * 120, y2 + 8, 112, lab)

    corp(c, "THE HOOK, CLOSE UP", 706, y2, 10.5, bold=True)
    for i, (t, lab) in enumerate(((0.0, "on the lapel"), (0.33, "caught"), (0.66, "stretched"), (1.0, "snapped"))):
        x0 = 706 + i * 116
        boxed(c, x0, y2 + 8, 110, 120, lab, fill=PAPER)
        c.save(); c.rectangle(x0, y2 + 8, 110, 120); c.clip()
        c.set_source_rgb(*d.TRENCH_SHADE); c.rectangle(x0, y2 + 8, 110, 120); c.fill()
        cx_, cy_ = x0 + 58, y2 + 40
        c.set_source_rgb(*pr.MON_BEZEL); c.rectangle(cx_, cy_, 60, 90); c.fill()
        c.set_source_rgb(*pr.MON_SCREEN); c.rectangle(cx_ + 7, cy_ + 7, 60, 90); c.fill()
        pr.hook_peel(c, (x0 + 30, y2 + 62), (cx_, cy_), (cx_ + 20, cy_ + 26), 13, t)
        c.restore()

    notes = [
        "The monitor stays fully visible and sits in front of him: its corner meets his lapel. The heart's curled tip "
        "catches on it, the heart stretches sideways (white back, a white peel line), then snaps onto the screen.",
        "A security camera never moves: the scale changes are the robot's ENHANCE (x2, then x4 pixelated, with a zoom "
        "box). Then back to wide.",
        "The motion is shown first; then the freeze, 0.6 s, a small punch-in and one playback click; the robot "
        "(off frame) says \"Suspect identified.\" Don walks off unaware. Timestamps follow the real elapsed time.",
        "Shot 6 opens with his eyes dropping to the empty lapel (the faint outline), then the tilt and the brim.",
        "Flashback: his gloved hand flips the flask open; the informant is lit from below, eyes in shadow. A thin grey "
        "hatband keeps the fedora readable (with the rim light).",
        "Script: the robot's line becomes \"Suspect identified.\" at the freeze; shot 4 is a silent click.",
    ]
    corp(c, "NOTES", 706, y2 + 160, 10.5, bold=True)
    y = y2 + 180
    for n in notes:
        y = wrap(c, "· " + n, 706, y, 9.5, 466, col=(0.2, 0.22, 0.28)) + 12
    flush(c)
    surf.write_to_png(out)

    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for i, (sf, lab) in enumerate(((catch, "shot 5, the hook"), (stuck, "shot 5, the freeze"))):
        x = 20 + i * 410
        cp.save(); cp.translate(x, 20); sc = 390 / 540; cp.scale(sc, sc)
        cp.set_source_surface(sf, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab + ", phone width", x, 20 + 390 * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)
    d.FEDORA_BAND, d.FEDORA_RIM = None, False


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "props_sheet_on_v2.png",
         sys.argv[2] if len(sys.argv) > 2 else "props_phone_on_v2.png")
