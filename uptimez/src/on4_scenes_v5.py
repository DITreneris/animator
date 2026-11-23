"""OFFICE NOIR 4: SEVEN LIVES, the scene file, v5 = board v2 (23 Nov; v1-v4 pinned). After the board's G4 (2 of 5) and
Tomas's picks: 5.2 cut (its second to the lift); the envelope's journey in inserts (2.3 on his knee, 2.3b into his coat,
5.3b her glove draws it out of his coat); 6.2 Sofia's photograph big (the face from 1.2); 6.5 the beam swinging from her
to the card table, seen whole, the room's backs to her; Sofia holds her phone, not a clipboard. v4 = board v1: After the layout review ("Tobulinam"):
the blocking sheet is generated from the shots' own positions; 3.1-3.2 closer (1.5); 3.2 her silhouette lit from behind by
the headlights, an impact burst at her knees, her palm open; 3.3 in two keys (3.3a the glove flat on the bonnet at the car's
visible front corner, 3.3b the glove up at his eye) and her small wave; 3.4 the rear door reads (the wheel arch, the tail
lamp); 3.6 she sits up, a hand to her mask; the CV drawn. v3 (23 Nov): v3: Don the traffic cop v4b (on4_cast.don_cop2: the
cap, the shield, the STOP / GO paddle; Tomas: "more serious, and a comic prop"). 3.1: STOP flashed at Pam's side, GO to the
car, she stops dead in its path. 3.2: GO raised to the car as it rolls into her. 3.3: Don on the far side of the car, his
back to her, the car between them, his glove on the bonnet, his eyes on it (cold test v2: he read as helping her).
v2 (23 Nov): v2, Tomas's picks at stop 3:
3.2-3.3 restaged after the cold test (0 of 4 read: the bump unseen, Don read as blaming her): 3.2 Pam from behind facing the
headlights, the bumper at her knees, tipping back; 3.3 the bumper right over her head, Don bent to it, palm flat, eyes on
his glove. Don's crossbelt dropped (read as a wand). The crossing lamp's post lit (its heads read as headlights, eyes).
Bigger characters in the wides and at S6. The stage, the back seat and the fire escape drawn (no longer stand-ins).
v1 (stage 4, series/production-process.md, 23 Nov). From here on this file
is the episode: every shot with its time and line, its location and camera, who is in frame and where, the props that
must stay out of the dead zones, the action and the reaction. Generated from it, never edited by hand:

  python3 on4_scenes.py [out]  ->  office-noir-4-script-v6.md     the script (generated)
                                   on4_layout_s<N>_v2.png          a layout sheet per beat: every shot at 270, with its checks
                                   on4_shotplan_v2.png             the top-down shot plan (locations, cameras, the table)
                                   on4_blocking_v2.png             the blocking sheet for the hardest beat (3.2-3.3)
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
    "board v2: 5.2 cut (5.3 +1.0 s); the envelope's journey in inserts (2.3, 2.3b, 5.3b); 6.2 Sofia's photograph big; 6.5 the beam seen leaving her for the card table; Sofia's phone.",
    "board v1: 3.1-3.2 closer; 3.2 lit from behind, the impact at her knees, her palm open; 3.3 in two keys (glove on the bonnet, glove at his eye) and her small wave; 3.4 the rear door reads; 3.6 she sits up, a hand to her mask.",
    "v3: Don the traffic cop with the STOP / GO paddle; 3.1 STOP at Pam's side, GO to the car, so she stops in its path; 3.3 Don on the far side of the car, the car between them.",
    "v2 (stop 3): 3.2-3.3 restaged after the cold test; Don's crossbelt dropped; the crossing lamp's post lit; bigger characters in the wides and at S6; the stage, the back seat and the fire escape drawn.",
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
    st.ZEBRA[0] = "v6"; st.C_POST[0] = "v7"
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


BS_WIN = (20, 700, 1.66)                                      # the window's bottom left and scale (car.cabin)


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
    """6.2 (board v2): Sofia's CV, her photograph big: the face that walked past Pam in 1.2 (the dream's drawing, lesson 160)."""
    import sofia_dh as sd
    c = k.c
    c.set_source_rgb(0.10, 0.08, 0.08); c.paint()
    kit.cut(k, [(70, 150), (470, 140), (478, 690), (78, 700)], (0.99, 0.98, 0.95), shadow=False, lw=2.2)
    kit.text(k, "CURRICULUM VITAE", 274, 196, 24, INK, bold=True)
    kit.cut(k, [(120, 226), (424, 220), (428, 560), (124, 566)], (0.86, 0.84, 0.80), shadow=False, lw=2)
    c.save(); c.new_path(); c.move_to(120, 226); c.line_to(424, 220); c.line_to(428, 560); c.line_to(124, 566); c.close_path(); c.clip()
    c.push_group(); o = sd.sofia(k, 0, 0, 1.9, "hold", "smile", (0, 0), tablet_kind=None); c.pop_group()
    hx, hy = o["head"]                                       # put her face in the middle of the photograph
    sd.sofia(k, 274 - hx, 400 - hy, 1.9, "hold", "smile", (0, 0), tablet_kind=None); c.restore()
    kit.text(k, "SOFIA", 274, 612, 40, INK, bold=True)
    for i in range(3):
        c.set_source_rgb(0.6, 0.6, 0.62); c.set_line_width(3); c.move_to(130, 640 + i * 18); c.line_to(420 - i * 40, 640 + i * 18); c.stroke()


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


def knee_coat(k, env=True, hand=True):
    """2.3b: the Client's coat open, the envelope half into the inside pocket, his hand flat on it."""
    c = k.c
    c.set_source_rgb(0.10, 0.10, 0.11); c.paint()
    st.poly(k, [(40, 120), (520, 120), (520, 900), (40, 900)], (0.20, 0.22, 0.28), 2.4)          # his coat, close
    st.poly(k, [(150, 120), (300, 120), (280, 760), (200, 760)], (0.95, 0.95, 0.93), 2.0)        # the shirt
    st.poly(k, [(300, 120), (470, 300), (420, 900), (280, 760)], (0.16, 0.17, 0.22), 2.4)        # the lapel held open
    st.poly(k, [(300, 380), (440, 380), (436, 420), (300, 420)], (0.08, 0.08, 0.10), 1.6)        # the pocket's mouth
    if env:
        oc.envelope(k, 360, 360, 2.4)                                                             # half in
    st.poly(k, [(296, 400), (444, 400), (440, 520), (300, 520)], (0.16, 0.17, 0.22), 2.0)        # the pocket over it
    if hand:
        kit.ellipse(k, 250, 460, 60, 40, (0.87, 0.70, 0.58), 7111, shadow=False, lw=2.2)          # his hand, patting


