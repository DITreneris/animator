"""v2, pinned: builds on2_cast_v2.png from noir2_cast_v2. on2_cast_sheet.py is current.
OFFICE NOIR 2: the cast sheet, v2 (noir2_cast.py v2). Script v2, 17 Nov. on2_cast_sheet_v1.py = v1, pinned.
v2 is what changed with concept v4: Sofia in the gown (front, back, running, behind the money), Detective Don, Pam with
the broom, the robot at the door, the taxi, the hands, the one drawing on the napkin and the roll, and Sofia awake in
the party dress. The Shadow, Mom and the Bartender are on sheet v1 and are unchanged.
Writes ../office-noir-2/on2_cast_v2.png (2400 x 3280, drawn at 1200 x 1640) and on2_cast_phone_v2.png (the same sheet
540 wide: what survives on a phone). Dream panels are shown as rendered: through engine_on's noir pass, grey with
the one key red. Party panels are in colour.
  python3 on2_cast_sheet.py [folder]"""
import sys
import math
import cairo
import kit
import brand
import engine_on as eng
import client_ob as co
import acts_ob as ac
import noir2_cast_v2 as n
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v2"
W2, H2 = 1200, 1640
GREY = (0.35, 0.40, 0.50)
BG = (0.97, 0.96, 0.93)
NIGHT = (0.30, 0.30, 0.32)          # a dark wall: what the dream stands in
WALL = (0.80, 0.79, 0.76)           # a lit wall: what a shadow falls on
PARTY = (0.93, 0.90, 0.82)


def boxed(c, x, y, w, h, label=None):
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()
    if label:
        corp(c, label, x, y + h + 15, 10.5, bold=True)


def noir(c, x, y, w, h, draw, label=None, bg=NIGHT, scale=2):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w * scale), int(h * scale))
    cc = cairo.Context(sf); cc.scale(scale, scale)
    cc.set_source_rgb(*bg); cc.paint()
    draw(Ctx(cc, 0))
    eng.accent_pass(sf, n.ACCENTS2)
    c.save(); c.translate(x, y); c.scale(1.0 / scale, 1.0 / scale); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()
    boxed(c, x, y, w, h, label)


def colour(c, x, y, w, h, draw, label=None, bg=PARTY):
    c.save(); c.rectangle(x, y, w, h); c.clip(); c.translate(x, y)
    c.set_source_rgb(*bg); c.paint()
    draw(Ctx(c, 0)); c.restore()
    boxed(c, x, y, w, h, label)


def lamp_pool(k, w, h):
    """A desk lamp's light on a wall, for the shadow panels."""
    c = k.c
    g = cairo.RadialGradient(w * 0.5, h * 0.42, 10, w * 0.5, h * 0.42, max(w, h) * 0.75)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.55); g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    c.set_source(g); c.paint()


