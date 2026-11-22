"""THE OFFER (episode 13): the scene file, v1 (stage 4, series/production-process.md). From here on this file is the
episode: every shot with its time and line, its camera, who is in frame and where, the props and signs, the action
and the reaction. Everything below is generated from it and never edited by hand:

  python3 of_scenes.py [out_dir]  ->  the-offer-script-v5.md    the script (generated)
                                      of_layout_s<N>_v1.png     a layout sheet per scene, every shot at 270 with its checks
  The checks on every layout frame are uz_check's own (scale, signs); the build stops (exit 1) on a failure that is not
  listed in KNOWN with its reason.

Script v4 (approved at stop 2) is the plan this file starts from (of_script_v4.py); the timing is the recorded takes'
(of_timing_v2.json). Changes against v4 are in CHANGES. The Client is drawn as in episodes 9-11 for now: Tomas is
redrawing him and his clothes separately (22 Nov)."""
import json
import math
import os
import sys
import textwrap
import cairo
import kit
import of_set as gs
import uz_check as uz
import cs_frame as cf
from kit import Ctx, INK, rect, ellipse, cut

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "the-offer")
W, H = 540, 960
F = gs.F
FS, GS, CS = gs.FS, gs.GS, gs.CS

CHANGES = [
    "**Timing v3** (`of_timing_v3.json`, after scene 1's cold viewers): 0.1 0.6 -> 0.4 s, 0.2 0.8 -> 1.0 s (the reach), "
    "0.4 1.8 -> 1.4 s (the phone held too long), 0.10 1.0 -> 1.4 s (the payoff needs a beat). The length is unchanged.",
    "**1.5** is 1.1's frame, not a close-up (chosen by Claude on Tomas's \"choose what is better\", 22 Nov): the plan stays whole, "
    "and the action is his head turning to Father.",
    "**3.6** INVITATION reads **from FATHER** (chosen the same way): new information, not the robot's line again.",
    "The garage is set v2 (`of_set.py`, `the-offer-set-v2.md`): the sign and the plan are on the wall right of the door, the "
    "pegboard to their left, a walkway behind the car.",
    "**2.3** is a MEDIUM on the handover (the lamp between his hand and the bodyguard's), not the two-shot: in the mute "
    "test both viewers saw only \"a heavy with a flashlight\" (layout v3).",
    "**0.8**: the car tilts on its stands; **0.10**: the bodyguard's hands come off open, he steps back and looks to "
    "Father; **1.7**: he looks at Father as he shuts the lighter; **0.4**: his arm holds the phone down from the top of the "
    "frame (both viewers had taken it for the Client's phone). The burn mark is bigger and darker (layout v3).",
    "The Client wears his garage look (`client_of.py` v2: navy coveralls tied at the waist, white T-shirt, the rag; the "
    "faces bored, listen, glance, stare), and in 2.1-2.3 he is bent into the engine in his true profile (layout v4).",
    "**2.8f** is 1.1's frame, not a close-up: bodyguard 1 stands behind the car under the plan, the burn mark above "
    "him (the same reason as 1.5: a close-up of anyone behind the car cuts the plan).",
    "The car's body is 20 % lower (set v3), so its roof is at a man's shoulder and bodyguard 1 can lean on it (0.8).",
    "Every shot now has its camera, cast, signs, action and reaction here; the script is generated from them.",
]

# --- where they stand, per scene (set units; feet) -------------------------------------------------------------------
BLOCK = {
    1: dict(father=(120, 884), g1=(206, 862), g2=(40, 870)),
    0: dict(father=(160, 840), g1=(104, 856), g2=(218, 856)),          # 0.3: arriving, in the doorway
    2: dict(father=(96, 880), g1=(240, 872), g2=(470, F + 18), client=(318, 916)),
    3: dict(father=(380, 884), g1=(596, F + 18), g2=(150, 872), client=(588, 872)),        # v6: bodyguard 1 right of the Client
    5: dict(),
}
LAMP_HELD = (516, 698)                                     # v9 (22 Nov): beside the bay, low, lighting the engine (not his face)
LAMP_HIGH = (482, 560)                                     # 2.3 v3: high over the bay, pointing down
FATHER_LAMP = (450, 640, 2.0)                              # Father's closes in scene 3: the plan whole above, the lamp man behind him
FX_LAMP = 410
LAMP_CAM = (530, 770, 1.30)                                # 2.3 (v7): both men whole, the plan whole above them


# --- the shots -------------------------------------------------------------------------------------------------------
def S(id_, size, cam, picture, line="", action="", reaction="", cast=(), state=None, fx="", draw=None, then=None):
    """cam: (fx, fy, z) | "wide" | [names to frame by the series' rule] | "insert"."""
    return dict(id=id_, size=size, cam=cam, picture=picture, line=line, action=action, reaction=reaction,
                cast=tuple(cast), state=state or {}, fx=fx, draw=draw, then=then)


PLAN_FRAME = (426, 520, 1.75)
CAR_CAM = (350, 752, 1.40)                                 # 0.8 (v7): the car, its roof, the legs under it; the heavy at the left
ROOF_CAM = (128, 736, 1.45)                                # 0.8 / 0.10 (v6): the roof, the hand on it, the legs under it

