"""Hoodyz QA gate (G5). Fails (exit 1) on any miss; prints PASS / FAIL / SKIP per check.
Usage: python3 qa.py film.mp4 FRAMES [lines.json]
lines.json: [{"name": "h_best", "start": 4.9, "dur": 1.0, "text": "Best birthday ever!"}, ...]
Speech recognition needs sherpa-onnx and the Whisper base.en model in $ASR_DIR (k2-fsa/sherpa-onnx release asr-models);
without it the check is SKIP, which also fails the gate unless QA_ALLOW_SKIP=1."""
import json, os, re, subprocess, sys
import numpy as np

def run(*a): return subprocess.run(a, capture_output=True, text=True).stdout + subprocess.run(a, capture_output=True, text=True).stderr
results = []
def check(name, ok, detail): results.append((name, ok, detail)); print(f"{'PASS' if ok is True else 'SKIP' if ok is None else 'FAIL'}  {name}: {detail}")

film, frames = sys.argv[1], int(sys.argv[2])
lines = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []

v = json.loads(run('ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
                   'stream=width,height,r_frame_rate,nb_read_frames,color_primaries,color_transfer,color_space', '-of', 'json', film))['streams'][0]
check('size', (v['width'], v['height']) == (1080, 1920), f"{v['width']}x{v['height']}")
check('frame rate', v['r_frame_rate'] == '30/1', v['r_frame_rate'])
check('frame count', int(v['nb_read_frames']) == frames, f"{v['nb_read_frames']} (expected {frames})")
check('BT.709 tags', v.get('color_primaries') == 'bt709' and v.get('color_transfer') == 'bt709', f"{v.get('color_primaries')}/{v.get('color_transfer')}")

e = run('ffmpeg', '-hide_banner', '-nostats', '-i', film, '-af', 'ebur128=peak=true', '-f', 'null', '-')
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]); TP = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])
check('loudness', -16.0 <= I <= -14.0, f'{I} LUFS (target -14 to -16)')
check('true peak', TP <= -1.0, f'{TP} dBTP (limit -1.0)')

if lines:
    d = os.environ.get('ASR_DIR', '')
    try:
        import sherpa_onnx
        enc, dec, tok = (os.path.join(d, f'base.en-{x}') for x in ('encoder.int8.onnx', 'decoder.int8.onnx', 'tokens.txt'))
        assert os.path.exists(enc)
        rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=enc, decoder=dec, tokens=tok, language='en', task='transcribe')
    except Exception as ex:
        rec = None; check('speech in the mix', None, f'no recognizer ({ex.__class__.__name__}); set ASR_DIR')
    if rec:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', film, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
        pcm = np.frombuffer(raw, np.float32)
        norm = lambda t: [re.sub(r'm+', 'm', w) for w in re.findall(r"[a-z']+", t.lower().replace('-', ''))]
        for L in lines:
            a = pcm[int(max(0, L['start'] - .1) * 16000): int((L['start'] + L['dur'] + .35) * 16000)]
            s = rec.create_stream(); s.accept_waveform(16000, a); rec.decode_stream(s); got = s.result.text.strip()
            want = norm(L['text']); have = norm(got); hit = sum(w in have for w in want) / max(1, len(want))
            check(f"line {L['name']}", hit >= .6, f'"{L["text"]}" -> "{got}" ({hit:.0%})')

fails = [n for n, ok, _ in results if ok is False or (ok is None and os.environ.get('QA_ALLOW_SKIP') != '1')]
print(('GATE FAIL: ' + ', '.join(fails)) if fails else 'GATE PASS')
sys.exit(1 if fails else 0)
