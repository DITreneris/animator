# UptimeZ Inc. — Episode 10: *First Search* — the film as built (v35)

UptimeZ Inc. · episode 10 · 21 Nov. This is the record of the film as it stands: every shot with its time and line. Script v10 (`first-search-script-v10.md`) was the plan the film started from; the film grew past it in production (the threat and the court, the post, the lipstick, the flashback, the huddle), so for what is on screen, this file is current. Scripts v1–v10 are kept.

- **Film:** `fs_film35_540.mp4` (committed), `fs_film35_1080.mp4` (rebuilt, not committed). 62.9 s, 1886 frames, 1080×1920, 30 fps, BT.709.
- **Builder:** `src/fs_film35.py` (`python3 fs_film35.py ../first-search 1080`; `FS_ONLY=C,U` renders only those shots to `fs_test35_<shots>_<res>.mp4`). Every earlier builder, `fs_film5.py` … `fs_film34.py`, is kept, and each version is a copy of the one before with asserted patches.
- **Voices:** `src/fs_voices/film_v13` (Kokoro). **Timing:** `fs_timing_film35.json`.
- **QA (v35):** −15.2 LUFS, peak −2.2 dBFS; Whisper hears every line (the windowed check scores "Zero results." 1/3 because its window catches "Ask the machine." too; heard alone it passes); the last frame leads into frame 0, and only the calendar differs (MON 1 / MON 8).
- **Cold tests:** two fresh viewers on v29 and on v32 told back the whole story (the blueprint, the guarantee, the $999, the post, the green zero, the plaster, "hussy", the bump, STUPID, the shredded plan, the court, the loop).

## The episode in one line

