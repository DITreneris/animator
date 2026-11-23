"""OFFICE NOIR 4: SEVEN LIVES, the scene file, v1 (stage 4, series/production-process.md, 23 Nov). From here on this file
is the episode: every shot with its time and line, its location and camera, who is in frame and where, the props that
must stay out of the dead zones, the action and the reaction. Generated from it, never edited by hand:

  python3 on4_scenes.py [out]  ->  office-noir-4-script-v5.md     the script (generated)
                                   on4_layout_s<N>_v1.png          a layout sheet per beat: every shot at 270, with its checks
                                   on4_shotplan_v1.png             the top-down shot plan (locations, cameras, the table)
                                   on4_blocking_v1.png             the blocking sheet for the hardest beat (3.2-3.3)
                                   on4_test_32_v1.png, _33_v1.png  two real camera frames of it, for the cold viewers
  The build exits 1 on a check that fails and is not in KNOWN with its reason.

The plan it starts from: script v4 (office-noir-4-script-v4.md); the timing: on4_timing_v1.json (narration A, no remark).
The sets: on4_street (A, B, C; the crossing ZEBRA v6), on4_car v2, on4_club v7, on4_lying v3, on4_props v2, fs_set4 (S6).
Locations not drawn yet are STAND-INS, named on the sheet: the fire escape (2.1, 2.4), the back seat (2.2, 2.3), the
stage (6.1, 6.3-6.6), the CV (6.2). Sofia's coat and bag are not drawn yet (her office rig, sofia_dh, stands in)."""
import json
import math
import os
import sys
import cairo
import kit
from kit import Ctx, INK
import engine_on as eng
import on_set as ons
import on4_street as st
import on4_car as car
import on4_cast as oc
import on4_props as pr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "office-noir-4")
W, H = 540, 960
TIMING = "on4_timing_v1.json"
DEAD = lambda x, y: y > 720 or (x > 470 and 380 < y < 860)

CHANGES = [
    "Script v4 is the plan: 5.2 is the plan and the UptimeZ card, 3.1 the car's turn at the junction.",
    "The crossing is raised to y 646-712 (on4_street ZEBRA v6, Tomas's pick): the bump, her head and the bills above y 720.",
    "8.2 is a push in from S6 to the lamp; the room goes dark round it; its head ends where frame 0's streetlamp hangs.",
    "Sofia's mug is her own (tall, black, the kiss outside the rim): the eighth reads without counting.",
]

# --- the locations: a drawing in frame units (camera 270, 480, 1) and its light, after the grade ---------------------------
def loc_a(k, taillights=False):
    st.setup_a(k, taillights=taillights)


def loc_b(k):
    st.setup_b(k, car=False); car.b_end(k)


def loc_c(k):
    st.ZEBRA[0] = "v6"
    try:
        st.setup_c(k)
    finally:
        st.ZEBRA[0] = "v4"


def fire_escape(k, y=700):
    """STAND-IN: the fire escape's railing in the foreground, black iron against the lane below."""
    c = k.c
    c.set_source_rgb(*INK)
    c.rectangle(-10, y - 6, 560, 12); c.fill(); c.rectangle(-10, y + 70, 560, 14); c.fill()
    for x in range(10, 550, 34):
        c.rectangle(x, y, 5, 80); c.fill()


def back_seat(k):
    """STAND-IN: the back seat through the open window (car.cabin's door and glass), the people clipped to it later."""
    car.cabin(k, 40, 640, 1.5, 1.0, hand=False)


BS_WIN = (40, 640, 1.5)                                      # the window's bottom left and scale (car.cabin)


def bs_clip(c):
    x, y, s = BS_WIN
    c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(0, 0); c.line_to(300, 0); c.line_to(300, -140); c.line_to(260, -170); c.line_to(0, -170)
    c.close_path(); c.identity_matrix() if False else None


