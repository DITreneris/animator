"""PAM model sheet for "Office Noir" (pam_on.py), v2 (pam_sheet_on_v1.py = v1, kept). v2 after the review: the
rolls without the headphone look, three distinct faces (curious, knowing, delighted), the heart in the pinning
pose, the heart 25 % bigger in shot 7, 7B as three beats (Don glances down at the heart, back up at her, the
almost-smile) framed to keep Pam's hand and the edge of her face, thicker gold rims, bigger captions.
Writes pam_sheet_on_v2.png and pam_phone_on_v2.png.
v1 notes: Writes pam_sheet_on_v1.png (2400x2260, drawn at 1200x1130,
2x) and pam_phone_on_v1.png. Noir as rendered (accent pass, tone v2); Pam keeps the only soft light in the dream.
Sections: noir front (soft light), the same figure before the pass, poses, faces and speech mouths, details, her
light against the others', shot 7 as a two-shot (the line) and the push to the lapel (his eyes revealed), notes."""
import sys
import math
import cairo
import kit
import brand
import pam_on_v2 as pn
import don_on as d
import engine_on as eng
import sofia_sheet_on as sh
from kit import Ctx, INK, rect
from charsheets import corp, wrap
from pam_sheet_mf import boxed, LABELS


def flush(c):
    """v2: bigger captions on a taller strip."""
    for x, y, w, h, label in LABELS:
        if label:
            c.set_source_rgb(1, 1, 1); c.rectangle(x + 1, y + h - 22, w - 2, 21); c.fill()
            corp(c, label, x + 5, y + h - 7, 11, col=(0.25, 0.28, 0.36))
    LABELS.clear()

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
PAPER = (0.82, 0.80, 0.77)
ACC = sh.ACC


def soft_light(c, cx, cy, r, amount=0.28):
    """Pam's light: a soft frontal glow on her, nothing hard."""
    g = cairo.RadialGradient(cx, cy, r * 0.1, cx, cy, r)
    g.add_color_stop_rgba(0, 1, 1, 1, amount); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.save(); c.set_source(g); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill(); c.restore()


def noir_box(c, x, y, w, h, draw, label=None, bg=PAPER, glow=None, scale=2):
    sw, sh_ = int(w * scale), int(h * scale)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh_)
    cc = cairo.Context(sf); cc.scale(scale, scale)
    cc.set_source_rgb(*bg); cc.paint()
    draw(Ctx(cc, 0))
    eng.accent_pass(sf, ACC)
    if glow:
        c2 = cairo.Context(sf); c2.scale(scale, scale)
        soft_light(c2, *glow)
    boxed(c, x, y, w, h, label)
    c.save(); c.translate(x, y); c.scale(1 / scale, 1 / scale); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()


HEART7 = 16                                                     # v2: 25 % bigger than the lapel's 13


def shot7(kk, zoom=1.0, focus=None, don_face="almost", don_look=(-0.8, 0.0)):
    """Two-shot: Pam (screen left, soft light) presses the heart onto Don's lapel; his brim lifted, both eyes,
    the almost-smile. zoom > 1 pushes in on focus (the lapel and his eyes)."""
    c = kk.c
    c.set_source_rgb(0.24, 0.23, 0.22); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(270, 120, 20, 270, 300, 620)                                # the overhead office light
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.75); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    c.save()
    if zoom != 1.0:
        fx, fy = focus
        c.translate(270, 480); c.scale(zoom, zoom); c.translate(-fx, -fy)
    s, feet = 2.0, 1010
    dx_ = 340
    d.don_noir(kk, dx_, feet, s, face=don_face, look=don_look, brim=0.0, heart_on=False)
    lx, ly = dx_ + d.LAPEL_HEART[0] * s, feet + d.LAPEL_HEART[1] * s
    px_ = 165
    pn.pam_noir(kk, px_, feet, s, pose=pn.POSE_PRESS((lx - 16 * s - px_) / s, (ly - feet) / s + 10), face="knowing",
                look=(1.0, -0.15))
    d.heart(c, lx, ly, HEART7 * s)                               # the heart on top: her fingertips at its edge
    kit.ellipse(kk, lx - HEART7 * s, ly + 4 * s, 5 * s, 7 * s, pn.ps.SKIN, 760, shadow=False, lw=1.6 * s)
    c.restore()
    return (lx, ly)


