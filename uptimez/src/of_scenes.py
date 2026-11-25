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
    3: dict(father=(380, 884), g1=(596, F + 18), g2=(318, 868), client=(588, 872)),   # v48: g2 stays, at the wall behind his boss        # v6: bodyguard 1 right of the Client
    5: dict(),
}
LAMP_HELD = (516, 698)                                     # v9 (22 Nov): beside the bay, low, lighting the engine (not his face)
LAMP_HIGH = (482, 560)                                     # 2.3 v3: high over the bay, pointing down
FATHER_LAMP = (450, 640, 2.0)                              # Father's closes in scene 3: the plan whole above, the lamp man behind him
FX_LAMP = 410
LAMP_CAM = (505, 802, 1.20)                               # v48: wider: the second guard at the wall behind his boss
MED_CAM = (467, 772, 1.5)                                  # v48: the medium inside 2.1 and 2.4: room over Father's head for his line, the plan whole                                # 2.3 (v7): both men whole, the plan whole above them


# --- the shots -------------------------------------------------------------------------------------------------------
def S(id_, size, cam, picture, line="", action="", reaction="", cast=(), state=None, fx="", draw=None, then=None):
    """cam: (fx, fy, z) | "wide" | [names to frame by the series' rule] | "insert"."""
    return dict(id=id_, size=size, cam=cam, picture=picture, line=line, action=action, reaction=reaction,
                cast=tuple(cast), state=state or {}, fx=fx, draw=draw, then=then)


PLAN_FRAME = (426, 520, 1.75)
CAR_CAM = (350, 752, 1.40)                                 # 0.8 (v7): the car, its roof, the legs under it; the heavy at the left
ROOF_CAM = (128, 736, 1.45)                                # 0.8 / 0.10 (v6): the roof, the hand on it, the legs under it

TIMING = "of_timing_v26.json"                               # v9 (23 Nov): Father arrives, held

