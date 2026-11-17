"""THE ONBOARDING: the set sheet, v5 (ob_set_sheet_v4.py = v4, kept): Pam on the floor has hips and a curved hem (acts_ob
v4). Nothing else changed. Below, the notes of v4.
THE ONBOARDING: the set sheet, v4 (ob_set_sheet_v3.py = v3, kept): set_ob v4 (one closer camera, the cast in depth, the
ficus moved, a desk with a corner) and Pam on the floor (acts_ob "floor_up"). Below, the notes of v3.
THE ONBOARDING: the set sheet, v3 (ob_set_sheet_v2.py = v2, kept): the walls of set_ob v3 (OUR FIRST CLIENT, empty;
the ficus from The Best Candidate by the door) and the arms of acts_ob v3. Below, the notes of v2.
THE ONBOARDING: the set and the robot, sheet v2 (ob_set_sheet_v1.py = v1, kept): in the last frame the Client is
walking away with his eyes on his watch (facing the glass, he read as locked out), and the robot leans toward the
card. Below, the notes of v1. THE ONBOARDING: the set and the robot (sheet v1). Frame 0 and the last frame on the same camera, the robot's four
actions, the shredder filling, the payment insert. Writes ob_set_v2.png at 2400x1860 (drawn at 1200x930, 2x)."""
import sys
import cairo
import kit
import brand
import set_ob as st
import acts_ob as ac
import sofia_ob as so
import client_ob as co
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v5"
W2, H2 = 1200, 930
GREY = (0.35, 0.40, 0.50)


def staged(c, x, y, sc, draw):
    c.save(); c.translate(x, y); c.scale(sc, sc); c.rectangle(0, 0, st.W, st.H); c.clip()
    draw()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(x, y, st.W * sc, st.H * sc); c.stroke()


