"""v2 (v1 pinned in don_sheet_ss_v1.py). DON model sheet for "Secret Santa" (don_ss.py v2): AGENT SECRET SANTA,
80% incompetent agent, 20% Christmas: no hat, the bald dome free, the bigger card, the fake beard as an optional
shot 3 gag, and a phone-size A/B/C of the three heads. Writes don_sheet_ss_v2.png at 2400x2260
(drawn at 1200x1130, 2x), plus don_heads_phone_v2.png: the look (office v4 + cheap shades, an earpiece, his TOP SECRET card
with a ketchup thumbprint; no police kit), faces and poses by shot, mouths, details (the pompom bounce, the shades
on and down, the card), 9:16 camera crops on the drawings and the shades/hat beats through the film."""
import sys
import math
import cairo
import kit
import brand
import don_mf as dm
import don_ss as ds
import pam_ss as ps
import sofia_ss as ss
import robot_mf as rm
import props_ss as props
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush
from sofia_sheet_mf import HY as SHY

W2, H2 = 1200, 1130
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.92, 0.96)
RED = (0.72, 0.12, 0.16)
HY = ds.HY
k = None


def head(cx, cy, s, face, look=(0, 0), shades="on", mouth=None, card=None):
    ds.don(k, cx, cy - HY * s, s, "stand", face, look=look, shades=shades, mouth=mouth, card=card)