SCENES = [
    ("1 · The Legs", "The Client's garage, bay 7. Morning.", 1, [
        S("0.1", "WIDE", "wide", "**FRAME 0.** The bay: the car on stands, the legs on the creeper, the lamp on the floor, the radio, "
          "the plan under GARAGE 7, the roller door up on the bright street.", action="the legs work", fx="radio, low"),
        S("0.2", "WIDE", "wide", "SAME FRAME. Headlights sweep the wall; a deep engine stops outside. A hand comes out, feels for a "
          "wrench. **The watch.**", action="the hand takes the wrench", reaction="the legs don't move", fx="engine stops; clank",
          state=dict(sweep=True)),
        S("0.3", "LOW", (160, 846, 5.0), "LOW, floor level. In the doorway's light: two pairs of black shoes, shoulder to shoulder; "
          "they step apart; between them, a smaller polished pair: Father.", action="they step apart", cast=("father", "g1", "g2"),
          state=dict(doorway=True)),
        S("0.4", "HIGH", (318, 860, 2.0), "HIGH, over Father's shoulder, down at the legs. Bodyguard 1's sleeve holds the phone down: "
          "the one-star post, **DELETE POST**, his thumb over it.", action="the thumb hovers", reaction="the legs go on: a clank",
          state=dict(phone="delete"), fx="clank"),
        S("0.5", "CLOSE", "under", "UNDER THE CAR, close. The Client on his back, lit by the lamp, working. He doesn't look out.",
          line='CLIENT: "Is it wrong?"', action="he works", reaction="he doesn't look out"),
        S("0.6", "CLOSE", ["father"], "CLOSE, Father. Eyes up from under his brows, chin down. No answer.",
          reaction="no answer", cast=("father",)),
        S("0.8", "MEDIUM", CAR_CAM, "MEDIUM on the car (v7). Bodyguard 1 leans one big hand on the roof. **The car rocks on its stands over "
          "the man underneath.** A stand scrapes. The legs stop.", action="the hand on the roof; the car rocks",
          reaction="the legs stop", cast=("g1",), state=dict(lean=True, tilt=-0.045), fx="the stand scrapes"),
        S("0.9", "CLOSE", "under", "UNDER THE CAR, as 0.5. The sump a hand above his face, swaying. He doesn't look out, doesn't "
          "raise his voice.", line='CLIENT: "Off the car."', action="the sump sways", reaction="he stays flat",
          state=dict(sway=True)),
        S("0.10", "TWO-SHOT", ["g1", "father"], "TWO-SHOT (v7). The hand comes off the roof at once. Only then does he look at Father. "
          "**Father has seen it.**", action="the hand comes off", reaction="Father has seen it", cast=("father", "g1"),
          state=dict(zmax=1.7)),
    ]),
    ("2 · The Lighter", "Same bay.", 2, [
        S("1.1", "TWO-SHOT", PLAN_FRAME, "GARAGE 7 painted, the plan, and bodyguard 2 behind the car. His finger to one square: "
          "**GARAGE 7**. He looks round at the real bay.", action="the finger on 7", reaction="he looks round at the bay",
          cast=("g2",)),
        S("1.2", "TWO-SHOT", PLAN_FRAME, "SAME FRAME. The gold lighter in his fist. CLICK: the flame under 7's corner. The paper "
          "browns. **Nobody says it.**", action="CLICK, the flame", cast=("g2",), state=dict(burn=0.4, flame=True),
          fx="CLICK; the radio alone; the paper crackles"),
        S("1.3", "WIDE", "wide", "FRAME 0's frame. The creeper rolls out; the Client sits up, wipes his hands on a rag, looks at "
          "the flame, then **at his watch**.", action="he sits up", reaction="he checks his watch",
          cast=("father", "g1", "g2", "client"), state=dict(burn=0.7, flame=True, sit=True)),
        S("1.4", "CLOSE", ["client"], "CLOSE, the Client, to Father, flat, the rag in his hands.",
          line='CLIENT: "Burn them. Your son loses his only customer."', cast=("client",),
          state=dict(burn=0.7, sit=True)),
        S("1.5", "TWO-SHOT", PLAN_FRAME, "1.1's FRAME. Bodyguard 2, the flame still held: **his head turns to Father** for the order.",
          action="the head turns to Father", cast=("g2",), state=dict(burn=0.8, flame=True)),
        S("1.6", "CLOSE", ["father"], "CLOSE, Father alone. **The left eyebrow goes up.** A small shake of the head.",
          action="the eyebrow; the shake", cast=("father",), state=dict(burn=0.8)),
        S("1.7", "TWO-SHOT", PLAN_FRAME, "SAME FRAME as 1.2. CLICK: the lighter shuts. **The burn mark on 7 stays** for the arc.",
          action="CLICK shut", reaction="the mark stays", cast=("g2",), state=dict(burn=1.0), fx="CLICK"),
    ]),
    ("3 · The Offer", "Same bay.", 3, [
        S("2.1", "TWO-SHOT", ["father", "client"], "Father and the Client, the car between them. Father speaks to him. "
          "**He has only ever spoken to Don.**", line='FATHER: "My son says his machine finds anything."',
          cast=("father", "client", "g2"), state=dict(bonnet=1.0, burn=1.0)),
        S("2.2", "CLOSE", ["client"], "CLOSE, the Client, back under the bonnet, not looking up.",
          line='CLIENT: "It found nothing."', cast=("client",), state=dict(bonnet=1.0, burn=1.0)),
        S("2.3", "MEDIUM", LAMP_CAM, "MEDIUM on the handover (v2). Without looking he holds the lamp out behind him; bodyguard 1 "
          "takes it unasked and holds it over the engine. **He is a garage hand now.**", action="the lamp, handed back",
          reaction="bodyguard 1 takes it", cast=("father", "client", "g1", "g2"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.3b", "CLOSE", FATHER_LAMP, "CLOSE, Father, watching that. A long look; his eyes go from the lamp to the Client. "
          "**This is when he decides.**", reaction="he decides", cast=("father", "g1"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.4", "CLOSE", FATHER_LAMP, "CLOSE, Father, the bodyguard with the lamp behind him.",
          line='FATHER: "How would you run his company?"', cast=("father", "g1"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.5", "CLOSE", ["client"], "CLOSE, the Client. He straightens up. Checks the watch.", line='CLIENT: "Without him."',
          action="the watch", cast=("client",), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.6a", "CLOSE", FATHER_LAMP, "CLOSE, Father. HELD, silent. He weighs it. Nothing moves.", reaction="nothing moves",
          cast=("father", "g1"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.6", "CLOSE", FATHER_LAMP, "SAME FRAME. Business.", line='FATHER: "And then?"', cast=("father", "g1"),
          state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.7", "MEDIUM", ["client"], "MEDIUM. The Client takes his phone from his top pocket, wipes it on his trousers, turns it "
          "round.", action="the phone, turned round", cast=("client",), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, zmax=1.9)),
        S("2.8", "INSERT", "insert", "INSERT, the phone, filling the frame: one contact card. **PAM — finds things.**",
          state=dict(insert="card")),
        S("2.8b", "CLOSE", ["client"], "CLOSE, the Client, phone still held out. His terms from episode 9, now for her.",
          line='CLIENT: "One month. I ask. She finds it."', cast=("client",), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.8c", "TWO-SHOT", ["father", "client"], "TWO-SHOT. Father nods once. That is all.", line='FATHER: "Done."',
          action="one nod", cast=("father", "client", "g1", "g2"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.8d", "MEDIUM", ["client"], "MEDIUM, the car. The Client drops the bonnet: SLAM. Wipes it once with the rag.",
          action="SLAM", cast=("client", "g1"), state=dict(bonnet=0.0, burn=1.0, lamp_held=True, zmax=1.5), fx="SLAM"),
        S("2.8e", "INSERT", "insert", "INSERT, the ignition, his oily fingers on the key. It turns; the engine coughs, catches, "
          "runs: **he fixed it.**", action="the key turns", reaction="the engine runs", state=dict(insert="key"),
          fx="the engine drowns the radio"),
        S("2.8f", "CLOSE", (470, 680, 1.8), "1.1's FRAME (the plan above him, the burn on 7): bodyguard 1, still holding the lamp over a shut bonnet. Nothing left to light.",
          reaction="he keeps holding it", cast=("g1",), state=dict(bonnet=0.0, burn=1.0, lamp_held=True)),
        S("2.9", "MEDIUM", ["father"], "MEDIUM. Father, on his way to the door, without turning his head, to bodyguard 2, "
          "who thumbs a calendar entry.", line='FATHER: "Put it in the calendar."', action="the thumb on the phone", cast=("father", "g2"),
          state=dict(bonnet=0.0, burn=1.0, phone2=True, zmax=1.7, moved=dict(father=(214, 880), g2=(120, 872)))),
    ]),
    ("4 · The Calendar", "The front desk, UptimeZ. The same minute.", 4, [
        S("3.1", "WIDE", "desk", "HARD CUT. THE FRONT DESK, wide: Don on the throne, feet up, the crown behind his head; the robot "
          "at its station by the door; Pam at the counter. A cheerful **chime**.", fx="chime", state=dict(desk="wide")),
        S("3.2", "CLOSE", "desk", "CLOSE, the robot. Its visor: one line, **WITHOUT HIM**. Delighted.",
          line='ROBOT: "New meeting. Agenda: without him."', state=dict(desk="robot", visor=True)),
        S("3.3", "CLOSE", "desk", "CLOSE, Don on the throne. He has sat up for good news. The smile stays on.",
          line='DON: "Without who?"', state=dict(desk="don", don="happy")),
        S("3.4", "CLOSE", "desk", "CLOSE, the robot. **ITS HEAD TURNS, SLOWLY**, to Don. Still smiling. **The peak: hold it.**",
          action="the head turns", state=dict(desk="robot", turn=True)),
        S("3.5", "CLOSE", "desk", "CLOSE, Don, as 3.3. He follows the look down, to himself. The smile goes in one drawing.",
          reaction="the smile goes", state=dict(desk="don", don="stiff")),
        S("3.6", "CLOSE", "desk", "CLOSE, Pam at the counter. Her phone buzzes: **INVITATION, from FATHER**. She reads it, looks "
          "at Don, turns the phone **face down**. (Inside its 1.4 s: 0.45 s on the phone, filling the frame; then face down, held 0.6 s.)",
          action="the phone, face down", fx="buzz", state=dict(desk="pam"),
          then=S("3.6 insert", "INSERT", "insert", "the phone: INVITATION, from FATHER", state=dict(insert="invite"))),
        S("3.7", "CLOSE", "desk", "CLOSE, Don, as 3.3. He grabs his phone off the throne's arm and dials DAD. The sweat comes back.",
          action="he dials DAD", state=dict(desk="don", don="panic")),
    ]),
    ("5 · Frame 0", "The garage.", 5, [
        S("4.1", "INSERT", (112, 640, 1.9), "INSERT, the doorway, the bright street. Father's hand, walking out, the phone buzzing: "
          "DONNIE. He turns it face down against his palm without stopping.", action="face down", state=dict(insert="donnie")),
        S("4.2", "WIDE", "wide", "HARD CUT. **FRAME 0'S DRAWING**, nobody else; the only difference: **the burn mark on GARAGE 7**. "
          "The engine outside pulls away. Cut to 0.1.", state=dict(burn=1.0), fx="the car pulls away; the radio runs on"),
    ]),
]

KNOWN = {}   # (shot, check text) -> why it is allowed. None yet.


# --- drawing ---------------------------------------------------------------------------------------------------------
def _timing():
    d = json.load(open(os.path.join(OUT, "of_timing_v3.json")))
    return {s["shot"]: s for s in d["shots"]}


# --- the key poses (layout v2): what each shot's action looks like at its extreme ------------------------------------
# per shot: name -> what that person does. Targets are set points or names resolved in _pt(); the Client's poses are
# stand-ins until Tomas's redraw.
POSES = {
    "0.3": dict(),
    "0.4": dict(g1=dict(phone="delete")),
    "0.6": dict(father=dict(face="low", look=(1, 0))),
    "0.8": dict(g1=dict(targets=["roof"], push=True)),          # hand flat on the roof, arm out
    "0.10": dict(father=dict(look=(1, -0.1), face="hard"), g1=dict(targets=["off_l", "off_r"], turn=-1.0, back=26)),
    "1.1": dict(g2=dict(targets=["bay7_point"], point=True)),
    "1.2": dict(g2=dict(targets=["lighter"], lighter=1.0)),
    "1.3": dict(father=dict(look=(1, 0)), g2=dict(targets=["lighter"], lighter=1.0), client=dict(kind="sit", look=(1, -0.6))),
    "1.4": dict(client=dict(kind="sit", look=(-1, -0.2))),
    "1.5": dict(g2=dict(targets=["lighter"], lighter=1.0, turn=-1.0)),
    "1.6": dict(father=dict(face="brow", look=(1, -0.2))),
    "1.7": dict(g2=dict(targets=["lighter"], lighter=0.0, turn=-1.0)),                      # shutting it, looking at Father
    "2.1": dict(father=dict(face="talk", look=(1, 0)), client=dict(kind="bent")),
    "2.2": dict(client=dict(kind="bent")),
    "2.3": dict(father=dict(look=(1, -0.2)), client=dict(kind="bent", hand_back=True), g1=dict(targets=["handoff"])),
    "2.3b": dict(father=dict(look=(1, -0.5)), g1=dict(targets=["lamp"], lamp="held")),
    "2.4": dict(father=dict(face="talk", look=(1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.5": dict(client=dict(kind="watch", look=(1.9, 2.0), face="glance")),
    "2.6a": dict(father=dict(face="hard", look=(1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.6": dict(father=dict(face="talk", look=(1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.7": dict(client=dict(kind="pocket", look=(-0.4, 0.8))),
    "2.8b": dict(client=dict(kind="phone_out", look=(-1, 0))),
    "2.8c": dict(father=dict(face="low", look=(1, 0)), client=dict(kind="phone_out", look=(-1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.8d": dict(client=dict(kind="slam"), g1=dict(targets=["lamp"], lamp="held")),
    "2.8f": dict(g1=dict(targets=["lamp"], lamp="held")),
    "2.9": dict(father=dict(look=(1, 0)), g2=dict(targets=["chest_l"], phone="calendar")),
}


def _pt(name, x, f):
    c_ = gs.CAR_X
    return {"roof": (x + 82, 650), "bay7_point": (gs.bay7()[0] - 12, gs.bay7()[1] - 14),
            "lighter": (gs.bay7()[0] + 2, gs.bay7()[1] + 92), "lamp": LAMP_HELD, "handoff": (600, 640),
            "chest_l": (x + 36, f - 118), "off_l": (x - 22, f - 118), "off_r": (x + 26, f - 120)}[name]


BENT_AT = (506, 846)                                      # the Client bent over the bay: x, and his feet (hidden by the car)
TAIL_K = {"2.9": 0.45}                                     # stage 7: a small face in a wide frame: the tip further in
MOUTH_AT = {}                                              # mouths a pose knows better than the face point (the profile)


def _cast_draw(k, n, scene, sh, heads):
    import dh_cast as dc
    import of_cast as oc
    st = sh["state"]
    ps = POSES.get(sh["id"], {}).get(n, {})
    pos = dict(BLOCK[0] if st.get("doorway") else BLOCK[scene], **st.get("moved", {}))
    c = k.c
    if n == "father":
        x, f = pos["father"]
        x += st.get("fshake", 0.0)
        if ps.get("front_lighter"):                                           # v9 veto: bodyguard 2's arm over the roof, to him
            lx, ly, fl, ld = ps["front_lighter"]
            gs.protect(c, "the lighter", lx - 22, ly - 60, lx + 22, ly + 56)
            for col, lw in ((INK, 30), ((0.11, 0.11, 0.13), 25)):                 # his sleeve, up to his shoulder over the roof
                c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
                c.move_to(lx + 26, ly + 30); c.line_to(448, 652); c.stroke()
            gs.lighter(k, lx, ly, 0.75, fl, hand=False, lid=ld)
            ellipse(k, lx + 20, ly + 32, 13, 17, (0.92, 0.74, 0.60), 3460, lw=2)    # his fist round the case
        o = oc.father(k, x, f, FS, face=ps.get("face", "hard"), look=ps.get("look", (1, 0)), targets=ps.get("targets_xy", ()))
        heads[n] = (o["head"][0], o["head"][1], 50 * FS)
        if ps.get("two_fingers") and ps.get("targets_xy"):                     # the veto: two fingers on the lid
            hx, hy = ps["targets_xy"][0]
            for dx in (-5, 5):                                                   # pointing DOWN, pressing the lid shut
                c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(1); c.move_to(hx + dx, hy - 2); c.line_to(hx + dx, hy + 16); c.stroke()
                c.set_source_rgb(*dc.SKIN_F); c.set_line_width(6); c.move_to(hx + dx, hy - 2); c.line_to(hx + dx, hy + 16); c.stroke()
    elif n in ("g1", "g2"):
        x, f = pos[n]
        x -= ps.get("back", 0)
        behind = (n == "g2" and scene == 2) or (n == "g1" and scene == 3)
        flip = behind
        tg = ps.get("targets_xy") or [_pt(t, x, f) for t in ps.get("targets", [])]
        o = oc.guard(k, x, f, GS, flip=flip, targets=tg, turn=ps.get("turn", 0.0), seed=1600 if n == "g1" else 1640)
        heads[n] = (o["head"][0], o["head"][1], 55 * GS)
        if ps.get("lamp"):
            hx, hy = ps.get("lamp_xy") or tg[0]
            if ps.get("cone"):                                       # v3: held high, pointing down into the bay
                cx0, cy0 = hx - 2, hy + 24
                g_ = cairo.LinearGradient(cx0, cy0, cx0, 712)
                g_.add_color_stop_rgba(0, 1.0, 0.93, 0.55, 0.85 * ps["cone"]); g_.add_color_stop_rgba(1, 1.0, 0.93, 0.55, 0.35 * ps["cone"])
                c.set_source(g_); c.move_to(cx0 - 6, cy0); c.line_to(cx0 + 6, cy0); c.line_to(548, 712); c.line_to(452, 712)
                c.close_path(); c.fill()
                c.set_source_rgba(1.0, 0.95, 0.65, 0.45 * ps["cone"])               # the pool of light on the engine
                c.save(); c.translate(500, 708); c.scale(50, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
                gs.lamp(k, hx - 2, hy + 10, ang=-math.pi / 2, lit=True)
            elif ps.get("cone_side", ps.get("lamp") == "held"):              # v9: from the side, into the bay, on his hands
                cs = ps.get("cone_side", 1.0) if ps.get("cone_side") is not None else 1.0
                bx0, by0 = hx - 14, hy + 18
                g_ = cairo.LinearGradient(bx0, by0, 500, 712)
                g_.add_color_stop_rgba(0, 1.0, 0.93, 0.55, 0.80 * cs); g_.add_color_stop_rgba(1, 1.0, 0.93, 0.55, 0.40 * cs)
                c.set_source(g_); c.move_to(bx0, by0 - 6); c.line_to(bx0 + 4, by0 + 6); c.line_to(510, 716); c.line_to(488, 700)
                c.close_path(); c.fill()
                c.set_source_rgba(1.0, 0.95, 0.65, 0.55 * cs)                          # the pool of light on his hands
                c.save(); c.translate(496, 706); c.scale(34, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
                gs.lamp(k, hx + 4, hy - 6, ang=2.5, lit=True)                     # the cage down-left, into the bay
            else:
                gs.lamp(k, hx - 8, hy + 22, ang=-1.3)
            gs.protect(c, "the lamp in his hand", hx - 40, hy - 10, hx + 30, hy + 50)
        if "lighter" in ps:
            hx, hy = tg[0]
            gs.protect(c, "the lighter", hx - 20, hy - 90, hx + 20, hy - 8)
            gs.lighter(k, hx - 2, hy - 46, 0.75, ps["lighter"], hand=False, lid=ps.get("lid", 1.0 if ps["lighter"] else 0.0))   # v8: bigger
        if ps.get("point") and tg:                                            # the finger on 7
            hx, hy = tg[0]
            c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(1); c.move_to(hx, hy + 8); c.line_to(hx - 4, hy - 6); c.stroke()
            c.set_source_rgb(0.92, 0.74, 0.60); c.set_line_width(5); c.move_to(hx, hy + 8); c.line_to(hx - 4, hy - 6); c.stroke()
        if ps.get("phone") == "calendar":
            hx, hy = tg[0]
            def cal(c_):
                c_.set_source_rgb(0.85, 0.15, 0.15); c_.rectangle(-19, -34, 38, 14); c_.fill()
                c_.set_source_rgb(1, 1, 1); c_.select_font_face("Lilita One"); c_.set_font_size(9)
                c_.move_to(-14, -24); c_.show_text("+ EVENT")
                c_.set_source_rgb(0.2, 0.2, 0.25)
                for i in range(3):
                    for j in range(3):
                        c_.rectangle(-15 + i * 11, -14 + j * 11, 8, 8); c_.fill()
            oc.phone(k, hx, hy - 10, 0.75, cal, ang=-0.1)
        if ps.get("push"):                                                    # the flat hand pressing the roof
            hx, hy = tg[0]
            ellipse(k, hx, hy - 2, 18, 7, (0.92, 0.74, 0.60), 3400, lw=2)
    elif n == "client":
        x, f = pos["client"]
        kind = ps.get("kind", "stand")
        look = ps.get("look", (-1, 0))
        if kind == "sit":
            o = oc.client_sit(k, x, f, CS, look=look, face=ps.get("face", "bored"), wipe=ps.get("wipe", 0.0))
        elif kind == "bent":                                            # v6: from the front, behind the car, bent over
            bx, bf = BENT_AT                                                # the open bay toward us; the lid up behind him
            w = ps.get("work", 0.0)                                          # stage 7: the hands busy in the bay
            hands = [(bx - 34 + 5 * w, 704 - 3 * abs(w)), (bx + 6 - 4 * w, 706 + 2 * w)]
            if ps.get("hand_back"):
                hands = [(bx - 34, 704), ps.get("hand_back_at", (bx + 70, 650))]
            c.save(); c.translate(bx, bf); c.scale(1, 0.86); c.translate(-bx, -bf)   # the trunk foreshortened, tipped to us
            o = oc.client(k, bx, bf, CS, look=(-0.4, 2.0), targets=hands, face="glance")   # eyes down, into the bay
            c.restore()
            o["head"] = (o["head"][0], bf + (o["head"][1] - bf) * 0.86)
            if ps.get("hand_back") and ps.get("client_lamp", True):
                hx_, hy_ = ps.get("hand_back_at", (bx + 70, 650))
                gs.lamp(k, hx_ - 6, hy_ + 2, ang=-1.3, lit=ps.get("lamp_lit", True))
        elif kind == "watch":
            wu = ps.get("watch_u", 1.0)                                       # stage 7: the wrist comes up to the eyes
            wx, wy = oc.watch_pose(x, f, CS)[0]
            o = oc.client(k, x, f, CS, look=look, targets=[(x + 40 + (wx - x - 40) * wu, f - 110 + (wy - f + 110) * wu)],
                          face=ps.get("face", "bored"))
        elif kind == "pocket":
            pu = ps.get("pocket_u", 0.0)                                     # stage 7: out of the pocket, turned round
            tx, ty = x - 30 - 66 * pu, f - 150
            o = oc.client(k, x, f, CS, look=look, targets=[(tx, ty)])
            oc.phone(k, tx - 6 * pu, ty - 2 - 8 * pu, 0.55 + 0.05 * pu, None, ang=0.4 - 0.5 * pu)
        elif kind == "phone_out":
            tx, ty = x - 96, f - 150
            o = oc.client(k, x, f, CS, look=look, targets=[(tx, ty)])
            oc.phone(k, tx - 6, ty - 10, 0.6, None, ang=-0.1)
        elif kind == "slam":
            sy = ps.get("slam_y", 0.0)                                       # stage 7: the hands come down with the lid
            o = oc.client(k, x, f, CS, look=(-1, 0.6), targets=[(x - 64, 668 - sy), (x - 40, 664 - sy)])
        else:
            o = oc.client(k, x, f, CS, look=look)
        heads[n] = (o["head"][0], o["head"][1], 55 * CS)


def garage_shot(k, sh, scene, heads, cam):
    st = sh["state"]
    behind_names = [n for n in sh["cast"] if (n == "g2" and scene == 2) or (n == "g1" and scene == 3)
                    or (n == "client" and POSES.get(sh["id"], {}).get("client", {}).get("kind") == "bent")]
    behind_names.sort(key=lambda n: n != "g1")                         # the lamp man furthest back
    front_names = [n for n in sh["cast"] if n not in behind_names]
    if scene == 3:
        legs_out = None
    elif "client" in sh["cast"] or st.get("sit"):
        legs_out = None
    else:
        legs_out = 0.0
    if st.get("sit") and "client" not in sh["cast"]:
        legs_out = gs.LEGS_OUT
    if st.get("legs_out_v") is not None:
        legs_out = st["legs_out_v"]
    if legs_out is not None and st.get("legs_jolt"):
        legs_out += st["legs_jolt"]
    bon = st.get("bonnet", 0.0)
    if sh["id"] == "2.8d" and not st.get("anim"):
        bon = 0.35                                                            # the slam, on its way down

    def behind(k):
        for n in behind_names:
            _cast_draw(k, n, scene, sh, heads)

    def front(k):
        for n in front_names:
            _cast_draw(k, n, scene, sh, heads)
    gs.LID_BEHIND[0] = any(POSES.get(sh["id"], {}).get("client", {}).get("kind") == "bent" for _ in (0,))
    gs.garage(k, burn=st.get("burn", 0.0), legs_out=legs_out, bonnet=bon,
              lamp_on_floor=scene in (1, 2, 5), behind=behind, front=front, tilt=st.get("tilt", 0.0))
    gs.LID_BEHIND[0] = False
    c = k.c
    if st.get("running"):                                                 # v9: 2.8e, the car runs: lights on, a puff of exhaust
        r_ = st["running"]
        x0_, x1_ = gs.CAR_X
        ly_ = gs.SILL + (712 - gs.SILL) * gs.CAR_SQUASH
        g_ = cairo.RadialGradient(x1_ - 10, ly_, 4, x1_ - 10, ly_, 120)
        g_.add_color_stop_rgba(0, 1.0, 0.97, 0.75, 0.95 * r_); g_.add_color_stop_rgba(1, 1.0, 0.97, 0.75, 0.0)
        c.set_source(g_); c.arc(x1_ - 10, ly_, 120, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(1.0, 0.98, 0.8, 0.9 * r_); c.move_to(x1_ - 6, ly_ - 8); c.line_to(x1_ + 140, ly_ - 40)
        c.line_to(x1_ + 140, ly_ + 50); c.line_to(x1_ - 6, ly_ + 8); c.close_path(); c.fill()
        p_ = st.get("puff", 0.0)
        for i in range(3):                                                # puffs from the tail pipe, drifting left and up
            a_ = p_ - i * 0.18
            if a_ <= 0:
                continue
            ex, ey = x0_ + 14 - 20 * a_, gs.SILL - 4 - 70 * a_
            c.set_source_rgba(0.35, 0.35, 0.38, max(0.0, 0.85 - 0.7 * a_))
            c.arc(ex, ey, 16 + 34 * a_, 0, 2 * math.pi); c.fill()
    if st.get("reach") is not None:                                       # 0.2: his hand out from under the sill, the wrench
        u = st["reach"]
        sx_, sy_ = gs.CREEPER[0] + 40, gs.SILL + 26
        hx_, hy_ = sx_ + 70 * u, sy_ + 34 * u
        mx_, my_ = sx_ + (hx_ - sx_) * 0.45, sy_ + (hy_ - sy_) * 0.45
        for col, lw in ((INK, 19), ((0.90, 0.69, 0.55), 15)):                  # v2: the forearm
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(mx_, my_); c.line_to(hx_, hy_); c.stroke()
        for col, lw in ((INK, 23), ((0.96, 0.95, 0.91), 19)):                  # the T-shirt sleeve from under the sill
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(0)
            c.move_to(sx_ - 6, sy_ - 3); c.line_to(mx_, my_); c.stroke()
        wx_, wy_ = (gs.CREEPER[0] + 112, gs.SILL + 62) if u < 0.8 else (hx_ + 6, hy_ + 2)
        c.set_source_rgb(0.66, 0.68, 0.70); c.set_line_width(6); c.move_to(wx_ - 18, wy_); c.line_to(wx_ + 14, wy_ - 4); c.stroke()
        c.set_source_rgb(*INK); c.set_line_width(1.6); c.new_path(); c.arc(wx_ + 18, wy_ - 5, 6, 0.6, 5.6); c.stroke()
        ellipse(k, hx_ + 4, hy_ + 2, 13, 10, (0.90, 0.69, 0.55), 3520, lw=1.8)        # the hand, open on the floor
        c.set_source_rgb(*INK); c.set_line_width(1.6)
        for q in range(3):
            c.move_to(hx_ + 10 + q * 0.5, hy_ - 4 + q * 4); c.line_to(hx_ + 18, hy_ - 3 + q * 4); c.stroke()
        rect(k, hx_ - 14, hy_ - 5, 8, 10, (0.86, 0.72, 0.30), 3521, shadow=False, lw=1.2)   # the watch
    if st.get("sweep"):                                                   # the headlights on the wall: a hard bright wedge
        dx_ = st.get("sweep_x", 0.0)                                       # v8: it moves across the wall
        c.set_source_rgba(1.0, 0.98, 0.78, 0.65)
        c.move_to(200 + dx_, 470); c.line_to(600 + dx_, 360); c.line_to(600 + dx_, 520); c.line_to(200 + dx_, 700); c.close_path(); c.fill()
    if POSES.get(sh["id"], {}).get("g1", {}).get("phone") == "delete":    # 0.4: HIS arm, from the top, holding it down
        import dh_cast as dc
        px, py = 300, 812
        for col, lw in ((INK, 46), (dc.SUIT, 40)):                            # the black sleeve, down from above right
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(500, 600); c.line_to(px + 66, py - 10); c.stroke()
        c.save(); c.translate(px + 62, py - 6); c.rotate(-0.55)
        rect(k, -24, -8, 48, 16, (0.97, 0.97, 0.94), 3409, shadow=False, lw=1.8)            # his white cuff
        c.restore()
        c.save(); c.translate(px, py); c.rotate(0.2); c.scale(1.5, 1.5)
        gs.protect(c, "the DELETE POST phone", -30, -48, 30, 48)
        rect(k, -30, -48, 60, 96, (0.10, 0.11, 0.14), 3410, lw=2)
        c.set_source_rgb(0.95, 0.96, 0.98); c.rectangle(-25, -42, 50, 84); c.fill()
        gs.T(c, "1", -10, -12, 18, col=(0.85, 0.55, 0.05))
        _star(c, 9, -18, 8)
        gs.T(c, "REVIEW", 0, 2, 8.5, col=INK, font="Inter")
        c.set_source_rgb(0.20, 0.42, 0.62); c.rectangle(-25, -42, 50, 13); c.fill()                # v6: whose post it is
        gs.T(c, "YOUR POST", 0, -32.5, 7.5, col=(1, 1, 1))
        rect(k, -22, 12, 44, 20, gs.RED, 3411, shadow=False, lw=1.2)
        gs.T(c, "DELETE", 0, 27, 10.5, col=(1, 1, 1))
        c.restore()
        ellipse(k, px + 48, py + 8, 22, 30, (0.92, 0.74, 0.60), 3412, lw=2)               # his big hand round its side
        ellipse(k, px + 14, py + 54, 11, 8, (0.92, 0.74, 0.60), 3413, lw=1.6)              # the thumb, over DELETE


def _star(c, x, y, r):
    c.new_path()
    for j in range(10):
        rr = r if j % 2 == 0 else r / 2.3
        a = -math.pi / 2 + j * math.pi / 5
        (c.move_to if j == 0 else c.line_to)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    c.close_path(); c.set_source_rgb(0.98, 0.72, 0.10); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()


def dc_velvet():
    import dh_cast as dc
    return dc.VELVET


def under_shot(k, sh, heads):
    """UNDER THE CAR: his face up, lit from the lamp's side; the sump a hand above it. In frame units."""
    import of_cast as oc
    c = k.c
    c.set_source_rgb(0.16, 0.17, 0.19); c.paint()                                  # the car's underside
    sway = sh["state"].get("sway_v", 16 if sh["state"].get("sway") else 0)
    c.save(); c.translate(sway * 0.3, abs(sway) * 1.4); c.rotate(0.004 * sway)       # v6: it drops toward his face
    rect(k, 120, 230, 300, 120, (0.30, 0.30, 0.32), 3420, lw=2.6)                  # the sump
    c.set_source_rgb(*INK); c.set_line_width(5)
    for x in (60, 480):
        c.move_to(x, 140); c.line_to(x + 20, 380); c.stroke()
    c.restore()
    g = cairo.RadialGradient(470, 900, 20, 470, 900, 520)
    g.add_color_stop_rgba(0, 1.0, 0.92, 0.6, 0.55); g.add_color_stop_rgba(1, 1.0, 0.92, 0.6, 0.0)
    c.set_source(g); c.paint()
    heads["client"] = oc.client_lying(k, 1.6, sway=sway, wrench_up=True)


def insert_shot(k, sh):
    c = k.c
    kind = sh["state"].get("insert")
    if kind == "card":
        gs.insert_card(k)
    elif kind == "invite":
        gs.insert_invite(k)
    elif kind == "key":                                                            # the steering column, the key, his fingers
        c.set_source_rgb(0.16, 0.16, 0.18); c.paint()
        c.set_source_rgb(0.08, 0.08, 0.09); c.set_line_width(46); c.set_line_cap(1)
        c.new_path(); c.arc(330, 170, 300, 1.7, 3.0); c.stroke()                     # the wheel's rim, above
        rect(k, 90, 360, 330, 200, (0.22, 0.22, 0.24), 3430, lw=2.6)                   # the column's shroud
        ellipse(k, 300, 460, 56, 56, (0.62, 0.64, 0.66), 3431, lw=2.4)                 # the lock barrel
        gs.protect(c, "the key at START", 150, 300, 470, 660)
        ku = sh["state"].get("key_u", 1.0)                                            # stage 7: the turn; then the engine runs
        if sh["state"].get("run"):
            c.translate(sh["state"]["run"], 0)
        c.save(); c.translate(300, 460); c.rotate(-0.5 + 1.4 * ku)                     # the key, turned to START
        rect(k, -8, -100, 16, 100, (0.80, 0.80, 0.78), 3432, lw=2)
        ellipse(k, 0, -122, 34, 30, (0.30, 0.32, 0.36), 3433, lw=2.2)                  # its head
        c.restore()
        rect(k, 380, 520, 70, 40, (0.85, 0.65, 0.20), 3434, lw=2)                      # the key ring's tag
        a_ = -0.5 + 1.4 * ku                                                          # oily fingers ON the key head, turning it
        kx, ky = 300 + 122 * math.sin(a_), 460 - 122 * math.cos(a_)
        # v9 (22 Nov, decided): HIS arm, so it reads as the Client in this car: the oily forearm, the white T-shirt sleeve
        for col, lw in ((INK, 62), ((0.80, 0.62, 0.50), 56)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.move_to(kx + 26, ky + 14); c.line_to(640, 600); c.stroke()
        c.set_source_rgba(0.12, 0.10, 0.08, 0.45)                                    # oil on the forearm
        for i, (u_, w_) in enumerate(((0.3, 9), (0.5, 12), (0.65, 7))):
            c.arc(kx + 26 + (640 - kx - 26) * u_, ky + 14 + (600 - ky - 14) * u_ + (-8 if i % 2 else 6), w_, 0, 2 * math.pi); c.fill()
        c.save(); c.translate(kx + 26 + (640 - kx - 26) * 0.55, ky + 14 + (600 - ky - 14) * 0.55); c.rotate(math.atan2(600 - ky - 14, 640 - kx - 26))
        rect(k, -10, -44, 120, 88, (0.97, 0.97, 0.95), 3450, lw=2.6)                    # the white sleeve
        c.restore()
        c.save(); c.translate(452, 548)                                                 # his red rag, off the key ring
        cut(k, [(-8, -6), (16, -8), (24, 34), (6, 56), (-12, 40)], (0.82, 0.30, 0.22), 3451, lw=2)
        c.set_source_rgba(0.1, 0.08, 0.05, 0.4); c.arc(6, 24, 7, 0, 2 * math.pi); c.fill()
        c.restore()
        c.save(); c.translate(kx, ky); c.rotate(a_)
        for i, (dx, dy) in enumerate(((-30, 6), (-10, -10), (10, -12), (30, -4))):
            ellipse(k, dx, dy, 14, 28, (0.80, 0.62, 0.50), 3440 + i, lw=2)
            c.set_source_rgba(0.1, 0.08, 0.05, 0.5); c.arc(dx, dy + 10, 7, 0, 2 * math.pi); c.fill()
        c.restore()
        for i, (x0, txt) in enumerate(((150, "OFF"), (210, "ON"), (380, "START"))):
            gs.T(c, txt, x0, 640, 26, col=(0.95, 0.95, 0.90) if txt != "START" else (1.0, 0.75, 0.2))


def donnie_shot(k, sh, heads):
    """4.1: the doorway full of daylight, the black car outside; Father's hand walking out, the phone buzzing: DONNIE,
    turning face down."""
    import dh_cast as dc
    import of_cast as oc
    c = k.c
    gs.garage(k, burn=1.0, legs_out=0.0)
    c.save(); c.rectangle(20, F - 330, 180, 330); c.clip()                          # outside: the black car at the kerb
    cut(k, [(-10, F - 40), (10, F - 110), (70, F - 140), (170, F - 140), (230, F - 100), (240, F - 40)], (0.07, 0.07, 0.08), lw=2.4)
    c.set_source_rgb(0.30, 0.34, 0.40); c.rectangle(80, F - 130, 80, 28); c.fill()
    c.restore()
    c.set_source_rgba(1.0, 0.98, 0.88, 0.35); c.rectangle(20, F - 330, 180, 330); c.fill()
    st = sh["state"]
    c.save(); c.translate(132 + st.get("hand_dx", 0.0) + st.get("buzz", 0.0), 690)     # stage 7: walking out; it buzzes
    for col, lw in ((INK, 40), (dc.VELVET, 34)):                                     # his sleeve, velvet, going out
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(110, 60); c.line_to(24, 14); c.stroke()
    def scr(c_):
        c_.set_source_rgb(0.20, 0.70, 0.35); c_.rectangle(-19, -34, 38, 68); c_.fill()
        c_.set_source_rgb(1, 1, 1); c_.select_font_face("Lilita One"); c_.set_font_size(11)
        e = c_.text_extents("DONNIE"); c_.move_to(-e.x_advance / 2, 0); c_.show_text("DONNIE")
    oc.phone(k, 0, -10, 0.95, None if st.get("donnie_down") else scr, ang=-0.35)   # face down against his palm
    ellipse(k, 10, 22, 24, 18, dc.SKIN_F, 3441, lw=2)
    c.restore()


def desk_shot(k, sh, heads):
    import dh_layout as dl
    import of_cast as oc
    import pam_bc as pb
    which = sh["state"]["desk"]
    CH = dl.CH
    rs = sb_sc("robot")
    don_kw = dict(happy=dict(face="happy"), stiff=dict(face="neutral", look=(0.2, 1), pose=(-150, -110, 150, 110)),
                  panic=dict(face="panic", look=(0, -0.2), pose=(-40, 95, 30, 10), sweat=3, phone_dad=True, forward=1.0))

    drawn = {}                                                    # v7: the faces where the rigs drew them

    def don(k_, o):
        d = oc.don_throne(k_, CH[0], dl.FLOOR, CH[2], **dict(don_kw[sh["state"].get("don", "happy")], **sh["state"].get("don_over", {})))
        drawn["don"] = (d["head"][0], d["head"][1], 50 * CH[2])

    def robot(k_, o):
        if sh["state"].get("don_edge"):                                # 3.4 (v7): the throne slid in at the right edge
            c_ = k_.c
            c_.save(); c_.translate(dl.RX + DON_EDGE[0] - CH[0], 0)
            don(k_, o)
            c_.restore()
        else:
            don(k_, o)
        r = oc.robot(k_, dl.RX, F + 4, rs, turn=float(sh["state"].get("turn", 0.0)))
        heads["_screen"] = r["screen"]
        drawn["robot"] = (r["screen"][0], r["screen"][1], 50 * rs)

    def pam(k_, o):
        don(k_, o)
        q = pb.pam(k_, 652, F + 6, dl.PS, sh["state"].get("pam_pose", (-8, 0, 140, 60)), "neutral", look=sh["state"].get("pam_look", (0.4, 0.6)), glasses="up")
        heads["_pamhand"] = q["hands"][1]
        drawn["pam"] = (q["head"][0], q["head"][1], 50 * dl.PS)
    vis = visor_point()
    if which == "wide":
        def wide(k_, o):
            pam(k_, o); r = oc.robot(k_, dl.RX, F + 4, rs)
            drawn["robot"] = (r["screen"][0], r["screen"][1], 50 * rs)
        shot = dl.shot("3.1", [dl.h_seat(), vis, dl.hp(652, F + 6, dl.PS)], wide, "", rb=False, chair=False,
                       cam=(434, 640, 0.85))                     # v7: the OUT OF ORDER sign just out at the right
    elif which == "robot":
        shot = dl.shot("3.2", [vis], robot, "", rb=False, zmax=3.6, chair=False, cam=ROBOT_CAM[0] or cf.face_cam([vis], z_max=3.6))
    elif which == "don":
        shot = dl.shot("3.3", [dl.h_seat()], don, "", chair=False)
    else:
        shot = dl.shot("3.6", [dl.hp(652, F + 6, dl.PS)], pam, "", chair=False)
    cam = dl.draw(shot, k)
    DON_FAULTS[:] = don_rule({n: (CH[2] if n == "don" else rs if n == "robot" else dl.PS) for n in drawn})
    for name, h in drawn.items():
        if which == "wide" or name == which:
            heads[name] = h
    c = k.c
    z = cam[2]
    if sh["state"].get("visor") and "_screen" in heads:                          # the visor: one line
        sx, sy = heads.pop("_screen")
        x, y = (sx - cam[0]) * z + 270, (sy - cam[1]) * z + 480
        r = 50 * rs * z
        gs.protect(c, "WITHOUT HIM on the visor", x - 0.82 * r, y - 0.82 * r, x + 0.82 * r, y + 0.82 * r)
        c.set_source_rgb(0.08, 0.12, 0.22); c.arc(x, y, 0.82 * r, 0, 2 * math.pi); c.fill()
        gl = sh["state"].get("visor_glow", 0.0)                                  # stage 7: it glows as it talks
        if gl:
            g_ = cairo.RadialGradient(x, y, 0.1 * r, x, y, 0.82 * r)
            g_.add_color_stop_rgba(0, 0.35, 0.85, 0.95, 0.35 * gl); g_.add_color_stop_rgba(1, 0.35, 0.85, 0.95, 0.0)
            c.set_source(g_); c.arc(x, y, 0.82 * r, 0, 2 * math.pi); c.fill()
        vk = sh["state"].get("visor_k", 1.0)                                     # stage 7: the line pops on
        gs.T(c, "WITHOUT", x, y - 0.04 * r, 0.30 * r * vk, col=(0.35, 0.85, 0.95))
        gs.T(c, "HIM", x, y + 0.40 * r, 0.40 * r * vk, col=(0.35, 0.85, 0.95))
    heads.pop("_screen", None)
    if which == "pam" and "pam" in heads:                                              # v10: the desk in front of her
        px, py, pr = heads["pam"]
        X, Y = (px - cam[0]) * z + 270, (py - cam[1]) * z + 480
        dy = Y + 2.25 * pr * z
        DESK_Y[0] = dy
        rect(Ctx(c, 0), -20, dy, 580, 1000, (0.62, 0.48, 0.34), 3510, lw=2.6)
        c.set_source_rgb(0.72, 0.58, 0.42); c.rectangle(-20, dy, 580, 16); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2.6); c.move_to(-20, dy + 16); c.line_to(560, dy + 16); c.stroke()
    if "_pamhand" in heads and which != "pam":
        heads.pop("_pamhand")
    if "_pamhand" in heads:                                                          # her phone, held up: INVITATION
        hx, hy = heads.pop("_pamhand")
        x, y = (hx - cam[0]) * z + 270, (hy - cam[1]) * z + 480
        def scr(c_):
            c_.set_source_rgb(0.97, 0.94, 0.86); c_.rectangle(-19, -34, 38, 68); c_.fill()
            c_.set_source_rgb(0.55, 0.16, 0.46); c_.select_font_face("Lilita One"); c_.set_font_size(6.5)
            c_.move_to(-17, -14); c_.show_text("INVITATION")
            c_.set_source_rgb(*INK); c_.set_font_size(9); c_.move_to(-17, 6); c_.show_text("FATHER")
        bz = sh["state"].get("buzz", 0.0)                                          # stage 7: it buzzes; then face down
        down = sh["state"].get("phone_down", False)
        if down:                                                                   # v10: SLAPPED face down on the desk
            px_, py_ = x - 70, DESK_Y[0] + 6
            gs.protect(c, "the phone, face down", px_ - 44 * z * 0.55, py_ - 16, px_ + 44 * z * 0.55, py_ + 16)
            c.save(); c.translate(px_, py_); c.scale(z * 0.55, z * 0.55)
            rect(Ctx(c, 0), -44, -10, 88, 18, (0.08, 0.09, 0.12), 3502, lw=2.4)
            c.set_source_rgba(1, 1, 1, 0.25); c.rectangle(-40, -9, 76, 3); c.fill()
            c.set_source_rgb(0.3, 0.3, 0.32); c.arc(30, -2, 3, 0, 2 * math.pi); c.fill()     # the camera: its back
            c.restore()
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.set_line_cap(1)               # the slap
            for a in (-2.6, -1.9, -1.2):
                c.move_to(px_ + 60 * math.cos(a), py_ - 6 + 34 * math.sin(a)); c.line_to(px_ + 80 * math.cos(a), py_ - 6 + 46 * math.sin(a)); c.stroke()
        else:
            c.save(); c.translate(x + bz, y - 40); c.scale(z * 0.55, z * 0.55)
            oc.phone(Ctx(c, 0), 0, 0, 1.0, scr); c.restore()
    return cam


DESK_Y = [0.0]                                             # the desk top in 3.6 (screen y), for the phone slapped on it
ROBOT_CAM = [None]                                         # a camera forced on the robot shots (the planted fault)
_VIS = []


def visor_point():
    """the robot's visor in set units, where its rig draws it (a dry run on a scratch surface)."""
    if not _VIS:
        import dh_layout as dl
        import of_cast as oc
        rs = sb_sc("robot")
        r = oc.robot(Ctx(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)), 0), dl.RX, F + 4, rs)
        _VIS.append((r["screen"][0], r["screen"][1], 50 * rs))
    return _VIS[0]


DON_FAULTS = []                                            # the Don rule's faults for the last desk frame
DON_EDGE = [60]                                            # 3.4: how far right of the robot the throne slides in
ROBOT_S = 0.48                                             # v10 (22 Nov, decided): the front-desk set's canon (fs_set4.HOME);
                                                           # the storyboard's 0.40 made it a gnome beside the throne


# --- the series rule "DON is always the tallest and widest" (22 Nov, decided: checked wherever Don shares a frame) -------
UNIT_H = {"don": 358, "robot": 310, "pam": 331, "client": 458, "father": 366, "g1": 455, "g2": 455}
UNIT_W = {"don": 145, "robot": 132, "pam": 143, "client": 254, "father": 129, "g1": 218, "g2": 218}
# standing height and width at scale 1.0, measured from each rig's drawing (22 Nov: Don 215 px at 0.60, robot 149 at 0.48,
# Pam 179 at 0.54, the Client 238 and 132 wide at 0.52, Father 227 at 0.62, a bodyguard 255 at 0.56)


def don_rule(cast):
    """cast: {name: scale} for everyone in one frame. -> faults: anyone taller or wider than Don, standing, beside him."""
    if "don" not in cast:
        return []
    dh, dw = UNIT_H["don"] * cast["don"], UNIT_W["don"] * cast["don"]
    out = []
    for n, s_ in cast.items():
        if n == "don" or n not in UNIT_H:
            continue
        if UNIT_H[n] * s_ > dh + 1:
            out.append("DON RULE: %s is taller than Don (%d vs %d px at 1.0 zoom)" % (n, UNIT_H[n] * s_, dh))
        if UNIT_W[n] * s_ > dw + 1:
            out.append("DON RULE: %s is wider than Don (%d vs %d px)" % (n, UNIT_W[n] * s_, dw))
    return out


def don_rule_validate():
    """the check on a planted fault: the Client (0.52) beside Don (0.60) must fail; the office cast must pass."""
    office = {"don": 0.60, "robot": ROBOT_S, "pam": 0.54}
    planted = dict(office, client=0.52)
    ok = not don_rule(office) and any("client is taller" in m for m in don_rule(planted))
    print("don_rule: office", don_rule(office) or "pass", "| planted Client:", don_rule(planted))
    return ok


def sb_sc(n):
    import fs_storyboard as sb
    return ROBOT_S if n == "robot" else sb.SC[n]


BOXES = {"GARAGE 7": gs.SIGN, "the plan": (gs.PLAN[0] - 86, gs.PLAN[1] - 72, gs.PLAN[0] + 86, gs.PLAN[1] + 66)}


def box_state(cam, b):
    """whole in the picture, out of it, or CUT by an edge (the top bar is picture: a sign may sit under it whole)."""
    x0, y0 = gs.to_frame(cam, b[0], b[1]); x1, y1 = gs.to_frame(cam, b[2], b[3])
    if x1 <= 0 or x0 >= W or y1 <= 0 or y0 >= H:
        return "out"
    if x0 >= 0 and x1 <= W and y0 >= 0 and y1 <= H:
        return "whole"
    return "CUT"


def clear_boxes(cam, heads, y_min=210):
    """a wall sign cut by the frame: first the camera comes down until the sign is out above the frame; if that puts
    a face above y_min, it goes up until the sign is whole (when it fits across); else it closes in, a step at a
    time, until the sign can go out above with the faces still low enough."""
    fx, fy, z = cam

    def ok(c_):
        return all(box_state(c_, b) != "CUT" for b in BOXES.values())

    def faces_ok(c_):
        fr = [((h[0] - c_[0]) * c_[2] + 270, 480 + (h[1] - c_[1]) * c_[2], h[2] * c_[2]) for h in heads]
        return all(y_min <= y <= cf.BOTTOM - r and r <= x <= W - r for x, y, r in fr)
    if ok((fx, fy, z)):
        return (fx, fy, z)
    for zz in [z - 0.05 * i for i in range(0, 8)] + [z + 0.05 * i for i in range(1, 40)]:
        for d in range(0, 220, 20):                                           # or slide off the signs, to the left
            if faces_ok((fx - d, fy, zz)) and ok((fx - d, fy, zz)):
                return (fx - d, fy, round(zz, 3))
        for b in sorted(BOXES.values(), key=lambda b_: -b_[3]):
            out_fy = max(b_[3] for b_ in BOXES.values()) + 480 / zz + 1
            if faces_ok((fx, out_fy, zz)) and ok((fx, out_fy, zz)):
                return (fx, round(out_fy, 1), round(zz, 3))
            top_fy = min(b_[1] for b_ in BOXES.values()) + (480 - 2) / zz
            for fx2 in (fx, (gs.SIGN[0] + gs.SIGN[2]) / 2):
                if faces_ok((fx2, top_fy, zz)) and ok((fx2, top_fy, zz)):
                    return (round(fx2, 1), round(top_fy, 1), round(zz, 3))
    return (fx, fy, z)


def off_rail(cam, heads):
    """the faces that matter clear of the right-hand buttons: the camera slides right (the faces left), as long as the
    leftmost face stays whole in the frame and no wall sign gets cut."""
    fx, fy, z = cam
    for _ in range(60):
        fr = [((h[0] - fx) * z + 270, (h[1] - fy) * z + 480, h[2] * z) for h in heads]
        if not any(x > cf.RAIL[0] - 6 and cf.RAIL[1] <= y <= cf.RAIL[2] for x, y, r in fr):
            return (round(fx, 1), fy, z)
        if min(x - r for x, y, r in fr) < 4 or any(box_state((fx + 4 / z, fy, z), b) == "CUT" for b in BOXES.values()):
            break
        fx += 4 / z
    return (fx, fy, z)


def zone_check(boxes):
    """every declared story prop: what of it is in the picture stays out of the bottom quarter and the buttons."""
    out = []
    for name, x0, y0, x1, y1 in boxes:
        vx0, vy0, vx1, vy1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
        if vx1 - vx0 < 4 or vy1 - vy0 < 4:
            continue
        if vy1 > cf.BOTTOM + 2:
            out.append("ZONE: %s in the bottom quarter (%d-%d)" % (name, vy0, vy1))
        elif vx1 > cf.RAIL[0] + 2 and vy1 > cf.RAIL[1] and vy0 < cf.RAIL[2]:
            out.append("ZONE: %s under the right-hand buttons (x %d-%d, y %d-%d)" % (name, vx0, vx1, vy0, vy1))
    return out


# --- one frame: draw it, record its text, check it ---------------------------------------------------------------------
class TextRec(cairo.Context):
    """a context that keeps every text it shows (in its device units) for uz_check.check_signs."""
    def __init__(self, surf):
        super().__init__()
        self.texts = []

    def show_text(self, s):
        x, y = self.get_current_point()
        e = self.text_extents(s)
        pts = [self.user_to_device(x + e.x_bearing + dx, y + e.y_bearing + dy) for dx in (0, e.width) for dy in (0, e.height)]
        self.texts.append(dict(text=s, bbox=(min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts),
                                              max(p[1] for p in pts)), clip=(-1e9, -1e9, 1e9, 1e9)))
        return super().show_text(s)


def render(sh, scene):
    """-> (surface at 1080, the uz_check frame record, the camera)."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920)
    surf.set_device_scale(2, 2)
    del gs.PROTECT[:]
    c = TextRec(surf)
    c.set_source_rgb(1, 1, 1); c.paint()
    k = Ctx(c, 0)
    heads = {}
    cam = sh["cam"]
    if cam == "under":
        under_shot(k, sh, heads); cam = (270, 480, 1.0)
    elif cam == "insert":
        insert_shot(k, sh); cam = (270, 480, 1.0)
    elif cam == "desk":
        cam = desk_shot(k, sh, heads)
    elif sh["state"].get("insert") == "donnie":
        gs.frame(k, cam, draw=lambda k_: donnie_shot(k_, sh, heads))
    else:
        # pass 1, off the page: where the heads fall, then the camera; pass 2 through it
        tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)
        garage_shot(Ctx(cairo.Context(tmp), 0), sh, scene, heads, None)
        if cam == "wide":
            cam = gs.FRAME0
        elif isinstance(cam, list):
            z_max = sh["state"].get("zmax")
            cam = cf.face_cam([heads[n] for n in cam], z_max=z_max)
            cam = clear_boxes(cam, [heads[n] for n in sh["cam"]])
            cam = off_rail(cam, [heads[n] for n in sh["cam"]])
            if "fx" in sh["state"] and sh["cam"] == ["father"]:
                cam = (sh["state"]["fx"], cam[1], cam[2])
        if sh["state"].get("shake"):                              # stage 7: the SLAM jolts the camera
            cam = (cam[0] + sh["state"]["shake"], cam[1] + 0.6 * sh["state"]["shake"], cam[2])
        heads.clear()
        del gs.PROTECT[:]                                         # only pass 2, through the camera, counts
        gs.frame(k, cam, draw=lambda k_: garage_shot(k_, sh, scene, heads, cam))
    # the text in set units, for check_signs (it maps them through the camera itself)
    fx, fy, z = cam if isinstance(cam, tuple) else (270, 480, 1.0)
    text = []
    for t in c.texts:
        b = t["bbox"]
        x0, y0 = (b[0] - 270) / z + fx, (b[1] - 480) / z + fy
        x1, y1 = (b[2] - 270) / z + fx, (b[3] - 480) / z + fy
        text.append(dict(text=t["text"], bbox=(x0, y0, x1, y1), clip=t["clip"]))
    if sh["cam"] == "desk":                                    # v7: its signs are checked as the garage's are
        heads_set = {n: h for n, h in heads.items()}
    else:
        heads_set = dict(heads)
    if sh["cam"] in ("under", "insert") or sh["state"].get("insert") == "donnie":
        heads_set = {} if sh["cam"] == "insert" else heads_set
    f = dict(cam=cam, heads=heads_set, scene=dict(text=text), bubbles=[], shot=sh["id"])
    msgs = uz.check_signs(f) + (uz.check_scale(f) if sh["cam"] not in ("under", "insert") else [])
    if sh["cam"] == "desk":
        msgs += list(DON_FAULTS)
    if sh["cam"] == "desk":
        msgs += ["SIGN cut by the frame: %s" % n for n in ("portrait+plaque", "calendar") if cf.sign_state(cam, cf.SIGNS[n]) == "CUT"]
    if sh["cam"] not in ("under", "insert", "desk"):
        msgs += ["SIGN %s: %s" % (n, box_state(cam, b)) for n, b in BOXES.items() if box_state(cam, b) == "CUT"]
    msgs += zone_check(gs.PROTECT)
    msgs = [m for m in msgs if (sh["id"], m.split(" at ")[0]) not in KNOWN]
    return surf, f, cam, msgs


# --- what is generated -------------------------------------------------------------------------------------------------
def script(out):
    tm = _timing()
    t = 0.0
    L = ["# The Offer: the script, v6 (generated)", "",
         "UptimeZ Inc. · episode 13 · *Civil War* 1 of 5. **Generated from `src/of_scenes.py`; do not edit by hand** "
         "(series/production-process.md). The timing is the recorded takes' (`of_timing_v2.json`).", "",
         "## What changed against v4", ""] + ["- " + x for x in CHANGES] + [""]
    nshots = nlines = 0
    for title, where, scene, shots in SCENES:
        dur = sum(tm[s["id"]]["len"] for s in shots)
        m, sec = divmod(t, 60)
        L += ["## Scene %s · %d:%04.1f · %.1f s" % (title, m, sec, dur), "", where, "",
              "| Shot | At | s | Frame | Picture | Action → reaction | Line | Sound |", "|---|---|---|---|---|---|---|---|"]
        for s in shots:
            m, sec = divmod(t, 60)
            ar = " → ".join(x for x in (s["action"], s["reaction"]) if x)
            L.append("| %s | %d:%04.1f | %.2f | %s | %s | %s | %s | %s |" % (s["id"], m, sec, tm[s["id"]]["len"], s["size"],
                                                                             s["picture"], ar, s["line"], s["fx"]))
            t += tm[s["id"]]["len"]; nshots += 1; nlines += bool(s["line"])
        L.append("")
    L.insert(4, "**%.1f s, %d shots, %d lines.**" % (t, nshots, nlines))
    L.insert(5, "")
    open(out, "w").write("\n".join(L) + "\n")
    return t, nshots, nlines


def layout_sheet(scene_i, out):
    title, where, scene, shots0 = SCENES[scene_i]
    shots = []
    for sh in shots0:
        shots.append(sh)
        if sh.get("then"):
            shots.append(sh["then"])
    cols, tw, th = 4, 270, 480
    rows = (len(shots) + cols - 1) // cols
    SW, SH = 30 + cols * (tw + 30), 110 + rows * (th + 130)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, SW * 2, SH * 2); s.set_device_scale(2, 2)
    c = cairo.Context(s); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
    gs._label(c, "THE OFFER · layout v4 · scene %s · %s" % (title, where), 30, 44, 22)
    gs._label(c, "generated by of_scenes.py · each frame at 270 · red: the apps' zones · the checks are uz_check's (scale, signs)",
              30, 72, 14, col=(0.3, 0.3, 0.3))
    fails = []
    for i, sh in enumerate(shots):
        surf, f, cam, msgs = render(sh, scene)
        g = cairo.Context(surf); _zones(g)
        x = 30 + (i % cols) * (tw + 30); y = 100 + (i // cols) * (th + 130)
        c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(surf, 0, 0); c.paint(); c.restore()
        lines = textwrap.wrap("%s  %s · %s" % (sh["id"], sh["size"], _plain(sh["picture"])), 42)[:3]
        for j, ln in enumerate(lines):
            gs._label(c, ln, x, y + th + 18 + j * 16, 12)
        if sh["line"]:
            gs._label(c, sh["line"][:46], x, y + th + 70, 12, col=(0.2, 0.3, 0.6))
        fc = uz.faces(f)
        rmax = max([v[2] for v in fc.values() if 0 <= v[0] <= W and 0 <= v[1] <= H] or [0])
        verdict = ("OK" if not msgs else "FAIL: " + "; ".join(m.split(" at ")[0] for m in msgs)[:60])
        gs._label(c, "r %d · %s" % (rmax, verdict), x, y + th + 90, 12, col=(0.1, 0.45, 0.2) if not msgs else (0.8, 0.1, 0.1))
        fails += [(sh["id"], m) for m in msgs]
    s.write_to_png(out)
    return fails


def _zones(c):
    c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(1.5); c.set_dash([6, 4])
    c.move_to(0, cf.BOTTOM); c.line_to(W, cf.BOTTOM); c.stroke()
    c.rectangle(cf.RAIL[0], cf.RAIL[1], W - cf.RAIL[0], cf.RAIL[2] - cf.RAIL[1]); c.stroke(); c.set_dash([])
    c.set_source_rgba(0.1, 0.1, 0.1, 0.18); c.rectangle(0, 0, W, 96); c.fill()


def _plain(s):
    return s.replace("**", "")


def loop_check():
    """frame 0 (0.1) and the last frame (4.2): drawn by the same code, they may differ only inside the plan."""
    import numpy as np
    sh0 = SCENES[0][3][0]; sh1 = SCENES[-1][3][-1]
    a = render(sh0, SCENES[0][2])[0]; b = render(sh1, SCENES[-1][2])[0]
    A = np.ndarray((1920, 1080, 4), np.uint8, a.get_data()).astype(int)
    B = np.ndarray((1920, 1080, 4), np.uint8, b.get_data()).astype(int)
    d = np.abs(A - B)[..., :3].max(axis=2) > 8
    x0, y0 = gs.to_frame(gs.FRAME0, BOXES["the plan"][0], BOXES["the plan"][1])
    x1, y1 = gs.to_frame(gs.FRAME0, BOXES["the plan"][2], BOXES["the plan"][3])
    d[int(y0 * 2):int(y1 * 2) + 1, int(x0 * 2):int(x1 * 2) + 1] = False
    n = int(d.sum())
    inside = int((np.abs(A - B)[..., :3].max(axis=2) > 8).sum()) - n
    return n, inside


def main(out=OUT):
    os.makedirs(out, exist_ok=True)
    t, n, l = script(os.path.join(out, "the-offer-script-v6.md"))
    print("script v5: %.1f s, %d shots, %d lines" % (t, n, l))
    fails = []
    for i in range(len(SCENES)):
        p = os.path.join(out, "of_layout_s%d_v4.png" % (i + 1))
        fails += layout_sheet(i, p)
        print("wrote", p, flush=True)
    n, inside = loop_check()
    print("loop: %d px differ outside the plan, %d inside it (the burn)" % (n, inside))
    if n or not inside:
        fails.append(("0.1/4.2", "LOOP: frame 0 and the last frame differ outside the plan (%d px), or not at all inside" % n))
    for sid, m in fails:
        print("FAIL", sid, m)
    if fails:
        sys.exit(1)
    print("all layout frames pass")


if __name__ == "__main__" and not (len(sys.argv) > 1 and sys.argv[1] in ("board", "zones-validate", "don-validate")):
    main(sys.argv[1] if len(sys.argv) > 1 else OUT)


# --- stage 5: the board (one key frame per shot at 540, with its line) ------------------------------------------------
# Bubbles follow the series' lessons (docs/lessons.md 174, 325, 339, 357-363, 398): one table of lines (SAY, read from
# the shots above, so the board and the animation share it); First Search v36's speech() with the tip beside the mouth
# drawn in that frame and a curved tail round the outside of the head; never from above unless bare scalp; the robot
# in its own mono caps; and a check that reads the rendered pixels, not the numbers the tail was aimed with.
SPEAKERS = {"CLIENT": "client", "FATHER": "father", "ROBOT": "robot", "DON": "don"}


def say_table():
    out = {}
    for title, where, scene, shots in SCENES:
        for sh in shots:
            if sh["line"]:
                who, txt = sh["line"].split(":", 1)
                out[sh["id"]] = (SPEAKERS[who.strip()], txt.strip().strip('"'))
    return out


SAY = say_table()


def _skin_near(arr, x, y, rad=7):
    """the rendered frame has skin within rad px of (x, y) (a reddish light tone: the cast's faces)."""
    import numpy as np
    h, w = arr.shape[:2]
    x0, x1 = max(0, int(x - rad)), min(w, int(x + rad) + 1)
    y0, y1 = max(0, int(y - rad)), min(h, int(y + rad) + 1)
    p = arr[y0:y1, x0:x1, :3].astype(int)
    b, g, r = p[..., 0], p[..., 1], p[..., 2]                       # cairo's RGB24 is BGRx in memory
    return bool(((r > 150) & (r > g + 12) & (g > b + 8) & (r - b > 45)).any())


def board_frame(sh, scene, bubble=True):
    """-> (surface 540 x 960 at 2x, problems). The frame, its line's bubble, and the pixel check of the tail."""
    import numpy as np
    import fs_animatic as an
    MOUTH_AT.clear()
    surf, f, cam, msgs = render(sh, scene)
    if sh["id"] not in SAY or not bubble:
        return surf, msgs
    who, txt = SAY[sh["id"]]
    fc = uz.faces(f) if sh["cam"] not in ("under",) else {n: tuple(v) for n, v in f["heads"].items()}
    if sh["cam"] == "desk":                                           # the desk frame's heads are in set units already mapped
        fc = {n: ((v[0] - cam[0]) * cam[2] + 270, (v[1] - cam[1]) * cam[2] + 480, v[2] * cam[2]) for n, v in f["heads"].items()}
        fc = {("don" if n in ("don", "seat") else n): v for n, v in fc.items()}
    if who not in fc:
        return surf, msgs + ["BUBBLE: %s speaks but is not in the frame" % who]
    head = fc[who]
    if who == "robot":                                                # v7: the head point IS the visor, as drawn
        head = (head[0], head[1], head[2] * 1.15)
        fc[who] = head
    # the tip lands on the cheek beside the mouth (lesson 360: over the hair to skin): aim at a smaller face, so the
    # tip sits inside the face's edge; the bubble still keeps clear of the whole head
    tail = (head[0], head[1] + head[2] * 0.08, head[2] * TAIL_K.get(sh["id"], 0.72))
    if who in MOUTH_AT and sh["cam"] not in ("under", "insert", "desk"):    # the profile: the mouth at the front of the head
        mx, my = MOUTH_AT[who]
        mx, my = (mx - cam[0]) * cam[2] + 270, (my - cam[1]) * cam[2] + 480
        tail = (mx - 2, my - 3, 4)
    if sh["cam"] == "under":                                          # lying, head to the left: the mouth is to the right
        tail = (head[0] + 0.30 * head[2], head[1] - 0.50 * head[2], 10)  # of the face's middle; the tip on the cheek above it
    if who == "robot":                                                # to the visor's rim, never across its card
        tail = (head[0] - head[2] * 0.62, head[1] - head[2] * 0.62, 2)
    others = [v for n, v in fc.items() if n != who]
    before = np.ndarray((1920, 1080, 4), np.uint8, surf.get_data()).copy()
    c = cairo.Context(surf); c.scale(1, 1)
    k = Ctx(c, 0)
    box = an.speech(c, k, txt.upper() if who == "robot" else txt, head, others, mono=(who == "robot"), size=30,
                    tail_head=tail, top_tip_at=None)
    surf.flush()
    after = np.ndarray((1920, 1080, 4), np.uint8, surf.get_data())
    d = np.abs(after.astype(int) - before.astype(int))[..., :3].max(axis=2) > 30
    ys, xs = np.nonzero(d)
    bx0, by0, bx1, by1 = [v * 2 for v in box]
    dist = np.maximum(np.maximum(bx0 - xs, 0), np.maximum(xs - bx1, 0)) + np.maximum(np.maximum(by0 - ys, 0), np.maximum(ys - by1, 0))
    i = int(dist.argmax()) if len(dist) else None
    probs = list(msgs)
    if i is None or dist[i] < 6:
        probs.append("BUBBLE %s: no tail drawn" % sh["id"])
    else:
        tx, ty = xs[i] / 2.0, ys[i] / 2.0
        if who != "robot" and not _skin_near(before, xs[i], ys[i], 6):
            probs.append("TAIL %s: the tip (%d, %d) is not beside skin (hair, wall or collar)" % (sh["id"], tx, ty))
        hx, hy, r = head
        if who == "robot" and math.hypot(tx - hx, ty - hy) > 1.0 * r:
            probs.append("TAIL %s: the tip (%d, %d) is not on the visor" % (sh["id"], tx, ty))
        if who != "robot" and sh["cam"] != "under" and not (hy - 0.1 * r <= ty <= hy + 1.4 * r):
            probs.append("TAIL %s: the tip (%d, %d) is not at mouth height (face %d, %d, r %d)" % (sh["id"], tx, ty, hx, hy, r))
    x0, y0, x1, y1 = box
    if x0 < 18 or y0 < 96 or x1 > 522 or y1 > 720:
        probs.append("BUBBLE %s outside the safe area %s" % (sh["id"], tuple(round(v) for v in box)))
    for n, (hx, hy, r) in fc.items():                                  # no bubble over a face
        if x0 < hx + r * 0.8 and x1 > hx - r * 0.8 and y0 < hy + r * 0.8 and y1 > hy - r * 0.8:
            probs.append("BUBBLE %s over %s's face" % (sh["id"], n))
    return surf, probs


def app_overlay(c):
    """a plain mock of a short-video app over a 540 x 960 frame (no real app, no brand): the top bar, the column of
    buttons at the right, and the caption block at the bottom; what the viewer's phone covers."""
    c.save()
    c.set_source_rgba(0, 0, 0, 0.28); c.rectangle(0, 0, W, 70); c.fill()
    c.set_source_rgba(1, 1, 1, 0.85); c.select_font_face("Inter", 0, 1); c.set_font_size(17)
    c.move_to(170, 44); c.show_text("Following      For you")
    for i, y in enumerate((470, 560, 650, 740)):                                     # the buttons
        c.set_source_rgba(0, 0, 0, 0.30); c.arc(500, y, 24, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(1, 1, 1, 0.92); c.set_line_width(3); c.arc(500, y, 15, 0, 2 * math.pi); c.stroke()
        c.set_font_size(12); c.move_to(487, y + 42); c.show_text(("12.4K", "318", "Share", "")[i])
    c.set_source_rgba(1, 1, 1, 0.92); c.arc(500, 830, 22, 0, 2 * math.pi); c.fill()  # the sound disc
    g = cairo.LinearGradient(0, 720, 0, 960)                                          # the caption block
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.set_source(g); c.rectangle(0, 720, W, 240); c.fill()
    c.set_source_rgba(1, 1, 1, 0.92); c.set_font_size(18); c.move_to(20, 820); c.show_text("@uptimez")
    c.set_font_size(15)
    c.move_to(20, 850); c.show_text("He came to delete one post. #office #garage")
    c.move_to(20, 878); c.show_text("original sound")
    c.set_source_rgba(1, 1, 1, 0.5); c.rectangle(0, 948, W, 3); c.fill()            # the progress line
    c.restore()


def board(out=OUT, frames_dir="/tmp/of_board_v1"):
    """the board: every shot's key frame at 540 (in frames_dir) and two sheets at 270 with time, shot and line."""
    os.makedirs(frames_dir, exist_ok=True)
    tm = _timing()
    items, t, probs = [], 0.0, []
    for title, where, scene, shots in SCENES:
        for sh in shots:
            L = tm[sh["id"]]["len"]
            surf, p = board_frame(sh, scene)
            surf.write_to_png(os.path.join(frames_dir, "%s.png" % sh["id"]))
            items.append((t, sh["id"], surf)); probs += p
            if sh.get("then"):
                s2, p2 = board_frame(sh["then"], scene)
                items.append((t + L - 0.6, sh["id"] + " ins", s2)); probs += p2
            t += L
    half = (len(items) + 1) // 2
    for page, part in enumerate((items[:half], items[half:])):
        cols, tw, th = 7, 270, 480
        rows = (len(part) + cols - 1) // cols
        S = cairo.ImageSurface(cairo.FORMAT_RGB24, (cols * (tw + 12) + 12) * 2, (rows * (th + 46) + 70) * 2); S.set_device_scale(2, 2)
        c = cairo.Context(S); c.set_source_rgb(0.96, 0.95, 0.92); c.paint()
        gs._label(c, "THE OFFER · board v2 · %d of 2 · one key frame per shot, with its line, under a mock of the app's buttons and captions" % (page + 1), 12, 40, 22)
        for i, (tt, sid, img) in enumerate(part):
            x = 12 + (i % cols) * (tw + 12); y = 60 + (i // cols) * (th + 46)
            c.save(); c.translate(x, y); c.scale(0.5, 0.5); c.set_source_surface(img, 0, 0); c.paint()
            c.scale(1, 1); app_overlay(c); c.restore()
            gs._label(c, "%s   %d:%04.1f" % (sid, tt // 60, tt % 60), x, y + th + 22, 14)
        S.write_to_png(os.path.join(out, "of_board_v2_%d.png" % (page + 1)))
    return probs


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "board":
    ps = board()
    for p_ in ps:
        print("FAIL", p_)
    print("board: %d problems" % len(ps))
    sys.exit(1 if ps else 0)


def zones_validate():
    """the planted faults (series rule: a check counts once it has caught a known failure). Each must FAIL; the real
    shot must PASS."""
    import dh_layout as dl
    rows = []
    sh32 = [x for _, _, _, shots in SCENES for x in shots if x["id"] == "3.2"][0]
    vx, vy, vr = visor_point()
    _, _, real, m0 = render(sh32, 4)
    rows.append(("3.2 as framed", not [q for q in m0 if "robot" in q or "ZONE" in q], "must pass", m0))
    # the robot lowered: its visor at y 790 (the camera 110 set units higher at zoom 3.6)
    ROBOT_CAM[0] = (real[0], vy - (790 - 480) / real[2], real[2])
    try:
        _, f, cam, m1 = render(sh32, 4)
    finally:
        ROBOT_CAM[0] = None
    rows.append(("3.2 with the visor at y 790", any("robot" in q for q in m1) and any("ZONE" in q for q in m1), "must fail", m1))
    typed = (dl.ROBOT[1] - cam[1]) * cam[2] + 480                          # what the old typed head point would have said
    rows.append(("  (the typed head point says y %d: the old check passed it)" % typed, True, "", []))
    sh04 = [x for _, _, _, shots in SCENES for x in shots if x["id"] == "0.4"][0]
    _, _, _, m2 = render(dict(sh04, cam=(160, 860, 2.0)), 1)               # the camera slid left: the phone under the buttons
    rows.append(("0.4 with the phone under the buttons", any("ZONE" in q and "DELETE" in q for q in m2), "must fail", m2))
    ok = True
    for name, good, need, msgs in rows:
        print("%-58s %s %s" % (name, need, "OK" if good else "WRONG"))
        for q in msgs[:2]:
            print("      ", q)
        ok &= good
    return ok


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "zones-validate":
    sys.exit(0 if zones_validate() else 1)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "don-validate":
    sys.exit(0 if don_rule_validate() else 1)
