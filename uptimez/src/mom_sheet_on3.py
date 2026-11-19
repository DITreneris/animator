"""v2 (mom_sheet_on3_v1.py = v1, kept), after the outside review and Tomas (19 Nov): the quieter fur, cuffs and
"Approved.", her car as a 1940s limousine (car_on3), and the three phone frames recomposed so that the thing each
shot is about leads it.
Model sheet and phone check for Mom as the queen of the dark city in Office Noir 3: The Last Round (mom_on3 v2).
Sheet: the queen beside the Mom of episode 10 (what changed), five poses with her things, five faces close, low behind
the wheel, the look as the dream shows it, her size beside the Client, the rules.
Phone: three 540x960 frames in the dream's look (the car, the folder at the window, "Approved."), shown at 270 px.
Usage: python3 mom_sheet_on3.py [out_dir]  ->  uptimez-mom-on3-v2-sheet.png, uptimez-mom-on3-v2-phone.png"""
import sys
import math
import cairo
import kit
import engine_on as eo
import mom_on3 as q
import mom_fs as mf
import car_on3 as car
import client_on3 as b
import sofia_sheet_on3 as ssh
import client_sheet_on3 as csh
from kit import Ctx, INK, cut

PAPER = (0.95, 0.93, 0.88)
WALL = kit.WALL
HY = q.HY
label = ssh.label
noir = csh.noir


def folder(k, x, y, s=1.0, ang=0.0):
    c = k.c
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    cut(k, [(-30, -40), (30, -40), (30, 40), (-30, 40)], (0.80, 0.74, 0.60), lw=2.2)
    cut(k, [(-30, -40), (-6, -40), (-2, -48), (-26, -48)], (0.80, 0.74, 0.60), shadow=False, lw=2)
    c.restore()


def car_front(c, w, h, y0):
    """The long black car, head on, before the noir pass: the bonnet, two headlights and their glare, the windscreen
    lit from the dashboard. y0: the bottom of the windscreen."""
    c.set_source_rgb(0.08, 0.08, 0.10); c.rectangle(0, 0, w, h); c.fill()
    c.set_source_rgb(0.05, 0.05, 0.06)
    c.move_to(w * 0.10, y0 - h * 0.26); c.line_to(w * 0.90, y0 - h * 0.26); c.line_to(w * 0.98, y0); c.line_to(w * 0.02, y0)
    c.close_path(); c.fill()                                             # the roof and pillars
    g = cairo.LinearGradient(0, y0 - h * 0.24, 0, y0)
    g.add_color_stop_rgba(0, 0.30, 0.30, 0.33, 1); g.add_color_stop_rgba(1, 0.62, 0.62, 0.66, 1)
    c.move_to(w * 0.16, y0 - h * 0.24); c.line_to(w * 0.84, y0 - h * 0.24); c.line_to(w * 0.92, y0); c.line_to(w * 0.08, y0)
    c.close_path(); c.set_source(g); c.fill()                            # the glass, lit from below
    c.set_source_rgb(0.12, 0.12, 0.14); c.rectangle(0, y0, w, h * 0.16); c.fill()      # the bonnet
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(0, y0 + h * 0.16, w, h); c.fill()  # the grille and below
    c.set_source_rgb(0.34, 0.34, 0.38); c.set_line_width(3)
    for i in range(9):
        xx = w * 0.30 + i * w * 0.05
        c.move_to(xx, y0 + h * 0.18); c.line_to(xx, y0 + h * 0.30); c.stroke()
    for sx in (0.15, 0.85):
        gx, gy = w * sx, y0 + h * 0.24
        gl = cairo.RadialGradient(gx, gy, 6, gx, gy, w * 0.34)
        gl.add_color_stop_rgba(0, 1, 1, 1, 1); gl.add_color_stop_rgba(0.18, 1, 1, 1, 0.85); gl.add_color_stop_rgba(1, 1, 1, 1, 0)
        c.set_source(gl); c.arc(gx, gy, w * 0.34, 0, 2 * math.pi); c.fill()