def coat_lift(k):
    """5.3b: the same coat, in the club light; her black glove draws the envelope out by its edge."""
    import hands_ps as hp
    knee_coat(k, env=False, hand=False)
    c = k.c
    oc.envelope(k, 330, 330, 2.4)                                                                 # out of the pocket, by its edge
    hp.draw(k, "grab", 380, 270, 70, oc.GLOVE_DARK, (0.6, -0.8), 1)


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



# --- v2: the locations drawn (were stand-ins) -------------------------------------------------------------------------------
VELV = (0.36, 0.08, 0.12)


def stage_front(k, lit=True):
    """6.1 / 6.3, from the room: the velvet curtain, the boards with a strip of bulbs on their edge, the spotlight on its
    stand at stage right, its cone on her (lit) or swung away (dark)."""
    c = k.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.paint()
    for i, x in enumerate(range(-20, 560, 40)):              # the curtain's folds
        g = cairo.LinearGradient(x, 0, x + 40, 0)
        g.add_color_stop_rgb(0, *[v * 0.55 for v in VELV]); g.add_color_stop_rgb(0.5, *VELV); g.add_color_stop_rgb(1, *[v * 0.55 for v in VELV])
        c.set_source(g); c.rectangle(x, 0, 40, 640); c.fill()
    st.poly(k, [(-10, 0), (550, 0), (550, 70), (-10, 70)], (0.22, 0.05, 0.08), 2.0)            # the pelmet
    for i in range(14):
        st.bulb(c, 20 + i * 39, 60, 4)
    st.poly(k, [(-10, 640), (550, 640), (550, 700), (-10, 700)], (0.45, 0.32, 0.20), 2.2)       # the boards
    for x in range(0, 540, 60):
        c.set_source_rgb(0.30, 0.20, 0.12); c.set_line_width(1.4); c.move_to(x, 640); c.line_to(x - 20, 700); c.stroke()
    for i in range(16):                                      # the footlights on the edge
        st.bulb(c, 14 + i * 34, 704, 4)
    st.poly(k, [(-10, 710), (550, 710), (550, 960), (-10, 960)], (0.06, 0.06, 0.07), 1.5)
    c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(466, 640); c.line_to(466, 330); c.stroke()   # the stand
    c.move_to(440, 640); c.line_to(492, 640); c.stroke()
    st.poly(k, [(430, 300), (494, 312), (486, 352), (424, 338)], (0.22, 0.22, 0.24), 2.0)       # the lamp
    c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(488, 330); c.line_to(512, 330); c.stroke()   # its handle
    if lit:
        c.set_source_rgba(1, 1, 0.92, 0.28)
        c.move_to(428, 322); c.line_to(90, 700); c.line_to(360, 700); c.line_to(432, 344); c.close_path(); c.fill()
        c.save(); c.translate(225, 690); c.scale(130, 16)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 1); g.add_color_stop_rgba(0, 1, 1, 0.92, 0.55); g.add_color_stop_rgba(1, 1, 1, 0.92, 0)
        c.set_source(g); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()


def room_reverse(k, beam=False):
    """6.5 / 6.6, from behind her on the stage, into the room: the swung spotlight's pool on the card table, the two
    shadows dealing, the booth's velvet wall with its neon line behind them, the Client and the ringed hand over the plan."""
    import client_ob as co
    import dh_cast as dc
    c = k.c
    c.set_source_rgb(0.05, 0.05, 0.06); c.paint()
    st.poly(k, [(-10, 200), (550, 200), (550, 620), (-10, 620)], (0.20, 0.06, 0.09), 1.8)      # the booth wall, velvet
    for x in range(10, 540, 28):
        c.set_source_rgb(0.28, 0.08, 0.12); c.rectangle(x, 210, 16, 400); c.fill()
    c.set_source_rgb(*st.NEON); c.set_line_width(4); c.move_to(-10, 236); c.line_to(550, 236); c.stroke()
    g = cairo.RadialGradient(290, 520, 10, 290, 520, 260)                                          # the pool on the table
    g.add_color_stop_rgba(0, 1, 1, 0.92, 0.85); g.add_color_stop_rgba(0.6, 1, 1, 0.92, 0.35); g.add_color_stop_rgba(1, 1, 1, 0.92, 0)
    c.set_source(g); c.rectangle(0, 200, 540, 520); c.fill()
    co.client(k, 120, 600, 0.40, "open", "plain", look=(0.6, 0.6), roll=False, badge=False)
    st.poly(k, [(560, 540), (440, 556), (444, 600), (560, 600)], dc.VELVET, 2.2)                # only Dad's cuff and ring
    kit.ellipse(k, 420, 574, 36, 24, dc.SKIN_F, 7401, shadow=False, lw=2.0); dc.ring(k, 414, 566, 1.1)
    for x in (220, 360):
        st.thug(k, x, 640, 0.34, (-40, 60, 40, -60), seed=4800 + x, hands=("relax", "relax"))
    st.poly(k, [(170, 560), (410, 560), (420, 584), (160, 584)], (0.10, 0.10, 0.11), 2.0)       # the card table
    for i, x in enumerate((210, 250, 300, 350)):
        st.poly(k, [(x, 556), (x + 22, 556), (x + 24, 566), (x - 2, 566)], (0.97, 0.97, 0.95), 1.0)
    if beam:                                                 # board v2: the beam itself, from the lamp on the stage behind her
        c.set_source_rgba(1, 1, 0.92, 0.32)                  # (top left, the glove on its handle) down onto the card table
        c.move_to(40, 60); c.line_to(150, 560); c.line_to(420, 560); c.line_to(80, 40); c.close_path(); c.fill()
        st.poly(k, [(10, 20), (96, 30), (88, 84), (4, 70)], (0.22, 0.22, 0.24), 2.0)            # the lamp, swung away
        import hands_ps as hp
        hp.draw(k, "grab", 100, 40, 40, st.GLOVE, (0.0, 1.0), 1)
    st.poly(k, [(-10, 700), (550, 700), (550, 960), (-10, 960)], (0.30, 0.21, 0.13), 2.0)       # the stage's boards, ours
    for i in range(16):
        st.bulb(c, 14 + i * 34, 704, 4)


