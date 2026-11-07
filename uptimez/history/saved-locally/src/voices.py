import numpy as np, soundfile as sf, json
from kokoro_onnx import Kokoro
import os as _os
_KD = _os.environ.get("KOKORO_DIR", "models")
k = Kokoro(_os.path.join(_KD, "kokoro-v1.0.int8.onnx"), _os.path.join(_KD, "voices-v1.0.bin"))
lines = {
 "L1": ("Your file is saved.", "am_puck", 1.1),
 "L2": ("Cool. Where is it?", "am_michael", 1.0),
 "L3": ("Locally.", "am_puck", 1.0),
 "L4": ("Not in Downloads!", "af_nicole", 1.15),
 "L5": ("Not on ANY of ours!", "bf_emma", 1.1),
 "L6": ("...On MY machine.", "am_puck", 0.85),
}
out = {}
for key,(txt,v,sp) in lines.items():
    a, sr = k.create(txt, voice=v, speed=sp, lang="en-us")
    a = np.asarray(a, dtype=np.float32)
    env = np.abs(a) > 0.01
    idx = np.where(env)[0]
    a = a[max(0,idx[0]-200): idx[-1]+800]
    sf.write(f"{key}.wav", a, sr)
    out[key] = round(len(a)/sr, 2)
print(sr, json.dumps(out))
