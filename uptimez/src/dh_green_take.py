import os, sys, json, numpy as np, soundfile as sf
import sound_iwry as si, sound_xmas as sx, sound_on as so, sound_fs as sfs, sound_ob as ob
SR = 48000
def lpc(x, p):
    r = np.correlate(x, x, "full")[len(x)-1:len(x)+p]
    a = np.zeros(p+1); a[0] = 1; e = r[0]
    for i in range(1, p+1):
        k = -(r[i] + np.dot(a[1:i], r[i-1:0:-1])) / e
        a[1:i+1] = a[1:i+1] + k * np.concatenate([a[i-1:0:-1], [1]])
        e *= (1 - k*k)
    return a
def formants(seg, fs=11025):
    x = np.interp(np.linspace(0, len(seg)-1, int(len(seg)*fs/SR)), np.arange(len(seg)), seg)
    out = []
    n = int(0.025*fs); h = int(0.010*fs)
    for i in range(0, len(x)-n, h):
        f = x[i:i+n] * np.hamming(n); f = np.append(f[0], f[1:] - 0.97*f[:-1])
        if np.sqrt(np.mean(f**2)) < 1e-4: continue
        rts = [r for r in np.roots(lpc(f, 12)) if np.imag(r) > 0]
        fr = sorted((np.angle(r)*fs/(2*np.pi), -fs/np.pi*np.log(abs(r))) for r in rts)
        fr = [q for q, b in fr if 200 < q < 4000 and b < 400]
        if len(fr) >= 2: out.append(fr[:2])
    return np.array(out)
def green_f2(a, where):
    # the voiced run of the word: loud 20 ms frames; 'end' = the last run, 'start' = the first
    e = np.array([np.sqrt(np.mean(a[i:i+960]**2)) for i in range(0, len(a)-960, 480)])
    on = e > 0.35 * e.max()
    runs = []; s = None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None: runs.append((s, i)); s = None
    if s is not None: runs.append((s, len(on)))
    r0, r1 = runs[-1] if where == "end" else runs[0]
    seg = a[r0*480:r1*480]
    m = len(seg) // 4                                     # the vowel's middle half
    F = formants(seg[m:-m] if len(seg) > 8 * 960 else seg)
    return (float(np.median(F[:, 0])), float(np.median(F[:, 1]))) if len(F) else (0, 0)
import sherpa_onnx as so_
d = os.environ.get("ASR_DIR", "/home/claude/models/asr/sherpa-onnx-whisper-base.en") + "/"
R = so_.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx", decoder=d + "base.en-decoder.int8.onnx", tokens=d + "base.en-tokens.txt")
def heard(a, line):
    a16 = np.interp(np.linspace(0, len(a)-1, int(len(a)*16000/SR)), np.arange(len(a)), a); pad = np.zeros(4800); hs = []
    for w in (a16, np.concatenate([pad, a16]), np.concatenate([a16, pad])):
        s = R.create_stream(); s.accept_waveform(16000, w.astype(np.float32)); R.decode_stream(s); hs.append(s.result.text.strip())
    return sum(1 for h in hs if sfs._match(h, " ".join(sfs._words(line)))), hs
def tts(txt, sp, ph=False):
    if ph:
        a, sr = si.K.create(txt, voice=si.DON, speed=sp, is_phonemes=True)
        a = np.asarray(a, dtype=np.float64); a = np.interp(np.linspace(0, len(a)-1, int(len(a)*SR/sr)), np.arange(len(a)), a)
        idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0]-600):idx[-1]+2400]
    else:
        a = sx.best_take(txt, si.DON, sp, "en-us")
    a = a / np.sqrt(np.mean(a**2)) * 0.11
    return ob.trim(a)
cmd = sys.argv[1]
if cmd == "old":
    for k, w in (("3.1", "end"), ("3.5", "start"), ("3.1_v1", "end"), ("3.5_v1", "start")):
        a, _ = sf.read("dh_voices/film_v1/%s.wav" % k)
        print(k, "F1/F2 %.0f/%.0f" % green_f2(np.asarray(a, float), w))
    sys.exit()
try:
    print("phonemes:", si.K.tokenizer.phonemize("Make it green.", "en-us"), "|", si.K.tokenizer.phonemize("Green is all he sees.", "en-us"))