def lane_above(k):
    """2.1, high: down from the fire escape into the lane. The cobbles running away, the car's roof from above (its rear
    window down, two bare heads and a pale glove at it), the iron grating in the foreground."""
    c = k.c
    c.set_source_rgb(0.10, 0.10, 0.11); c.paint()
    st.poly(k, [(60, 200), (480, 200), (540, 960), (0, 960)], st.ROAD, 2.0)                    # the lane, from above
    st.setts(k, lambda: (c.new_path(), c.move_to(60, 200), c.line_to(480, 200), c.line_to(540, 960), c.line_to(0, 960), c.close_path()),
             200, 960, 60, 480, 0, 540, seed=88)
    st.poly(k, [(-10, 0), (60, 200), (0, 960), (-10, 960)], st.CREAM_SH, 2.0)                  # the walls
    st.poly(k, [(550, 0), (480, 200), (540, 960), (550, 960)], st.CREAM_SH, 2.0)
    cx, cy = 300, 470                                                                          # the car from above
    car._rr(c, cx - 70, cy - 160, 140, 320, 40); car._fs(c, car.BODY, 2.4)
    car._rr(c, cx - 56, cy - 110, 112, 60, 12); car._fs(c, car.GLASS, 1.6)                     # the windscreen
    car._rr(c, cx - 58, cy - 40, 116, 120, 16); car._fs(c, (0.10, 0.10, 0.12), 1.6)            # the roof
    car._rr(c, cx - 56, cy + 86, 112, 50, 12); car._fs(c, car.GLASS, 1.6)                      # the rear glass
    for sx in (-1, 1):
        c.set_source_rgb(*st.NEON); c.rectangle(cx + sx * 56 - 6, cy + 156, 12, 6); c.fill()  # the taillights
    for (hx, hy) in ((cx + 96, cy + 40), (cx + 112, cy + 80)):                                 # two bare heads at its window
        kit.ellipse(k, hx, hy, 34, 30, (0.04, 0.04, 0.05), int(hx), shadow=False, lw=1.6)
    import hands_ps as hp
    hp.draw(k, "point", cx + 70, cy + 60, 34, st.GLOVE, (0.0, 1.0), -1)                        # one glove points down the lane
    c.set_source_rgb(*INK)                                                                     # the grating, ours
    for i in range(-4, 16):
        c.set_line_width(5); c.move_to(-20 + i * 44, 960); c.line_to(140 + i * 44, 640); c.stroke()
    c.set_line_width(10); c.move_to(-10, 640); c.line_to(560, 640); c.stroke()


def fire_escape_close(k):
    """2.4, close: her on the fire escape; the brick wall and a dark window behind, the railing at her waist, the ladder."""
    c = k.c
    c.set_source_rgb(0.30, 0.28, 0.27); c.paint()
    for row in range(0, 30):
        y = row * 32
        for col in range(-1, 12):
            x = col * 64 + (32 if row % 2 else 0)
            c.set_source_rgb(0.20, 0.19, 0.18); c.set_line_width(2); c.rectangle(x, y, 64, 32); c.stroke()
    st.poly(k, [(300, 150), (470, 150), (470, 420), (300, 420)], (0.05, 0.05, 0.06), 2.4)       # a dark window
    c.set_source_rgb(0.4, 0.4, 0.42); c.set_line_width(3); c.move_to(385, 150); c.line_to(385, 420); c.stroke()


def railing(k, y=640):
    c = k.c
    c.set_source_rgb(*INK)
    c.rectangle(-10, y - 6, 560, 12); c.fill(); c.rectangle(-10, y + 70, 560, 14); c.fill()
    for x in range(10, 550, 34):
        c.rectangle(x, y, 5, 80); c.fill()
    c.set_line_width(6); c.move_to(80, 0); c.line_to(80, y + 90); c.stroke(); c.move_to(130, 0); c.line_to(130, y + 90); c.stroke()
    for yy in range(20, y, 40):
        c.move_to(80, yy); c.line_to(130, yy); c.stroke()


def back_seat2(k):
    """2.2: the rear door from outside, window down, the cabin lit warm: cream seats, starlit roof; the people are drawn
    inside the window (clipped), the window's top edge cuts Dad at the chin; his ringed hand on the seat between them."""
    car.cabin(k, 20, 700, 1.66, 1.0, hand=False)


# --- the cast, in frame units ----------------------------------------------------------------------------------------------
def P(who, *a, **kw):
    return (who, a, kw)


