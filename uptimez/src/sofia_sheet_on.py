"""SOFIA model sheet for "Office Noir" (sofia_on.py), v2 (sofia_sheet_on_v1.py = v1, kept). v2 after the review:
shot 3 relit (half her face in deep shadow, a diagonal shadow across her forehead, lips and one hoop in the
light, a harder side light); the tilted nail file and a three-beat strip for shot 3 (stroke, stop and one brow up,
the smallest smirk on "darling", never looking up); shot 2 with Sofia 30 % bigger and the heart next to her
face; a two-line bubble in bigger type; the side-eye, brow and smirk faces; full-size mouths.
Writes sofia_sheet_on_v2.png and sofia_phone_on_v2.png.
v1 notes: Writes sofia_sheet_on_v1.png (2400x2260, drawn at
1200x1130, 2x) and sofia_phone_on_v1.png. The noir look is shown as rendered (engine_on accent pass, tone v2,
the light after the accents): grey, with her lips in the heart's red and her hoops in gold at 50 %.
Sections: noir front, the same figure before the pass (key colours), poses, faces and speech mouths, details,
shot 2 as Don's point of view (the heart held up to his eye lines up with her lips), shot 3 under the desk lamp
with a noir dialogue bubble, notes."""
import sys
import math
import cairo
import kit
import brand
import sofia_on as so
import don_on as d
import engine_on as eng
from kit import Ctx, INK, rect, ellipse
from charsheets import corp, wrap
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
WASH = (0.93, 0.95, 0.94)
PAPER = (0.82, 0.80, 0.77)
ACC = so.ACCENTS + [(d.TIE, 0.4)]


def noir_box(c, x, y, w, h, draw, label=None, bg=PAPER, light=0.0, scale=2):
    sw, sh = int(w * scale), int(h * scale)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    cc = cairo.Context(sf); cc.scale(scale, scale)
    cc.set_source_rgb(*bg); cc.paint()
    draw(Ctx(cc, 0))
    eng.accent_pass(sf, ACC)
    if light:
        eng.side_light(cairo.Context(sf), 0, 0, sw, sh, from_left=True, amount=light)
    boxed(c, x, y, w, h, label)
    c.save(); c.translate(x, y); c.scale(1 / scale, 1 / scale); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()


def colour_box(c, x, y, w, h, draw, label=None, fill=PAPER):
    boxed(c, x, y, w, h, label, fill=fill)
    c.save(); c.rectangle(x, y, w, h); c.clip(); c.translate(x, y); draw(Ctx(c, 0)); c.restore()


def bubble(kk, txt, x, y, tail=(0, 0), size=30):
    """The noir dialogue bubble: white, a thick black outline, a hard offset shadow, a sharp tail, mono type.
    txt may hold "\n" for two lines."""
    c = kk.c
    c.select_font_face("DejaVu Sans Mono", 0, 1); c.set_font_size(size)
    lines = txt.split("\n")
    w = max(c.text_extents(t).x_advance for t in lines) + 40
    h = size * 1.25 * len(lines) + 30

    def shape(dx=0, dy=0):
        c.new_path()
        r = 14
        x0, y0 = x + dx, y + dy
        c.arc(x0 + w - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, math.pi / 2)
        c.line_to(x0 + w * 0.36, y0 + h); c.line_to(x0 + tail[0] + dx, y0 + h + tail[1]); c.line_to(x0 + w * 0.22, y0 + h)
        c.arc(x0 + r, y0 + h - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi); c.close_path()
    shape(7, 7); c.set_source_rgb(0, 0, 0); c.fill()
    shape(); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(0, 0, 0); c.set_line_width(4); c.stroke()
    for i, t in enumerate(lines):
        c.move_to(x + 20, y + 15 + size * 0.95 + i * size * 1.25); c.show_text(t)


def _lips_y(s, x, feet):
    dummy = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
    hx, hy = so.sofia_noir(Ctx(cairo.Context(dummy), 0), x, feet, s, pose="file")["head"]
    return hy + 35 * s


