# Perfect Date (in development)

ME + MY AI episode. Hoody asks his AI to help him impress Eva; the AI's demonstration wins her instead ("Your turn!").
Concept and character work only; nothing is built yet.

- `characters/eva.py`: Eva v2 (gold hoops, a lash on every expression, the one-brow signature, four poses) and her dog. `python3 characters/eva.py` writes `characters/eva_sheet.png`
- `characters/myai.py`: MY AI v2, his companion robot (body from `whos-a-good-boy/v3/v.py`). Arms are a fixed two-segment rig (upper arm 68, forearm 68, shoulders at ±72, 112) posed by joint angles within limits, so arm length cannot drift; ten named poses incl. WAIT; head tilt ±15°; a three-quarter turn; eight eye shapes incl. CONFUSED and BLANK; the rose, speaker and heart balloon. `python3 characters/myai.py` writes `characters/myai_sheet.png`
- `kit.py`: a copy of the series drawing kit (from `says-here-boss/v3/`)

**Eva** first appeared, unnamed, as the neighbour walking the red-collared dog in *Who's a Good Boy?* (`whos-a-good-boy/v3/v9.py`, `neighbor()`). v1 keeps that design (yellow coat, dark curls, coffee, the dog) and moves her onto the series face system. Her scarf is MY AI's eye colour (#33bfff).