ARM_UP = (-8, 0) + oc.pm.ik(1, 30, oc.HY - 150)             # 7.1 / 6.5: one arm up on its elbow, the hand open
HAND_STOP = (-8, 0) + oc.pm.ik(1, 80, oc.HY + 10)          # 3.2: one hand up at the headlights
oc.CAT_POSES.setdefault("stop_palm", (HAND_STOP, ("relax_s", "palm")))      # board v1: the palm open at the car
oc.CAT_POSES.setdefault("mask_fix", ((-8, 0) + oc.pm.ik(1, 34, oc.HY - 6), ("relax_s", "point")))   # 3.6: a finger to the mask
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
        kw = dict(kw); lean = kw.pop("lean", 0.0)
        if lean:
            k.c.save(); k.c.translate(a[0], a[1]); k.c.rotate(lean); k.c.translate(-a[0], -a[1])
        if who == "pam_cat":
            cy = kw.pop("clip_y", None)
            if cy is not None:                               # 3.6: sitting: only her top half rises from the road
                k.c.save(); k.c.rectangle(-2000, -2000, 5000, cy + 2000); k.c.clip()
            o = oc.pam_cat(k, *a, **kw)
            if cy is not None:
                k.c.restore()
        elif who == "pam_from_behind":                       # her back to us: the figure, the face covered by the back of
            o = oc.pam_cat(k, *a, **kw)                      # the head (her dark bob) and the ears
            hx, hy = o["head"]; s_ = a[2]
            kit.ellipse(k, hx, hy - 4 * s_, 62 * s_, 58 * s_, (0.14, 0.12, 0.14), 7301, shadow=False, lw=2.4)
            oc.ears(k, hx, hy, s_)
        elif who == "pam_black":                             # 6.5: a black shape against the lit wall
            c = k.c
            c.push_group(); o = oc.pam_cat(k, *a, **kw); g = c.pop_group()
            c.set_source_rgb(0.03, 0.03, 0.04); c.mask(g)
        elif who == "pam_awake":
            o = oc.pam_awake(k, *a, **kw)
        elif who == "don":
            clip_y = kw.pop("clip_y", None)
            if clip_y is not None:                           # behind the car: only what shows above its bonnet
                k.c.save(); k.c.rectangle(-2000, -2000, 5000, clip_y + 2000); k.c.clip()
            o = oc.don_cop2(k, *a, **kw)
            if clip_y is not None:
                k.c.restore()
        elif who == "sofia":                                  # board v2: her phone, not the clipboard (read as one)
            kw.setdefault("tablet_kind", None)
            o = sd.sofia(k, *a, **kw)
            hx, hy = o["hands"][1]; s_ = a[2]
            car._rr(k.c, hx - 9 * s_ * 2, hy - 30 * s_ * 2, 18 * s_ * 2, 32 * s_ * 2, 4 * s_ * 2); car._fs(k.c, (0.10, 0.10, 0.12), 1.6)
            car._rr(k.c, hx - 7 * s_ * 2, hy - 27 * s_ * 2, 14 * s_ * 2, 24 * s_ * 2, 3 * s_ * 2); k.c.set_source_rgb(0.75, 0.88, 1.0); k.c.fill()
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
        if lean:
            k.c.restore()
            if o and "head" in o:                           # the rig's points, rotated with the figure
                ca, sa = math.cos(lean), math.sin(lean)
                def rot(p):
                    dx, dy = p[0] - a[0], p[1] - a[1]
                    return (a[0] + dx * ca - dy * sa, a[1] + dx * sa + dy * ca)
                o = dict(o); o["head"] = rot(o["head"])
                if "hands" in o:
                    o["hands"] = [rot(h) for h in o["hands"]]
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
    kit.ellipse(k, 96, 660, 150, 140, (0.10, 0.09, 0.10), 7201, shadow=False, lw=2.4)
    oc.ears(k, 96, 660, 1.6)


HANDS = {}


def _sofia_post(k):                                        # 7.2: the envelope going into Pam's raised hand (her rig's hand)
    hx, hy = HANDS.get("pam_awake", (706, 510))
    pr.envelope(k, hx + 4, hy - 26, 0.28, 0.3)


def _rota_held(k):                                         # 7.5: the sheet in her hands, close
    pr.rota(k, 706, 668, 0.28, -0.05)                      # held low in her hands, under her face


def lying_over(k):                                         # 3.3: her body over Don's feet (he stands behind her)
    import on4_lying as ly
    ly.body(k); ly.head(k, *ly.HEAD, ly.ANG)


def _impact(k, x, y):                                      # 3.2: the bump: stars round her head, two impact lines
    import on4_lying as ly
    ly.stars(k.c, x, y, 1.0, 0.0)
    c = k.c; c.set_source_rgb(1, 1, 1); c.set_line_width(4)
    for dx, dy in ((-70, 150), (70, 150), (-90, 110), (90, 110)):
        c.move_to(x + dx * 0.8, y + dy); c.line_to(x + dx, y + dy + 30); c.stroke()


def _burst(k, x, y, r=26):                                 # the impact: a white jagged star where the bumper meets her
    c = k.c; c.new_path()
    for i in range(16):
        a = i * math.pi / 8; rr = r if i % 2 == 0 else r * 0.45
        (c.move_to if i == 0 else c.line_to)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path(); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()


def _wave(k):                                              # 3.3b: her flung hand lifts off the road, open: a small wave
    import on4_lying as ly
    import hands_ps as hp
    x0, y = ly.HEAD[0] + 34, ly.BACK_Y
    hp.draw(k, "palm", x0 - 104, y - 26, 30, oc.GLOVE_DARK, (0.0, -1.0), -1)
    c = k.c; c.set_source_rgb(1, 1, 1); c.set_line_width(3)
    for dx in (-22, 22):
        c.move_to(x0 - 104 + dx, y - 50); c.line_to(x0 - 104 + dx * 1.4, y - 62); c.stroke()


def _sit_legs(k):                                          # 3.6: sitting: her legs out along the road toward us, apart
    for (hx, fx) in ((196, 120), (246, 330)):
        st.poly(k, [(hx - 24, 796), (hx + 24, 796), (fx + 30, 930), (fx - 30, 930)], oc.SUIT_LEG, 2.2)
        st.poly(k, [(fx - 34, 920), (fx + 34, 920), (fx + 30, 975), (fx - 30, 975)], (0.06, 0.06, 0.07), 2.2)   # boots, soles up
    st.poly(k, [(164, 786), (278, 786), (282, 812), (160, 812)], oc.COAT, 2.0)
    c = k.c; c.set_source_rgba(0, 0, 0, 0.35)
    c.save(); c.translate(222, 812); c.scale(120, 14); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()


def _bills(k):
    import on4_lying as ly
    for (x, y, a) in ((360, 520, 0.3), (330, 560, -0.6), (380, 600, 0.9)):
        ly.bill(k, x, y, a, 1.4, seed=int(x))


