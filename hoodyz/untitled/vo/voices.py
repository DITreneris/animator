"""Untitled voices. MY AI: the locked series voice (perfect-date/vo/voices.py: Kokoro am_puck, pitched up 1.35x, light echo).
Hoody: Tomas's own takes (My_recording_35 / 36), trimmed and levelled here. KOKORO_DIR = folder with kokoro.onnx and voices.bin;
REC = folder with rec35.wav and rec36.wav (48 kHz mono)."""
import os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.environ.get('KOKORO_DIR', '.'); REC = os.environ.get('REC', '.')
MY_AI = dict(voice='am_puck', lang='en-us')
CHAIN = 'asetrate=24000*1.35,aresample=24000,aecho=0.8:0.5:20:0.22,highpass=f=90'
k = Kokoro(os.path.join(D, 'kokoro.onnx'), os.path.join(D, 'voices.bin'))
for name, text, speed in (('ai_masterpiece', 'A masterpiece! Ten out of ten!', 0.9), ('ai_vandalism', 'Vandalism!', 0.85), ('ai_art', 'This is art!', 0.85)):
    a, sr = k.create(text, speed=speed, **MY_AI)
    nz = np.where(np.abs(a) > .01)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 1500]
    sf.write(os.path.join(HERE, f'raw_{name}.wav'), a, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, f'raw_{name}.wav'), '-af', CHAIN, '-ar', '48000', '-ac', '1', os.path.join(HERE, f'{name}.wav')], check=True)
    os.remove(os.path.join(HERE, f'raw_{name}.wav'))

def cut(src, pieces, out, gap=0.0):
    """Cut [(start, end), ...] from a take (seconds), join them with `gap` s of silence, 10 ms fades, peak -3 dBFS."""
    x, sr = sf.read(os.path.join(REC, src)); parts = []
    for a, b in pieces:
        y = x[int(a * sr):int(b * sr)].copy(); f = int(.01 * sr); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
        parts += [y, np.zeros(int(gap * sr))]
    y = np.concatenate(parts[:-1]); y = y - y.mean(); y *= 10 ** (-3 / 20) / np.abs(y).max()
    sf.write(os.path.join(HERE, out), y, sr)
cut('rec35.wav', [(6.02, 7.33)], 'h_honest.wav')                        # take 2 of "Be brutally honest."
cut('rec36.wav', [(4.66, 5.28), (5.70, 6.62)], 'h_art.wav', gap=.22)    # take 2 of "See? This is art.", the pause tightened
cut('rec36.wav', [(11.95, 12.86)], 'h_art2.wav')                       # take 4: "This is art." (the 2nd of the three)
print('voices ok')