def dream_panel(w, h):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s); k = Ctx(c, 0)
    half = w // 2
    c.save(); c.rectangle(0, 0, half, h); c.clip()                       # her car, head on
    c.set_source_rgb(0.20, 0.20, 0.23); c.paint()
    sc = 0.62
    car.limo_front(k, half * 0.5, 176, sc, inside=lambda: q.queen(k, half * 0.5, 100 - HY * 0.86, 0.86, "q_wheel", "stern",
                                                                 (0.2, -0.9), wheel_=True, chain=False))
    c.restore()
    c.save(); c.translate(half, 0); c.rectangle(0, 0, w - half, h); c.clip()   # her table at the arena door
    ssh.ring(c, w - half, h, h - 26, lamp_x=(w - half) * 0.5)
    fy, sc = h - 22, 0.74
    q.queen(k, (w - half) * 0.56, fy, sc, "q_rake", "bored", (-0.5, 0.6), rake_=True)
    ty = fy + (q.WAIST + 52) * sc
    c.set_source_rgb(0.78, 0.78, 0.80); c.rectangle((w - half) * 0.56 - 150, ty, 250, 12); c.fill()
    c.set_source_rgb(0.16, 0.16, 0.19); c.rectangle((w - half) * 0.56 - 140, ty + 12, 230, h); c.fill()
    q.cash_box(k, (w - half) * 0.56 + 44, ty, 0.62)
    c.restore()
    noir(s)
    c.set_source_rgb(0.02, 0.02, 0.02); c.rectangle(half - 3, 0, 6, h); c.fill()
    return s


def sheet(out):
    W, H = 2200, 1700
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s); c.set_source_rgb(*PAPER); c.paint()
    k = Ctx(c, 0)
    c.select_font_face("Inter", 0, 1); c.set_font_size(40); c.set_source_rgb(*INK)
    c.move_to(50, 70); c.show_text("MOM · Office Noir 3: The Last Round · v2 · the queen of the dark city")
    c.select_font_face("Inter", 0, 0); c.set_font_size(22)
    c.move_to(50, 106); c.show_text("A black coat, a silver fur collar and cuffs, the order pinned on the fur · a small black hat, the one curler under it · rings on every finger")
    c.move_to(50, 136); c.show_text("Her things: a long cigarette holder, tarot cards (symbols only), a croupier's rake for the money, champagne · her face is BORED; her eyes come up twice")
    S, F = 1.22, 740
    mf.mom(k, 150, F, S, "fists", "glare", (0.3, 0), chin=True); label(c, "ep 10 (First Search)", 150, F + 42, 22)
    q.queen(k, 430, F, S, "q_stand", "bored", (0, 0)); label(c, "the queen (Office Noir 3)", 430, F + 42, 22)
    c.set_source_rgb(*INK); c.set_line_width(2); c.move_to(600, 170); c.line_to(600, F + 50); c.stroke()
    row = ((770, "q_holder", "bored", (0.5, 0), dict(holder_=True), "q_holder"),
           (1070, "q_cards", "bored", (0, 0.6), dict(cards=True), "q_cards: his gear on top"),
           (1440, "q_rake", "bored", (-0.6, 0.6), dict(rake_=True), "q_rake: she rakes it in"),
           (1730, "q_read", "bored", (-1.0, 0.2), dict(note=True), "q_read: \"Approved.\""),
           (2020, "q_toast", "stern", (0.3, -0.6), dict(coupe_=True), "q_toast"))
    for x, p, f, lk, kw, t in row:
        q.queen(k, x, F, S, p, f, lk, **kw); label(c, t, x, F + 42, 22)
    faces = (("bored", (0, 0), None, "bored"), ("bored", (-0.9, 0.4), None, "bored · counting"), ("stern", (0.2, -0.9), None, "stern: \"skunk\""),
             ("glare", (0.3, 0), None, "glare: understood"), ("bored", (-0.9, 0.3), "dry", "\"Approved.\""))
    for i, (f, lk, m, t) in enumerate(faces):
        x = 150 + 270 * i; y0 = 880
        c.save(); c.rectangle(x - 125, y0, 250, 380); c.clip(); c.set_source_rgb(*WALL); c.paint()
        q.queen(k, x, y0 + 215 - HY * 1.9, 1.9, "q_stand", f, lk, mouth=m)
        c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(x - 125, y0, 250, 380); c.stroke()
        label(c, t, x, y0 + 415, 22)
    c.save(); c.rectangle(1390, 880, 750, 380); c.clip(); c.set_source_rgb(0.30, 0.30, 0.33); c.paint()   # behind the wheel
    g = cairo.LinearGradient(0, 880, 0, 1260); g.add_color_stop_rgba(0, 0.34, 0.34, 0.38, 1); g.add_color_stop_rgba(1, 0.70, 0.70, 0.74, 1)
    c.set_source(g); c.paint()
    q.queen(k, 1585, 1060 - HY * 1.5, 1.5, "q_wheel", "stern", (0.2, -0.9), wheel_=True)
    q.queen(k, 1950, 1060 - HY * 1.5, 1.5, "q_wheel", "glare", (0.3, 0), wheel_=True)
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(1390, 880, 750, 380); c.stroke()
    label(c, "low behind the wheel: \"skunk\" (2.2) and the glove (2.3)", 1765, 1295, 22)
    dp = dream_panel(760, 340)
    c.set_source_surface(dp, 60, 1330); c.paint()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(60, 1330, 760, 340); c.stroke()
    c.save(); c.rectangle(850, 1330, 330, 340); c.clip(); c.set_source_rgb(*WALL); c.paint()        # beside the Client
    c.set_source_rgb(0.78, 0.74, 0.68); c.rectangle(850, 1640, 330, 30); c.fill()
    q.queen(k, 930, 1644, 0.72, "q_holder", "bored", (0.6, 0), holder_=True)
    b.boxer(k, 1085, 1644, 0.72 * b.REL, "b_walk", "hard", (-0.6, 0.3), outfit="street")
    c.restore(); c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(850, 1330, 330, 340); c.stroke()
    c.select_font_face("Inter", 0, 0); c.set_font_size(21); c.set_source_rgb(*INK)
    notes = ["Rules for this look",
             "· She is black, white and grey: nothing on her is red. The fur frames her face against the black.",
             "· BORED is her face. Her eyes come up twice only: STERN for \"skunk\", GLARE for the glove.",
             "· She never looks at the fight. \"Approved.\" is said to the money, mid-count.",
             "· Rings on every finger: her bare, ringed hands against his gloves, each time money moves.",
             "· The rake takes his hundred off his gloves (4.4): she never touches him.",
             "· Tarot: symbols only, never words. The top card is the Client's gear.",
             "· One prop per shot: the holder in the car, the rake at her table, the coupe at ringside.",
             "· \"Approved.\": eyes to the money, the mouth opens a crack, the face is still again.",
             "· Her car: a black 1940s limousine, a winged chrome curler on the grille. No make, no plate.",
             "· The one curler stays, under the hat: she is still Mom. She does not shout in this film."]
    for i, t in enumerate(notes):
        c.select_font_face("Inter", 0, 1 if i == 0 else 0)
        c.move_to(1215, 1362 + 32 * i); c.show_text(t)
    s.write_to_png(out)