def notes(c, x, y, w, title, lines):
    corp(c, title, x, y, 12, bold=True)
    yy = y + 20
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(10.6)
    for ln in lines:
        line, rows = "", 0                                  # charsheets.wrap does not say where it ended: count the rows
        for wd in ("·  " + ln).split():
            trial = (line + " " + wd).strip()
            if c.text_extents(trial).x_advance > w and line:
                rows += 1; line = wd
            else:
                line = trial
        wrap(c, "·  " + ln, x, yy, 10.6, w)
        yy += (rows + 1) * 10.6 * 1.35 + 6
    return yy


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "OFFICE NOIR 2", 68, 44, 28, bold=True)
    corp(c, "The Shadow of Fate  ·  what is new in Sofía's dream", 318, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()
    STREET = (0.22, 0.22, 0.24)

    # ------------------------------------------------ Sofia, in the dream
    noir(c, 24, 84, 300, 540, lambda k: n.star(k, 150, 522, 1.42, "g_stand", "interested", (-0.9, 0.0)),
         "SOFÍA · the dream: gown, gloves, wrap, clutch")
    colour(c, 336, 84, 200, 262, lambda k: n.star(k, 100, 256, 0.70, "g_pose", "interested", (0.5, -0.2)),
           "before the pass (key colours)", bg=(0.82, 0.80, 0.77))

    def back(k):
        cc = k.c
        cc.set_source_rgb(0.46, 0.46, 0.48); cc.rectangle(0, 200, 200, 62); cc.fill()                 # the wet stones, lit
        cc.set_source_rgb(*n.BLACK)                                                                 # his shadow, sliding after her
        cc.new_path(); cc.move_to(-6, 262); cc.line_to(40, 226); cc.line_to(66, 226); cc.line_to(52, 262); cc.close_path(); cc.fill()
        cc.save(); cc.translate(54, 224); cc.scale(30, 5.5); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
        cc.new_path(); cc.move_to(40, 224); cc.line_to(44, 208); cc.line_to(52, 212); cc.line_to(58, 207); cc.line_to(66, 210); cc.line_to(70, 224); cc.close_path(); cc.fill()
        n.star_back(k, 132, 250, 0.66, step=0.2)
    noir(c, 548, 84, 200, 262, back, "2.1  from behind, his shadow after her", bg=STREET)

    def mirror(k):
        o = n.star(k, 84, 560, 1.45, "g_stand", "smile", (0.9, -0.1), wrap=False, bag=False)
        n.compact2(k, 162, 150, 1.7, 0.10, hat=True)
        kit.ellipse(k, 160, 208, 16, 16, n.KEY, 363, shadow=False, lw=2.4)
    noir(c, 760, 84, 200, 262, mirror, "2.2  the hat in her mirror. She smiles")

    def run(k):
        cc = k.c
        cc.set_source_rgb(0.12, 0.12, 0.13); cc.rectangle(0, 206, 200, 46); cc.fill()
        n.powder_puff(k, 40, 226, 0.9)
        n.footprints(k, 60, 238, 0.8, n=3, step=22)
        n.wrap_flying(k, 46, 92, 0.62, 0.45)
        n.star(k, 132, 236, 0.66, "g_run", "caught", (-0.9, 0.0), lean=8, lag=(-14, -4), wrap=False)
    noir(c, 336, 372, 200, 252, run, "2.6  she runs. The powder, the wrap", bg=STREET)
    noir(c, 548, 372, 200, 252, lambda k: n.star(k, 100, 540, 1.40, "g_fan", "caught", (-1.0, 0.0), wrap=False),
         "5.2  behind a stranger's money")

    def count(k):
        k.c.set_source_rgb(0.20, 0.17, 0.14); k.c.rectangle(0, 216, 200, 40); k.c.fill()             # the bar
        o = n.star(k, 72, 372, 0.98, "g_count", "appraise", (0.5, 0.9), wrap=False)
        hx, hy = o["hands"][1]
        n.napkin2(k, hx + 16, hy - 34, 0.60, ang=-0.06)
        n._glove_finger(k, hx - 1, hy - 5, 0.98, -0.5, 300 + 332)
    noir(c, 760, 372, 200, 252, count, "5.5  her finger stops on the L")
    notes(c, 978, 96, 198, "SOFÍA, v2", [
        "Her face, her hair and her proportions are her own. Only the costume is new.",
        "A strapless red gown to the floor, with a slit. Long red gloves to above the elbow. Red shoes.",
        "No pearls in the dream. Diamond drops: a stud and one long stone, with a glint.",
        "A black wrap, worn low on her arms. It is gone after 2.6, and Don carries it from then on.",
        "A short silver tube for a bag: the first of the three rolls, and what his hand goes for.",
        "Red is the gown, the gloves, the shoes, her lips and what she writes. Nothing else in the dream has colour.",
        "From behind she is hair, bare shoulders, the wrap and the gown; the diamonds only glint.",
    ])

    # ------------------------------------------------ Don, Pam, the robot
    y0 = 660

    def don_full(k):
        k.c.set_source_rgb(0.12, 0.12, 0.13); k.c.rectangle(0, 404, 250, 48); k.c.fill()
        n.footprints(k, 150, 430, 1.0, n=4, step=24)
        n.detective(k, 104, 438, 1.02, "look", "squint", (0.8, 0.7), wrap=True)
    noir(c, 24, y0, 250, 452, don_full, "DETECTIVE DON · the glass, and her wrap", bg=STREET)

    def eye(k):
        n.glass_view(k, 100, 104, 84, "eye")
    noir(c, 286, y0, 200, 216, eye, "5.9  his eye, on her", bg=(0.10, 0.10, 0.11))

    def stamp(k):
        n.detective(k, 100, 364, 0.95, "stamp", "almost", (0.0, 0.6), napkin_in_band=True)
    noir(c, 286, y0 + 240, 200, 212, stamp, "5.10  closed, on one side of the napkin")

    def pam_full(k):
        k.c.set_source_rgb(0.12, 0.12, 0.13); k.c.rectangle(0, 404, 250, 48); k.c.fill()
        n.footprints(k, 14, 432, 1.0, n=2, step=24)
        n.sweeper(k, 150, 438, 1.20, "lean", "neutral", (-0.9, 0.2))
        n.dustpan(k, 40, 418, 0.9, full=False)
    noir(c, 498, y0, 250, 452, pam_full, "PAM · the cap, the broom", bg=STREET)

    def prints(k):
        n.glass_view(k, 100, 104, 84, "prints")
    noir(c, 760, y0, 200, 216, prints, "3.3  the prints stop at a broom", bg=(0.10, 0.10, 0.11))

    def swept(k):
        k.c.set_source_rgb(0.12, 0.12, 0.13); k.c.rectangle(0, 170, 200, 42); k.c.fill()
        n.sweeper(k, 112, 262, 0.78, "sweep", "neutral", (-0.9, -0.1))
        n.dustpan(k, 36, 196, 0.8, full=True)
    noir(c, 760, y0 + 240, 200, 212, swept, "3.2  one sweep, and she looks at him", bg=STREET)

    def robot(k):
        k.c.set_source_rgb(0.12, 0.12, 0.13); k.c.rectangle(0, 404, 204, 48); k.c.fill()
        k.c.set_source_rgb(0.62, 0.61, 0.56); k.c.rectangle(4, 130, 104, 274); k.c.fill()               # the bar door, lit, behind it
        n.beggar(k, 54, 428, 0.60, "eager", (0.6, 0.0), reach=True)
        n.coin_tag(k, 138, 34, 1.25, 0.0)                                                            # the tag, to read
    noir(c, 972, y0, 204, 452, robot, "THE ROBOT · the coin comes back", bg=STREET)

    # ------------------------------------------------ awake, the taxi, the hands, the drawing
    y1 = 1150

    def awake(k):
        kit.rect(k, 176, 326, 100, 10, (0.70, 0.56, 0.40), 5, lw=1.8)                                 # the table she slept on
        kit.rect(k, 236, 336, 10, 104, (0.56, 0.44, 0.30), 6, shadow=False, lw=1.6)
        n.doughnut(k, 220, 316, 0.9)
        n.party(k, 112, 428, 1.10, "g_blower", "caught", (0.7, 0.0))
    colour(c, 24, y1, 260, 440, awake, "AWAKE · a plain red dress, her pearls, sugar")
    noir(c, 296, y1, 200, 210, lambda k: n.star(k, 100, 520, 1.45, "g_hide", "caught", (0.7, -0.7), wrap=False),
         "7.1  under the desk", bg=(0.16, 0.16, 0.18))
    noir(c, 296, y1 + 238, 200, 202, lambda k: n.star(k, 104, 400, 1.05, "g_beckon", "interested", (-1.0, 0.0), wrap=False),
         "6.5  she beckons")

    def cab(k):
        cc = k.c
        cc.set_source_rgb(0.12, 0.12, 0.13); cc.rectangle(0, 170, 330, 40); cc.fill()
        g = cairo.RadialGradient(70, 20, 4, 70, 20, 170)                                             # the street lamp
        g.add_color_stop_rgba(0, 1, 1, 1, 0.55); g.add_color_stop_rgba(1, 1, 1, 1, 0.0); cc.set_source(g); cc.paint()
        n.taxi(k, 176, 178, 0.82, door=1.0)
        cc.save(); cc.translate(246, 176); cc.scale(0.9, 0.9)                                        # a red heel on the stones
        kit.cut(k, [(-7, -34), (5, -34), (4, -12), (-5, -12)], n.so.SKIN, shadow=False, lw=1.8)
        kit.cut(k, [(-8, -14), (6, -14), (18, 0), (4, 0), (-2, -6), (-4, 0), (-8, 0)], n.KEY, shadow=False, lw=1.8)
        kit.cut(k, [(-16, -60), (14, -60), (10, -30), (-10, -30)], n.KEY, shadow=False, lw=2)          # the hem
        cc.restore()
    noir(c, 508, y1, 330, 210, cab, "1.1  the taxi, the lamp, a red heel", bg=STREET)

    def hands(k):
        n.rich_hand(k, 118, 74, 1.15, 0.10, "money")
        n.rich_hand(k, 104, 168, 1.15, -0.06, "coupe")
        n.rich_hand(k, 222, 60, 1.15, 0.06, "coupe", flip=-1)
        n.rich_hand(k, 232, 150, 1.15, -0.08, "money", flip=-1)
    noir(c, 508, y1 + 238, 330, 202, hands, "5.1  hands out of the dark, from both sides", bg=(0.34, 0.34, 0.36))

    def drawing(k):
        n.napkin2(k, 62, 62, 0.82)
        n.napkin2(k, 62, 150, 0.82, back=True, ang=0.05)
        n.plan_open2(k, 232, 106, 1.25, -0.03)
    noir(c, 850, y1, 326, 210, drawing, "one drawing, twice: his note, and the roll", bg=(0.20, 0.18, 0.16))
    notes(c, 852, 1400, 322, "THE OTHERS", [
        "Detective Don is his first Office Noir look, with a glass. He collects what she drops: the wrap, then the number.",
        "Pam is her Office Noir self with a sweeper's cap. The broom is the only thing she needs.",
        "The robot has no cap and no costume: a tin cup, a card with an empty battery, and an arm that comes out too fast.",
        "The rich men are sleeves, cuffs and hands. They have no faces.",
        "The Shadow, Mom and the Bartender are as on sheet v1.",
    ])

    c.set_source_rgb(*GREY); c.select_font_face("Inter", 0, 0); c.set_font_size(9.5)
    c.move_to(24, H2 - 14); c.show_text("Office Noir 2 · cast sheet " + V + " · from script v2 · for review: nothing is storyboarded or animated from this yet")
    surf.write_to_png(out)
    return surf


def phone(surf, out):
    w = 540; h = int(H2 * w / float(W2))
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    cc = cairo.Context(sf); cc.scale(w / float(W2 * 2), w / float(W2 * 2)); cc.set_source_surface(surf, 0, 0)
    cc.get_source().set_filter(cairo.FILTER_BEST); cc.paint()
    sf.write_to_png(out)


if __name__ == "__main__":
    d_ = sys.argv[1] if len(sys.argv) > 1 else "../office-noir-2"
    s_ = main("%s/on2_cast_%s.png" % (d_, V))
    phone(s_, "%s/on2_cast_phone_%s.png" % (d_, V))
    print("wrote", d_)