def stage(k, lit="pam"):
    """STAND-IN: the club's stage close. Dark room, the boards, a curtain, the spotlight on its stand at the right;
    lit = "pam" (the cone on her) or "table" (swung away: the card table and the booth wall lit behind her)."""
    c = k.c
    c.set_source_rgb(0.08, 0.07, 0.08); c.paint()
    if lit == "table":                                       # the lit wall and the card table behind her
        g = cairo.RadialGradient(270, 560, 20, 270, 560, 300)
        g.add_color_stop_rgba(0, 0.95, 0.93, 0.88, 1); g.add_color_stop_rgba(1, 0.95, 0.93, 0.88, 0.0)
        c.set_source(g); c.rectangle(0, 300, 540, 420); c.fill()
        st.poly(k, [(150, 600), (390, 600), (380, 616), (160, 616)], (0.06, 0.06, 0.07), 2)
        for x in (200, 340):
            st.thug(k, x, 640, 0.30, "open", seed=4700 + x, hands=("relax", "relax"))
    for x in range(0, 540, 46):                              # the curtain folds
        c.set_source_rgb(0.16, 0.06, 0.08) if (x // 46) % 2 else c.set_source_rgb(0.22, 0.08, 0.10)
        c.rectangle(x, 0, 46, 250 if lit == "table" else 640); c.fill()
    st.poly(k, [(-10, 640), (550, 640), (550, 700), (-10, 700)], (0.42, 0.30, 0.20), 2.0)   # the stage's boards
    c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(470, 700); c.line_to(470, 330); c.stroke()   # the stand
    st.poly(k, [(440, 300), (500, 310), (492, 350), (436, 336)], (0.20, 0.20, 0.22), 2.0)
    if lit == "pam":
        c.set_source_rgba(1, 1, 0.92, 0.30)
        c.move_to(440, 320); c.line_to(120, 700); c.line_to(330, 700); c.line_to(446, 336); c.close_path(); c.fill()


def cv_insert(k):
    """STAND-IN: Sofia's CV in the envelope's warm light; her photograph is her own face (the dream's drawing, lesson 160)."""
    import sofia_dh as sd
    c = k.c
    c.set_source_rgb(0.10, 0.08, 0.08); c.paint()
    kit.cut(k, [(110, 170), (430, 160), (440, 600), (120, 610)], (0.99, 0.98, 0.95), shadow=False, lw=2.2)
    kit.text(k, "CURRICULUM VITAE", 300, 220, 22, INK, bold=True)
    kit.cut(k, [(140, 250), (250, 248), (252, 390), (142, 392)], (0.86, 0.84, 0.80), shadow=False, lw=1.6)
    c.save(); c.rectangle(142, 250, 110, 140); c.clip(); sd.sofia(k, 196, 560, 0.62, "hold", "smile", (0, 0)); c.restore()
    kit.text(k, "SOFIA", 340, 300, 34, INK, bold=True)
    for i in range(7):
        c.set_source_rgb(0.6, 0.6, 0.62); c.set_line_width(3); c.move_to(150, 430 + i * 22); c.line_to(400 - (i % 3) * 40, 430 + i * 22); c.stroke()


def knee_insert(k):
    """STAND-IN, 2.3: the envelope on the Client's knee, his finger on it, his watch; the ringed hand flat on the seat."""
    import dh_cast as dc
    c = k.c
    c.set_source_rgb(0.10, 0.10, 0.11); c.paint()
    st.poly(k, [(-10, 520), (330, 470), (360, 700), (-10, 720)], (0.20, 0.22, 0.28), 2.4)      # his knee and thigh
    oc.envelope(k, 200, 520, 2.6)
    st.poly(k, [(330, 300), (430, 260), (470, 330), (360, 380)], (0.20, 0.22, 0.28), 2.4)      # his sleeve
    kit.ellipse(k, 316, 400, 40, 30, (0.87, 0.70, 0.58), 7101, shadow=False, lw=2.2)           # his hand,
    c.set_source_rgb(*INK); c.set_line_width(16); c.set_line_cap(1); c.move_to(290, 420); c.line_to(250, 476); c.stroke()
    c.set_source_rgb(0.87, 0.70, 0.58); c.set_line_width(12); c.move_to(290, 420); c.line_to(250, 476); c.stroke()
    c.set_line_cap(0)
    st.poly(k, [(352, 372), (372, 362), (380, 384), (360, 392)], (0.85, 0.80, 0.55), 1.4)    # the watch
    st.poly(k, [(560, 600), (430, 620), (434, 680), (560, 690)], dc.VELVET, 2.4)            # Dad's cuff, his hand flat
    kit.ellipse(k, 400, 650, 44, 26, dc.SKIN_F, 7102, shadow=False, lw=2.2)
    dc.ring(k, 392, 640, 1.4)


def spot_insert(k):
    """STAND-IN, 6.4: the spotlight's head and handle; a pale glove from the top of the frame on the handle."""
    import hands_ps as hp
    c = k.c
    c.set_source_rgb(0.06, 0.06, 0.07); c.paint()
    st.poly(k, [(150, 420), (390, 380), (420, 560), (170, 600)], (0.22, 0.22, 0.24), 2.6)      # the lamp's barrel
    c.new_path(); c.arc(160, 510, 92, 0, 2 * math.pi); c.set_source_rgb(1, 1, 0.94); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(10); c.move_to(400, 470); c.line_to(470, 470); c.stroke()  # the handle
    c.set_source_rgb(0.05, 0.05, 0.06); c.rectangle(372, 90, 60, 300); c.fill()                 # his black sleeve
    hp.draw(k, "grab", 410, 440, 120, st.GLOVE, (0.0, 1.0), 1)


# --- the cast, in frame units ----------------------------------------------------------------------------------------------
def P(who, *a, **kw):
    return (who, a, kw)


ARM_UP = (-8, 0) + oc.pm.ik(1, 30, oc.HY - 150)             # 7.1 / 6.5: one arm up on its elbow, the hand open
HAND_STOP = (-8, 0) + oc.pm.ik(1, 80, oc.HY + 10)          # 3.2: one hand up at the headlights
DON_REACH = (-70, 20, 8, 0)                                # 3.3: his screen-left arm out and down to the bumper


def draw_cast(k, cast):
    """Draws each figure; returns {who: rig points}."""
    import client_ob as co
    import dh_cast as dc
    import sofia_dh as sd
    out = {}
    cast = list(cast)
    for i, (who, a, kw) in enumerate(cast):                 # reach_to: move the figure so its right hand lands on a point
        if "reach_to" in kw:
            kw = dict(kw); tx, ty = kw.pop("reach_to"); hi = kw.pop("reach_hand", 1)
            c = k.c; c.push_group(); o = draw_cast(k, [(who, a, kw)])[who]; c.pop_group()
            hx, hy = o["hands"][hi]
            a = (a[0] + tx - hx, a[1] + ty - hy) + tuple(a[2:])
            cast[i] = (who, a, kw)
    for who, a, kw in cast:
        if who == "pam_cat":
            o = oc.pam_cat(k, *a, **kw)
        elif who == "pam_black":                             # 6.5: a black shape against the lit wall
            c = k.c
            c.push_group(); o = oc.pam_cat(k, *a, **kw); g = c.pop_group()
            c.set_source_rgb(0.03, 0.03, 0.04); c.mask(g)
        elif who == "pam_awake":
            o = oc.pam_awake(k, *a, **kw)
        elif who == "don":
            o = oc.don_cop(k, *a, **kw)
        elif who == "sofia":
            o = sd.sofia(k, *a, **kw)
        elif who == "client":
            o = co.client(k, *a, **kw)
        elif who == "father":
            o = dc.father(k, *a, **kw)
        elif who.startswith("thug"):
            o = st.thug(k, *a, **kw)
        elif who == "flat":                                  # a shadow lying flat on the cobbles
            st.cast(k, *a, **kw); o = {}
        else:
            raise ValueError(who)
        out[who] = o
    return out


# --- the shots --------------------------------------------------------------------------------------------------------------
def S(id_, size, loc, cam, picture, cast=(), protect=(), line="", action="", reaction="", eyeline="", standin=False,
      after=None, dream=True):
    """cam: (fx, fy, z): the frame point to the middle of the picture, zoom. protect: story props, frame units."""
    return dict(id=id_, size=size, loc=loc, cam=cam, picture=picture, cast=tuple(cast), protect=tuple(protect), line=line,
                action=action, reaction=reaction, eyeline=eyeline, standin=standin, after=after, dream=dream)


WIDE = (270, 480, 1.0)
A_SHADOW = lambda: [P("flat", 150, 740, 0.42, seed=4101), P("flat", 330, 760, 0.42, seed=4102)]
ROAD_Y = 712                                               # the crossing's near edge (ZEBRA v6)


def _ears_back(k):                                         # 2.1: the back of her head, her ears, in the foreground
    c = k.c
    kit.ellipse(k, 120, 640, 120, 110, (0.06, 0.06, 0.07), 7201, shadow=False, lw=2.4)
    oc.ears(k, 120, 640, 1.3)


HANDS = {}


def _sofia_post(k):                                        # 7.2: the envelope going into Pam's raised hand (her rig's hand)
    hx, hy = HANDS.get("pam_awake", (706, 510))
    pr.envelope(k, hx + 4, hy - 26, 0.28, 0.3)


def _rota_held(k):                                         # 7.5: the sheet in her hands, close
    pr.rota(k, 650, pr.F - 216, 0.46, -0.05)


def lying_over(k):                                         # 3.3: her body over Don's feet (he stands behind her)
    import on4_lying as ly
    ly.body(k); ly.head(k, *ly.HEAD, ly.ANG)


def _bills(k):
    import on4_lying as ly
    for (x, y, a) in ((360, 520, 0.3), (330, 560, -0.6), (380, 600, 0.9)):
        ly.bill(k, x, y, a, 1.4, seed=int(x))


SCENES = [
    ("01 Ignored hero", [
        S("1.1", "wide, low", "A", WIDE, "Frame 0, held 0.5 s. The streetlamp, the neon heart. Pam-Cat in the hero pose, "
          "eyes back over her shoulder; two shadows flat on the cobbles; Sofia one step behind, eyes on her phone.",
          cast=A_SHADOW() + [P("sofia", 330, 640, 0.40, "hold", "neutral", (0, 0.6)),
                              P("pam_cat", 230, 720, 0.62, "hero", "proud", (0.6, -0.1))],
          protect=[("streetlamp", st.A_LAMP), ("heart", (342, 266))], eyeline="Pam back to Sofia; Sofia to her phone",
          action="(held)", reaction="Pam: Here it comes."),
        S("1.2", "wide, low", "A", WIDE, "0:01. Sofia sidesteps Pam like a puddle and walks on, past the camera; she never looks up.",
          cast=A_SHADOW() + [P("pam_cat", 230, 720, 0.62, "hero", "proud", (0.6, -0.1)),
                              P("sofia", 380, 800, 0.56, "hold", "neutral", (0, 0.6))],
          action="Sofia sidesteps her (the 0:01 joke)", reaction="the hero pose held at nobody"),
        S("1.3", "close", "A", (230, 600, 2.1), "The pose holds; her eyes follow Sofia out; the pose sags; she pulls her coat straight.",
          cast=[P("pam_cat", 230, 720, 0.62, "sag", "sad", (0.8, 0.2))], line="N: I know how to survive.",
          action="the pose sags", reaction="Fine. (to where Sofia went)"),
        S("1.4", "wide", "A_tail", WIDE, "The shadows peel off the cobbles and run up the street to a pair of taillights; she turns to follow.",
          cast=[P("thug1", 300, 600, 0.26, "open", seed=4111), P("thug2", 340, 590, 0.24, "open", seed=4112),
                P("pam_cat", 200, 740, 0.64, "hero", "surprised", (0.6, -0.6))],
          eyeline="Pam to the taillights", action="the shadows run", reaction="Where are you going?"),
    ]),
    ("02 The witness", [
        S("2.1", "high, over her shoulder", "B_high", WIDE, "Her cat ears in the foreground on the fire escape; below, the car; "
          "the shadows at its rear window; one pale glove points back down the street.",
          cast=[P("thug1", 270, 578, 0.18, "open", seed=4121), P("thug2", 330, 578, 0.18, (-8, 0, 60, -30), seed=4122)],
          protect=[("the car", (300, 560))], standin=True, after=_ears_back, eyeline="down to the car"),
        S("2.2", "medium, through the window", "back_seat", WIDE, "The back seat: the Client, whole; beside him a velvet sleeve, "
          "a ringed hand on a knee, a chin (the window's top cuts Dad at the chin).",
          cast=[P("client", 170, 760, 0.52, "open", "plain", look=(0.7, 0.4), roll=False, badge=False),
                P("father", 380, 760, 0.60, (-20, 30, 20, -30), "hard", (-0.6, 0.6))],
          standin=True, eyeline="both to the envelope"),
        S("2.3", "insert, 1.2 s", "knee", WIDE, "The envelope on his knee; his finger taps it twice; into his coat; the ringed hand flat "
          "on the seat: agreed.", protect=[("envelope", (200, 520)), ("ring", (392, 640))], standin=True,
          line="The Client: Mine until it's done.", action="two taps", reaction="the ringed hand flat: agreed"),
        S("2.4", "close", "B_high", (220, 560, 1.7), "Her eyes narrow; she swings onto the ladder and drops out of frame.",
          cast=[P("pam_cat", 220, 760, 0.62, "hero", "angry", (0.4, 0.6))], line="N: I know where to see what others do not see.",
          standin=True, eyeline="down to the car", action="she drops out of frame", reaction="Got you."),
    ]),
    ("03 Ignored victim", [
        S("3.1", "wide, low", "C_turn", (270, 600, 1.35), "The car swings round at the junction, nose to us; Pam runs onto the crossing after it; "
          "in the middle Don, turned away from her, waves it through.",
          cast=[P("don", 380, 690, 0.46, "wave", "neutral", (0.6, -0.3)),
                P("pam_cat", 130, ROAD_Y, 0.52, "hero", "angry", (0.8, -0.3))],
          protect=[("the car", (250, 600))], line="Don: Traffic flows.", eyeline="Don to the car; Pam to the car",
          action="the car turns; Don waves it on", reaction="Pam runs after it"),
        S("3.2", "same wide, 0.8 s", "C_bump", (270, 600, 1.35), "She sees the headlights, stops, one hand up; the car rolls into her at walking pace: "
          "the bump, stars; she goes over backwards onto the stripes.",
          cast=[P("pam_cat", 250, ROAD_Y + 6, 0.52, HAND_STOP, "surprised", (0, -0.2)),
                P("don", 380, 690, 0.46, "wave", "neutral", (-0.6, -0.3))],
          protect=[("bumper", (250, 690)), ("headlights", (250, 640))], action="the bump", reaction="she goes over backwards"),
        S("3.3", "medium, low", "C_lying", WIDE, "Don walks over, bends, a flat palm on the bumper, rubs one spot, looks at his glove: "
          "clean. Pam's face in the foreground; she lifts one hand off the road, a small wave. He doesn't see it.",
          cast=[P("don", 330, 640, 0.56, DON_REACH, "neutral", (-0.7, 0.6), reach_to=(250, 562), reach_hand=0)],
          protect=[("bumper", (150, 590)), ("Don's palm", (262, 560)), ("her face", (112, 610))],
          line="Don: Not a scratch.", eyeline="Don to the bumper and his glove; Pam to Don",
          action="the palm on the bumper", reaction="her small wave, unseen", after=lying_over),
        S("3.4", "medium", "cabin", WIDE, "Don waves the car on; the rear window opens: the ringed hand drops a fold of bills into the road.",
          protect=[("ring", (211, 480)), ("bills", (200, 620))], line="Dad: For the boys.", action="the bills dropped",
          reaction="(they fall to her)"),
        S("3.5", "low, close", "lying", WIDE, "The bills land on her; the shadows step over her; a pale glove plucks a bill off her coat; "
          "nobody looks down.", protect=[("her face", (112, 610)), ("the glove", (300, 560))],
          eyeline="each shadow to the bills", action="a glove plucks a bill", reaction="nobody looks down"),
        S("3.6", "close", "C", (200, 560, 1.9), "She sits up and pushes her mask straight; her eyes follow the car.",
          cast=[P("pam_cat", 200, 760, 0.62, "sag", "sad", (0.6, -0.3))], line="N: I am like a cat. I have seven lives.",
          eyeline="to the car", action="she sits up", reaction="Six left."),
    ]),
    ("04 False recognition", [
        S("4.1", "wide, low angle", "front", WIDE, "A new place, held: the car parked and empty, the club door, the marquee coming on line "
          "by line; Pam-Cat walks in and stops under it.", cast=[P("pam_cat", 330, 700, 0.50, "hero", "surprised", (0, -1))],
          protect=[("marquee", (270, 340)), ("the car", (150, 680))], line="Pam: There you are.", eyeline="to the car, then up"),
        S("4.2", "insert, top band", "front", (270, 345, 1.15), "The marquee: PAM-CAT · the bulb strip · ONLY FOR YOU.",
          protect=[("marquee", (270, 345))]),
        S("4.3", "medium, under the sign", "front", (300, 520, 1.5), "She points up at the sign, then at herself; turns to show "
          "someone: the street is empty. A small smile anyway; she pats her ears up and pushes the door.",
          cast=[P("pam_cat", 300, 700, 0.50, "point_up", "happy", (0.4, -1))], protect=[("ONLY FOR YOU", (270, 416))],
          eyeline="to the sign, then to nobody", action="the point at the sign, at herself", reaction="Finally."),
    ]),
    ("05 The club", [
        S("5.1", "wide", "hall", WIDE, "Inside: the booth, the game table, the stage at the end. The Client and the ringed hand over the "
          "plan; the spotlight on the empty stage.", eyeline="both to the plan"),
        S("5.2", "insert, 1 s", "plan", WIDE, "The MY GARAGES plan; the ringed hand lays the UPTIMEZ card across the middle and lifts away.",
          protect=[("card", (262, 392)), ("ring", (394, 484))]),
        S("5.3", "medium", "hall", (160, 610, 1.9), "Pam-Cat walks to the booth; her gloved hand goes into the Client's coat and comes out "
          "with the envelope by its edge. Neither man looks up.", cast=[P("pam_cat", 250, 716, 0.46, "lift", "sly", (-0.8, 0.4))],
          line="Pam: Easy.", eyeline="Pam to the coat; the men to the plan", action="the lift", reaction="neither looks up"),
    ]),
    ("06 Ignored star", [
        S("6.1", "medium, low", "stage", WIDE, "She steps into the spotlight and opens the envelope.",
          cast=[P("pam_cat", 230, 700, 0.66, "hero", "proud", (0.3, 0.6), env=True)], standin=True, eyeline="to the envelope"),
        S("6.2", "insert", "cv", WIDE, "Sofia's CV, her photograph.", protect=[("photo", (196, 320))], standin=True),
        S("6.3", "medium wide", "stage", WIDE, "She lifts it high, the triumph pose, and waits; the music stops.",
          cast=[P("pam_cat", 230, 700, 0.66, "triumph", "proud", (0.3, -0.6))], standin=True, line="Pam: Well?",
          protect=[("envelope", (270, 420))], eyeline="out to the room"),
        S("6.4", "insert, 0.7 s", "spot", WIDE, "A pale glove from the top of the frame rests on the spotlight's handle and swings it away.",
          protect=[("glove", (410, 440))], standin=True),
        S("6.5", "wide, held 1 s", "stage_table", WIDE, "The light is on the card table; Pam a black shape against the lit room, arm up.",
          cast=[P("pam_black", 230, 760, 0.66, "triumph", "proud", (0.3, -0.6))], standin=True, eyeline="THE SHOT AND THE COVER"),
        S("6.6", "close, rim-lit", "stage_table", (230, 560, 1.7), "Her arm comes slowly down; she tucks the envelope in and pats it twice.",
          cast=[P("pam_cat", 230, 760, 0.66, "sag", "sad", (0.2, 0.4), env=True)], standin=True, reaction="Of course."),
    ]),
    ("07 Awake", [
        S("7.1", "S6, the counter's end", "desk7", (720, 600, 1.6), "The match: the shape of 6.5. Pam asleep on the counter, the mask "
          "over her eyes, one arm up, the hand open. The lamp, seven cups, the machine.",
          cast=[P("pam_awake", 692, 760, 0.50, "down", "neutral", (0, 0), ARM_UP)], dream=False,
          protect=[("her hand", (713, 660)), ("cups", (730, 650))]),
        S("7.2", "S6", "desk7", (720, 600, 1.6), "Sofia comes round the counter's end mid-step, eyes on her phone; posts the envelope "
          "into Pam's raised hand; sets her mug at the end of the row. Clink. Walks on.",
          cast=[P("pam_awake", 692, 760, 0.50, "down", "neutral", (0, 0), ARM_UP), P("sofia", 600, 806, 0.47, "hold", "neutral", (0.2, 0.7))],
          line="SOFIA: Only for you.", eyeline="Sofia to her phone, never to Pam", after=_sofia_post, dream=False,
          protect=[("envelope", (706, 510))], action="the posting", reaction="the fingers close on it"),
        S("7.3", "close", "desk7", (692, 640, 3.0), "The clink wakes her; she pushes the mask up, ears up; she looks at her hand.",
          cast=[P("pam_awake", 692, 735, 0.50, "up", "surprised", (0.4, -0.6), ARM_UP)], dream=False, eyeline="to her hand"),
        S("7.4", "insert, top band", "rota", WIDE, "INTERNAL MAIL; the COFFEE ROTA: MON to SUN, PAM on every line.",
          protect=[("rota", (270, 300))], dream=False),
        S("7.5", "close, Pam and the sheet", "desk7", (672, 640, 2.6), "Her fingertip goes down the rows to the seventh PAM. Stops. Hold 0.6 s.",
          cast=[P("pam_awake", 692, 735, 0.50, "up", "sad", (-0.3, 0.8), "stand")], after=_rota_held, dream=False,
          protect=[("rota", (650, 584))], eyeline="to the sheet", reaction="Only for me."),
    ]),
    ("08 Back to the dream", [
        S("8.1", "S6", "desk8", (720, 600, 1.6), "She lays the rota over the cups, pulls the mask back down, head on her arm.",
          cast=[P("pam_awake", 692, 764, 0.50, "down", "neutral", (0, 0.4), "stand")], dream=False, reaction="Back to work."),
        S("8.2", "close (push in)", "lampclose", WIDE, "The counter lamp; the room goes dark; rain begins under it. Its head is frame 0's "
          "streetlamp: the loop.", protect=[("lamp", st.A_LAMP)], dream=False),
    ]),
]

KNOWN = {}


def _loc(k, name):
    """draws a location; returns its light function (after the grade) or None."""
    import on4_club as cl
    import on4_lying as ly
    c = k.c
    if name == "A":
        loc_a(k); return st.light_a
    if name == "A_tail":
        loc_a(k, taillights=True); return st.light_a
    if name == "B_high":
        loc_b(k); fire_escape(k); return st.light_b
    if name == "back_seat":
        back_seat(k); return None
    if name == "knee":
        knee_insert(k); return None
    if name in ("C", "C_turn", "C_bump"):
        loc_c(k)
        if name == "C_turn":
            car.c_turn(k)
        if name == "C_bump":
            car.reflect(k, lambda: car.front(k, 250, 700, 0.95), 700, 0.25, 30)
        return lambda c_: (st.light_c(c_), name == "C_bump" and car.glow(c_, "front", 250, 700, 0.95),
                           name == "C_turn" and car.glow_three_q(c_, 250, 640, 0.62, "front"))
    if name == "C_lying":
        st.setup_c(k); ly.ground(k)
        car.front(k, 150, 596, 1.05)                         # her body is drawn after the cast (lying_over): Don behind her
        return st.light_c
    if name == "cabin":
        loc_c(k); car.c_cabin(k); return None
    if name == "lying":
        return "surface"
    if name == "front":
        cl.FRONT_LIGHT[0] = "v7"; cl.front(k, True); return lambda c_: cl.light_front(c_, True)
    if name == "hall":
        cl.HALL_LAMP[0] = "v7"; cl.hall(k); return cl.light_hall
    if name == "plan":
        cl.PLAN_CARD[0] = "v7"; cl.plan_insert(k); return cl.light_inside
    if name == "stage":
        stage(k, "pam"); return lambda c_: ons.vignette(c_, 0.6)
    if name == "stage_table":
        stage(k, "table"); return lambda c_: ons.vignette(c_, 0.5)
    if name == "spot":
        spot_insert(k); return None
    if name == "cv":
        cv_insert(k); return None
    if name == "desk7":
        return "desk7"
    if name == "desk8":
        return "desk8"
    if name == "rota":
        pr.insert74(k); return None
    if name == "lampclose":
        pr.lamp_match(k); return None
    raise ValueError(name)


def _apply(c, cam):
    fx, fy, z = cam
    c.translate(270, 480); c.scale(z, z); c.translate(-fx, -fy)


def _to_screen(cam, p):
    fx, fy, z = cam
    return (270 + (p[0] - fx) * z, 480 + (p[1] - fy) * z)


def _desk(k, sh, eighth):
    """the front desk set at S6 world units: Pam behind the counter, the props, the rest of the cast in front."""
    import fs_set4 as fs4
    import dh_props as dp
    heads = {}
    back = [p for p in sh["cast"] if p[0] == "pam_awake"]
    front = [p for p in sh["cast"] if p[0] != "pam_awake"]
    def pam_over(k_):                                      # over the counter's top, clipped at its front edge: asleep on it
        k_.c.save(); k_.c.rectangle(0, 0, 2000, pr.F - 150); k_.c.clip()
        heads.update(draw_cast(k_, back))
        k_.c.restore()
        if "pam_awake" in heads:
            HANDS["pam_awake"] = heads["pam_awake"]["hands"][1]
    def pam_back(k_):
        pass
    def props(k_):
        pam_over(k_)
        dp.coffee_machine(k_, 770, pr.F - 166, 0.62, "ok")
        pr.counter_lamp(k_, *pr.LAMP)
        pr.cups(k_, eighth=eighth)
        if sh["id"] == "8.1":
            pr.rota(k_, 734, pr.F - 168, 0.30, 0.12)
        heads.update(draw_cast(k_, front))
        if sh["after"]:
            sh["after"](k_)
    fs4.draw_set(k_ := k, {"pam_back": pam_back, "mom_front": props})
    return heads


def render(sh, scale=1):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * scale, H * scale); s.set_device_scale(scale, scale)
    c = cairo.Context(s); k = Ctx(c, 0)
    c.set_source_rgb(*kit.WALL); c.paint()
    heads = {}
    if sh["loc"] == "lying":
        import on4_lying as ly
        src = ly.scene(scale)
        c.set_source_surface(src, 0, 0); c.paint()
        return s, {"pam_cat": {"head": ly.HEAD}}
    c.save(); _apply(c, sh["cam"])
    lit = _loc(k, sh["loc"])
    if lit in ("desk7", "desk8"):
        heads = _desk(k, sh, lit == "desk8")
        lit = None
    else:
        if sh["loc"] == "back_seat":                          # the people clipped to the window (Dad cut at the chin)
            x, y, sc = BS_WIN
            c.save(); c.translate(x, y); c.scale(sc, sc)
            c.new_path(); c.move_to(0, 0); c.line_to(300, 0); c.line_to(300, -140); c.line_to(260, -170); c.line_to(0, -170); c.close_path()
            c.restore(); c.clip()
            heads = draw_cast(k, sh["cast"]); c.reset_clip()
        else:
            heads = draw_cast(k, sh["cast"])
        if sh["after"]:
            sh["after"](k)
    c.restore()
    if sh["dream"]:
        eng.TONE = "v3"; eng.accent_pass(s, [(st.NEON, 1.0), (st.GOLD, 0.35)])
        c2 = cairo.Context(s)
        if lit and sh["cam"] == WIDE:
            lit(c2)
        else:
            ons.vignette(c2, 0.55)
    return s, heads


