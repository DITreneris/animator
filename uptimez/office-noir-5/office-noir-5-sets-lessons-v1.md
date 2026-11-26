# Office Noir 5: the sets, decisions and lessons (v1, 25 Nov)

## Tomas's picks (/grill-me, 25 Nov)

Source: his photo walk of 25 Nov, 19:26–19:30 (11 photos, `on5_photos_contact.png`, not committed).

| Decision | Pick |
|---|---|
| The alley (photo 1) | the opening (0:00); hero frame = a figure under the near doorway's canopy, in its pool of light, his long shadow to the kerb; colour = warm yellow against cold blue; redrawn in pycairo as a set module (`src/alley_on5.py`, v1 stills done) |
| Sets | all four: the wrapped dome behind the long wall (8–10), the empty crossing (5–6), the garages with graffiti (2), the traffic light close (7) |
| Structure | **a chase** along the walk's route: alley → garages → crossing → light → dome |
| The dome | **the goal**: the place he must reach all night; the wrap hides what is inside (the reveal at the end) |
| Motion-blur photos (3, 4, 11) | **transitions**: whip-pan smears between places |

Still open (next /grill-me): whose dream, who runs, who chases, what is under the wrap, the physical gag by 0:01.

## The lessons that apply (docs/lessons.md, line numbers as of 25 Nov)

| # | Line | Rule | For Noir 5 |
|---|---|---|---|
| — | 17 | The first seconds make sense with no context; several quick shots, not one static wide | the alley opens on the hero frame, then cuts; not a slow push on an empty street |
| — | 19 | Loop through an action, not a repeated line | the dome back to the alley's pool of light by an action (he steps into the light again) |
| 47 | 611 | A silhouette needs a lit wall behind it, measured on a phone | the alley: figure against the lit doorway (v1 does this); the crossing: figures against lamp pools, never against black sky; the dome wall must be lit where the shadows play |
| 50 | 614 | Noir is light, not grey: one source per place, one side dark | each set gets ONE key light: doorway (alley), the lamp over the garages, the three lamps (crossing), the floodlight on the dome |
| — | 150, 160 | Smear with ghosts reads as a second character in a pause; use speed lines and a stretch along the motion | the blur transitions: streaks and stretch only, no ghost copies of a person; a smear never held as a still |
| — | 238 | Push-ins wait for entrances | a chase cut: the runner fully in frame before the camera moves |
| 55 | 622 | Catch an entrance mid-step | each place entered mid-stride, a foot still behind the wall's end or the van |
| 53 | 620 | Reactions face their target | chaser and chased look at each other across the crossing, not at the lens |
| — | 186, 214, 216 | Plant the ending in the opening shot; plants readable the first time | the dome (the goal) visible far away in the alley's first frames, then bigger each place; the graffiti word (our own) big enough at 270 px |
| 51 | 618 | Cold-test the whole board, with the loop question | the chase board as a whole, not place by place |
| 52 | 619 | Three fixes that don't land: cut | per shot |
| CLAUDE.md | — | No real brands or logos | the van has no livery; the graffiti is ours (the photo's tags belong to their writers); the church is a generic domed building, not a copy of the real one |

## Reuse before new code

| Set | Reused | New |
|---|---|---|
| Alley | `street_on3.view`, `kit`, `noir2_cast.shadow`, `on2_motion.glints` (copied) | perspective layout (done, `alley_on5.py` v1) |
| Garages | Noir 3's side-on lit wall and shadow staging (`alley_on3_v5.py`: `draw_alley2`, `gangster` shadows), its brick | the garage doors, our graffiti |
| Crossing | `street_on3`: the lamp post, its cone and pool; `glints` | the wide road, lane marks, the cyan signal, the moon in haze |
| Traffic light | — | the pole, the cyan lamp, the crossing sign (no real sign artwork beyond the generic pictogram) |
| Dome | — | the wrapped dome, scaffold ring, the long wall, trolley wires |
| Blur transitions | the series' speed lines | a streak pass over the outgoing frame |
