# UptimeZ Inc. — document index

A map of every document in `uptimez/`, so a person, worker or agent can find the right source without reading the whole repo. If two documents disagree, the one higher in **Read first** wins.

## Read first, in this order

| # | Document | What it's for | Authority |
|---|---|---|---|
| 0 | [`CANON.md`](CANON.md) | **Where the current canon is:** scenes (the set pages and locked stills), character looks, and the hand class sheet with how a row changes | Map. The page it links wins |
| 1 | [`STORYLINE.md`](STORYLINE.md) | **The series bible (v3.4).** Premise, world rules (why Find returns 0), the four leads (want, private lie, contradiction, silent reaction, moral line), the supporting cast, relationships, Season 1 in four acts (including physical *Civil War*), episode rules, canon locks | **Canon.** Overrides anything older |
| — | [`series/production-process.md`](series/production-process.md) | v1, current (22 Nov): how an episode goes from script to final film; stages, checks, Tomas's five stops, version budgets | Process |
| — | [`gates-v2-plan.md`](gates-v2-plan.md) | v1 (23 Nov): the four measured gates (`src/gates_os.py`) — **GV** shot variety, **GP** proportions, **GD** depth and volume, **GH** hands | Gates |
| 2 | [`CLAUDE.md`](CLAUDE.md) | **How to work here:** gates, production rules, QA, rules for bubbles and tails, how Tomas wants decisions asked | Process |
| 3 | [`README.md`](README.md) | Cast table, brand, every episode (synopsis + files + how it's built) | Episode facts |
| 4 | [`../docs/rules-hands-and-phones.md`](../docs/rules-hands-and-phones.md) | The hand for every film: one job table (`quiet`, `point`, `grab`, `clutch`, `pinch`, `phone_grip`, …), then the drawing rules. History stays at the bottom. A new job is a new row on this page | Craft rules |
| 5 | [`../docs/lessons.md`](../docs/lessons.md) | What went wrong before and the rule it produced, by episode | Craft rules |
| 6 | [`../docs/sessions.md`](../docs/sessions.md) | Work log for the whole repo: what each session made and what's in the repo | History |

## Series development

| Document | Contents |
|---|---|
| [`STORYLINE.md`](STORYLINE.md) | v3.4, current (23 Nov): *Civil War* made physical ($49,999 throne, floor tape line, 0:01 physical joke); v3.3 (22 Nov): Act D *Civil War* (episodes 13–17); v3.2 (17 Nov): Act B around the blueprint |
| [`series/front-desk-set.md`](series/front-desk-set.md) | The front desk set v4: zones A/B/C, depth, home positions, the way out from behind the counter, camera setups S1–S6; the room from episode 10 on. **9:16 only** |
| [`the-blueprint/set-16x9.md`](the-blueprint/set-16x9.md) | **16:9 source of truth** for *The Blueprint* room, locked 25 Nov 2026. Stills `the-blueprint/stills/bp_still_s0.png`. Night still approved the same day. Progress: [`the-blueprint/changelog.md`](the-blueprint/changelog.md). Drawing audit: `/quality-assurance-agent`, checker [`src/bp_draw_audit.py`](src/bp_draw_audit.py). Checklist: [`the-blueprint/todo.md`](the-blueprint/todo.md). Roadmap: [`the-blueprint/16-9-developing.md`](the-blueprint/16-9-developing.md) |
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
| — | *Office Noir 2: The Shadow of Fate* (New Year special) | [`office-noir-2/`](office-noir-2/) | `office-noir-2-script-v6.md` (current, release v28); concepts v1–v4; README section |
| 8 | *The Best Candidate* | [`the-best-candidate/`](the-best-candidate/) | `the-best-candidate-interview-script-v1.md` … `v6.md` (v6 is current) |
| 9 | *The Onboarding* | [`the-onboarding/`](the-onboarding/) | `the-onboarding-script-v11.md` (current, line by line with the shot list; animation v12–v19 changes are in `src/ob_anim.py`); concepts v1–v9; `storyline-proposal-act-b.md` (STORYLINE v3.2 decides). Release: `uptimez_ob_anim_v19.mp4` (+ cover `ob_cover_v1.png`) |
| 10 | *First Search* | [`first-search/`](first-search/) | `first-search-film-v35.md` (current: the film as built, shot by shot); film `fs_film35_540.mp4` (62.9 s; `fs_film36`–`v37` tail/limb fixes in `src/`); scripts v1–v10, concepts v1–v6 and premises v1–v3 kept |
| — | *Office Noir 3: The Last Round* (Client's dream, between 10 and 11) | [`office-noir-3/`](office-noir-3/) | `office-noir-3-script-v73.md` (current; v1–v72 kept); `office-noir-3-concept-v1.md`; `ring-set.md`. Release: `office_noir_3_release_v6_540.mp4` (87.2 s; native 1080 rebuilt by `src/on3_native.py`), `on3_cover_v1.png` |
| 11 | *One Star* (working title: Customer Success) | [`customer-success/`](customer-success/) | **Master:** `one_star_master_v13_540.mp4` + `one_star_cover_v1.png` (`one-star-master-v13.md`, 61.3 s); `one-star-shot-list-v19.md`; `one-star-gates-v19-r2.md` (GV/GP/GD/GH pass); `customer-success-script-v18.md` |
| 12 | *Daddy's Home* | [`daddys-home/`](daddys-home/) | `daddys-home-script-v2.md` (current, generated from the eight scene sheets); `daddys-home-fix-plan-v1.md`, `daddys-home-bubble-lessons-v1.md`, `daddys-home-restaging-lessons-v1.md`; animation `daddys_home_anim_v7.mp4` (v8 scenes 3–4 restaged in `src/`; <90 s trim & 1080 master pending) |
| 13 | *The Offer* (Civil War 1 of 5) | [`the-offer/`](the-offer/) | `the-offer-script-v6.md` (current, **generated** from `src/of_scenes.py`); `the-offer-set-v2.md`; unified phone UI `src/of_ui.py` (v39); `of_roughcut_v30_540.mp4` (master & cover pending) |
| 14 | *Pick a Side* (Civil War 2 of 5; board and tests, no film yet) | [`pick-a-side/`](pick-a-side/) | `pick-a-side-script-v9.md` (current, **generated** by `src/ps_scenes.py script v5`: 38 shots, 66.3 s, HR? in place of COO?; v8 is board v3's; v1–v7 by hand); concept v3.2 (approved) with v1–v3.1; `pick-a-side-plan-v1.md` (the stage plan, with its status table); `pick-a-side-tests-v1.md` (the checks, the board cold tests, rounds 1–4, motion tests A–G, Tomas's decisions). Board `ps_board_v3_1.png`, `ps_board_v3_2.png`; layouts `ps_layout_s*_v3.png` (approved; v4 only under the board's `FIX_V4`); motion tests `ps_motion_A` … `K` (H–K: review round 1); animatic `ps_animatic_v1.mp4` (540, not committed); `pick-a-side-animation-plan-v1.md` (stage 7); hands/phones audit fixes (`8eee4b1`) |
| 15 | *The Double Agent* (Civil War 3 of 5; concept stage) | [`the-double-agent/`](the-double-agent/) | `the-double-agent-concept-v3.md` (current; v1–v2 kept, with two outside reviews triaged); the establishing frame `da_establish_v3.png` (+ `_world`) drawn by `src/da_set.py` on front desk v4 + 14's `ps_set` (new: DON's office glass in zone C); `da_coldtest_establish_v3.md` (3 viewers: premise 3/3, Don read as a robot 0/3) |
| — | *Office Noir 4: Seven Lives* (Pam's Valentine's dream special) | [`office-noir-4/`](office-noir-4/) | `office-noir-4-script-v16.md` (current, **generated** from `src/on4_scenes.py`); `office-noir-4-concept-v2.md`; `on4_coldtest_*.md`, `on4_motiontest_v*.md`; roughs `on4_rough_v1.mp4` … `v13` (68.9 s+); final animation groups 1–3 stills & 24 drawings/s (`sub=2`) motion tests |
| — | *The Blueprint* (16:9 pilot, Act B) | [`the-blueprint/`](the-blueprint/) | **Set SOT:** `set-16x9.md` (locked 25 Nov). **Picture:** `bp_pic_v4.mp4` (400 s, watched 27 Nov). **Sound:** `bp_sound_v3.mp4` still on `bp_pic_v3.mp4` (400 s, local only; note `rough/bp_pic_v3_note.md`). **Next:** `bp_pic_v5` clutch hands. `bp_sound_v1.mp4` is the silent rough-v5 picture with the same takes. Checklist: `todo.md`. Roadmap: `16-9-developing.md`. Progress: `changelog.md`. Paper cut: `the-blueprint-shot-list-v1.md`, `the-blueprint-line-ledger-v1.md`, `the-blueprint-script-v1.md`, `the-blueprint-cutdown-v1.md`. Locked stills: `stills/bp_still_s0.png`, `bp_still_shred.png`, `bp_still_counter.png`, `bp_still_night.png`. `bp_rough_v1.mp4` is the old room |
| — | *Saved Locally* (retired) | [`history/saved-locally/`](history/saved-locally/) | its own README |

## Characters and brand

| Document | Contents |
|---|---|
| [`characters/README.md`](characters/README.md) | Every model sheet and phone check, per episode look (`*-ss-*` Secret Santa, `*-mf-*` Mandatory Fun, `*-tg-*` Thanksgiving, `*-xmas-*` Christmas, `*-on-*` Office Noir) |
| [`brand/README.md`](brand/README.md) | Logo files and lockups. The full design system is the *UptimeZ Inc.* Design System artifact on claude.ai |

## Code (`src/`)

Each episode has its own file prefix. Existing `_v1`, `_v2`… files stay untouched and must still rebuild byte for byte; from 24 Nov on, **new episodes pin approved versions with immutable `git tag`s** (plus opt-in flags on shared modules) instead of copying whole `_vN.py` files in `src/`.

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
| `*_xmas*`, `xmas_*`, `santa_robot`, `sound_xmas` | Happy Compliance (v2: `xmas_anim2`, `xmas_pam3`; final: `xmas_anim11`) | `build.sh xmas`, `xmas2`, `xmas_final` |
| `*_on`, `on_*`, `engine_on`, `sound_on*`, `thumb_on` | Office Noir | `build.sh on` |
| `on2_*`, `noir2_cast`, `thumb_on2` | Office Noir 2 | `build.sh on2` |
| `*_bc`, `bc_*`, `cand_bc`, `qa_bc*`, `sound_bc*` | The Best Candidate | `build.sh bc` |
| `*_ob`, `ob_*`, `client_ob`, `qa_ob*`, `sound_ob*`, `thumb_ob` | The Onboarding | `build.sh ob` |
| `fs_*`, `sound_fs*`, `thumb_fs` | First Search | `python3 fs_film35.py ../first-search 1080` |
| `*_on3`, `on3_*`, `film_on3*`, `board_on3`, `on3_native` | Office Noir 3 | `python3 on3_native.py` |
| `cs_*`, `gates_os` | One Star (ep. 11) | `python3 cs_film_v13.py ../customer-success`, `python3 gates_os.py` |
| `dh_*`, `gates_dh`, `dh_tailcheck` | Daddy's Home (ep. 12) | `python3 dh_film_v7.py 1..8`, `join` |
| `of_*`, `client_of`, `of_ui` | The Offer (ep. 13) | `python3 of_scenes.py`, `of_sound.py` |
| `ps_scenes` (the one source: `check`, `board`, `script`), `ps_checks`, `ps_text`, `ps_set`, `ps_motion`, `ps_voices`; pinned `ps_scenes_v3`, `ps_motion_v3` | Pick a Side (ep. 14) | `python3 ps_scenes.py check\|board\|script`, `python3 ps_motion.py` |
| `on4_*` | Office Noir 4 | `python3 on4_scenes.py`, `python3 on4_motion.py` |
| `bp_frame`, `bp_set`, `bp_scenes`, `bp_picture`, `bp_sound`, `bp_voices`, `bp_draw_audit` | The Blueprint (16:9). The set is locked in `the-blueprint/set-16x9.md`. Picture and mix are opt-in; a bare `bp_scenes` / `bp_sound` mix still rebuilds the silent rough and `bp_sound_v1` | `python3 bp_scenes.py stills`, `python3 bp_picture.py`, `python3 bp_sound.py` |
| `kit`, `hands_ps`, `speech`, `speech_gate`, `hand_gate`, `charsheets`, `brand`, `engine`, `engine_hd`, `anim`, `emoji`, `uz_check` | Shared: drawing kit, series hand, shared bubble drawer & gates, sheets, logo, frame engines, checks | `build.sh sheets`, `python3 speech_gate.py`, `python3 hand_gate.py`, `python3 uz_check_validate.py` |

**QA workers and gates** (each exits non-zero on a miss): `speech_gate.py` (`selftest`), `hand_gate.py` (`selftest`), `uz_check.py` (+ `uz_check_validate.py`), `bp_draw_audit.py` (Blueprint 16:9 cameras; `--plant` must fail; `--lines --picture` is a picture-pass check; the hand pass is `--grips`, and `--grips --plant` must fail; `--hands` only measures pose boxes), `gates_os.py` (GV shot variety, GP proportions, GD depth/volume, GH hands; One Star, report), `gates_dh.py`, `ps_checks.py`, `qa_dlx.py`, `qa_iwry.py`, `qa_bc.py`, `qa_ob.py` and `qa_ob_speech.py`, and `on_qa.py` (Office Noir: the full G5 standard in [`CLAUDE.md`](CLAUDE.md), including speech recognition; `--selftest` runs every check on a known failure). A still is looked at with `/quality-assurance-agent`. Episode render checks live in each episode's README section.

## Where things are *not*

- **Voices:** the kept takes are in `src/*_voices/` or `src/*_takes/`. Re-recording needs the Kokoro model files in `src/models` or `KOKORO_DIR`.
- **1080 renders** from 17 Nov on: not committed (`.gitignore`); rebuild with `build.sh <episode>`. Older 1080 files are still in the repo.
- **Speech-recognition model** for QA: Whisper base.en through sherpa-onnx, kept outside the repo.
- **Outside reviews** are summarized in each episode's lessons and in STORYLINE.md's history; the raw review files are not stored.