except Exception as ex:
    print("no phonemize", ex)
if cmd == "try":
    C = {"3.1": ("Make it green.", "end", [("Make it green.", 1.0, 0), ("Make it green!", 1.0, 0), ("Make it greeen.", 0.96, 0), ("Make it, green.", 1.0, 0),
                                          ("mˌeɪk ɪt ɡɹˈiːn.", 1.0, 1), ("mˌeɪk ɪt ɡɹˈiːn!", 0.96, 1), ("mˌeɪk ɪt ɡɹˈin.", 1.0, 1),
                                          ("mˌeɪk ɪt ɡɹˈiːːn.", 0.96, 1), ("mˌeɪk ɪt, ɡɹˈiːn.", 1.0, 1)]),
         "3.5": ("Green is all he sees.", "start", [("Green is all he sees.", 1.0, 0), ("Green! is all he sees.", 1.0, 0), ("ɡɹˈiːn ɪz ˈɔːl hiː sˈiːz.", 1.0, 1),
                                                   ("ɡɹˈiːn, ɪz ˈɔːl hiː sˈiːz.", 1.0, 1), ("ɡɹˈin ɪz ˈɔːl hiː sˈiːz.", 1.0, 1), ("ɡɹˈiːn ɪz ˈɔːl hiː sˈiːz!", 0.96, 1)])}
    res = {}
    for key, (line, w, cands) in C.items():
        for i, (txt, sp, ph) in enumerate(cands):
            a = tts(txt, sp, ph)
            g, hs = heard(a, line)
            f1, f2 = green_f2(a, w)
            sf.write("/tmp/green/%s_%d.wav" % (key, i), a.astype(np.float32), SR)
            res.setdefault(key, []).append(dict(i=i, txt=txt, sp=sp, ph=ph, len=round(len(a)/SR, 2), ok=g, heard=hs[0], f1=round(f1), f2=round(f2)))
            print("%s %d %-28s %.2f s  %d/3  F1 %4.0f F2 %4.0f  %s" % (key, i, txt, len(a)/SR, g, f1, f2, hs[0]), flush=True)
    json.dump(res, open("/tmp/green/res.json", "w"), indent=1)
def cut_after_first_pause(a, after=0.45, gap=0.06):
    e = np.array([np.sqrt(np.mean(a[i:i+480]**2)) for i in range(0, len(a)-480, 240)])
    th = 0.06 * e.max(); n = int(gap*SR/240)
    i0 = int(after*SR/240)
    for i in range(i0, len(e)-n):
        if (e[i:i+n] < th).all():
            b = a[:i*240 + 1200].copy(); f = int(0.03*SR); b[-f:] *= np.linspace(1, 0, f); return b
    return None
if cmd == "try2":
    cands = [("Make it green, now.", 1.0), ("Make it green, please.", 1.0), ("Make it green, Robot.", 1.0), ("Make it green; and now.", 1.0),
             ("Make it green, green.", 1.0), ("Make it green, then.", 0.96), ("Make it green, okay?", 1.0)]
    for i, (txt, sp) in enumerate(cands):
        full = tts(txt, sp)
        a = cut_after_first_pause(full)
        if a is None:
            print(i, txt, "no pause"); continue
        g, hs = heard(a, "Make it green.")
        f1, f2 = green_f2(a, "end")
        sf.write("/tmp/green/31b_%d.wav" % i, a.astype(np.float32), SR)
        print("3.1b %d %-26s %.2f s  %d/3  F1 %4.0f F2 %4.0f  %s" % (i, txt, len(a)/SR, g, f1, f2, hs), flush=True)
