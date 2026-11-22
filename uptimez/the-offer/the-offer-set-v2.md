# The Offer: the garage set, v2 (stage 3)

Built by `src/of_set.py` (`python3 of_set.py`). It uses the series' set units (floor line F = 800) and the series' scales: the Client 0.52, the bodyguards 0.56, Father 0.62.

| Sheet | What it shows |
|---|---|
| `of_set_v2.png` | Frame 0 at 540, then with the apps' zones; frame 0 and the last frame at 270; the plan close up before and after the burn |
| `of_set_plan_v2.png` | The bay from above, with every garage camera in script v4 and where people stand in scene 2 |
| `of_set_props_v2.png` | The new props as inserts at 270: DELETE POST, the lighter, PAM — finds things, WITHOUT HIM, INVITATION |
| `of_blocking_s2_v2.png` | Scene 2 (The Lighter), shots 1.1–1.7, with the cast. Each shot shows the biggest face, anything in the apps' zones, and the state of the GARAGE 7 sign |

## The set

- **Layout:** one bay, clean and organised. A blue hatchback on four stands, nose to the right. Legs on a creeper come out from under the sill. The caged lamp lies on the floor on its cable. A red cabinet with the radio on it stands in front at the left. A pegboard holds every tool on its painted outline. The roller door is up onto a bright street.
- **The plan:** episode 11's drawing (`cs_props.plan`, "whole"), pinned under a painted **GARAGE 7**.
- **Frame 0:** camera (290, 677, 1.00). GARAGE 7 is whole in it. The legs end at y 717, inside the 720 line.
- **The last frame:** the same drawing with the brown burn mark on 7's corner.
- **Space behind the car:** there is a walkway between the car and the wall, so the loyal bodyguard can reach the plan.

## v2, after the outside review (22 Nov)

Fixed:
- **1.2 lighter:** a square case, the lid open on its hinge, the chimney and the wheel; the loyal bodyguard's fist holds it, his sleeve and white cuff going off right.
- **1.7 burn:** a charred patch on 7's corner, black at the centre with a ragged brown edge. It reads at 270.
- **1.6 Father alone:** bodyguard 1 now stands by the car's tail (x 240), so Father has the frame to himself and the wide no longer hides him.
- **1.3 creeper:** the board and its castors show under the Client when he sits up.
- **1.4 the Client's face:** `plain` (level, nothing in it), not the brow that read as nervous.
- **Moved:** the sign and the plan moved 50 right and the pegboard went to the left of the plan, so the 1.1 frame holds GARAGE 7 whole with bodyguard 1 out. Frame 0 is now (310, 677, 1.00).

Chosen by Claude (Tomas: "choose what is better"); not yet in the script:
- **1.5** is 1.1's frame, not a close-up: the plan stays whole and his head turn to Father is the action. Script v5 to say so.
- **3.6 INVITATION** reads "from FATHER" rather than repeating the robot's line. Script v4 said only INVITATION.

Kept against the review: the plan as drawn in episode 11, the one-star post, PAM — finds things (protect #3), the scene's order with 1.3–1.4 (protect #2), the series' face size (r 78).

## Scene 2 blocking

| Shot | Biggest face (r) | In the apps' zones | GARAGE 7 sign |
|---|---|---|---|
| 1.1 / 1.2 / 1.5 / 1.7 | 54 | nothing | whole (camera set by hand: the sign is the "real bay" he looks round at) |
| 1.3 | 31 (wide) | nothing | whole |
| 1.4, 1.6 | 78 | nothing | out |

## Open, for Tomas

1. **The Client's garage clothes.** He wears the green jacket from episodes 9–11, without the visitor badge; only his legs wear the work trousers from the script.
2. **Poses still to build** for the motion tests: the Client sitting up (here his top half is clipped over the creeper), the finger on 7, and the head turn in 1.5.
3. **1.4:** bodyguard 1's chin and body are cut at the top left of the frame. A cheat of a few units moves him out.

## v3 (22 Nov, stage 4)

The car's body is drawn 20 % lower (`CAR_SQUASH`), so its roof is at a man's shoulder and bodyguard 1 can lean on it in 0.8. The sheets are `of_*_v3.png`; the v2 sheets are kept.

## v4 (22 Nov, after the mute test of layout v2)

- **The plan is 50 lower** (centre y 526), so bodyguard 2 can reach bay 7 from behind the car.
- **The burn mark is bigger and darker** (`BURN_R` 30, a black centre): neither cold viewer saw it in the last frame.
- **The car can tilt on its stands** (`tilt`, used in 0.8).
- The sheets are `of_*_v4.png`; v2 and v3 are kept.
