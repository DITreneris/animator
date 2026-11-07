# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines used by audio.py are already in vo/.
# Needs kokoro-v1.0.int8.onnx and voices-v1.0.bin from the thewh1teagle/kokoro-onnx GitHub release, in $KOKORO_DIR.
# The model file is expected as kokoro.onnx and voices.bin there. Post-processing filters are listed in the README.
from kokoro_onnx import Kokoro
import soundfile as sf
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
for n,v,t,s in(('dont','am_puck',"Don't touch that!",1.15),('now','am_puck','Just for now.',1.05),('fri1','am_puck',"I'll fix it Friday.",1.1),('fri2','am_puck','Friday.',.95),('fix','af_nicole','So. Should we fix it?',.95)):
    a,sr=k.create(t,voice=v,speed=s,lang='en-us');sf.write(n+'.wav',a,sr)
