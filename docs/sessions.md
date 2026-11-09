# Work log

What has been made so far, chat by chat, and what is in this repo. Dates are 2026.

| Dates | Session | Output | In repo |
|---|---|---|---|
| 3–4 Nov | **Video skill research → Payday Slot Machine** | Studied `claude-video-effects`; wrote the `video-creator` skill; five concepts for the "Choose your career" meme; *Payday Slot Machine* (19 s, slot reels per career, synthesized SFX); skill revised after review (reveal timing, BT.709 colour, audio headroom, honest checks) | Payday Slot Machine ✅ (added 7 Nov) · skill — not code |
| 3–6 Nov | **Payday Slam → The List** | *Payday Slam* (17 s, meme table animated, synthesized music and SFX). Reworked as *The List*: one screen, doodle faces, your recorded voice lines, jaw-drop punchline "Wait, you guys are getting paid?" | Payday Slam ✅ · The List ✅ |
| 3–6 Nov | **"Says Here You Were Our Boss"** | Five concepts, winner combines the interview cold open with a loop ending and a hidden detail; lessons saved to the `viral-loop-animation` skill | ⏳ |
| 5 Nov | **Choose Your Career SFX** | `choose_career_reveal_sfx.mp4`: stamps, coin pings, jackpot, error buzzes and deflate cued to each panel; −14.4 LUFS. 9:16 cut (meme raised 100 px) added with the repo upload | ✅ |
| 6 Nov | **Chat GIF sound design** | *Emma Blocked* and *Babe / Voice Agent* re-timed from ~20 s to 13–15 s, cropped and filled to 9:16, sharpened, chat SFX with music that tape-stops at the punchline; lessons saved to the `viral-loop-animation` skill | ✅ |
| 6–7 Nov | **Futuristic concepts → UptimeZ Inc.** | Concepts *Elevator 2077: "Saved Locally"*, *The Infinite Archive*, *Sandbox Moon*. *Saved Locally* v1–v3 (retired: nobody knew what SAVI was). *Where Files Live* storyboards S1/S3 with ending variants. *Prompt Telephone* v03 A/B → v04.1 → v04.2 (renamed **UptimeZ Inc.**, logo, tagline "99.9% uptime. 0% findability.", company post card) → v04.3 (bigger opening speaker, lip-sync, louder mix at −14.5 LUFS). Design System artifact, character sheets, two tester packs in Claude Docs | ✅ `uptimez/` |
| 7–8 Nov | **UptimeZ: Saved to Cloud** | S1v2 frames reviewed → S1v3 concept (Claude Docs) → outside review → S1v3.1 A/B → B extended to 21.5 s with an animation pass → cold open + rewind + emoji name tags → doodle payoff → S1v3.6 polish and remix, first 1080×1920 release | ✅ `uptimez/saved-to-cloud/` |
| 8–9 Nov | **UptimeZ: Downloads Expedition** | Concept doc (Claude Docs) → three outside reviews → v1 A/B → v2–v4 (emoji tags, salute, exterior tower ending, impact frames) → fourth review put v4 on HOLD (props crossing faces, floating hat, stray beam) → v5 rebuilt with props parented to bodies and automatic eye/prop/bubble-tail checks, 1080×1920 release and cover thumbnail → v6 polish (tighter hold, MAX reaction, helmet tug, smear, shorter beard) → v7–v10 review rounds (no ghost copies, arm behind the head, RUMBLE off the building, FINAL (29) loop object, BT.709 tags, brand card behind `TAG=1`; PAM now asks the first line, both tails on open mouths) | ✅ `uptimez/downloads-expedition/` (v10 current) |
| 3–6 Nov | **Robot office episodes** (one long chat) | *Says Here You Were Our Boss* v1 + v2 (voices, sunglasses payoff); *He Always Said Thank You*; *Make It Better* v1 + v2; *Just For Now* test clips, rough and v2 after two tester reviews. Lessons in [`lessons.md`](lessons.md) | ✅ |
| 7 Nov | **The List added** | `the-list/`: source, six trimmed voice lines, Permanent Marker font, history stills; rebuild matches the released video exactly | ✅ |
| 4–7 Nov | **Repo setup** | This repo: structure, build docs, Anton font + OFL, first push | ✅ |

## Next ideas

- **Just For Now**: viewer test of v2 (two laughs? tape rule clear?), then better faces and motion
- **Make It Better / Says Here**: swap in real recorded voice lines

- **Who Gets…? series**, same format as *The List*: *Who Gets Sleep?*, *Who Gets Weekends?*, *Who Gets Customers?*
- **Vibe Coder Learns**: *Backups*, *Security*, *The Bill*
- **Downloads Expedition**: viewer test of v6 (does the 3 → 27 → 28 count get noticed? laugh at the THUNK or at "Downloads."?)
- **UptimeZ Inc.**: v04.3 viewer test (does the opening read? laugh at BALD or at "A post about me."?), then a 1080×1920 release cut and the extended ~25 s version
- **UptimeZ branding of the earlier cuts**: undecided; v04.2 onwards are already branded

## Missing from the repo

Code, renders and voice recordings for everything marked ⏳ live in earlier chat sessions or on your computer. To add them, attach the files in a chat or reconnect the computer that holds them.
