# UptimeZ Inc. — document index

A map of every document in `uptimez/`, so a person, worker or agent can find the right source without reading the whole repo. If two documents disagree, the one higher in **Read first** wins.

## Read first, in this order

| # | Document | What it's for | Authority |
|---|---|---|---|
| 1 | [`STORYLINE.md`](STORYLINE.md) | **The series bible.** Premise, world rules (why Find returns 0), the four leads (want, private lie, contradiction, silent reaction, moral line), the supporting cast, relationships, Season 1 in three acts, episode rules, canon locks | **Canon.** Overrides anything older |
| 2 | [`CLAUDE.md`](CLAUDE.md) | **How to work here:** gates, production rules, QA, rules for bubbles and tails, how Tomas wants decisions asked | Process |
| 3 | [`README.md`](README.md) | Cast table, brand, every episode (synopsis + files + how it's built) | Episode facts |
| 4 | [`../docs/lessons.md`](../docs/lessons.md) | What went wrong before and the rule it produced, by episode | Craft rules |
| 5 | [`../docs/sessions.md`](../docs/sessions.md) | Work log for the whole repo: what each session made and what's in the repo | History |

## Series development

| Document | Contents |
|---|---|
| [`STORYLINE.md`](STORYLINE.md) | v3.1, current (17 Nov): v3 plus Act B rebuilt around the Client's blueprint |
| [`series/storyline-v3.md`](series/storyline-v3.md) | v3: after three outside showrunner reviews (character engines, relationships, world rules) |
| [`series/storyline-v1.md`](series/storyline-v1.md) | v1: the first canon cleanup (early cast as prequel shorts; one promoted robot; Mom hired; Sofía flirts upward; calendar order; the one-client spine) |
| [`series/storyline-v2.md`](series/storyline-v2.md) | v2: goals that collide, Don can sell, the robot's permission rule, episodes 9–11, *The Human Algorithm* finale planned |

## Episode documents

Episodes in **story order** (STORYLINE.md, Season 1). Each folder holds its renders (`*.mp4`), sheets (`*.png`) and covers; the README section says which file is the current release.

| # | Episode | Folder | Scripts and notes |
|---|---|---|---|
| — | *Prompt Telephone* (prequel short) | [`prompt-telephone/`](prompt-telephone/) | `scenario_v01.md` … `scenario_v04_2.md` |
| — | *Saved to Cloud* (prequel short) | [`saved-to-cloud/`](saved-to-cloud/) | README section |
| — | *Downloads Expedition* (prequel short) | [`downloads-expedition/`](downloads-expedition/) | README section |
| — | *Where Files Live* (storyboards) | [`storyboards/`](storyboards/) | README section |
| 1 | *How Sofía Survived Day One* | [`sofia-day-one/`](sofia-day-one/) | README section |
| 2 | *I Will Replace You* | [`i-will-replace-you/`](i-will-replace-you/) | README section |
| 3 | *Raises for Everyone* (Thanksgiving) | [`raises-for-everyone/`](raises-for-everyone/) | README section |
| 4 | *Mandatory Fun* | [`mandatory-fun/`](mandatory-fun/) | README section |
| 5 | *Secret Santa* | [`secret-santa/`](secret-santa/) | README section |
| 6 | *Happy Compliance* (Christmas Eve) | [`happy-compliance/`](happy-compliance/) | README section |
| 7 | *Office Noir: The Secret of a Stolen Heart* | [`office-noir/`](office-noir/) | README section |
| 8 | *The Best Candidate* | [`the-best-candidate/`](the-best-candidate/) | `the-best-candidate-interview-script-v1.md` … `v6.md` (v6 is current) |
| 9 | *The Onboarding* | not in the repo yet | Concepts v1–v4 are in the claude.ai chat "The Onboarding". STORYLINE v3.1 keeps concept v4's blueprint ending, with one change: the Client pockets the strip without looking |
| 10 | *First Search* | [`first-search/`](first-search/) | `first-search-premise-v2.md` (current, the blueprint); v1 (the van) kept |
| — | *Saved Locally* (retired) | [`history/saved-locally/`](history/saved-locally/) | its own README |

## Characters and brand

| Document | Contents |
|---|---|
| [`characters/README.md`](characters/README.md) | Every model sheet and phone check, per episode look (`*-ss-*` Secret Santa, `*-mf-*` Mandatory Fun, `*-tg-*` Thanksgiving, `*-xmas-*` Christmas, `*-on-*` Office Noir) |
| [`brand/README.md`](brand/README.md) | Logo files and lockups. The full design system is the *UptimeZ Inc.* Design System artifact on claude.ai |

## Code (`src/`)

Each episode has its own file prefix; earlier versions are kept as `_v1`, `_v2`… and must still rebuild byte for byte.

| Prefix | Episode | Entry points |
|---|---|---|
| `pt*`, `sound_pt*` | Prompt Telephone | `build.sh pt43` |
| `s13*`, `sound_s13*` | Saved to Cloud | `build.sh s131a` … |
| `dlx*`, `qa_dlx`, `sound_dlx` | Downloads Expedition | `build.sh dlx` |
| `day1_*`, `sofia`, `sound_day1*`, `thumb_day1` | Day One | `build.sh day1` |
| `iwry_*`, `cafe_kit`, `waiter_kit`, `qa_iwry`, `sound_iwry` | I Will Replace You | `build.sh iwry`, `iwry_anim` |
| `*_tg`, `tg_*`, `sound_tg` | Raises for Everyone | `build.sh tg` |
| `*_mf`, `mf_*`, `sound_mf*` | Mandatory Fun | `build.sh mf` |
| `*_ss`, `ss_*` | Secret Santa | `build.sh ss` |
| `*_xmas*`, `xmas_*`, `santa_robot`, `sound_xmas` | Happy Compliance (v2: `xmas_anim2`, `xmas_pam3`) | `build.sh xmas`, `xmas2` |
| `*_on`, `on_*`, `engine_on`, `sound_on*` | Office Noir | `build.sh on` |
| `*_bc`, `bc_*`, `cand_bc`, `qa_bc*`, `sound_bc*` | The Best Candidate | `build.sh bc` |
| `kit`, `charsheets`, `brand`, `engine`, `engine_hd`, `anim`, `emoji` | Shared: drawing kit, sheets, logo, frame engines | `build.sh sheets` |

**QA workers** (each exits non-zero on a miss): `qa_dlx.py`, `qa_iwry.py`, `qa_bc.py`, and `on_qa.py` (Office Noir: the full G5 standard in [`CLAUDE.md`](CLAUDE.md), including speech recognition; `--selftest` runs every check on a known failure). Episode render checks live in each episode's README section.

## Where things are *not*

- **Voices:** the kept takes are in `src/*_voices/` or `src/*_takes/`. Re-recording needs the Kokoro model files in `src/models` or `KOKORO_DIR`.
- **1080 renders** from 17 Nov on: not committed (`.gitignore`); rebuild with `build.sh <episode>`. Older 1080 files are still in the repo.
- **Speech-recognition model** for QA: Whisper base.en through sherpa-onnx, kept outside the repo.
- **Outside reviews** are summarized in each episode's lessons and in STORYLINE.md's history; the raw review files are not stored.
