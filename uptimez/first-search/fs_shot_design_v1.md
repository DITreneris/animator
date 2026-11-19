# First Search: shot design v1 (decided 19 Nov; drawn as board v22)

Board v21 is almost all medium shots at eye level, about 1.3 s each. This pass gives each shot a size, an angle and a camera setup (S1–S6 from `series/front-desk-set.md`). It also says what sits in front of or behind the subject in the frame, and whether the shot is a full-screen close-up of an object (an insert) or folded into another shot. It is decided before key poses, so animation only touches timing.

**Rules:**
- Angles only where status moves.
- Over the shoulder only for the two confrontations.
- Inserts only for text that is the joke.
- At most two extreme close-ups.
- Three wides: the opening, the reset before Mom's act, and the loop.

**Sizes:** WS wide · MS medium · MCU medium close-up · CU close-up · ECU extreme close-up · OTS over the shoulder · INS insert.

| Shot | Beat | Size | Angle | Setup | In front / behind | Insert or folded in |
|---|---|---|---|---|---|---|
| 1.1a | The buzz; it jumps off the nail | WS | eye | S1 | the portrait above Don | frame 0 |
| 1.1b | BONK | WS | eye | S1 | | |
| 1.2 | She flirts; he looks past her. CLIENT: "Friday. The bank…" | MS | eye | S3 | Sofía in front, the Client behind | |
| 1.3 | FRIDAY · BANK MEETING | INS (the card fills the frame, his hand under it) | | | | insert: failed at phone size twice |
| 2.1 | Don's eyes light up | MCU | eye | S3 | | |
| 2.2 | DON: "Garage eleven. Guaranteed by Friday." | MS | **low** | S4 | the portrait above him | |
| 2.3 | The thumb taps GUARANTEED | **OTS** (Client onto the tablet) | eye | S3 | the tablet in front, Don behind | replaces the hand insert |
| 3.1 | Red again; he ducks; it holds | MS | eye | S3 | the portrait above | folded in |
| 3.2 | PREMIUM · PAID $999 | MCU | eye | S2 | the phone big | |
| 3.3 | SOFÍA: "It found nothing." | MS two-shot | eye | S3 | | |
| 3.4 | Sofía, on the chair, sticks the plaster on | MS | eye | S3 | | |
| 4.1 | DON: "Can you make the zero green?" | MS | eye | S2 | the robot in front | |
| 4.2 | ROBOT: "Interface change…" | MCU | eye | S2 | | |
| 4.3 | APPROVED | INS | | | | insert (the joke is text) |
| 4.4 | Pam's tape | MS | eye | S6 | Don in front, smug; Pam behind the counter, taping the plan | folded in (replaces the hand insert) |
| 4.5 | The sweep to green | INS | | | | insert |
| 5.1 | The Client finds nothing; Don beams | MS | eye | S3 | | |
| 5.2 | CLIENT: "Where's my blueprint?" | **OTS** (behind the Client, onto Don) | eye | S3 | the Client's shoulder in front | |
| 5.2b | His eyes dart to the shredder | **ECU** | **high** | S4 | the shredder in front | ECU 1 of 2 |
| 5.2c | Flashback to episode 9 | INS | | | | |
| 5.3 | DON: "The zero's green." Pam's plan up behind | MS | **low** | S6 | Pam and the plan behind | folded in |
| 6.1b | MOM: "Machines." | MCU | eye | S5 | | |
| 6.2a/b | The post, the comments | INS | | | | insert |
| 7.1 | MOM: "Young man." | OTS (her cheek, curls, glasses, pearls; the phone big) | eye | S5 | her in front, the phone behind | |
| 7.2 | She comes round the counter's end | MS | **low** | S6 | mid-stride | |
| 7.3 | The lick | CU bust (picked after the v18 cold test) | eye | S6 | Don's head at the edge of the frame | |
| 7.4 | The thumb on his hair; "Eww." | MS three-shot | eye | S3 | | |
| 7.5 | Her arm round Pam; "That hussy." | MS | eye | S6 | | |
| 8.1 | Pam brings the plan; "Pam has a plan." | **WS** | eye | S1 | | the reset |
| 8.2 | The near-shred | MS | eye | S3 | the shredder in front | |
| 9.1 | 100% COMPLETE; he doesn't buy it | MCU | eye | S2 | the phone big | |
| 9.2 | RETRY UNTIL FRIDAY | INS | | | | |
| 9.3 | It heals; nobody notices | CU | eye | | | |
| 9.4–9.5 | Frame 0; the shake | WS | eye | S1 | | the loop |

## Decided (/grill-me, 19 Nov)

- **Angles:** only the four status moves: low on Don at 2.2 and 5.3, high on Don at 5.2b, low on Mom at 7.2. Everything else is at eye level.
- **1.3:** a full-screen insert.
- **4.4:** Pam taping behind Don, in his shot.
- **7.1:** over Mom's shoulder onto her phone.
- **7.3:** stays the close-up bust picked earlier, so 5.2b is the only extreme close-up.

**How the angles are drawn:** a paper world has no 3D camera. The shot is drawn wider than the frame and then keystoned (`_warp` in `fs_storyboard.py`). For a low angle the verticals close in at the top; for a high angle, at the bottom. The heads move with the picture, so the bubbles still find the mouths.
