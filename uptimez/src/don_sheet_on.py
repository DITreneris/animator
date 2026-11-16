"""DON model sheet for "Office Noir" (don_on.py), v2 (don_sheet_on_v1.py = v1, kept). v2: the cynical default
face; tone v2 (true blacks, faces mid-grey) and a side light on the noir crops; 10B with the pink bunny in his
arms and the strawberry milk on the nightstand; the flashback (ONE DRINK / ONE INFORMANT / ONE BOSS) as three
noir frames with their caption cards. Also writes don_tone_on_v2.png (shot 2: tone v1 against tone v2 + side
light). Writes don_sheet_on_v2.png
v1 notes: Writes don_sheet_on_v1.png at 2400x2260 (drawn at 1200x1130,
2x) and don_phone_on_v1.png. The dream look is shown as it will be rendered: through engine_on's accent pass
(greyscale, the heart full red, the tie navy at 40 %). The reality look is in colour.
Sections: dream front, reality front, the dream poses by shot, faces by shot, details, the brim (control to
exposed), shot 2 as a noir 9:16 crop, shot 10B as a colour 9:16 crop, notes."""
import sys
import math
import cairo
import kit
import brand
import don_on as d
import engine_on as eng
import mom_sheet_on as ms
import mom_on as mo
import props_on as pr
from kit import Ctx, INK, ellipse, rect
from charsheets import corp, wrap
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
WASH = (0.93, 0.95, 0.94)
NOIR_WALL = (0.55, 0.52, 0.50)
ACC = [(d.HEART, 1.0), (d.TIE, 0.4)]
k = None


def noir_box(c, x, y, w, h, draw, label=None, bg=NOIR_WALL, scale=2):
    """Draw into an offscreen surface at the sheet's 2x, run the accent pass, paste it."""
    sw, sh = int(w * scale), int(h * scale)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    cc = cairo.Context(sf); cc.scale(scale, scale)
    cc.set_source_rgb(*bg); cc.paint()
    draw(Ctx(cc, 0))
    eng.accent_pass(sf, ACC)
    boxed(c, x, y, w, h, label)
    c.save(); c.translate(x, y); c.scale(1 / scale, 1 / scale); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()


def colour_box(c, x, y, w, h, draw, label=None, fill=WASH):
    boxed(c, x, y, w, h, label, fill=fill)
    c.save(); c.rectangle(x, y, w, h); c.clip(); c.translate(x, y); draw(Ctx(c, 0)); c.restore()


def lamp_wall(kk, w, h, lx, ly):
    """A dark office wall lit by one lamp: the falloff the light pass will give."""
    c = kk.c
    c.set_source_rgb(0.30, 0.28, 0.27); c.rectangle(0, 0, w, h); c.fill()
    g = cairo.RadialGradient(lx, ly, 10, lx, ly, max(w, h) * 0.9)
    g.add_color_stop_rgba(0, 0.92, 0.88, 0.80, 0.85); g.add_color_stop_rgba(1, 0.92, 0.88, 0.80, 0.0)
    c.set_source(g); c.rectangle(0, 0, w, h); c.fill()


def shot2(kk, light=True):
    """540x960: low-angle close-up, the heart held up to his eye, smug, brim half up; lamp from screen left."""
    lamp_wall(kk, 540, 960, 120, 160)
    d.don_noir(kk, 290, 1380, 3.2, pose=d.POSE_HEART_EYE, face="smug", brim=0.55)


def noir_frame(fn, light=0.0, **kw):
    """Render a 540x960 noir frame like the engine: draw, accent pass, then the light (so accents keep their key)."""
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(sf)
    fn(Ctx(cc, 0), **kw)
    eng.accent_pass(sf, ACC)
    if light:
        eng.side_light(cairo.Context(sf), 0, 0, 540, 960, from_left=True, amount=light)
    return sf


def caption(kk, s, x=24, y=40):
    """The pulp narration card (typewriter stand-in font until the font is licensed)."""
    c = kk.c
    c.select_font_face("DejaVu Sans Mono", 0, 1); c.set_font_size(34)
    w = c.text_extents(s).x_advance + 32
    c.set_source_rgba(0, 0, 0, 0.8); c.rectangle(x + 6, y + 6, w, 58); c.fill()
    c.set_source_rgb(0.97, 0.95, 0.90); c.rectangle(x, y, w, 58); c.fill()
    c.set_source_rgb(0, 0, 0); c.set_line_width(3); c.rectangle(x, y, w, 58); c.stroke()
    c.move_to(x + 16, y + 41); c.show_text(s)