def checks(sh, heads):
    """faces (where the rig drew them) and the declared story props out of the dead zones."""
    probs = []
    cam = sh["cam"]
    for who, o in heads.items():
        if not o or "head" not in o or who in ("flat",) or who.startswith("thug") or who == "father" and sh["id"] in ("2.2",):
            continue
        x, y = _to_screen(cam, o["head"])
        if -40 < x < 580 and -40 < y < 1000 and DEAD(x, y):
            probs.append("%s: %s's face in a dead zone at (%d, %d)" % (sh["id"], who, x, y))
    for name, p in sh["protect"]:
        x, y = _to_screen(cam, p) if sh["loc"] not in ("lying",) else p
        if DEAD(x, y):
            probs.append("%s: %s in a dead zone at (%d, %d)" % (sh["id"], name, x, y))
    return [p for p in probs if (sh["id"], p) not in KNOWN]


def _timing():
    d = json.load(open(os.path.join(OUT, TIMING)))
    return {s["shot"]: s for s in d["shots"]}, d


def script(out):
    tm, d = _timing()
    L = ["# Office Noir 4: Seven Lives — script v5 (GENERATED from src/on4_scenes.py; do not edit by hand)", "",
         "Length %.2f s (timing %s, narration %s). Changes against v4:" % (d["length"], TIMING, d["narration"]), ""]
    L += ["- " + x for x in CHANGES] + [""]
    for title, shots in SCENES:
        L += ["## " + title, "", "| Shot | Time | Size | Location · camera | What we see | Line | Action → reaction | Eyeline |",
              "|---|---|---|---|---|---|---|---|"]
        for sh in shots:
            t = tm.get(sh["id"], {})
            cam = "" if sh["cam"] == WIDE else " · (%d, %d, ×%.1f)" % sh["cam"]
            L.append("| %s | %.2f +%.2f | %s | %s%s%s | %s | %s | %s → %s | %s |" % (
                sh["id"], t.get("start", 0), t.get("dur", 0), sh["size"], sh["loc"], cam, " (stand-in)" if sh["standin"] else "",
                sh["picture"], sh["line"], sh["action"], sh["reaction"], sh["eyeline"]))
        L.append("")
    open(out, "w").write("\n".join(L))
    return out


