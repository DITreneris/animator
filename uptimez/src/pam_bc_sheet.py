"""PAM, "The Best Candidate": model sheet v2 (pam_bc_sheet_v1.py = v1, kept). v2 after the audit: six frames, the
paddle visibly coming down, a pen that reads as a pen, the mirror as three steps (Mom smiles, Pam copies, \"No.\")
with Don held in frame so it is plain whose mother she is, and subtitles on the two lines that carry a joke.
Writes pam_bc_sheet_v2.png at 2400x1960 (1200x980, 2x) and pam_bc_phone_v2.png (six 360x640 frames)."""
import sys
import cairo
import kit
import brand
import pam_ss as ps
import pam_bc as pb
import mom_bc as mb
import don_bc as db
from kit import Ctx, INK
from charsheets import corp
from pam_sheet_mf import boxed, flush

W2, H2 = 1200, 980
GREY = (0.35, 0.40, 0.50)
ACCENT = (0.90, 0.92, 0.96)
WARM = (1.0, 0.95, 0.93)
TABLE = (0.47, 0.34, 0.24)
TABLE_TOP = (0.60, 0.46, 0.33)
k = None


def box(x, y, w, h, draw, label=None, warm=False):
    c = k.c
    boxed(c, x, y, w, h, label, fill=WARM if warm else (1, 1, 1))
    c.save(); c.rectangle(x, y, w, h); c.clip(); draw(); c.restore()


def panel(x, y, u, draw_her):
    """A 180x320 frame: the wall, Pam from the waist up, the panel table across the bottom."""
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, 180 * u, 320 * u); c.fill()
    draw_her()
    kit.rect(k, x - 6 * u, y + 246 * u, 192 * u, 14 * u, TABLE_TOP, 811, shadow=False, lw=2 * u)
    c.set_source_rgb(*TABLE); c.rectangle(x, y + 259 * u, 180 * u, 61 * u); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(2 * u); c.move_to(x, y + 259 * u); c.line_to(x + 180 * u, y + 259 * u); c.stroke()


def subtitle(x, y, u, lines, yy=286):
    """Sound off: the line itself, small, over the bottom of the frame."""
    c = k.c
    for i, t in enumerate(lines):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(11.5 * u)
        w = c.text_extents(t).x_advance
        tx, ty = x + 90 * u - w / 2, y + (yy + i * 15) * u
        c.set_source_rgba(0.08, 0.08, 0.12, 0.82); c.rectangle(tx - 5 * u, ty - 11 * u, w + 10 * u, 15 * u); c.fill()
        c.set_source_rgb(1, 1, 1); c.move_to(tx, ty); c.show_text(t)


def gag_lower(x, y, u=1.0):
    panel(x, y, u, lambda: pb.pam(k, x + 54 * u, y + 374 * u, 1.0 * u, pb.POSE_LOWER, "dip", paddle="YES"))


def gag_kind(x, y, u=1.0):
    panel(x, y, u, lambda: pb.pam(k, x + 92 * u, y + 374 * u, 1.0 * u, pb.POSE_WRITE, "peer", note="KIND", pen=True))


def gag_ask(x, y, u=1.0):
    panel(x, y, u, lambda: pb.pam(k, x + 92 * u, y + 374 * u, 1.0 * u, pb.POSE_ASK, "probe", mouth="E", pen=True, lean=-3))
    subtitle(x, y, u, ["\"Any family in", "the company?\""], 284)


def _trio(x, y, u, mom_face, mom_look, pam_face, pam_pose, tilt=None):
    c = k.c
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, 180 * u, 320 * u); c.fill()
    db.don(k, x + 16 * u, y + 350 * u, 0.7 * u, "stand", "obey", look=(1.0, 0.3), tense=True, seed=500)
    mb.mom(k, x + 84 * u, y + 350 * u, 0.7 * u, "bag", mom_face, look=mom_look, seed=70, tilt=tilt)
    pb.pam(k, x + 150 * u, y + 350 * u, 0.7 * u, pam_pose, pam_face, note="" if pam_pose == pb.POSE_MIRROR else None,
           lean=-4 if pam_face == "mirror" else 0)


def gag_m1(x, y, u=1.0):
    _trio(x, y, u, "sweet", (0, 0), "hopeful", "stand")


def gag_m2(x, y, u=1.0):
    _trio(x, y, u, "sweet", (0, 0), "mirror", pb.POSE_MIRROR)
    subtitle(x, y, u, ["\"Call me Pam... Mum.\""], 300)


def gag_m3(x, y, u=1.0):
    _trio(x, y, u, "unimpressed", (0.9, 0.3), "frozen", pb.POSE_MIRROR, tilt=0.0)
    subtitle(x, y, u, ["\"No.\""], 300)


GAGS = ((gag_lower, "2-3 · DON SAYS NO", "The paddle comes down. Her eyes are on him."),
        (gag_kind, "3 · THE MACHO", "Right after the pen is handed back: one word."),
        (gag_ask, "5 · THE QUESTION", "One eyebrow, a lean. She knows what she asks."),
        (gag_m1, "9 · MOM SMILES", "Still the act. Don has not moved."),
        (gag_m2, "9 · PAM COPIES", "The same smile, a size smaller."),
        (gag_m3, "9 · \"NO.\"", "The act drops. Pam's smile stays a beat too long."))