def mom_shadow(kk, x, feet, s, skew=-0.25, alpha=0.82):
    """Mom as a black wall shadow: her figure used as a mask, skewed away from the light."""
    import cairo as _c
    sf = _c.ImageSurface(_c.FORMAT_ARGB32, 540, 960)
    cc = _c.Context(sf)
    mo.mom(Ctx(cc, 0), 270, 900, 2.2, pose="hip_mug")
    c = kk.c
    c.save()
    c.translate(x, feet); c.transform(_c.Matrix(1, 0, skew, 1, 0, 0)); c.scale(s / 2.2, s / 2.2); c.translate(-270, -900)
    c.set_source_rgba(0.02, 0.02, 0.03, alpha); c.mask_surface(sf, 0, 0)
    c.restore()


def flash_drink(kk):
    c = kk.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(200, 420, 20, 200, 420, 420)
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.9); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    rect(kk, -20, 640, 580, 400, (0.20, 0.17, 0.15), 901)                               # the bar top
    pr.flask(kk, 270, 560, 3.2)
    caption(kk, "ONE DRINK.")


def flash_informant(kk):
    c = kk.c
    c.set_source_rgb(0.06, 0.06, 0.07); c.rectangle(0, 0, 540, 960); c.fill()
    c.set_source_rgba(0.98, 0.95, 0.85, 0.85)                                           # the lamp cone
    c.move_to(230, 160); c.line_to(310, 160); c.line_to(520, 760); c.line_to(20, 760); c.close_path(); c.fill()
    kit.cut(kk, [(200, 120), (340, 120), (310, 170), (230, 170)], (0.15, 0.15, 0.16), shadow=False)
    rect(kk, -20, 720, 580, 300, (0.25, 0.22, 0.20), 902)
    pr.bunny(kk, 270, 730, 3.0, mode="noir")
    caption(kk, "ONE INFORMANT.")


def flash_boss(kk):
    c = kk.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, 0, 540, 960); c.fill()
    g = cairo.RadialGradient(330, 420, 20, 330, 420, 520)                               # the streetlamp on the wall
    g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.95); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
    c.set_source(g); c.rectangle(0, 0, 540, 960); c.fill()
    mom_shadow(kk, 300, 900, 2.0, skew=-0.05, alpha=0.9)                                # the boss, huge on the wall
    rect(kk, 30, 40, 14, 920, (0.10, 0.10, 0.11), 903, shadow=False)                    # lamp post, foreground
    d.don_noir(kk, 150, 1010, 1.45, brim=1.0)                                           # Don passes, small
    caption(kk, "ONE BOSS.")


def shot10b(kk):
    """540x960, colour: Don frozen in bed, eyes open, fedora lifted 4 px, hugging the pink bunny; strawberry milk
    on the nightstand; the heart on his pocket."""
    ms.bedroom(kk)
    rect(kk, 410, 600, 150, 260, (0.62, 0.45, 0.30), 812)                                 # the nightstand
    pr.milk(kk, 470, 600, 1.7)
    d.don_pj(kk, 230, 1370, 2.8, face="frozen", lift=4, bunny=True)
    c = kk.c
    rect(kk, -20, 860, 600, 200, (0.70, 0.84, 0.94), 811)                                  # the blanket over him
    c.set_source_rgb(0.98, 0.95, 0.88); c.rectangle(-20, 860, 600, 18); c.fill()
    kit.text(kk, "Mom: off-frame", 400, 940, 15, (0.4, 0.4, 0.45))


