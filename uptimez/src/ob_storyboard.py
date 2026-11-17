"""THE ONBOARDING: the storyboard, v3 (ob_storyboard_v2.py = v2, kept): in beat 3 the Client has a plain face (his
half-smile read as smirking back at Sofia; he is meant to be unaware). Nothing else changed.
THE ONBOARDING: the storyboard, v2 (ob_storyboard_v1.py = v1, kept), after the cold mute test (beat 3 was misread
as Sofia eyeing the roll and conspiring with Don) and the director's audit: her look lands on his FACE; the Client is
in her frame for the pearl; Don reacts alone, by going still; the drawing is shown open, with its gear; Pam's finger
shares a frame with Don; the robot is in frame 0; Pam starts to crouch in 8.5. Still 55 shots.
THE ONBOARDING: the storyboard (v1), every shot of script v4, one frame a shot, drawn with the film's own modules.
Wide shots are the stage (set_ob) at tile size; two-shots and three-shots take a double tile; inserts are the sheets'
inserts. It is a storyboard: framing, who shares a frame with whom, and the order of action and reaction. It is not
timing, and the mouths are not lip-sync.
Writes ob_storyboard_v1.png (captions), ob_storyboard_v1_mute.png (numbers only), and with a third argument a folder
of contact sheets for the cold mute test."""
import os
import sys
import math
import cairo
import kit
import brand
import sofia_ob as so
import client_ob as co
import don_v4 as dv
import acts_ob_v2 as ac
import set_ob_v2 as st
import hands_ob as hd
import ob_sofia_sheet as sh
import ob_chain as ch
from kit import Ctx, INK
from charsheets import corp, wrap

V = "v3"
FW, FH, GAP, COLS = 172, 306, 8, 7
WIDE = FW * 2 + GAP
GREY = (0.35, 0.40, 0.50)
F = st.FLOOR
BUST, EYES = (0, so.HY + 22), (0, so.HY + 12)
DOWN, UP = (-0.8, 1.0), (-0.8, -0.2)