def phone(out):
    frames = []
    for name, txt in (("wide", "2.2: the car, and her behind the wheel"), ("medium", "2.4: the folder, out of the window"),
                      ("close", "5.4: \"Approved.\", to the money")):
        f = cairo.ImageSurface(cairo.FORMAT_RGB24, 540, 960); c = cairo.Context(f); k = Ctx(c, 0)
        if name == "wide":
            csh.street(c, 540, 960, 900, 270, 300)
            car.limo_front(k, 270, 470, 1.12, inside=lambda: q.queen(k, 270, 352 - HY * 1.55, 1.55, "q_wheel", "stern",
                                                                    (0.2, -0.9), wheel_=True, chain=False))
        elif name == "medium":
            sill = car.limo_side(k, 190, 560, 1.0, inside=lambda: q.queen(k, 352, 392 - HY * 1.62, 1.62, "q_stand", "bored", (-0.2, 0.3)))
            sx, sy = sill
            hx, hy = 128, 684                                             # her arm, out over the sill, the folder tipped down to him
            ang = math.atan2(hy - sy, hx - sx)
            nx, ny = -math.sin(ang) * 20, math.cos(ang) * 20
            cut(k, [(sx + 40 + nx, sy - 14 + ny), (hx + nx, hy + ny), (hx - nx, hy - ny), (sx + 40 - nx, sy - 14 - ny)], q.SLEEVE, lw=2.4)
            folder(k, hx - 30, hy + 56, 1.55, -0.62)
            c.save(); c.translate(hx, hy); c.scale(1.8, 1.8); q._hand(k, 0, 0, 160); c.restore()
        else:
            ssh.ring(c, 540, 960, 1500, lamp_x=300, lamp_y=380)
            q.queen(k, 334, 430 - HY * 2.9, 2.9, "q_read", "bored", (-1.0, 0.2), note=True, mouth="dry")
        noir(f)
        frames.append((name, txt, f))
    W = 3 * 270 + 4 * 20
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, 480 + 80); c = cairo.Context(s); c.set_source_rgb(0.15, 0.15, 0.16); c.paint()
    for i, (name, txt, f) in enumerate(frames):
        c.save(); c.translate(20 + i * 290, 20); c.scale(0.5, 0.5); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.set_source_rgb(1, 1, 1)
        c.move_to(20 + i * 290, 522); c.show_text(name.upper() + " · at 270 px")
        c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.move_to(20 + i * 290, 542); c.show_text(txt)
    s.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../characters"
    sheet(d + "/uptimez-mom-on3-v2-sheet.png")
    phone(d + "/uptimez-mom-on3-v2-phone.png")
