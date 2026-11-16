"""Pam's Christmas v4 sheet (pam_sheet_xmas3_v3.py = the v3 sheet script). v4: the review fixes; the film row is
the new shot-10 order (line with the mask up, the visible drop, the hold) plus the side-eye.
v3 notes: Pam's Christmas v3 sheet (pam_xmas3.py): v2 against v3, the faces, the mask states, and five frames of the
real film with the new Pam routed in (xmas_pam3). Writes pam_sheet_xmas_v3.png. Earlier sheets untouched."""
import sys
import cairo
import kit
import brand
import pam_xmas as px
import pam_xmas3 as p3
import xmas_anim as xa
import xmas_pam3 as route
from kit import Ctx, INK
from charsheets import corp, wrap

W, H = 1200, 1330
BG = (0.97, 0.96, 0.93)
GREY = (0.35, 0.40, 0.50)
PANEL = (0.93, 0.90, 0.84)


def head(c, x, y, sc, draw):
    """A head-and-shoulders crop of a figure drawn by draw(k, fx, feet, s)."""
    c.save(); c.rectangle(x, y, 170, 190); c.clip()
    c.set_source_rgb(*PANEL); c.paint()
    s = 2.1
    feet = y + 100 - (-300 * kit.PEOPLE["PAM"]["h"] + 34) * s          # the head centre at y + 100
    draw(Ctx(c, 0), x + 85, feet, s)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x, y, 170, 190); c.stroke()


def film_frame(t):
    for t0, t1, fn in xa.PANELS:
        if t0 <= t < t1:
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
            fn(Ctx(cairo.Context(s), 0), t, t - t0)
            return s


def main(out):
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * 2, H * 2)
    c = cairo.Context(sheet); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 26, bold=True)
    corp(c, "\"Happy Compliance\" v4  ·  deadpan, the side-eye, the mask drop", 132, 44, 13, col=GREY)
    corp(c, "UPTIMEZ INC. · CHARACTER MODEL SHEET · CHRISTMAS v4", 880, 34, 9.5, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 70); c.line_to(W - 24, 70); c.stroke()

    # before / after
    corp(c, "BEFORE (v2) and AFTER (v4)", 24, 98, 12, bold=True)
    for i, (lab, fn, kw) in enumerate((("v2: no streak, no glasses, mask at the neck", px.pam, {}),
                                        ("v4: pressed lips, mask up flatter, the tape clear", p3.pam, {}),
                                        ("v4 hero: the mask DOWN over her readers", p3.pam, dict(mask="down", **p3.HERO)))):
        x0 = 24 + i * 250
        c.save(); c.rectangle(x0, 110, 236, 470); c.clip(); c.set_source_rgb(*PANEL); c.paint()
        pose = p3.POSE_HERO if "mask" in kw else p3.POSE_THERMOS
        fn(Ctx(c, 0), x0 + 118, 560, 1.25, pose, "neutral", look=(0.8, 0), thermos_in_hand="mask" not in kw, **kw)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 110, 236, 470); c.stroke()
        wrap(c, lab, x0, 596, 9.5, 236, col=(0.25, 0.28, 0.36))

    # faces
    corp(c, "FACES (deadpan; one side-eye, one look over)", 790, 98, 12, bold=True)
    faces = (("neutral", (0.8, 0), "neutral: pressed lips"), ("over", (0, 0), "over: half lids, eyes up, glasses low"),
             ("glance", (1.0, 0.1), "glance: a fond side-eye at Don"), ("squint", (0, 0), "squint (blink)"))
    for i, (f, lk, lab) in enumerate(faces):
        x0, y0 = 790 + (i % 2) * 190, 110 + (i // 2) * 232
        head(c, x0, y0, 1, lambda k, fx, feet, s, f=f, lk=lk: p3.pam(k, fx, feet, s, p3.POSE_FISTS, f, lk))
        wrap(c, lab, x0, y0 + 206, 9.5, 170, col=(0.25, 0.28, 0.36))
    corp(c, "MOUTHS (rose lips)", 790, 590, 11, bold=True)
    for i, m in enumerate(("A", "E", "O", "C")):
        x0 = 790 + i * 95
        c.save(); c.translate(x0, 600); c.scale(0.55, 0.55)
        head(c, 0, 0, 1, lambda k, fx, feet, s, m=m: p3.pam(k, fx, feet, s, p3.POSE_FISTS, "neutral", (0, 0), mouth=m))
        c.restore()
        corp(c, m, x0 + 40, 718, 10, bold=True)

    # the film
    corp(c, "IN THE FILM (the release's own frames, the new Pam routed in)", 24, 760, 12, bold=True)
    times = ((9.65, "9.65 s  the side-eye at Don, then the fists"),
             (23.6, "23.6 s  \"Human in the loop.\" said with the mask UP"),
             (24.45, "24.45 s  her hand goes up, the mask comes down"),
             (24.55, "24.55 s  mid-drop (0.35 s, visible)"),
             (25.2, "25.2 s  down over her readers: push-in, silent hold"))
    route.apply()
    try:
        frames = [film_frame(t) for t, _ in times]
    finally:
        route.restore()
    for i, ((t, lab), fr) in enumerate(zip(times, frames)):
        x0, w = 24 + i * 232, 220
        h = w * 960 / 540
        c.save(); c.translate(x0, 774); c.scale(w / 540, w / 540); c.set_source_surface(fr, 0, 0)
        c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1); c.rectangle(x0, 774, w, h); c.stroke()
        wrap(c, lab, x0, 774 + h + 16, 9.5, w, col=(0.25, 0.28, 0.36))

    notes = ("Kept: the costume joke (cardboard mask with tape, towel cape, cardigan one button off, paper P, thermos, "
             "hero stance) and her deadpan. Sofía unchanged.",
             "New: the grey streak and smile lines, reading glasses low on the gold bead chain, dusty-rose lips "
             "(her canon from Thanksgiving, Mandatory Fun, Secret Santa).",
             "Shot 10 reordered: the line first with the mask up, then the drop and a 0.5 s hold; the mask is never at her neck. "
             "Streak and chain kept as series canon.")
    for i, n in enumerate(notes):
        corp(c, "- " + n, 24, 1262 + i * 20, 9.5, col=(0.25, 0.28, 0.36))
    sheet.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_sheet_xmas_v4.png")
