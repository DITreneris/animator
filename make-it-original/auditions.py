"""Render the audio auditions: each riff as 1986 guitar, 2016 Hoodyz fragment, cat version;
two AI tunes; the effects. Writes WAVs to aud/ and an audition reel (MP4 with title cards)."""
import os, subprocess, numpy as np, soundfile as sf, cairo
import sound as S, riffs as R
os.makedirs('aud', exist_ok=True)

AI_TUNES = {   # pleasant, confident, clearly different contour (stepwise arc, major)
    'T1 electric piano': ([(67, 2), (69, 2), (74, 2), (78, 2), (76, 2), (81, 6)], [55, 59, 62], 'epiano'),
    'T2 synth lead':     ([(72, 3), (74, 1), (76, 2), (79, 2), (77, 2), (76, 6)], [48, 55, 64], 'lead'),
    'T3 electric piano, T2 melody': ([(72, 3), (74, 1), (76, 2), (79, 2), (77, 2), (76, 6)], [48, 55, 64], 'epiano'),
}

def riff_versions(name, notes):
    g86, _ = S.guitar_phrase(notes, detune_cents=18, seed=11)
    frag, _ = S.guitar_phrase(notes[:3], detune_cents=8, seed=21)
    cat, t_end = S.guitar_phrase(notes, paws=True, seed=31)
    s16 = 60 / 120 / 4; t_last = 0.02 + sum(l for _, l in notes[:-1]) * s16
    cat = S.place(cat, S.meow(), t_last + 0.05, 0.7)
    return {f'riff_{name}_1986': g86, f'riff_{name}_2016_fragment': frag, f'riff_{name}_cat': cat}

clips = []
for k, n in R.CANDIDATES.items():
    for nm, x in riff_versions(k, n).items():
        clips.append((nm, S.norm(x)))
for k, (notes, chord, kind) in AI_TUNES.items():
    hits, _ = R.screen(notes)
    print(k, 'screen', 'FAIL' if hits else 'PASS')
    x, _ = S.tune(notes, chord, kind)
    clips.append(('ai_' + k.split()[0], S.norm(x, .7)))
clips += [('sfx_tape_ff', S.norm(S.tape_ff(), .7)), ('sfx_swipe', S.norm(S.swipe(), .6)),
          ('sfx_tick_roll', S.norm(S.tick_roll(), .5)), ('sfx_meow', S.meow())]
for nm, x in clips:
    sf.write(f'aud/{nm}.wav', x.astype(np.float32), S.SR)

# reel: title card + clip + 0.6 s gap each
LABEL = {'1986': 'Hoodyz, 1986 (rough guitar)', '2016_fragment': 'Hoodyz, 2016 (first 3 notes)', 'cat': 'The cat (paws + meow)'}
def card(text, sub, path):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(s)
    c.set_source_rgb(.98, .95, .88); c.paint(); c.select_font_face('Lilita One'); c.set_source_rgb(.12, .12, .2)
    for t, y, sz in ((text, 880, 110), (sub, 1020, 56)):
        c.set_font_size(sz); e = c.text_extents(t); c.move_to(540 - e.width / 2 - e.x_bearing, y); c.show_text(t)
    s.write_to_png(path)
audio = []; segs = []
for nm, x in clips:
    if nm.startswith('riff_'):
        _, k, *rest = nm.split('_'); title = f'Riff {k}'; sub = LABEL['_'.join(rest)]
    elif nm.startswith('ai_'):
        title = 'AI tune ' + nm[3:]; sub = [v for v in AI_TUNES if v.startswith(nm[3:])][0][3:]
    else:
        title = 'Effect'; sub = nm[4:].replace('_', ' ')
    png = f'aud/card_{nm}.png'; card(title, sub, png)
    seg = np.concatenate([np.zeros(int(.3 * S.SR)), x, np.zeros(int(.6 * S.SR))])
    segs.append((png, len(seg) / S.SR)); audio.append(seg)
full = np.concatenate(audio); st = np.stack([full, full], 1).astype(np.float32)
sf.write('aud/reel.wav', st, S.SR)
with open('aud/cards.txt', 'w') as f:
    for png, d in segs:
        f.write(f"file '{os.path.basename(png)}'\nduration {d:.3f}\n")
    f.write(f"file '{os.path.basename(segs[-1][0])}'\n")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', 'aud/cards.txt', '-i', 'aud/reel.wav',
                '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', 'aud/make_it_original_auditions.mp4'], check=True)
print('clips', len(clips), 'reel', round(len(full) / S.SR, 1), 's')