def layout_sheet(i, title, shots, out):
    tm, _ = _timing()
    n = len(shots)
    Wd = 20 + n * 290
    sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, max(Wd, 900), 70 + 480 + 200)
    c = cairo.Context(sheet); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(24)
    c.move_to(20, 40); c.show_text("Office Noir 4 · layouts v1 · %s" % title)
    allp = []
    for j, sh in enumerate(shots):
        s, heads = render(sh, 1)
        probs = checks(sh, heads); allp += probs
        x = 20 + j * 290
        c.save(); c.translate(x, 60); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint()
        c.set_source_rgba(1, 0.2, 0.2, 0.18); c.rectangle(0, 720, 540, 240); c.fill(); c.rectangle(470, 380, 70, 340); c.fill()
        c.restore()
        if sh["standin"]:
            c.set_source_rgb(0.85, 0.45, 0.05); c.set_line_width(4); c.rectangle(x, 60, 270, 480); c.stroke()
        t = tm.get(sh["id"], {})
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(16)
        c.move_to(x, 562); c.show_text("%s  %.1f s  %s" % (sh["id"], t.get("dur", 0), sh["size"][:22]))
        c.select_font_face("Inter", 0, 0); c.set_font_size(12)
        yy = 580
        for ln in _wrap(sh["picture"], 44)[:5] + ([sh["line"]] if sh["line"] else []):
            c.move_to(x, yy); c.show_text(ln); yy += 15
        c.set_source_rgb(0.75, 0.1, 0.1) if probs else c.set_source_rgb(0.1, 0.5, 0.2)
        c.select_font_face("Inter", 0, 1); c.set_font_size(13)
        c.move_to(x, yy + 6); c.show_text(("FAIL: " + probs[0][len(sh["id"]) + 2:])[:44] if probs else
                                         "zones OK" + ("  · STAND-IN" if sh["standin"] else ""))
    sheet.write_to_png(out)
    return allp


