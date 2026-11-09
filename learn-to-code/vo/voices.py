# Regenerates the raw voice lines with Kokoro (kokoro-onnx). Optional: the processed lines (v_*.wav) are already here.
# Needs kokoro.onnx and voices.bin (kokoro-v1.0.int8.onnx / voices-v1.0.bin from the thewh1teagle/kokoro-onnx release) in $KOKORO_DIR.
# Processing: silence trimmed at both ends with ffmpeg silenceremove; the robot's "Done!" is also pitched up 1.35x with a light echo.
from kokoro_onnx import Kokoro
import soundfile as sf,sys
import os;T=os.environ.get('KOKORO_DIR','.').rstrip('/')+'/'
k=Kokoro(T+'kokoro.onnx',T+'voices.bin')
L=[('this','am_puck','I learned to code for THIS?',1.0),
('done','am_puck','Done!',1.1),
('answer','am_puck','My AI will answer.',1.0),
('hired','bf_emma',"You're hired!",1.0),
('andme','am_puck','And me?',.9),
('charger','bf_emma',"You're the charger guy.",.95),
('fired','am_puck','They fired you too?',1.0),
('worse','bf_emma','Worse.',.9),
('promo','bf_emma','Our AIs promoted each other.',.95),
('still','bf_emma','My AI is still talking with your AI.',1.0)]
for n,v,t,s in L:
    a,sr=k.create(t,voice=v,speed=s,lang='en-gb' if v.startswith('b') else 'en-us');sf.write(n+'.wav',a,sr)
for t in('My AI will answer.','My AI is still talking with your AI.',"You're the charger guy."):print(k.tokenizer.phonemize(t,'en-gb'))
