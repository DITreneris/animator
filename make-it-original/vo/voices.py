"""Scratch voices (Kokoro). Run from this folder. Hoodyz = am_puck (series voice), lowered ~1.5 semitones in 2026;
drummer = am_onyx, flat and slow. Trims silence; writes <name>.wav (48 kHz mono) and prints lengths."""
import subprocess, sys
import soundfile as sf
from kokoro_onnx import Kokoro
T = sys.argv[1] if len(sys.argv) > 1 else '../../../tmp_tts/'
k = Kokoro(T + 'kokoro.onnx', T + 'voices.bin')
L = [('drum', 'am_onyx', 'Play something we know.', .88, 0),
     ('ask', 'am_puck', 'Make something completely original.', .97, -1.5),
     ('know', 'am_puck', 'Play something we know.', .88, -1.5),     # the drummer's delivery: flat and slow
     ('orig', 'am_puck', "nˈaʊ ðˈˈæts ɚɹˈɪdʒɪnəl!", .9, -1.5)]   # phonemes: stress written onto THAT'S
for n, v, t, sp, semi in L:
    ph = 'ˈ' in t
    print(n, t if ph else k.tokenizer.phonemize(t, 'en-us'))
    a, sr = k.create(t, voice=v, speed=sp, lang='en-us', is_phonemes=ph); sf.write(f'_{n}.wav', a, sr)
    r = 2 ** (semi / 12)
    flt = (f'asetrate={sr}*{r:.5f},aresample=48000,atempo={1 / r:.5f},' if semi else 'aresample=48000,') + \
          'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'_{n}.wav', '-af', flt, '-ac', '1', f'{n}.wav'], check=True)
    d = sf.info(f'{n}.wav').duration; print(f'  {n}: {d:.2f} s')
