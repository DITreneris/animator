# Daddy's Home: hands audit v1 (24 Nov)

Scope (Tomas, /grill-me): Daddy's Home only. The film as it stands for v8: `daddys_home_anim_v7.mp4` (scenes 1, 2, 4–8), `dh_s3_anim_v8.mp4` (scene 3, round 7) and the scene 4 v8 stills (`dh_s4_v8.py`, round 1). Method: frames at 2 fps over the whole film, then every frame with a hand doing something at full size. Judged against `docs/rules-hands-and-phones.md` sections 0–1 and lessons 163, 178, 179, 200, 207, 208, 221, 224, 225, 245, 263, 264, 336, 417. Found faults are fixed in v8 only; shipped films are not touched.

## Fail

| # | Time (v7) / shot | Who | What a viewer sees | Rule |
|---|---|---|---|---|
| 1 | 3.0–9.5 s (scene 1) | Don | The hand is behind his head; the phone sits by his cheek, not in it | phone_grip (179), one hand per wrist (208) |
| 2 | 40.5–43.5 s | Don and the inspector | Don's arm a straight white bar across to the inspector's fist: "a pole", and a handshake | reach (179), 221 |
| 3 | 60.0–61.5 s | Pam | The mug hangs in front of her chest with no hand on it; her other hand on her brow over the glasses | 208, a face beats a gesture (163) |
| 4 | 65.0–66.5 s insert | Mom | A teal sleeve from the corner to Don's zip, no person: "a tube" | inserts (224, 225) |
| 5 | 67.0–68.5 s | Sofía | The CV floats beside her, both hands empty | 208 |
| 6 | 75.0–89.0 s | Don | His raised arm behind the price tag, his body cut by the frame edge: an arm without a body, "holding the tag" | 245, finger near a sign (rules §1 Gestures) |
| 7 | 3A (scene 3 v8) | Don | Finger near the rating sign: "holds the sign", the sign floats when the arm drops (3 cold tests) | Gestures, 178 |
| 8 | 3C (scene 3 v8) | Pam | "One" finger beside her ear: "on a phone call" (2 of 2) | Gestures (ear = phone), 417 |
| 9 | 3E (scene 3 v8) | Mom, Sofía | Cloth hand next to Sofía's palm: "a handshake" (4 cold tests) | Gestures, 178 |
| 10 | 4D2 (scene 4 v8 stills) | Pam | The mug raised beside her head, at ear height: the same place as Pam's finger in #8 | Gestures (ear = phone) |
| 11 | 4D (scene 4 v8 stills) | Pam | The near counter covers her shins and shoes, as 3C did before round 7 | not a hand rule: the same layering fault |

## Partial

| Time / shot | Who | What | Rule |
|---|---|---|---|
| 2.5–11.0 s, 34–35.5 s, 47.5 s | Dad, the inspector | Mitten hands with no fingers, not the series hand; the tablet and the case read, but the grip is a blob on the edge | one hand for the cast (147, 206) |
| 19.0–19.5 s | Don | "...was invested": a straight arm to the chair ending in a mitten, no pointing finger | a shape per state (207), reach (179) |
| 36.0 s | Don | His arms across Mom's chest and toward Sofía's clipboard | 221 |
| 40.0 s (v7 scene 4) | Pam | The mug held up beside her head | Gestures (ear = phone) |
| 58.0–59.5 s | Inspector | A straight arm out, the hand hidden behind the invoice | reach (179), draw the object then the fingers (224) |
| 79.0–79.5 s | Sofía, bodyguard | Her arm straight out toward his hand on the CV | Gestures (two people's hands = handshake) |

## OK

Don's arms up or out (13.0, 22.0, 37.0 s), his hand at the back of his head in worry (16.0 s), the inspector's tool at the machine (51.0 s) and the insert from the edge (51.5–52.0 s), the bodyguards' clasped hands (70–74 s), Pam holding the HAND OF THE CEO sign in both hands, the APPROVE insert (scene 3 v8, round 7).

## What correlates

1. **A prop beside the hand, not in it** (#1, #3, #5, the invoice). These shots predate the rule "a prop held by a rig's hand is drawn in that hand's coordinates" (found on the mug in 4D''). The fix is the same one: record the hand's matrix, draw the prop under it, draw the hand again over it.
2. **A straight arm reaching across to someone else or something far** (#2, #6, Don at 19 s, the inspector at 58 s, Sofía at 79 s). The target is out of reach, so the arm goes straight ("a pole"), and when the target is another person's hand it reads as a handshake. The fix: move the person closer or change the gesture (178), not the arm.
3. **Hands at the head** (#8, #10, the mug at 40 s, Pam's hand over her glasses at 60 s). Beside the ear it reads as a phone; over the eyes it hides the face.
4. **Two hand systems:** the PS rigs use `hands_ps`; Dad and the inspector have mittens. They read, but they cannot hold or point like the others.

## For v8 (in order of the scenes being restaged)

- Scene 3: #7, #8, #9 (siluetai first, rules §0).
- Scene 4: #10 (the mug in front of her chest, not at her head), #11 (the counter below her soles), the partial at 36.0 s if it is in scene 4.
- Scenes 1, 5–8 when they are restaged: #1–#6 and the partials, each by the correlate's fix above.
