"""APPROVED. (episode 16): the scene file, v1 (stage 4, series/production-process.md rule 1: one source).

From here on this file is the episode's shot list. Every shot's text (picture, reaction, line, sound) was moved here
once from script v4 (the-review-script-v4.md) and is edited here from now on, with the amendments below. Its staging
(setup, size, cast, Don's side of the tape, the Client's place) and the props' states are records next to it; its
timing is rv_timing_v1.json (the picked takes). Generated from it:

  python3 rv_scenes.py [out_dir]  ->  the-review-script-v5.md   (generated; do not edit by hand)
                                     the checks below, printed; exit 1 on a failure not listed in KNOWN

The checks (data, before any layout is drawn; Tomas 28 Nov /grill-me: all four):
  lines   no two lines overlap; every line ends inside its shot; every line names its speaker (lesson 169)
  loop    the last frame's state equals frame 0's for everything K1 shows (the card under the caster and its word,
          the blanket, Don's pose, the robot's screen, the confetti); what K1 hides is listed with the reason
  tape    Don is on his own side (A+B, screen left of the tape at x 560) except between the two crossings, and he
          crosses only in a shot whose picture shows the crossing; the Client never stands on Don's floor line
  props   every story prop has a state in every shot (the tag, the HR card, the report and its spill, the Client's
          card, the invoice, Father's chair, Pam's mug, the needle, the robot's screen); a state changes only in a
          shot whose text shows it; the needle never moves on a line or a peak (E15's rule for the robot's clips)
Layouts (stage 4.3) are drawn from the same records: rv_layouts.py (next).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..", "the-review")
TEMPLATE = os.path.join(EP, "the-review-script-v4.md")      # the prose around the tables (frozen at v4)
TIMING = os.path.join(EP, "rv_timing_v1.json")
TAKES = os.path.join(HERE, "rv_voices", "takes", "takes.json")

TEXT = {'1.1': {'setup': 'S4 · C',
         'picture': '**Frame 0 (K1), night:** Don asleep in the throne, tilted back, his weight on it; a folded card '
                    "wedges the front caster. **0:00.4 the robot's gripper pulls the card; 0:00.6 the throne rolls "
                    'back** and Don slides off its front',
         'reaction': '—',
         'line': '—',
         'sound': "(from the loop's end: a soft hum) caster squeak; a slither"},
 '1.2': {'setup': 'S4 · C',
         'picture': 'Don on his back on the floor, eyes still shut; **he raises the empty cup straight up**, like a '
                    'baby bird',
         'reaction': 'the cup stays up; 0.5 s',
         'line': '**DON: "Pam! Coffee."**',
         'sound': 'a night hum'},
 '1.3': {'setup': 'S6 · M',
         'picture': "Behind the counter, in her monitor's glow, Pam holds the MY GARAGES blueprint open. She looks "
                    'at the raised cup and **turns to the next page**. Her mustard mug sits by the coffee machine '
                    '(needle green)',
         'reaction': '—',
         'line': '—',
         'sound': 'a page turn'},
 '1.4': {'setup': 'S1 · W',
         'picture': 'Polished shoes and the burgundy hem walk in (A). **Father unfolds a cheap folding chair on the '
                    'tape**, beside the throne. Don still on the floor, cup up',
         'reaction': 'Father glances at the throne, then at his chair',
         'line': '**FATHER: "Executive."**',
         'sound': 'a folding-chair clack'},
 '1.5': {'setup': 'S3 · MC',
         'picture': "The chair **wobbles** under Father's hand. The Client comes round the counter's left end and "
                    'kneels at the leg without being asked: **a washer from his pocket, under the leg**',
         'reaction': 'Father watches his hands',
         'line': '—',
         'sound': "a washer's tink"},
 '1.6': {'setup': 'S3 · M',
         'picture': "Father sits and **leans hard to one side**; the chair doesn't budge. His eyes go to the gold "
                    'throne, then to the Client',
         'reaction': 'the Client back on his feet behind the counter; 0.5 s',
         'line': '—',
         'sound': "a creak that doesn't come"},
 '1.7': {'setup': 'S3 · I',
         'picture': "The ringed hand turns the tag on the throne's back: **REVIEW · TOMORROW → REVIEW · TODAY**",
         'reaction': 'the tag swings, settles',
         'line': '—',
         'sound': 'tag flick'},
 '2.1': {'setup': 'S1 · W',
         'picture': 'Don scrambles up. **Sofía is quicker:** she sits in the throne, chin up, legs crossing. '
                    "**Father's eyes go past her before she is down**",
         'reaction': 'she finishes sitting anyway',
         'line': '—',
         'sound': "a cushion's puff"},
 '2.2': {'setup': 'S3 · MC',
         'picture': 'Sofía gets up, smoothing her skirt; **her eyes are already on the robot**',
         'reaction': '—',
         'line': '—',
         'sound': 'heels'},
 '2.3': {'setup': 'S2 · M',
         'picture': 'The robot rolls up, holding out a report. **Father raises his palm** before it can present it. '
                    'The robot slowly retracts the report',
         'reaction': '—',
         'line': '—',
         'sound': 'a servo whine down'},
 '2.4': {'setup': 'S3 · I',
         'picture': "The robot's screen: **POSITION VACANT** (it left HR to apply)",
         'reaction': '—',
         'line': '—',
         'sound': 'a soft blip'},
 '2.5': {'setup': 'S3 · MC',
         'picture': "**Sofía's eyes snap to the screen; she pivots on the spot:** unpins the HR card from its chest, "
                    'pins it on her jacket, checks it hangs straight, and points the robot to the corner',
         'reaction': 'the robot looks at the corner',
         'line': '**SOFÍA (professional): "We\'ll be in touch."**',
         'sound': "a pin's click"},
 '2.6': {'setup': 'S3 · C',
         'picture': "The robot's face: **one oil drop rolls down**. Then the screen goes flat: **NOTED.**",
         'reaction': '0.5 s',
         'line': '—',
         'sound': 'a drip; a flat beep'},
 '2.7': {'setup': 'S1 · W',
         'picture': 'It rolls to its station in A, the report still in its gripper',
         'reaction': 'Don watches it go, pleased',
         'line': '—',
         'sound': 'a wheel'},
 '3.1': {'setup': 'S1 · W',
         'picture': "Don will show he doesn't need Pam. He **steps over his own tape** to the counter (Father's "
                    'side), glancing down at the line as he crosses',
         'reaction': 'Father watches',
         'line': '—',
         'sound': 'a step'},
 '3.2': {'setup': 'S6 · MC',
         'picture': 'At the machine for the first time in his life: **the filter goes in upside down**. The Client, '
                    "on the customer side, watches. Pam, behind, doesn't move",
         'reaction': '—',
         'line': '**DON (to Father, proud): "I usually delegate."**',
         'sound': 'a plastic clunk'},
 '3.3': {'setup': 'S6 · I',
         'picture': 'The panel: **HUMAN APPROVAL REQUIRED**',
         'reaction': '—',
         'line': '—',
         'sound': 'a polite chime'},
 '3.4': {'setup': 'S6 · MC',
         'picture': '**Don, eyes on Father, not the panel, jabs the button with a fingertip** (gesture 1)',
         'reaction': '—',
         'line': '**DON: "Approved."** · **PANEL: "Human approval required."** comes first, under 3.3',
         'sound': "the button's click"},
 '3.5': {'setup': 'S6 · I',
         'picture': 'The needle swings into the yellow; **the machine shudders a step toward the counter edge**',
         'reaction': '—',
         'line': '—',
         'sound': 'a rising gurgle'},
 '3.6': {'setup': 'S6 · MC',
         'picture': "A small **tick** from the machine: **only the Client's head turns**",
         'reaction': "Don hasn't heard",
         'line': '—',
         'sound': 'tick'},
 '3.7': {'setup': 'S6 · M',
         'picture': '**A visible jet of steam with a hiss.** The Client is already dropping flat below the counter, '
                    "eyes shut; his hand, without looking, **catches Pam's mug by its handle** as it slides off the "
                    'edge',
         'reaction': 'Pam, behind the counter, looks at the hand holding her mug',
         'line': '—',
         'sound': 'hiss; a soft catch, no smash'},
 '3.8': {'setup': 'S6 · I',
         'picture': 'The cup: the coffee drops in **one tar-like glug**; the spoon stands upright in it by itself',
         'reaction': '—',
         'line': '—',
         'sound': 'glug'},
 '3.9': {'setup': 'S1 · W',
         'picture': "Don carries the cup back over his tape and **sets it on the throne's armrest** beside Father's "
                    'chair',
         'reaction': "Father doesn't touch it; 0.6 s",
         'line': '—',
         'sound': 'a saucerless clack'},
 '3.10': {'setup': 'S3 · C',
          'picture': "Father's eyes: the cup, then away",
          'reaction': '—',
          'line': '—',
          'sound': '—'},
 '4.1': {'setup': 'S1 · W',
         'picture': "Father props the **Client's name card** (wrench pictogram, his name) on the throne's seat",
         'reaction': "Don's face falls: he is losing the chair",
         'line': '—',
         'sound': 'card on leather'},
 '4.2': {'setup': 'S6 · MC',
         'picture': 'Father leans to the Client, flat under the counter, the mug still in his hand. **A barely '
                    'visible smile, for the Client only**',
         'reaction': '—',
         'line': '**FATHER: "Good hands."**',
         'sound': '—'},
 '4.3': {'setup': 'S4 · MC',
         'picture': '**Don has seen the smile. He looks down at his own hands**',
         'reaction': '0.6 s',
         'line': '—',
         'sound': '—'},
 '4.4': {'setup': 'S6 · M',
         'picture': 'Pam, **her eyes going from Father to the robot in the corner**, the refused report in its '
                    'gripper',
         'reaction': '—',
         'line': '**PAM: "Did anyone review the business?"**',
         'sound': '—'},
 '4.5': {'setup': 'S1 · W',
         'picture': "Nobody moves. In A the robot's head lifts",
         'reaction': '—',
         'line': '—',
         'sound': '—'},
 '5.1': {'setup': 'S2 · M',
         'picture': 'The robot at its station, head up',
         'reaction': '—',
         'line': '**ROBOT: "Yes."**',
         'sound': '—'},
 '5.2': {'setup': 'S1 · W',
         'picture': "It rolls to Father. **The report unfurls from its chest, accordion-folding over Don's shoes**; "
                    'Don steps back; the paper follows; another step, more paper',
         'reaction': '—',
         'line': '—',
         'sound': 'a long printer rattle'},
 '5.3': {'setup': 'S3 · MC',
         'picture': '**The gripper tears off one sheet and holds it out to Father across a clear gap; Father takes '
                    'it in his fingertips**',
         'reaction': '—',
         'line': '—',
         'sound': 'a tear'},
 '5.4': {'setup': 'S3 · I',
         'picture': 'The sheet: **COFFEE MACHINE REPAIR · $80 · UNPAID** (a red stamp)',
         'reaction': '—',
         'line': '—',
         'sound': '—'},
 '5.5': {'setup': 'S3 · MC',
         'picture': 'Father folds it into his inside pocket and reads the report, the only one reading anything',
         'reaction': '—',
         'line': '—',
         'sound': 'paper'},
 '5.6': {'setup': 'S3 · I',
         'picture': "The robot's screen: **UPTIME 100%**",
         'reaction': '—',
         'line': '—',
         'sound': 'a blip'},
 '5.7': {'setup': 'S4 · C',
         'picture': 'Don: **his eyes close mid-yawn, his head nods, he jerks awake**',
         'reaction': 'hold 0.5 s',
         'line': '—',
         'sound': 'a yawn'},
 '5.8': {'setup': 'S3 · I',
         'picture': "The robot's screen: **SALARY $0**",
         'reaction': '—',
         'line': '—',
         'sound': 'a blip'},
 '5.9': {'setup': 'S3 · MC',
         'picture': 'Father **straightens in his cheap chair**; his eye goes up to the **$49,999 tag on the crown**',
         'reaction': 'hold 0.4 s before the line',
         'line': '**FATHER (slow, quiet): "There it is."**',
         'sound': 'the chair creaks now'},
 '5.10': {'setup': 'S4 · MC',
          'picture': 'Don, **smiling proudly** at Father: he thinks Father admires the chair. **He tilts the '
                     "throne's back to show it**",
          'reaction': 'hold 0.5 s',
          'line': '**DON: "It reclines."**',
          'sound': '—'},
 '5.11': {'setup': 'S3 · M',
          'picture': "Father takes the Client's card off the throne: **the card in one hand, the report in the "
                     'other.** Doubt. Behind, small on the counter: the needle in the orange',
          'reaction': '—',
          'line': '—',
          'sound': '—'},
 '6.1': {'setup': 'S1 · W',
         'picture': '**The robot sits in the throne**, formally. Its screen: **HUMAN APPROVAL REQUIRED** (the same '
                    'drawing as 3.3)',
         'reaction': '—',
         'line': '—',
         'sound': 'the same polite chime as 3.3'},
 '6.2': {'setup': 'S3 · MC',
         'picture': "**Father reaches his finger toward the screen to approve; it changes: APPROVER: CEO with Don's "
                    'face.** His finger stops, clearly apart',
         'reaction': '—',
         'line': '—',
         'sound': 'a soft refusal buzz'},
 '6.3': {'setup': 'S1 · W',
         'picture': "Father turns to Don. **Everyone turns to Don**: Sofía, Pam, the robot, the Client's eyes over "
                    "the counter's edge",
         'reaction': '—',
         'line': '— *(animatic test only: FATHER "Well, Donnie?")*',
         'sound': '—'},
 '6.4': {'setup': 'S4 · C',
         'picture': "**Push in on Don's eyes: for the first time he reads what he is approving**",
         'reaction': '—',
         'line': '—',
         'sound': 'room tone only'},
 '6.5': {'setup': 'S4 · MC',
         'picture': 'His fingertip rises toward the screen, **the same gesture as 3.4**, and hovers',
         'reaction': '—',
         'line': '—',
         'sound': '—'},
 '6.6': {'setup': 'S4 · MC',
         'picture': 'His eyes go to the robot in his throne. **The hand freezes**',
         'reaction': '—',
         'line': '—',
         'sound': '—'},
 '6.7': {'setup': 'S4 · M',
         'picture': '**The hand pulls back. Fists on his hips.** Two full seconds of silence',
         'reaction': '**2.0 s, never trimmed**',
         'line': '—',
         'sound': 'room tone'},
 '6.8': {'setup': 'S3 · M', 'picture': 'Sofía adjusts her new HR card', 'reaction': '—', 'line': '—', 'sound': '—'},
 '6.9': {'setup': 'S1 · W',
         'picture': 'The robot sits dead still a beat, then **rises slowly and stiffly out of the throne**, formal '
                    'to the last, and steps aside',
         'reaction': '—',
         'line': '—',
         'sound': 'a long servo whine'},
 '6.10': {'setup': 'S3 · MC',
          'picture': 'Father turns the tag: **REVIEW · TODAY → REVIEW · TOMORROW**. He folds his chair and leaves '
                     "with the report and the Client's card, the invoice in his pocket",
          'reaction': 'Don watches him go',
          'line': '—',
          'sound': 'tag flick; chair clack'},
 '7.1': {'setup': 'S4 · C',
         'picture': 'The room empties. Don unhooks the tag, **folds it the same way as frame 0, and wedges it under '
                    'the front caster**. He sits, leans back, his weight on the throne; **left hand on the armrest, '
                    'right hanging**; eyes close',
         'reaction': '—',
         'line': '—',
         'sound': "the machine's gurgle, far off"},
 '7.2': {'setup': 'S4 · C',
         'picture': "**The same close as 1.1 (K1)**: beside him the robot's screen glows **UPTIME 100%**; its "
                    'gripper reaches for the card → **frame 0**',
         'reaction': '—',
         'line': '—',
         'sound': 'a soft hum, through the seam'}}

# ---- 28 Nov amendments (moved here, edited here from now on) ----------------------------------------------------
# K1 v6 locked (Tomas 28 Nov): Don asleep ACROSS the throne (rv_poses.don_sprawl "B"), a medium on the whole throne.
# The blanket (Tomas /grill-me "Likutis kaip antklodė"): the robot's report is so long that Father leaves with the
# torn sheet and the report itself (6.10); the spilled tail stays on the floor, and Don folds it over himself (7.1).
# He sleeps under the audit, unread. Frame 0's paper is last loop's tail.
# The tag: the robot pulls it from the caster (1.1) and, tidy, hooks it back on the throne's back (1.4, behind).
TEXT["1.1"].update(setup="S4 · M", picture=(
    "**Frame 0 (K1 v6), night:** Don asleep ACROSS the throne, his back against its left armrest, chin down, legs over "
    "the right one; a folded paper (last night's report tail) over his belly like a blanket; the folded tag wedges the "
    "front-left caster. **0:00.4 the robot's gripper, from behind the throne, pulls the card; 0:00.6 the throne rolls "
    "back** and Don slides off its front, the paper with him"))
TEXT["1.2"]["picture"] = ("Don on his back on the floor, eyes still shut, the folded paper beside him; **he raises the "
                          "empty cup straight up**, like a baby bird")
TEXT["1.4"]["picture"] += (". Behind the throne the robot hooks the tag (REVIEW · TOMORROW) back on the throne's back "
                           "by its string, tidy")
TEXT["1.5"].update(setup="S3 · I", picture=(
    "**Insert (Tomas 28 Nov: the reaching arm failed two layout rounds):** the folding chair's short leg, a gap under it. "
    "The Client's hand comes in from the edge, a rolled white sleeve, a washer between its fingers, and **pushes it under "
    "the leg**; the leg settles; the hand withdraws"), reaction="—")
TEXT["3.7"]["picture"] += (". **Cut-in (Tomas 28 Nov, the hand review):** an insert of his hand alone, up from the "
                           "frame's edge, the watch on its strap, the mug standing on his level palm, a "
                           "waiter's catch, the coffee level, the steam drifting over it (3.7's last 0.6 s)")
TEXT["6.10"]["picture"] = ("Father turns the tag: **REVIEW · TODAY → REVIEW · TOMORROW**. He folds his chair and "
                           "leaves with the report and the Client's card, the invoice in his pocket. **The spilled "
                           "tail of the report stays on the floor**")
TEXT["7.1"].update(setup="S4 · M", picture=(
    "The room empties. Don unhooks the tag, **folds it the same way as frame 0, and wedges it under the front-left "
    "caster**. He picks up the spilled tail of the report, folds it once, lies down ACROSS the throne, legs over the "
    "right armrest, and **pulls the paper over his belly like a blanket**; chin down, eyes close"),
    sound="the machine's gurgle, far off (its needle is in the red now, out of frame)")
TEXT["7.2"].update(setup="S4 · M", picture=(
    "**The same frame as 1.1 (K1 v6)**: behind the throne the robot's screen glows **UPTIME 100%**; its gripper "
    "reaches for the card → **frame 0**"))

ORDER = list(TEXT)
SPEAKER = re.compile(r"\*\*([A-ZÁÉÍÓÚ][A-ZÁÉÍÓÚ ]+)\b[^*]*?:\s*\"")
LINE_SHOTS = {"3.3"}                       # the panel's voice: listed in 3.4's line cell, its take placed in 3.3
KNOWN = {}                                 # check -> [shots]: failures accepted, with the reason


# ---- staging -----------------------------------------------------------------------------------------------------
# don: "L" his side (A+B, screen left of the tape), "R" Father's side (C), "-" not in frame
# client: where the Client is, if in frame ("C" behind/at the counter, "knee" at Father's chair leg on the tape,
# "under" flat under the counter); "L" would put him on Don's floor line (never)
def st(cam, size, cast, don="-", client=None, peak=False, cross=None):
    return dict(cam=cam, size=size, cast=cast, don=don, client=client, peak=peak, cross=cross)


STAGE = {
    "1.1": st("S4", "M", ["don"], "L", peak=True),
    "1.2": st("S4", "C", ["don"], "L", peak=True),
    "1.3": st("S6", "M", ["pam"]),
    "1.4": st("S1", "W", ["father", "don", "robot"], "L"),
    "1.5": st("S3", "I", []),                                   # v2: an insert (the Client's hand at the leg)
    "1.6": st("S3", "M", ["father", "client"], client="C"),
    "1.7": st("S3", "I", []),
    "2.1": st("S1", "W", ["don", "sofia", "father"], "L", peak=True),
    "2.2": st("S3", "MC", ["sofia"]),
    "2.3": st("S2", "M", ["robot", "father"]),
    "2.4": st("S3", "I", []),
    "2.5": st("S3", "MC", ["sofia", "robot"], peak=True),
    "2.6": st("S3", "C", ["robot"]),
    "2.7": st("S1", "W", ["robot", "don"], "L"),
    "3.1": st("S1", "W", ["don", "father"], "R", cross="R"),
    "3.2": st("S6", "MC", ["don", "client", "pam"], "R", client="C"),
    "3.3": st("S6", "I", []),
    "3.4": st("S6", "MC", ["don"], "R", peak=True),
    "3.5": st("S6", "I", []),
    "3.6": st("S6", "MC", ["client", "don"], "R", client="C"),
    "3.7": st("S6", "M", ["client", "pam"], client="under", peak=True),
    "3.8": st("S6", "I", []),
    "3.9": st("S1", "W", ["don", "father"], "L", cross="L"),
    "3.10": st("S3", "C", ["father"]),
    "4.1": st("S1", "W", ["father", "don"], "L"),
    "4.2": st("S6", "MC", ["father", "client"], client="under", peak=True),
    "4.3": st("S4", "MC", ["don"], "L", peak=True),
    "4.4": st("S6", "M", ["pam"]),
    "4.5": st("S1", "W", ["don", "father", "robot"], "L"),
    "5.1": st("S2", "M", ["robot"]),
    "5.2": st("S1", "W", ["robot", "father", "don"], "L"),
    "5.3": st("S3", "MC", ["robot", "father"], peak=True),
    "5.4": st("S3", "I", []),
    "5.5": st("S3", "MC", ["father"]),
    "5.6": st("S3", "I", []),
    "5.7": st("S4", "C", ["don"], "L"),
    "5.8": st("S3", "I", []),
    "5.9": st("S3", "MC", ["father"], peak=True),
    "5.10": st("S4", "MC", ["don"], "L"),
    "5.11": st("S3", "M", ["father"]),
    "6.1": st("S1", "W", ["robot", "father", "don"], "L", peak=True),
    "6.2": st("S3", "MC", ["robot", "father", "don"], "L", peak=True),      # K2 v3
    "6.3": st("S1", "W", ["father", "sofia", "pam", "robot", "client", "don"], "L", client="C"),
    "6.4": st("S4", "C", ["don"], "L", peak=True),
    "6.5": st("S4", "MC", ["don"], "L"),
    "6.6": st("S4", "MC", ["don"], "L"),
    "6.7": st("S4", "M", ["don"], "L", peak=True),
    "6.8": st("S3", "M", ["sofia"]),
    "6.9": st("S1", "W", ["robot", "don"], "L"),
    "6.10": st("S3", "MC", ["father", "don"], "L"),
    "7.1": st("S4", "M", ["don"], "L"),
    "7.2": st("S4", "M", ["don"], "L", peak=True),
}

# ---- the props: the state each shot ENDS in is the start's state with this shot's changes applied ------------------
START = dict(tag="caster TOMORROW", badge="robot", paper="on Don", spill="none", card="Client's pocket",
             invoice="none", chair="none", mug="counter", needle="green", screen="UPTIME 100%", don_pose="asleep across",
             confetti="off")
CHANGES = {                                         # shot -> {prop: new state}; each must be shown by the shot's text
    "1.1": dict(tag="robot's gripper", paper="floor", don_pose="sliding"),
    "1.2": dict(don_pose="on his back, cup up"),
    "1.4": dict(tag="back TOMORROW", chair="open, wobbling"),
    "1.5": dict(chair="open, fixed"),
    "1.7": dict(tag="back TODAY"),
    "2.1": dict(don_pose="standing"),
    "2.4": dict(screen="POSITION VACANT"),
    "2.5": dict(badge="Sofía"),
    "2.6": dict(screen="NOTED."),
    "3.5": dict(needle="yellow"),
    "3.7": dict(mug="the Client's hand"),
    "4.1": dict(card="throne seat"),
    "5.2": dict(spill="floor"),
    "5.3": dict(invoice="Father's hand"),
    "5.5": dict(invoice="Father's pocket"),
    "5.6": dict(screen="UPTIME 100%"),
    "5.8": dict(screen="SALARY $0"),
    "5.11": dict(card="Father's hand", needle="orange"),
    "6.1": dict(screen="HUMAN APPROVAL REQUIRED"),
    "6.2": dict(screen="APPROVER: CEO"),
    "6.7": dict(don_pose="fists on hips"),
    "6.10": dict(tag="back TOMORROW", chair="gone", card="gone", invoice="gone"),
    "7.1": dict(tag="caster TOMORROW", paper="on Don", spill="none", don_pose="asleep across", needle="red"),
    "7.2": dict(screen="UPTIME 100%"),
}
SHOWS = {                    # a word in the shot's text that shows each change (the props check reads it)
    "tag": r"tag|card", "chair": r"chair", "paper": r"paper|slides off", "spill": r"unfurl|spill|tail",
    "badge": r"HR card", "screen": r"screen|UPTIME|APPROVAL|APPROVER|POSITION|NOTED|SALARY", "needle": r"needle",
    "mug": r"mug", "card": r"card", "invoice": r"sheet|pocket|invoice", "don_pose": r"Don|He |his |fists|asleep|lies",
    "confetti": r"confetti",
}
# what K1 shows at both ends (the loop check); what it hides, and why
K1_SHOWS = ("tag", "paper", "spill", "don_pose", "screen", "confetti")
K1_HIDES = {"badge": "the robot's chest is behind the throne in K1 (v3 failed on it)",
            "needle": "the machine is out of K1's frame; it goes on climbing between loops (G0)",
            "mug": "out of frame", "card": "gone with Father", "invoice": "gone with Father",
            "chair": "gone with Father"}


def states():
    """the state of every prop at the END of every shot."""
    cur, out = dict(START), {}
    for sid in ORDER:
        cur = dict(cur, **CHANGES.get(sid, {}))
        out[sid] = dict(cur)
    return out


def timing():
    return json.load(open(TIMING))


def _text(sid):
    t = TEXT[sid]
    return " ".join((t["picture"], t["reaction"], t["line"], t["sound"]))


def check_lines(tm):
    meta = json.load(open(TAKES))
    ev = sorted((s["start"] + o, k, s) for s in tm["shots"] for k, o in zip(s["takes"], s["take_at"]))
    bad, prev = [], (0.0, None)
    for t, k, s in ev:
        if t < prev[0] - 1e-6:
            bad.append("%s starts at %.2f s, before %s ends (%.2f s)" % (k, t, prev[1], prev[0]))
        end = t + meta[k]["len"]
        if end > s["start"] + s["len"] + 1e-6:
            bad.append("%s runs past its shot (%.2f > %.2f)" % (k, end, s["start"] + s["len"]))
        prev = (end, k)
    for s in tm["shots"]:
        sid = s["shot"]
        if s["takes"] and sid not in LINE_SHOTS and not SPEAKER.search(TEXT[sid]["line"]):
            bad.append("%s: a take with no named speaker in the line cell (lesson 169)" % sid)
        if not s["takes"] and TEXT[sid]["line"] not in ("—", "") and "animatic test only" not in TEXT[sid]["line"]:
            bad.append("%s: a line with no take" % sid)
    if [s["shot"] for s in tm["shots"]] != ORDER:
        bad.append("the timing's shots are not the scene file's (re-run rv_voices.py timing)")
    return bad


def check_loop():
    end, bad = states()[ORDER[-1]], []
    for p in K1_SHOWS:
        if end[p] != START[p]:
            bad.append("%s: frame 0 has %r, the last frame %r" % (p, START[p], end[p]))
    for p in START:
        if p not in K1_SHOWS and p not in K1_HIDES:
            bad.append("%s: neither shown nor hidden by K1 (say which)" % p)
    for sid in (ORDER[0], ORDER[-1]):
        if STAGE[sid]["cam"] != STAGE[ORDER[0]]["cam"] or STAGE[sid]["size"] != STAGE[ORDER[0]]["size"]:
            bad.append("%s: not K1's setup" % sid)
    return bad


def check_tape():
    bad, side = [], "L"
    for sid in ORDER:
        s_ = STAGE[sid]
        if s_["cross"]:
            if s_["cross"] == side:
                bad.append("%s: a crossing to the side he is already on" % sid)
            if not re.search(r"over (his|the|its) (own )?tape|over his tape|over the line", TEXT[sid]["picture"]):
                bad.append("%s: Don crosses, but the picture doesn't show it" % sid)
            side = s_["cross"]
        if s_["don"] != "-" and s_["don"] != side:
            bad.append("%s: Don on side %s, but he last crossed to %s" % (sid, s_["don"], side))
        if ("don" in s_["cast"]) != (s_["don"] != "-"):
            bad.append("%s: Don in the cast but no side (or the reverse)" % sid)
        if s_["client"] == "L" or ("client" in s_["cast"]) != bool(s_["client"]):
            bad.append("%s: the Client's place (%s) is wrong or missing" % (sid, s_["client"]))
    return bad


def check_props():
    bad = []
    for sid, ch in CHANGES.items():
        if sid not in TEXT:
            bad.append("%s: a change in a shot that doesn't exist" % sid); continue
        for p, v in ch.items():
            if p not in START:
                bad.append("%s: %s is not a declared prop" % (sid, p))
            elif not re.search(SHOWS[p], _text(sid)):
                bad.append("%s: %s becomes %r, but the shot's text doesn't show it" % (sid, p, v))
        if "needle" in ch and (TEXT[sid]["line"] not in ("—", "") or STAGE[sid]["peak"]) and sid != "3.5":
            bad.append("%s: the needle moves on a line or a peak" % sid)
    if set(STAGE) != set(TEXT):
        bad.append("staging and text differ: %s" % sorted(set(STAGE) ^ set(TEXT)))
    return bad


def selftest():
    """each check must fail on a planted fault (CLAUDE.md: validate on a known failure first)."""
    import copy
    keep = (copy.deepcopy(STAGE), copy.deepcopy(CHANGES), copy.deepcopy(TEXT))
    tm = timing()
    tm_bad = copy.deepcopy(tm)
    s4 = [s for s in tm_bad["shots"] if s["shot"] == "4.2"][0]; s4["take_at"] = [s4["len"] - 0.2]
    plants = [
        ("lines_long", lambda: None, lambda: check_lines(tm_bad)),
        ("lines_name", lambda: TEXT["5.9"].update(line='"There it is."'), lambda: check_lines(tm)),
        ("loop_tag", lambda: CHANGES["7.1"].update(tag="back TOMORROW"), check_loop),
        ("loop_blanket", lambda: CHANGES["7.1"].pop("paper"), check_loop),
        ("tape_side", lambda: STAGE["3.4"].update(don="L"), check_tape),
        ("tape_cross", lambda: TEXT["3.1"].update(picture="Don walks to the counter"), check_tape),
        ("client_line", lambda: STAGE["1.6"].update(client="L"), check_tape),
        ("props_shown", lambda: CHANGES.setdefault("4.4", {}).__setitem__("card", "Pam"), check_props),
        ("needle_line", lambda: CHANGES.setdefault("4.2", {}).__setitem__("needle", "orange"), check_props),
    ]
    ok = True
    for name, plant, chk in plants:
        plant()
        caught = bool(chk())
        STAGE.clear(); STAGE.update(copy.deepcopy(keep[0]))
        CHANGES.clear(); CHANGES.update(copy.deepcopy(keep[1]))
        TEXT.clear(); TEXT.update(copy.deepcopy(keep[2]))
        print("selftest %-13s %s" % (name, "caught" if caught else "MISSED"))
        ok = ok and caught
    return ok


def script_v5(tm, out):
    """script v4's prose, its act tables regenerated from TEXT and the timing, then the staging and the props."""
    times = {s["shot"]: s for s in tm["shots"]}
    lines = open(TEMPLATE).read().split("\n")
    out_l = []
    for ln in lines[1:]:
        m = re.match(r"\| (\d\.\d+) \| (\d:\d\d\.\d) \| ([\d.]+) \|", ln)
        if m and m.group(1) in TEXT:
            sid = m.group(1); t = TEXT[sid]; s = times[sid]; mm, ss = divmod(s["start"], 60)
            out_l.append("| %s | %d:%04.1f | %.2f | %s | %s | %s | %s | %s |" % (sid, mm, ss, s["len"], t["setup"],
                         t["picture"], t["reaction"], t["line"], t["sound"]))
        else:
            out_l.append(ln)
    head = ("# Approved.: script v5 (GENERATED by `src/rv_scenes.py` from the scene file; do not edit by hand)\n\n"
            "Times and lengths from the picked takes (`rv_timing_v1.json`, total %.1f s). Amended in the scene file "
            "(28 Nov): 1.1, 1.2, 1.4, 6.10, 7.1, 7.2 (K1 v6 locked: Don asleep across the throne; the report's tail as "
            "his blanket). The prose below the tables is script v4's, kept as written.\n" % tm["total"])
    sts = states()
    props = list(START)
    rows = ["", "## The staging and the props (generated)", "",
            "| Shot | Setup · size | In frame | Don | Client | " + " | ".join(props) + " |",
            "|---" * (5 + len(props)) + "|",
            "| start | | | | | " + " | ".join(START[p] for p in props) + " |"]
    for sid in ORDER:
        s_ = STAGE[sid]; ch = CHANGES.get(sid, {})
        cells = ["**%s**" % sts[sid][p] if p in ch else "·" for p in props]
        rows.append("| %s | %s · %s | %s | %s | %s | %s |" % (sid, s_["cam"], s_["size"], ", ".join(s_["cast"]) or "—",
                    s_["don"], s_["client"] or "—", " | ".join(cells)))
    rows += ["", "Bold: the shot where the state changes; · as before. K1 hides: " +
             "; ".join("%s (%s)" % kv for kv in K1_HIDES.items()) + "."]
    open(out, "w").write(head + "\n".join(out_l).rstrip("\n") + "\n" + "\n".join(rows) + "\n")


def main(out_dir=EP):
    if not selftest():
        print("a check misses its planted fault: not trusted"); return False
    tm = timing()
    results = dict(lines=check_lines(tm), loop=check_loop(), tape=check_tape(), props=check_props())
    fail = False
    for name, bad in results.items():
        new = [b for b in bad if b.split(":")[0].split(" ")[0] not in KNOWN.get(name, [])]
        print("%-6s %s" % (name, "PASS" if not new else "FAIL"))
        for b in bad:
            print("    " + b)
        fail = fail or bool(new)
    out = os.path.join(out_dir, "the-review-script-v5.md")
    script_v5(tm, out)
    print("wrote", out)
    return not fail


if __name__ == "__main__":
    sys.exit(0 if main(*sys.argv[1:]) else 1)