def _wrap(t, n):
    out, ln = [], ""
    for w in t.split():
        if len(ln) + len(w) + 1 > n:
            out.append(ln); ln = w
        else:
            ln = (ln + " " + w).strip()
    return out + ([ln] if ln else [])


def main(out=OUT):
    probs = []
    print(script(os.path.join(out, "office-noir-4-script-v5.md")))
    for i, (title, shots) in enumerate(SCENES):
        p = os.path.join(out, "on4_layout_s%d_v1.png" % (i + 1))
        probs += layout_sheet(i + 1, title, shots, p)
        print(p)
    for p in probs:
        print("FAIL", p)
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else OUT))


def zones_validate():
    """the zone check must catch a planted fault: Pam's face moved under the buttons, and a prop into the bottom band."""
    import copy
    sh = copy.deepcopy([x for _, ss in SCENES for x in ss if x["id"] == "3.1"][0])
    sh["cast"] = (P("pam_cat", 420, 800, 0.52, "hero", "angry", (0.8, -0.3)),)
    sh["protect"] = (("the car", (250, 790)),)
    _, heads = render(sh, 1)
    probs = checks(sh, heads)
    ok = len(probs) == 2
    print("zones-validate:", "PASS (caught %d)" % len(probs) if ok else "FAIL %s" % probs)
    return ok