def shot2_pov(kk):
    """Don's point of view: the heart held up in his fingers, and across the room Sofia's lips at the same height."""
    c = kk.c
    c.set_source_rgb(0.20, 0.19, 0.18); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(380, 330, 10, 380, 330, 380)
    g.add_color_stop_rgba(0, 0.92, 0.88, 0.80, 0.85); g.add_color_stop_rgba(1, 0.92, 0.88, 0.80, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    rect(kk, -20, 560, 580, 420, (0.30, 0.24, 0.20), 701)                                 # her desk, far side
    s = 1.95
    feet = 900
    feet += 400 - _lips_y(s, 395, feet)                                                   # her lips at y = 400
    so.sofia_noir(kk, 395, feet, s, pose="file", face_kind="bored")
    rect(kk, -20, 640, 580, 400, (0.30, 0.24, 0.20), 702)                                 # desk front (hides legs)
    kit.cut(kk, [(-10, 970), (-10, 760), (118, 470), (200, 492), (130, 970)], d.TRENCH, shadow=False, lw=3)  # his sleeve
    for i, (dx, dy) in enumerate(((-26, 62), (0, 72), (24, 66))):                         # his fingers
        ellipse(kk, 175 + dx, 400 + dy, 15, 22, d.SKIN, 710 + i, shadow=False, lw=3)
    d.heart(c, 175, 400 + 8, 58)                                                          # the heart, next to her face


HEAD3 = {}


def shot3(kk, face_kind="bored", stroke=0.0, line=True):
    """Medium close-up under the hard desk-lamp key: she files her nails and does not look up."""
    c = kk.c
    c.set_source_rgb(0.10, 0.10, 0.11); c.rectangle(0, 0, 540, 960); c.fill()
    c.set_source_rgba(0.98, 0.95, 0.86, 0.80)                                              # the lamp's cone
    c.move_to(50, 255); c.line_to(130, 255); c.line_to(600, 960); c.line_to(-60, 960); c.close_path(); c.fill()
    o = so.sofia_noir(kk, 300, 1100, 2.5, pose="file", face_kind=face_kind, lag=(1, 0), stroke=stroke)
    HEAD3["head"] = o["head"]
    rect(kk, -20, 880, 580, 200, (0.22, 0.18, 0.15), 703)                                  # desk edge
    kit.cut(kk, [(30, 200), (150, 200), (130, 260), (50, 260)], (0.30, 0.30, 0.32), shadow=False)   # lamp shade
    c.set_source_rgb(0.30, 0.30, 0.32); c.set_line_width(10); c.move_to(90, 200); c.line_to(40, 150); c.line_to(-10, 150)
    c.stroke()


def relight3(sf, amount=0.72):
    """After the accent pass: a hard side light, half her face in deep shadow (lips and the near hoop stay lit),
    and a diagonal shadow across her forehead."""
    c = cairo.Context(sf)
    eng.side_light(c, 0, 0, 540, 960, from_left=True, amount=amount)
    hx, hy = HEAD3["head"]
    s = 2.5
    c.save(); c.new_path(); c.arc(hx, hy, 50 * s, 0, 2 * math.pi); c.clip()
    c.set_source_rgba(0, 0, 0, 0.62)                                   # the far half of her face
    c.move_to(hx + 6 * s, hy - 60 * s); c.line_to(hx + 70 * s, hy - 60 * s); c.line_to(hx + 70 * s, hy + 60 * s)
    c.line_to(hx + 24 * s, hy + 60 * s); c.line_to(hx + 20 * s, hy + 26 * s); c.line_to(hx + 4 * s, hy + 18 * s)
    c.close_path(); c.fill()
    c.restore()
    c.save(); c.new_path(); c.arc(hx, hy - 6 * s, 66 * s, 0, 2 * math.pi); c.clip()
    c.set_source_rgba(0, 0, 0, 0.5)                                    # the diagonal across the forehead
    c.move_to(hx - 80 * s, hy - 44 * s); c.line_to(hx + 80 * s, hy - 80 * s); c.line_to(hx + 80 * s, hy - 58 * s)
    c.line_to(hx - 80 * s, hy - 24 * s); c.close_path(); c.fill()
    c.restore()


def main(out, phone_out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "SOFÍA", 68, 44, 28, bold=True)
    corp(c, "\"Office Noir\"  ·  the false suspect  ·  red lips, gold hoops", 172, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · OFFICE NOIR v2", 890, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    noir_box(c, 28, 92, 280, 528, lambda kk: so.sofia_noir(kk, 140, 500, 1.25, pose="file", face_kind="bored"),
             label="NOIR · AS RENDERED (TONE v2)")
    colour_box(c, 320, 92, 280, 528, lambda kk: so.sofia_noir(kk, 140, 500, 1.25, pose="file", face_kind="bored"),
               label="BEFORE THE PASS · KEY COLOURS")

    corp(c, "POSES", 620, 104, 10.5, bold=True)
    poses = [(dict(pose="file", face_kind="bored", stroke=0.0), "3: file, stroke 1"),
             (dict(pose="file", face_kind="bored", stroke=1.0), "3: file, stroke 2"),
             (dict(pose="file", face_kind="smirk"), "3: \"darling.\""),
             (dict(pose="bored", face_kind="side"), "side-eye at Don")]
    for i, (kw, lab) in enumerate(poses):
        x0 = 620 + i * 139
        noir_box(c, x0, 112, 133, 250, (lambda kk, kw=kw: so.sofia_noir(kk, 66, 238, 0.56, **kw)), label=lab)

    corp(c, "FACES  +  SPEECH MOUTHS (her lips stay the key red)", 620, 390, 10.5, bold=True)
    faces = [(dict(face_kind="bored"), "bored"), (dict(face_kind="brow"), "brow, eyes down"),
             (dict(face_kind="smirk"), "smirk"), (dict(face_kind="side"), "side-eye"),
             (dict(face_kind="neutral", mouth="E"), "E"), (dict(face_kind="neutral", mouth="O"), "O"),
             (dict(face_kind="neutral", mouth="A"), "A")]
    for i, (kw, lab) in enumerate(faces):
        x0 = 620 + i * 79

        def f(kk, kw=kw):
            dummy = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
            hy = so.sofia_noir(Ctx(cairo.Context(dummy), 0), 37, 0, 0.66, pose="bored", **kw)["head"][1]
            so.sofia_noir(kk, 37, 46 - hy, 0.66, pose="bored", **kw)
        noir_box(c, x0, 398, 75, 100, f, label=lab)

    corp(c, "DETAILS", 620, 526, 10.5, bold=True)

    def det_hoop(kk):
        so.hoop(kk, 66, 8)
    noir_box(c, 620, 534, 133, 86, det_hoop, label="gold hoop · 35 % in noir")

    def det_reds(kk):
        kc = kk.c
        kc.set_source_rgb(*so.HEART); kc.rectangle(14, 12, 46, 40); kc.fill()
        d.heart(kc, 98, 34, 18)
    noir_box(c, 759, 534, 133, 86, det_reds, label="lips = the heart's red")

    def det_nails(kk):
        so.nail_file(kk, 50, 70, ang=-0.9, s=1.4)
        kc = kk.c
        for i in range(4):
            ellipse(kk, 84 + i * 10, 46, 4, 5, so.NAIL, 720 + i, shadow=False, lw=1.2)
    noir_box(c, 898, 534, 133, 86, det_nails, label="nail file · dark nails")

    def det_belt(kk):
        rect(kk, 14, 36, 105, 12, so.BELT_BLACK, 730, shadow=False, lw=1.4)
        ellipse(kk, 66, 42, 9, 9, so.BELT_BLACK, 731, shadow=False, lw=1.4)
    noir_box(c, 1037, 534, 133, 86, det_belt, label="black belt (gold = hoops only)")

    s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot2_pov(Ctx(cairo.Context(s2), 0)); eng.accent_pass(s2, ACC)
    s3 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot3(Ctx(cairo.Context(s3), 0)); eng.accent_pass(s3, ACC); relight3(s3)
    bubble(Ctx(cairo.Context(s3), 0), "I sign my work,\ndarling.", 150, 40, tail=(120, 110), size=34)   # overlay, after the light
    beats = []
    for (fk, st) in (("bored", 0.0), ("brow", 0.5), ("smirk", 0.5)):
        sb = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
        shot3(Ctx(cairo.Context(sb), 0), face_kind=fk, stroke=st, line=False); eng.accent_pass(sb, ACC); relight3(sb)
        beats.append(sb)
    corp(c, "SHOT 2 · DON'S POINT OF VIEW", 28, 652, 10.5, bold=True)
    corp(c, "SHOT 3 · UNDER THE DESK LAMP", 260, 652, 10.5, bold=True)
    for (sf, x0) in ((s2, 28), (s3, 260)):
        w = 216
        c.save(); c.translate(x0, 662); c.scale(w / 540, w / 540)
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 662, w, w * 960 / 540); c.stroke()
    corp(c, "SHOT 3 BEATS", 496, 652, 10.5, bold=True)
    labs = ["filing", "stops, one brow up", "\"darling.\" smirk"]
    for i, sb in enumerate(beats):
        x0, y0, w = 496, 662 + i * 128, 66
        c.save(); c.translate(x0, y0); c.scale(w / 540, w / 540)
        c.set_source_surface(sb, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, y0, w, w * 960 / 540); c.stroke()
        wrap(c, labs[i], x0 + 72, y0 + 56, 9, 120, col=GREY)

    notes = [
        "v2: shot 3 relit, the file tilted with two strokes, shot 2 tighter, a two-line bubble, no gloss, hoops 35 %.",
        "She looks guilty to Don and ordinary on a rewatch: bored, teasing, never looking at the heart with recognition.",
        "The false suspect: everything in the frame is grey except her lips and the heart, in the same red.",
        "Shot 2 is Don's point of view: the heart held up in his fingers, and across the room her lips at the same "
        "height. The match reads with the sound off.",
        "Her lips use the heart's exact key colour (#D21F2B), so the noir pass keeps them full red. Her nails are dark "
        "burgundy, not the key: only the lips match.",
        "Gold hoops replace the Secret Santa crystal drops; gold is kept for the hoops only (the belt goes black).",
        "Hair: a 1940s wave over her screen-right eye and two loose strands soften the helmet; the silhouette stays.",
        "Shot 3: she never looks up. The desk lamp is the only light; the cone falls on her hands and face.",
        "Bubbles: white, a thick outline, a hard shadow, mono type (a stand-in until the typewriter font is licensed).",
    ]
    corp(c, "NOTES", 710, 652, 10.5, bold=True)
    y = 672
    for n in notes:
        y = wrap(c, "· " + n, 710, y, 9.5, 460, col=(0.2, 0.22, 0.28)) + 16
    flush(c)
    surf.write_to_png(out)

    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for (sf, x, lab) in ((s2, 20, "shot 2, phone width"), (s3, 430, "shot 3, phone width")):
        cp.save(); cp.translate(x, 20); sc = 390 / 540; cp.scale(sc, sc)
        cp.set_source_surface(sf, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab, x, 20 + 390 * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sofia_sheet_on_v2.png",
         sys.argv[2] if len(sys.argv) > 2 else "sofia_phone_on_v2.png")
