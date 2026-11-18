"""v1, pinned: builds on2_cast_v1.png from noir2_cast_v1. on2_cast_sheet.py is current.
OFFICE NOIR 2: the cast sheet, v1 (noir2_cast.py). Script v1, 17 Nov.
Writes ../office-noir-2/on2_cast_v1.png (2400 x 3280, drawn at 1200 x 1640) and on2_cast_phone_v1.png (the same sheet
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
import noir2_cast_v1 as n
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v1"
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
    eng.accent_pass(sf, n.ACCENTS)
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
    corp(c, "The Shadow of Fate  ·  the cast of Sofía's dream", 318, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # ------------------------------------------------ Sofia
    noir(c, 24, 84, 300, 540, lambda k: n.sofia(k, 150, 522, 1.42, "n_walk", "interested", (-0.9, 0.0)),
         "SOFÍA · the dream: trench, pearls, the rolled umbrella")
    colour(c, 336, 84, 200, 262, lambda k: n.sofia(k, 100, 256, 0.70, "n_walk", "interested", (-0.9, 0.0)),
           "before the pass (key colours)", bg=(0.82, 0.80, 0.77))
    noir(c, 336, 372, 200, 252, lambda k: n.sofia(k, 100, 560, 1.45, "n_lips", "interested", (-0.9, 0.2)),
         "1.2  her lips, in the shop window")

    def tap(k):
        k.c.set_source_rgb(0.20, 0.17, 0.14); k.c.rectangle(0, 226, 200, 40); k.c.fill()             # the bar
        o = n.sofia(k, 72, 372, 0.98, "n_tap", "appraise", (0.5, 0.9))
        hx, hy = o["hands"][1]
        n.napkin(k, hx + 14, hy - 34, 0.56, ang=-0.06)                                                # held up to count
        n._nail_finger(k, hx - 1, hy - 5, 0.98, -0.5, 300 + 332)                                      # her nail, on the first box
    noir(c, 548, 84, 200, 262, tap, "2.3  one nail counts the boxes")
    noir(c, 760, 84, 200, 262, lambda k: n.sofia(k, 104, 420, 1.05, "n_beckon", "interested", (-1.0, 0.0)),
         "4.3  she beckons. Her eyes on him")
    noir(c, 548, 372, 200, 252, lambda k: n.sofia(k, 100, 540, 1.45, "n_hide", "caught", (0.7, -0.7)),
         "5.1  under the desk", bg=(0.16, 0.16, 0.18))

    def awake(k):
        o = n.sofia(k, 100, 404, 1.02, "n_blower", "caught", (0.7, 0.0), coat=False, blow=0.0)
        hx, hy = o["head"]
        n.paper_hat(k, hx - 24, hy - 54, 0.92, -0.42)
    colour(c, 760, 372, 200, 252, awake, "7.2  awake: what she is holding")
    notes(c, 978, 96, 198, "SOFÍA", [
        "Her face, her hair and her proportions are the ones she has in The Onboarding. Only the costume is new.",
        "A light belted trench coat, the collar up, sleeves pushed to the elbow so the bracelet and the nails stay in sight.",
        "The pearls stay: the short strand, the drops, the bracelet.",
        "Red: her lips, her nails, her lipstick and what she writes with it. Nothing else in the dream has colour.",
        "The umbrella is rolled and under her arm, in the rain. It is the first of three rolls.",
        "Her confidence never wavers until the keys: pleased, amused, in command. Under the desk her eyes do the acting.",
        "Awake she wears what she wears at work, and a paper hat over one eye.",
    ])

    # ------------------------------------------------ the Shadow, the Client, Mom's shadow
    y0 = 660
    noir(c, 24, y0, 300, 452, lambda k: (lamp_pool(k, 300, 452), n.shadow(k, 150, 436, 0.92, "open")),
         "THE SHADOW · the Client, without a face", bg=WALL)
    def reach(k):
        lamp_pool(k, 280, 200)
        k.c.set_source_rgb(0.10, 0.10, 0.11); k.c.rectangle(128, 178, 152, 22); k.c.fill()               # the desk's edge
        ac.roll(k, 226, 169, 0.50, math.pi / 2, ln=150)
        pose = co.POSES["open"][:2] + co._ik(1, 150, co.BT + 66)
        n.shadow(k, 70, 334, 0.62, pose, look_down=1.0)
    noir(c, 336, y0, 280, 200, reach, "his hand goes for the object, never for her", bg=WALL)

    def note_hand(k):
        cc = k.c
        cc.set_source_rgb(0.20, 0.17, 0.14); cc.rectangle(0, 150, 280, 82); cc.fill()                    # the bar
        n.napkin(k, 186, 156, 0.86, ang=0.05)
        pose = co.POSES["open"][:2] + co._ik(1, 168, co.BT + 118)
        n.shadow(k, -86, 420, 1.15, pose, lit_hand=1)
        n.coupe(k, 258, 132, 0.9)
    noir(c, 336, 892, 280, 220, note_hand, "2.2  the note: ten boxes and a question mark", bg=NIGHT)

    def client_awake(k):
        o = co.client(k, 112, 436, 0.92, "open", "puzzled", look=(0.6, 0.0), roll=False)
        n.paper_hat(k, 204, 384, 0.9, 2.2)                                                             # on its way to the floor
    colour(c, 628, y0, 250, 452, client_awake, "awake: who he was")
    noir(c, 890, y0, 286, 452, lambda k: (lamp_pool(k, 286, 452), n.mom_up(k, 204, 438, 1.0, True)),
         "MOM'S SHADOW · an arm, something long and dark", bg=WALL)

    # ------------------------------------------------ Mom awake, the Bartender, props
    y1 = 1150
    colour(c, 24, y1, 300, 440, lambda k: n.mom_up(k, 224, 428, 0.96, False),
           "MOM, awake · the same arm; it was a bottle")
    noir(c, 336, y1, 290, 440, lambda k: n.bartender(k, 132, 424, 0.92, brow=False),
         "THE BARTENDER · a white jacket, one glass")
    noir(c, 638, y1, 200, 210, lambda k: n.bartender(k, 96, 700, 1.75, brow=True),
         "his whole part: one eyebrow")

    def rolls(k):
        n.umbrella(k, 36, 112, 0.92, 0.0)
        ac.roll(k, 100, 108, 0.74, 0.0, ln=170)
        n.blower(k, 150, 70, 0.9, 0.0, ang=0.0)
        n.blower(k, 138, 150, 0.62, 1.0, ang=0.0)
    colour(c, 638, 1388, 200, 202, rolls, "three rolls: umbrella, plan, blower", bg=(0.82, 0.80, 0.77))

    def naps(k):
        n.napkin(k, 86, 100, 1.05)
        n.napkin(k, 242, 108, 1.05, back=True, ang=0.05)
    noir(c, 850, y1, 326, 210, naps, "the napkin: his question, her answer", bg=(0.20, 0.18, 0.16))
    notes(c, 852, 1400, 322, "THE OTHERS", [
        "The Shadow is the Client's own figure filled black, with a hat; awake, his paper hat is the hat that fell. Only the hat's rim, his collar, the gear pin, the watch and the reaching hand catch light. He has no eyes: the hat's tilt says what he is looking at.",
        "Mom's shadow and Mom with the bottle are drawn from one pose, so the cut from the bang can match exactly. Nothing in the shadow is a gun; it is only long and dark, along her arm.",
        "The Bartender never speaks. The dream has no Don, no Pam and no robot.",
    ])

    c.set_source_rgb(*GREY); c.select_font_face("Inter", 0, 0); c.set_font_size(9.5)
    c.move_to(24, H2 - 14); c.show_text("Office Noir 2 · cast sheet " + V + " · from script v1 · for review: nothing is storyboarded or animated from this yet")
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