def main(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "PAM", 68, 44, 28, bold=True)
    corp(c, "\"The Best Candidate\"  ·  the lead  ·  knows Don is wrong, likes him anyway", 146, 44, 13, col=GREY)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · v2"
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    y0 = 92
    c.set_source_rgb(*ACCENT); c.rectangle(24, y0, 240, 400); c.fill()
    pb.pam(k, 144, y0 + 376, 1.1, "stand", "neutral")
    corp(c, "FRONT · lipstick and a brooch for the panel", 32, y0 + 392, 9, col=brand.NAVY, bold=True)

    corp(c, "SECRET SANTA, THEN THE PANEL", 280, y0 - 6, 10, bold=True)
    boxed(c, 280, y0, 300, 230)
    ps.pam(k, 346, y0 + 218, 0.62, "stand", "neutral", glasses="low")
    pb.pam(k, 452, y0 + 218, 0.62, "stand", "neutral")
    for i, n in enumerate(("fresh lipstick,", "a shade bolder", "", "a lilac flower", "brooch", "", "glasses on,", "low on her nose")):
        corp(c, n, 506, y0 + 50 + i * 14.5, 9.2, col=INK)

    corp(c, "THE MIRROR: WHAT SHE SHARES WITH MOM", 596, y0 - 6, 10, bold=True)
    boxed(c, 596, y0, 580, 230)
    c.save(); c.rectangle(596, y0, 380, 230); c.clip()
    mb.mom(k, 690, y0 + 116 - mb.HY * 1.0, 1.0, "stand", "sweet", seed=70, bag=False)
    pb.pam(k, 880, y0 + 122 - pb.HY * 1.0, 1.0, "stand", "mirror", lean=-4)
    c.restore()
    for i, (kind, n) in enumerate([("h", "ALREADY TRUE"), ("t", "Glasses on a bead chain."), ("t", "Hair set, a neat fringe."),
                                   ("g", ""), ("h", "ADDED HERE"), ("t", "A flower brooch, on the"), ("t", "opposite side to Mom's."),
                                   ("t", "The same shut-eyed smile,"), ("t", "copied in beat 9."),
                                   ("g", ""), ("h", "THE JOKE"), ("t", "Mom looks at a smaller,"), ("t", "younger her. \"No.\"")]):
        corp(c, n, 990, y0 + 22 + i * 15.2, 9 if kind == "h" else 9.4, col=brand.NAVY if kind == "h" else INK, bold=kind == "h")

    y1 = y0 + 254
    corp(c, "FACES", 280, y1 - 6, 10, bold=True)
    faces = [("peer", (-1, 0), "cool: the macho", False), ("dip", (0, 0), "Don says no (new)", False),
             ("probe", (0, 0), "the question (new)", False), ("mirror", (0, 0), "Mom's smile, copied", True),
             ("frozen", (0, 0), "after \"No.\" (new)", False)]
    for i, (f, lk, lab, warm) in enumerate(faces):
        x = 280 + i * 124
        box(x, y1, 118, 146, lambda x=x, f=f, lk=lk: pb.pam(k, x + 59, y1 + 64 - pb.HY * 0.82, 0.82, "stand", f, look=lk), lab,
            warm)
    box(900, y1, 276, 146, lambda: pb.pam(k, 1000, y1 + 252, 0.74, pb.POSE_YES, "hopeful", paddle="YES"),
        "2-3: YES, both times")

    y2 = 536
    corp(c, "HER SIX FRAMES  (9:16, sound off; the last three are one beat)", 24, y2 - 6, 10, bold=True)
    for i, (g, lab, cap) in enumerate(GAGS):
        x = 24 + i * 193.6
        c.save(); c.rectangle(x, y2, 184, 327); c.clip(); g(x, y2, 184 / 180.0); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.rectangle(x, y2, 184, 327); c.stroke()
        c.set_source_rgb(*brand.NAVY); c.rectangle(x, y2, 184, 18); c.fill()
        corp(c, lab, x + 7, y2 + 13, 9.2, col=(1, 1, 1), bold=True)
        corp(c, cap, x, y2 + 343, 7.9, col=INK)
    boxed(c, 24, y2 + 360, W2 - 48, 54)
    corp(c, "FOR THE ANIMATION", 36, y2 + 378, 9, col=brand.NAVY, bold=True)
    corp(c, "A blink before the paddle dips. The smile at KIND grows after she glances over. An eyebrow and a lean on the "
            "question. With Mom her shoulders come up: she is a girl again.", 36, y2 + 398, 9.4, col=INK)
    flush(c)
    surf.write_to_png(out)


def phone(out):
    global k
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2160, 640)
    c = cairo.Context(surf)
    k = Ctx(c, 0)
    for i, (g, _, _) in enumerate(GAGS):
        c.save(); c.rectangle(360 * i, 0, 360, 640); c.clip()
        g(360 * i, 0, 2.0)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(360 * i, 0, 360, 640); c.stroke()
    surf.write_to_png(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pam_bc_sheet_v2.png")
    phone(sys.argv[2] if len(sys.argv) > 2 else "pam_bc_phone_v2.png")
