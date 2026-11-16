"""MY AI's voice - LOCKED for the series. It is the robot's voice from Learn to Code ("Done!"), measured, not guessed:
Kokoro am_puck, then pitched up exactly 1.35x (asetrate) with a light echo. For one-word lines the generation speed is 0.85,
because the 1.35x also speeds the line up and at 1.0 speech recognition misheard "Watch." and "Your turn!".
Needs kokoro-onnx; set KOKORO_DIR to the folder with kokoro.onnx and voices.bin."""
import os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = os.environ.get('KOKORO_DIR', '.')
MY_AI = dict(voice='am_puck', lang='en-us'); SPEED = 0.85
CHAIN = 'asetrate=24000*1.35,aresample=24000,aecho=0.8:0.5:20:0.22,highpass=f=90'
k = Kokoro(os.path.join(D, 'kokoro.onnx'), os.path.join(D, 'voices.bin'))
for name, text, ph in (('ai_watch', 'Watch.', False), ('ai_turn', 'jɔɹ tˈˈɜɹn!', True)):    # "Your TURN!", stress by phonemes
    a, sr = k.create(text, speed=SPEED, is_phonemes=ph, **MY_AI)
    nz = np.where(np.abs(a) > .01)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 1500]
    sf.write(f'raw_{name}.wav', a, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'raw_{name}.wav', '-af', CHAIN, '-ar', '48000', '-ac', '1', f'{name}.wav'], check=True)
    os.remove(f'raw_{name}.wav')
