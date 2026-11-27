# The Blueprint — 16:9 developing

Roadmap for the pilot after the room lock. The boxes are [`todo.md`](todo.md). The room is [`set-16x9.md`](set-16x9.md). Progress of the picture is [`changelog.md`](changelog.md).

A Windows filename cannot hold a colon, so this file is `16-9-developing.md`.

## Where the work stands

The room is locked (25 Nov 2026). The film is not. Live `bp_draw_audit.py` exits 0; `--plant` exits 1 with the eight **old** planted misses only. Geometry (phase 1) is done.

**Current picture:** `bp_pic_v5.mp4` (clutch on shred, card and tape; opened, not watched). **Current mix:** `bp_sound_v3.mp4` on `bp_pic_v3`. **Next:** watch v5, then `bp_sound_v4` with `picture=bp_pic_v5`. Pin tag `uptimez-blueprint-pic-v4` freezes the watched v4 commit.

The locked cameras are S0, SHRED, COUNTER, PUSH and NIGHT. ZERO, STAMP and PLAN are rough crops in `bp_frame.py`, not in the set file. SCREEN, BIN, VOID and the new axes stay unasked.

## The order

Each phase ends with something that can be looked at. The next phase starts from that, not from a new idea.

```text
1 Geometry     the eight fails gone, audit exits 0
2 NIGHT still  both heads seen, then the number may enter the set file
3 Silent rough the 6:40 on this room, watched
4 Walks        arrival, and the walk back at 1:20
5 Crops        only the words the rough could not read
6 New axes     only a beat the front wall could not tell
```

### 1. Geometry

Cost: coordinates and one camera triple. No new drawing. No new prop.

Move the shred, the finger, the pocket, and the stamp onto the locked objects. Point shot 11 at PUSH. Point shot 05 at a crop centred between Sofía and Pam. A starting triple, not yet locked, is (560, 360, 1.85): world x about 300–820, which holds Sofía, Don, the shredder, Pam, and Mom, and drops the Client and both doors.

Pass: `bp_draw_audit.py` exits 0, and shot 01 still passes.

### 2. NIGHT still

Cost: one PNG.

Render it and look at both heads at full size. The counter close-up already teaches the rule: a crop can cut a sign, and the set file has to say so. OUR FIRST CLIENT's cropped top is that written exception. A new crop does not get the same courtesy until someone has seen it.

Pass: both heads inside, no new furniture. Then the triple may be written into `set-16x9.md`.

### 3. Silent rough

Cost: one render on this room. The rough budget is 5. `bp_rough_v1.mp4` is the old room and has already spent a version that cannot be used to judge this set.

Watch the 6:40 with the sound off. The Kokoro licence blocks a public master. It does not block this viewing.

Pass: a note of which beats read, and which beat the front wall cannot tell. That note is the only brief for phases 5 and 6.

Passed 25 Nov 2026. `bp_rough_v2.mp4`. The note is `rough/bp_rough_v2_note.md`. Version 1 is the old room and was not rewritten.

### 4. Walks

Cost: paths on the existing homes.

Two walks are already in the cut. The Client comes in through the glass door at 0:00. He walks back to it at 1:20. Catch each one mid-step. The people on one side of the cut are the people on the other.

The passage between the desk (ends x 846) and the CEO door (x 888) is 42 px. It stays narrow. Nobody's path widens it.

Passed 25 Nov 2026. `bp_rough_v3.mp4`. The note is `rough/bp_rough_v3_note.md`. He arrives during the first 3 seconds of shot 01 and steps back during the first 3 seconds of shot 04. The hold of shot 04 puts him on the mark again. That return is a cut.

### 5. Crops

Cost: tighter triples on the same drawing. SCREEN, BIN, STAMP, PLAN. VOID only if phase 3 says the empty office has to read alone.

The CEO door is a slot, about 44 px of leaf and a dark opening. It is not a view of the room.

Passed 25 Nov 2026 for the words the rough could not read. `bp_rough_v4.mp4`. The note is `rough/bp_rough_v4_note.md`. ZERO opens shots 07 and 12. STAMP follows the landing on shot 13. PLAN opens shot 05, and the night hold hides the strips again. The poster still says 0. SCREEN alone, BIN, and VOID were not asked for. The triples are not in `set-16x9.md`.

The four pictures the rough named are on the locked cameras. They are not a new axis, and they are not in the set file. The cannon is an insert on the shot 04 hold, after the walk (`stills/bp_still_cannon.png`). The one star is an insert on shot 12, after ZERO (`stills/bp_still_star.png`). The poster still says 0. The mute week fills shot 08 on COUNTER: retries, STUPID in lipstick, MON 1 and THU 4, one deleted message. Rough v5 is the cut that carries them. It is the last rough in the budget.

### 6. New axes

Cost: a new drawing per angle. The cast's sides, or the room from outside the glass door, or the room from above. A three-quarter face is one of those drawings. The cameras in this cut are crops of the front wall, and `look` only shifts the pupils. Do not draw a turned head until phase 3 names the beat. The window stays light off the left. It is not a new window on the back wall. There is no street beyond the door. The open hole is the street.

Build one only when phase 3 names the beat. Suggested order if the rough asks for the door: the reverse through the glass door at 1:20, then the walk in. The bird's view is one shot, for a beat whose joke is where the paper is. `bp_ground_plan.png` is the label sheet, not that shot.

