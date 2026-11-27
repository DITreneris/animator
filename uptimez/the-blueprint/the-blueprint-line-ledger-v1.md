# The Blueprint — line ledger v1

Three buckets. Inherit means the words match a kept take and the mouth will be refit because the hold is longer than the take. The mix of episodes 9–11 is not reused. No wav files are stored next to these JSON takes (`ob_voices/film/` is the timing file only), so the rough cut carries room tone, not the dry takes.

## Inherit

| Line | Who | Take | Take length |
|---|---|---|---:|
| Ten garages. And I keep losing this. | CLIENT | `src/ob_voices/film/takes.json` key 3.1 | 2.523 s |
| Does your missus love your garages? | SOFIA | same, 3.2 | 1.850 s |
| I live alone. | CLIENT | same, 3.3 | 0.934 s |
| Oh... | SOFIA | same, 3.7 | 0.658 s |
| Can it find this when I lose it? | CLIENT | same, 3.12 | 1.704 s |
| Here, you will never lose anything again. | DON | same, 4.1 | 2.287 s |
| We'll take care of it. | DON | same, 4.3 | 1.158 s |
| One month. I ask, you find it. | CLIENT | same, 5.4 | 1.941 s |
| Approved. | DON | same, 5.5 | 0.718 s |
| FIRST CUSTOMER. CELEBRATION REQUIRED. | ROBOT | same, 8.1 | 1.999 s |
| SOFÍA! WE HAVE A CUSTOMER! | DON | same, 8.3 | 1.800 s |
| Some shit, others scoop. | PAM | `src/ob_voices/film_v10/takes.json` key 9.1 | 1.482 s |
| ONBOARDING COMPLETE. | ROBOT | `src/ob_voices/film/takes.json` key 10.4 | 1.216 s |
| Friday, the bank. I need my blueprint. | CLIENT | `src/fs_voices/film_v13/takes.json` key 1.2 | 2.492 s |
| Garage eleven. Guaranteed by Friday. | DON | same, 2.2 | 2.544 s |
| Friday. Or I sue. | CLIENT | same, t1 | 1.586 s |
| It found nothing. | SOFIA | same, 3.3 | 0.852 s |
| Can you make the zero green? | DON | same, 4.1 | 1.766 s |
| Interface change. Human approval required. | ROBOT | same, 4.2 | 2.296 s |
| Approved. | DON | same, 4.3 | 0.718 s |
| Where's my blueprint? | CLIENT | same, 5.2 | 1.390 s |
| Where is his blueprint? | DON | same, x1 | 1.276 s |
| Ask the machine. | SOFIA | same, x2 | 0.868 s |
| Zero results. | ROBOT | same, x3 | 1.042 s |
| Young man. | MOM | same, 7.1 | 1.295 s |
| See you in court. | CLIENT | same, t2 | 1.107 s |
| Paid $999. They lost my blueprint. My lawyer will call. | CLIENT | `src/cs_voices/film_v9/takes.json` key 1.2 | 4.816 s |
| Reply drafted. Human approval required. | ROBOT | same, 1.4r | 2.368 s |
| Approved. | DON | same, 1.4d | 0.718 s |
| Stupid human. | DON | same, 1.4b | 1.169 s |
| Is this a joke? | CLIENT | same, 3.5 | 1.074 s |
| Check your pocket. | PAM | same, 4.2p | 1.080 s |
| The result was obtained by a h-human. | ROBOT | same, 4.4 | 2.180 s |
| Your number. | CLIENT | same, 5.1 | 0.813 s |
| Customer success. | DON | same, 5.4d | 1.357 s |
| Some post. Others find. | PAM | same, 6.3p | 1.687 s |
| Still one star. | SOFIA | same, 6.5 | 0.875 s |

`ob_voices/film/takes.json` has no Pam line. The scoop that shipped is key 9.1 in `film_v10` and in `ob_anim_timing_v19.json`. That is the take to inherit.

Friday-or-I-sue and the First Search "Approved." share files with other lines. The ledger matches on the text above, not on a guessed duplicate key. `bp_scenes.py` records the same paths.

## New — night scene only

No takes. Record after a Kokoro licence decision if this cut is a public master. A local rough cut may use them later. This pass does not record them.

| Line | Who |
|---|---|
| Put recovered on it. | SOFIA |
| Recovered from what? | PAM |
| He needs a page by Friday. | SOFIA |
| He needs the bays. | PAM |
| I won't draw one. | SOFIA |
| I'm matching them. | PAM |

## Silent

The week (retries, lipstick, calendar, deleted message). Sofía's closed mouth when the zero turns green. The look from Sofía to Pam after "Still one star." The CUSTOMER SUCCESS stamp.

## Cut

Listed in `the-blueprint-shot-list-v1.md`. Those takes stay in their episode files and are not called.