def clip_box(x, y, w, h, draw, fill=None, label=None, frame=False):
    c = k.c
    if frame:
        c.save(); c.rectangle(x, y, w, h); c.clip()
        c.set_source_rgb(*(fill or kit.WALL)); c.rectangle(x, y, w, h); c.fill()
        draw()
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()
        if label:
            corp(c, label, x, y + h + 12, 8.5, col=GREY, bold=True)
    else:
        boxed(c, x, y, w, h, label, fill=fill or (1, 1, 1))
        c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def door(c, x, y, w, h):
    c.set_source_rgb(0.62, 0.45, 0.30); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(x, y, w, h); c.stroke()
    c.set_source_rgb(0.30, 0.22, 0.16); c.rectangle(x + 6, y + 6, w - 12, h - 6); c.fill()


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "DON", 68, 44, 28, bold=True)
    corp(c, "\"Secret Santa\"  ·  AGENT SECRET SANTA  ·  he heard \"secret\" and took it as a mission", 150, 44, 13,
         col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · SECRET SANTA v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # 1. front
    c.set_source_rgb(*ACCENT); c.rectangle(24, 80, 240, 450); c.fill()
    ds.don(k, 144, 500, 0.9, "stand", "neutral", seed=71)
    corp(c, "FRONT · OFFICE v4 + AGENT KIT, NO HAT", 32, 524, 9, col=brand.NAVY, bold=True)

    # 2. Mandatory Fun / Secret Santa
    corp(c, "MANDATORY FUN  ·  SECRET SANTA", 284, 92, 10, bold=True)
    boxed(c, 284, 98, 330, 210)
    c.save(); c.rectangle(284, 98, 330, 210); c.clip()
    dm.don(k, 376, 300, 0.52, "stand", "neutral", seed=72)
    ds.don(k, 524, 300, 0.52, "stand", "neutral", seed=72)
    c.restore()
    for lx, lw, lab, col in ((318, 112, "OLD · AI POLICE", GREY), (462, 128, "FINAL v2 · AGENT SANTA", RED)):
        c.set_source_rgb(1, 1, 1); c.rectangle(lx, 104, lw, 16); c.fill()
        c.set_source_rgb(*col); c.set_line_width(1.2); c.rectangle(lx, 104, lw, 16); c.stroke()
        corp(c, lab, lx + 6, 116, 8.5, col=col, bold=True)
    corp(c, "Same Don, vest and ketchup. A cheap agent kit; the set and his card say Christmas.", 290, 322, 9, col=GREY)

    # 3. faces
    corp(c, "FACES, BY SHOT  (the fool, at his own expense; vain, never lewd)", 284, 348, 10, bold=True)
    faces = [("showman", (0, 0), "on", None, "3: entrance"), ("showman", (0, 0), "on", "A", "3: \"Santa!\""),
             ("neutral", (1, 0), "on", None, "5: past Pam"), ("smug", (1, 0), "down", None, "6: vain"),
             ("smug", (1, 0), "down", "E", "6: \"mirror\""), ("smug", (1, -0.2), "on", None, "15: preens")]
    for i, (f, lk, sh, m, lab) in enumerate(faces):
        x, y = 284 + i * 55.5, 354
        clip_box(x, y, 52.5, 92, lambda x=x, y=y, f=f, lk=lk, sh=sh, m=m: head(x + 26, y + 40, 0.6, f, lk, sh, m),
                 fill=(1.0, 0.95, 0.93) if i == 3 else None, label=lab)
    corp(c, "MOUTHS  (big and loud; he talks wide)", 284, 466, 10, bold=True)
    for i, m in enumerate(("M", "E", "F", "O", "A", "C", "U")):
        x, y = 284 + i * 47.4, 472
        clip_box(x, y, 45, 58, lambda x=x, y=y, m=m: head(x + 22, y + 2, 0.8, "neutral", (0, 0), "on", m), label=m)

    # 4. poses
    corp(c, "POSES", 634, 92, 10, bold=True)
    poses = [(ds.POSE_WIDE, "showman", dict(beard="slipped"), "3: beard slipped (opt.)"),
             (ds.POSE_WIDE_CARD, "showman", dict(card="hand"), "3: the card"),
             ("stand", "neutral", dict(look=(1, 0)), "5: eyes past her"),
             (ds.POSE_SMOOTH, "smug", dict(shades="down", look=(1, 0), glint=True), "6: smooths the dome"),
             ("stand", "smug", dict(look=(1, -0.2), lean=5), "15: preens")]
    for i, (pose, f, kw, lab) in enumerate(poses):
        x = 634 + i * 109
        clip_box(x, 98, 105, 210, lambda x=x, pose=pose, f=f, kw=kw, i=i: ds.don(k, x + 52, 286, 0.46, pose, f,
                                                                                seed=80 + i, **kw),
                 fill=(1.0, 0.95, 0.93) if i == 3 else None, label=lab)

    # 5. details
    corp(c, "DETAILS", 634, 348, 10, bold=True)
    def beard_detail():
        ds.don(k, 676, 434 - HY * 0.6, 0.6, "stand", "showman", beard="on", seed=10)
        ds.don(k, 762, 434 - HY * 0.6, 0.6, "stand", "showman", beard="slipped", seed=11)
    clip_box(634, 354, 170, 160, beard_detail, label="optional gag: beard on · slipped")
    def shades_detail():
        head(855, 440, 0.72, "neutral", (0, 0), "on")
        head(938, 440, 0.72, "smug", (1, 0), "down")
    clip_box(812, 354, 170, 160, shades_detail, label="shades on · slid down (6)")
    clip_box(990, 354, 186, 160, lambda: ds.secret_card(k, 1083, 428, 2.6, -0.06, 3), fill=(1.0, 0.95, 0.93),
             label="his card: ketchup-sealed")

    # 6. 9:16 crops
    y0 = 562
    corp(c, "9:16 CROPS ON THE DRAWINGS  (stand-ins for the others)", 24, y0 - 6, 10, bold=True)
    W, H, G = 98, 174, 104

    def c3():
        x = 24
        door(c, x + 8, y0 - 10, 84, 200)
        c.save(); c.translate(x + 49, y0 + 87); c.rotate(math.radians(-6)); c.translate(-(x + 49), -(y0 + 87))
        ds.don(k, x + 46, y0 + 250, 0.6, ds.POSE_WIDE_CARD, "showman", card="hand", seed=91)
        c.restore()
        c.set_source_rgb(0.78, 0.18, 0.20); c.rectangle(x + 4, y0 + 140, 44, 40); c.fill()     # Pam's present, foreground
        c.set_source_rgb(*props.LIP_GOLD); c.rectangle(x + 22, y0 + 140, 7, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x + 4, y0 + 140, 44, 40); c.stroke()
    clip_box(24, y0, W, H, c3, frame=True, label="3: low, dutch")

    def c6():
        x = 24 + G
        def bg(lc):
            rm.robot(Ctx(lc, 0), x + 90, y0 + 150, 0.42, "stand", "approved", seed=93)
        props.soft(c, bg, 1.8)
        head(x + 50, y0 + 100, 0.85, "smug", (1, 0), "down", "E")
        def fg(lc):                                     # Pam's hair and glasses chain soft at the frame edge
            ps.pam(Ctx(lc, 0), x - 26, y0 + 330, 1.1, "stand", "hopeful", look=(1, 0), glasses="chain", seed=94)
        props.soft(c, fg, 2.4)
    clip_box(24 + G, y0, W, H, c6, frame=True, label="6: over Pam")

    def c6b():
        x = 24 + 2 * G
        ds.don(k, x + 38, y0 + 290, 0.8, ds.POSE_SMOOTH, "smug", look=(1, 0), shades="down", glint=True, seed=95)
    clip_box(24 + 2 * G, y0, W, H, c6b, frame=True, label="6: the dome")

    def c15():
        x = 24 + 3 * G
        ss.sofia(k, x + 74, y0 + 250, 0.62, "stand", "unimpressed", look=(1.0, 0.1), lag=(-5, 0), badge=False, seed=96)
        ds.don(k, x + 24, y0 + 250, 0.56, "stand", "smug", look=(1, -0.2), lean=6, seed=97)
    clip_box(24 + 3 * G, y0, W, H, c15, frame=True, label="15: she turns away")

    # 7. the beats
    x1 = 452
    corp(c, "HIS BEATS  (short: he interrupts, the film goes back to Pam)", x1, y0 - 6, 10, bold=True)
    boxed(c, x1, y0, 724, 174)
    beats = [("3", "Door bangs. Arms wide, TOP SECRET SANTA flashed. Shades ON. 2.6 s, no more."),
             ("3", "\"Secret Santa! HR-approved!\"  The robot THUNKs APPROVED on the word."),
             ("5", "He never looks at Pam: his eyes go past her to Sofía. Shades ON."),
             ("6", "CU: shades slide DOWN his nose, eyes on Sofía; his palm glides over the bare dome (squeak, glint)."),
             ("6", "\"Sofía. Or a full-length mirror.\"  Smug half-lids, a one-sided smirk. Vain, not lewd."),
             ("15", "Background only: he preens at Sofía, she turns away. No line.")]
    for i, (sh, txt) in enumerate(beats):
        corp(c, sh, x1 + 14, y0 + 26 + i * 25, 12, col=brand.NAVY, bold=True)
        corp(c, txt, x1 + 44, y0 + 26 + i * 25, 10, col=INK)

    # 8. A / B / C at phone size
    y1 = 790
    corp(c, "THE HEAD, A / B / C AT PHONE SIZE  (shot 3 and shot 6 for each; which Don is most convinced he's a spy?)",
         24, y1 - 6, 10, bold=True)
    boxed(c, 24, y1, 1152, 180)
    opts = [("A · v1 hat", dict(hat=True), RED, "hides the dome; 3 things on his head"),
            ("B · fake beard", dict(beard="on"), GREY, "funny, but most Santa; covers the smirk"),
            ("C · bald agent", dict(), (0.10, 0.50, 0.30), "RECOMMENDED: dome free, face reads")]
    for i, (lab, kw, col, why) in enumerate(opts):
        x = 40 + i * 380
        for j in range(2):
            fx = x + j * 84
            def fr(fx=fx, j=j, kw=kw):
                if j == 0:
                    ds.don(k, fx + 40, y1 + 178, 0.46, ds.POSE_WIDE_CARD, "showman", card="hand", seed=130, **kw)
                else:
                    kk = dict(kw)
                    if "beard" in kk:
                        kk["beard"] = "on"
                    ds.don(k, fx + 34, y1 + 335, 0.78, ds.POSE_SMOOTH, "smug", look=(1, 0), shades="down",
                           glint=True, seed=131, **kk)
            clip_box(fx, y1 + 10, 78, 139, fr, frame=True)
        corp(c, lab, x + 172, y1 + 34, 13, col=col, bold=True)
        corp(c, "left: shot 3", x + 172, y1 + 56, 8.5, col=GREY)
        corp(c, "right: shot 6", x + 172, y1 + 70, 8.5, col=GREY)
        for li, part in enumerate(why.split("; ")):
            corp(c, part, x + 172, y1 + 98 + li * 15, 9, col=INK)
        corp(c, "real size: don_heads_phone_v2.png", x + 4, y1 + 166, 7.5, col=GREY) if i == 0 else None

    # 9. notes
    y2 = 996
    corp(c, "NOTES", 24, y2, 10, bold=True)
    notes = ["Office v4 unchanged: navy fleece vest, white shirt, khakis, the ketchup squiggle, staff badge.",
             "80% incompetent agent, 20% Christmas: black shades, a coiled earpiece, TOP SECRET SANTA card. No hat.",
             "No tuxedo, no trench coat, no numbers or gadgets from any real spy franchise: original only.",
             "The card's ketchup thumbprint is his 'seal'. It rhymes with the robot: Don plays classified, HR classifies.",
             "Shades ON for the entrance; slid DOWN in shot 6 so his eyes visibly go past Pam to Sofía.",
             "He is bald and nothing covers it: the 'hair' smooth is his palm on the bare dome, a squeak and a glint.",
             "Optional: a fake beard on elastic in shot 3 that slips to his neck on \"HR-approved!\"; he doesn't notice.",
             "Don is the fool, at his own expense; he gets 2 short shots and a background beat, then it's Pam's film."]
    for i, n in enumerate(notes):
        corp(c, "·  " + n, 24 + (i % 2) * 588, y2 + 24 + (i // 2) * 30, 10, col=INK)
    flush(c)
    surf.write_to_png(out)


def phone_heads(out):
    """Shot 6 for A / B / C at real phone size: three 360x640 frames side by side."""
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, kw in enumerate((dict(hat=True), dict(beard="on"), dict())):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        c.set_source_rgb(*kit.WALL); c.paint()
        c.translate(360 * i, 0); c.scale(360 / 78.0, 360 / 78.0)
        ds.don(k, 34, 325, 0.78, ds.POSE_SMOOTH, "smug", look=(1, 0), shades="down", glint=True, seed=131,
               **kw)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "don_sheet_ss_v2.png")
    phone_heads("don_heads_phone_v2.png")
