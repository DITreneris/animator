"""Just One Line voices. MY AI: its LOCKED series voice (Kokoro am_puck, pitched 1.35x + light echo; perfect-date/vo/voices.py).
HARV: Kokoro bm_george (his voice from Says Here). Hoody (h_*.wav): Tomas's takes (23 Nov, recordings 40-52), not generated here. Set KOKORO_DIR to the folder with kokoro.onnx and voices.bin."""
import os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = os.environ.get('KOKORO_DIR', '.')
k = Kokoro(os.path.join(D, 'kokoro.onnx'), os.path.join(D, 'voices.bin'))
AI = 'asetrate=24000*1.35,aresample=24000,aecho=0.8:0.5:20:0.22,highpass=f=90'
LINES = [         ('ai_onit', 'On it!', 'am_puck', .85, AI),
         ('ai_almost', 'Almost done!', 'am_puck', .9, AI),
         ('harv_ok', 'Approved.', 'bm_george', 1.0, 'highpass=f=70'),
         ('ai_line', 'Just one line.', 'am_puck', .9, AI)]
for name, text, voice, speed, chain in LINES:
    a, sr = k.create(text, voice=voice, lang='en-us' if voice != 'bm_george' else 'en-gb', speed=speed)
    nz = np.where(np.abs(a) > .01)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 1500]
    sf.write(f'raw_{name}.wav', a, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'raw_{name}.wav', '-af', chain, '-ar', '48000', '-ac', '1', f'{name}.wav'], check=True)
    os.remove(f'raw_{name}.wav'); print(name, round(len(sf.read(f'{name}.wav')[0]) / 48000, 2), 's')
