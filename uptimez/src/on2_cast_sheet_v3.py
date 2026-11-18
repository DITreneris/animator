"""v3, pinned: builds on2_cast_v3.png from noir2_cast_v3. on2_cast_sheet.py is current.
OFFICE NOIR 2: the cast sheet, v3 (noir2_cast.py with LOOK = 3). Script v2, 17 Nov, after the design audit and four
answers: the wrap stays black, with a pale edge, at her elbows; she runs in the long gown, the slit open; Pam gets a
pale sweeper's apron; the sheet carries six two-shots. on2_cast_sheet_v2.py and _v1.py are pinned.
Writes ../office-noir-2/on2_cast_v3.png (2400 x 3980, drawn at 1200 x 1990) and on2_cast_phone_v3.png (540 wide).
Dream panels go through engine_on's noir pass; the six key frames are drawn at film size (540 x 960) and shown at a third.
  python3 on2_cast_sheet.py [folder]"""
import sys
import math
import cairo
import kit
import brand
import engine_on as eng
import client_ob as co
import acts_ob as ac
import noir2_cast_v3 as n
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v3"
W2, H2 = 1200, 1990
n.LOOK[0] = 3
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


STREET = (0.22, 0.22, 0.24)
STONE = (0.40, 0.40, 0.43)


def keyframe(c, x, y, draw, label, tilt=0.0, w=180):
    """One film frame, 540 x 960, through the noir pass, shown w wide."""
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
    cc = cairo.Context(sf)
    cc.set_source_rgb(*STREET); cc.paint()
    if tilt:
        cc.translate(270, 480); cc.rotate(tilt); cc.scale(1.10, 1.10); cc.translate(-270, -480)
    draw(Ctx(cc, 0))
    eng.accent_pass(sf, n.ACCENTS2)
    g = w / 540.0
    c.save(); c.translate(x, y); c.scale(g, g); c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST)
    c.paint(); c.restore()
    boxed(c, x, y, w, w * 16 / 9.0, label)


def _pool(cc, x, y, r, a=0.5):
    g = cairo.RadialGradient(x, y, 6, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, a); g.add_color_stop_rgba(1, 1, 1, 1, 0.0); cc.set_source(g); cc.paint()


def _street(k, floor=640):
    cc = k.c
    cc.set_source_rgb(*STONE); cc.rectangle(-60, floor, 660, 1000 - floor); cc.fill()
    cc.set_source_rgb(0.30, 0.30, 0.33); cc.set_line_width(2)
    for i in range(1, 6):
        yy = floor + i * i * 9; cc.move_to(-60, yy); cc.line_to(600, yy); cc.stroke()
    _pool(cc, 300, 120, 520, 0.38)


def _arm_in(k, x0, y0, x1, y1, w=58):
    """The Shadow's arm from off screen to his lit hand at (x1, y1): a black sleeve, the watch, the hand."""
    cc = k.c
    n._seg(k, x0, y0, x1, y1, w, w * 0.78, n.BLACK)
    g = math.atan2(y1 - y0, x1 - x0)
    wx, wy = x1 - math.cos(g) * 30, y1 - math.sin(g) * 30
    kit.ellipse(k, x1, y1, 30, 27, co.SKIN, 403, shadow=False, lw=3.2)
    kit.ellipse(k, wx, wy - 16, 15, 15, (0.20, 0.20, 0.22), 404, shadow=False, lw=2.6)
    kit.ellipse(k, wx, wy - 16, 8, 8, (0.92, 0.92, 0.88), 405, shadow=False, lw=1.4)


def kf_hand(k):                                             # 2.4
    _street(k, 720)
    n.shadow(k, 20, 1180, 2.5, "open", lit_hand=None, look_down=1.0)
    o = n.star(k, 330, 1060, 2.6, "g_stand", "caught", (-1.0, 0.7))
    lx, ly = o["hands"][0]
    _arm_in(k, -40, 500, lx + 44, ly - 40)


def kf_pam(k):                                              # 3.2
    _street(k, 560)
    n.detective(k, 432, 640, 0.80, "look", "squint", (0.6, 0.8), wrap=True)
    n.footprints(k, 300, 900, 2.6, n=3, step=30)
    n.sweeper(k, 190, 930, 2.25, "sweep", "neutral", (1.0, -0.2))