# --- the top-down shot plan and the blocking sheet ---------------------------------------------------------------------------
def _cam_icon(c, x, y, ang, lab, col=(0.80, 0.20, 0.10)):
    c.save(); c.translate(x, y); c.rotate(ang)
    c.set_source_rgba(*col, 0.15); c.move_to(0, 0); c.line_to(70, -34); c.line_to(70, 34); c.close_path(); c.fill()
    c.set_source_rgb(*col); c.rectangle(-12, -9, 18, 18); c.fill(); c.move_to(6, -6); c.line_to(16, -12); c.line_to(16, 12); c.line_to(6, 6); c.fill()
    c.restore()
    c.set_source_rgb(*col); c.select_font_face("Inter", 0, 1); c.set_font_size(13); c.move_to(x - 14, y + 26); c.show_text(lab)


def _mark(c, x, y, lab, col):
    c.set_source_rgb(*col); c.new_path(); c.arc(x, y, 9, 0, 2 * math.pi); c.fill()
    c.select_font_face("Inter", 0, 1); c.set_font_size(13); c.move_to(x + 12, y + 5); c.show_text(lab)


def _box(c, x, y, w, h, lab, fill=(0.85, 0.83, 0.78)):
    c.set_source_rgb(*fill); c.rectangle(x, y, w, h); c.fill_preserve(); c.set_source_rgb(0.2, 0.2, 0.2); c.set_line_width(1.5); c.stroke()
    c.select_font_face("Inter", 0, 0); c.set_font_size(12); c.set_source_rgb(0.15, 0.15, 0.15); c.move_to(x + 4, y + 15); c.show_text(lab)


