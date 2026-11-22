# Office Noir 3: The Last Round. Script note v72 (22 Nov): release_v5

Film v37, animatic v32 (87.2 s, 2616 frames), drawn at 1080. No line is changed.

## An outside frame review (17 holds): triage and what was done

What correlated: (1) no worker ever checked this film's tails: they aimed at a tracked head point, not at the mouth as drawn; (2) nor its signs: the cameras were re-aimed round the figures and the signs fell where the edge was; (3) two were the film's own choices (the glove over his eye, the white).

Tomas's decisions: off-screen speakers get no tail; the glove moves to his cheek, both eyes seen, the same gesture; at "How much?" the tail stays, to the side of his hood; Don gets his own voice back.

| Hold | Done |
|---|---|
| Tails on a hat, hair, brim, beside the glasses (27, 44-46, 57, 63, 73 s) | The mouth is found on the drawing (the speaker drawn mouth open and mouth shut; the difference), carried by the tracked head; the tail ends on the cheek beside it and comes round the outside of the head |
| "One hundred bucks." above the mouth (4.3b) | Her mouth measured the same way on her close picture |
| Tail to the car, down the sleeve, to nothing (5, 36, 75 s) | No tail; the bubble sits at the edge the speaker is at (on the car, by her hand, at the robot's side) |
| "How much?" (31 s) | The tail to the side of his hood |
| ONIGHT, AR, O GA, 10, 10 GAR, ND 1, posters at the edge | A sign that the frame's edge would cut is not drawn (the bill, the ARENA plate, the hung plan, the round card in the glass): whole or out |
| LAST / ROUN (68 s) | Left: the card crosses the frame; it is cut while it enters and leaves |
| GES (75 s) | Left: his gloves cover the plan as he takes hold of it; the frame does not cut it |
| A glove covers one eye (53, 78.7 s) | The glove lands lower and further out, on the cheek: both eyes and the mouth are seen (5.5 and 7.5) |
| Eleven white frames | Five |

**Don's voice:** the series' Don (am_onyx, sound_bc.don) in all four of his lines; he had am_michael at 1.08 since v6.

## G5 (src/on3_qa.py) on office_noir_3_release_v5_1080.mp4: PASS

1080x1920, 30 fps, 2616 frames, BT.709; -15.5 LUFS, true peak -1.1 dBTP; speech 37 of 37; frame 0 = the last frame.
New check, TAILS: 208 tail positions over 9 lines end beside the drawn mouth (within 0.2 to 0.6 of the head's half-width, level with it). Proved on a known failure: release_v4 fails it. Exempt, by name: the Client at 4.3 and Don at 6.4 (backs to us).

## Not checked, not tested

- No worker for signs (the rule is built into the drawing, not checked on pixels), for text boxes in the safe area, or for bubbles on faces.
- Nobody has heard Don's new takes but the recogniser (words right). No cold test since test 68.
- While building: the sign rule did nothing in the first 1080 build (it halved its coordinates there); found on the frames, fixed, rebuilt.
