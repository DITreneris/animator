"""Sets + lights sheet for "Office Noir", v2 (on_set_sheet_v1.py = v1, kept). v2 after the review (darkness is not
noir): one large lit area on each face and lifted darks in 1, 3 and 9 (no new lamp); Mom's wall shadow with an
oversized curler head, the mug and the beads, the same outline in the flashback and in 9; 10B is the punchline
close-up (face and bunny, a thousand-yard stare, a sweat drop, his fingers clutching the bunny); the agency sign
bigger and brighter; Sofia's lit eye catches a glint, the dark side deeper, her mouth in the light; the hand
rhyme: in 9 his screen-left hand is in his coat pocket, in 10B the same hand clutches the bunny.
Writes on_set_sheet_v2.png and on_set_phone_v2.png.
v1 notes: Sets + lights sheet for "Office Noir", v1. Writes on_set_sheet_v1.png (2400x2260, drawn at 1200x1130, 2x) and
on_set_phone_v1.png. Row 1: key frames with the characters and each shot's light (1, 3, 9, the flashback's boss,
10A, 10B). Row 2: the empty plates (office with the agency door and the rain window, Sofia's desk under the lamp,
the street corner, the bedroom with its star wallpaper), the light rule per shot, notes."""
import sys
import math
import cairo
import kit
import brand
import on_set_v2 as st
import don_on as d
import don_mf as dm
import mom_on as mo
import pam_on as pn
import props_on as pr
import sofia_on as so
import engine_on as eng
import don_sheet_on as dsh
import sofia_sheet_on as ssh
from kit import Ctx, INK, rect
from charsheets import corp, wrap
from pam_sheet_mf import boxed, LABELS

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
ACC = [(d.HEART, 1.0), (d.TIE, 0.4)] + so.ACCENTS[1:]


def flush(c):
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 22, w - 2, 21); c.fill()
            corp(c, label, x + 5, y + h - 7, 11, col=(0.25, 0.28, 0.36))
    LABELS.clear()


def noir(draw, light):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    draw(Ctx(cairo.Context(sf), 0))
    eng.accent_pass(sf, ACC)
    light(cairo.Context(sf))
    return sf


def colour(draw):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    draw(Ctx(cairo.Context(sf), 0))
    return sf


# ---- key frames ----------------------------------------------------------------------------------------------

def k1(kk):
    """Shot 1, frame 0: the heart on Pam's monitor in the foreground; Don in shadow behind, cynical, eyes under the
    brim; the agency door and the rain window behind him."""
    st.office_back(kk, t=0.4, door_x=24, window_x=250)
    d.don_noir(kk, 445, 1150, 1.9, face="cynic", brim=1.0, outline=True)
    st.pam_desk(kk, x=120, y=1060, s=2.4)                      # the monitor close to camera: the heart big


def l1(c):
    st.blinds(c, 230, 120, 310, 620, angle=-0.30, amount=0.36)        # through the window onto Don and the wall
    eng.side_light(c, 0, 0, 540, 960, from_left=False, amount=0.38)
    st.vignette(c, 0.38)
    st.key_light(c, 445, 1150 + d.HY * 1.9, 170, 0.30)                  # one large lit area: his face and lapels


POSE_POCKET = dm.ik(-1, -30, d.BT + 128) + (10, -4)                    # his screen-left hand in the coat pocket


def k9(kk):
    """Shot 9: low angle, Don turning away by the window, his hand in his pocket; Mom's shadow (oversized curler
    head, the mug, the beads) sweeps up the wall."""
    st.office_back(kk, t=1.2, door_x=330, window_x=40)
    st.mom_shadow(kk, 440, 820, 1.5, skew=-0.10, alpha=0.9, head=1.45)
    d.don_noir(kk, 190, 1320, 2.6, pose=POSE_POCKET, face="cynic", brim=1.0, outline=True)
    s, x, feet = 2.6, 190, 1320
    rect(kk, x - 52 * s, feet + (d.BT + 120) * s, 30 * s, 16 * s, d.TRENCH_SHADE, 330, shadow=False, lw=2 * s)  # pocket flap


def l9(c):
    st.blinds(c, 0, 0, 260, 700, angle=-0.25, amount=0.28)
    eng.side_light(c, 0, 0, 540, 960, from_left=True, amount=0.32)
    st.vignette(c, 0.4)
    st.key_light(c, 190, 1320 + d.HY * 2.6, 190, 0.28)


