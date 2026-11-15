# Perfect Trip

ME + MY AI episode. 1080×1920, 30 fps, 816 frames (27.2 s), −14.3 LUFS, true peak −1.9 dBTP.

On the park bench Hoody asks Eva, "Do you want to go on a trip?" MY AI pops up from behind the bench: "I'LL PLAN EVERYTHING!" At every landmark the perfectionist director demonstrates the classic tourist photo better than Hoody can, and Hoody loses his role: **hero** in Pisa, **extra** in Paris ("STEP BACK!"), **assistant** in Giza ("MORE!", the bags, the camel), **cameraman** in Rome. The Rome photo is Eva and MY AI, and the label turns HIS TRIP → ITS TRIP. Back on the bench: "How did you like our trip?" Eva turns her phone to him. "THANKS FOR THE PHOTOS!" "…Another trip?" MY AI facepalms, ducks behind the bench, and the last frame is frame 0.

- `perfect_trip.mp4`: the final (x264 crf 14 slow, AAC 256k, faststart)
- `cover.png`: the Paris photo with the title (`cover.py`)

## The memory look

The trip plays like a phone's photo-story video (generic, no real app or brand): a thin title card, **PERFECT TRIP · NOV 2026**; a synthesised gentle piano with warm strings (80 bpm, C–Am–F–G, an original tune) from the title card to the Rome photo, swelling on Rome and fading back to the park on the bench; 6-frame crossfades between trip shots; each album photo drifts slowly towards Hoody's spot (Rome: where he isn't), with a soft vignette and grain. The bench before and after is real life: park sounds only. The sweet music over his demotion is the irony.

## Build

```bash
bash build.sh        # render.py final → audio.py → master.sh → perfect_trip.mp4, then cover.py
```

A clean rebuild from `git archive` gives the same decoded video and audio (md5). It needs `../perfect-date/` (characters, park, bench).

## Files

- `render.py`: 12 shots. `VO` places every line; the lip sync and `audio.py` both read it
- `trip_photos.py`: the four album photos (also used live, animated by a progress value) and the shared pieces: MY AI's **telescopic arm**, the cat's **backpack and moods**, the camel, the luggage
- `places.py`: Pisa, Paris, Giza, Rome as flat backgrounds; landmark size, centre and horizon are parameters (forced perspective), plus the passport **stamps**
- `photo.py`: the Rome ledge and the first stills; loads Perfect Date's `render.py` under its own name
- `audio.py`: per-place ambience, the arm's clicks, a shutter and a stamp thunk per photo, the rope, the flourish, the voices
- `vo/`: Tomas's takes (invite 1, selfie 3, how-did-you-like 2, another-trip 4; huh, whoa, effort, proud hm, sigh) and MY AI's locked voice (`voices.py`)

## Checks on the final

| Check | Result |
|---|---|
| Frames, size, rate | 816, 1080×1920, 30 fps |
| Loudness | −14.3 LUFS, true peak −1.9 (music bed about 5 dB under the voices) |
| Speech recognition in the final mix | all 8 lines read correctly ("MORE!" regenerated at speed 0.8: at 0.85 the single word flipped with the window) |
| Phone-app zones | no text in the top strip, right rail or caption area |
| Loop | the last frame is frame 0 below the title bar (difference 0.45/255); the label resets HIS TRIP on the cut |
| Clean rebuild | identical decoded md5 (checked on the version before the music) |
| Cold mute tests | three rounds on the roughs; fixes in the commit log |

## Lessons from this episode

1. **Lose the role, not just the size.** "He shrinks photo by photo" needed decoding. Hero → extra → assistant → cameraman reads at once, because each is a situation.
2. **Forced perspective needs arms that can reach.** MY AI's arms only reach its head, so every landmark came out tiny or hidden behind it. A telescopic arm fixed the geometry and became a joke in its own right: a body that does poses no human can copy.
3. **One gag per place.** "The robot touches the landmark" three times read as one joke; each place now has its own beat.
4. **A frame story makes the loop.** The bench before and after, with "…Another trip?" leading into "Do you want to go on a trip?", the same two-shot, and MY AI's antenna peeking over the backrest from frame 0 (planted, then paid off).
5. **Clothes can impersonate a character.** Eva's navy trousers read as Hoody's legs in a photo he wasn't in. Distinct colours per character, all the way down.
6. **Speech tails go to the mouth, and only cross the chin.** A bubble above the head sends its tail through the hair and eyes, so on a phone it reads as stopping in his hair. Hoody's bubbles now sit below his face and come up into the mouth. Aim at the drawn body part, not a fixed point: MY AI's tail follows the antenna as it tilts (`myai.antenna()`).
7. **A punchline label must stay inside its bar.** The ITS TRIP pulse grew over the series name; it now swells in place.

## Caption (draft)

> He asked her on a trip. His AI planned everything. ✈️🤖 Watch the top bar.

Pinned comment: *Which photo hurt the most: Paris, Giza or Rome? 📸*

Hashtags: #MEandMYAI #Hoodyz #AIcomedy #animation #travel #fyp