The Client needs his blueprint by Friday. Don sells him a guarantee, takes his $999, posts the win, and has the robot paint the empty search result green; everyone fixes the surface (the plaster, the green, the tape, Mom's licked thumb), and the Client walks out to sue. On Monday the portrait is whole again and Don is smiling under it.

## Shot by shot

| Time | Shot | What we see | Line |
|---|---|---|---|
| 0:00.0 | A open | MON 1. Don smiling under OUR FIRST CLIENT, the shredder beside him; the lift bell. The frame holds 0.45 s, the camera pans to the glass door; the Client walks in; the slam drops the portrait on Don's head (stars) and back onto its nail, crooked; Sofía comes in during the pan | — |
| 0:04.3 | S flirt | Sofía's heart-eyes for the Client | — |
| 0:05.0 | B | The Client, close | CLIENT: Friday, the bank. I need my blueprint. |
| 0:07.7 | C | Don holds the tablet PREMIUM · GUARANTEED BY FRIDAY at his chest, a hand on each edge, and pushes it at us on "Guaranteed" | DON: Garage eleven. Guaranteed by Friday. |
| 0:11.1 | D0 tap · D1 payok | Don's hand holds out the card terminal; the Client's card comes down; beep, green, $999 | — |
| 0:12.5 | PH photo | The robot photographs Don with the Client (flash) | — |
| 0:14.0 | M1 post | The post goes up: OUR FIRST CLIENT · PAID · $999 | — |
| 0:15.3 | D paid | The Client, unimpressed | CLIENT: Friday. Or I sue. |
| 0:17.2 | E0 red | "blueprint" typed into UptimeZ Find: 0 RESULTS, red | — |
| 0:18.5 | E fright · nothing | The portrait's glass is cracked; Sofía says it | SOFIA: It found nothing. |
| 0:20.2 | F | Don at the robot; the robot holds its paddle | DON: Can you make the zero green? · ROBOT: Interface change. Human approval required. · DON: Approved. |
| 0:25.9 | G wipe | The green sweeps over the zero; the robot's hand holds the green paddle | — |
| 0:27.0 | L machines | Mom at her desk (ASSISTANT TO DON, WORLD'S BEST MOM), lips moving | MOM: Machines. |
| 0:28.3 | E2 plaster | Sofía, on a chair, sticks a plaster over the crack | — |
| 0:29.2 | N like · M comments | Mom hearts the post; the comments: Pam's, then Sofía's (open-to-work ring) "Congrats Don!!" | PAM: Some post. Others tape. |
| 0:32.2 | L2 hussy | Mom, chin down to her phone | MOM: That hussy. |
| 0:33.5 | N3 zoom · youngman | She pinches the photo up to the bump on Don's head | MOM: Young man. |
| 0:35.9 | O round … O5 scrub | She marches him over, licks her thumb (mouth close-up), and scrubs the bump off | — |
| 0:39.8 | P eww | Pam and Sofía | PAM+SOFIA: Eww. |
| 0:41.1 | T week | The search retries: 0 RESULTS slides up, RETRY UNTIL FRIDAY with a spinner | — |
| 0:42.2 | T2 write | Pam writes STUPID in lipstick on the robot's back; beside the portrait the calendar drops its days, MON to FRI | — |
| 0:44.5 | RET | The retry screen | — |
| 0:45.4 | H | Friday. The Client is back | CLIENT: Where's my blueprint? |
| 0:47.5 | I glance · J memory | Don glances at the shredder; LAST WEEK: the plan going into it | — |
| 0:49.4 | X huddle | Don, then Sofía; the robot answers | DON: Where is his blueprint? · SOFIA: Ask the machine. · ROBOT: Zero results. |
| 0:53.5 | Q hug | Mom arm in arm with Pam; a heart rises and fades | MOM: Pam has a plan. |
| 0:55.2 | R show · R1 plancu | Pam holds the taped plan at her waist in her two hands; the close-up: crooked strips, tape, confetti, bay 7 a hole | — |
| 0:56.9 | R2 fury | The Client, red | CLIENT: See you in court. |
| 0:58.3 | OUT leave | He walks out (drawn from behind); the door slams | — |
| 1:00.2 | U heal | Close-up: the crack closes under the plaster, the plaster falls, the glass is whole; the portrait lifts an eyebrow | — |
| 1:01.4 | U zero · shake | The camera pulls back (0.65 s) to frame 0's shot; FRI drops off the calendar: MON 8; Don smiling | — |

## Running props

- **The calendar** (from v30) hangs between the portrait and the desk, and nowhere else: a red header with a spiral, the day in three big red letters, the date big and dark (readable at 270 px). MON 1 at frame 0, MON 8 at the end. The week shot has no calendar; the STUPID shot shows the portrait's frame at its edge, so it is the same wall.
- **The portrait:** clean at frame 0; cracked by the slam; plastered by Sofía; the crack heals under the plaster in the close-up at the end.
- **The bump** on Don's head from the portrait: in the photo, in Mom's zoom, scrubbed off by her thumb.

## Hand-off to episode 11 (One Star, `customer-success/`)

Decided 21 Nov; not yet made in episode 11's files:

1. **The calendar** hangs right of the portrait, between it and the desk (`cs_board.calendar_on()` puts it left, by the door).
2. **The same drawing** as episode 10's (`calendar()` in `src/fs_film35.py`); best moved into a shared module, so both episodes draw from one source.
3. **The date** on the calendar is whatever day episode 11 opens on, shown big (the day and the number), and the phone's calendar (2.2) agrees with it.
4. `cs_props.py`: "new to the set in ep 11" becomes "from ep 10". Script v12's calendar line: "right of the portrait, by the desk", with the date.
5. **Episode 11 picks up after the court threat** (decided 21 Nov). Episode 10 already shows the Client Pam's taped plan and ends on "See you in court."; episode 11 starts after it, whenever its story needs, and its handing-over of the plan is the plan he has already seen. Episode 10 stays as it is.

## How it got here (film versions)

- **v5–v16:** the board becomes a film: 15 drawings a second for acting, a 30 fps camera, voices, breaths and blinks, the lift bell at 0:00, the loop.
- **v17–v24:** the client threatens ("Friday. Or I sue.", "See you in court."); how he pays (the terminal, after The Onboarding); the robot's photo and Don's post; Pam's line recorded; STUPID on the robot's back; the client leaves drawn from behind (a fade read as a ghost).
- **v25–v27:** Mom's lips at her desk, the payoff in Pam's two hands, the close-up of the plan (both lost to a map override until v34 and v35, see below).
- **v28–v30:** the crack heals on screen; the sign at Don's chest; one text at a time on the retry screen; Mom's lean halved; the pinch on her phone; the loop's sound; the calendar redrawn and given one place.
- **v31–v32:** frame 0 holds 0.45 s; the paddle held; the STUPID shot pulled back; trims from 65.6 s to 62.2 s.
- **v33–v35:** Pam's arm drawn as an arm; the thumb's white flash removed; the post and comments longer; v27's payoff and v25's desk shot restored.