PAM_C, DON_C, CAR_C, SOF_C, SHAD_C = (0.45, 0.25, 0.55), (0.13, 0.16, 0.30), (0.1, 0.1, 0.1), (0.85, 0.45, 0.55), (0.4, 0.4, 0.4)


def shotplan(out):
    tm, _ = _timing()
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, 1800, 1500); c = cairo.Context(sh)
    c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 40); c.show_text("Office Noir 4 · shot plan v1 (top down: locations, cameras, who stands where)")
    def panel(x0, y0, title):
        c.set_source_rgb(1, 1, 1); c.rectangle(x0, y0, 400, 420); c.fill()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(16); c.move_to(x0 + 10, y0 + 22); c.show_text(title)
    # A: the lane (1.1-1.4, 8.2 lands here)
    x0, y0 = 20, 60; panel(x0, y0, "A  the lane (frame 0, 1.1-1.4; 8.2 lands on it)")
    _box(c, x0 + 40, y0 + 40, 70, 340, "houses"); _box(c, x0 + 290, y0 + 40, 70, 340, "houses")
    _mark(c, x0 + 270, y0 + 130, "streetlamp", (0.9, 0.7, 0.1)); _mark(c, x0 + 270, y0 + 170, "heart", (0.9, 0.1, 0.2))
    _mark(c, x0 + 170, y0 + 290, "Pam-Cat", PAM_C); _mark(c, x0 + 210, y0 + 250, "Sofia (1.1) -> past camera (1.2)", SOF_C)
    _mark(c, x0 + 200, y0 + 90, "taillights (1.4)", (0.9, 0.1, 0.2))
    _cam_icon(c, x0 + 200, y0 + 390, -math.pi / 2, "1.1 1.2 1.4 (low)"); _cam_icon(c, x0 + 120, y0 + 350, -1.2, "1.3")
    # B: the lane's end, from the fire escape
    x0 = 440; panel(x0, y0, "B  the lane's end (2.1, 2.4; stand-in fire escape)")
    _box(c, x0 + 40, y0 + 40, 70, 340, "houses"); _box(c, x0 + 290, y0 + 40, 70, 340, "wall")
    _box(c, x0 + 170, y0 + 70, 60, 30, "the car", (0.3, 0.3, 0.3)); _mark(c, x0 + 160, y0 + 120, "shadows", SHAD_C)
    _box(c, x0 + 40, y0 + 330, 120, 20, "fire escape", (0.2, 0.2, 0.2)); _mark(c, x0 + 100, y0 + 320, "Pam-Cat", PAM_C)
    _cam_icon(c, x0 + 110, y0 + 380, -math.pi / 2, "2.1 high, 2.4")
    # C: the crossing
    x0 = 860; panel(x0, y0, "C  the crossing (3.1-3.6)")
    _box(c, x0 + 110, y0 + 40, 180, 340, "road", (0.75, 0.73, 0.70))
    for i in range(7):
        c.set_source_rgb(1, 1, 1); c.rectangle(x0 + 116 + i * 25, y0 + 250, 14, 50); c.fill()
    _mark(c, x0 + 200, y0 + 70, "junction: the car turns", CAR_C); _mark(c, x0 + 250, y0 + 220, "Don", DON_C)
    _mark(c, x0 + 160, y0 + 275, "Pam lands", PAM_C)
    _cam_icon(c, x0 + 200, y0 + 395, -math.pi / 2, "3.1 3.2 (low wide)"); _cam_icon(c, x0 + 60, y0 + 320, -0.5, "3.3 3.5 3.6")
    # the club front
    x0 = 1280; panel(x0, y0, "the club front (4.1-4.3)")
    _box(c, x0 + 30, y0 + 50, 340, 60, "facade, the marquee over the arch"); _box(c, x0 + 160, y0 + 110, 80, 50, "arch")
    _box(c, x0 + 60, y0 + 200, 130, 40, "the car, parked", (0.3, 0.3, 0.3)); _mark(c, x0 + 250, y0 + 190, "Pam-Cat", PAM_C)
    _cam_icon(c, x0 + 200, y0 + 390, -math.pi / 2, "4.1 low; 4.2; 4.3")
    # the hall
    x0, y0 = 20, 500; panel(x0, y0, "the hall (5.1, 5.3; the stage 6.x is a stand-in)")
    _box(c, x0 + 40, y0 + 240, 140, 80, "booth: Client, Dad"); _box(c, x0 + 220, y0 + 220, 110, 70, "game table, 2 shadows")
    _box(c, x0 + 150, y0 + 40, 100, 50, "stage, spotlight"); _mark(c, x0 + 200, y0 + 260, "Pam-Cat (5.3)", PAM_C)
    _cam_icon(c, x0 + 200, y0 + 395, -math.pi / 2, "5.1"); _cam_icon(c, x0 + 330, y0 + 360, -2.4, "5.3")
    # the stage
    x0 = 440; panel(x0, y0, "the stage (6.1-6.6, stand-in)")
    _box(c, x0 + 40, y0 + 60, 320, 30, "curtain"); _box(c, x0 + 40, y0 + 90, 320, 120, "boards")
    _mark(c, x0 + 150, y0 + 150, "Pam-Cat", PAM_C); _mark(c, x0 + 320, y0 + 140, "spotlight", (0.9, 0.7, 0.1))
    _box(c, x0 + 120, y0 + 280, 160, 50, "card table (lit in 6.5)")
    _cam_icon(c, x0 + 150, y0 + 260, -math.pi / 2, "6.1 6.3 6.6 (from the room)", (0.8, 0.2, 0.1))
    # the desk
    x0 = 860; panel(x0, y0, "front desk, zone C (7.1-8.2), setup S6")
    _box(c, x0 + 60, y0 + 90, 290, 50, "counter: lamp · Pam · cups · machine")
    _mark(c, x0 + 110, y0 + 70, "Pam (behind)", PAM_C); _mark(c, x0 + 40, y0 + 190, "Sofia: round the end, posts, walks on", SOF_C)
    _cam_icon(c, x0 + 200, y0 + 380, -math.pi / 2, "S6: 7.1 7.2 8.1"); _cam_icon(c, x0 + 330, y0 + 260, -2.2, "7.3 7.5 8.2 (push)")
    # the table
    x0, y0 = 1280, 500
    c.set_source_rgb(1, 1, 1); c.rectangle(x0, y0, 500, 960); c.fill()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(15); c.move_to(x0 + 10, y0 + 22)
    c.show_text("shot · location · size · time")
    c.select_font_face("Inter", 0, 0); c.set_font_size(12.5)
    yy = y0 + 44
    for title, shots in SCENES:
        for s_ in shots:
            t = tm.get(s_["id"], {})
            c.set_source_rgb(0.75, 0.35, 0.0) if s_["standin"] else c.set_source_rgb(0.1, 0.1, 0.1)
            c.move_to(x0 + 10, yy); c.show_text("%-4s  %-11s  %-24s  %5.2f +%.1f" % (s_["id"], s_["loc"], s_["size"][:24], t.get("start", 0), t.get("dur", 0)))
            yy += 17
    c.set_source_rgb(0.75, 0.35, 0.0); c.move_to(x0 + 10, yy + 14); c.show_text("orange: stand-in location, not drawn yet")
    # time by zone
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(16); c.move_to(20, 960); c.show_text("time by location (s)")
    order = ["A", "A_tail", "B_high", "back_seat", "knee", "C_turn", "C_bump", "C_lying", "cabin", "lying", "C", "front", "hall", "plan", "stage", "cv", "spot", "stage_table", "desk7", "rota", "desk8", "lampclose"]
    total = sum(t["dur"] for t in tm.values())
    for title, shots in SCENES:
        for s_ in shots:
            t = tm.get(s_["id"], {})
            x = 20 + t.get("start", 0) / total * 1240; w = t.get("dur", 0) / total * 1240
            row = order.index(s_["loc"])
            c.set_source_rgb(0.75, 0.35, 0.0) if s_["standin"] else c.set_source_rgb(0.25, 0.35, 0.55)
            c.rectangle(x, 980 + row * 20, w - 1, 16); c.fill()
    c.select_font_face("Inter", 0, 0); c.set_font_size(11); c.set_source_rgb(0.2, 0.2, 0.2)
    for i, n in enumerate(order):
        c.move_to(1266 - 0, 992 + i * 20) if False else c.move_to(20 + 1244 - 0, 992 + i * 20)
    sh.write_to_png(out)
    return out