First person entering and the Client cannot share a frame. First person leaving stops on the door frame and does not replace the stamp.

### 7. Rough with sound

Cost: no drawing. v5's picture, stream-copied, under the dry takes. A budget of its own, `bp_sound_v1` to `v5`, because v1 to v5 were silent picture roughs: they could not judge the holds that were timed for talk, and the v5 cold watch said the meaning is in the talk.

The voices are the shipped takes, copied (`bp_voices.py`). The night lines are local only until the Kokoro licence is decided. The times come from the source films (`bp_scenes.timeline`), and `bp_draw_audit.py --lines` keeps each speaker inside the camera of the moment. Loudness is measured on the AAC.

Pass: `uz_check` without faults, every line heard inside the mix, the drawing audits at their exit codes, the locked stills unchanged, and two cold viewers on frames plus the transcript.

`bp_sound_v1.mp4`, 26 Nov 2026. The note is `rough/bp_sound_v1_note.md`. Stop 2: the night takes stay, local only, and "Paid $999" stays. The cold watch failed on the picture (3 of 5), so there is no `bp_sound_v2` on this picture. Shot 10's two off-screen voices are accepted on this file only.

### 8. Picture pass

Cost: a new picture, not a redraw of v5. Budget `bp_pic_v1` to `v5`. The silent budget of 5 was picture without talk, and the sound budget is mixes on a frozen picture.

Bubbles on the hold while that person talks (`speech.draw`, `SAFE_16X9`). The poster zero stays dull until Don's "Approved." on shot 07, then green, as an overlay: `bp_set._poster` and the four locked stills are not edited. Shot 03's shred follows "We'll take care of it." with Don's hand on the sheet. Shot 11's pocket follows "Is this a joke?" with Pam's hand on the card. Shot 10 is PUSH in this cut only.

Pass: `speech_gate` on every bubble, the zero plant, the hand plant, `uz_check`, the locked stills at their md5, and two cold viewers. A failed bubble check is fixed before any hand work. Two check runs with no fall in faults stops the session.

`bp_pic_v2.mp4`, 26 Nov 2026. The note is `rough/bp_pic_v2_note.md`. v1 (`rough/bp_pic_v1_note.md`) is bubbles, the dull zero and shot 10 on PUSH, with the inserts left in v5 order. Three attribution watches. The third passed on the body: "I won't draw one" is the blonde, and the other two lines are the woman in the purple top at the desk. Names are not printed.

v2 moves the shred to after the promise, with Don's hand on the sheet, and the pocket to after the joke, with Pam's hand on the card. Both viewers read 4 of 5. Don shreds. That same desk woman finds the card. Both missed what the robot stamps, and they gave different wrong answers (the zero turned green; a blank yellow circle). The stamp draws CUSTOMER SUCCESS. That miss does not spend v3.

`bp_sound_v2.mp4` is those packets with the v1 takes and the v2 times. −15.2 LUFS. Whisper 43 of 43 and 37 of 37. A bare mix still rebuilds `bp_sound_v1_nonight` at md5 `ce8403457c981d5f1d05cd8c01e5cd5e`. Stop 4 is `rough/bp_stop4.md`.

Stop 4 is answered 1. The stamp miss does not get a version: the words stay CUSTOMER SUCCESS in the note. `bp_pic_v3` spends the next picture on three beats the wide still cannot tell. The portrait falls off the wall. The cannon fires. Pam matches the strips on "I'm matching them." 400 s and the v2 line times stay.

`bp_pic_v3.mp4`, 26 Nov 2026. The note is `rough/bp_pic_v3_note.md`. Both viewers read a framed face, a cannon that fires, and the desk woman matching the strips. [I](0f3375b4-fdc7-4442-8a3b-ac458a3f13ef) 5 of 5, [J](c775c735-83e1-48fc-a6db-cf321cc6c07d) 4 of 5. J gave the finder to the older woman. Both read the stamp as CUSTOMER SUCCESS.

`bp_sound_v3.mp4` is those packets with the v2 times. −15.2 LUFS. Whisper 43 of 43 and 37 of 37. A bare mix still rebuilds `bp_sound_v1_nonight` at md5 `ce8403457c981d5f1d05cd8c01e5cd5e`.

`bp_pic_v4.mp4`, 27 Nov 2026. The note is `rough/bp_pic_v4_note.md`. Sheet look on (`SHEET`, `MOM_ARMS`). Watched the same day against `rough_work/pic_use/`. Shred, card and tape stayed `point`. `bp_pic_v5` is the clutch pass on those three holds. No `bp_sound_v4` until that picture is watched.

## What stays put

- The three locked stills, the homes, Don at 0.60, the desk, both doors, the one ficus.
- The paper cut's length, 400 s, and the cut lines in the shot list. The closed loop stays out.
- The ending: the robot stamps CUSTOMER SUCCESS. No loop.
- 9:16. `fs_set4.py` and `series/front-desk-set.md` are the other room. `uz_check.py` is the other checker.

## How a phase is allowed to fail

`bp_draw_audit.py` is the geometry check. Before a still is called locked, run `/quality-assurance-agent`. The command is `.cursor/commands/quality-assurance-agent.md`. The agent is `.cursor/agents/quality-assurance-agent.md`. A still also gets the look in that skill: signs whole or fully out, type inside its plate, one shadow direction, the speaker's head in frame.

A failed phase goes back to the phase that made the miss. It does not add a prop.