def panel(c, x, y, w, h, draw):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.set_source_rgb(*kit.WALL); c.rectangle(x, y, w, h); c.fill()
    c.set_source_rgb(0.72, 0.63, 0.50); c.rectangle(x, y + h - 16, w, 16); c.fill()
    draw(x, y, w, h)
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2 * 2, H2 * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    brand.mark(c, 24, 20, 34, zzz=False)
    corp(c, "THE ONBOARDING", 68, 44, 28, bold=True)
    corp(c, "the set and the robot  ·  the front desk, at the door", 330, 44, 13, col=GREY)
    t = "UPTIMEZ INC. · SET SHEET · " + V
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(10)
    corp(c, t, W2 - 24 - c.text_extents(t).x_advance, 30, 10, col=GREY, bold=True)
    c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(24, 64); c.line_to(W2 - 24, 64); c.stroke()
    F, SC = st.FLOOR, 0.60

    P = st.POS

    def frame0():
        st.cam(c)
        st.stage(k, open_=0.85)
        st.desk(k, shred=0.0)
        st.robot(k, P["robot"][0], F, P["robot"][2], "idle", look=(-1, 0), side=-1)
        co.client(k, 112, F, 0.66, "arrive", "confident", look=(0.8, 0.0))
        ac.pam(k, *P["pam"], "typing")                                       # back at the desk's end, on her tablet
        so.sofia(k, *P["sofia"], "hold", "smile", look=(-0.9, -0.2))         # a clear view of the door
        ac.don(k, *P["don"], "stand", look=(-1, 0))                          # half a step toward him

    def last():
        st.cam(c)
        st.stage(k, open_=0.0)
        c.save(); c.rectangle(*st.DOOR); c.clip()                          # through the glass: he is leaving
        ac.client(k, 98, F + 6, 0.50, "watch", look=(-0.9, 2.2))
        c.set_source_rgba(*st.GLASS, 0.26); c.rectangle(*st.DOOR); c.fill()    # a lighter glass: his face and his watch read
        c.restore()
        st.stamp(c, st.STAMP_AT[0], st.STAMP_AT[1], 0.74)
        st.desk(k, shred=0.0)
        st.confetti(k, 190, 300, 480, 600, n=9, seed=11, s=1.25)             # a few, plainly falling
        st.robot(k, 204, F, 0.62, "stamp", look=(-1, 0), side=-1)
        ac.scatter(k, 214, 286, F + 10, 1.0, n=7, seed=4)                    # the mess: at the shredder, and round Pam
        ac.scatter(k, 322, 478, F + 30, 1.0, n=13, seed=9)
        ac.don(k, 292, F + 6, 0.72, "hand_up", look=(-1.2, -0.4))            # his eyes on the door: he does not see her
        ac.pam(k, 446, F + 46, 0.63, "floor_up")
    staged(c, 24, 84, SC, frame0)
    staged(c, 24 + st.W * SC + 16, 84, SC, last)
    y = 84 + st.H * SC + 16
    corp(c, "FRAME 0", 24, y, 11, bold=True)
    wrap(c, "The door slides open and he walks in. Don is half a step forward, Sofía a little behind him with a clear view "
         "of the door, Pam back at the desk, on her tablet. The robot is parked by the shredder.", 24, y + 15, 10, st.W * SC - 4, col=GREY)
    x2 = 24 + st.W * SC + 16
    corp(c, "THE LAST FRAME  ·  the same camera", x2, y, 11, bold=True)
    wrap(c, "He has left, content, his eyes on his watch. The stamp is on the glass, clear of his face. Don's hand is still "
         "up and his eyes are on the door. Pam is on her knees, one hand on a strip, and looks up at him. He does not see her.", x2, y + 15, 10,
         st.W * SC - 4, col=GREY)

    px0 = 24 + 2 * (st.W * SC + 16)
    pw, ph = (W2 - 24 - px0 - 12) / 2.0, 214
    cells = [
        ("THE BLOCK", "beat 02: red, between the palms", lambda x, yy, w, h: st.robot(k, x + w / 2 - 14, yy + h - 18, 0.56, "block")),
        ("THE CARD", "beat 07: green, and it leans in", lambda x, yy, w, h: st.robot(k, x + w / 2 - 14, yy + h - 18, 0.56, "approve")),
        ("THE CELEBRATION", "beat 08: the bin into the cannon", lambda x, yy, w, h: (
            st.cannon(k, x + w - 44, yy + h - 18, 0.9), st.robot(k, x + 70, yy + h - 18, 0.56, "tip"))),
        ("THE STAMP", "beat 10: on the glass", lambda x, yy, w, h: (
            st.robot(k, x + w - 84, yy + h - 18, 0.56, "stamp", side=-1), st.stamp(c, x + 56, yy + 96, 0.42))),
        ("THE SHREDDER", "empty, then his drawing", lambda x, yy, w, h: (
            ac.shredder(k, x + 54, yy + h - 18, 0.9, fill=0.0), ac.shredder(k, x + w - 54, yy + h - 18, 0.9, fill=0.8))),
        ("THE PAYMENT", "beat 07: the insert", lambda x, yy, w, h: st.payment(c, k, x + w / 2, yy + h / 2 - 2, 0.74)),
    ]
    for i, (lab, note, fn) in enumerate(cells):
        x0 = px0 + (i % 2) * (pw + 12); y0 = 84 + (i // 2) * (ph + 44)
        panel(c, x0, y0, pw, ph, fn)
        corp(c, lab, x0, y0 + ph + 15, 10, bold=True)
        corp(c, note, x0, y0 + ph + 29, 8.6, col=GREY)
    wrap(c, "The robot is the HR robot of the last films, unchanged. Every screen it shows is true: the contact was not "
         "verified, the contact (a card) was approved, a celebration is required, the onboarding is complete.", px0,
         84 + 3 * (ph + 44) + 6, 10, W2 - 24 - px0, col=GREY)
    surf.write_to_png(out)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_set_%s.png" % (d, V))
    print("wrote", d)
