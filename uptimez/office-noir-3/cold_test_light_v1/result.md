# Cold test 43: the film lit (20 Nov)

Tomas: "why did Office Noir 1 and 2 look better; the lighting?" Measured: Noir 1 mean brightness 0.30, Noir 2 0.33, Noir 3 0.41; mid grey 34%, 34%, 48%; and Noir 3 called none of the first two films' lighting tools. A trial of two recipes on seven frames (`on3_light_trial_v1.png`); Tomas: "I think it is good"; an outside audit of the trial: A 7.5/10 the base, B 7/10 for depth; faces lighter, the vignette a quarter less, no shadow ovals.

`src/light_on3.py` `auto`, `src/film_on3.py` v14 (v13 pinned), `on3_animatic_v10.mp4`, 93.7 s. On every finished frame of the dream, after the noir pass: a pool of light round the tracked figures and the rest sinks; each face lifted a little from above; a brow shadow in close shots only; a vignette of 0.25; grain. The waking scene stays plain and in colour. The cards and bubbles are drawn after the light.

| The dream, measured | v9 | v10 as tested | Noir 1 / Noir 2 |
|---|---|---|---|
| Mean brightness | 0.39 | 0.31 | 0.30 / 0.33 |
| Mid grey | 46% | 39% | 34% / 34% |
| Centre brighter than the edges by | 0.11 | 0.20 | 0.06 / 0.20 |

**The audit's points:** faces lighter than B (done: faces are lifted, never darkened, in wide shots); the vignette less (0.34 -> 0.25); no shadow ovals (B's body shadow is out); light gathered on the head and the raised glove (the pool follows the tracked heads); edges on the alley's shadow figures (not done: they are shadows on a wall, drawn flat; a drawing change, not a light).

**Also found:** the last frame had not equalled the first since the cast began to breathe (film v9): the two ends breathed at different moments. The loop's two shots are now still; first and last frame differ by 0.

**Two fresh viewers, the whole picture silent (157 tiles at 2 fps) and at phone size.** Both tell the story; the loop closes for both.

| Asked | Viewer VV | Viewer WW |
|---|---|---|
| Where is the light | "a central cone or pool (streetlamp, ring lamp, blinds stripes); the top and bottom thirds and the edges are dark. The ring scenes and close-ups read well" | the lamp's cone, the ring's lamp, the blinds, "soft centre spotlights on close-ups"; "The main faces in close-ups are all readable" |
| Too dark | the car "black on black"; the Client small and dim under the shadows (3.1); the figure in the doorway (4.1); his back at the desk "an almost solid black blob" | the same three; and the robot "dark against a dark crowd" in wide shots |
| Lit wrongly | "a grey oval with a soft halo" round the boxer seen from above (5.6); a grey oval in the white flash; "a bright glow blob behind the robot's head"; the glove in frame 1 "semi-transparent" | the same ovals |
| Phone size | poster yes; ticket yes; Tower yes; stamp words yes; CV number "just readable"; matches "not really"; 10 GARAGES in close shots only | the same |
| His back at her desk | "the hooded boxer seen from behind… the rounded hood with a seam down the middle and the red glove"; "Without the glove it would be an unidentifiable black shape" | "a rounded hood with a centre seam, sloping shoulders"; "On its own… could pass for a chair back" |

**Changed after the test (looked at in frames by me, not re-tested):** the pool sinks less (0.56 -> 0.48) and is taller, for the car and the far figures; no pool on the view from above; a white flash is left alone; the robot's head is not lifted; no face light where the glove covers the face (the first and last picture, the last punch); his back at the desk is lighter with a strong edge of light from the window.
**As delivered, after those changes:** mean brightness 0.33, mid grey 44% (the softer pool gave back some grey). The file is encoded at crf 27: with grain, crf 18 made it 102 MB, over the repository's limit.
**Open:** the matches at phone size; the figure in the doorway (4.1) dark on dark; the oval round him in the view from above is that picture's own drawing.