def frames(k, c):
    A = sh.at
    mid = lambda r: (r[0] + r[2] / 2, r[1] + r[3] / 2)

    def stage(draw, open_=0.0):
        def fn(*r):
            sc = r[2] / float(st.W)                                  # a double tile: the lower part of the stage
            c.save(); c.translate(r[0], r[1] + r[3] - (F + 20) * sc); c.scale(sc, sc)
            st.stage(k, open_=open_); st.desk(k)
            draw()
            c.restore()
        return fn

    def cast(don="stand", sof=("hold", "smile", (-0.9, -0.2)), pam="typing", cli=None, shred=0.0, dlook=None, robot=True):
        if robot:
            st.robot(k, 198, F, 0.50, "idle", look=(-1, 0), side=-1)         # the robot is here from frame 0
        ac.shredder(k, st.SHRED_X, F, 1.0, fill=shred)
        if cli:
            cli()
        ac.don(k, 322, F + 4, 0.70, don, dlook)
        so.sofia(k, 402, F + 4, 0.70, sof[0], sof[1], look=sof[2])
        ac.pam(k, 486, F + 4, 0.70, pam)

    def S(pose, face, look, s=1.7, lean=0, pt=BUST, dy=-4):               # Sofia, close
        return lambda *r: A(k, mid(r)[0], mid(r)[1] + dy, s, pt, pose, face, look=look, lean=lean)

    def D(act, look=None, s=1.0, dy=10, conf=False, raw=None):            # Don, close, the stain below the frame line
        def fn(*r):
            x, y = mid(r)
            if raw:
                dv.don(k, x, y + dy + 302 * s, s, raw[0], raw[1], look=look or (-1, 0))
            else:
                ac.don(k, x + (10 if act == "hand_out" else 0), y + dy + 302 * s, s, act, look)
            if conf:
                st.confetti(k, x - 46, y - 70, x + 46, y + 40, n=11, seed=4, s=0.9)
        return fn

    def C(face, pose="open", look=(0.7, 0.0), s=1.05):                    # the Client, close
        return lambda *r: co.client(k, mid(r)[0] + 4, mid(r)[1] - 10 - (co.HY + 10) * s, s, pose, face, look=look)

    def CM(act, s=0.62, dx=0):                                            # the Client, medium, acting
        return lambda *r: ac.client(k, mid(r)[0] + dx, r[1] + r[3] - 8, s, act)

    def P(act, s=0.84, dx=0, look=None):                                  # Pam, medium
        return lambda *r: ac.pam(k, mid(r)[0] + dx, r[1] + r[3] - 6, s, act, look)

    def R(act, s=0.80, dx=0, extra=None):
        def fn(*r):
            if extra:
                extra(*r)
            st.robot(k, mid(r)[0] + dx, r[1] + r[3] - 8, s, act)
        return fn

    def two(left, right):
        return lambda *r: (left(r[0], r[1], r[2] / 2, r[3]), right(r[0] + r[2] / 2, r[1], r[2] / 2, r[3]))

    def handshake(robot):
        def fn(*r):
            fl = r[1] + r[3] - 8
            co.client(k, r[0] + 84, fl, 0.52, "offer", "confident", look=(0.8, 0.0))
            ac.don(k, r[0] + 286, fl, 0.62, "hand_out")
            if robot:
                st.robot(k, r[0] + 196, fl, 0.50, "block")
        return fn

    def handover(act):
        def fn(*r):
            fl = r[1] + r[3] - 8
            ac.client(k, r[0] + 92, fl, 0.56, act)
            ac.don(k, r[0] + 280, fl, 0.62, "hand_out")
        return fn

    def setdown(*r):
        x, fl = mid(r)[0] + 26, r[1] + r[3] - 6
        ac.shredder(k, x - 44 * 0.78, fl, 0.78, fill=0.3)
        ac.don(k, x, fl, 0.78, "set_down")

    def slot(*r):
        x, fl = mid(r)[0], r[1] + r[3] - 10
        ac.roll(k, x, fl - 236, 1.5, 0.0, ln=100)
        ac.shredder(k, x, fl, 1.7, fill=0.7)

    def pair(pose, face, look, dact, dlook=None):
        def fn(*r):
            cy = r[1] + r[3] / 2
            A(k, r[0] + 112, cy - 6, 1.5, BUST, pose, face, look=look)
            ac.don(k, r[0] + 290, cy + 34 + 302 * 0.98, 0.98, dact, dlook)
        return fn

    def take(*r):
        fl = r[1] + r[3] - 6
        so.sofia(k, r[0] + 120, fl, 0.84, "show", "recover", look=(1.0, 0.1))
        ac.pam(k, r[0] + 272, fl, 0.84, "empty", look=(-0.9, 0.0))

    def present(*r):
        fl = r[1] + r[3] - 6
        co.client(k, r[0] + 84, fl, 0.56, "open", "confident", look=(0.8, 0.3))
        so.sofia(k, r[0] + 262, fl, 0.84, "show", "recover", look=(-0.9, -0.15), lean=2)

    def press(done):
        return lambda *r: ch.frames.__globals__["his_thumb"](c, k, *((r[0] + 30, mid(r)[1] + 78, -0.5, 0.78) if done else
                                                                     (mid(r)[0] - 8, mid(r)[1] + 30, -0.42, 0.78))) or None

    def device(done):
        def fn(*r):
            sh.device_insert(c, k, mid(r)[0] + 6, mid(r)[1] - 6, 0.95, done=done)
            press(done)(*r)
        return fn

    def card(*r):
        fl = r[1] + r[3] - 8
        co.client(k, r[0] + 84, fl, 0.52, "offer", "confident", look=(0.8, 0.5), roll=False)   # the roll is gone by now
        ac.don(k, r[0] + 286, fl, 0.62, "hand_out")
        st.card_terminal(k, r[0] + 196, fl - 96, 1.5)
        kit.rect(k, r[0] + 162, fl - 150, 30, 19, (0.20, 0.42, 0.84), 77, lw=1.6)     # his card, on it

    def boom():
        st.cannon(k, 232, F, 1.0)
        st.robot(k, 176, F, 0.62, "tip")
        cast(don="hand_up", sof=("low", "smile", (-0.9, -0.2)), pam="stand", cli=lambda: co.client(
            k, 112, F, 0.66, "open", "warm", look=(0.8, 0.0)), dlook=(1, 0), robot=False)
        st.confetti(k, 150, 300, 530, 790, n=60, seed=11)
        st.confetti(k, 296, 520, 350, 600, n=10, seed=5, s=1.1)                       # full in Don's face

    def leaving():
        st.robot(k, 196, F, 0.50, "idle", look=(1, 0))
        ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
        co.client(k, 118, F, 0.66, "open", "warm", look=(-0.7, 0.0))
        so.sofia(k, 300, F + 4, 0.70, "low", "recover", look=(-0.9, -0.2))
        ac.don(k, 392, F + 4, 0.70, "hand_up", (-1, 0))
        ac.pam(k, 486, F + 4, 0.70, "stand", (-0.8, 0.9))
        st.confetti(k, 150, 300, 530, 790, n=50, seed=13)

    def hold(*r):
        fl = r[1] + r[3] - 6
        st.confetti(k, r[0] + 10, r[1] + 10, r[0] + r[2] - 10, fl - 30, n=34, seed=17, s=0.9)
        so.sofia(k, r[0] + 196, fl - 8, 0.56, "trophy", "knowing", look=(-0.9, 0.5))
        st.robot(k, r[0] + 262, fl - 8, 0.44, "idle")
        ac.scatter(k, r[0] + 150, r[0] + r[2] - 8, fl - 4, 0.8, n=16, seed=9)
        ac.pam(k, r[0] + 296, fl + 44, 0.74, "kneel")
        ac.don(k, r[0] + 78, fl + 96, 1.0, "hand_up", (1, 0))

    def strip_insert(*r):
        x, y = mid(r)
        hd.palm(k, x + 4, y + 96, 4.4, 0.0, co.SKIN, 3)
        c.save(); c.translate(x + 2, y + 6); c.rotate(0.35)
        kit.rect(k, -13, -62, 26, 124, ac.STRIP, 5, lw=2)
        c.set_source_rgb(1, 1, 1); c.set_line_width(2.6); c.arc(0, 30, 17, math.pi, 2 * math.pi); c.stroke()
        for a in (-2.4, -1.57, -0.74):
            c.move_to(17 * math.cos(a), 30 + 17 * math.sin(a)); c.line_to(24 * math.cos(a), 30 + 24 * math.sin(a)); c.stroke()
        c.move_to(0, -54); c.line_to(0, -8); c.stroke()
        c.restore()

    def last():
        c.save(); c.rectangle(*st.DOOR); c.clip()
        ac.client(k, 62, F + 6, 0.50, "watch", look=(-0.9, 2.2))
        c.set_source_rgba(*st.GLASS, 0.50); c.rectangle(*st.DOOR); c.fill()
        c.restore()
        st.stamp(c, 97, 560, 0.74)
        ac.shredder(k, st.SHRED_X, F, 1.0, fill=0.0)
        st.confetti(k, 170, 330, 530, 780, n=46, seed=11)
        st.robot(k, 204, F, 0.62, "stamp", look=(-1, 0), side=-1)
        ac.don(k, 352, F + 4, 0.70, "hand_up")
        ac.scatter(k, 190, 530, F + 8, 1.0, n=20, seed=9)
        ac.pam(k, 458, F + 64, 0.82, "kneel")

    def pam_don(act):                                                     # her finger and the man who does not see it
        def fn(*r):
            fl = r[1] + r[3] - 6
            dv.don(k, r[0] + r[2] - 34, fl - 26, 0.46, "pleased", "smug", look=(-1, 0))
            ac.pam(k, r[0] + 62, fl, 0.84, act, look=(-0.9, 0.6) if act == "finger" else (0.9, -0.2))
        return fn

    enter = lambda: co.client(k, 112, F, 0.66, "arrive", "confident", look=(0.8, 0.0))
    return [
        ("1.1", 2, "The door slides open. He walks in.", "", stage(lambda: cast(cli=enter, dlook=(1, 0)), 0.85)),
        ("1.2", 2, "Pam looks at Don, Don at Sofía, Sofía at him. Pam is already typing.", "",
         lambda *r: (ac.don(k, r[0] + 84, r[1] + r[3] - 6, 0.80, "stand", (1, 0)),
                     so.sofia(k, r[0] + 184, r[1] + r[3] - 6, 0.80, "hold", "smile", look=(-0.9, -0.2)),
                     ac.pam(k, r[0] + 290, r[1] + r[3] - 6, 0.80, "typing", look=(-0.9, 0.0)))),
        ("1.3", 1, "", "CLIENT: \"Hi. I'd like to sign up.\"", C("confident", "arrive")),
        ("1.4", 1, "Don: the vest.", "", D("pro", (1.0, 0.0))),
        ("2.1", 2, "A hand out. His nose wrinkles: oil.", "DON: \"Don. CEO.\"", handshake(False)),
        ("2.2", 2, "The red paddle snaps up between the palms.", "ROBOT: \"CONTACT NOT VERIFIED.\"", handshake(True)),
        ("2.3", 1, "Stranded. A bigger title.", "DON: \"Founder. And CEO.\"", D("hand_out", s=0.9, dy=0)),
        ("2.4", 1, "What just happened?", "", C("puzzled", look=(0.8, 0.2))),
        ("3.1", 2, "He shows the drawing; it springs shut in his hand.", "CLIENT: \"Ten garages. And I keep losing this.\"",
         lambda *r: (co.client(k, r[0] + 80, r[1] + r[3] - 6, 0.56, "open", "plain", look=(0.8, 0.0)),
                     ac.blueprint_open(k, r[0] + 96, r[1] + r[3] - 150, 0.92),
                     so.sofia(k, r[0] + 214, r[1] + r[3] - 6, 0.80, "hold", "smile", look=(-0.9, -0.3)),
                     ac.don(k, r[0] + 306, r[1] + r[3] - 6, 0.80, "stand", (-1, 0)))),
        ("3.2", 1, "Sweet.", "SOFÍA: \"Does your missus love your garages?\"", S("hold", "smile", (-0.8, -0.1), lean=-4)),
        ("3.3", 1, "Plain.", "CLIENT: \"I live alone.\"", C("plain")),
        ("3.4", 1, "Her eyes go down him.", "", S("low", "appraise", DOWN, 2.3, pt=EYES, dy=-8)),
        ("3.5", 1, "What they are on: him. Plain, friendly, unaware.", "", C("plain", look=(0.0, 0.0), s=0.80)),
        ("3.6", 1, "They come back up. Her face answers.", "", S("low", "interested", (-0.9, -0.2), 2.3, pt=EYES, dy=-8)),
        ("3.7", 1, "Thumb and index take one pearl, and roll it.", "SOFÍA: \"Oh...\"",
         S("pearl", "oh", (-0.9, -0.2), 2.5, pt=(16, so.BODY_TOP + 18), dy=4)),
        ("3.8", 2, "She rolls the pearl, her eyes on him. He is looking at his drawing.", "",
         lambda *r: (co.client(k, r[0] + 84, r[1] + r[3] - 6, 0.62, "arrive", "plain", look=(-0.6, 1.4)),
                     A(k, r[0] + 250, r[1] + r[3] / 2 - 6, 1.5, BUST, "pearl", "interested", look=(-1.0, -0.1)))),
        ("3.9", 1, "Don has seen it. He goes still; the smile is gone.", "", D("still")),
        ("3.10", 1, "She sees that he saw. Her hand stops. Her mouth closes.", "", S("pearl", "caught", (1.0, 0.0))),
        ("3.11", 1, "The vest. The smile comes back, too wide.", "", D("pro")),
        ("3.12", 1, "He saw none of it.", "CLIENT: \"Can it find this when I lose it?\"", C("plain", "arrive", s=0.80)),
        ("4.1", 1, "He believes it.", "DON: \"Here, you will never lose anything again.\"", D(None, (-1, 0), raw=("pleased", "grin"))),
        ("4.2", 2, "An open palm. He holds the roll back a moment.", "", handover("hesitate")),
        ("4.3", 2, "He gives it.", "DON: \"We'll take care of it.\"", handover("give")),
        ("4.4", 1, "Eyes on Sofía. He stands it beside him.", "", setdown),
        ("4.5", 1, "The slot. Blue strips fill the bin.", "", slot),
        ("4.6", 1, "Impressed.", "", C("warm")),
        ("5.1", 1, "Pam saw. A finger goes up. Don does not see her.", "", pam_don("finger")),
        ("5.2", 1, "Don, glowing.", "", D(None, (-1, 0), raw=("pleased", "smug"))),
        ("5.3", 1, "She looks at him, and lowers it.", "", pam_don("lower")),
        ("5.4", 1, "The watch.", "CLIENT: \"One month. I ask, you find it.\"", CM("watch")),
        ("5.5", 1, "No question asked. His eyes go to Sofía.", "DON: \"Approved.\"", D(None, (1.4, 0), raw=("stand", "grin"))),
        ("5.6", 1, "She is looking at the Client.", "", S("low", "interested", (-0.9, -0.2))),
        ("6.1", 2, "Clipboard under her arm, she takes Pam's tablet without a look.", "", take),
        ("6.2", 2, "One green button. A breath, close to him.", "SOFÍA: \"Tap here.\"", present),
        ("6.3", 1, "His thumb.", "", device(False)),
        ("6.4", 1, "A tick. His thumbprint, in oil.", "", device(True)),
        ("6.5", 1, "Pleased with a result.", "CLIENT: \"That worked.\"", C("warm")),
        ("6.6", 1, "Her smile turns real. Half a second.", "", S("low", "real", (-0.6, 0.0))),
        ("6.7", 2, "The smile goes; then her eyes cut to Don. He saw, and has gone still.", "", pair("low", "caught", (1.0, 0.0), "still")),
        ("6.8", 1, "Her CV, into the welcome pack.", "SOFÍA: \"Everything you need is in there.\"",
         lambda *r: sh.cv_insert(c, k, mid(r)[0] - 6, mid(r)[1] - 6, 1.0)),
        ("6.9", 1, "Pam's empty hands.", "", P("empty")),
        ("7.1", 2, "The handshake framing again. He taps his card.", "", card),
        ("7.2", 1, "", "", lambda *r: st.payment(c, k, mid(r)[0], mid(r)[1], 0.86)),
        ("7.3", 1, "Green at once. It leans toward the card.", "ROBOT: \"CONTACT APPROVED.\"",
         R("approve", s=0.66, dx=14, extra=lambda *r: st.card_terminal(k, r[0] + 30, r[1] + r[3] - 96, 1.4, state="ok"))),
        ("7.4", 1, "He pumps his unshaken hand. One dollar.", "", D("hand_up", (-1, 0.4), s=0.9, dy=30)),
        ("8.1", 1, "The bin, into the cannon.", "ROBOT: \"FIRST CUSTOMER. CELEBRATION REQUIRED.\"",
         R("tip", dx=-22, extra=lambda *r: st.cannon(k, r[0] + r[2] - 36, r[1] + r[3] - 8, 0.9))),
        ("8.2", 2, "Boom. Full in Don's face.", "", stage(boom)),
        ("8.3", 1, "Strips in his face, still beaming.", "DON: \"SOFÍA! WE HAVE A CUSTOMER!\"", D("hand_up", (1, 0), s=0.9, dy=30, conf=True)),
        ("8.4", 2, "Sofía walks him to the door.", "", stage(leaving)),
        ("8.5", 1, "Pam looks at his hand. Then at the floor, and starts down.", "",
         lambda *r: (ac.scatter(k, r[0] + 6, r[0] + r[2] - 6, r[1] + r[3] - 16, 0.8, n=12, seed=9), P("crouch")(*r))),
        ("9.1", 2, "Held: his hand is free; she is on the floor; Sofía takes her trophy; the robot reports.", "", hold),
        ("10.1", 1, "A strip settles in his palm.", "", CM("palm", dx=-12)),
        ("10.2", 1, "White lines on blue. Part of a gear.", "", strip_insert),
        ("10.3", 1, "Into his pocket, eyes already up. The watch.", "", CM("pocket")),
        ("10.4", 2, "", "ROBOT: \"ONBOARDING COMPLETE.\"", stage(last)),
    ]


