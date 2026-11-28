"""THE DOUBLE AGENT (episode 15): the scene file, v1 (stage 4, series/production-process.md rule 1: one source).

From here on this file is the episode's shot list: every shot's text (picture, reaction, line, sound: from script v4
with the 27 Nov amendments, moved here once and edited here from now on), its staging (the space, the setup and size,
who is in frame, what of the other space shows, the robot's pile and state, the motive of every floor <-> office cut),
and its timing (da_timing_v3.json, from the recorded takes). Generated from it:

  python3 da_scenes.py [out_dir]  ->  the-double-agent-script-v5.md   (generated; do not edit by hand)
                                      the checks below, printed; exit 1 on a failure not listed in KNOWN

The checks (data, before any layout is drawn):
  two_spaces   every floor <-> office cut has the other space on one side of it, as a still state or by sound
               (lessons 249-253; script v4 "The two spaces at every cut"); a background is a state, not an action (22)
  lines        no two lines overlap; a run-on line fits its next shot (42); every line's speaker is named (169)
  robot        its pile never grows after 1.4; it is frozen on every line shot and every named peak it is in
  pairs        every inside line has a partner outside (253)
  direction    Don's side: screen left on the floor setups seen from the street side (S1, S3, S4, S5, S6, S7),
               screen right from the office side (S8, S8r, S9): the mirror rule (da_s8)
Layouts (stage 4.3) are drawn from the same records: da_layouts.py (next).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..", "the-double-agent")
TEMPLATE = os.path.join(EP, "the-double-agent-script-v4.md")         # the prose around the tables (frozen at v4)
TIMING = os.path.join(EP, "da_timing_v4.json")   # 27 Nov: v4 with the seven micro-shots (v3 kept)

TEXT = {'1.1': {'script': 1.4,
         'setup': 'S8r · M',
         'picture': "**Frame 0** (the push's last framing): Don and the robot pull the gold throne across the tape "
                    "line, Don leaning back toward his side, the robot toward Father's. **0:00.4 Don's back foot "
                    "lands on the roll's sticky tail; the roll comes up with his foot**",
         'reaction': 'Don looks down at it',
         'line': '—',
         'sound': 'throne casters squeak; tacky *thk*'},
 '1.2': {'script': 0.8,
         'setup': 'S3 · M',
         'picture': 'He shakes his foot once; the roll swings round and **whacks his other shin**; he lets go with '
                    'one hand',
         'reaction': "the robot gains a hand's width",
         'line': '(Don, effort: "Oof")',
         'sound': 'thwack'},
 '1.3': {'script': 1.0,
         'setup': 'S1 · W',
         'picture': "**Polished shoes and a burgundy hem step over the tape** between them, toward the office; **the "
                    "robot lets go at once** (it obeys the owner); Don is left on one leg, holding his shin",
         'reaction': 'Don frozen, watching the shoes go to his office door; 0.5 s',
         'line': '—',
         'sound': 'slow heels'},
 '1.3b': {'script': 1.0,
          'setup': 'S3 · MC',
          'picture': "**The tag (Tomas 27 Nov: its own MC; the words can't be read in the wide):** the ringed hand, "
                     "in passing, hangs **REVIEW · TOMORROW** on the throne's **back** (to this camera; the "
                     "price tag is on its front); the burgundy sleeve goes on out of frame",
          'reaction': 'the tag swings, settles',
          'line': '—',
          'sound': 'tag flick'},
 '1.4': {'script': 1.2,
         'setup': 'S1 · W',
         'picture': '**Sofía follows Father over the line** with a folder and a box of paperclips; the box catches '
                    "on the throne's armrest and **the clips spill across the floor**, round the throne's casters. "
                    "She doesn't stop; she goes in after Father. **The robot kneels and starts picking them up**",
         'reaction': 'Don looks at the clips, then at the robot',
         'line': '—',
         'sound': 'a bright clatter; one pincer *tik*'},
 '1.5': {'script': 0.8,
         'setup': 'S3 · M',
         'picture': 'He pulls the roll off his sole and drops it by the throne',
         'reaction': '—',
         'line': '—',
         'sound': 'rip; thud'},
 '2.1': {'script': 2.2,
         'setup': 'S7 · W',
         'picture': "Don walks to his line, toes at the edge. **Inside the glass:** Father sits down in Don's chair; "
                    'the Client already there, Sofía just putting her folder down. Low on the floor: the robot '
                    'picking clips',
         'reaction': 'Don stares',
         'line': '—',
         'sound': "the chair's creak, muffled; *tik*"},
 '2.2': {'script': 2.6,
         'setup': 'S8 · M',
         'picture': "Father's foot up on Don's desk; Don's gold desk photo (DON · CEO) is where the second foot "
                    'goes: **his heel nudges it face down, then rests on it** like a footstool. The Client glances '
                    'at the photo. Behind the glass, small: Don at his line, the robot crouched beside the throne',
         'reaction': "Father doesn't look at it",
         'line': '**FATHER (calm): "I paid for it."**',
         'sound': 'clack'},
 '2.3': {'script': 1.2,
         'setup': 'S3 · MC',
         'picture': '**Don straightens his vest**, offended, chin up (a readable human face: cold test F1)',
         'reaction': '—',
         'line': '—',
         'sound': 'vest snap'},
 '2.4': {'script': 2.8,
         'setup': 'S3 · M two-shot',
         'picture': '**The gift:** Don, dignity restored, turns to Pam at the counter end and presents **a mustard '
                    "mug with a gold bow** (his side's loyalty gift). Pam, flustered, **lets go of her old blue mug: "
                    'it shatters** at her feet; she takes the new one in both hands and holds it to her chest',
         'reaction': 'Don already turning away, satisfied; Pam looking at the mug, then at him',
         'line': '—',
         'sound': 'the shatter; a tiny intake of breath'},
 '3.1': {'script': 1.2,
         'setup': 'S3 · MC',
         'picture': 'Don, without turning, holds his empty cup up over his shoulder, upside down (27 Nov: the snap read as a wave, 3 tests)',
         'reaction': '—',
         'line': '**DON: "Pam! Coffee."**',
         'sound': '—'},
 '3.2': {'script': 1.2,
         'setup': 'S6 · M',
         'picture': "Pam at the counter's end pours from her thermos: **her mustard mug** and Don's cup and saucer",
         'reaction': 'inside: Father and the Client waiting',
         'line': '—',
         'sound': 'pour'},
 '3.3': {'script': 2.4,
         'setup': 'S7 · W',
         'picture': "Pam carries both past Mom's desk toward Don; the office door opens a hand's width; **the "
                    "Client's hand takes her mustard mug** and turns back inside with it. **Pam follows her mug "
                    "on reflex**, Don's cup still in her other hand (nobody pulls her: the first crossing is an "
                    'accident). **Mom stands up**, her knitting still in one hand',
         'reaction': '—',
         'line': '**CLIENT (from the door): "Pam. We need you."**',
         'sound': 'door; chair scrape'},
 '3.4': {'script': 3.6,
         'setup': 'S7 · M',
         'picture': '**The shoulder-pad wall:** Don leans left, the pads go left; right, right; **then he feints** '
                    "and stays put. **Mom doesn't move.** She never looks at him: **one hand keeps knitting** the "
                    'whole time, the body blocks on its own (low behind her, the robot frozen, pincer up). **Through '
                    "the glass behind them, small and still: her mug already on Father's table, Pam's hand on it** "
                    '(the two spaces, 27 Nov; a state, not an action: lesson 22)',
         'reaction': "hold on Mom 0.5 s after the feint; then the line; Don's face",
         'line': '**MOM: "Your rule, sweetheart."** (after the hold, never on the feint)',
         'sound': 'two swishes; silence on the feint; needles click'},
 '3.5': {'script': 1.6,
         'setup': 'S8 · MC',
         'picture': "Pam sets **her mug** down in front of Father, her hand still on it; he looks at it "
                    "(27 Nov: the napkin's wipe read as a note, 5 of 5 cold viewers; Tomas: another shot)",
         'reaction': '—',
         'line': '—',
         'sound': 'wipe squeak'},
 '4.1': {'script': 1.6,
         'setup': 'S6 · M',
         'picture': 'Pam comes out, **crosses the tape** to Don, hands him the cup and saucer. Mom sits. **Through '
                    'the glass, small and still: the Client and Father seated, her mustard mug between them** (the '
                    'two spaces, 27 Nov; a state: lesson 22)',
         'reaction': '—',
         'line': '—',
         'sound': 'cup on saucer'},
 '4.2': {'script': 3.0,
         'setup': 'S1 · M',
         'picture': "**Don turns his back on his office** to preen in the street door's glass, alone: he sees "
                    "nothing (27 Nov, simplified: Pam's slip is 4.3's, her hand on the office door)",
         'reaction': '—',
         'line': '—',
         'sound': 'her quiet steps'},
 '4.3': {'script': 1.2,
         'setup': 'S5 · M',
         'picture': "Pam passes Mom's desk; Mom knits on, doesn't look up; Pam slips in",
         'reaction': '—',
         'line': '—',
         'sound': '—'},
 '5.1': {'script': 1.4,
         'setup': 'S9 · C',
         'picture': "Don's view: **her mug on Father's table**",
         'reaction': '—',
         'line': '—',
         'sound': 'music stops'},
 '5.2': {'script': 2.8,
         'setup': 'S3 · MC',
         'picture': '**The coffee betrayal:** his cup rattles on the saucer, coffee slops into it; he sips from the '
                    'cup, the saucer held out in his other hand, eyes never leaving the office; **he notices how it '
                    'looks, lifts his little finger** and goes on as if he meant to (Tomas 27 Nov: the saucer sip '
                    'read 0/2 in silhouette)',
         'reaction': 'held, dead serious',
         'line': '—',
         'sound': 'rattle; slurp'},
 '5.3': {'script': 2.0,
         'setup': 'S1 · M',
         'picture': 'He charges, **slips on the robot\'s clips** (they fly), slides and **stops dead at his own line**: '
                    'two moments (27 Nov, Tomas: the slip read by 3 of 3; keep it, then the line)',
         'reaction': '—',
         'line': '—',
         'sound': 'skid; cup clink'},
 '5.4': {'script': 2.2,
         'setup': 'S7 · M',
         'picture': "**Mom's step:** round the counter's left end, she plants herself on Father's side between him "
                    'and the glass, arms folded, looking at him; the robot, between them and the throne, freezes '
                    'with a clip',
         'reaction': 'he looks from her to the glass and back',
         'line': '—',
         'sound': 'her heels, two steps'},
 '6.1': {'script': 1.4,
         'setup': 'S6 · M',
         'picture': "Pam comes out of the door behind Mom with the robot's printed minutes, crosses to Don",
         'reaction': '—',
         'line': '—',
         'sound': 'door'},
 '6.2': {'script': 1.2,
         'setup': 'S3 · M two-shot',
         'picture': 'Don narrows his eyes at her; she holds out the page',
         'reaction': '—',
         'line': '**PAM (quiet, a fact, holding out the page): "I took notes."** (Tomas 27 Nov: her one line '
                 'outside; true, she did; it makes him read "spying for me" and sets up 8.1\'s "Others take notes.") '
                 '**Runs on into 6.3** (the page): 6.2 stays 1.2 s (lesson 42, Tomas 27 Nov)',
         'sound': '—'},
 '6.3': {'script': 1.0,
         'setup': 'I',
         'picture': "**AGENDA: WITHOUT HIM** (the robot's printout)",
         'reaction': '—',
         'line': '—',
         'sound': 'paper'},
 '6.4': {'script': 1.8,
         'setup': 'S3 · MC',
         'picture': 'Suspicion → **delight**',
         'reaction': '—',
         'line': '**DON: "You\'re spying for me?"**',
         'sound': '—'},
 '6.5': {'script': 1.0,
         'setup': 'C',
         'picture': 'Pam opens her mouth to correct him',
         'reaction': '—',
         'line': '—',
         'sound': '—'},
 '6.6': {'script': 1.0,
         'setup': 'S9 · C',
         'picture': 'Her view: **the Client waiting, his blue blueprint rolled in his hands**, looking at her',
         'reaction': '—',
         'line': '—',
         'sound': 'music stops'},
 '6.7': {'script': 0.8,
         'setup': 'C',
         'picture': '**Pam closes her mouth**',
         'reaction': 'held 0.6 s',
         'line': '—',
         'sound': '—'},
 '6.8': {'script': 2.4,
         'setup': 'S3 · MC',
         'picture': '**Don looks left, looks right** (Pam half a metre away), **pulls his headset mic to his mouth** '
                    'and whispers into it; **Pam leans in** to hear him',
         'reaction': '—',
         'line': '**DON: "Keep infiltrating."**',
         'sound': 'mic tap'},
 '7.1': {'script': 1.2,
         'setup': 'S4 · C',
         'picture': 'He crouches and **peels a long strip of his tape up**',
         'reaction': '—',
         'line': '—',
         'sound': 'a long peel'},
 '7.2': {'script': 2.8,
         'setup': 'S7 · W',
         'picture': '**The barrier:** the strip held high, chin up; **Pam ducks under it** and walks past Mom to the '
                    'door; the robot, frozen, has one clip left: under the throne. **Through the glass, small and '
                    'still: the Client seated, the rolled blueprint in his hands** (the two spaces, 27 Nov; a state: '
                    'lesson 22)',
         'reaction': '—',
         'line': '**DON (grandly, as she passes under): "Approved."**',
         'sound': '—'},
 '7.3': {'script': 3.4,
         'setup': 'S8 · MC two-shot',
         'picture': '**The Client slides his blueprint (MY GARAGES) across the desk to Pam; she takes it with both '
                    'hands; Father nods once** (the hand-over: cold test S8 v3 left it to this shot)',
         'reaction': "Pam looks down at it; then the casters start outside (7.4's sound, a J-cut): **Father doesn't "
                     'turn round**',
         'line': '**CLIENT: "Don\'t lose it."** · then **FATHER (calm, not turning): "Let him play."** (Tomas 27 '
                 'Nov: the order is the Client → the casters start outside, low, about −12 dB under speech → Father '
                 'answers the sound without turning: inside answers outside)',
         'sound': "paper slide; casters under, from outside; **the casters ducked under Father's line** (held "
                  'envelope, lesson 83; the speech check rerun after the mix)'},
 '7.4': {'script': 3.0,
         'setup': 'S1 · W',
         'picture': "Don, proud, lowers the strip and turns. **The last paperclip lies under the throne's caster:** "
                    "the robot rolls the throne off it, **through the gap in his line toward Father's side**, and "
                    'reaches for the clip. Don sees only his throne going: he dives, grabs an armrest and **hauls it '
                    'back onto the clip**, his back foot ending just in front of the dropped roll. The robot pulls '
                    'it off again to reach it: **the tug begins, each for something else** (Don the chair, the robot '
                    'the clip). **Through the office glass behind them, small and still: Pam holding MY GARAGES, '
                    "Father's back to the glass** (the two spaces, 27 Nov; a state: lesson 22)",
         'reaction': "the robot's pincer hovering over the clip, then the caster back on it",
         'line': '**DON (on the dive, bubble after the first grab): "NOT THE CHAIR!"**',
         'sound': "*tik*; casters; Don's grunt"},
 '8.1': {'script': 4.0,
         'setup': 'S8r → S8 · pull 1.5 s, then S8 · W held 2.5 s',
         'picture': "**The pull-back (Tomas 27 Nov, /grill-me):** 7.4 cuts to S8r (frame 0's framing), the camera "
                    "pulls back through the glass into the office (9.1's three-plane dolly played backwards, "
                    '`da_push91.py pull`), revealing the deal, and holds. **The final image (now '
                    "`da_s8_final_v9.png`: v8 with S8r itself in the glass, A1):** inside, the Client's finger on MY "
                    "GARAGES, Pam's hands on it, Father in Don's chair, Sofía reading; behind the glass Don and the "
                    'robot pulling the throne across the line. Nobody inside looks up',
         'reaction': 'long hold',
         'line': '**PAM (under her breath): "Some take sides. Others take notes."** (kept as written, Tomas 26 Nov) '
                 '**from 1.4 s, as the pull ends** (Tomas 27 Nov: never over the outside picture)',
         'sound': 'pen; muffled squeaks of the tug'},
 '9.1': {'script': 1.8,
         'setup': 'S8 → S8r · push',
         'picture': "**The push:** the camera moves through the glass (the blinds' rail passes the top, the glass's "
                    'sheen slides off) into the tug on the floor; **the new S8r background** (the floor from the '
                    "office side) takes over from the far room as the glass passes, ending on **1.1's framing: frame "
                    '0**',
         'reaction': '—',
         'line': '—',
         'sound': "the tug's squeak grows; the room tone carries through the seam"}}


# --- the staging, per shot ---------------------------------------------------------------------------------------------
# space: floor | office | glass (a view of the office from the floor: 5.1, 6.6) | insert | move (8.1, 9.1)
# cast: who is in frame (story faces); other: what of the other space this shot carries ("inside: ..." / "outside: ...",
# as a still state; "sound: ..." for a close shot); robot: (pile, "working" | "frozen") if it is in frame;
# motive: for a shot that follows a change of place, what carries the cut (script v4, plan v2's cut table).
FLOOR_FRONT = ("S1", "S3", "S4", "S5", "S6", "S7")             # seen from the street side: Don's side screen left
OFFICE_SIDE = ("S8", "S8r", "S9")                             # seen from the office side: Don's side screen right


def st(space, cam, size, cast, other=None, robot=None, motive=None, peak=False, don_side=None):
    return dict(space=space, cam=cam, size=size, cast=cast, other=other, robot=robot, motive=motive, peak=peak,
                don_side=don_side)


STAGE = {
    "1.1": st("floor", "S8r", "M", ["don", "robot"], robot=(0, "working"), don_side="R"),
    "1.2": st("floor", "S3", "M", ["don"], peak=True, don_side="L"),
    "1.3": st("floor", "S1", "W", ["don", "robot"], robot=(0, "frozen"), don_side="L"),   # Father: the near layer (no face)
    "1.3b": st("floor", "S3", "MC", [], don_side="L"),
    "1.4": st("floor", "S1", "W", ["don", "robot", "sofia"], robot=(30, "working"), don_side="L"),
    "1.5": st("floor", "S3", "M", ["don"], don_side="L"),
    "2.1": st("floor", "S7", "W", ["don", "robot"], other="inside: Father sitting down in Don's chair; the Client; "
              "Sofía putting her folder down", robot=(28, "working"), don_side="L"),
    "2.2": st("office", "S8", "M", ["father", "client"], other="outside: Don at his line, the robot crouched",
              robot=(27, "frozen"), motive="Don's stare at the glass (2.1)", don_side="R"),
    "2.3": st("floor", "S3", "MC", ["don"], other="sound: the photo's clack and \"I paid for it.\" run over the cut",
              motive="action -> reaction (the heel on the photo -> Don offended)", don_side="L"),
    "2.4": st("floor", "S3", "M", ["don", "pam"], peak=True, don_side="L"),
    "3.1": st("floor", "S3", "MC", ["don"], don_side="L"),
    "3.2": st("floor", "S6", "M", ["pam"], other="inside: Father and the Client waiting", don_side="L"),
    "3.3": st("floor", "S7", "W", ["pam", "mom", "client"], robot=(22, "frozen"), don_side="L"),
    "3.4": st("floor", "S7", "M", ["don", "mom"], other="inside: her mug already on Father's table, Pam's hand on it",
              robot=(20, "frozen"), peak=True, don_side="L"),
    "3.5": st("office", "S8", "MC", ["pam"], other=None,                        # close on the mug: no glass (layout v2)
              motive="the mug: Pam followed it through the door (3.3)", don_side="R"),
    "4.1": st("floor", "S6", "M", ["pam", "don", "mom"], other="inside: the Client and Father seated, her mug "
              "between them", motive="the door: Pam comes out, mid-step", don_side="L"),
    "4.2": st("floor", "S1", "M", ["don"], robot=(16, "working"), don_side="L"),     # 27 Nov: simplified, Don alone
    "4.3": st("floor", "S5", "M", ["pam", "mom"], don_side="L"),
    "5.1": st("glass", "S9", "C", [], other="inside: her mug on Father's table (Don's view)", don_side="R"),
    "5.2": st("floor", "S3", "MC", ["don"], peak=True, don_side="L"),
    "5.3": st("floor", "S1", "M", ["don"], robot=(12, "frozen"), peak=True, don_side="L"),   # 27 Nov: the robot out
    "5.4": st("floor", "S7", "M", ["mom", "don", "robot"], robot=(11, "frozen"), peak=True, don_side="L"),
    "6.1": st("floor", "S6", "M", ["pam", "mom"], don_side="L"),
    "6.2": st("floor", "S3", "M", ["don", "pam"], don_side="L"),
    "6.3": st("insert", "I", "I", []),
    "6.4": st("floor", "S3", "MC", ["don"], don_side="L"),
    "6.5": st("floor", "S3", "C", ["pam"], don_side="L"),
    "6.6": st("glass", "S9", "C", ["client"], other="inside: the Client waiting, the blueprint rolled (her view)",
              don_side="R"),
    "6.7": st("floor", "S3", "C", ["pam"], peak=True, don_side="L"),
    "6.8": st("floor", "S3", "MC", ["don", "pam"], don_side="L"),
    "7.1": st("floor", "S4", "C", ["don"], don_side="L"),
    "7.2": st("floor", "S7", "W", ["don", "pam", "mom", "robot"], other="inside: the Client seated, the rolled "
              "blueprint in his hands", robot=(1, "frozen"), peak=True, don_side="L"),
    "7.3": st("office", "S8", "MC", ["client", "pam", "father"], other="sound: the casters start outside (J-cut), "
              "ducked under Father's line", motive="the action: Pam ducks under the strip to the door (7.2)",
              don_side="R"),
    "7.4": st("floor", "S1", "W", ["don", "robot"], other="inside: Pam holding MY GARAGES, Father's back to the "
              "glass", robot=(1, "working"), motive="the casters' sound (7.3)", peak=True, don_side="L"),
    "8.1": st("move", "S8r>S8", "W", ["don", "robot", "father", "client", "pam", "sofia"], other="both: the deal "
              "inside, the tug outside", motive="the pull-back through the glass", don_side="R"),
    "9.1": st("move", "S8>S8r", "M", ["don", "robot"], other="both", motive="the push through the glass", don_side="R"),
}
FOCUS = {"1.1": "the absurdly expensive throne", "1.2": "Don's fail with the roll", "1.3": "Father's shoes over the line",
         "1.3b": "REVIEW · TOMORROW", "1.4": "the clips falling", "1.5": "Don's annoyance", "2.1": "Don alone at his line",
         "2.2": "Father's feet on Don's desk", "2.3": "Don's hurt pride", "2.4": "the gift: a bribe for loyalty"}
FOCUS.update({"3.1": "his empty cup held up, not turning", "3.2": "the pour into HER mug first", "3.3": "the mug taken at the door",
              "3.4": "Mom's wall", "3.5": "her mug set before Father", "4.1": "the cup handed across the tape",
              "4.2": "Don preening, alone", "4.3": "Mom not looking up", "5.1": "her mug on Father's table",
              "5.2": "the pinky out", "5.3": "the slip on the clips, then his line", "5.4": "Mom planted, the robot frozen"})
FOCUS.update({"6.1": "Pam out of the door, the page in hand", "6.2": "the page held out across the tape",
              "6.3": "AGENDA: WITHOUT HIM", "6.4": "his thumbs up, delighted", "6.5": "her mouth opening",
              "6.6": "the Client waiting, the roll in his hands", "6.7": "her mouth closed", "6.8": "the mic at his mouth",
              "7.1": "the strip peeling up", "7.2": "the strip raised like a gate, Pam under it",
              "7.3": "MY GARAGES handed to Pam", "7.4": "he holds on to his chair, HR comes for it",
              "8.1": "the deal held inside, the tug in the glass", "9.1": "through the glass into the tug"})

for _k, _v in FOCUS.items():                                  # the audit (27 Nov): one centre of attention per shot
    STAGE[_k]["focus"] = _v

# ---- 27 Nov: the comedy micro-shots (the pre-animatic audit; Tomas /grill-me: all seven, the length may grow to ~76 s,
# the clips stay A). Inserted after their anchors; each a reaction or a prop, none a new place or person.
def _after(d, anchor, sid, rec):
    out = {}
    for k_, v_ in d.items():
        out[k_] = v_
        if k_ == anchor:
            out[sid] = rec
    return out


_MICRO = [
    ("1.3", "1.3c", dict(script=0.6, setup="S3 · C", picture="**Don's eyes follow the polished shoe over his line**, "
                         "one eyebrow twitching: his rule just ended, before he can protest", reaction="—", line="—",
                         sound="a short border beep"),
     st("floor", "S3", "C", ["don"], don_side="L")),
    # 2.3b (the frozen smile) cut 27 Nov: the whole-board test found frames 10-13 "too much happy mugging" (2 of 3);
    # it only repeated 2.3 (Tomas /grill-me)
    ("3.2", "3.2b", dict(script=0.7, setup="I", picture="**The two cups side by side**: her big steaming mustard mug, "
                         "his tiny white cup on its saucer (remember the yellow one)", reaction="—", line="—",
                         sound="the pour"),
     st("insert", "I", "C", [])),
    # 3.4b (Mom the goalkeeper) cut 27 Nov: her block failed 4 layout rounds and 2 motion tests (his raised knee read as
    # a kick); 3.4's tiptoe pose read in Act II round 6 and carries it (Tomas: "B good")
    ("4.2", "4.2b", dict(script=0.8, setup="S1 · C", picture="**In the door's glass Don rehearses Father's face**: chin "
                         "up, lips flat, the hard stare", reaction="—", line="—", sound="—"),
     st("floor", "S1", "C", ["don"], don_side="L")),
    ("5.3", "5.3b", dict(script=0.6, setup="I", picture="**His cup flies**: the coffee arcs out and lands in a splash "
                         "right at the tape, not over it", reaction="—", line="—", sound="skrrt, splash"),
     st("insert", "I", "C", [])),
    ("6.8", "6.8b", dict(script=0.6, setup="S3 · C", picture="**Pam looks at his headset mic, then at him** (half a "
                         "metre away)", reaction="—", line="—", sound="—"),
     st("floor", "S3", "C", ["pam"])),
]
for _a, _sid, _rec, _st in _MICRO:
    TEXT = _after(TEXT, _a, _sid, _rec)
    STAGE[_sid] = _st
FOCUS.update({"1.3c": "his eyes on the shoe over his line", "3.2b": "the big yellow mug, the tiny white cup",
              "4.2b": "Don rehearsing Father's face", "5.3b": "the coffee lands at the line",
              "6.8b": "her eyes on his mic"})
for _k in ("1.3c", "3.2b", "4.2b", "5.3b", "6.8b"):
    STAGE[_k]["focus"] = FOCUS[_k]


# ---- 27 Nov: the tape gate replaced (four rounds unread, and Tomas: "C v1 man neaiskus"; Tomas /grill-me: Don bows from
# his own line, she opens the door herself). 7.1 (the peel) cut; 7.2 the doorman.
TEXT.pop("7.1", None); STAGE.pop("7.1", None); FOCUS.pop("7.1", None)
TEXT["7.2"] = dict(TEXT["7.2"], setup="S3 · MC",
                   picture="**The doorman, close:** at his own line Don bows low, both arms rolled out toward the office "
                           "door off screen, beaming; behind him the glass (the Client seated, the roll in his hands, a "
                           "state). No Pam, no door in frame: the door's sound carries her in (28 Nov, Tomas: 1; the wide "
                           "doorman failed three mute tests, the tape gate four)",
                   line='**DON (grandly, bowing her in): "Approved."**',
                   sound="the office door opens and shuts (off screen)")
STAGE["7.2"] = st("floor", "S3", "MC", ["don"], other=STAGE["7.2"]["other"], robot=(1, "frozen"), peak=True,
                  don_side="L")
FOCUS["7.2"] = "his grand bow, both arms to the door"
STAGE["7.2"]["focus"] = FOCUS["7.2"]

ORDER = list(TEXT)
SPEAKER = re.compile(r"\*\*([A-Z]+)\b[^*]*?:\s*\"")
INSIDE = ("FATHER", "CLIENT")                                   # who speaks inside (Pam: 8.1 inside, 6.2 outside)
PAIRS = [("3.1", "3.3"), ("3.4", "7.3"), ("7.2", "7.3"), ("2.2", "7.4"), ("6.2", "8.1")]   # script v4, the lines table
KNOWN = {}                                                     # check -> [shots]: failures accepted, with the reason


def side(space):
    return {"floor": "floor", "office": "office"}.get(space)


def check_two_spaces():
    """every change of place (floor <-> office, the moves included) carries the other space on one side."""
    bad, cuts = [], []
    seq = [(i, STAGE[i]) for i in ORDER if STAGE[i]["space"] in ("floor", "office", "move")]
    for (a, sa), (b, sb) in zip(seq, seq[1:]):
        pa = "office" if sa["space"] == "move" and sa["cam"].endswith("S8") else side(sa["space"]) or "floor"
        pb = "office" if sb["space"] == "move" and sb["cam"].startswith("S8>") else side(sb["space"]) or "floor"
        if sb["space"] == "move":
            pb = "office" if sb["cam"].endswith("S8") else "floor"
        if pa != pb or sb["space"] == "move":
            cuts.append((a, b))
            if not (sa["other"] or sb["other"]):
                bad.append("%s -> %s: neither side shows or sounds the other space" % (a, b))
            for s_, x in ((a, sa), (b, sb)):
                o = x["other"] or ""
                if o.startswith(("inside", "outside")) and re.search(r"\b(setting|takes|walks|sits down|slides)\b", o):
                    bad.append("%s: the other space is an action, not a state (lesson 22): %s" % (s_, o))
            if not sb["motive"]:
                bad.append("%s -> %s: no motive for the cut" % (a, b))
    return bad, cuts


def timing():
    return json.load(open(TIMING))


def check_lines(tm):
    meta = json.load(open(os.path.join(HERE, "da_voices", "takes", "takes.json")))
    ev = sorted((s["start"] + o, k, s) for s in tm["shots"] for k, o in zip(s["takes"], s["take_at"]))
    bad, prev = [], (0.0, None)
    for t, k, s in ev:
        if t < prev[0]:
            bad.append("%s starts at %.2f s, before %s ends (%.2f s)" % (k, t, prev[1], prev[0]))
        end = t + meta[k]["len"]
        shot_end = s["start"] + s["len"]
        if s.get("run_on"):
            nxt = [x for x in tm["shots"] if x["shot"] == s["run_on"]][0]
            shot_end = nxt["start"] + nxt["len"]
        if end > shot_end + 1e-6:
            bad.append("%s runs past its shot (%.2f > %.2f)" % (k, end, shot_end))
        prev = (end, k)
    for i in ORDER:
        ln = TEXT[i]["line"]
        if ln not in ("—", "") and not ln.startswith("(") and not SPEAKER.search(ln):
            bad.append("%s: a line with no named speaker (lesson 169)" % i)
    return bad


def check_robot():
    bad, last = [], None
    for i in ORDER:
        r = STAGE[i]["robot"]
        if not r or i in ("1.1", "1.3", "8.1", "9.1"):                 # the loop's tug and Father's step: before the spill
            continue
        n, state = r
        if last is not None and n > last:
            bad.append("%s: the pile grows (%d after %d)" % (i, n, last))
        last = n
        has_line = TEXT[i]["line"] not in ("—", "")
        if (has_line or STAGE[i]["peak"]) and state != "frozen" and i not in ("1.4", "7.4"):
            bad.append("%s: the robot works through a %s" % (i, "line" if has_line else "peak"))
    return bad


def check_pairs():
    bad = []
    for o, i in PAIRS:
        if TEXT[o]["line"] in ("—", "") or TEXT[i]["line"] in ("—", ""):
            bad.append("pair %s / %s: a side has no line" % (o, i))
    inside = [i for i in ORDER if STAGE[i]["space"] in ("office", "move") and TEXT[i]["line"] not in ("—", "")]
    paired = {b for _, b in PAIRS} | {a for a, _ in PAIRS}
    bad += ["%s: an inside line with no partner outside (lesson 253)" % i for i in inside if i not in paired]
    return bad


def check_direction():
    bad = []
    for i in ORDER:
        s_ = STAGE[i]
        cam = s_["cam"].split(">")[-1]
        want = "R" if cam in OFFICE_SIDE else "L" if cam in FLOOR_FRONT else None
        if want and s_["don_side"] and s_["don_side"] != want:
            bad.append("%s (%s): Don's side on screen %s, the mirror rule wants %s" % (i, cam, s_["don_side"], want))
    return bad


def selftest():
    """each check must fail on a planted fault (CLAUDE.md: validate on a known failure first)."""
    import copy
    keep = copy.deepcopy(STAGE)
    plants = [
        ("two_spaces", lambda: (STAGE["3.4"].update(other=None), STAGE["3.5"].update(other=None)),
         lambda: check_two_spaces()[0]),
        ("state", lambda: STAGE["4.1"].update(other="inside: the Client takes her mug"), lambda: check_two_spaces()[0]),
        ("motive", lambda: STAGE["3.5"].update(motive=None), lambda: check_two_spaces()[0]),
        ("robot_grows", lambda: STAGE["4.2"].update(robot=(25, "working")), check_robot),
        ("robot_line", lambda: STAGE["5.4"].update(robot=(11, "working")), check_robot),
        ("direction", lambda: STAGE["3.5"].update(don_side="L"), check_direction),
    ]
    ok = True
    for name, plant, chk in plants:
        plant()
        caught = bool(chk())
        STAGE.clear(); STAGE.update(copy.deepcopy(keep))
        print("selftest %-12s %s" % (name, "caught" if caught else "MISSED"))
        ok = ok and caught
    return ok


def script_v5(tm, out):
    """script v4's prose, its act tables regenerated from TEXT and the timing, and the staging table."""
    times = {s["shot"]: s for s in tm["shots"]}
    src = open(TEMPLATE).read().split("\n")
    tids = set(re.findall(r"^\| (\d\.\d+) \| \d:", open(TEMPLATE).read(), re.M))
    out_l, i = [], 0
    while i < len(src):
        ln = src[i]
        m = re.match(r"\| (\d\.\d+) \| (\d:\d\d\.\d) \| ([\d.]+) \|", ln)
        if m and m.group(1) in TEXT:
            sid = m.group(1); t = TEXT[sid]; s = times[sid]
            mm, ss = divmod(s["start"], 60)
            out_l.append("| %s | %d:%04.1f | %.2f | %s | %s | %s | %s | %s |" % (sid, mm, ss, s["len"], t["setup"], t["picture"],
                         t["reaction"], t["line"], t["sound"]))
            j = ORDER.index(sid) + 1                              # new shots (not in v4) follow the row before them
            while j < len(ORDER) and ORDER[j] not in tids:
                n = ORDER[j]; t = TEXT[n]; s = times[n]; mm, ss = divmod(s["start"], 60)
                out_l.append("| %s | %d:%04.1f | %.2f | %s | %s | %s | %s | %s |" % (n, mm, ss, s["len"], t["setup"],
                             t["picture"], t["reaction"], t["line"], t["sound"]))
                j += 1
        else:
            out_l.append(ln.replace("script v4", "script v5").replace("Script v4", "Script v5") if i < 3 else ln)
        i += 1
    head = ("# The Double Agent: script v5 (GENERATED by `src/da_scenes.py` from the scene file; do not edit by hand)\n\n"
            "Times and lengths from the recorded takes (`da_timing_v3.json`, total %.1f s). The prose below the tables is "
            "script v4's, kept as written.\n" % tm["total"])
    body = "\n".join(out_l[1:])
    st_rows = ["", "## The staging (generated)", "",
               "| Shot | Space | Setup · size | In frame | The other space | The robot | The cut's motive |", "|---|---|---|---|---|---|---|"]
    for sid in ORDER:
        s_ = STAGE[sid]
        rb = "%d clips, %s" % s_["robot"] if s_["robot"] else "—"
        st_rows.append("| %s | %s | %s · %s | %s | %s | %s | %s |" % (sid, s_["space"], s_["cam"], s_["size"],
                       ", ".join(s_["cast"]) or "—", s_["other"] or "—", rb, s_["motive"] or "—"))
    open(out, "w").write(head + body.rstrip("\n") + "\n" + "\n".join(st_rows) + "\n")


def main(out_dir=EP):
    if not selftest():
        print("a check misses its planted fault: not trusted"); return False
    tm = timing()
    two, cuts = check_two_spaces()
    results = dict(two_spaces=two, lines=check_lines(tm), robot=check_robot(), pairs=check_pairs(),
                   direction=check_direction())
    print("place changes (%d): %s" % (len(cuts), ", ".join("%s>%s" % c for c in cuts)))
    fail = False
    for name, bad in results.items():
        new = [b for b in bad if b.split(":")[0].split(" ")[0] not in KNOWN.get(name, [])]
        print("%-10s %s" % (name, "PASS" if not new else "FAIL"))
        for b in bad:
            print("    " + b)
        fail = fail or bool(new)
    out = os.path.join(out_dir, "the-double-agent-script-v5.md")
    script_v5(tm, out)
    print("wrote", out)
    return not fail


if __name__ == "__main__":
    sys.exit(0 if main(*sys.argv[1:]) else 1)
