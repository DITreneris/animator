# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines used by audio.py are already in vo/.
# Needs kokoro-v1.0.int8.onnx and voices-v1.0.bin from the thewh1teagle/kokoro-onnx GitHub release, in $KOKORO_DIR.
# The model file is expected as kokoro.onnx and voices.bin there. Post-processing filters are listed in the README.
from kokoro_onnx import Kokoro
import soundfile as sf
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
for n,v,t,s in(('garbage','am_puck','Who made this garbage?!',1.1),('back','af_nicole','Should I put it back?',.95),('passed','af_nicole','Test passed.',.95)):
    a,sr=k.create(t,voice=v,speed=s,lang='en-us');sf.write(n+'.wav',a,sr)