SCENES = [
    ("01 Ignored hero", [
        S("1.1", "wide, low", "A", WIDE, "Frame 0, held 0.5 s. The streetlamp, the neon heart. Pam-Cat in the hero pose, "
          "eyes back over her shoulder; two shadows flat on the cobbles; Sofia one step behind, eyes on her phone.",
          cast=A_SHADOW() + [P("sofia", 330, 650, 0.50, "hold", "neutral", (0, 0.6)),
                              P("pam_cat", 220, 730, 0.84, "hero", "proud", (0.6, -0.1))],
          protect=[("streetlamp", st.A_LAMP), ("heart", (342, 266))], eyeline="Pam back to Sofia; Sofia to her phone",
          action="(held)", reaction="Pam: Here it comes."),
        S("1.2", "wide, low", "A", WIDE, "0:01. Sofia sidesteps Pam like a puddle and walks on, past the camera; she never looks up.",
          cast=A_SHADOW() + [P("pam_cat", 220, 730, 0.84, "hero", "proud", (0.6, -0.1)),
                              P("sofia", 380, 820, 0.70, "hold", "neutral", (0, 0.6))],
          action="Sofia sidesteps her (the 0:01 joke)", reaction="the hero pose held at nobody"),
        S("1.3", "close", "A", (220, 560, 1.9), "The pose holds; her eyes follow Sofia out; the pose sags; she pulls her coat straight.",
          cast=[P("pam_cat", 220, 730, 0.84, "sag", "sad", (0.8, 0.2))], line="N: I know how to survive.",
          action="the pose sags", reaction="Fine. (to where Sofia went)"),
        S("1.4", "wide", "A_tail", WIDE, "The shadows peel off the cobbles and run up the street to a pair of taillights; she turns to follow.",
          cast=[P("thug1", 300, 600, 0.26, "open", seed=4111), P("thug2", 340, 590, 0.24, "open", seed=4112),
                P("pam_cat", 200, 760, 0.84, "hero", "surprised", (0.6, -0.6))],
          eyeline="Pam to the taillights", action="the shadows run", reaction="Where are you going?"),
    ]),
    ("02 The witness", [
        S("2.1", "high, over her shoulder", "above", WIDE, "Her cat ears in the foreground on the fire escape; below, the car "
          "from above; two bare heads at its rear window; one pale glove points back down the lane.",
          protect=[("the car", (300, 470)), ("the glove", (370, 530))], after=_ears_back, eyeline="down to the car"),
        S("2.2", "medium, through the window", "back_seat", WIDE, "The back seat: the Client, whole; beside him a velvet sleeve, "
          "a ringed hand on a knee, a chin (the window's top cuts Dad at the chin).",
          cast=[P("client", 170, 820, 0.66, "open", "plain", look=(0.7, 0.4), roll=False, badge=False),
                P("father", 370, 640, 0.78, (-20, 30, 20, -30), "hard", (-0.6, 0.6))],
          eyeline="both to the envelope", after=lambda k: oc.envelope(k, 200, 680, 1.4)),
        S("2.3", "insert, 1.2 s", "knee", WIDE, "Through the window: the envelope on the Client's knee, his finger taps it twice; the "
          "ringed hand lays itself flat on the seat: agreed.", protect=[("envelope", (200, 520)), ("ring", (392, 640))],
          line="The Client: Mine until it's done.", action="two taps", reaction="the ringed hand flat: agreed"),
        S("2.3b", "insert (b: into his coat)", "knee_coat", WIDE, "It slides into his own coat, inside left, his hand patting it flat.",
          protect=[("envelope", (250, 430))], action="into his coat", reaction="(Pam is watching)"),
        S("2.4", "close", "escape", WIDE, "Her eyes narrow; she swings onto the ladder and drops out of frame.",
          cast=[P("pam_cat", 270, 900, 0.96, "hero", "angry", (0.4, 0.6))], line="N: I know where to see what others do not see.",
          after=lambda k: railing(k, 690), eyeline="down to the car", action="she drops out of frame", reaction="Got you."),
    ]),
    ("03 Ignored victim", [
        S("3.1", "wide, low", "C_turn", (270, 610, 1.5), "The car swings round at the junction, nose to us; Pam runs onto the crossing after it. "
          "Don flashes STOP at her side without looking at her, flips the paddle, GO to the car; she stops dead in its path.",
          cast=[P("pam_cat", 340, ROAD_Y + 6, 0.62, "hero", "angry", (-0.6, -0.3)),
                P("don", 150, 700, 0.56, "stop", "confused", (0.2, -1.0), paddle_side="STOP", chin=1)],
          protect=[("the car", (250, 600))], line="Don: Traffic flows.", eyeline="Don to the car; Pam to the car",
          action="STOP at her side, GO to the car", reaction="she obeys: stops in its path"),
        S("3.2", "same wide, 0.8 s", "C_bump", (270, 610, 1.5), "Her back to us, she faces the headlights, one palm out; the car "
          "rolls into her at walking pace: the bumper at her knees, she tips back, stars; over backwards onto the stripes.",
          cast=[P("don", 132, 700, 0.56, "wave", "pleased", (0.6, -0.4), paddle_side="GO", paddle_ang=0.10, whistle_in=True),
                P("pam_from_behind", 292, ROAD_Y + 10, 0.66, "stop_palm", "surprised", (0, -0.2), lean=-0.22)],
          protect=[("bumper", (250, 690)), ("headlights", (250, 630))], after=lambda k: (_impact(k, 272, 520), _burst(k, 330, 690)),
          action="the bump", reaction="she tips back"),
        S("3.3", "medium, low (a: the glove on the bonnet)", "C_lying", WIDE, "Don walks to the car's front corner, lays his white "
          "glove flat on the bonnet, rubs one spot. Pam in the foreground under the bumper. He doesn't look at her.",
          cast=[P("don", 318, 604, 0.62, DON_REACH, "neutral", (-0.8, 0.6), reach_to=(272, 500), reach_hand=0, lean=-0.22,
                  paddle_side="GO", paddle_ang=0.9)],
          protect=[("bumper", (170, 586)), ("Don's glove", (272, 500)), ("her face", (112, 610))],
          line="Don: Not a scratch.", eyeline="Don to the bonnet; Pam to Don",
          action="the glove on the bonnet", reaction="(she watches him)", after=lying_over),
        S("3.3b", "same (b: the glove at his eye)", "C_lying", WIDE, "He holds the glove up to his eye: clean. Her small wave: her "
          "hand lifts off the road. He doesn't see it.",
          cast=[P("don", 318, 604, 0.62, "inspect", "neutral", (-0.9, -0.5), paddle_side="GO", paddle_ang=0.9)],
          protect=[("bumper", (170, 586)), ("her face", (112, 610))],
          eyeline="Don to his glove; Pam to Don", action="the glove at his eye: clean", reaction="her small wave, unseen",
          after=lambda k: (lying_over(k), _wave(k))),
        S("3.4", "medium", "cabin", WIDE, "Don waves the car on; the rear window opens: the ringed hand drops a fold of bills into the road.",
          protect=[("ring", (211, 480)), ("bills", (200, 620))], line="Dad: For the boys.", action="the bills dropped",
          reaction="(they fall to her)"),
        S("3.5", "low, close", "lying", WIDE, "The bills land on her; the shadows step over her; a pale glove plucks a bill off her coat; "
          "nobody looks down.", protect=[("her face", (112, 610)), ("the glove", (300, 560))],
          eyeline="each shadow to the bills", action="a glove plucks a bill", reaction="nobody looks down"),
        S("3.6", "close, sitting up", "C_low", WIDE, "She sits up and pushes her mask straight; her eyes follow the car.",
          cast=[P("pam_cat", 220, 900, 0.96, "mask_fix", "sad", (0.6, -0.3), clip_y=800)], line="N: I am like a cat. I have seven lives.",
          after=_sit_legs,
          eyeline="to the car", action="she sits up", reaction="Six left."),
    ]),
    ("04 False recognition", [
        S("4.1", "wide, low angle", "front", WIDE, "A new place, held: the car parked and empty, the club door, the marquee coming on line "
          "by line; Pam-Cat walks in and stops under it.", cast=[P("pam_cat", 330, 712, 0.62, "hero", "surprised", (0, -1))],
          protect=[("marquee", (270, 340)), ("the car", (150, 680))], line="Pam: There you are.", eyeline="to the car, then up"),
        S("4.2", "insert, top band", "front", (270, 345, 1.15), "The marquee: PAM-CAT · the bulb strip · ONLY FOR YOU.",
          protect=[("marquee", (270, 345))]),
        S("4.3", "medium, under the sign", "front", (300, 520, 1.5), "She points up at the sign, then at herself; turns to show "
          "someone: the street is empty. A small smile anyway; she pats her ears up and pushes the door.",
          cast=[P("pam_cat", 300, 712, 0.62, "point_up", "happy", (0.4, -1))], protect=[("ONLY FOR YOU", (270, 416))],
          eyeline="to the sign, then to nobody", action="the point at the sign, at herself", reaction="Finally."),
    ]),
    ("05 The club", [
        S("5.1", "wide", "hall", WIDE, "Inside: the booth, the game table, the stage at the end. The Client and the ringed hand over the "
          "plan; the spotlight on the empty stage.", eyeline="both to the plan"),
        S("5.3", "medium", "hall", (160, 610, 1.9), "Pam-Cat walks to the booth; her gloved hand goes into the Client's coat and comes out "
          "with the envelope by its edge. Neither man looks up.", cast=[P("pam_cat", 250, 716, 0.46, "lift", "sly", (-0.8, 0.4))],
          line="Pam: Easy.", eyeline="Pam to the coat; the men to the plan", action="the lift", reaction="neither looks up"),
        S("5.3b", "insert (b: the lift)", "coat_lift", WIDE, "Her black glove draws the envelope out of his coat by its edge.",
          protect=[("envelope", (300, 470))], action="the lift", reaction="(he doesn't look)"),
    ]),
    ("06 Ignored star", [
        S("6.1", "medium, low", "stage", WIDE, "She steps into the spotlight and opens the envelope.",
          cast=[P("pam_cat", 225, 700, 0.86, "hero", "proud", (0.3, 0.6), env=True)], eyeline="to the envelope"),
        S("6.2", "insert", "cv", WIDE, "Sofia's CV, her photograph.", protect=[("photo", (196, 320))]),
        S("6.3", "medium wide", "stage", WIDE, "She lifts it high, the triumph pose, and waits; the music stops.",
          cast=[P("pam_cat", 225, 700, 0.86, "triumph", "proud", (0.3, -0.6))], line="Pam: Well?",
          protect=[("envelope", (270, 420))], eyeline="out to the room"),
        S("6.4", "insert, 0.7 s", "spot", WIDE, "A pale glove from the top of the frame rests on the spotlight's handle and swings it away.",
          protect=[("glove", (410, 440))]),
        S("6.5", "wide, held 1 s", "stage_beam", WIDE, "The beam swings off her onto the card table; Pam a black shape against the lit room, arm "
          "still up; the room's backs to her.",
          cast=[P("pam_black", 250, 930, 1.20, "triumph", "proud", (0.3, -0.6))], eyeline="THE SHOT AND THE COVER"),
        S("6.6", "close, rim-lit", "stage_table", WIDE, "Her arm comes slowly down; she tucks the envelope in and pats it twice.",
          cast=[P("pam_cat", 250, 930, 1.20, "sag", "sad", (0.2, 0.4), env=True)], reaction="Of course."),
    ]),
    ("07 Awake", [
        S("7.1", "S6, the counter's end", "desk7", (714, 606, 2.0), "The match: the shape of 6.5. Pam asleep on the counter, the mask "
          "over her eyes, one arm up, the hand open. The lamp, seven cups, the machine.",
          cast=[P("pam_awake", 692, 760, 0.50, "down", "neutral", (0, 0), ARM_UP)], dream=False,
          protect=[("her hand", (713, 660)), ("cups", (730, 650))]),
        S("7.2", "S6", "desk7", (714, 606, 2.0), "Sofia comes round the counter's end mid-step, eyes on her phone; posts the envelope "
          "into Pam's raised hand; sets her mug at the end of the row. Clink. Walks on.",
          cast=[P("pam_awake", 692, 760, 0.50, "down", "neutral", (0, 0), ARM_UP), P("sofia", 600, 806, 0.47, "hold", "neutral", (0.2, 0.7))],
          line="SOFIA: Only for you.", eyeline="Sofia to her phone, never to Pam", after=_sofia_post, dream=False,
          protect=[("envelope", (706, 510))], action="the posting", reaction="the fingers close on it"),
        S("7.3", "close", "desk7", (692, 640, 3.0), "The clink wakes her; she pushes the mask up, ears up; she looks at her hand.",
          cast=[P("pam_awake", 692, 735, 0.50, "up", "surprised", (0.4, -0.6), ARM_UP)], dream=False, eyeline="to her hand"),
        S("7.4", "insert, top band", "rota", WIDE, "INTERNAL MAIL; the COFFEE ROTA: MON to SUN, PAM on every line.",
          protect=[("rota", (270, 300))], dream=False),
        S("7.5", "close, Pam and the sheet", "desk7", (700, 620, 2.4), "Her fingertip goes down the rows to the seventh PAM. Stops. Hold 0.6 s.",
          cast=[P("pam_awake", 692, 735, 0.50, "up", "sad", (-0.3, 0.8), "stand")], after=_rota_held, dream=False,
          protect=[("rota", (706, 668))], eyeline="to the sheet", reaction="Only for me."),
    ]),
    ("08 Back to the dream", [
        S("8.1", "S6", "desk8", (714, 606, 2.0), "She lays the rota over the cups, pulls the mask back down, head on her arm.",
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
    if name == "above":
        lane_above(k); return lambda c_: ons.vignette(c_, 0.6)
    if name == "escape":
        fire_escape_close(k); return lambda c_: ons.vignette(c_, 0.5)
    if name == "back_seat":
        back_seat2(k); return None
    if name == "knee":
        knee_insert(k); return None
    if name in ("C", "C_turn", "C_bump"):
        loc_c(k)
        if name == "C_turn":                                 # v3: head on at the junction (the three-quarter read as two cars)
            car.reflect(k, lambda: car.front(k, 250, 640, 0.52), 640, 0.25, 20)
        if name == "C_bump":
            car.reflect(k, lambda: car.front(k, 250, 702, 1.15), 702, 0.25, 30)
            g = cairo.RadialGradient(292, 640, 10, 292, 640, 130)       # board v1: the headlights light her from behind
            g.add_color_stop_rgba(0, 1, 1, 0.95, 0.85); g.add_color_stop_rgba(1, 1, 1, 0.95, 0)
            k.c.set_source(g); k.c.rectangle(130, 480, 330, 260); k.c.fill()
        return lambda c_: (st.light_c(c_), name == "C_bump" and car.glow(c_, "front", 250, 702, 1.15),
                           name == "C_turn" and car.glow(c_, "front", 250, 640, 0.52))
    if name == "C_low":                                      # 3.6: low on the road, the crossing behind her
        import on4_lying as ly
        loc_c(k); ly.ground(k); return st.light_c
    if name == "C_lying":
        loc_c(k); ly.ground(k)
        car.front(k, 170, 600, 1.15)                         # her body is drawn after the cast (lying_over): Don behind her
        return st.light_c
    if name == "cabin":                                      # board v1: the rear door reads: its wheel arch, the tail lamp
        loc_c(k); car.c_cabin(k)
        c = k.c
        c.set_source_rgb(0.02, 0.02, 0.03); c.new_path(); c.arc(420, 760, 70, math.pi, 2 * math.pi); c.fill()
        car._wheel(c, 420, 760, 56)
        car._rr(c, 500, 520, 14, 60, 5); c.set_source_rgb(*st.NEON); c.fill()
        return None
    if name == "lying":
        return "surface"
    if name == "front":
        cl.FRONT_LIGHT[0] = "v7"; cl.front(k, True); return lambda c_: cl.light_front(c_, True)
    if name == "hall":
        cl.HALL_LAMP[0] = "v7"; cl.hall(k); return cl.light_hall
    if name == "plan":
        cl.PLAN_CARD[0] = "v7"; cl.plan_insert(k); return cl.light_inside
    if name == "stage":
        stage_front(k, True); return lambda c_: ons.vignette(c_, 0.55)
    if name == "stage_table":
        room_reverse(k); return lambda c_: ons.vignette(c_, 0.5)
    if name == "stage_beam":
        room_reverse(k, beam=True); return lambda c_: ons.vignette(c_, 0.5)
    if name == "knee_coat":
        knee_coat(k); return None
    if name == "coat_lift":
        coat_lift(k); return lambda c_: ons.vignette(c_, 0.5)
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
        pr.cups(k_, x0=668, eighth=eighth)
        if sh["id"] == "8.1":
            pr.rota(k_, 734, pr.F - 168, 0.30, 0.12)
        heads.update(draw_cast(k_, front))
        if sh["after"]:
            sh["after"](k_)
    fs4.draw_set(k_ := k, {"pam_back": pam_back, "mom_front": props})
    return heads


def render(sh, scale=1):
    oc.CROSSBELT[0] = False; st.C_POST[0] = "v7"
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


DUR = {"5.3": 4.6}                                         # board v2: 5.2 cut, its second to the lift


def _timing():
    d = json.load(open(os.path.join(OUT, TIMING)))
    tm = {s["shot"]: dict(s) for s in d["shots"]}
    for k_, v in DUR.items():
        tm[k_]["dur"] = v
    return tm, d


def script(out):
    tm, d = _timing()
    L = ["# Office Noir 4: Seven Lives — script v7 (GENERATED from src/on4_scenes.py; do not edit by hand)", "",
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
    c.move_to(20, 40); c.show_text("Office Noir 4 · layouts v3 · %s" % title)
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
    print(script(os.path.join(out, "office-noir-4-script-v7.md")))
    for i, (title, shots) in enumerate(SCENES):
        p = os.path.join(out, "on4_layout_s%d_v3.png" % (i + 1))
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
    c.move_to(20, 40); c.show_text("Office Noir 4 · shot plan v3 (top down: locations, cameras, who stands where)")
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
    x0 = 440; panel(x0, y0, "B  the lane from the fire escape (2.1, 2.4)")
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
    x0, y0 = 20, 500; panel(x0, y0, "the hall (5.1, 5.3)")
    _box(c, x0 + 40, y0 + 240, 140, 80, "booth: Client, Dad"); _box(c, x0 + 220, y0 + 220, 110, 70, "game table, 2 shadows")
    _box(c, x0 + 150, y0 + 40, 100, 50, "stage, spotlight"); _mark(c, x0 + 200, y0 + 260, "Pam-Cat (5.3)", PAM_C)
    _cam_icon(c, x0 + 200, y0 + 395, -math.pi / 2, "5.1"); _cam_icon(c, x0 + 330, y0 + 360, -2.4, "5.3")
    # the stage
    x0 = 440; panel(x0, y0, "the stage (6.1-6.4) and its reverse (6.5, 6.6)")
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
    order = ["A", "A_tail", "B_high", "above", "escape", "back_seat", "knee", "C_turn", "C_bump", "C_lying", "cabin", "lying", "C", "front", "hall", "plan", "stage", "cv", "spot", "stage_table", "desk7", "rota", "desk8", "lampclose"]
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
    c.move_to(20, 40); c.show_text("Office Noir 4 · blocking v4 · 3.1-3.3 (generated from the shots; each panel in its shot's own camera)")
    # board v1: generated from the shots' own positions (frame x, feet y), not drawn by hand
    CAR = {"C_turn": (250, 640), "C_bump": (250, 702), "C_lying": (170, 600)}
    def td(x, y):                                            # frame (x, feet) -> the top view: x across, depth from the feet line
        return 110 + x / 540 * 180, 40 + (y - 560) / 170 * 360
    for i, sid in enumerate(("3.1", "3.2", "3.3")):
        sh_ = by[sid]; x0, y0 = 20 + i * 420, 70
        c.set_source_rgb(1, 1, 1); c.rectangle(x0, y0, 400, 440); c.fill()
        _box(c, x0 + 110, y0 + 30, 180, 380, "", (0.75, 0.73, 0.70))
        sx_, sy_ = td(0, 646); ex_, ey_ = td(0, 712)
        for j in range(7):
            c.set_source_rgb(1, 1, 1); c.rectangle(x0 + 116 + j * 25, y0 + sy_, 14, ey_ - sy_); c.fill()
        cx, cy = CAR[sh_["loc"]]; tx, ty = td(cx, cy)
        c.set_source_rgb(*CAR_C); c.rectangle(x0 + tx - 26, y0 + ty - 100, 52, 100); c.fill()
        c.set_source_rgb(1, 1, 0.6); c.rectangle(x0 + tx - 22, y0 + ty - 4, 12, 4); c.fill(); c.rectangle(x0 + tx + 10, y0 + ty - 4, 12, 4); c.fill()
        for who, a_, kw_ in sh_["cast"]:
            mx, my = td(a_[0], a_[1])
            if who == "don":
                _mark(c, x0 + mx, y0 + my, "Don" + (" (%s)" % kw_["paddle_side"] if kw_.get("paddle_side") else ""), DON_C)
            elif who.startswith("pam"):
                _mark(c, x0 + mx, y0 + my, "Pam", PAM_C)
        if sh_["loc"] == "C_lying":
            import on4_lying as ly
            mx, my = td(ly.HEAD[0] + 120, 690); _mark(c, x0 + mx, y0 + my, "Pam (lying)", PAM_C)
        _cam_icon(c, x0 + 200, y0 + 430, -math.pi / 2, "camera, low")
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 0); c.set_font_size(13)
        yy = y0 + 470
        for ln in _wrap(sid + "  " + sh_["action"] + " -> " + sh_["reaction"], 52):
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


def board(out=OUT, ver=2):
    """stage 5: one key frame per shot at 540, generated; two sheets at 400 px tiles, numbered with the time, and a phone
    sheet at 270 px. Neutral copies for the cold viewers go to /tmp/on4_board_cv (frame_NN.png, no names)."""
    import shutil
    tm, _ = _timing()
    shots = [x for _, ss in SCENES for x in ss]
    surf, probs = [], []
    cvdir = "/tmp/on4_board_cv"
    shutil.rmtree(cvdir, ignore_errors=True); os.makedirs(cvdir)
    for i, sh in enumerate(shots):
        s_, heads = render(sh, 1)
        probs += checks(sh, heads)
        surf.append(s_)
        s_.write_to_png(os.path.join(cvdir, "frame_%02d.png" % (i + 1)))
    def sheet_(items, path, tile, cols, labels=True):
        th = int(tile * 960 / 540)
        rows = (len(items) + cols - 1) // cols
        S_ = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (tile + 12) + 12, rows * (th + 40) + 60)
        c = cairo.Context(S_); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(22)
        c.move_to(12, 36); c.show_text("Office Noir 4 · board v%d" % ver)
        for j, (n, sh) in enumerate(items):
            x = 12 + (j % cols) * (tile + 12); y = 50 + (j // cols) * (th + 40)
            c.save(); c.translate(x, y); c.scale(tile / 540, tile / 540); c.set_source_surface(surf[n], 0, 0); c.paint(); c.restore()
            if labels:
                t = tm.get(sh["id"].rstrip("b"), {})
                c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("Inter", 0, 1); c.set_font_size(14 if tile > 300 else 11)
                c.move_to(x, y + th + 18); c.show_text("%d  %s  %.1f s" % (n + 1, sh["id"], t.get("start", 0)))
        S_.write_to_png(path)
        return path
    items = list(enumerate(shots))
    half = (len(items) + 1) // 2
    outs = [sheet_(items[:half], os.path.join(out, "on4_board_v%d_a.png" % ver), 400, 6),
            sheet_(items[half:], os.path.join(out, "on4_board_v%d_b.png" % ver), 400, 6),
            sheet_(items, os.path.join(out, "on4_board_v%d_phone.png" % ver), 270, 9)]
    return outs, probs