def kboss(kk):
    st.street(kk)
    st.mom_shadow(kk, 350, 860, 1.65, skew=-0.10, alpha=0.9, head=1.45)
    d.don_noir(kk, 260, 1020, 1.45, brim=1.0)
    rect(kk, 92, 40, 16, 740, (0.10, 0.10, 0.11), 320, shadow=False)


def lboss(c):
    g = cairo.RadialGradient(260, 380, 60, 260, 380, 640)                 # the streetlamp lights the wall
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.70)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    import props_sheet_on as ps2
    ps2.caption(c, "ONE BOSS.", 24, 40)


def k10a(kk):
    """Mom looms from the right; her fingertip stops just above the heart on his pyjama pocket."""
    st.bedroom(kk)
    dummy = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
    tip = mo.mom(Ctx(cairo.Context(dummy), 0), 575, 1010, 2.4, pose="loom", face="shout", lean=-12,
                 look=(-0.9, 0.8), thrust=1.0)["tip"]
    s = 2.8
    dx = tip[0] - 25 * s + 2
    feet = tip[1] + 14 + 0.75 * 13 * s - (d.BT + 48) * s
    d.don_pj(kk, dx, feet, s, face="frozen", bunny=True)
    rect(kk, -20, 880, 600, 200, (0.70, 0.84, 0.94), 811)
    mo.mom(kk, 575, 1010, 2.4, pose="loom", face="shout", lean=-12, look=(-0.9, 0.8), thrust=1.0)


def k10b(kk):
    """The punchline close-up: his face and the bunny. A thousand-yard stare, a sweat drop, rigid shoulders, his
    screen-left fingers clutching the bunny; the heart on his pocket; the milk at the edge."""
    st.bedroom(kk)
    rect(kk, 440, 560, 140, 260, (0.62, 0.45, 0.30), 812)
    pr.milk(kk, 500, 560, 1.6)
    s, x = 4.3, 250
    feet = 400 - d.HY * s
    d.don_pj(kk, x, feet, s, face="frozen", lift=6, bunny=True)
    bx, by = x - 28 * s, feet + (d.BT + 92) * s                               # the bunny's bottom
    for i in range(3):                                                         # his fingers dug into the plush
        kit.ellipse(kk, bx + (-14 + i * 12) * s * 0.62, by - 40 * s * 0.62, 5 * s * 0.6, 8 * s * 0.6, d.SKIN,
                    840 + i, shadow=False, lw=1.6 * s * 0.6)
    st.sweat_drop(kk.c, x + 46 * s, feet + (d.HY - 20) * s, 0.9 * s / 2)


def paste(c, sf, x0, y0, w, lab=None):
    c.save(); c.translate(x0, y0); c.scale(w / 540, w / 540)
    c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, y0, w, w * 960 / 540); c.stroke()
    if lab:
        wrap(c, lab, x0, y0 + w * 960 / 540 + 16, 10.5, w, col=(0.25, 0.28, 0.36))


