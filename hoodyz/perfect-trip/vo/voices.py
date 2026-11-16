"""Perfect Trip voices. MY AI: its LOCKED voice (Kokoro am_puck, speed 0.85, pitched 1.35x + light echo; see perfect-date/vo/voices.py).
Hoody: STAND-INS only (Kokoro am_adam) to time the rough - Tomas records "Do you want to go on a trip?", "One selfie?",
"How did you like our trip?" and "...Another trip?" to replace them.
Set KOKORO_DIR to the folder with kokoro.onnx and voices.bin."""
import os, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = os.environ.get('KOKORO_DIR', '.')
k = Kokoro(os.path.join(D, 'kokoro.onnx'), os.path.join(D, 'voices.bin'))
AI_CHAIN = 'asetrate=24000*1.35,aresample=24000,aecho=0.8:0.5:20:0.22,highpass=f=90'
LINES = [('ai_stepback', 'stˈɛp bˈˈæk!', True, 'am_puck', .85, AI_CHAIN),          # "Step BACK!"
         ('ai_more', 'mˈˈɔɹ!', True, 'am_puck', .8, AI_CHAIN),                      # "MORE!" (0.8: steadier for speech recognition)
         ('ai_thanks', 'Thanks for the photos!', False, 'am_puck', .9, AI_CHAIN),
         ('h_selfie_STANDIN', 'One selfie?', False, 'am_adam', 1.0, 'highpass=f=80'),
         ('h_more_STANDIN', 'One more?', False, 'am_adam', 1.0, 'highpass=f=80'),
         ('ai_plan', "I'll plan everything!", False, 'am_puck', .9, AI_CHAIN),
         ('h_invite_STANDIN', 'Do you want to go on a trip?', False, 'am_adam', 1.0, 'highpass=f=80'),
         ('h_howtrip_STANDIN', 'How did you like our trip?', False, 'am_adam', 1.0, 'highpass=f=80'),
         ('h_another_STANDIN', 'Another trip?', False, 'am_adam', .95, 'highpass=f=80')]
for name, text, ph, voice, speed, chain in LINES:
    a, sr = k.create(text, voice=voice, lang='en-us', speed=speed, is_phonemes=ph)
    nz = np.where(np.abs(a) > .01)[0]; a = a[max(0, nz[0] - 120):nz[-1] + 1500]
    sf.write(f'raw_{name}.wav', a, sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'raw_{name}.wav', '-af', chain, '-ar', '48000', '-ac', '1', f'{name}.wav'], check=True)
    os.remove(f'raw_{name}.wav'); print(name, round(len(sf.read(f'{name}.wav')[0]) / 48000, 2), 's')
