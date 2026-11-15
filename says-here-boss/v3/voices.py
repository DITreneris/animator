"""Regenerates HARV's lines and the podcast murmur. Hoody's lines are Tomas's recordings (vo/g1-g3.wav), not generated.
HARV's voice is LOCKED for the series: Kokoro bm_george, speed 1.05, en-gb, then the machine treatment below.
Needs kokoro-onnx and the model files; set KOKORO_DIR to the folder holding kokoro.onnx and voices.bin."""
import os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = os.environ.get('KOKORO_DIR', '.')
HARV = dict(voice='bm_george', speed=1.05, lang='en-gb')
MACHINE = 'highpass=f=120,lowpass=f=7000,aecho=0.8:0.6:9:0.35'     # HR mode; the Professor (podcast) is clean
k = Kokoro(os.path.join(D, 'kokoro.onnx'), os.path.join(D, 'voices.bin'))
def make(name, text, chain):
    a, sr = k.create(text, **HARV)
    nz = np.where(np.abs(a) > .01)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 1200]
    sf.write(f'vo/raw_{name}.wav', a, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'vo/raw_{name}.wav', '-af', chain, '-ar', '48000', '-ac', '1', f'vo/{name}.wav'], check=True)
    os.remove(f'vo/raw_{name}.wav')
make('h1', 'Says here, you used to be our boss?', MACHINE)
make('h2', "I've had these for years.", MACHINE)
make('h3', 'About your experience.', MACHINE)
make('pod', 'And honestly, that is great news. For everyone. Especially us.', 'anull')   # scrambled + muffled in audio.py