def main(out, phone_out):
    d.FEDORA_BAND, d.FEDORA_RIM = (0.42, 0.42, 0.44), True
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SETS + LIGHT", 68, 44, 26, bold=True)
    corp(c, "\"Office Noir\"  ·  one light per shot", 262, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · SETS SHEET · OFFICE NOIR v2", 930, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    corp(c, "KEY FRAMES UNDER THEIR LIGHT", 28, 92, 10.5, bold=True)
    s3 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    ssh.shot3(Ctx(cairo.Context(s3), 0)); eng.accent_pass(s3, ssh.ACC); ssh.relight3(s3)
    c3 = cairo.Context(s3)                                                    # v2: deeper dark side, a glint, the mouth lit
    hx, hy = ssh.HEAD3["head"]; s_ = 2.5
    c3.save(); c3.new_path(); c3.arc(hx, hy, 50 * s_, 0, 2 * math.pi); c3.clip()
    c3.set_source_rgba(0, 0, 0, 0.25); c3.rectangle(hx + 8 * s_, hy - 60 * s_, 70 * s_, 120 * s_); c3.fill(); c3.restore()
    st.key_light(c3, hx - 6 * s_, hy + 30 * s_, 26 * s_, 0.22)
    c3.set_source_rgb(1, 1, 1); c3.arc(hx - 18 * s_ + 3 * s_, hy + 1 * s_, 2.6 * s_, 0, 2 * math.pi); c3.fill()
    keys = [(noir(k1, l1), "1 · window: blinds + hard side"), (s3, "3 · the desk lamp only"),
            (noir(k9, l9), "9 · window behind; Mom's shadow"), (noir(kboss, lboss), "flashback · the streetlamp"),
            (colour(k10a), "10A · colour: morning light"), (colour(k10b), "10B · colour: Don frozen")]
    for i, (sf, lab) in enumerate(keys):
        paste(c, sf, 28 + i * 192, 100, 182, lab)

    y2 = 470
    corp(c, "EMPTY PLATES", 28, y2, 10.5, bold=True)
    plates = [(noir(lambda kk: st.office_back(kk, t=0.4), lambda cc: st.vignette(cc, 0.4)), "the office: agency door, rain"),
              (noir(lambda kk: (st.sofia_desk(kk), st.lamp(kk), st.lamp_pool(kk.c)),
                    lambda cc: st.lamp_cone(cc, (50, 255), (130, 255), (-60, 960), (600, 960), 0.5)),
               "Sofía's desk + lamp"),
              (noir(st.street, lambda cc: None), "the street corner"),
              (colour(st.bedroom), "the bedroom: star wallpaper")]
    for i, (sf, lab) in enumerate(plates):
        paste(c, sf, 28 + i * 150, y2 + 8, 140, lab)

    rows = [("1", "the window (screen right)", "blind shadows + hard side, deep vignette"),
            ("M", "one hard source per insert", "flask: spot · informant: from below · boss: streetlamp"),
            ("2", "the window", "hard side; brim shadow on his eyes"),
            ("3", "Sofía's desk lamp", "a cone; half her face in deep shadow"),
            ("4", "the robot's screen glow", "soft, cool, from the screen"),
            ("5", "overhead office light", "CCTV: flat, then the overlay"),
            ("6", "the window", "hard side, the tilt"),
            ("7", "overhead, Pam soft", "Pam: soft frontal; Don: hard side, rim on the fedora"),
            ("8", "the window", "hard side"),
            ("9", "the window behind him", "low-angle silhouette, blinds, Mom's shadow"),
            ("10", "morning sun (colour)", "warm, flat, no hard shadows: reality")]
    x0, y0 = 640, y2 + 8
    corp(c, "ONE LIGHT PER SHOT", x0, y2, 10.5, bold=True)
    for j, (sh_, src, kind) in enumerate(rows):
        yy = y0 + 16 + j * 22
        corp(c, sh_, x0, yy, 10.5, bold=True)
        corp(c, src, x0 + 30, yy, 10, col=(0.2, 0.22, 0.28))
        corp(c, kind, x0 + 200, yy, 10, col=GREY)

    notes = [
        "v2: darkness is not noir. One large lit area on each face (from the shot's own source), lifted darks; Mom's "
        "shadow is unmistakably her (oversized curler head, the mug, the beads); 10B is the punchline close-up.",
        "The hand rhyme: in 9 his screen-left hand is in his coat pocket; in 10B that hand clutches the bunny.",
        "The office door reads DON · PRIVATE INVESTIGATIONS: his dream rewrites the office as his agency. The "
        "lettering is drawn readable (not mirrored) so it lands in the first second.",
        "Rain only outside the window: streaks that move with time and a few beads; the blinds throw slatted "
        "shadows across Don in shots 1 and 9, nowhere else.",
        "The street corner is a lit brick wall, a streetlamp and wet pavement; Mom's curler shadow falls on the bricks.",
        "The bedroom: a soft cream wallpaper with tiny mustard stars says 'boy's room' without a prop. Teal, mustard, "
        "pale blue, cream; no red except the heart.",
        "Every light is drawn after the accent pass, so the heart and the accents sit in the same light as the rest.",
    ]
    corp(c, "NOTES", 640, y2 + 290, 10.5, bold=True)
    y = y2 + 310
    for n in notes:
        y = wrap(c, "· " + n, 640, y, 9.5, 530, col=(0.2, 0.22, 0.28)) + 10
    flush(c)
    surf.write_to_png(out)

    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for i, (sf, lab) in enumerate((keys[2], keys[5])):
        x = 20 + i * 410
        cp.save(); cp.translate(x, 20); sc = 390 / 540; cp.scale(sc, sc)
        cp.set_source_surface(sf, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab + ", phone width", x, 20 + 390 * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)
    d.FEDORA_BAND, d.FEDORA_RIM = None, False


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "on_set_sheet_v2.png",
         sys.argv[2] if len(sys.argv) > 2 else "on_set_phone_v2.png")
