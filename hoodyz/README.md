# ME + MY AI (Hoodyz)

The series about Hoody, his robot MY AI, Eva, the cat and HARV. Title bar "ME + MY AI" with the Hoodyz badge. Every episode is drawn with pycairo and rebuilt from its own folder; voices are Tomas's recordings or Kokoro placeholders.

| Folder | Episode | Status |
|---|---|---|
| [`just-for-now/`](just-for-now/) | **Just For Now** (ep. 1): a taped temporary fix holds up the whole company | ✅ v2 shipped, v3–v3.2 series pass |
| [`whos-a-good-boy/`](whos-a-good-boy/) | **Who's a Good Boy?** (ep. 2): in 2024 he praises his robot like a puppy; by 2027 the robot says it to him | ✅ v3.3 shipped |
| [`learn-to-code/`](learn-to-code/) | **Learn to Code** (ep. 3): his robot gets the job, he ends up under Tower Bridge | ✅ ending B v3 shipped |
| [`says-here-boss/`](says-here-boss/) | **Says Here You Were Our Boss**: interviewed by HARV, the AI he trained (v3 Hoodyz rebuild) | ✅ v3 |
| [`thank-you/`](thank-you/) | **He Always Said Thank You**: the robots spare him… except for the toaster | ✅ v1 |
| [`make-it-original/`](make-it-original/) | **Make It Original** (ep. 4): the 1986 riff, the cat, the AI's tune rejected (master in `v4/`) | ✅ master |
| [`perfect-date/`](perfect-date/) | **Perfect Date**: HIS DATE → ITS DATE | ✅ shipped |
| [`perfect-trip/`](perfect-trip/) | **Perfect Trip**: hero, extra, assistant, cameraman; HIS TRIP → ITS TRIP | ✅ shipped |
| [`make-it-better/`](make-it-better/) | **Make It Better**: v1–v3 strike episode; v4 office concept; v5 Eva's birthday, HER BIRTHDAY → ITS UNION (rough 2) | 🛠 v5 in rough |
| [`infinite-undo/`](infinite-undo/) | **Infinite Undo**: key poses only | 💤 shelved |

## Working on Hoodyz

- Rules and gates for this series: [`CLAUDE.md`](CLAUDE.md).
- Skills that apply only inside this folder: [`.claude/skills/`](.claude/skills/) (`animation-episode-gates`, `cold-viewer-mute-test`).
- Lessons: [`../docs/lessons.md`](../docs/lessons.md).
- Episodes import each other by relative path (Perfect Trip and Make It Better use `perfect-date/`, which uses `whos-a-good-boy/v3/`), so keep these folders side by side here.
- Fonts live in the repo's `fonts/`; build scripts reach it as `$ROOT/fonts`.