def layout(fr, top, cap):
    out, col, row = [], 0, 0
    for _, span, *_ in fr:
        if col + span > COLS:
            col, row = 0, row + 1
        out.append((40 + col * (FW + GAP), top + row * (FH + cap), FW if span == 1 else WIDE))
        col += span
    return out, row + 1


def main(out, mute=False):
    fr = frames(None, None)
    cap, top = (26, 30) if mute else (80, 86)
    pos, rows = layout(fr, top, cap)
    W = 40 + COLS * FW + (COLS - 1) * GAP + 40
    H = top + rows * (FH + cap) + 10
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * 2, H * 2)
    c = cairo.Context(surf); c.scale(2, 2)
    c.set_source_rgb(0.97, 0.96, 0.93); c.paint()
    k = Ctx(c, 0)
    if not mute:
        brand.mark(c, 40, 20, 34, zzz=False)
        corp(c, "THE ONBOARDING", 84, 44, 28, bold=True)
        corp(c, "storyboard " + V + "  ·  script v4, %d shots" % len(fr), 346, 44, 13, col=GREY)
        c.set_source_rgb(*brand.NAVY); c.set_line_width(1.2); c.move_to(40, 64); c.line_to(W - 40, 64); c.stroke()
    for i, ((shot, span, what, line, fn), (x0, y0, w)) in enumerate(zip(frames(k, c), pos)):
        c.save(); c.rectangle(x0, y0, w, FH); c.clip()
        c.set_source_rgb(*kit.WALL); c.rectangle(x0, y0, w, FH); c.fill()
        fn(x0, y0, w, FH)
        c.restore()
        c.set_source_rgb(*INK); c.set_line_width(1.4); c.rectangle(x0, y0, w, FH); c.stroke()
        corp(c, "%d" % (i + 1) if mute else shot, x0, y0 + FH + 15, 10.5, bold=True)
        if not mute:
            yy = y0 + FH + 15
            if what:
                yy = wrap(c, what, x0, yy + 14, 9.2, w - 4)
            if line:
                wrap(c, line, x0, yy + 14, 8.8, w - 4, col=GREY)
    surf.write_to_png(out)
    return [(x0 * 2, y0 * 2, w * 2) for x0, y0, w in pos]


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "../the-onboarding"
    main("%s/ob_storyboard_%s.png" % (d, V))
    pos = main("%s/ob_storyboard_%s_mute.png" % (d, V), mute=True)
    if len(sys.argv) > 2:
        print(ch.sheets("%s/ob_storyboard_%s_mute.png" % (d, V), pos, sys.argv[2]))
    print("wrote", d, len(pos), "frames")