def main(out, phone_out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "\"Office Noir\"  ·  the only honest thing in the dream  ·  1940s secretary, gold glasses", 150, 44,
         13, col=GREY)
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · OFFICE NOIR v2", 890, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    head_y = 500 + pn.HY * 1.35
    noir_box(c, 28, 92, 280, 528, lambda kk: pn.pam_noir(kk, 140, 500, 1.35, face="knowing", look=(0.4, 0.0)),
             label="NOIR · AS RENDERED, HER SOFT LIGHT", glow=(140, head_y, 190))
    sh.colour_box(c, 320, 92, 280, 528, lambda kk: pn.pam_noir(kk, 140, 500, 1.35, face="knowing", look=(0.4, 0.0)),
                  label="BEFORE THE PASS · BLOUSE, BOW, GOLD")

    corp(c, "POSES", 620, 104, 10.5, bold=True)
    poses = [(dict(face="curious"), "2: the heart"),
             (dict(pose=pn.POSE_PRESS(80, pn.BT + 40), face="knowing", heart=True, heart_size=16), "7: pins it on him"),
             (dict(face="knowing", look=(1.0, -0.15)), "7: the knowing smile"),
             (dict(face="delighted"), "quietly delighted")]
    for i, (kw, lab) in enumerate(poses):
        x0 = 620 + i * 139
        dxp = 46 if "pose" in kw else 66
        noir_box(c, x0, 112, 133, 250, (lambda kk, kw=kw, dxp=dxp: pn.pam_noir(kk, dxp, 238, 0.6, **kw)), label=lab,
                 glow=(66, 238 + pn.HY * 0.6, 70))

    corp(c, "FACES  +  SPEECH MOUTHS (\"You left me your heart.\")", 620, 390, 10.5, bold=True)
    faces = [(dict(face="neutral"), "neutral"), (dict(face="curious"), "curious"),
             (dict(face="knowing", look=(1.0, -0.15)), "knowing"), (dict(face="delighted"), "delighted"),
             (dict(face="neutral", mouth="E"), "E"), (dict(face="neutral", mouth="O"), "O"),
             (dict(face="neutral", mouth="A"), "A")]
    for i, (kw, lab) in enumerate(faces):
        x0 = 620 + i * 79
        noir_box(c, x0, 398, 75, 100, (lambda kk, kw=kw: pn.pam_noir(kk, 37, 46 - pn.HY * 0.7, 0.7, **kw)), label=lab,
                 glow=(37, 46, 50))

    corp(c, "DETAILS", 620, 526, 10.5, bold=True)

    def det_glasses(kk):
        kc = kk.c
        kc.save(); kc.translate(66, 30); kc.scale(1.5, 1.5)
        pn._glasses_gold(__import__("pam_mf").glasses_draw)(kk, 0, -6, "low")
        kc.restore()
    noir_box(c, 620, 534, 133, 86, det_glasses, label="gold rims, chain")

    def det_bow(kk):
        kc = kk.c
        kc.save(); kc.translate(66, 30 - pn.BT * 1.6); kc.scale(1.6, 1.6)
        pn._costume()(kk, "PAM", None, pn.BT, 3)
        kc.restore()
    noir_box(c, 759, 534, 133, 86, det_bow, label="the pussy bow")

    def det_roll(kk):
        pn.pam_noir(kk, 66, 40 - pn.HY * 0.62, 0.62, face="knowing", look=(0.4, 0))
    sh.colour_box(c, 898, 534, 133, 86, det_roll, label="bob, rolled under")

    def det_legs(kk):
        kc = kk.c
        kc.save(); kc.translate(66, 66); kc.scale(0.42, 0.42); pn._legs(kk, 3); kc.restore()
    sh.colour_box(c, 1037, 534, 133, 86, det_legs, label="pencil skirt")

    corp(c, "HER LIGHT vs THE OTHERS'", 28, 652, 10.5, bold=True)

    def face_crop(kk):
        pn.pam_noir(kk, 67, 80 - pn.HY * 1.05, 1.05, face="knowing", look=(0.4, 0))
    noir_box(c, 28, 662, 134, 150, face_crop, label="soft (Pam only)", glow=(67, 80, 90))

    def hard(kk):
        face_crop(kk)
    sw_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 268, 300)
    cc = cairo.Context(sw_); cc.scale(2, 2); cc.set_source_rgb(*PAPER); cc.paint(); hard(Ctx(cc, 0))
    eng.accent_pass(sw_, ACC); eng.side_light(cairo.Context(sw_), 0, 0, 268, 300, from_left=True, amount=0.68)
    boxed(c, 168, 662, 134, 150, "hard (the others)")
    c.save(); c.translate(168, 662); c.scale(0.5, 0.5); c.set_source_surface(sw_, 0, 0); c.paint(); c.restore()

    frames = []
    beats = [(1.0, "almost", (-0.8, 0.0), "7A: the two-shot, the line"),
             (1.7, "neutral", (-0.3, 0.9), "7B-1: he looks down at the heart"),
             (1.7, "neutral", (-0.9, 0.0), "7B-2: back up at her"),
             (1.7, "almost", (-0.9, 0.0), "7B-3: the almost-smile, 0.5 s")]
    for (zoom, dface, dlook, lab) in beats:
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        kk = Ctx(cairo.Context(sf), 0)
        foc = shot7(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)), 0))
        foc = (foc[0] - 75, foc[1] - 80)                          # v2: keep her hand and the edge of her face
        shot7(kk, zoom, foc, dface, dlook)
        eng.accent_pass(sf, ACC)
        cg = cairo.Context(sf)
        if zoom == 1.0:
            soft_light(cg, 165, 1010 + pn.HY * 2.0, 230, 0.30)
            eng.side_light(cg, 300, 0, 240, 960, from_left=True, amount=0.45)
            sh.bubble(Ctx(cg, 0), "You left me\nyour heart.", 40, 60, tail=(110, 120), size=34)
        else:
            eng.side_light(cg, 0, 0, 540, 960, from_left=True, amount=0.35)
        frames.append((sf, lab))
    corp(c, "SHOT 7: THE LINE, THEN HIS COMPOSURE SLIPS", 320, 652, 10.5, bold=True)
    for i, (sf, lab) in enumerate(frames):
        x0, w = 320 + i * 130, 124
        c.save(); c.translate(x0, 662); c.scale(w / 540, w / 540)
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 662, w, w * 960 / 540); c.stroke()
        wrap(c, lab, x0, 662 + w * 960 / 540 + 16, 10.5, w, col=(0.25, 0.28, 0.36))

    notes = [
        "v2: no headphone rolls, three distinct faces, the heart in the pin pose and 25 % bigger in 7, thicker gold rims.",
        "7B: he looks down at the heart, back up at her, then the almost-smile; shot 8 restores the scowl and the finger.",
        "Pam is the only soft light in the dream: frontal, no hard shadow. Everyone else is cut by a hard side light.",
        "1940s secretary: a cream silk pussy-bow blouse with pearl buttons, a charcoal pencil skirt below the knee, "
        "seamed stockings, low pumps; her bob rolled under at the sides. No lanyard, no badge.",
        "Her glasses keep the gold: gold rims and the bead chain in the episode's gold key (shared with Sofía's hoops), "
        "35 % in noir. She is the one who sees clearly.",
        "Shot 2: curious and quietly hopeful at the heart, never hurt.",
        "Faces: curious = raised brows, eyes on the heart; knowing = one brow up, an asymmetric smile; delighted = "
        "soft closed eyes, a real smile.",
    ]
    corp(c, "NOTES", 860, 652, 10.5, bold=True)
    y = 672
    for n in notes:
        y = wrap(c, "· " + n, 860, y, 9.5, 312, col=(0.2, 0.22, 0.28)) + 12
    flush(c)
    surf.write_to_png(out)

    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for i, (sf, lab) in enumerate((frames[0], frames[3])):
        x = 20 + i * 410
        cp.save(); cp.translate(x, 20); sc = 390 / 540; cp.scale(sc, sc)
        cp.set_source_surface(sf, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab + ", phone width", x, 20 + 390 * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_on_v2.png",
         sys.argv[2] if len(sys.argv) > 2 else "pam_phone_on_v2.png")
