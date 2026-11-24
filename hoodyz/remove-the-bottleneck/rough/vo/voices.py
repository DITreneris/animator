"""Remove the Bottleneck voices. The film uses Tomas's takes (h_*.wav, recordings 53-63, 23 Nov); this script only made the
stand-ins that timed rough 1 (Kokoro am_adam, h_*_STANDIN.wav, since deleted).
Set KOKORO_DIR to the folder with kokoro.onnx and voices.bin."""
import os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = os.environ.get('KOKORO_DIR', '.')
k = Kokoro(os.path.join(D, 'kokoro.onnx'), os.path.join(D, 'voices.bin'))
LINES = [('h_remove_STANDIN', 'Remove the bottleneck.', 1.0, 'highpass=f=80'),
         ('h_suit_STANDIN', 'New suit?', .95, 'highpass=f=80'),
         ('h_faster_STANDIN', 'Faster!', 1.0, 'highpass=f=80,lowpass=f=1800,volume=1.4')]          # inside the crate (muffled, still clear)
for name, text, speed, chain in LINES:
    a, sr = k.create(text, voice='am_adam', lang='en-us', speed=speed)
    nz = np.where(np.abs(a) > .01)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 1500]
    sf.write(f'raw_{name}.wav', a, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'raw_{name}.wav', '-af', chain, '-ar', '48000', '-ac', '1', f'{name}.wav'], check=True)
    os.remove(f'raw_{name}.wav'); print(name, round(len(sf.read(f'{name}.wav')[0]) / 48000, 2), 's')
