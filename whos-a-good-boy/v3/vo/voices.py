# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines (v_*.wav) are already here.
# Needs kokoro.onnx and voices.bin (kokoro-v1.0.int8.onnx / voices-v1.0.bin from the thewh1teagle/kokoro-onnx release) in $KOKORO_DIR.
# Processing: silence trimmed at both ends with ffmpeg silenceremove; the robot's "Done!" is also pitched up 1.35x with a light echo.
from kokoro_onnx import Kokoro
import soundfile as sf
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
for n,v,t,s in(('wait','am_puck','Wait!',1.0),('good','am_puck',"Who's a good boy?",0.95),('read','af_nicole','Did you read it?',.95),('appr','am_puck','Approve.',1.0),('appr2','am_puck','Approve.',.85)):
    a,sr=k.create(t,voice=v,speed=s,lang='en-us');sf.write(n+'.wav',a,sr)
