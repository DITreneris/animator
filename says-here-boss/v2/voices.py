# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines used by audio.py are already in vo/.
# Needs kokoro-v1.0.int8.onnx and voices-v1.0.bin from the thewh1teagle/kokoro-onnx GitHub release, in $KOKORO_DIR.
# The model file is expected as kokoro.onnx and voices.bin there. Post-processing filters are listed in the README.
from kokoro_onnx import Kokoro
import soundfile as sf
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
L={'r1':('bm_george','Says here, you used to be our boss?',1.12),
'g1':('am_puck','Yes?',.95),
'g2':('am_puck','Thank you, sir!',1.2),
'r2':('bm_george','Nice shades, by the way.',1.15),
'r3':('bm_george','Now. About your experience.',1.12)}
for n,(v,t,s) in L.items():
    a,sr=k.create(t,voice=v,speed=s,lang='en-us' if v.startswith('a') else 'en-gb')
    sf.write(n+'.wav',a,sr);print(n,round(len(a)/sr,2),sr)
from kokoro_onnx import Kokoro
import soundfile as sf
a,sr=Kokoro(T+'kokoro.onnx',T+'voices.bin').create('About your experience.',voice='bm_george',speed=1.12,lang='en-gb');sf.write('r3.wav',a,sr)
