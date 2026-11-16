# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines used by audio.py are already in vo/.
# Needs kokoro-v1.0.int8.onnx and voices-v1.0.bin from the thewh1teagle/kokoro-onnx GitHub release, in $KOKORO_DIR.
# The model file is expected as kokoro.onnx and voices.bin there. Post-processing filters are listed in the README.
from kokoro_onnx import Kokoro
import soundfile as sf
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
L={'head':('am_puck','Make it better?',1.0),
'pop':('am_puck','Make it pop.',1.1),
'pro':('am_puck','More professional.',1.15),
'less':('am_puck','Less professional.',1.15),
'first':('am_puck','Actually, the first one was better.',1.05),
'tail':('am_puck','Love the energy. Could you just',1.0),
'chant':('bm_george','No more versions!',1.1)}
for n,(v,t,s) in L.items():
    a,sr=k.create(t,voice=v,speed=s,lang='en-us' if v[0]=='a' else 'en-gb');sf.write(n+'.wav',a,sr)