def blocking(out):
    """3.1-3.3, the hardest beat, top down in three moments, and the two camera frames."""
    by = {x["id"]: x for _, ss in SCENES for x in ss}
    sh = cairo.ImageSurface(cairo.FORMAT_RGB24, 1700, 1100); c = cairo.Context(sh)
    c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(26)
    c.move_to(20, 40); c.show_text("Office Noir 4 · blocking v1 · 3.1-3.3: the turn, the bump, the palm on the bumper")
    moments = [("3.1  the car turns at the junction; Don waves it on; Pam runs onto the crossing",
                dict(car=(200, 110, "turning"), don=(250, 230), pam=(120, 300), path_car=[(330, 60), (260, 80), (200, 120), (200, 240)],
                     path_pam=[(40, 300), (120, 300)])),
               ("3.2  the headlights; one hand up; the bump at walking pace; she goes over backwards",
                dict(car=(200, 250, "at the crossing"), don=(290, 220), pam=(200, 300), path_pam=[(200, 300), (200, 340)])),
               ("3.3  Don walks to the bumper, bends, palm on it, checks his glove; her small wave",
                dict(car=(200, 250, "stopped"), don=(270, 290), pam=(200, 350), path_don=[(290, 220), (270, 290)]))]
    for i, (lab, m) in enumerate(moments):
        x0, y0 = 20 + i * 420, 70
        c.set_source_rgb(1, 1, 1); c.rectangle(x0, y0, 400, 440); c.fill()
        _box(c, x0 + 110, y0 + 30, 180, 380, "", (0.75, 0.73, 0.70))
        for j in range(7):
            c.set_source_rgb(1, 1, 1); c.rectangle(x0 + 116 + j * 25, y0 + 280, 14, 50); c.fill()
        cx, cy, st_ = m["car"]
        c.set_source_rgb(*CAR_C); c.rectangle(x0 + cx - 30, y0 + cy - 55, 60, 110); c.fill()
        c.set_source_rgb(1, 1, 0.6); c.rectangle(x0 + cx - 26, y0 + cy + 50, 14, 5); c.fill(); c.rectangle(x0 + cx + 12, y0 + cy + 50, 14, 5); c.fill()
        for key, col in (("path_car", CAR_C), ("path_pam", PAM_C), ("path_don", DON_C)):
            if key in m:
                c.set_source_rgb(*col); c.set_line_width(3); c.set_dash([8, 5]); pts = m[key]
                c.move_to(x0 + pts[0][0], y0 + pts[0][1])
                for q in pts[1:]:
                    c.line_to(x0 + q[0], y0 + q[1])
                c.stroke(); c.set_dash([])
        _mark(c, x0 + m["don"][0], y0 + m["don"][1], "Don", DON_C); _mark(c, x0 + m["pam"][0], y0 + m["pam"][1], "Pam", PAM_C)
        _cam_icon(c, x0 + 200, y0 + 430, -math.pi / 2, "camera, low")
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 0); c.set_font_size(13)
        yy = y0 + 470
        for ln in _wrap(lab, 52):
            c.move_to(x0, yy); c.show_text(ln); yy += 17
    for i, sid in enumerate(("3.1", "3.2", "3.3")):
        s, _ = render(by[sid], 1)
        x0 = 1280 if i == 0 else 1280
        c.save(); c.translate(20 + i * 420 + 65, 610); c.scale(0.5, 0.5); c.set_source_surface(s, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(15)
        c.move_to(20 + i * 420 + 340, 640); c.show_text(sid)
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 0); c.set_font_size(14)
    for j, ln in enumerate(_wrap("Rules held: the same cast on both sides of each cut (Pam, Don, the car). Don never looks at "
                                 "her: his eyelines go to the car, the bumper, his glove. The bump at walking pace, with a pause "
                                 "before and after (lesson 158). Her face, the bumper and his palm above y 720.", 34)):
        c.move_to(1290, 120 + j * 20); c.show_text(ln)
    sh.write_to_png(out)
    return out
