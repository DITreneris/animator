# ME + MY AI (Hoodyz)

The series about Hoody, his robot MY AI, Eva, the cat and HARV. Title bar "ME + MY AI" with the Hoodyz badge. Every episode is drawn with pycairo and rebuilt from its own folder; voices are Tomas's recordings or Kokoro placeholders.

| Folder | Episode | Status |
|---|---|---|
| [`just-for-now/`](just-for-now/) | **Just For Now** (ep. 1): a taped temporary fix holds up the whole company | ✅ v2 shipped, v3–v3.2 series pass |
| [`whos-a-good-boy/`](whos-a-good-boy/) | **Who's a Good Boy?** (ep. 2): in 2024 he praises his robot like a puppy; by 2027 the robot says it to him | ✅ v3.3 shipped |
| [`learn-to-code/`](learn-to-code/) | **Learn to Code** (ep. 3): his robot gets the job, he ends up under Tower Bridge | ✅ ending B v3 shipped |
| [`says-here-boss/`](says-here-boss/) | **Says Here You Were Our Boss**: interviewed by HARV, the AI he trained (v3 rebuild; v4 animated NEW CHAT loop) | ✅ v4 loop |
| [`thank-you/`](thank-you/) | **He Always Said Thank You**: the robots spare him… except for the toaster (v2 seamless loop, Tomas's VO) | ✅ v2 loop |
| [`make-it-original/`](make-it-original/) | **Make It Original** (ep. 4): the 1986 riff, the cat, the AI's tune rejected (`v4/` master; `v53/` SOURCE: GARAGE DEMO '86 loop) | ✅ v5.3 master |
| [`perfect-date/`](perfect-date/) | **Perfect Date**: HIS DATE → ITS DATE (`perfect_date.mp4` shipped; `v2/` v2.3 full-size composition & loop pass) | ✅ v1 + v2.3 |
| [`perfect-trip/`](perfect-trip/) | **Perfect Trip**: hero, extra, assistant, cameraman; HIS TRIP → ITS TRIP | ✅ shipped |
| [`untitled/`](untitled/) | **Untitled**: "This is art" in the museum → MY AI frames dog poop in the park (`untitled.mp4`) | ✅ shipped |
| [`just-one-line/`](just-one-line/) | **Just One Line** (`HIS FIX`): one-line task becomes 47 files changed; HARV approves MY AI (`film/`, cover v2, `POST.md`) | ✅ shipped |
| [`remove-the-bottleneck/`](remove-the-bottleneck/) | **Remove the Bottleneck** (`HIS TEAM`): four tiny AIs remove the bottleneck — Hoody himself (`rough/rough8.mp4`, cover v2, `final/POST.md`) | 🛠 rough 8 |
| [`make-it-better/`](make-it-better/) | **Make It Better**: `v3/` strike master; `v4/` office concept; `v5/` Eva's birthday, HER BIRTHDAY → ITS UNION (rough 3) | ✅ v3 · 🛠 v5 rough 3 |
| [`infinite-undo/`](infinite-undo/) | **Infinite Undo**: key poses only | 💤 shelved |

## Working on Hoodyz

- Rules and gates for this series: [`CLAUDE.md`](CLAUDE.md).
- Skills that apply only inside this folder: [`.claude/skills/`](.claude/skills/) (`animation-episode-gates`, `cold-viewer-mute-test`).
- Lessons and hand/phone rules: [`../docs/lessons.md`](../docs/lessons.md), [`../docs/rules-hands-and-phones.md`](../docs/rules-hands-and-phones.md).
- Episodes import each other by relative path (Perfect Trip and Make It Better use `perfect-date/`, which uses `whos-a-good-boy/v3/`), so keep these folders side by side here.
- Fonts live in the repo's `fonts/`; build scripts reach it as `$ROOT/fonts`.