if cmd == "try3":
    cands = [("mˌeɪk ɪt ɡɹˈiːnt.", 1.0, 1), ("mˌeɪk ɪt ɡɹˈiːnp.", 1.0, 1), ("mˌeɪk ɪt ɡɹˈiːn tuː.", 1.0, 1), ("mˌeɪk ɪt ɡɹˈiːn kˈɪŋ.", 1.0, 1),
             ("Make it greenpeace.", 1.0, 0), ("Make it greenkeeper.", 1.0, 0), ("Make it green tea.", 1.0, 0), ("Make it greenback.", 1.0, 0)]
    for i, (txt, sp, ph) in enumerate(cands):
        full = tts(txt, sp, ph)
        for gap in (0.035, 0.02):
            a = cut_after_first_pause(full, after=0.5, gap=gap)
            if a is not None: break
        if a is None:
            print(i, txt, "no pause"); continue
        g, hs = heard(a, "Make it green.")
        f1, f2 = green_f2(a, "end")
        sf.write("/tmp/green/31c_%d.wav" % i, a.astype(np.float32), SR)
        print("3.1c %d %-26s %.2f s (of %.2f) %d/3  F1 %4.0f F2 %4.0f  %s" % (i, txt, len(a)/SR, len(full)/SR, g, f1, f2, hs), flush=True)
def first_word(a, lo=0.22, hi=0.55):
    e = np.array([np.sqrt(np.mean(a[i:i+480]**2)) for i in range(0, len(a)-480, 240)])
    i0, i1 = int(lo*SR/240), int(hi*SR/240)
    j = i0 + int(np.argmin(e[i0:i1]))
    b = a[:j*240].copy(); f = int(0.025*SR); b[-f:] *= np.linspace(1, 0, f); return b
if cmd == "splice":
    old, _ = sf.read("dh_voices/film_v1/3.1.wav"); old = np.asarray(old, float)
    mi = cut_after_first_pause(old, after=0.15, gap=0.03)        # "Make it" (a pause before green?) else by energy dip
    e = np.array([np.sqrt(np.mean(old[i:i+480]**2)) for i in range(0, len(old)-480, 240)])
    print("old env (per 5ms, x100):", " ".join("%d" % (v*100/e.max()) for v in e[::4]))
    srcs = [("Green is all he sees.", 1.0), ("Green, he said.", 1.0), ("Green it is.", 1.0), ("Green ones.", 1.0)]
    for i, (txt, sp) in enumerate(srcs):
        full = tts(txt, sp); g = first_word(full)
        sf.write("/tmp/green/word_%d.wav" % i, g.astype(np.float32), SR)
        gg, hs = heard(g, "Green.")
        print("word %d %-24s %.2f s heard %s F %s" % (i, txt, len(g)/SR, hs, green_f2(g, "start")), flush=True)
if cmd == "join":
    old, _ = sf.read("dh_voices/film_v1/3.1.wav"); old = np.asarray(old, float)
    for cut in (0.38, 0.40, 0.42):
        mi = old[:int(cut*SR)].copy(); f = int(0.015*SR); mi[-f:] *= np.linspace(1, 0, f)
        for wi in (3, 0):
            w, _ = sf.read("/tmp/green/word_%d.wav" % wi); w = np.asarray(w, float)
            w = w / np.sqrt(np.mean(w[np.abs(w) > 0.01]**2)) * np.sqrt(np.mean(old[int(0.44*SR):][np.abs(old[int(0.44*SR):]) > 0.01]**2))
            a = np.concatenate([mi, np.zeros(int(0.02*SR)), w, np.zeros(int(0.12*SR))])
            g, hs = heard(a, "Make it green.")
            f1, f2 = green_f2(a, "end")
            p = "/tmp/green/join_%d_%d.wav" % (int(cut*100), wi); sf.write(p, a.astype(np.float32), SR)
            print("join cut %.2f word %d %.2f s %d/3 F1 %.0f F2 %.0f %s" % (cut, wi, len(a)/SR, g, f1, f2, hs), flush=True)
if cmd == "mix":
    a, _ = sf.read("/tmp/out/s3v8.wav"); a = np.asarray(a, float)
    a48 = np.interp(np.linspace(0, len(a)-1, int(len(a)*3)), np.arange(len(a)), a)
    AT = {"3.1": (0.1, "Make it green.", 1.01), "3.4": (4.0, "It's still one.", 1.0), "3.5": (5.2, "Green is all he sees.", 1.45), "4.3": (10.1, "Different chair.", 1.0)}
    for k, (t0, line, n) in AT.items():
        g, hs = heard(a48[int((t0-0.05)*SR):int((t0+n+0.2)*SR)], line)
        print("LINE", k, g, hs, flush=True)