SCENES = [
    ("1 · The Legs", "The Client's garage, bay 7. Morning.", 1, [
        S("0.8", "MEDIUM", CAR_CAM, "**FRAME 0 (v8, the joke at 0:00).** MEDIUM on the car: Bodyguard 1's fist already up over the "
          "roof; it SLAMS down. **The car rocks on its stands over the legs underneath.** A stand scrapes.",
          action="the SLAM; the car rocks", reaction="the legs jolt", cast=("g1",), state=dict(lean=True, tilt=-0.045),
          fx="the slam; the stand scrapes"),
        S("0.9", "MEDIUM", CAR_CAM, "v13 (23 Nov, cold tests 3 of 3, decided): **0.8's FRAME, held**: the hand still on the roof, "
          "the voice from under the car, the tail into the dark by his hips. He doesn't roll out, doesn't raise his voice.",
          line='CLIENT: "Off the car."', action="the knee taps", reaction="the hand stays, for now", cast=("g1",),
          state=dict(voice_at=(300, 790))),
        S("0.10", "MEDIUM", CAR_CAM, "SAME FRAME as 0.8 (v8). **The hand snaps off the roof**, two drawings; he steps back. "
          "Only then does he look left, to Father.", action="the hand off at once", reaction="he looks to Father", cast=("g1",)),
        S("0.6", "CLOSE", ["father"], "CLOSE, Father. Eyes up from under his brows, chin down. No answer.",
          reaction="no answer", cast=("father",)),
        S("0.4", "HIGH", (318, 860, 2.0), "HIGH, over Father's shoulder, down at the legs. Bodyguard 1's sleeve holds the phone down: "
          "the one-star post, **DELETE POST**, his thumb over it.", action="the thumb hovers", reaction="the legs go on: a clank",
          state=dict(phone="delete"), fx="clank"),
        S("0.5", "CLOSE", "under", "UNDER THE CAR, from above (v10, the other view: 0.9 is the side): the whole of him on the "
          "creeper, the underside cut away over his chest, both hands up at a bolt. He doesn't look out.", state=dict(view="top"),
          line='CLIENT: "Is it wrong?"', action="he works", reaction="he doesn't look out"),
    ]),
    ("2 · The Lighter", "Same bay.", 2, [
        S("1.1", "TWO-SHOT", PLAN_FRAME, "GARAGE 7 painted, the plan, and bodyguard 2 behind the car. His finger to one square: "
          "**GARAGE 7**. He looks round at the real bay.", action="the finger on 7", reaction="he looks round at the bay",
          cast=("g2",)),
        S("1.2", "TWO-SHOT", PLAN_FRAME, "SAME FRAME. The gold lighter in his fist. CLICK: the flame under 7's corner. The paper "
          "browns. **Nobody says it.**", action="CLICK, the flame", cast=("g2",), state=dict(burn=0.4, flame=True),
          fx="CLICK; the radio alone; the paper crackles"),
        S("1.3", "WIDE", (322, 742, 1.45), "FRAME 0's frame. The creeper rolls out; the Client sits up, wipes his hands on a rag, looks at "
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
        S("2.1", "TWO-SHOT", MED_CAM, "Father and the Client, the car between them. Father speaks to him. "
          "**He has only ever spoken to Don.**", line='FATHER: "My son says his machine finds anything."',
          cast=("father", "client"), state=dict(bubble_over=True, bonnet=1.0, burn=1.0)),
        S("2.2", "CLOSE", (560, 780, 2.9), "CLOSE, the Client, back under the bonnet, not looking up.",
          line='CLIENT: "It found nothing."', cast=("client",), state=dict(bonnet=1.0, burn=1.0)),
        S("2.3", "MEDIUM", LAMP_CAM, "MEDIUM on the handover (v2). Without looking he holds the lamp out behind him; bodyguard 1 "
          "takes it unasked and holds it over the engine. **He is a garage hand now.**", action="the lamp, handed back",
          reaction="bodyguard 1 takes it", cast=("father", "client", "g1", "g2"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.3b", "CLOSE", FATHER_LAMP, "CLOSE, Father, watching that. A long look; his eyes go from the lamp to the Client. "
          "**This is when he decides.**", reaction="he decides", cast=("father", "client", "g1"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.4", "CLOSE", FATHER_LAMP, "CLOSE, Father, the bodyguard with the lamp behind him.",
          line='FATHER: "How would you run his company?"', cast=("father", "client", "g1"), state=dict(bubble_over=True, bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.5", "CLOSE", ["client"], "CLOSE, the Client. He straightens up. Checks the watch.", line='CLIENT: "Without him."',
          action="the watch", cast=("client",), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.6a", "CLOSE", FATHER_LAMP, "CLOSE, Father. HELD, silent. He weighs it. Nothing moves.", reaction="nothing moves",
          cast=("father", "client", "g1"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.6", "CLOSE", FATHER_LAMP, "SAME FRAME. Business.", line='FATHER: "And then?"', cast=("father", "client", "g1"),
          state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.7", "MEDIUM", (560, 846, 2.0), "MEDIUM. The Client takes his phone from his top pocket, wipes it on his trousers, turns it "
          "round.", action="the phone, turned round", cast=("client",), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, zmax=1.9)),
        S("2.8", "INSERT", "insert", "INSERT, the phone, filling the frame: one contact card. **PAM — finds things.**",
          state=dict(insert="card")),
        S("2.8b", "CLOSE", ["client"], "CLOSE, the Client, phone still held out. His terms from episode 9, now for her.",
          line='CLIENT: "One month. I ask. She finds it."', cast=("client",), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP)),
        S("2.8c", "TWO-SHOT", ["father", "client"], "TWO-SHOT. Father nods once. That is all.", line='FATHER: "Done."',
          action="one nod", cast=("father", "client", "g1"), state=dict(bonnet=1.0, burn=1.0, lamp_held=True, fx=FX_LAMP,
          moved=dict(g1=(900, F + 18)))),          # v12 (23 Nov audit): his head was stacked on the Client's
        S("2.8d", "MEDIUM", ["client"], "MEDIUM, the car. The Client drops the bonnet: SLAM. Wipes it once with the rag.",
          action="SLAM", cast=("father", "client", "g1"), state=dict(bonnet=0.0, burn=1.0, lamp_held=True, zmax=1.5,
          moved=dict(g1=(770, F + 18))), fx="SLAM"),      # v13 (cold test 3 of 3: "grabbing him from behind"): a step away
        S("2.8e", "INSERT", "insert", "INSERT, the ignition, his oily fingers on the key. It turns; the engine coughs, catches, "
          "runs: **he fixed it.**", action="the key turns", reaction="the engine runs", state=dict(insert="key"),
          fx="the engine drowns the radio"),
        S("2.8f", "CLOSE", (470, 680, 1.8), "1.1's FRAME (the plan above him, the burn on 7): bodyguard 1, still holding the lamp over a shut bonnet. Nothing left to light.",
          reaction="he keeps holding it", cast=("g1",), state=dict(bonnet=0.0, burn=1.0, lamp_held=True)),
        S("2.9", "MEDIUM", ["father"], "MEDIUM. Father, on his way to the door, without turning his head, to bodyguard 2, "
          "who thumbs a calendar entry.", line='FATHER: "Put it in the calendar."', action="the thumb on the phone", cast=("father", "g2"),
          state=dict(bonnet=0.0, burn=1.0, phone2=True, zmax=2.3, moved=dict(father=(214, 880), g2=(120, 872)))),   # v12: zmax 1.7 -> 2.3
    ]),
    ("4 · The Calendar", "The front desk, UptimeZ. The same minute.", 4, [
        S("3.0", "EXT", "insert", "v9 (23 Nov): **UptimeZ Inc.**, the glass doors, the logo on the glass, the lobby lit behind. "
          "The calendar's chime starts here.", fx="chime", state=dict(insert="uptimez")),
        S("3.1", "WIDE", "desk", "HARD CUT. THE FRONT DESK, wide: Don on the throne, feet up, the crown behind his head; the robot "
          "at its station by the door; Pam at the counter. A cheerful **chime**.", fx="chime", state=dict(desk="wide")),
        S("3.2", "CLOSE", "desk", "CLOSE, the robot. Its visor: one line, **WITHOUT HIM**. Delighted.",
          line='ROBOT: "New meeting. Agenda: without him."', state=dict(desk="robot", visor=True)),
        S("3.3", "CLOSE", "desk", "CLOSE, Don on the throne. He has sat up for good news. The smile stays on.",
          line='DON: "Without who?"', state=dict(desk="don", don="happy")),
        S("3.4", "CLOSE", "desk", "CLOSE, the robot. **ITS HEAD TURNS, SLOWLY**, to Don. Still smiling. **The peak: hold it.**",
          action="the head turns", state=dict(desk="robot", turn=True)),
        S("3.4b", "CLOSE", "desk", "v9: CLOSE, the robot, turned to Don, still smiling. It doesn't say who.",
          line='ROBOT: "Calendar says... wait."', state=dict(desk="robot", turn=True, don_edge=True)),   # v10 (Tomas, 0:49:
          # "he flies away, only the robot is left"): the throne stays where 3.4 slid it in; the robot is turned TO him
        S("3.5", "CLOSE", "desk", "CLOSE, Don, as 3.3. He follows the look down, to himself. The smile goes in one drawing.",
          reaction="the smile goes", state=dict(desk="don", don="stiff")),
        S("3.5b", "CLOSE", "desk", "v9: CLOSE, Don, as 3.3. He turns to the counter, to Pam. Nobody has told him.",
          line='DON: "Pam?"', state=dict(desk="don", don="stiff")),
        S("3.6", "CLOSE", "desk", "CLOSE, Pam at the counter. Her phone buzzes: **INVITATION, from FATHER**. She reads it, looks "
          "at Don, turns the phone **face down**. (Inside its 1.4 s: 0.45 s on the phone, filling the frame; then face down, held 0.6 s.)",
          action="the phone, face down", fx="buzz", state=dict(desk="pam"),
          then=S("3.6 insert", "INSERT", "insert", "the phone: INVITATION, from FATHER", state=dict(insert="invite"))),
        S("3.6b", "CLOSE", "desk", "v9: CLOSE, the robot's visor: **MEETING IN 4:59**, 4:58. Ticking.",
          action="the countdown", fx="tick", state=dict(desk="robot", turn=True, visor=True, count=299)),
        S("3.7", "CLOSE", "desk", "CLOSE, Don, as 3.3. He calls DAD. It rings. And rings. Nobody answers. The sweat comes back.",
          action="he dials DAD", state=dict(desk="don", don="panic")),
    ]),
    ("5 · Frame 0", "The garage.", 5, [
        S("4.1", "INSERT", (112, 640, 1.9), "INSERT, the doorway, the bright street. Father's hand, walking out, the phone buzzing: "
          "DONNIE. He turns it face down against his palm without stopping.", action="face down", state=dict(insert="donnie")),
        S("4.2", "MEDIUM", CAR_CAM, "HARD CUT. **0.8's FRAME** (v8): the bodyguard, alone, holding the work lamp down for the legs "
          "under the car. Father gone. The burn mark on GARAGE 7. Then frame 0's fist slams the roof again: the loop.",
          action="he holds the lamp", cast=("g1",), state=dict(burn=1.0, lamp_up=True, moved=dict(g1=(206, 862))),
          fx="the car pulls away; the radio runs on"),
    ]),
]

KNOWN = {}   # (shot, check text) -> why it is allowed. None yet.


# --- drawing ---------------------------------------------------------------------------------------------------------
def _timing_total():
    return json.load(open(os.path.join(OUT, TIMING)))["total"]


def _timing():
    d = json.load(open(os.path.join(OUT, TIMING)))
    return {s["shot"]: s for s in d["shots"]}


# --- the key poses (layout v2): what each shot's action looks like at its extreme ------------------------------------
# per shot: name -> what that person does. Targets are set points or names resolved in _pt(); the Client's poses are
# stand-ins until Tomas's redraw.
POSES = {
    "0.3": dict(),
    "0.4": dict(g1=dict(phone="delete")),
    "0.6": dict(father=dict(face="low", look=(1, 0))),
    "0.8": dict(g1=dict(targets=["roof"], push=True)),          # hand flat on the roof, arm out
    "0.10": dict(g1=dict(targets=["off_l", "off_r"], turn=-1.0, back=26)),
    "4.2": dict(g1=dict(targets_xy=[(264, 792)], lamp=True, lamp_ang=3.0)),       # v8: the lamp held down for the legs
    "1.1": dict(g2=dict(targets=["bay7_point"], point=True)),
    "1.2": dict(g2=dict(targets=["lighter"], lighter=1.0)),
    "1.3": dict(father=dict(look=(1, 0)), g2=dict(targets=["lighter"], lighter=1.0), client=dict(kind="sit", look=(1, -0.6))),
    "1.4": dict(client=dict(kind="sit", look=(-1, -0.2))),
    "1.5": dict(g2=dict(targets=["lighter"], lighter=1.0, turn=-1.0)),
    "1.6": dict(father=dict(face="brow", look=(1, -0.2))),
    "1.7": dict(g2=dict(turn=-1.0)),          # v5 (23 Nov): the lighter is the veto's front_lighter now; its old second copy hid behind his sleeve
    "2.1": dict(father=dict(face="hard", look=(1, 0)), client=dict(kind="bent")),   # v2: the mouth from the take
    "2.2": dict(client=dict(kind="bent")),
    "2.3": dict(father=dict(look=(1, -0.2)), client=dict(kind="bent", hand_back=True), g1=dict(targets=["handoff"])),
    "2.3b": dict(client=dict(kind="bent"), father=dict(look=(1, -0.5)), g1=dict(targets=["lamp"], lamp="held")),
    "2.4": dict(client=dict(kind="bent"), father=dict(face="hard", look=(1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.5": dict(client=dict(kind="watch", look=(1.9, 2.0), face="glance")),
    "2.6a": dict(client=dict(kind="bent"), father=dict(face="hard", look=(1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.6": dict(client=dict(kind="bent"), father=dict(face="hard", look=(1, 0)), g1=dict(targets=["lamp"], lamp="held")),
    "2.7": dict(client=dict(kind="pocket", look=(-0.4, 0.8))),
    "2.8b": dict(client=dict(kind="phone_out", look=(-1, 0))),
    "2.8c": dict(father=dict(face="low", look=(1, 0)), client=dict(kind="phone_out", look=(-1, 0)), g1=dict(targets_xy=[(840, 700)], lamp="held")),   # v14: out of the frame, to the right
    "2.8d": dict(father=dict(face="low", look=(1, 0)), client=dict(kind="slam"), g1=dict(targets_xy=[(780, 690)], lamp="held")),   # v13: he has stepped back with it
    "2.8f": dict(g1=dict(targets=["lamp"], lamp="held")),
    "2.9": dict(father=dict(look=(1, 0)), g2=dict(targets=["chest_l"], phone="calendar")),
}


def _pt(name, x, f):
    c_ = gs.CAR_X
    return {"roof": (x + 82, 650), "bay7_point": (gs.bay7()[0] - 12, gs.bay7()[1] - 14),
            "lighter": (gs.bay7()[0] + 2, gs.bay7()[1] + 92), "lamp": LAMP_HELD, "handoff": (600, 640),
            "chest_l": (x + 36, f - 118), "off_l": (x - 22, f - 118), "off_r": (x + 26, f - 120)}[name]


BENT_AT = (580, 836)                                      # the Client bent over the bay: x, and his feet (hidden by the car)
TAIL_K = {"2.9": 0.45}                                     # stage 7: a small face in a wide frame: the tip further in
SPEECH = [True]                                            # v40 (24 Nov, decided): the repo speech.py bubble (Offer settings in board_frame); off = the v39 bubbles (tag uptimez-the-offer-v39)
MOUTH_AT = {}                                              # mouths a pose knows better than the face point (the profile)


LIGHT = [True]     # v41 (24 Nov, Tomas: "flat colours, no light"): contact shadows and the room's light (grade)
SHADOW_W = dict(father=40, g1=46, g2=46, client=42, don=40, pam=34, robot=34)


def _contact_shadow(k, n, scene, sh):
    """a soft dark ellipse on the floor under his feet, drawn before him."""
    if not LIGHT[0]:
        return
    st = sh["state"]
    if n == "client" and (st.get("sit") or scene in (1, 2, 3) and not st.get("front_of_car")):
        return                                                       # under the car, on the creeper, or bent in behind its wing
    pos = dict(BLOCK[0] if st.get("doorway") else BLOCK[scene], **st.get("moved", {}))
    if n not in pos:
        return
    x, f = pos[n]
    if f < F - 6:
        return
    w = SHADOW_W.get(n, 38)
    c = k.c
    c.save(); c.translate(x, f + 3); c.scale(w, 8)
    g = cairo.RadialGradient(0, 0, 0.2, 0, 0, 1.0)
    g.add_color_stop_rgba(0, 0.04, 0.04, 0.07, 0.34); g.add_color_stop_rgba(1, 0.04, 0.04, 0.07, 0.0)
    c.set_source(g); c.arc(0, 0, 1.0, 0, 2 * math.pi); c.fill(); c.restore()


def grade(c, scene):
    """the room's light over the whole frame, under the bubbles: a darker ceiling and corners, a warm pool where the
    light is, the floor darker toward us. Subtle: the drawing stays flat-coloured, it just stops being evenly lit."""
    if not LIGHT[0]:
        return
    office = scene == 4
    c.save(); c.identity_matrix()
    g = cairo.LinearGradient(0, 0, 0, 300)
    g.add_color_stop_rgba(0, 0.05, 0.05, 0.08, 0.10 if office else 0.22); g.add_color_stop_rgba(1, 0.05, 0.05, 0.08, 0.0)
    c.set_source(g); c.rectangle(0, 0, 540, 300); c.fill()
    g = cairo.LinearGradient(0, 760, 0, 960)
    g.add_color_stop_rgba(0, 0.05, 0.05, 0.08, 0.0); g.add_color_stop_rgba(1, 0.05, 0.05, 0.08, 0.12 if office else 0.20)
    c.set_source(g); c.rectangle(0, 760, 540, 200); c.fill()
    g = cairo.RadialGradient(270, 470, 230, 270, 470, 640)
    g.add_color_stop_rgba(0, 0.04, 0.04, 0.07, 0.0); g.add_color_stop_rgba(1, 0.04, 0.04, 0.07, 0.20 if office else 0.34)
    c.set_source(g); c.paint()
    g = cairo.RadialGradient(270, 380, 10, 270, 380, 330)
    w_ = (1.0, 0.92, 0.70) if not office else (1.0, 0.96, 0.86)
    g.add_color_stop_rgba(0, w_[0], w_[1], w_[2], 0.10); g.add_color_stop_rgba(1, w_[0], w_[1], w_[2], 0.0)
    c.set_source(g); c.paint()
    c.restore()


def _cast_draw(k, n, scene, sh, heads):
    """v2 (23 Nov, decided: no frozen frames): every cast member breathes; his head point follows. v3 (24 Nov, decided):
    the breath lifts the chest, shoulders and head (above the hips) and the legs stand; a speaker's head and shoulders
    dip a little on a stressed syllable. The figure is drawn ONCE into a group and painted in two parts."""
    _contact_shadow(k, n, scene, sh)
    b_ = _oc.breath(n)
    who_, acc_ = _oc.ACCENT[0]
    dip = 2.2 * acc_ if (who_ == n and _oc.LIVE[0]) else 0.0
    if not b_ and not dip:
        return _cast_draw0(k, n, scene, sh, heads)
    pos = dict(BLOCK[0] if sh["state"].get("doorway") else BLOCK[scene], **sh["state"].get("moved", {}))
    x, f = pos.get(n, (0, F))
    c = k.c
    if not _oc.LIVE[0]:
        c.save(); c.translate(x, f); c.scale(1.0, 1.0 + b_); c.translate(-x, -f)
        try:
            r = _cast_draw0(k, n, scene, sh, heads)
        finally:
            c.restore()
        if n in heads:
            hx_, hy_, hr_ = heads[n]
            heads[n] = (hx_, f + (hy_ - f) * (1.0 + b_), hr_)
        return r
    c.push_group()
    try:
        r = _cast_draw0(k, n, scene, sh, heads)
    finally:
        pat = c.pop_group()
    hy0 = heads[n][1] if n in heads else f - 300
    hip = f + (hy0 - f) * 0.42                                   # about the belt
    c.save(); c.rectangle(-5000, hip, 10000, 10000); c.clip(); c.set_source(pat); c.paint(); c.restore()
    c.save(); c.rectangle(-5000, -10000, 10000, 10000 + hip + 0.5); c.clip()
    c.translate(x, hip); c.scale(1.0, 1.0 + b_ * (f - hip) / max(1.0, hip - hy0) * 2.2); c.translate(-x, -hip)
    c.translate(0, dip)
    c.set_source(pat); c.paint(); c.restore()
    return r                                                     # heads[n] stays the still head: the camera and the bubble don't swim


def _cast_draw0(k, n, scene, sh, heads):
    import dh_cast as dc
    import of_cast as oc
    st = sh["state"]
    ps = POSES.get(sh["id"], {}).get(n, {})
    pos = dict(BLOCK[0] if st.get("doorway") else BLOCK[scene], **st.get("moved", {}))
    c = k.c
    if n == "father":
        x, f = pos["father"]
        x += st.get("fshake", 0.0)
        tgs = list(ps.get("targets_xy") or ())
        if ps.get("show_hand") and tgs:                                      # v14 (Tomas at 0:20): his gesture is the point: no bubble on it
            gs.protect(c, "his open hand", tgs[0][0] - 22, tgs[0][1] - 26, tgs[0][0] + 22, tgs[0][1] + 22)
        if ps.get("guard_lighter"):                                          # v10 (23 Nov): the guard's own arm over the roof, the lighter in its hand
            gt, gfl, glid, gexp = ps["guard_lighter"]
            gx_, gf_ = pos["g2"]
            gpo = POSES.get(sh["id"], {}).get("g2", {})
            gx_ -= gpo.get("back", 0)
            H, _ = oc.guard_arm_front(k, gx_, gf_, GS, scene == 2, gt, (0.92, 0.74, 0.60), hand=False, from_elbow=False)
            gs.protect(c, "the lighter", H[0] - 14, H[1] - LIGHTER_LIFT - 40, H[0] + 14, H[1] - 4)
            fx_, fy_ = held_lighter(k, H[0], H[1], gfl, glid, (0.92, 0.74, 0.60))
            ox_, oy_ = fx_ - gexp[0], fy_ - gexp[1]                           # where the lid really is: his palm goes there
            tgs = [(a_ + ox_, b_ + oy_) for a_, b_ in tgs]
            ps = dict(ps, targets_xy=tgs)
        hk = _kit.HAND[0]
        if ps.get("palm") and ps.get("targets_xy"):                          # v5: the flat palm below IS his hand; ONLY that hand
            pd_ = c.user_to_device(*ps["targets_xy"][0]); pt_ = math.hypot(*c.user_to_device_distance(30, 0))
            def _pskip(k_, hx_, hy_, *a_):
                dx_, dy_ = k_.c.user_to_device(hx_, hy_)
                return None if math.hypot(dx_ - pd_[0], dy_ - pd_[1]) < pt_ else hk(k_, hx_, hy_, *a_)
            _kit.HAND[0] = _pskip
        dc.FATHER_STEP[0] = st.get("father_step")                                # v1 (23 Nov): his feet, when he walks
        ln_ = ps.get("lean", 0.0)                                                # v1 (23 Nov audit, decided): a weight shift,
        if ln_:                                                                  # the whole man tilted about his feet
            c.save(); c.translate(x, f); c.rotate(ln_); c.translate(-x, -f)
        try:
            draw_f = lambda: oc.father(k, x, f, FS, face=ps.get("face", "hard"), look=ps.get("look", (1, 0)), targets=ps.get("targets_xy", ()))
            if ps.get("phone_donnie") and ps.get("targets_xy"):                  # v2 (hand audit): the phone's hand is the only one there
                w_ = ps["targets_xy"][0]
                o = oc.held(k, draw_f, lambda o_: [min(o_.get("hands") or [w_], key=lambda h: (h[0] - w_[0]) ** 2 + (h[1] - w_[1]) ** 2)])
            else:
                o = draw_f()
        finally:
            dc.FATHER_STEP[0] = None
            _kit.HAND[0] = hk
            if ln_:
                c.restore()
        hx0_, hy0_ = o["head"]
        if ln_:
            hx0_, hy0_ = (x + (hx0_ - x) * math.cos(ln_) - (hy0_ - f) * math.sin(ln_),
                          f + (hx0_ - x) * math.sin(ln_) + (hy0_ - f) * math.cos(ln_))
        heads[n] = (hx0_, hy0_, 50 * FS)
        if ps.get("phone_donnie") and ps.get("targets_xy"):                  # v1 (23 Nov): DONNIE calling, in his hand, he looks at it
            want = ps["targets_xy"][0]
            hx, hy = min(o.get("hands") or [want], key=lambda h: (h[0] - want[0]) ** 2 + (h[1] - want[1]) ** 2)
            def scr_d(c_):
                import of_ui as ui
                ui.hand(c_, ui.call, "DONNIE")
            oc.phone_grip(k, hx + ps.get("buzz", 0.0), hy, 0.42, scr_d, ang=-0.15, skin=dc.SKIN_F, body_x=x)
        if ps.get("palm") and ps.get("targets_xy"):                          # v6 (23 Nov, motion_on3's hand): palm and fingers in ONE
            hx, hy = ps["targets_xy"][0]                                         # shape, flat across the lid, the fingers pointing on, a thumb
            sk = dc.SKIN_F
            c.save(); c.translate(hx + 5, hy); c.scale(0.95, 0.95)                # v7 (audit: "the guard's hand"): from HIS cuff, short of the sleeve
            c.new_path(); c.move_to(-8, -7); c.curve_to(4, -10, 18, -9, 21, -3); c.curve_to(22, 3, 16, 7, 2, 7); c.line_to(-8, 7); c.close_path()
            c.set_source_rgb(*sk); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke()
            c.set_source_rgb(*INK); c.set_line_width(1.3); c.set_line_cap(1)
            for y0, x0, x1 in ((-4.5, 9, 19), (-0.5, 9, 20), (3.5, 9, 17)):        # three fingers' seams
                c.move_to(x0, y0); c.line_to(x1, y0); c.stroke()
            c.new_path(); c.move_to(-2, 6); c.curve_to(2, 12, 9, 12, 9, 6)          # the thumb, down the near side
            c.set_source_rgb(*sk); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.8); c.stroke()
            c.new_path(); c.arc(4, -6, 3.2, 0, 2 * math.pi)                          # his red ring, on top: his hand
            c.set_source_rgb(0.80, 0.10, 0.12); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.2); c.stroke()
            c.restore()
    elif n in ("g1", "g2"):
        x, f = pos[n]
        x -= ps.get("back", 0)
        behind = (((n == "g2" and scene == 2) or (n == "g1" and scene == 3)) and n not in st.get("front_of_car", ())) \
            or n in st.get("behind_car", ())
        flip = behind
        tg = ps.get("targets_xy") or [_pt(t, x, f) for t in ps.get("targets", [])]
        if ps.get("lamp_dx") or ps.get("lamp_dy"):                               # v1 (23 Nov audit): 2.8f's search, the lamp moved
            tg = [(tg[0][0] + ps.get("lamp_dx", 0.0), tg[0][1] + ps.get("lamp_dy", 0.0))] + list(tg[1:])
        hk = _kit.HAND[0]
        HELD_AT[0] = None
        CABLE_DONE[0] = False
        if tg and ps.get("lamp") == "held" and ps.get("cable_behind", True):
            la0 = ps.get("lamp_ang", LAMP_ANG)                                    # v12 (24 Nov): the cable BEHIND him: it drops from the
            lw0 = ps.get("lamp_xy") or tg[0]                                      # handle's end, and his arm, body and legs cover it
            gs.lamp_cable(k, lw0[0] + 16 * math.cos(la0), lw0[1] + 16 * math.sin(la0), la0, ps.get("cable_floor", F + 8), ps.get("cable_swing", 0.0))
            CABLE_DONE[0] = True
        if tg and (ps.get("lamp") or "lighter" in ps):                       # v11 (23 Nov, audit: "a fist with a second hand under it"):
            lw_ = ps.get("lamp_xy") or tg[0]                                     # the hand that holds it is the grip's own; the other stays
            td_ = c.user_to_device(*lw_); tol_ = math.hypot(*c.user_to_device_distance(30, 0))   # in DEVICE space: the rigs call the
            def _skip(k_, hx_, hy_, *a_):                                                         # hook in their own local units
                dx_, dy_ = k_.c.user_to_device(hx_, hy_)
                if math.hypot(dx_ - td_[0], dy_ - td_[1]) < tol_:
                    HELD_AT[0] = (dx_, dy_)                                      # where his arm REALLY ends (device)
                    return None
                return hk(k_, hx_, hy_, *a_)
            _kit.HAND[0] = _skip
        oc.ELBOW_LOW[0] = bool(ps.get("elbow_low"))
        oc.TURN_DOWN[0] = ps.get("look_down", 0.0)
        try:
            tn_ = ps.get("turn", 0.0)                                            # v3 (cold test 3 of 3: "the suits never move"):
            sp_ = SAY.get(sh["id"], (None,))[0]                                  # a guard LISTENS: his head toward whoever speaks
            if not tn_ and sp_ in pos and sp_ in sh.get("cast", ()) and "turn" not in ps and abs(pos[sp_][0] - x) > 60:
                tn_ = 0.55 if pos[sp_][0] > x else -0.55
            draw_g = lambda: oc.guard(k, x, f, GS, flip=flip, targets=tg, turn=tn_, seed=1600 if n == "g1" else 1640)
            gl_ = POSES.get(sh["id"], {}).get("father", {}).get("guard_lighter") if n == "g2" else None
            if ps.get("phone") in ("calendar", "pam") and tg:                    # v2 (hand audit): one hand per wrist
                o = oc.held(k, draw_g, lambda o_: [tg[0]])
            elif "lighter" in ps and tg:                                         # the lighter's fist is that hand, even when the
                o = oc.held(k, draw_g, lambda o_: [min(o_.get("hands") or [tg[0]],   # target is out of reach (the skip above misses it)
                                                          key=lambda h: (h[0] - tg[0][0]) ** 2 + (h[1] - tg[0][1]) ** 2)])
            elif gl_:                                                            # the lighter's fist (drawn with Father) is his hand
                o = oc.held(k, draw_g, lambda o_: [gl_[0]] + [h for h in (o_.get("hands") or []) if math.hypot(h[0] - gl_[0][0], h[1] - gl_[0][1]) < 40])
            elif ps.get("push") and tg:                                          # v3 (23 Nov): the palm on the roof is one hand
                o = oc.held(k, draw_g, lambda o_: [tg[0]])
            else:                                                                # v3: clasped hands (two rig hands touching)
                def near_(o_):                                                   # are two QUIET hands, not a pile of fingers
                    hs = list(o_.get("hands") or [])
                    return hs if len(hs) == 2 and math.hypot(hs[0][0] - hs[1][0], hs[0][1] - hs[1][1]) < 34 * GS else []
                o = oc.held(k, draw_g, near_, alt=oc.quiet_hand)
        finally:
            _kit.HAND[0] = hk
            oc.ELBOW_LOW[0] = False; oc.TURN_DOWN[0] = 0.0
        heads[n] = (o["head"][0], o["head"][1], 55 * GS)
        if ps.get("lamp") and not (ps.get("lamp_front") and scene == 3):
            want = ps.get("lamp_xy") or tg[0]                                    # v4: the hand that reached for it
            hx, hy = min(o.get("hands") or [want], key=lambda h: (h[0] - want[0]) ** 2 + (h[1] - want[1]) ** 2)
            if HELD_AT[0]:
                hx, hy = c.device_to_user(*HELD_AT[0])                           # v11: the arm's real end, not the rig's report
            _lamp_in_hand(k, ps, hx, hy)
        if "lighter" in ps:                                                   # v9 (23 Nov, Office Noir 3's lighter_hand, lesson 399):
            want = tg[0]                                                         # on the hand the pose returns, narrower than the hand
            hx, hy = min(o.get("hands") or [want], key=lambda h: (h[0] - want[0]) ** 2 + (h[1] - want[1]) ** 2)
            if HELD_AT[0]:
                hx, hy = c.device_to_user(*HELD_AT[0])
            gs.protect(c, "the lighter", hx - 14, hy - LIGHTER_LIFT - 40, hx + 14, hy - 4)
            held_lighter(k, hx, hy, ps["lighter"], ps.get("lid", 1.0 if ps["lighter"] else 0.0), co_skin())
        if ps.get("point") and tg:                                            # the finger on 7
            want = tg[0]                                                      # v2 (24 Nov, Tomas at 0:08: "the finger is off the hand"): it
            hx, hy = min(o.get("hands") or [want], key=lambda h: (h[0] - want[0]) ** 2 + (h[1] - want[1]) ** 2)   # grows FROM the hand the rig
            dx_, dy_ = want[0] - hx, want[1] - hy - 6                          # drew, toward the square, never further than a finger
            dl_ = math.hypot(dx_, dy_) or 1.0
            L_ = min(dl_, 20.0)
            fx_, fy_ = hx + dx_ / dl_ * L_, hy + dy_ / dl_ * L_
            c.set_source_rgb(*INK); c.set_line_width(8); c.set_line_cap(1); c.move_to(hx, hy); c.line_to(fx_, fy_); c.stroke()
            c.set_source_rgb(*co_skin()); c.set_line_width(5); c.move_to(hx, hy); c.line_to(fx_, fy_); c.stroke()
        if ps.get("phone") in ("calendar", "pam"):
            hx, hy = tg[0]
            def cal(c_):
                import of_ui as ui                                            # v2 (24 Nov): the one phone UI
                ui.hand(c_, ui.pam_small if ps["phone"] == "pam" else ui.event)
            oc.phone_grip(k, hx, hy, 0.6, cal, ang=-0.1, skin=co_skin(), body_x=x)                 # v4 hands: held, on his palm
            gs.protect(c, "calendar phone", hx - 24, hy - 84, hx + 24, hy + 6)                  # v40: no bubble over it
        if ps.get("dent"):                                                    # v10: the roof gives under the palm, 2 drawings
            hx, hy = tg[0]
            c.set_source_rgb(*INK); c.set_line_width(2.4); c.new_path()
            c.move_to(hx - 34, hy + 4); c.curve_to(hx - 14, hy + 14, hx + 14, hy + 14, hx + 34, hy + 4); c.stroke()
        if ps.get("impact"):                                                  # stage 7: the SLAM, lines off the hand
            hx, hy = tg[0]
            c.set_source_rgb(*INK); c.set_line_width(3.2); c.set_line_cap(1)
            for a_ in (-2.6, -2.0, -1.4, -0.8, -0.3):
                r0, r1 = 26, 26 + 26 * ps["impact"]
                c.move_to(hx + r0 * math.cos(a_), hy + r0 * math.sin(a_)); c.line_to(hx + r1 * math.cos(a_), hy + r1 * math.sin(a_)); c.stroke()
        if ps.get("push"):                                                    # the flat hand pressing the roof
            hx, hy = tg[0]
            oc.ps_hand(k, "quiet", hx + 16, hy - 5, 24, (0.92, 0.74, 0.60), (-1.0, 0.12), 1)   # v2: the series' hand, flat on it
    elif n == "client":
        x, f = pos["client"]
        kind = ps.get("kind", "stand")
        look = ps.get("look", (-1, 0))
        if kind == "sit":
            und_ = ps.get("under", 0.0)                                      # v14 (grill 24 Nov): he rolls out from under the sill, side on
            sl_ = ps.get("slide", 0.0)
            if und_ or sl_:                                                  # the sill hides him only while he is still under it
                c.save()
                if und_ > 0.5:
                    c.rectangle(-2000, gs.SILL + 2, 4000, 2000); c.clip()
                c.translate(sl_, -und_)
            o = oc.client_sit(k, x, f, CS, look=look, face=ps.get("face", "bored"), wipe=ps.get("wipe", 0.0), hands_at=ps.get("hands_at"),
                              back=ps.get("back", 0.0), flick=ps.get("flick"), prop=ps.get("prop"), rag_to=ps.get("rag_to"),
                              roll=ps.get("roll", 0.0), head=ps.get("head", 0.0), fidget=ps.get("fidget", 0.0))
            if und_ or sl_:
                c.restore()
            bk_ = ps.get("back", 0.0)                                        # his head where the tipped trunk put it (the bubble's tail)
            if bk_ and isinstance(o, dict) and "head" in o:
                hx_, hy_ = o["head"][0] - x, o["head"][1] - (f - 30)
                o = dict(o, head=(x + hx_ * math.cos(bk_) - hy_ * math.sin(bk_) + ps.get("slide", 0.0),
                                  f - 30 + hx_ * math.sin(bk_) + hy_ * math.cos(bk_) - und_))
        elif kind == "bent":                                            # v8 (23 Nov, decided): IN FRONT of the car, at its nose, side on,
            bx, bf = BENT_AT                                                # bent over the wing into the bay (client_of.profile, the sheet's
            w = ps.get("work", 0.0)                                          # "bent into the engine"); his whole body seen, feet on the floor
            bolt = gs.bay_bolt()                                              # v9 (23 Nov, audit): the near hand on the wrench at the bolt,
            wa = -2.2 + 0.35 * w                                               # turning; the far hand braced on the wing's edge
            wrench_h = (bolt[0] + 26 * math.cos(wa) * -1, bolt[1] - 26 * math.sin(wa) * -1)
            wrench_h = (bolt[0] + 26 * math.cos(wa + math.pi), bolt[1] + 26 * math.sin(wa + math.pi))
            brace = (bolt[0] - 18, bolt[1] - 4)                                  # v10 (audit: "no second hand"): his far hand on the block, beyond the bolt, in sight
            hands = [wrench_h, brace]
            if ps.get("hand_back"):
                hands = [ps.get("hand_back_at", (bx + 60, 724)), brace]
            o = oc.client_bent(k, bx, bf, CS, hands=hands, lean=0.38, head34=0.7)   # v10: his own face, three-quarter
            if not ps.get("hand_back"):                                       # the wrench, from his fist to the bolt
                c.set_source_rgb(*INK); c.set_line_width(7); c.set_line_cap(1)
                c.move_to(*wrench_h); c.line_to(*bolt); c.stroke()
                c.set_source_rgb(0.72, 0.74, 0.77); c.set_line_width(4.4); c.move_to(*wrench_h); c.line_to(*bolt); c.stroke()
                c.set_source_rgb(*INK); c.new_path(); c.arc(bolt[0], bolt[1], 5, 0, 2 * math.pi); c.set_line_width(1.6); c.stroke()                # v8: his head over the bay, his hands below it
            if ps.get("hand_back") and ps.get("client_lamp", True):
                hx_, hy_ = ps.get("hand_back_at", (bx + 60, 724))
                gs.lamp(k, hx_ - 6, hy_ + 2, ang=-1.3, lit=ps.get("lamp_lit", True), hang=884, swing=ps.get("cable_swing", 0.0))
        elif kind == "watch":
            wu = ps.get("watch_u", 1.0)                                       # stage 7: the wrist comes up to the eyes
            wx, wy = oc.watch_pose(x, f, CS)[0]
            o = oc.client(k, x, f, CS, look=look, targets=[(x + 40 + (wx - x - 40) * wu, f - 110 + (wy - f + 110) * wu)],
                          face=ps.get("face", "bored"))
        elif kind == "thumb":                                                   # v1 (23 Nov audit, decided): "Without him." with
            tu = ps.get("thumb_u", 1.0)                                        # a thumb jerked over his shoulder, at the door
            T0, T1 = (x + 30, f - 112), (x + 60, f - 178)   # v2: the RIGHT hand, away from Father
            tx, ty = om_lerp(T0, T1, tu)
            wx, wy = oc.watch_pose(x, f, CS)[0]
            o = oc.held(k, lambda: oc.client(k, x, f, CS, look=look, targets=[(tx, ty)], face=ps.get("face", "bored")),
                        lambda o_: [(tx, ty)])                                  # v3 (hand audit): one hand at this wrist
            import client_ob as co_
            H, D = oc.guard_arm_front(k, x, f, CS, True, (tx, ty), co_skin(), hand=False, from_elbow=False,
                                      upper=co_.SHIRT, lower=co_skin(), cuff=False, w=19.0, short=0.55)
            oc.thumb_fist(k, H[0], H[1], 15.0, co_skin(), D, math.radians(-15 + 25 * tu))   # everyone's hand, thumb out
        elif kind == "pocket":
            pu = ps.get("pocket_u", 0.0)                                     # v5 (23 Nov, Tomas: "the hand is strange"): out of the
            P0, P1, P2 = (x - 8, f - 140), (x - 22, f - 106), (x - 66, f - 158)  # top pocket, a wipe on the thigh, held out to
            if pu < 0.4:                                                         # Father as in 2.8b, in ONE arm (2.8b's)
                tx, ty = om_lerp(P0, P1, pu / 0.4)
            elif pu < 0.6:
                tx, ty = P1[0] + 6 * math.sin((pu - 0.4) / 0.2 * 2 * math.pi), P1[1]
            else:
                tx, ty = om_lerp(P1, P2, (pu - 0.6) / 0.4)
            o = oc.held(k, lambda: oc.client(k, x, f, CS, look=look, targets=[(tx, ty)]), lambda o_: [(tx, ty)])
            import client_ob as co_
            H, _ = oc.guard_arm_front(k, x, f, CS, False, (tx, ty), co_skin(), hand=False, from_elbow=False,
                                      upper=co_.SHIRT, lower=co_skin(), cuff=False, w=19.0, short=0.55)
            oc.phone_grip(k, H[0], H[1], 0.6, None, ang=(0.9 if pu < 0.6 else 0.9 - 1.0 * (pu - 0.6) / 0.4), skin=co_skin(),
                          body_x=x)                                               # v2 (23 Nov, Tomas, 0:38): his right hand — the
        elif kind == "phone_out":                                               # thumb was on the far edge, crossed over his own fingers
            tx, ty = x - 66, f - 158                                             # v5 (23 Nov): the whole phone inside the frame
            o = oc.held(k, lambda: oc.client(k, x, f, CS, look=look, targets=[(tx, ty)]), lambda o_: [(tx, ty)])
            import client_ob as co_                                              # v6: his arm again in ONE piece (the rig's broke under the phone)
            H, _ = oc.guard_arm_front(k, x, f, CS, False, (tx, ty), co_skin(), hand=False, from_elbow=False,
                                      upper=co_.SHIRT, lower=co_skin(), cuff=False, w=19.0, short=0.55)
            oc.phone_grip(k, H[0], H[1], 0.6, None, ang=-0.1, skin=co_skin(), body_x=x)   # v2: same fix, same arm
        elif kind == "slam":
            sb_ = ps.get("slam_b", 0.0)                                      # v2 (24 Nov, cold test v37, 3 of 3: "it shuts by itself, he waves"):
            aa_ = -1.45 * sb_                                                # ONE hand, flat ON the lid's free edge all the way down
            o = oc.client(k, x, f, CS, look=(-1, 0.6), targets=[(462 + 66 * math.cos(aa_) + 4 - 34 * (1 - sb_) ** 3, 676 + 66 * math.sin(aa_) + 6 + 16 * (1 - sb_) ** 3)])
        else:
            o = oc.client(k, x, f, CS, look=look)
        heads[n] = (o["head"][0], o["head"][1], 55 * CS)


HELD_AT = [None]                                           # v11: the device point where the holding arm really ends
LIGHTER_S = 0.34                                           # v9 (23 Nov): a lighter is narrower than the hand that holds it
LIGHTER_LIFT = 74 * LIGHTER_S - 5                           # the flame's foot above the hand point: the case stands on the fist


LATE_POOL = []
CABLE_DONE = [False]
LAMP_ANG = -0.2                                            # v12: held, the cage a little down: its light falls where it points


def _late_pools(c):
    """v12 (24 Nov): the lamp's warm pool on whatever is in front of the man who holds it (the bonnet)."""
    for (px_, py_), (rx_, ry_), cs in LATE_POOL:
        c.save(); c.identity_matrix(); c.translate(px_, py_); c.scale(abs(rx_), abs(ry_))
        g_ = cairo.RadialGradient(0, 0, 0.1, 0, 0, 1)
        g_.add_color_stop_rgba(0, 1.0, 0.96, 0.66, 0.75 * cs); g_.add_color_stop_rgba(1, 1.0, 0.93, 0.55, 0.0)
        c.set_source(g_); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    del LATE_POOL[:]


def _lamp_in_hand(k, ps, hx, hy, arm=None):
    """the work lamp in a guard's hand at (hx, hy) (v10: one function, so it can be drawn after the Client)."""
    c = k.c
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
        la_ = ps.get("lamp_ang", LAMP_ANG)                                         # v11 (23 Nov, audit): the HANDLE in his hand, the cage
        cx_, cy_ = hx - 26 * math.cos(la_), hy - 26 * math.sin(la_)              # out in front of it
        # v12 (24 Nov, audit: "the beam is not tied to the lamp's angle"): the light leaves the cage's OPEN side, turned
        # a little down from its axis, and lands where that ray meets the surface (pool_y); no surface, no pool
        dx_, dy_ = -math.cos(la_ - 0.5), -math.sin(la_ - 0.5)
        bx_, by_ = cx_ - 14 * math.cos(la_), cy_ - 14 * math.sin(la_) + 3        # the bulb
        py0 = ps.get("pool_y", 712)
        ln_ = (py0 - by_) / dy_ if dy_ > 0.15 else 150
        hit = dy_ > 0.15 and ln_ < 260
        ln_ = min(ln_, 260)
        ex_, ey_ = bx_ + dx_ * ln_, by_ + dy_ * ln_
        nx_, ny_ = -dy_, dx_
        g_ = cairo.LinearGradient(bx_, by_, ex_, ey_)
        g_.add_color_stop_rgba(0, 1.0, 0.93, 0.55, 0.80 * cs); g_.add_color_stop_rgba(1, 1.0, 0.93, 0.55, (0.38 if hit else 0.0) * cs)
        w1 = 0.30 * ln_
        c.set_source(g_); c.move_to(bx_ + 8 * nx_, by_ + 8 * ny_); c.line_to(bx_ - 8 * nx_, by_ - 8 * ny_)
        c.line_to(ex_ - w1 * nx_, ey_ - w1 * ny_); c.line_to(ex_ + w1 * nx_, ey_ + w1 * ny_); c.close_path(); c.fill()
        if hit and not ps.get("pool_late"):                                      # in the open bay: where it lands, behind the car's side
            c.set_source_rgba(1.0, 0.95, 0.65, 0.55 * cs)
            c.save(); c.translate(ex_, ey_); c.scale(34, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        elif hit:                                                                # on a shut bonnet: drawn AFTER the
            LATE_POOL.append((c.user_to_device(ex_, ey_), c.user_to_device_distance(max(26, w1 / max(dy_, 0.3)), 9), cs))   # car (he stands behind it)
        if arm:
            arm()
        gs.lamp(k, cx_, cy_, ang=la_, lit=cs > 0.5, hang=ps.get("cable_floor", F + 8), glow=False,   # the cone is its light; no halo over his arm
                cable=not CABLE_DONE[0], swing=ps.get("cable_swing", 0.0))
        _oc.handle_grip(k, hx, hy, 20, la_ + math.pi / 2, co_skin())
        if cs > 0.5:                                                             # the light on the fingers that face the bulb
            c.set_source_rgba(1.0, 0.92, 0.55, 0.42)
            c.save(); c.translate(hx - 9 * math.cos(la_), hy - 9 * math.sin(la_)); c.rotate(la_); c.scale(4, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    else:
        la_ = ps.get("lamp_ang", -1.3)
        gs.lamp(k, hx - 8, hy + 22, ang=la_, lit=ps.get("lamp_lit", False) or "lamp_ang" in ps)
        _oc.handle_grip(k, hx - 8 + 26 * math.cos(la_), hy + 22 + 26 * math.sin(la_), 24, la_ + math.pi / 2, co_skin())   # v3: held
    gs.protect(c, "the lamp in his hand", hx - 40, hy - 10, hx + 30, hy + 50)
    if ps.get("napkin"):                                                     # v1 (23 Nov, the mid-film gag): a white napkin
        cut(Ctx(c, 0) if False else k, [(hx + 4, hy + 6), (hx + 30, hy + 2), (hx + 34, hy + 46), (hx + 22, hy + 52), (hx + 8, hy + 44)],
            (0.98, 0.98, 0.96), lw=2)                                         # over his forearm: he serves the lamp like a waiter
        c.set_source_rgb(0.80, 0.80, 0.80); c.set_line_width(1.4); c.move_to(hx + 18, hy + 6); c.line_to(hx + 20, hy + 48); c.stroke()


def held_lighter(k, hx, hy, flame, lid, skin):
    """Office Noir 3's lighter_hand, for a hand at (hx, hy): the case stands IN the fist (the fist round its lower half,
    drawn over it), the thumb up its side to the wheel."""
    c = k.c
    _oc.log_grip(c, "lighter", hx, hy)
    fx, fy = hx, hy - LIGHTER_LIFT
    gs.lighter(k, fx, fy, LIGHTER_S, flame, hand=False, lid=lid)
    c.save(); c.translate(hx, hy - 4); c.scale(12.5, 9.5); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()   # the fist
    c.set_source_rgb(*skin); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.0); c.stroke()
    c.set_line_width(1.3); c.set_line_cap(1)
    for dy in (-6, -2, 2):                                                    # the curled fingers' seams
        c.move_to(hx - 3, hy - 4 + dy); c.line_to(hx + 9, hy - 4 + dy); c.stroke()
    _oc._capsule(c, hx - 9, hy - 8, fx - 7, fy + 4, 3.4, skin)                 # the thumb, up the near side
    return fx, fy


def om_lerp(a, b, u):
    u = max(0.0, min(1.0, u))
    return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u


def garage_shot(k, sh, scene, heads, cam):
    st = sh["state"]
    behind_names = [n for n in sh["cast"] if (n == "g2" and scene == 2) or (n == "g1" and scene == 3)
                    ]                                                              # v8: the bent Client is in front now
    behind_names.sort(key=lambda n: n != "g1")                         # the lamp man furthest back
    behind_names = [n for n in behind_names if n not in st.get("front_of_car", ())]   # v11 (23 Nov, lesson 292): he steps round the car
    behind_names += [n for n in st.get("behind_car", ()) if n in sh["cast"] and n not in behind_names]   # v12: at the wall
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
        gp = POSES.get(sh["id"], {}).get("g1", {})
        if scene == 3 and "g1" in behind_names and gp.get("lamp") and gp.get("lamp_front"):   # v10 (23 Nov, lessons 129/245):
            gx_, gf_ = dict(BLOCK[3], **st.get("moved", {}))["g1"]              # his lamp arm AFTER the Client, so the hand shows
            gx_ -= gp.get("back", 0)
            want = gp.get("lamp_xy") or gp["targets_xy"][0]
            H, _ = _oc.guard_arm_front(k, gx_, gf_, GS, True, want, co_skin(), draw=False)   # lesson 168: the arm stays BEHIND him,
            _lamp_in_hand(k, gp, H[0], H[1])                                     # only the hand and the lamp in front

    def front(k):
        for n in front_names:
            _cast_draw(k, n, scene, sh, heads)
    gs.LID_BEHIND[0] = False                                              # v8: nobody works behind the lid now
    gs.LEGS_ROT[0], gs.LEGS_TORSO[0] = st.get("legs_rot", 0.0), st.get("legs_torso", 0.0)   # v13: the roll-out's in-betweens
    gs.LEGS_WORK[0] = st.get("legs_work", 0.0)                            # v8: the knee taps while he works
    gs.FIRE[0], gs.FIRE[1] = st.get("fire", 0.0), st.get("fire_t", 0.0)       # v9: the fire, the sheet
    gs.SHEET[0], gs.SHEET[1] = st.get("sheet_fly"), st.get("sheet_floor")
    gs.NEW_PLAN[0] = st.get("new_plan")                                     # v1 (23 Nov, decided): the fresh plan going up
    gs.BLACK_CAR[0] = bool(st.get("black_car"))                              # v1 (23 Nov, decided): Father has arrived
    gs.garage(k, burn=st.get("burn", 0.0), legs_out=legs_out, bonnet=bon,
              lamp_on_floor=scene in (1, 2, 5) and (not st.get("lamp_up") or st.get("lamp_floor")), behind=behind, front=front, tilt=st.get("tilt", 0.0))
    gs.LID_BEHIND[0] = False
    c = k.c
    _late_pools(c)
    if st.get("dim"):                                                     # v12 (24 Nov): the lamp has died: the frame a shade darker
        c.save(); c.identity_matrix(); c.set_source_rgba(0.04, 0.05, 0.09, st["dim"]); c.paint(); c.restore()
    if st.get("lamp_fly") is not None:                                    # v1 (23 Nov): the lamp in the air, onto its floor spot
        w_ = st["lamp_fly"]
        x0_, y0_ = BLOCK[1]["g1"][0] + 50, BLOCK[1]["g1"][1] - 60
        x1_, y1_ = gs.LAMP_AT
        gs.lamp(k, x0_ + (x1_ - x0_) * w_, y0_ + (y1_ - y0_) * w_ - 70 * 4 * w_ * (1 - w_), ang=-0.5 + 2.5 * (1 - w_), lit=True)
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
        for i in range(5):                                                # v10 (23 Nov audit: "a dial"): BIG cartoon puffs from
            a_ = p_ - i * 0.14                                            # the tail pipe, outlined, rising: it RUNS
            if a_ <= 0:
                continue
            ex, ey = x0_ + 30 + 18 * a_ + (8 if i % 2 else -8), gs.SILL + 6 - 120 * a_
            al_ = max(0.0, 0.95 - 0.8 * a_)
            for (ox, oy, rr) in ((0, 0, 1.0), (-0.7, 0.3, 0.7), (0.7, 0.25, 0.75)):
                R_ = 18 + 30 * a_
                c.new_path(); c.arc(ex + ox * R_, ey + oy * R_, rr * R_, 0, 2 * math.pi)
                c.set_source_rgba(0.55, 0.55, 0.58, al_); c.fill_preserve()
                c.set_source_rgba(0.12, 0.12, 0.14, al_); c.set_line_width(2.2); c.stroke()
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
        c.save(); c.set_source_rgba(0.10, 0.10, 0.12, 0.32); c.paint(); c.restore()   # v11 (audit): the car steps back,
        c.save(); c.translate(px, py); c.scale(1.15, 1.15); c.translate(-px, -py)      # the phone 15 % bigger
        for col, lw in ((INK, 66), (dc.SUIT, 60)):                            # v9 (24 Nov, cold test 3 of 3: "a black diagonal",
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(0)       # "floating"; decided: hand + SHORT THICK forearm):
            c.move_to(px + 40, py + 26); c.line_to(px + 150, py - 230); c.stroke()   # his sleeve, as wide as the hand, straight
        c.save(); c.translate(px + 51, py + 0.4); c.rotate(math.atan2(-256, 110))    # v10 (24 Nov, cold test v31: still "a pole"; decided hand + cuff only): a short stub
        rect(k, -9, -35, 18, 70, (0.97, 0.97, 0.94), 3409, shadow=False, lw=1.8)            # his white cuff, at the phone
        c.restore()
        S04, A04 = 90 / 44.0, 0.0                                             # v7: the same phone grip as every phone, big
        gx_, gy_ = px - 22 * S04 * math.sin(A04) * 0 - 45 * math.sin(A04), py + 45 * math.cos(A04)
        _oc.phone_grip(k, gx_, gy_, S04, ang=A04, skin=(0.92, 0.74, 0.60), body_x=gx_ + 400, part="back", ink=0.6)
        c.save(); c.translate(px, py); c.rotate(0.0); c.scale(1.5, 1.5)    # v8 (cold test 3 of 3): UPRIGHT
        gs.protect(c, "the DELETE POST phone", -30, -48, 30, 48)
        rect(k, -30, -48, 60, 96, (0.10, 0.11, 0.14), 3410, lw=2)
        import of_ui as ui                                                     # v12 (24 Nov, Tomas: "like PowerPoint"): the one phone UI
        ui.full(c, -25, -42, 50, 84, ui.review)
        c.restore()
        _oc.phone_grip(k, gx_, gy_, S04, ang=A04, skin=(0.92, 0.74, 0.60), body_x=gx_ + 400, part="front", ink=0.6, thumb_tip=(23.5, 1))   # thumb (v12: short, off the screen), fingertips
        c.restore()


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


UPRIGHT = [False]                                         # v14 (23 Nov, Tomas + 2 cold viewers: lying ACROSS tells the
# story, 'he answers from under the car'; upright read as a man behind a counter)                                           # v12: the overhead turned so he lies head-up
KSCALE = [1.0]                                             # the overhead is drawn in frame units


def under_shot(k, sh, heads):
    """UNDER THE CAR: his face up, lit from the lamp's side; the sump a hand above it. In frame units."""
    import of_cast as oc
    c = k.c
    c.set_source_rgb(0.16, 0.17, 0.19); c.paint()                                  # the car's underside
    sway = sh["state"].get("sway_v", 16 if sh["state"].get("sway") else 0)
    g = cairo.RadialGradient(470, 900, 20, 470, 900, 520)
    g.add_color_stop_rgba(0, 1.0, 0.92, 0.6, 0.55); g.add_color_stop_rgba(1, 1.0, 0.92, 0.6, 0.0)
    c.set_source(g); c.paint()
    if sh["state"].get("view") == "top" or sh["id"] == "0.9":                   # v10: the overhead (v11: 0.9 too, closer:
        zt = 1.0 if sh["state"].get("view") == "top" else 1.30                    # the side profile looked wrong; v12, 23 Nov
        zx = 300 if zt == 1.0 else 230                                            # audit: 1.55 -> 1.30, so the car's sill and a tyre
        if not UPRIGHT[0]:                                                        # v13 (23 Nov, Tomas: horizontal): lying ACROSS the
            zt, zx = (1.22, 262) if sh["state"].get("view") == "top" else (1.40, 250)   # frame, tight: face to sill, tyres at the edge
        R_ = UPRIGHT[0]                                                           # v12 (23 Nov, cold tests 3 of 3: "sideways"):
        c.save()                                                                  # turned a quarter: his head UP the frame
        if R_:
            c.translate(270 + (0 if zt == 1.0 else 80), 480); c.rotate(math.pi / 2); c.scale(1.15, 1.15); c.translate(-270, -480)
        c.translate(300, 500); c.scale(zt, zt); c.translate(-zx, -500)
        hx_, hy_, hr_ = oc.client_top(k, sway=sway, wrench_t=sh["state"].get("wrench_t", 0.0))
        dev = c.user_to_device(hx_, hy_); rr = math.hypot(*c.user_to_device_distance(hr_, 0))
        c.restore()
        heads["client"] = (dev[0] / KSCALE[0], dev[1] / KSCALE[0], rr / KSCALE[0]) if R_ else ((hx_ - zx) * zt + 300, (hy_ - 500) * zt + 500, hr_ * zt)
    else:
        heads["client"] = oc.client_under(k, 1.6, sway=sway, wrench_t=sh["state"].get("wrench_t", 0.0))   # v9: the side cutaway


def insert_shot(k, sh):
    c = k.c
    kind = sh["state"].get("insert")
    if kind == "card":                                                            # v2 (23 Nov audit: viewers read "an ad, a
        import cs_props as cp_                                                      # billboard"): HIS phone, in HIS hand, the
        c.set_source_rgb(*gs.WALL); c.paint()                                       # garage behind: the wall, the dado, the car
        c.set_source_rgb(*gs.WALL_D); c.rectangle(0, 600, 540, 360); c.fill()
        c.set_source_rgba(0.17, 0.36, 0.62, 0.55); c.new_path(); c.arc(40, 700, 230, 0, 2 * math.pi); c.fill()
        c.save(); c.translate(270, 430); c.rotate(-0.05); c.scale(0.76, 0.76); c.translate(-270, -440)
        sk_ = co_skin()                                                            # v3 (23 Nov, hand audit, decided): HIS phone grip,
        S_, PX_, PY_ = 464 / 44.0, 270, 480 + 22 * 464 / 44.0 + 110                   # the same oc.phone_grip as every phone in the film,
        for col, lw in ((INK, 150), (sk_, 142)):                                   # drawn big: his forearm up from the bottom right,
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1); c.move_to(PX_, PY_); c.line_to(640, 1260); c.stroke()
        c.save(); c.translate(560, 1180); c.rotate(0.75)
        rect(k, -90, -40, 180, 120, (0.97, 0.97, 0.95), 3485, lw=3)                 # his white T-shirt sleeve,
        c.restore()
        _oc.phone_grip(k, PX_, PY_, S_, skin=sk_, body_x=PX_ + 900, part="back", ink=0.34)   # the palm behind (he is off to the right)
        old_bg = cp_._bg; cp_._bg = lambda *a, **kw: None
        try:
            gs.insert_card(k)                                                      # the card, PAM finds things
        finally:
            cp_._bg = old_bg
        _oc.phone_grip(k, PX_, PY_, S_, skin=sk_, body_x=PX_ + 900, part="front", ink=0.34)  # the thumb and the fingertips
        c.restore()
    elif kind == "invite":
        gs.insert_invite(k)
    elif kind == "uptimez":                                                        # v9: the building, so we know where we are
        import brand
        st = sh["state"]
        c.set_source_rgb(0.62, 0.78, 0.92); c.paint()                                  # the sky
        rect(k, -20, 120, 580, 900, (0.86, 0.87, 0.90), 3700, lw=3)                     # the building's front
        for wy in (150,):                                                              # its upper windows
            for wx in (30, 150, 270, 390):
                rect(k, wx, wy, 100, 60, (0.55, 0.70, 0.86), 3701 + wx + wy, shadow=False, lw=2)
        rect(k, 20, 240, 500, 120, (1.0, 1.0, 1.0), 3710, lw=3)                        # the sign over the doors (clear of the buttons)
        c.save(); c.translate(44, 258); w_ = brand.lockup(c, 0, 0, 84); c.restore()
        gs.protect(c, "the UptimeZ sign", 20, 240, 520, 360)
        g = cairo.LinearGradient(0, 460, 0, 900)                                       # the lobby behind the glass, lit
        g.add_color_stop_rgb(0, 1.0, 0.93, 0.72); g.add_color_stop_rgb(1, 0.98, 0.84, 0.58)
        c.set_source(g); c.rectangle(40, 460, 460, 440); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(4); c.rectangle(40, 460, 460, 440); c.stroke()
        c.move_to(270, 460); c.line_to(270, 900); c.stroke()                           # two glass doors
        for dx in (240, 300):
            c.set_line_width(7); c.move_to(dx, 640); c.line_to(dx, 720); c.stroke()     # their handles
        c.set_source_rgba(1, 1, 1, 0.45); c.set_line_width(14)                          # glass glare
        for gx in (90, 330):
            c.move_to(gx, 860); c.line_to(gx + 90, 500); c.stroke()
        c.save(); c.translate(225, 520); brand.mark(c, 0, 0, 90); c.restore()            # the mark on the glass
        gs.protect(c, "the mark on the glass", 225, 520, 315, 610)
        rect(k, 0, 900, 540, 60, (0.48, 0.49, 0.52), 3720, shadow=False, lw=2)           # the pavement
    elif kind == "slap":                                                           # v53 (25 Nov, cold test v52, 3 of 3: the fresh plan read
        import dh_cast as dc_                                                      # as "a glitch"; decided): no plan. Outside, at his black
        u_ = sh["state"].get("slap_u", 0.0)                                         # car: Father brings the phone down, face down, on its ROOF.
        c.set_source_rgb(0.99, 0.96, 0.86); c.paint()                               # The film ends a hand above it; frame 0's fist lands it.
        c.set_source_rgb(0.88, 0.86, 0.78); c.rectangle(0, 470, 540, 200); c.fill()  # the bright street, the far kerb
        ROOF = 636
        c.new_path(); c.move_to(-20, 960); c.line_to(-20, ROOF + 30); c.curve_to(120, ROOF - 6, 420, ROOF - 6, 560, ROOF + 30)
        c.line_to(560, 960); c.close_path(); c.set_source_rgb(0.07, 0.07, 0.08); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.16); c.set_line_width(7); c.set_line_cap(1)      # the gloss along the roof
        c.new_path(); c.move_to(60, ROOF + 36); c.curve_to(180, ROOF + 16, 360, ROOF + 16, 480, ROOF + 36); c.stroke()
        c.set_source_rgb(0.30, 0.34, 0.40); c.new_path(); c.move_to(70, 960); c.line_to(96, 790); c.line_to(444, 790); c.line_to(470, 960)
        c.close_path(); c.fill()                                                     # the glass below it
        hy_ = 300 + (ROOF - 62 - 300) * u_ * u_                                      # it comes down faster and faster
        hx_ = 262 - 14 * (1 - u_)
        if u_ > 0.45:                                                                # the air above it
            c.set_source_rgba(0.08, 0.08, 0.10, 0.55); c.set_line_width(4)
            for j, dx_ in enumerate((-84, -34, 30, 86)):
                c.new_path(); c.move_to(hx_ + dx_, hy_ - 150 - 26 * (j % 2)); c.line_to(hx_ + dx_, hy_ - 150 - 26 * (j % 2) - 90 * u_); c.stroke()
        c.save(); c.translate(hx_, hy_ + 34); c.rotate(-0.06)                         # the phone, its dark back up, flat under his palm
        c.new_path(); c.move_to(-96, -24); c.line_to(112, -24); c.line_to(98, 20); c.line_to(-112, 20); c.close_path()   # seen a little from above: a slab
        c.set_source_rgb(0.13, 0.13, 0.15); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_join(1); c.stroke()
        c.new_path(); c.move_to(-112, 20); c.line_to(98, 20); c.line_to(98, 30); c.line_to(-112, 30); c.close_path()
        c.set_source_rgb(0.05, 0.05, 0.06); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        c.set_source_rgb(0.34, 0.35, 0.38); c.new_path(); c.arc(-78, -8, 8, 0, 2 * math.pi); c.fill()   # its camera: the BACK is up
        c.restore()
        sh_ = (590, hy_ - 250)                                                       # HE is in it: the velvet shoulder at the edge, the elbow up
        hd_ = (hx_ + 6, hy_ + 8)
        pd_ = insert_arm(c, hd_, bend(hd_, sh_, 80, -1), sh_, 60, dc_.SKIN_F, dc_.VELVET, cuff=(0.97, 0.97, 0.95), torso=dc_.VELVET)
        _oc.ps_hand(k, "grab", hd_[0] - 10 * pd_[0], hd_[1] - 10 * pd_[1], 76, dc_.SKIN_F, pd_, 1)   # the series' hand, over the phone
    elif kind == "pin":                                                            # v2 (23 Nov, cold tests 3 of 3: the plan "healed"):
        u_ = sh["state"].get("pin_u", 1.0)                                             # v5 (24 Nov, cold test 3 of 3: "the burnt map is
        sl_ = sh["state"].get("pin_slide", 1.0)                                        # whole again", "a pole from the floor"; decided):
        Z_, CX_, CY_, DY_ = 2.8, 408, 520, 22                                                   # the BURNT plan is there, with its hole; the FRESH
        c.save(); c.translate(270, 480 + DY_); c.scale(Z_, Z_); c.translate(-CX_, -CY_)      # one slides up over it under his hand, and his
        gs.room(k)
        c.save(); c.identity_matrix(); c.set_source_rgba(0.10, 0.10, 0.12, 0.34); c.paint(); c.restore()   # v9 (audit): the wall steps back
        c.push_group(); gs.plan(k, 1.0); c.pop_group_to_source(); c.paint_with_alpha(1.0 - 0.999 * ease_((sl_ - 0.55) / 0.45))   # and the burnt one is GONE under the fresh one
        pass                                                    # finger pins its bottom corner. It is covered,
        c.save(); c.translate(0, 340 * (1 - sl_))
        gs.CLEAN[0] = gs.DON_TAG[0] = True                                             # v8 (audit): no seam tape on the fresh one, DON on a tag
        gs.plan(k, 0.0)
        gs.CLEAN[0] = gs.DON_TAG[0] = False
        c.restore(); c.restore()
        px_, py_ = (336 - CX_) * Z_ + 270, (579 - CY_) * Z_ + 480 + DY_ + 340 * (1 - sl_) * Z_   # the fresh plan's bottom left corner
        ph_ = (px_ + 34 + 10 * (1 - u_), py_ + 78 + 18 * (1 - u_))
        sh_ = (ph_[0] + 60, 1400)                                                     # v6 (24 Nov, cold test v30: "a pole" 3 of 3): HE is in the
        pd_ = insert_cuff(c, ph_, bend(ph_, sh_, 70, -1), 70, (0.92, 0.74, 0.60), (0.11, 0.11, 0.13),   # v7: HAND + CUFF only
                          cuff=(0.97, 0.97, 0.95), stub=230)
        _oc.ps_hand(k, "point", ph_[0], ph_[1], 84, (0.92, 0.74, 0.60), pd_, 1)        # his INDEX finger on the pin (hands_ps "point")
        if u_ > 0.5:
            ellipse(k, px_, py_, 14, 14, (0.85, 0.12, 0.12), 3497, lw=2.4)              # the red pin, in
        gs.protect(c, "the fresh plan", 60, 290, 470, 660)
    elif kind == "bay":                                                            # v1 (23 Nov, decided A): his hands in the lamp's light
        c.save(); c.translate(270, 400); c.scale(1.04, 1.04); c.translate(-262, -330)   # v7 (24 Nov, decided): TIGHT on the hands
        c.set_source_rgb(0.10, 0.10, 0.11); c.paint()                                  # the bay, dark; all of it inside the safe area
        bu = sh["state"].get("bay_u", 1.0)
        g_ = cairo.RadialGradient(240, 340, 10, 240, 340, 230)                         # the lamp's pool, on the engine and his hands
        g_.add_color_stop_rgba(0, 1.0, 0.95, 0.70, 0.55 * bu); g_.add_color_stop_rgba(1, 1.0, 0.95, 0.70, 0.0)
        c.set_source(g_); c.arc(240, 340, 230, 0, 2 * math.pi); c.fill()
        rect(k, 40, 270, 400, 230, (0.50, 0.51, 0.54), 3460, lw=3)                     # v2 (23 Nov, decided): the SAME engine as the
        for i in range(3):                                                             # wide shot: the block, its red plug leads,
            c.set_source_rgb(*INK); c.set_line_width(13); c.set_line_cap(1)            # the round air filter, a black hose, the
            c.move_to(110 + i * 70, 270); c.line_to(90 + i * 70, 200); c.stroke()     # yellow oil cap, the bolt
            c.set_source_rgb(0.85, 0.15, 0.12); c.set_line_width(9); c.move_to(110 + i * 70, 270); c.line_to(90 + i * 70, 200); c.stroke()
        ellipse(k, 200, 225, 130, 46, (0.18, 0.18, 0.20), 3461, lw=2.6)                # the air filter
        ellipse(k, 200, 225, 40, 14, (0.30, 0.30, 0.32), 3462, shadow=False, lw=1.8)
        c.set_source_rgb(*INK); c.set_line_width(36); c.set_line_cap(1)
        c.move_to(330, 250); c.curve_to(390, 190, 440, 230, 470, 300); c.stroke()
        c.set_source_rgb(0.15, 0.15, 0.16); c.set_line_width(30); c.move_to(330, 250); c.curve_to(390, 190, 440, 230, 470, 300); c.stroke()
        ellipse(k, 380, 440, 34, 26, (0.98, 0.80, 0.12), 3463, lw=2.4)                 # the yellow oil cap
        c.set_source_rgb(0.20, 0.20, 0.22); c.set_line_width(22); c.set_line_cap(1)    # a pipe below
        c.move_to(20, 560); c.curve_to(160, 540, 280, 600, 440, 560); c.stroke()
        g2_ = cairo.RadialGradient(250, 350, 10, 250, 350, 200)                        # the light ON the work, soft, over the parts
        g2_.add_color_stop_rgba(0, 1.0, 0.95, 0.70, 0.35); g2_.add_color_stop_rgba(1, 1.0, 0.95, 0.70, 0.0)
        c.set_source(g2_); c.arc(250, 350, 200, 0, 2 * math.pi); c.fill()
        bo_ = sh["state"].get("bolt_out", 0.0)                                         # v3 (decided): the bolt comes FREE
        c.set_source_rgb(0.08, 0.08, 0.09); c.arc(250, 350, 15, 0, 2 * math.pi); c.fill()   # its hole (the plug sits in it: below)

        w_ = sh["state"].get("work", 0.0)
        ro_ = sh["state"].get("bay_reach", sh["state"].get("bolt_out", 0.0))
        wa_ = -2.2 + 0.2 * w_                                                          # v12: a 150 handle, worked about the bolt; then the
        hw_ = (250 + 170 * math.cos(wa_), 350 + 170 * math.sin(wa_))                   # HAND stays and the wrist swings the head off the hole
        c.save(); c.translate(*hw_); c.rotate(wa_ + math.pi + 0.6 * ro_)               # (the arm keeps its length: audit)
        rect(k, -40, -14, 224, 28, (0.70, 0.72, 0.75), 3471, lw=2.4)                   # the handle comes out past his fist
        c.restore()
        bo2_ = sh["state"].get("bolt_out", 0.0)
        fh_ = (330 - 80 * ro_, 270 + 43 * ro_ - 102 * bo2_)   # v10 (24 Nov, Tomas: "the hand JUMPED, whose is it?"): it goes to the hole FIRST, grips, then lifts; the plug is in the fist all the way                          # v4: the far hand comes up with the plug
        for side, (hx, hy, sx_, sy_) in enumerate(((hw_[0], hw_[1], 30, 70), (fh_[0], fh_[1], 500, 720))):
            sx_, sy_ = (112, 590) if side == 0 else (405, 590)                           # v11 (24 Nov, Tomas: "a hand walks in space, a wrist with
            el_ = ik2((hx, hy), (sx_, sy_), 207, 207, -1 if side == 0 else 1)             # v12 (audit: +33 % stretch): fixed bone lengths                  # no arm"): HE is in the frame, from behind: his back and
            dd_ = insert_arm(c, (hx, hy), el_, (sx_, sy_), 54, (0.80, 0.62, 0.50), None, lit=(330, 96), half=(0.97, 0.97, 0.95))
            if side == 0:
                WD_ = dd_                                                             # the watch sits ON this wrist
            if side == 1:                                                             # v13 (three audits: "a scrap of paper"): the plug stands in
                c.save(); c.rectangle(0, 0, 600, 357); c.clip()                           # its hole, thread DOWN; he takes it by the insulator's top and
                c.translate(250, 385 - 102 * bo2_); c.rotate(-0.10 * bo2_); c.scale(1.6, 1.6)   # draws it up: the hex, the thread and the sooty
                rect(k, -5, -84, 10, 16, (0.70, 0.72, 0.75), 3483, shadow=False, lw=2)     # electrode come out of the hole after it
                c.new_path(); c.move_to(-9, -68); c.line_to(9, -68); c.line_to(13, -22); c.line_to(-13, -22); c.close_path()
                c.set_source_rgb(0.95, 0.94, 0.90); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.4); c.stroke()
                c.set_line_width(1.6)
                for ry_ in (-58, -48, -38):
                    c.move_to(-10, ry_); c.line_to(10, ry_); c.stroke()
                rect(k, -19, -22, 38, 20, (0.70, 0.72, 0.75), 3481, lw=2.2)
                for vx_ in (-7, 7):
                    c.move_to(vx_, -21); c.line_to(vx_, -3); c.stroke()
                rect(k, -10, -2, 20, 30, (0.55, 0.56, 0.58), 3482, lw=2)
                c.set_source_rgb(*INK); c.set_line_width(1.6)
                for ty_ in (4, 11, 18):
                    c.move_to(-10, ty_ + 3); c.line_to(10, ty_ - 2); c.stroke()
                c.set_source_rgb(0.08, 0.07, 0.06); c.rectangle(-10, 19, 20, 10); c.fill()
                c.set_source_rgb(*INK); c.set_line_width(3.4); c.set_line_cap(1)
                c.move_to(7, 28); c.line_to(7, 38); c.line_to(-4, 38); c.stroke()
                c.restore()
            if side == 1 and ro_ > 0.6:                                                # his fist round the insulator
                _oc.ps_hand(k, "fist", hx - 12 * dd_[0], hy - 12 * dd_[1], 64, (0.80, 0.62, 0.50), dd_, 1)
                continue
            if side == 1:                                                             # v2 (decided): his far hand FLAT on the block
                _oc.ps_hand(k, "palm", hx - 12 * dd_[0], hy - 12 * dd_[1], 62, (0.80, 0.62, 0.50), dd_, 1)   # flat, four fingers
                c.set_source_rgba(0.1, 0.08, 0.05, 0.45); c.arc(hx + 6, hy + 4, 8, 0, 2 * math.pi); c.fill()
                continue
            _oc.ps_hand(k, "fist", hx - 12 * dd_[0], hy - 12 * dd_[1], 64, (0.80, 0.62, 0.50), dd_, -1)   # the fist on the wrench
            c.set_source_rgba(0.1, 0.08, 0.05, 0.45); c.arc(hx + 12, hy - 10, 8, 0, 2 * math.pi); c.fill()   # oil
        c.save(); c.translate(0, -30)                                                   # v13 (cold test v37): the whole of him 30 up, the frame wider: both ELBOWS are in it
        _limb(c, (118, 628), (399, 628), 70, 70, INK, 3.5)                               # his shoulders: one yoke from sleeve to sleeve
        ellipse(k, 266, 760, 196, 120, (0.97, 0.97, 0.95), 3490, lw=3)                    # v14 (Tomas: "don't grow the thick white"): his shoulders only;
        _limb(c, (118, 628), (399, 628), 70, 70, (0.97, 0.97, 0.95), 0.0)
        c.save(); c.rectangle(-100, 742, 800, 400); c.clip()                            # below them his overalls, tied at the waist (his own navy)
        ellipse(k, 266, 790, 190, 130, (0.14, 0.20, 0.36), 3489, shadow=False, lw=3)
        c.restore()
        pass                    # his T-shirt back, bent over the wing
        for ex_ in (198, 334):                                                         # v2 (Tomas: "is this the Client?"): HIS head from above:
            ellipse(k, ex_, 652, 13, 20, (0.80, 0.62, 0.50), 3493 + ex_, lw=2.2)        # ears, dark hair combed back in strands, the grey at
        ellipse(k, 266, 650, 66, 60, (0.80, 0.62, 0.50), 3491, lw=2.6)                    # both temples
        ellipse(k, 266, 642, 64, 54, (0.16, 0.13, 0.11), 3492, shadow=False, lw=2.2)
        c.save(); c.new_path(); c.save(); c.translate(266, 642); c.scale(64, 54); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
        c.set_source_rgb(0.62, 0.62, 0.64)
        for sx2_ in (-1, 1):
            c.save(); c.translate(266 + sx2_ * 58, 650); c.scale(17, 40); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
        c.set_source_rgba(0.42, 0.38, 0.35, 0.9); c.set_line_width(2.2); c.set_line_cap(1)
        for j_ in range(5):
            xx_ = 232 + j_ * 17
            c.move_to(xx_, 606 + abs(j_ - 2) * 5); c.curve_to(xx_ - 3, 630, xx_ + 3, 655, xx_ - 2, 682 - abs(j_ - 2) * 4); c.stroke()
        c.restore()
        c.restore()
        if False:                                                                        # v12: the plug is drawn in the fist (above)
            px_, py_ = 250 + (290 - 250) * bo2_, 350 + (215 - 350) * bo2_                   # out of the hole comes ONE thing you can
            c.save(); c.translate(px_, py_); c.rotate(-0.25); c.scale(1.0 + 0.6 * bo2_, 1.0 + 0.6 * bo2_)   # name: a spark plug,
            rect(k, -12, -70, 24, 50, (0.95, 0.94, 0.90), 3480, lw=2.4)                    # its tip black, cracked through
            rect(k, -18, -22, 36, 22, (0.70, 0.72, 0.75), 3481, lw=2.2)                     # the hex
            rect(k, -9, 0, 18, 26, (0.55, 0.56, 0.58), 3482, lw=2)                          # the thread
            c.set_source_rgb(0.08, 0.07, 0.06); c.rectangle(-9, 18, 18, 10); c.fill()        # soot
            c.set_source_rgb(*INK); c.set_line_width(2.6); c.set_line_cap(1)
            c.move_to(-6, -66); c.line_to(2, -54); c.line_to(-4, -44); c.line_to(5, -30); c.stroke()   # the crack
            c.restore()
        wx_, wy_ = hw_[0] - 62 * WD_[0], hw_[1] - 62 * WD_[1]          # HIS gold watch, on the wrench wrist
        ellipse(k, wx_, wy_, 21, 21, (0.86, 0.68, 0.22), 3477, lw=2.2)
        ellipse(k, wx_, wy_, 13, 13, (0.10, 0.16, 0.14), 3478, lw=1.6)
        # v50 (cold test v47, 2 of 3: "it dangles from above like a ceiling light"): the lamp is HELD: the bodyguard's black
        # sleeve and white cuff come in from the top right, his fist round the handle, the cage aimed down at the hands
        la_ = -0.62
        lx_, ly_ = 372, 150
        hx_, hy_ = lx_ + 26 * math.cos(la_), ly_ + 26 * math.sin(la_)
        ux_, uy_ = math.cos(la_), math.sin(la_)
        nx_, ny_ = -uy_, ux_
        w0, w1 = 21, 30
        cut(k, [(hx_ + 14 * ux_ + w0 * nx_, hy_ + 14 * uy_ + w0 * ny_), (hx_ + 240 * ux_ + w1 * nx_, hy_ + 240 * uy_ + w1 * ny_),
                (hx_ + 240 * ux_ - w1 * nx_, hy_ + 240 * uy_ - w1 * ny_), (hx_ + 14 * ux_ - w0 * nx_, hy_ + 14 * uy_ - w0 * ny_)], (0.11, 0.11, 0.13), lw=2.4)
        cut(k, [(hx_ + 10 * ux_ + 19 * nx_, hy_ + 10 * uy_ + 19 * ny_), (hx_ + 22 * ux_ + 20 * nx_, hy_ + 22 * uy_ + 20 * ny_),
                (hx_ + 22 * ux_ - 20 * nx_, hy_ + 22 * uy_ - 20 * ny_), (hx_ + 10 * ux_ - 19 * nx_, hy_ + 10 * uy_ - 19 * ny_)], (0.97, 0.97, 0.95), shadow=False, lw=1.8)
        gs.lamp(k, lx_, ly_, ang=la_, lit=True, glow=False, cable=False)
        _oc.handle_grip(k, hx_, hy_, 24, la_ + math.pi / 2, co_skin())
        c.save(); c.translate(120, 470)                                                 # his red rag, over the block's edge
        # v4 (24 Nov, audit: "a cylinder"; two rags at once): NO rag on the engine: his one rag is in his back pocket
        c.restore()
        gs.protect(c, "his hands in the light", 60, 150, 440, 460)
        c.restore()
    elif kind == "key":                                                            # the steering column, the key, his fingers
        c.set_source_rgb(0.16, 0.16, 0.18); c.paint()                                 # v10 (23 Nov audit, 2 of 3 viewers: "a dial"):
        ku = sh["state"].get("key_u", 1.0)                                            # a CAR: the wheel's rim with its spoke, the
        rr_ = sh["state"].get("run") or 0.0                                           # rev counter whose needle jumps when it
        rect(k, -20, -20, 580, 330, (0.22, 0.22, 0.25), 3428, lw=3)                   # the dashboard
        cx_, cy_ = 300, 118                                                           # its rev counter, seen through the wheel
        ellipse(k, cx_, cy_, 66, 66, (0.10, 0.10, 0.12), 3429, lw=3)
        c.set_source_rgb(0.92, 0.92, 0.88); c.set_line_width(3)
        for i in range(9):
            a0 = math.pi * (0.8 + 1.4 * i / 8)
            c.move_to(cx_ + 50 * math.cos(a0), cy_ + 50 * math.sin(a0)); c.line_to(cx_ + 60 * math.cos(a0), cy_ + 60 * math.sin(a0)); c.stroke()
        an_ = math.pi * (0.8 + 1.4 * (0.05 + (0.55 if rr_ else 0.0) + 0.04 * rr_))
        c.set_source_rgb(1.0, 0.35, 0.2); c.set_line_width(5); c.set_line_cap(1)
        c.move_to(cx_, cy_); c.line_to(cx_ + 52 * math.cos(an_), cy_ + 52 * math.sin(an_)); c.stroke()
        ellipse(k, cx_, cy_, 8, 8, (0.6, 0.6, 0.62), 3427, shadow=False, lw=2)
        WX, WY, WR = 300, 236, 214                                                    # the steering wheel: rim, three spokes, hub
        for col, lw in ((INK, 50), ((0.30, 0.30, 0.33), 42)):
            c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
            c.new_path(); c.arc(WX, WY, WR, 0, 2 * math.pi); c.stroke()
            for ax in (math.pi, 0.0, math.pi / 2):
                c.move_to(WX, WY); c.line_to(WX + WR * math.cos(ax), WY + WR * math.sin(ax)); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.16); c.set_line_width(8)
        c.new_path(); c.arc(WX, WY, WR + 8, 3.6, 5.8); c.stroke()                     # its highlight
        ellipse(k, WX, WY, 50, 44, (0.24, 0.24, 0.27), 3426, lw=3)                     # the hub
        rect(k, 90, 360, 330, 200, (0.22, 0.22, 0.24), 3430, lw=2.6)                   # the column's shroud
        ellipse(k, 300, 460, 56, 56, (0.62, 0.64, 0.66), 3431, lw=2.4)                 # the lock barrel
        c.set_source_rgb(0.15, 0.15, 0.16); c.rectangle(294, 422, 12, 30); c.fill()   # its slot
        for (lx, txt) in ((170, "OFF"), (232, "ON"), (400, "START")):                   # the positions, on the shroud
            gs.T(c, txt, lx, 548, 22, col=(1.0, 0.75, 0.2) if txt == "START" else (0.95, 0.95, 0.90))
        gs.protect(c, "the key at START", 150, 300, 470, 660)
        if sh["state"].get("run"):
            c.translate(sh["state"]["run"], 0)
        c.save(); c.translate(300, 460); c.rotate(-0.5 + 1.4 * ku)                     # the key, turned to START: its blade
        cut(k, [(-9, 0), (9, 0), (9, -60), (3, -66), (9, -72), (9, -84), (-9, -84)], (0.82, 0.82, 0.80), 3432, lw=2)
        rect(k, -26, -132, 52, 52, (0.10, 0.10, 0.12), 3433, lw=2.2)                   # its black head
        c.restore()
        sw_ = 0.25 * math.sin(4.0 * ku) + (0.08 * rr_ if rr_ else 0.0)               # the ring and the fob, swinging
        c.save(); c.translate(318, 500); c.rotate(sw_)
        c.set_source_rgb(0.75, 0.75, 0.72); c.set_line_width(4); c.new_path(); c.arc(0, 26, 20, 0, 2 * math.pi); c.stroke()
        rect(k, -26, 46, 52, 86, (0.08, 0.08, 0.10), 3434, lw=2.4)                     # the fob
        for j, col in enumerate(((0.7, 0.7, 0.72), (0.7, 0.7, 0.72), (0.85, 0.2, 0.2))):
            ellipse(k, 0, 64 + j * 22, 9, 7, col, 3435 + j, shadow=False, lw=1.4)
        c.restore()
        a_ = -0.5 + 1.4 * ku                                                          # oily fingers ON the key head, turning it
        kx, ky = 300 + 122 * math.sin(a_), 460 - 122 * math.cos(a_)
        # v9 (22 Nov, decided): HIS arm, so it reads as the Client in this car: the oily forearm, the white T-shirt sleeve
        ksh_ = (590, ky + 70)                                                          # v12 (24 Nov, cold test v30): his shoulder and chest at the
        kd_ = insert_arm(c, (kx + 26, ky + 14), bend((kx + 26, ky + 14), ksh_, 60, 1), ksh_, 56, (0.80, 0.62, 0.50),   # frame's edge,
                         (0.97, 0.97, 0.95), torso=(0.97, 0.97, 0.95))                         # the elbow bent, a bare forearm
        _oc.ps_hand(k, "fist", kx + 26 - 12 * kd_[0], ky + 14 - 12 * kd_[1], 62, (0.80, 0.62, 0.50), kd_, 1)   # v10 (hand audit):
        c.set_source_rgba(0.1, 0.08, 0.05, 0.5); c.arc(kx + 20, ky + 16, 8, 0, 2 * math.pi); c.fill()         # the series' fist on the key


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
    c.save(); c.translate(92 + st.get("hand_dx", 0.0) + st.get("buzz", 0.0), 680)      # stage 7: walking out; it buzzes (v2: in frame)
    for col, lw in ((INK, 40), (dc.VELVET, 34)):                                     # his sleeve, velvet, going out
        c.set_source_rgb(*col); c.set_line_width(lw); c.set_line_cap(1)
        c.move_to(110, 60); c.line_to(24, 14); c.stroke()
    def scr2(c_):                                                                   # v3 (24 Nov): the one phone UI: an incoming call,
        import of_ui as ui                                                           # red DECLINE, green answer; then DECLINED
        ui.hand(c_, ui.call, "DONNIE", declined=bool(st.get("declined")))
    u_ = st.get("thumb") or 0.0                                                    # v5 (hand audit): the same phone grip as
    tip = (20.5, 3) if not u_ else (20.5 + (-8.7 - 20.5) * u_, 3 + (-1 - 3) * u_)   # v6: it starts BELOW the name, goes to the red button
    tip = None if st.get("donnie_down") else tip   # every phone; its thumb
    oc.phone_grip(k, 7.2, 9.6, 1.07, None if st.get("donnie_down") else scr2, ang=-0.35, skin=dc.SKIN_F,   # goes to the red button
                  body_x=200, thumb_tip=tip)
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
        bob_ = sh["state"].get("robot_bob", 0.0)                       # v2 (23 Nov): it bobs as it talks (the wheel stays down)
        k_.c.save(); k_.c.translate(dl.RX, F + 4); k_.c.scale(1.0, 1.0 + bob_ / 300.0); k_.c.translate(-dl.RX, -(F + 4))
        r = oc.robot(k_, dl.RX, F + 4, rs, turn=float(sh["state"].get("turn", 0.0)), bob=bob_)
        sx_, sy_ = k_.c.user_to_device(*r["screen"]); k_.c.restore(); r = dict(r, screen=k_.c.device_to_user(sx_, sy_))
        heads["_screen"] = r["screen"]
        drawn["robot"] = (r["screen"][0], r["screen"][1], 50 * rs)

    def pam(k_, o):
        don(k_, o)
        import pam_mf as pm_
        pp_ = sh["state"].get("pam_pose", (-8, 0, 140, 60))
        pT_ = (sum(pp_) / 25.0) if isinstance(pp_, tuple) else 0.0
        pm_.GCHAIN_DX[0] = max(-9.0, min(9.0, 1.3 * oc.follow("pam_chain", pT_, 1.3, 0.2)))   # v10: her glasses' chain swings
        draw_p = lambda: pb.pam(k_, 652, F + 6, dl.PS, sh["state"].get("pam_pose", (-8, 0, 140, 60)), sh["state"].get("pam_face", "neutral"),
                                look=tuple(a_ + b_ for a_, b_ in zip(sh["state"].get("pam_look", (0.4, 0.6)), oc.dart("pam", False))), glasses=sh["state"].get("pam_glasses", "up"))   # v8: face, glasses per drawing
        if which == "pam" and not sh["state"].get("phone_down", False):          # v9 (hand audit): her phone's hand is the phone grip's
            q = _oc.held(k_, draw_p, lambda q_: [q_["hands"][1]])
        else:
            q = draw_p()
        pm_.GCHAIN_DX[0] = 0.0
        heads["_pamhand"] = q["hands"][1]
        drawn["pam"] = (q["head"][0], q["head"][1], 50 * dl.PS)
    def office_dressing(k_):
        """v18: the office read 'bare, placeholder-like' to 3 cold viewers vs. the garage's clutter (lesson 163).
        Tomas: augalas, uptimez. A floor plant right of Pam's counter, the UPTIMEZ wordmark on the wall left of the
        portrait. Background layer: drawn before the cast so they occlude it, not the other way round."""
        c = k_.c
        px, py = 672, F + 6                                              # v2: pulled in from 712 — the leaves touched the frame edge

        c.set_source_rgb(0.47, 0.33, 0.22); c.rectangle(px - 20, py - 46, 40, 46); c.fill()
        c.set_source_rgb(0.40, 0.27, 0.18); c.set_line_width(2); c.rectangle(px - 20, py - 46, 40, 46); c.stroke()
        c.set_source_rgb(0.56, 0.40, 0.27); c.rectangle(px - 24, py - 50, 48, 8); c.fill()
        leaf = (0.24, 0.52, 0.30)
        for ang, ln in ((-0.9, 58), (-0.25, 72), (0.3, 70), (0.85, 56)):
            c.set_source_rgb(*leaf); c.set_line_width(10); c.set_line_cap(1)
            c.move_to(px, py - 50)
            c.curve_to(px + 14 * math.sin(ang), py - 50 - ln * 0.5, px + 26 * math.sin(ang), py - 50 - ln * 0.85,
                       px + 30 * math.sin(ang), py - 50 - ln)
            c.stroke()
        sx, sy = 292, 350                                                 # the wordmark, a small plaque left of the portrait
        c.set_source_rgb(0.97, 0.96, 0.92); c.rectangle(sx - 46, sy - 20, 92, 40); c.fill()
        c.set_source_rgb(*INK); c.set_line_width(2); c.rectangle(sx - 46, sy - 20, 92, 40); c.stroke()
        gs.T(c, "UPTIMEZ", sx, sy, 15, col=(0.16, 0.42, 0.55))

    vis = visor_point()
    if which == "wide":
        def wide(k_, o):
            office_dressing(k_)
            pam(k_, o); r = oc.robot(k_, dl.RX, F + 4, rs)
            drawn["robot"] = (r["screen"][0], r["screen"][1], 50 * rs)
        shot = dl.shot("3.1", [dl.h_seat(), vis, dl.hp(652, F + 6, dl.PS)], wide, "", rb=False, chair=False,
                       cam=WIDE_CAM[0])                          # v10: closer (v7 was (434, 640, 0.85): a tiny cast, half the frame floor)
    elif which == "robot":
        shot = dl.shot("3.2", [vis], robot, "", rb=False, zmax=3.6, chair=False, cam=ROBOT_CAM[0] or cf.face_cam([vis], z_max=3.6))
    elif which == "don":
        shot = dl.shot("3.3", [dl.h_seat()], don, "", chair=False)
    else:
        shot = dl.shot("3.6", [dl.hp(652, F + 6, dl.PS)], pam, "", chair=False)
    import fs_storyboard as sb_
    old_rs = sb_.SC["robot"]
    sb_.SC["robot"] = ROBOT_S                                     # the storyboard forces every robot to its SC (0.40) inside a set
    try:                                                          # shot; episode 13 only, restored after the frame
        cam = dl.draw(shot, k)
    finally:
        sb_.SC["robot"] = old_rs
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
        gs.protect(c, "the visor's line", x - 0.82 * r, y - 0.82 * r, x + 0.82 * r, y + 0.82 * r)
        c.set_source_rgb(0.08, 0.12, 0.22); c.arc(x, y, 0.82 * r, 0, 2 * math.pi); c.fill()
        gl = sh["state"].get("visor_glow", 0.0)                                  # stage 7: it glows as it talks
        if gl:
            g_ = cairo.RadialGradient(x, y, 0.1 * r, x, y, 0.82 * r)
            g_.add_color_stop_rgba(0, 0.35, 0.85, 0.95, 0.35 * gl); g_.add_color_stop_rgba(1, 0.35, 0.85, 0.95, 0.0)
            c.set_source(g_); c.arc(x, y, 0.82 * r, 0, 2 * math.pi); c.fill()
        vk = sh["state"].get("visor_k", 1.0)                                     # stage 7: the line pops on
        if sh["state"].get("count") is not None:                                   # v9: MEETING IN 4:59, counting down
            n_ = int(sh["state"]["count"])
            gs.T(c, "MEETING IN", x, y - 0.12 * r, 0.17 * r, col=(0.35, 0.85, 0.95))
            gs.T(c, "%d:%02d" % (n_ // 60, n_ % 60), x, y + 0.42 * r, 0.42 * r, col=(1.0, 0.45, 0.35))
        else:
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
            import of_ui as ui
            ui.hand(c_, ui.invite_small)                                             # DAD not FATHER — it has
            # to read as the same man Don later calls DAD (lesson 163: 2/3 cold viewers had to guess who "him" was)
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
            bxd = (heads["pam"][0] - cam[0]) * z + 270 if "pam" in heads else x - 60   # her middle, on screen
            c.save(); c.translate(x + bz, y); c.scale(z * 0.55, z * 0.55)            # v9 (hand audit): the palm ON her hand, not 40 above
            oc.phone_grip(Ctx(c, 0), 0, 0, 1.0, scr, body_x=(bxd - x - bz) / (z * 0.55)); c.restore()
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


WIDE_CAM = [(450, 660, 0.95)]                         # 3.1 (v10): the cast as big as the button column allows
DON_FAULTS = []                                            # the Don rule's faults for the last desk frame
DON_EDGE = [90]                                            # v9: with the robot at 0.66, the throne further right: both faces clear                                            # 3.4: how far right of the robot the throne slides in
import kit as _kit
import of_cast as _oc
import client_of as _cof
_cof.POCKET_RAG[0] = False                                  # v48 (24 Nov, cold test 3 of 3: "a brick in his pocket"): the rag is in his HAND only
_cof.NEW_RAG[0] = True                                     # v4 (24 Nov): the one shop rag, this film on
_kit.HAND[0] = _oc.cartoon_hand  # v11 (23 Nov, decided): one cartoon hand for everyone, episode 13 only
_kit.ARM_RIM[0] = (0.46, 0.46, 0.52)                       # v1 (23 Nov): the guards' black sleeves get a grey rim
ROBOT_S = 0.66                                             # v11 (22 Nov, Tomas): the largest the Don rule allows (95 % of his height). The storyboard's 0.40
                                                           # and the set's 0.48 both read as a gnome, "a rat", beside the throne


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


def co_skin():
    import client_ob as co_
    return co_.SKIN


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
    def __new__(cls, surf):
        return super().__new__(cls, surf)

    def __init__(self, surf):
        self.texts = []

    def show_text(self, s):
        x, y = self.get_current_point()
        e = self.text_extents(s)
        pts = [self.user_to_device(x + e.x_bearing + dx, y + e.y_bearing + dy) for dx in (0, e.width) for dy in (0, e.height)]
        self.texts.append(dict(text=s, bbox=(min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts),
                                              max(p[1] for p in pts)), clip=(-1e9, -1e9, 1e9, 1e9)))
        return super().show_text(s)


def _limb(c, p, q, w0, w1, col, e=0.0):
    """one tapered limb segment p->q, width w0 -> w1 (+e on every side for the outline pass): a quad and a disc at each end,
    each filled whole, so nothing is left to the arc's winding."""
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    c.set_source_rgb(*col); c.new_path()
    c.move_to(p[0] + nx * (w0 / 2 + e), p[1] + ny * (w0 / 2 + e)); c.line_to(q[0] + nx * (w1 / 2 + e), q[1] + ny * (w1 / 2 + e))
    c.line_to(q[0] - nx * (w1 / 2 + e), q[1] - ny * (w1 / 2 + e)); c.line_to(p[0] - nx * (w0 / 2 + e), p[1] - ny * (w0 / 2 + e))
    c.close_path(); c.fill()
    for (x, y), w in ((p, w0), (q, w1)):
        c.new_path(); c.arc(x, y, w / 2 + e, 0, 2 * math.pi); c.fill()


def bend(hand, shoulder, off, side=1):
    """an elbow between the hand and the shoulder, pushed `off` px sideways (side +1/-1): a clear bend, not a straight band."""
    mx, my = (hand[0] + shoulder[0]) / 2, (hand[1] + shoulder[1]) / 2
    dx, dy = shoulder[0] - hand[0], shoulder[1] - hand[1]; L = math.hypot(dx, dy) or 1.0
    return (mx + side * off * -dy / L, my + side * off * dx / L)


def ease_(u):
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def ik2(hand, shoulder, l1, l2, side):
    """the elbow of a two-bone arm with FIXED lengths (shoulder->elbow l1, elbow->hand l2); side picks the bend."""
    dx, dy = hand[0] - shoulder[0], hand[1] - shoulder[1]
    d = max(1e-6, min(math.hypot(dx, dy), l1 + l2 - 0.5))
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d); h = math.sqrt(max(0.0, l1 * l1 - a * a))
    ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
    return (shoulder[0] + ux * a - uy * h * side, shoulder[1] + uy * a + ux * h * side)


def insert_cuff(c, hand, elbow, w, skin, sleeve, cuff=None, stub=26):
    """v3 (24 Nov, cold test v31: arms read "a pole / floating" 3 of 3 whatever their length; decided "hand + wrist cuff only"):
    NO arm. The hand, big, with a short stub of sleeve and its cuff (a suit), or a bare wrist (a T-shirt). The direction
    is the old forearm's. Returns it, as insert_arm does."""
    dl = math.hypot(hand[0] - elbow[0], hand[1] - elbow[1]); d = ((hand[0] - elbow[0]) / dl, (hand[1] - elbow[1]) / dl)
    back = (hand[0] - d[0] * (stub + 14), hand[1] - d[1] * (stub + 14))
    parts = []
    if cuff is not None:
        parts.append(((back[0], back[1]), (hand[0] - d[0] * 14, hand[1] - d[1] * 14), w * 0.98, w * 0.92, sleeve))
        cx_, cy_ = hand[0] - d[0] * 14, hand[1] - d[1] * 14
        parts.append(((cx_ - d[0] * 6, cy_ - d[1] * 6), (cx_ + d[0] * 6, cy_ + d[1] * 6), w * 0.84, w * 0.84, cuff))
    else:
        parts.append(((back[0], back[1]), (hand[0] - d[0] * 14, hand[1] - d[1] * 14), w * 0.80, w * 0.80, skin))
    for e, ink in ((3.5, True), (0.0, False)):
        for p0, p1, w0, w1, col in parts:
            _limb(c, p0, p1, w0, w1, INK if ink else col, e)
    return d


def insert_arm(c, hand, elbow, shoulder, w, skin, sleeve, cuff=None, torso=None, lit=None, half=None):
    """v2 (24 Nov, cold test v30: 8 of 9 mentions "a pole/tube" for a one-width band from the frame's edge; only the
    DONNIE shot, with the WHOLE person in it, passed): the owner is IN the insert. A forearm that tapers to the wrist,
    a bent elbow, a wider upper arm in his sleeve, and his SHOULDER and a piece of his body (torso colour) behind it.
    A suit's forearm is sleeve with a cuff at the wrist; a T-shirt's is bare. All outlines first, then all colours, so the
    joints are one shape. Returns the forearm's direction into the hand."""
    fore = sleeve if cuff is not None else skin
    up = sleeve if sleeve is not None else skin
    dl = math.hypot(hand[0] - elbow[0], hand[1] - elbow[1]); d = ((hand[0] - elbow[0]) / dl, (hand[1] - elbow[1]) / dl)
    parts = []
    if torso is not None:
        parts.append(("disc", shoulder, 3.8 * w, torso))
    parts.append(("limb", hand, elbow, w * 0.66, w * 1.02, fore))                      # v3 (audit: "a rubber tube"): a narrow wrist, a full
    parts.append(("limb", elbow, shoulder, w * 1.08, w * 1.40, up))                    # forearm, a heavier upper arm
    if cuff is not None:
        cx_, cy_ = hand[0] - d[0] * 14, hand[1] - d[1] * 14
        parts.append(("limb", (cx_ - d[0] * 6, cy_ - d[1] * 6), (cx_ + d[0] * 6, cy_ + d[1] * 6), w * 0.84, w * 0.84, cuff))
    if lit is not None:                                                               # its contact shadow on what is under it
        c.push_group()
        _limb(c, (hand[0] + 9, hand[1] + 12), (elbow[0] + 9, elbow[1] + 12), w * 0.9, w * 1.1, (0.05, 0.05, 0.06), 0.0)
        c.pop_group_to_source(); c.paint_with_alpha(0.30)
    for e, ink in ((3.5, True), (0.0, False)):
        for pt in parts:
            if pt[0] == "disc":
                c.set_source_rgb(*(INK if ink else pt[3])); c.new_path(); c.arc(pt[1][0], pt[1][1], pt[2] / 2 + e, 0, 2 * math.pi); c.fill()
            else:
                _limb(c, pt[1], pt[2], pt[3], pt[4], INK if ink else pt[5], e)
    if half is not None:                                                              # a short sleeve: the upper arm's top half
        m_ = (shoulder[0] + (elbow[0] - shoulder[0]) * 0.38, shoulder[1] + (elbow[1] - shoulder[1]) * 0.38)   # v2 (Tomas: "the thick white"): a SHORT sleeve,
        _limb(c, m_, shoulder, w * 1.26, w * 1.34, INK, 3.5); _limb(c, m_, shoulder, w * 1.26, w * 1.34, half, 0.0)   # no wider than the arm in it
    if lit is not None:                                                               # the lamp's warm light along the side that faces it
        for p_, q_, ww in ((hand, elbow, w * 0.8),) + (() if half is not None else ((elbow, shoulder, w * 1.2),)):
            mx_, my_ = (p_[0] + q_[0]) / 2, (p_[1] + q_[1]) / 2
            lx_, ly_ = lit[0] - mx_, lit[1] - my_; ll_ = math.hypot(lx_, ly_) or 1.0
            ax_, ay_ = q_[0] - p_[0], q_[1] - p_[1]; al_ = math.hypot(ax_, ay_) or 1.0
            nx_, ny_ = -ay_ / al_, ax_ / al_
            sg_ = 1 if nx_ * lx_ + ny_ * ly_ > 0 else -1
            c.set_source_rgba(1.0, 0.93, 0.70, 0.30); c.set_line_width(ww * 0.22); c.set_line_cap(1)
            c.move_to(p_[0] + nx_ * sg_ * ww * 0.26 + ax_ * 0.12, p_[1] + ny_ * sg_ * ww * 0.26 + ay_ * 0.12)
            c.line_to(q_[0] + nx_ * sg_ * ww * 0.26 - ax_ * 0.12, q_[1] + ny_ * sg_ * ww * 0.26 - ay_ * 0.12); c.stroke()
    return d


def hand_check():
    """v1 (23 Nov, hand audit, decided): one hand per wrist, and a held phone's thumb toward the body. Reads the hands
    the frame really drew (of_cast.HAND_LOG, GRIP_LOG), in frame units."""
    import hand_gate
    return hand_gate.check(_oc.GRIP_LOG, _oc.HAND_LOG, _oc.HAND_TOL)


def render(sh, scene):
    """-> (surface at 1080, the uz_check frame record, the camera)."""
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920)
    surf.set_device_scale(2, 2)
    del gs.PROTECT[:]
    del _oc.HAND_LOG[:], _oc.GRIP_LOG[:]                          # v1 (23 Nov, hand audit): every hand in this frame
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
        grade(c, 4)
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
        grade(c, scene)
    # the text in set units, for check_signs (it maps them through the camera itself)
    fx, fy, z = cam if isinstance(cam, tuple) else (270, 480, 1.0)
    text = []
    # user_to_device is 540 device space. set_device_scale is not part of that matrix, so a sign at
    # frame centre (270, 480) is already (270, 480) here; dividing by the scale would move it.
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
    msgs += hand_check()
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


if __name__ == "__main__" and not (len(sys.argv) > 1 and sys.argv[1] in ("board", "zones-validate", "don-validate", "hand-validate")):
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


def _speech_too_tall(surf, sh, who, txt, fc, cam, va_):
    """draw the repo's bubble on a scratch copy and measure it: True when it needs more than 3 rows."""
    import speech
    speech.SIZE[0], speech.MONO_SIZE[0], speech.MAX_W[0], speech.MONO_BOLD[0], speech.SIGNS_FIRST[0] = 30, 28, 300, True, True
    if who == "robot" or va_:
        return False
    if sh["state"].get("bubble_over") or any(p[0] == "his open hand" for p in gs.PROTECT):          # his gesture beside his face: the bubble goes over his head
        return True
    scratch = cairo.ImageSurface(cairo.FORMAT_RGB24, surf.get_width(), surf.get_height())
    sc_ = cairo.Context(scratch); sc_.scale(surf.get_width() / 540.0, surf.get_height() / 960.0)
    head = fc[who]
    box, _ = speech.draw(Ctx(sc_, 0), txt, head, mouth=(head[0], head[1] + 0.35 * head[2]),
                         others=[v for n, v in fc.items() if n != who], avoid=[p[1:] for p in gs.PROTECT])
    return (box[3] - box[1]) > 30 * 1.15 * 3 + 20


BUBBLE_AT = {                                               # v48: lines placed by hand, in the 540 x 960 frame, per camera
    "0.5": dict(at={"'under'": (30, 664)}, tip={"'under'": (186, 606)}, rows=["Is it wrong?"]),   # v49: off his working hands
    "2.1": dict(at={"*": (26, 430)}, rows=["My son says his", "machine finds anything."]),   # v51: one picture, pushing in
    "2.4": dict(at={"*": (26, 430)}, rows=["How would you", "run his company?"]),
    "2.6": dict(at={"(450, 640, 2.0)": (26, 470)}, rows=["And then?"]),
    "2.8b": dict(at={"['client']": (355, 140), "(575, 785, 2.6)": (355, 140)}, rows=["One month.", "I ask.", "She finds it."]),
    "2.8c": dict(at={"['father', 'client']": (60, 330)}, rows=["Done."]),
    "2.9": dict(at={"(170, 795, 1.8)": (330, 140), "(172, 752, 2.6)": (330, 140)}, rows=["Put it in the", "calendar."]),   # v51: one place across the cut
}


def robot_peek(c, x, y, r):
    """v51: the robot's own head, small, peeking in at the frame's left edge (it sits left of Don): navy round visor,
    the cyan eager eyes and smile, the antenna; the off-screen card's tail points at it."""
    cyan = (0.45, 0.92, 1.0)
    c.save()
    c.set_line_width(3); c.set_source_rgb(*kit.INK if hasattr(kit, "INK") else (0.1, 0.1, 0.12))
    c.move_to(x + 0.15 * r, y - r); c.line_to(x + 0.3 * r, y - 1.55 * r); c.stroke()
    c.arc(x + 0.3 * r, y - 1.62 * r, 0.16 * r, 0, 2 * math.pi); c.set_source_rgb(1.0, 0.82, 0.2); c.fill_preserve()
    c.set_source_rgb(0.1, 0.1, 0.12); c.set_line_width(2); c.stroke()
    c.arc(x, y, r * 1.08, 0, 2 * math.pi); c.set_source_rgb(0.93, 0.94, 0.95); c.fill_preserve()
    c.set_source_rgb(0.1, 0.1, 0.12); c.set_line_width(3); c.stroke()
    c.arc(x, y, r * 0.86, 0, 2 * math.pi); c.set_source_rgb(0.09, 0.12, 0.24); c.fill()
    c.set_source_rgb(*cyan); c.set_line_width(3.2); c.set_line_cap(1)
    for e in (-1, 1):
        c.new_path(); c.arc(x + 0.12 * r + e * 0.30 * r, y - 0.08 * r, 0.13 * r, math.pi * 1.1, math.pi * 1.9); c.stroke()
    c.new_path(); c.arc(x + 0.12 * r, y + 0.12 * r, 0.32 * r, 0.25 * math.pi, 0.75 * math.pi); c.stroke()
    c.restore()


def man_at(man, cam):
    """v51: a hand-placed box for this camera; "*" = every camera of the shot (a push-in under a line)."""
    return man["at"].get(repr(cam), man["at"].get("*"))
BUBBLE_LOCKS = {}                                           # (shot, camera, text) -> the bubble as it was drawn ONCE for that picture
BUBBLE_LOCK_ON = [True]
BUBBLE_UNLOCKED = []                                        # frames whose bubble was placed on the spot (the gate fails on any)


def bubble_key(sh):
    return (sh["id"], repr(sh["cam"]), sh["state"].get("say_txt"))


def lock_bubble(sh, scene):
    """v47 (24 Nov, Tomas: "the bubble jumps in several places", decided): a bubble is placed ONCE for a picture (one
    camera, one text) and then stands still: it was placed again on every drawing from the head, so it flipped sides
    (1.4), shook with the frame (0.9), bobbed with a nodding or walking head (3.2, 2.9) and slid with a lean (2.4).
    The frame is drawn with and without the bubble; what differs IS the bubble (box, text, tail), kept as a layer."""
    import numpy as np
    from scipy import ndimage
    a, msgs = _board_frame_raw(sh, scene, True)
    b, _ = _board_frame_raw(sh, scene, False)
    A = np.ndarray((a.get_height(), a.get_width(), 4), np.uint8, a.get_data()).copy()
    B = np.ndarray((b.get_height(), b.get_width(), 4), np.uint8, b.get_data())
    m = ndimage.binary_fill_holes((np.abs(A.astype(int) - B.astype(int))[..., :3].max(axis=2) > 0))
    P = np.zeros_like(A); P[m] = A[m]; P[m, 3] = 255
    patch = cairo.ImageSurface.create_for_data(bytearray(P.tobytes()), cairo.FORMAT_ARGB32, a.get_width(), a.get_height())
    ys, xs = np.nonzero(m)
    BUBBLE_LOCKS[bubble_key(sh)] = (patch, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None)
    return msgs


def board_frame(sh, scene, bubble=True):
    """the frame with its line's bubble: the picture's LOCKED bubble when there is one (lock_bubble), laid over the frame
    after everything, so a camera jolt does not move it."""
    if not bubble or sh["id"] not in SAY or not BUBBLE_LOCK_ON[0]:
        return _board_frame_raw(sh, scene, bubble)
    if sh["id"] in BUBBLE_AT and man_at(BUBBLE_AT[sh["id"]], sh["cam"]):   # placed by hand: its box is fixed, its tail follows the mouth
        return _board_frame_raw(sh, scene, True)
    lk = BUBBLE_LOCKS.get(bubble_key(sh))
    if lk is None:
        BUBBLE_UNLOCKED.append(bubble_key(sh))
        return _board_frame_raw(sh, scene, True)
    surf, msgs = _board_frame_raw(sh, scene, False)
    lk[0].set_device_scale(*surf.get_device_scale())                   # pixel for pixel, whatever the frame's scale
    c = cairo.Context(surf); c.identity_matrix(); c.set_source_surface(lk[0], 0, 0); c.paint(); surf.flush()
    return surf, msgs


def _board_frame_raw(sh, scene, bubble=True):
    """-> (surface 540 x 960 at 2x, problems). The frame, its line's bubble, and the pixel check of the tail."""
    import numpy as np
    import fs_animatic as an
    MOUTH_AT.clear()
    surf, f, cam, msgs = render(sh, scene)
    if sh["id"] not in SAY or not bubble:
        return surf, msgs
    who, txt = SAY[sh["id"]]
    txt = sh["state"].get("say_txt", txt)                             # v12: a long line shown in parts (bigger bubbles)
    fc = uz.faces(f) if sh["cam"] not in ("under",) else {n: tuple(v) for n, v in f["heads"].items()}
    if sh["cam"] == "desk":                                           # the desk frame's heads are in set units already mapped
        fc = {n: ((v[0] - cam[0]) * cam[2] + 270, (v[1] - cam[1]) * cam[2] + 480, v[2] * cam[2]) for n, v in f["heads"].items()}
        fc = {("don" if n in ("don", "seat") else n): v for n, v in fc.items()}
    man = BUBBLE_AT.get(sh["id"])
    if man and who in fc and man_at(man, sh["cam"]):
        # v48 (24 Nov, decided after cold test v47: the bubble jumped across cuts inside a line and sat on the lamp hand
        # and the phone): this line's box is PUT, the same place in every picture of its shot; the tail goes to the mouth
        # drawn in THIS frame, so it follows him.
        head = fc[who]
        mth = (head[0], head[1] + 0.35 * head[2])
        if who in MOUTH_AT and sh["cam"] not in ("under", "insert", "desk"):
            mx, my = MOUTH_AT[who]
            mth = ((mx - cam[0]) * cam[2] + 270 - 2, (my - cam[1]) * cam[2] + 480 - 3)
        import speech
        c = cairo.Context(surf); k_ = Ctx(c, 0)
        rows = man.get("rows") or [txt]
        size = 30
        c.select_font_face(kit.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
        bw = max(c.text_extents(r_).x_advance for r_ in rows) + 28
        bh = size * 1.15 * len(rows) + 18
        x0, y0 = man_at(man, sh["cam"])
        box = (x0, y0, x0 + bw, y0 + bh)
        cx_, cy_ = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
        d_ = math.hypot(cx_ - mth[0], cy_ - mth[1]) or 1.0
        tip = (mth[0] + (cx_ - mth[0]) / d_ * head[2] * 0.42, mth[1] + (cy_ - mth[1]) / d_ * head[2] * 0.30)
        tip = man.get("tip", {}).get(repr(sh["cam"]), tip)            # a turned head: the tip given too
        speech.SIZE[0], speech.MONO_SIZE[0], speech.MAX_W[0], speech.MONO_BOLD[0], speech.SIGNS_FIRST[0] = 30, 28, 300, True, True
        speech._paint(k_, box, tip, rows, size, kit.FONT, False)
        surf.flush()
        return surf, msgs
    va_ = sh["state"].get("voice_at")                                 # v13 (23 Nov, cold tests 3 of 3, decided): a voice from a
    if va_:                                                           # place we see but a face we don't (under the car): the tail
        fc[who] = ((va_[0] - cam[0]) * cam[2] + 270, (va_[1] - cam[1]) * cam[2] + 480, 14.0)   # goes INTO that dark
    if who not in fc and sh["state"].get("off_voice"):                # v49: the speaker is out of this picture (a cut inside
        import speech                                                  # its line): a named card, top left, as the repo draws one
        speech.SIZE[0], speech.MONO_SIZE[0], speech.MAX_W[0], speech.MONO_BOLD[0], speech.SIGNS_FIRST[0] = 30, 28, 300, True, True
        ov = sh["state"]["off_voice"]                                  # its rows in the robot's own caps, beside the listener,
        c = cairo.Context(surf)                                         # clear of his crown; the tail points out of the frame, to it
        c.select_font_face(kit.MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(28)
        bw = max(c.text_extents(r_).x_advance for r_ in ov["rows"]) + 28
        bh = 28 * 1.15 * len(ov["rows"]) + 18
        x0, y0 = ov["at"]
        hy_ = y0 + bh * 0.5
        pk = ov.get("peek", 1.0)                                       # v52 (audit: "a glued-on icon"): it LEANS IN from the edge,
        if pk > 0.02:                                                  # bigger, tipped, and leans out after the line
            c.save(); c.translate(-62 + 92 * pk, y0 + 2); c.rotate(0.30 * (1 - pk) - 0.12 * pk); robot_peek(c, 0, 0, 46); c.restore()
        if pk > 0.35:                                                  # its card comes and goes with it, under its chin
            speech._paint(Ctx(c, 0), (x0, y0 + 26, x0 + bw, y0 + 26 + bh), (x0 - 6, y0 + 34), ov["rows"], 28, kit.MONO, True)
                                           # v51 (cold test v50, 3 of 3: "Don says it"): WHO says it
        surf.flush()
        return surf, msgs
    if who not in fc:
        return surf, msgs + ["BUBBLE: %s speaks but is not in the frame" % who]
    if SPEECH[0] and not _speech_too_tall(surf, sh, who, SAY[sh["id"]][1], fc, cam, va_):   # the WHOLE line decides: its parts share one place   # v40: a line that would wrap past 3 rows
        import speech                                                  # beside the face keeps the v39 bubble over the head
        import speech_gate
        head = fc[who]
        if who == "robot":                                          # the head point is the visor, as drawn
            head = (head[0], head[1], head[2] * 1.15)
            fc[who] = head
        mouth = (head[0], head[1] + 0.35 * head[2])
        aim = None
        if who in MOUTH_AT and sh["cam"] not in ("under", "insert", "desk"):
            mx, my = MOUTH_AT[who]
            mx, my = (mx - cam[0]) * cam[2] + 270, (my - cam[1]) * cam[2] + 480
            aim = (mx - 2, my - 3)                                  # the mouth this pose drew, not the face centre
        if sh["cam"] == "under":
            side = 1 if head[0] < 270 else -1
            aim = (head[0] + side * head[2] * 0.98, head[1] + head[2] * 0.05)
        if who == "robot":
            # the left rim at eye height, so the line sits clear of the visor card
            aim = (head[0] - head[2], head[1] - head[2] * 0.05)
        if va_:
            # the hips in the dark under the car are the mechanic; the tip lands on him, the line sits clear
            hipx = (gs.CREEPER[0] - cam[0]) * cam[2] + 270
            hipy = (gs.CREEPER[1] - 46 - cam[1]) * cam[2] + 480
            hr = 26 * cam[2]
            head = (hipx, hipy, hr)
            fc[who] = head
            side = 1 if hipx < 270 else -1
            aim = (hipx + side * hr, hipy)
        before = speech_gate.snapshot(surf)
        c = cairo.Context(surf)
        speech.SIZE[0], speech.MONO_SIZE[0], speech.MAX_W[0], speech.MONO_BOLD[0], speech.SIGNS_FIRST[0] = 30, 28, 300, True, True   # v40 (24 Nov, decided):
        av_ = [p[1:] for p in gs.PROTECT]                                # the repo's bubble, read on a phone; never over a story prop
        above_ = (head[0] - head[2] * 0.35, head[1] - head[2] * 0.97) if who == "robot" else None   # people: beside the mouth only
        top_ = bool(sh["state"].get("bubble_top"))                       # v47 (2.9): no wall beside his mouth that is not his man's
        if top_:                                                         # face or the phone: two short rows OVER his head, the
            above_ = (head[0], head[1] - head[2] * 1.02); aim = None      # tail down to his crown
            speech.MAX_W[0] = 190
        speech.TOP_FIRST[0] = top_
        if who == "robot":                                               # over the antenna, never across the visor's card
            aim = None
        box, tip = speech.draw(Ctx(c, 0), txt.upper() if who == "robot" else txt, head, mouth=mouth, aim=aim, above=above_,
                               mono=(who == "robot"), others=[v for n, v in fc.items() if n != who], avoid=av_)
        gp_ = speech_gate.check(surf, box, tip, list(fc.values()), aim=aim, before=before)
        speech.TOP_FIRST[0] = False
        if who == "robot" or top_:                                       # the visor's dark rim is not hair: the tip is ON the visor
            gp_ = [m for m in gp_ if not m.startswith("TAIL on hair or eyes")]
        return surf, list(msgs) + gp_
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
    if sh["cam"] == "under":                                          # v12: head UP the frame (turned): his mouth is below the
        tail = (head[0] + 0.50 * head[2], head[1] + 0.30 * head[2], 10) if UPRIGHT[0] else \
            (head[0] + 0.30 * head[2], head[1] - 0.50 * head[2], 10)  # face's middle; the tip on the cheek beside it
    if who == "robot":                                                # to the visor's rim, never across its card
        tail = (head[0] - head[2] * 0.62, head[1] - head[2] * 0.62, 2)
    if va_:
        tail = (head[0], head[1], 2)
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
        if va_:
            if math.hypot(xs[i] / 2.0 - head[0], ys[i] / 2.0 - head[1]) > 22:
                probs.append("TAIL %s: the tip (%d, %d) is not at the voice (%d, %d)" % (sh["id"], xs[i] / 2, ys[i] / 2, head[0], head[1]))
        elif who != "robot" and not _skin_near(before, xs[i], ys[i], 6):
            probs.append("TAIL %s: the tip (%d, %d) is not beside skin (hair, wall or collar)" % (sh["id"], tx, ty))
        hx, hy, r = head
        if who == "robot" and math.hypot(tx - hx, ty - hy) > 1.0 * r:
            probs.append("TAIL %s: the tip (%d, %d) is not on the visor" % (sh["id"], tx, ty))
        if who != "robot" and sh["cam"] != "under" and not va_ and not (hy - 0.1 * r <= ty <= hy + 1.4 * r):
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


def hand_validate():
    """v1 (23 Nov, hand audit): the hand gate on planted faults. 2.7 with held() switched off (the rig's hand drawn under
    the phone) and 3.7 with a phone thumb forced outward must fail; the real frames must pass."""
    import of_film as ff
    def frame(sid, t):
        for title, where, scene, shots in SCENES:
            for sh0 in shots:
                if sh0["id"] == sid:
                    L = _timing()[sid]["len"]
                    st_over, pose_over = ff.MOTION.get(sid, ff.still)(t, L)
                    st_over = dict(st_over); cam_ = st_over.pop("_cam", None); st_over.pop("_cast", None)
                    sh = dict(sh0, state=dict(sh0["state"], **st_over))
                    if cam_ is not None:
                        sh["cam"] = cam_
                    saved = POSES.get(sid)
                    if pose_over:
                        base = dict(saved or {})
                        for who, ps in pose_over.items():
                            base[who] = dict(base.get(who, {}), **ps)
                        POSES[sid] = base
                    try:
                        return [m for m in render(sh, scene)[3] if m.startswith("HAND")]
                    finally:
                        if saved is None:
                            POSES.pop(sid, None)
                        else:
                            POSES[sid] = saved
    real = frame("2.7", 0.5) + frame("3.7", 0.9) + frame("1.3", 0.6)
    _oc.HELD_OFF[0] = True
    try:
        planted1 = frame("2.7", 0.5)
    finally:
        _oc.HELD_OFF[0] = False
    pg = _oc.phone_grip
    def wrong(*a, **kw):
        kw["thumb"] = -_oc.inner_thumb(a[1], kw["body_x"], kw.get("back", False)) if kw.get("body_x") is not None else 1
        return pg(*a, **kw)
    _oc.phone_grip = wrong
    try:
        planted2 = frame("2.7", 0.5)
    finally:
        _oc.phone_grip = pg
    ok = not real and any("two at one wrist" in m for m in planted1) and any("outer side" in m for m in planted2)
    print("hand gate: real", real or "pass", "| planted two hands:", planted1, "| planted thumb:", planted2)
    return ok


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "hand-validate":
    sys.exit(0 if hand_validate() else 1)
