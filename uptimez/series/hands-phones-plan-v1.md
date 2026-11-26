# Hands and phones: the plan for The Offer and Daddy's Home (26 Nov)

Tomas: "taip, tvarkom detaliai, suplanuok". The canon: DITreneris/uptimez `CANON.md` and `docs/rules-hands-and-phones.md`. The phone is v4c; grab, pinch and fist come from the sheet; `board_two` and `tap_insert` are new rows. The way in is `hands_v4.enable(phone="v4c")`. One Star v27 is done (only 0:30 and 1:04 changed; gates pass).

## 0. What I got wrong in audit v1, and what changes because of it

The audit's frames came from stale files:
- **The Offer:** rough cut v39 (main is at v57);
- **Daddy's Home:** anim v7 (main is at v8: scenes 3–4 restaged, a 1080 master script).

Both films' findings are re-done on the current builds **before** any fix. A fix goes only on a fault seen in the current film.

## 1. Baselines (no change, current builds)

| Film | Build | Output |
|---|---|---|
| The Offer | `of_film.py 1..5` (VER: s1–s4 v52, s5 v57), `of_cut.py` | `/tmp/of_base/`: 540, 1 fps and 4 fps sheets |
| Daddy's Home | `dh_film_v8.py 1..8`, `join` | `/tmp/dh_base/`: same |

From each baseline:
- a frame list of every **phone**, **held prop** and **hand at a prop or a face**, by time, with the job row it should be (rules §0.1);
- the faults per row: **fail** (a rule is broken: thumb on words, a hand with no wrist, two hands on one wrist, a pole arm) or **polish**.

## 2. The change per film (opt-in, new version numbers)

Each film gets a new entry script. The old versions and files stay.

**The Offer v58** (`of_film_v58.py` or `VER` +1 behind a flag):
1. `hands_v4.enable(phone="v4c")`: every `of_cast.phone_grip` (13 calls: DELETE, PAM, calendar, Father's phone) becomes v4c; grab, pinch and fist become the sheet's.
2. Calls with a pressing thumb (`thumb_tip`), parts (`part="back"/"front"`), the phone's back (`back=True`) or a tilt over 0.35 keep the old grip (`hands_v4` falls back). Listed by shot so Tomas sees which.
3. Only faults found in §1 get a manual fix, each a still first.

**Daddy's Home v9** (`dh_film_v9.py`, `dh_master_v9.py`):
1. `hands_v4.enable(phone="v4c")`: Don's phone at his ear (`dh_anim1_v8`, `phone_grip` with a tilt; at the ear it is the phone's back, so it falls back to the old grip, as the rules want).
2. **Father's tablet (0:02, 0:08, 0:12):** `board_two` if the current build still holds it by two plain blobs at the bottom corners.
3. **Don's straight arms ("Dad is coming", the cheer):** an elbow bend in the pose (rules: "an elbow under 20° that does not hang is a pole"), if the current build still has them.
4. Sofía's "show" tablet (3.x): `board_two` or `clutch`, if it reads as loose ovals.

## 3. Checks for every changed shot (rules §0.3–0.6)

1. A still at full size and at 270 px, **before** the render.
2. Pixel gaps: thumb to word, finger to face, hand to hand.
3. A diff against the baseline at the same times. The only drawings that change are the ones listed in §2. Anything else changed stops the work.
4. The film's own gates: `qa`/scene checks, The Offer's sign/scale/dead-zone checks, Daddy's Home's bubbles and `_fresh`.
5. A 10 fps strip of the encoded file for each changed shot.
6. Two cold viewers on the changed shots only: "what is in his/her hand, what is he/she doing with it".

## 4. Stop rules

- A drawing that gets worse than the baseline in any one place goes back to the old one for that shot, and is listed.
- After two full check runs without the faults going down: stop and report (CLAUDE.md rule 5).
- Nothing goes into a release file. New files have new names; Tomas approves before any master.

## 5. Order and stops for Tomas

1. Baselines and the re-done findings → sent (stop 1: Tomas confirms which faults to fix).
2. The Offer v58 stills → sent (stop 2).
3. The Offer v58 film → sent.
4. Daddy's Home v9 stills → sent (stop 3).
5. Daddy's Home v9 film → sent.
6. The audit doc closed: what changed, what was left and why.