def kf_robot(k):                                            # 4.1
    cc = k.c
    _street(k, 760)
    cc.set_source_rgb(0.70, 0.69, 0.64); cc.rectangle(300, 120, 300, 640); cc.fill()                # the bar door, lit
    cc.set_source_rgb(*INK); cc.set_line_width(5); cc.rectangle(300, 120, 300, 640); cc.stroke()
    n.star(k, 410, 1010, 2.25, "g_pose", "appraise", (-0.9, 0.6))
    n.coin_steps(k, 106, 800, 1.45, 3)


def kf_hide(k):                                             # 5.2
    cc = k.c
    cc.set_source_rgb(0.16, 0.16, 0.18); cc.paint()
    _pool(cc, 280, 60, 460, 0.30)
    n.rich_hand(k, 470, 372, 1.9, 0.0, "coupe", flip=-1)
    n.detective(k, 372, 800, 1.35, (-10, 4) + n.d.dm.ik(1, 58, n.d.BT + 6), "squint", (0.9, -0.2))
    n.star(k, 190, 1150, 2.7, "g_fan", "caught", (1.0, -0.1), wrap=False)
    n.rich_hand(k, 96, 820, 1.9, -0.25, "money")


def kf_caught(k):                                           # 5.9
    cc = k.c
    cc.set_source_rgb(0.16, 0.16, 0.18); cc.paint()
    _pool(cc, 400, 200, 420, 0.34)
    n.bartender(k, 492, 620, 0.95, brow=True, look=(-0.8, 0.3))
    cc.set_source_rgb(0.30, 0.26, 0.22); cc.rectangle(230, 560, 330, 420); cc.fill()                # the bar
    cc.set_source_rgb(0.62, 0.58, 0.52); cc.rectangle(230, 560, 330, 10); cc.fill()
    o = n.detective(k, 372, 760, 1.30, "up", "squint", (-0.9, 0.1), napkin_in_band=True)
    hx, hy = o["head"]
    n.glass_handle(k, hx - 26, hy + 8, 66, 0.5)
    n.glass_view(k, hx - 26, hy + 8, 66, "eye")
    n.star(k, 128, 1130, 2.5, "g_stand", "caught", (1.0, 0.0), wrap=False, bag=False)


