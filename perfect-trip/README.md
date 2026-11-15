# Perfect Trip

ME + MY AI episode. 1080×1920, 30 fps, 786 frames (26.2 s), −14.2 LUFS, true peak −2.1 dBTP.

On the park bench Hoody asks Eva, "Do you want to go on a trip?" MY AI pops up from behind the bench: "I'LL PLAN EVERYTHING!" At every landmark the perfectionist director demonstrates the classic tourist photo better than Hoody can, and Hoody loses his role: **hero** in Pisa, **extra** in Paris ("STEP BACK!"), **assistant** in Giza ("MORE!", the bags, the camel), **cameraman** in Rome. The Rome photo is Eva and MY AI, and the label turns HIS TRIP → ITS TRIP. Back on the bench: "How did you like our trip?" Eva turns her phone to him. "THANKS FOR THE PHOTOS!" "…Another trip?" MY AI facepalms, ducks behind the bench, and the last frame is frame 0.

- `perfect_trip.mp4`: the final (x264 crf 14 slow, AAC 256k, faststart)
- `cover.png`: the Paris photo with the title (`cover.py`)

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
| Frames, size, rate | 786, 1080×1920, 30 fps |
| Loudness | −14.2 LUFS, LRA 7.2, true peak −2.1 |
| Speech recognition in the final mix | all 8 lines read correctly |
| Phone-app zones | no text in the top strip, right rail or caption area |
| Loop | the last frame is frame 0 below the title bar (difference 0.45/255); the label resets HIS TRIP on the cut |
| Clean rebuild | identical decoded md5 |
| Cold mute tests | three rounds on the roughs; fixes in the commit log |

## Lessons from this episode

1. **Lose the role, not just the size.** "He shrinks photo by photo" needed decoding. Hero → extra → assistant → cameraman reads at once, because each is a situation.
2. **Forced perspective needs arms that can reach.** MY AI's arms only reach its head, so every landmark came out tiny or hidden behind it. A telescopic arm fixed the geometry and became a joke in its own right: a body that does poses no human can copy.
3. **One gag per place.** "The robot touches the landmark" three times read as one joke; each place now has its own beat.
4. **A frame story makes the loop.** The bench before and after, with "…Another trip?" leading into "Do you want to go on a trip?", the same two-shot, and MY AI's antenna peeking over the backrest from frame 0 (planted, then paid off).
5. **Clothes can impersonate a character.** Eva's navy trousers read as Hoody's legs in a photo he wasn't in. Distinct colours per character, all the way down.
6. **Speech tails go to the mouth.** Four of Hoody's tails stopped in his hair; a review caught them, as one did on Perfect Date. Check every tail against the open mouth.
7. **A punchline label must stay inside its bar.** The ITS TRIP pulse grew over the series name; it now swells in place.

## Caption (draft)

> He asked her on a trip. His AI planned everything. ✈️🤖 Watch the top bar.

Pinned comment: *Which photo hurt the most: Paris, Giza or Rome? 📸*

Hashtags: #MEandMYAI #Hoodyz #AIcomedy #animation #travel #fyp