def main(out, phone_out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "DON", 68, 44, 28, bold=True)
    corp(c, "\"Office Noir\"  ·  the detective in his head  ·  the man in his mother's house", 140, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · OFFICE NOIR v2", 890, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W2 - 24, 70); c.stroke()

    noir_box(c, 28, 92, 280, 528, lambda kk: d.don_noir(kk, 140, 500, 1.15, brim=0.6),
             label="DREAM · AS RENDERED (NOIR PASS)", bg=(0.82, 0.80, 0.77))
    colour_box(c, 320, 92, 280, 528, lambda kk: d.don_pj(kk, 140, 500, 1.15, face="deflated", bunny=True),
               label="REALITY · PYJAMAS, THE FEDORA, THE BUNNY")

    corp(c, "DREAM POSES BY SHOT", 620, 104, 10.5, bold=True)
    poses = [(dict(pose=d.POSE_HEART_EYE, face="smug", brim=0.55), "2: the heart to his eye"),
             (dict(pose=d.POSE_POINT, face="smug", brim=0.8), "2: the smug point"),
             (dict(pose=d.POSE_LEAN, face="neutral", brim=1, heart_on=True, lean=12), "5: the lean (CCTV)"),
             (dict(pose=d.POSE_OBJECT, face="indignant", brim=0), "8: I object")]
    for i, (kw, lab) in enumerate(poses):
        x0 = 620 + i * 139
        dx = 92 if kw["pose"] == d.POSE_POINT else (56 if kw.get("lean") else 66)
        noir_box(c, x0, 112, 133, 250, (lambda kk, kw=kw, dx=dx: d.don_noir(kk, dx, 238, 0.56, **kw)), label=lab,
                 bg=(0.82, 0.80, 0.77))

    corp(c, "FACES BY SHOT", 620, 390, 10.5, bold=True)
    faces = [("cynic", 1.0, "1: cynic"), ("smug", 0.6, "2: smug"), ("drop", 0.9, "6: it dies"),
             ("almost", 0.0, "7: almost"), ("indignant", 0.0, "8: object"), ("frozen", None, "10B: frozen"),
             ("deflated", None, "bed: defeated")]
    for i, (face, brim, lab) in enumerate(faces):
        x0 = 620 + i * 79
        if brim is None:
            colour_box(c, x0, 398, 75, 100, (lambda kk, face=face: d.don_pj(kk, 37, 48 - d.HY * 0.62, 0.62, face=face)),
                       label=lab)
        else:
            noir_box(c, x0, 398, 75, 100, (lambda kk, face=face, brim=brim: d.don_noir(kk, 37, 48 - d.HY * 0.62, 0.62,
                                                                                         face=face, brim=brim)),
                     label=lab, bg=(0.82, 0.80, 0.77))

    corp(c, "DETAILS", 620, 526, 10.5, bold=True)

    def det_fedora(kk):
        d.fedora(kk, 66, 62, 0.95)
    colour_box(c, 620, 534, 133, 86, det_fedora, label="charcoal fedora, black band")

    def det_lapel(kk):
        kc = kk.c
        kc.set_source_rgb(*d.TRENCH_SHADE); kc.rectangle(0, 0, 133, 86); kc.fill()
        d.outline_mark(kc, 38, 38, 22)
        d.heart(kc, 96, 38, 22)
    noir_box(c, 759, 534, 133, 86, det_lapel, label="lapel: outline · heart")

    def det_tie(kk):
        kc = kk.c
        kc.set_source_rgb(*d.TIE); kc.rectangle(14, 10, 46, 46); kc.fill()
    def det_tie_noir(kk):
        kc = kk.c
        kc.set_source_rgb(*d.TIE); kc.rectangle(14, 10, 46, 46); kc.fill()
    colour_box(c, 898, 534, 133, 86, det_tie, label="tie: navy key • noir 40 %")
    noir_box(c, 898 + 66, 534 + 6, 60, 52, det_tie_noir, bg=(1, 1, 1))

    def det_pocket(kk):
        kc = kk.c
        kc.set_source_rgb(*d.PJ); kc.rectangle(0, 0, 133, 86); kc.fill()
        rect(kk, 40, 14, 54, 54, d.PJ, 3, shadow=False, lw=1.8)
        kc.set_source_rgb(*d.PJ_PIPE); kc.set_line_width(2.4); kc.move_to(41, 19); kc.line_to(93, 19); kc.stroke()
        d.heart(kc, 67, 44, 17)
    colour_box(c, 1037, 534, 133, 86, det_pocket, label="pyjama pocket + the heart")

    corp(c, "FLASHBACK (twins in 10B: milk, the pink bunny, Mom)", 28,
         846, 10.5, bold=True)
    for i, fn in enumerate((flash_drink, flash_informant, flash_boss)):
        sf = noir_frame(fn)
        x0, w = 28 + i * 140, 134
        c.save(); c.rectangle(x0, 856, w, 238); c.clip(); c.translate(x0, 856); c.scale(w / 540, w / 540)
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 856, w, 238); c.stroke()
        if i == 0:
            flash = [sf]
        else:
            flash.append(sf)
    corp(c, "THE BRIM: IN CONTROL, THEN EXPOSED", 28, 652, 10.5, bold=True)
    for i, (b, lab) in enumerate(((1.0, "1–6: eyes hidden"), (0.5, "on the way up"), (0.0, "7: Pam's touch, both eyes"))):
        x0 = 28 + i * 140
        noir_box(c, x0, 662, 134, 150, (lambda kk, b=b: d.don_noir(kk, 67, 76 - d.HY * 1.05, 1.05, face="almost" if b == 0
                                                                     else "neutral", brim=b)), label=lab,
                 bg=(0.82, 0.80, 0.77))

    s2 = noir_frame(shot2, light=0.62)
    s10 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    shot10b(Ctx(cairo.Context(s10), 0))
    corp(c, "SHOT 2 (NOIR)", 448, 652, 10.5, bold=True)
    corp(c, "SHOT 10B (COLOUR)", 660, 652, 10.5, bold=True)
    for (sf, x0) in ((s2, 448), (s10, 660)):
        w = 196
        c.save(); c.translate(x0, 662); c.scale(w / 540, w / 540)
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 662, w, w * 960 / 540); c.stroke()

    notes = [
        "v2: the dream default is \"cynic\" (half lids, a lopsided smirk); tone v2 gives true blacks and mid-grey faces.",
        "Dream: a light trench, buttoned (the Secret Santa ketchup is under it), collar up, a navy tie, a fedora worn low.",
        "The brim shadow is the light rule: eyes hidden while he controls the case; it lifts in shot 7 when Pam touches him.",
        "The plant: a faint sticker outline on his screen-right lapel in shots 1–2; the heart sits there in shots 5 and 7.",
        "Shot 2 (lipstick clue): he holds the heart up to his eye; in the full shot its red lines up with Sofía's lips.",
        "Reality: pale blue pyjamas, the same fedora, the same paper heart on his pocket. 10B: frozen, the fedora lifts 4 px.",
        "The agent earpiece and the card are gone in this episode. Faces are his existing set plus \"almost\" and \"frozen\".",
        "Every noir prop has a twin in reality: flask \u2192 strawberry milk, the grey informant \u2192 the pink bunny, the boss \u2192 Mom.",
        "Caption cards use a stand-in mono font until the typewriter font's license is checked.",
    ]
    corp(c, "NOTES", 872, 652, 10.5, bold=True)
    y = 672
    for n in notes:
        y = wrap(c, "· " + n, 872, y, 9.0, 300, col=(0.2, 0.22, 0.28)) + 16
    flush(c)
    surf.write_to_png(out)

    # tone comparison: shot 2 with the v1 curve and no light against the v2 curve with the side light
    tv = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 800)
    ct = cairo.Context(tv); ct.set_source_rgb(*BG); ct.paint()
    old = eng.TONE
    for i, (tone, light, lab) in enumerate((("v1", False, "tone v1: grey-coloured"), ("v2", True, "tone v2 + side light"))):
        eng.TONE = tone
        sf = noir_frame(shot2, light=0.62 if light else 0.0)
        ct.save(); ct.translate(20 + i * 410, 20); ct.scale(390 / 540, 390 / 540)
        ct.set_source_surface(sf, 0, 0); ct.get_source().set_filter(cairo.FILTER_BEST); ct.paint(); ct.restore()
        corp(ct, lab, 20 + i * 410, 20 + 390 * 960 / 540 + 22, 14, col=GREY)
    eng.TONE = old
    tv.write_to_png(out.replace("don_sheet_on", "don_tone_on"))

    ps_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 840, 760)
    cp = cairo.Context(ps_); cp.set_source_rgb(*BG); cp.paint()
    for (sf, x, lab) in ((s2, 20, "shot 2, phone width"), (s10, 430, "shot 10B, phone width")):
        cp.save(); cp.translate(x, 20); sc = 390 / 540; cp.scale(sc, sc)
        cp.set_source_surface(sf, 0, 0); cp.get_source().set_filter(cairo.FILTER_BEST); cp.paint(); cp.restore()
        corp(cp, lab, x, 20 + 390 * 960 / 540 + 18, 13, col=GREY)
    ps_.write_to_png(phone_out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_on_v2.png",
         sys.argv[2] if len(sys.argv) > 2 else "don_phone_on_v2.png")
