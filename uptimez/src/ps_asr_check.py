"""G5 speech check: every take inside the final mix, three windows a line, scored by words (sherpa-onnx Whisper base.en,
as hoodyz/qa.py; model from the k2-fsa/sherpa-onnx asr-models release in /tmp/asr).  python3 ps_asr_check.py MASTER.mp4"""
import sys, re, subprocess, numpy as np
SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ps_master_v1_1080.mp4"
sys.path.insert(0,'.')
import ps_film_fix as fx, ps_film as pf, ps_scenes as ps
fx.setup()
import sherpa_onnx
d='/tmp/asr/sherpa-onnx-whisper-base.en/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+'base.en-encoder.int8.onnx',decoder=d+'base.en-decoder.int8.onnx',tokens=d+'base.en-tokens.txt',language='en',task='transcribe')
raw=subprocess.run(['ffmpeg','-loglevel','error','-i',SRC,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32)
def asr(t0,t1):
    s=rec.create_stream(); s.accept_waveform(16000,a[max(0,int(t0*16000)):int(t1*16000)]); rec.decode_stream(s); return s.result.text.strip()
norm=lambda x: re.findall(r"[a-z0-9']+", x.lower().replace("’","'"))
import ps_mix as mx_
VL = mx_._vid_len()   # each scene's video length, as muxed (was a fixed table)
st=0.0; rows=[]
for n in (1,2,3,4,5,6):
    acc=st
    for sid in pf.SCENES[n]:
        line=pf.TIMING[sid]["line"]
        if line:
            parts=ps.says(line)
            for i,(tk,at) in enumerate(zip(pf.TIMING[sid]["takes"],pf.TAKE_AT[sid])):
                aa,sr=pf._take(tk); L=len(aa)/sr; t0=acc+at
                want=norm(parts[i][1] if i<len(parts) else line)
                best=None
                for w0,w1 in ((t0-0.1,t0+L+0.2),(t0-0.4,t0+L+0.1),(t0-0.05,t0+L+0.5)):
                    got=norm(asr(w0,w1)); hit=sum(1 for x in want if x in got)/max(1,len(want))
                    if best is None or hit>best[0]: best=(hit,' '.join(got))
                rows.append((sid,round(t0,2),' '.join(want),best[1],round(best[0],2)))
        acc+=pf.DUR[sid]
    st += VL[n - 1]
for r in rows: print("%-5s %6.2f  want: %-45s got: %-45s %.2f"%r)
