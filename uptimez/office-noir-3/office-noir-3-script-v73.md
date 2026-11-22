# Office Noir 3: script note v73 (22 Nov) — release_v6, film v38

**What changed:** the man on the sofa in 8.2, 8.4 and the start of 8.5 is drawn anew (`src/garage_lying_on3.py`).

- **Fault (Tomas, 1:20):** his head was the whole standing boxer, turned 30° and clipped to a circle, so pieces of that boxer's robe and shoulders showed inside the circle. Taking the collar off in v32 ("a red square on his face") uncovered more of them. His body was straight quads.
- **Now:** the head is clipped to its own outline and turned 58° onto a pillow; one body on its side (neck, collar, shoulder, waist, hip, belt, gown to the knee, bent legs, bare feet); the arm hangs over the seat's edge to the phone, or goes round behind his head to the table in 8.4.
- **From the review of the still (triage in the chat):** his eyes on the phone while it lies on the floor; a contact shadow under that phone; the "10" of the faded plan darker (also in 8.2b). Refused: "GARAGES TRANSFERRED" on the screen (the garages are not transferred), a closer frame (feet and plan would be cut), a tie (he wears a gown). The reviewer took the Client for Don.
- **Opt-in:** `garage_on3.py` is untouched; the film's v38 calls `garage_lying_on3.install(ga)`. `film_on3_v37.py` and `on3_animatic_v32.py` are the pins.

**QA, release_v6 1080:** 1080×1920, 30 fps, 2616 frames, BT.709; −15.5 LUFS, true peak −1.1 dBTP; loop 0.63/255; speech 37/37, backwards 0/37; PSNR vs 540 mean 38.6 dB; tails pass. Not checked by a worker: text boxes, bubbles on faces, signs at the edge.

**Not done:** no cold test of the new figure; the approved earlier renders were not rebuilt for an md5 comparison; in 8.4 most of the reaching arm is behind his head; his second arm is under the pillow; the shins are short so the feet stay in frame.
