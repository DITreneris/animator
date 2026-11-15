# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines used by audio.py are already in vo/.
# Needs kokoro-v1.0.int8.onnx and voices-v1.0.bin from the thewh1teagle/kokoro-onnx GitHub release, in $KOKORO_DIR.
# The model file is expected as kokoro.onnx and voices.bin there. Post-processing filters are listed in the README.
from kokoro_onnx import Kokoro
import soundfile as sf
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
for n,t,s in(('ask','Could you just make it better?',1.1),('end','Love the energy. Could you just make it better?',1.05)):
    a,sr=k.create(t,voice='am_puck',speed=s,lang='en-us');sf.write(n+'.wav',a,sr)