def kf_trap(k):                                             # 6.6
    cc = k.c
    cc.set_source_rgb(0.20, 0.20, 0.22); cc.paint()
    cc.save(); cc.rotate(-0.10)                                                                   # light through the blinds
    for i in range(9):
        cc.set_source_rgba(1, 1, 1, 0.13); cc.rectangle(-80, 80 + i * 44, 520, 18); cc.fill()
    cc.restore()
    _pool(cc, 300, 600, 380, 0.42)
    n.shadow(k, -6, 1100, 2.3, "open", lit_hand=None, look_down=1.0)
    o = n.star(k, 400, 930, 2.3, "g_offer", "appraise", (-0.9, 0.8), wrap=False)
    cc.set_source_rgb(0.14, 0.13, 0.13); cc.rectangle(150, 730, 420, 260); cc.fill()                # Don's desk
    cc.set_source_rgb(0.48, 0.44, 0.40); cc.rectangle(150, 730, 420, 12); cc.fill()
    ac.roll(k, 196, 716, 1.15, math.pi / 2, ln=170)
    _arm_in(k, -40, 590, 96, 708, 54)


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(*BG); c.paint()
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "OFFICE NOIR 2", 68, 44, 28, bold=True)
    corp(c, "The Shadow of Fate  ·  the dream's cast, corrected, and six two-shots", 318, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · CHARACTER MODEL SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()

    # ------------------------------------------------ Sofia, in the dream
    noir(c, 24, 84, 300, 540, lambda k: n.star(k, 150, 522, 1.42, "g_stand", "interested", (-0.9, 0.0)),
         "SOFÍA · gloves red to above the elbow; the wrap behind", bg=STREET)
    colour(c, 336, 84, 200, 262, lambda k: n.star(k, 100, 256, 0.70, "g_pose", "interested", (0.5, -0.2)),
           "before the pass (key colours)", bg=(0.82, 0.80, 0.77))

    def back(k):
        cc = k.c
        cc.set_source_rgb(*STONE); cc.rectangle(0, 200, 200, 62); cc.fill()
        cc.set_source_rgb(*n.BLACK)                                                                 # his shadow, sliding after her
        cc.new_path(); cc.move_to(-6, 262); cc.line_to(40, 226); cc.line_to(66, 226); cc.line_to(52, 262); cc.close_path(); cc.fill()
        cc.save(); cc.translate(54, 224); cc.scale(30, 5.5); cc.arc(0, 0, 1, 0, 2 * math.pi); cc.restore(); cc.fill()
        cc.new_path(); cc.move_to(40, 224); cc.line_to(44, 208); cc.line_to(52, 212); cc.line_to(58, 207); cc.line_to(66, 210); cc.line_to(70, 224); cc.close_path(); cc.fill()
        n.star_back(k, 132, 250, 0.66, step=0.2)
    noir(c, 548, 84, 200, 262, back, "2.1  from behind", bg=STREET)

    def run(k):
        cc = k.c
        cc.set_source_rgb(*STONE); cc.rectangle(0, 204, 200, 48); cc.fill()
        n.powder_puff(k, 34, 224, 0.8)
        n.footprints(k, 52, 238, 0.7, n=2, step=22)
        n.wrap_flying(k, 46, 70, 0.60, 0.35)
        n.star(k, 136, 240, 0.64, "g_run3", "caught", (-0.9, 0.0), lean=7, lag=(-14, -4), wrap=False, run=True)
    noir(c, 760, 84, 200, 262, run, "2.6  the same gown, running", bg=STREET)
    noir(c, 336, 372, 200, 252, lambda k: n.star(k, 100, 540, 1.40, "g_fan", "caught", (1.0, -0.1), wrap=False),
         "5.2  hiding from Don, behind money")

    def count(k):
        k.c.set_source_rgb(0.20, 0.17, 0.14); k.c.rectangle(0, 0, 200, 252); k.c.fill()                # the bar, from above
        n.napkin2(k, 92, 112, 1.42, ang=-0.05)
        cc = k.c
        n._seg(k, 214, 262, 150, 176, 46, 40, n.KEY, 2.6)                                             # her glove, coming in
        kit.ellipse(k, 150, 176, 23, 21, n.KEY, 336, shadow=False, lw=2.6)
        n._glove_finger(k, 140, 164, 2.3, -0.62, 332)
    noir(c, 548, 372, 200, 252, count, "5.4  her finger stops on the odd bay")
    noir(c, 760, 372, 200, 252, lambda k: n.star(k, 86, 470, 1.25, "g_beckon3", "interested", (-1.0, 0.0), wrap=False),
         "6.5  she beckons: the finger first")
    notes(c, 978, 96, 198, "WHAT CHANGED IN v3", [
        "The gloves are red from above the elbow to the fingers, in every pose. Nothing black covers them.",
        "The wrap is still black. It hangs behind her from elbow to elbow, with a pale edge so it has an outline at night.",
        "She runs in the long gown: the slit opens, one leg and a red shoe come through, the hem streams behind.",
        "The odd bay is solid, on the napkin and on the roll, so it reads black on white and white on dark.",
        "Banknotes are grey-green with numerals; they no longer read as cards.",
        "Her face and hair are the same drawing as in The Onboarding; only what she wears is swapped.",
    ])

    # ------------------------------------------------ her faces
    yf = 660
    faces = [("interested", (-0.9, 0.0), "1.2  seen"), ("real", (0.8, -0.1), "2.3  an admirer"), ("caught", (-1.0, 0.6), "2.4  it is him"),
             ("appraise", (0.5, 0.9), "5.5  she can't answer"), ("recover", (0.0, -0.3), "6.3  chin up"), ("breath", (0, 0), "8.6  eyes shut")]
    for i, (f, lk, lab) in enumerate(faces):
        noir(c, 24 + i * 192, yf, 180, 160, lambda k, f=f, lk=lk: n.star(k, 90, 426, 1.22, "g_stand", f, lk, wrap=False, bag=False), lab)

    # ------------------------------------------------ Don, Pam, the robot
    y0 = 870

    def don_full(k):
        k.c.set_source_rgb(*STONE); k.c.rectangle(0, 404, 250, 48); k.c.fill()
        n.footprints(k, 160, 430, 1.0, n=3, step=24)
        n.detective(k, 122, 438, 1.02, "look", "squint", (0.8, 0.7), wrap=True)
    noir(c, 24, y0, 250, 452, don_full, "DETECTIVE DON · her wrap, by two fingers", bg=STREET)

    def eye(k):
        n.glass_handle(k, 92, 96, 76, 0.72); n.glass_view(k, 92, 96, 76, "eye")
    noir(c, 286, y0, 200, 216, eye, "5.9  his eye, in his glass", bg=(0.20, 0.20, 0.22))
    noir(c, 286, y0 + 240, 200, 212, lambda k: n.detective(k, 84, 372, 0.98, "proud", "almost", (0.3, -0.2), napkin_in_band=True),
         "5.10  solved. He never turns it over", bg=(0.24, 0.24, 0.26))

    def pam_full(k):
        k.c.set_source_rgb(*STONE); k.c.rectangle(0, 404, 250, 48); k.c.fill()
        n.footprints(k, 166, 432, 1.0, n=3, step=24)
        n.sweeper(k, 132, 438, 1.20, "sweep", "neutral", (0.9, -0.2))
    noir(c, 498, y0, 250, 452, pam_full, "PAM · the apron, the cap, the sweep", bg=STREET)

    def prints(k):
        n.glass_view(k, 100, 104, 84, "prints")
    noir(c, 760, y0, 200, 216, prints, "3.3  heel prints, and a broom", bg=(0.20, 0.20, 0.22))

    def looks(k):
        k.c.set_source_rgb(*STONE); k.c.rectangle(0, 170, 200, 42); k.c.fill()
        n.sweeper(k, 96, 268, 0.80, "lean", "neutral", (1.0, -0.3))
        n.dustpan(k, 166, 190, 0.8, full=True)
    noir(c, 760, y0 + 240, 200, 212, looks, "3.4  done. She watches him go", bg=STREET)
    for i, lab in enumerate(("4.1  her coin goes in", "the arm is already out", "4.2  the coin comes back")):
        yy = y0 + i * 155
        noir(c, 972, yy, 204, 128, lambda k, i=i: n.coin_steps(k, 46 if i else 100, 160, 0.48, i + 1), lab, bg=STREET)

    # ------------------------------------------------ six two-shots, at film size
    y2 = 1372
    corp(c, "SIX TWO-SHOTS · film frames (9:16), each with both people in it", 24, y2 - 12, 12, bold=True)
    for i, (fn, lab, tilt) in enumerate(((kf_hand, "2.4  his hand, past her", -0.07), (kf_pam, "3.2  she sees him coming", 0.0),
                                         (kf_robot, "4.1  stopped at the door", 0.0), (kf_hide, "5.2  behind the money", 0.0),
                                         (kf_caught, "5.9  caught", 0.0), (kf_trap, "6.6  again: past her hand", -0.07))):
        keyframe(c, 24 + i * 192, y2, fn, lab, tilt)

    # ------------------------------------------------ the drawing, the hands, notes
    y3 = 1736

    def drawing(k):
        n.napkin2(k, 62, 56, 0.80)
        n.napkin2(k, 62, 142, 0.80, back=True, ang=0.05)
        n.plan_open2(k, 232, 100, 1.25, -0.03)
    noir(c, 24, y3, 326, 200, drawing, "one drawing, twice: his note, and the roll", bg=(0.20, 0.18, 0.16))

    def hands(k):
        n.rich_hand(k, 118, 74, 1.15, 0.10, "money")
        n.rich_hand(k, 104, 166, 1.15, -0.06, "coupe")
        n.rich_hand(k, 222, 58, 1.15, 0.06, "coupe", flip=-1)
        n.rich_hand(k, 232, 148, 1.15, -0.08, "money", flip=-1)
    noir(c, 362, y3, 330, 200, hands, "5.1  hands out of the dark: money, not cards", bg=(0.34, 0.34, 0.36))
    notes(c, 708, y3 + 12, 466, "THE OTHERS, AND WHAT IS NOT HERE", [
        "Don holds her wrap up and away from him, so it is a thing he carries. His hat has a rim light. At the bar he is sure, and wrong.",
        "Pam's main pose is the sweep. The apron lifts her off the dark street; her bow blouse still shows.",
        "The robot's joke is three drawings: the coin in, the arm out, the coin back with the tag.",
        "Sofía awake, the taxi and the under-desk close-up are unchanged from sheet v2. The Shadow, Mom and the Bartender are unchanged from sheet v1.",
    ])

    c.set_source_rgb(*GREY); c.select_font_face("Inter", 0, 0); c.set_font_size(9.5)
    c.move_to(24, H2 - 14); c.show_text("Office Noir 2 · cast sheet " + V + " · from script v2 · for review: the six frames are staging tests, not the storyboard")
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
