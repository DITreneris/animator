"""DADDY'S HOME: the four gates' measurements on the animation as built (report only), from the rig log of dh_speech
(every rig redrawn alone gives its own pixels). One drawing per shot: the middle one.
  python3 gates_dh.py collect -> /tmp/dh_gates/rows.json and a tinted sheet; python3 gates_dh.py report"""
import json
import os
import sys
import numpy as np

OUT = os.environ.get("DH_GATES_OUT", "/tmp/dh_gates")
BANDS = (("CU", 120), ("MCU", 95), ("MS", 64), ("WS", 0))


def collect():
    import cairo
    from PIL import Image, ImageDraw
    from scipy import ndimage
    import dh_speech as SP
    import dh_anim as A
    SP.install()
    A.bubble = lambda *a, **k: None                           # the picture without bubbles: planes and people only
    import dh_scenes as ds
    import dh_anim1, dh_anim2, dh_anim3
    for m in (dh_anim1, dh_anim2, dh_anim3):
        if hasattr(m, "bubble"):
            m.bubble = A.bubble
    os.makedirs(OUT, exist_ok=True)
    rows, tiles = [], []
    only = [int(x) for x in os.environ.get("DH_GATES_SCENES", "1 2 3 4 5 6 7 8").split()]
    v8 = os.environ.get("DH_GATES_S3") == "v8"             # opt-in (24 Nov): measure scene 3 v8 instead of v7
    if v8:
        import dh_anim3_v8 as m8
        m8.NOBUB[0] = True
        SP._fresh(m8, "frame")
        import dh_back as db
        SP._wrap(db, "don_back", "antenna", False)
    for n in only:
        if n == 3 and v8:
            frame, R, T0 = m8.frame, m8.ROWS, m8.T0
            ds.ARM_PHONE[0] = True
        elif n <= 3:
            m = {1: dh_anim1, 2: dh_anim2, 3: dh_anim3}[n]; frame, R, T0 = m.frame, m.ROWS, m.T0
            ds.ARM_PHONE[0] = n != 1
        else:
            m = __import__("dh_anim%d" % n); frame, R, T0 = m.sc.frame, m.sc.rows, m.sc.T0
            ds.ARM_PHONE[0] = m.sc.phone
        for sid, d in R:
            tt = T0[sid] + d / 2.0
            del SP.REG[:]
            surf = frame(tt, int(tt * 30), 1)[0]
            surf.flush()
            fin = np.frombuffer(surf.get_data(), np.uint8).reshape(960, surf.get_stride() // 4, 4)[:, :540, :3][:, :, ::-1].astype(int)
            people, masks = [], []
            for rec in SP.REG:
                if "iso" not in rec or "f" not in rec:               # the booth's Father is logged another way
                    continue
                a, (hx, hy), sc = rec["iso"]
                own = ~((a[:, :, 0] < 40) & (a[:, :, 1] > 215) & (a[:, :, 2] < 40))
                if own.sum() < 0.004 * own.size:
                    continue
                try:
                    r = float(SP.read_face(rec)["r"])
                except Exception:
                    r = 40.0 * SP._scale_arg(rec) * sc
                masks.append(own); people.append((rec, own, a, r, hx, hy))
            per = []
            later = np.zeros(fin.shape[:2], bool)
            anyp = np.zeros(fin.shape[:2], bool)
            for mk in masks:
                anyp |= mk
            fg = np.zeros(fin.shape[:2], bool)
            for j, (rec, own, a, r, hx, hy) in enumerate(people):
                others = np.zeros_like(own)
                for o in masks[j + 1:]:
                    others |= o
                cov = own & (np.abs(fin - a).sum(-1) > 60) & ~others
                lab, _ = ndimage.label(cov)
                sizes = ndimage.sum(cov, lab, range(1, lab.max() + 1)) if lab.max() else []
                big = [i + 1 for i, s_ in enumerate(sizes) if s_ >= 400]
                cov = np.isin(lab, big)
                fg |= cov
                ys = np.nonzero(own.any(1))[0]
                vis = own & ~cov & ~others
                q = (fin[vis] // 8) if vis.any() else np.zeros((1, 3), int)
                _, cnt = np.unique(q[:, 0] * 4096 + q[:, 1] * 64 + q[:, 2], return_counts=True)
                per.append({"name": rec["name"], "kind": rec["kind"], "r": r, "x": float(hx), "y": float(hy),
                            "feet": int(ys.max()), "top": int(ys.min()), "covered": float(cov.sum() / max(1, own.sum())),
                            "flat": float(cnt.max() / max(1, vis.sum())), "scale": float(SP._scale_arg(rec) * rec["iso"][2])})
            ov = []
            for p in range(len(masks)):
                for q_ in range(p + 1, len(masks)):
                    if (masks[p] & masks[q_]).sum() > 30:
                        ov.append([people[p][0]["name"], people[q_][0]["name"]])
            rows.append({"scene": n, "shot": sid, "len": float(d), "fg": float(fg.mean()), "people": per, "overlap": ov})
            img = fin.astype(np.uint8).copy()
            bgm = ~anyp & ~fg
            img[bgm] = (0.6 * img[bgm] + 0.4 * np.array([90, 140, 230])).astype(np.uint8)
            img[fg] = (0.45 * img[fg] + 0.55 * np.array([240, 90, 60])).astype(np.uint8)
            tiles.append((sid, Image.fromarray(fin.astype(np.uint8)), Image.fromarray(img)))
        print("scene", n, "done", len(rows), flush=True)
    json.dump(rows, open(OUT + "/rows.json", "w"))
    for name, idx in (("frames", 1), ("planes", 2)):
        W, H, cols = 135, 240, 17
        sh = Image.new("RGB", (cols * W, ((len(tiles) + cols - 1) // cols) * (H + 16)), (245, 243, 238)); dr = ImageDraw.Draw(sh)
        for i, t in enumerate(tiles):
            x, y = (i % cols) * W, (i // cols) * (H + 16)
            sh.paste(t[idx].resize((W - 3, H)), (x, y + 14)); dr.text((x + 3, y + 1), t[0], fill=(0, 0, 0))
        sh.save("%s/dh_%s.png" % (OUT, name))


def size_class(r):
    if r is None:
        return "INS"
    for name, lo in BANDS:
        if r >= lo:
            return name


def report():
    import statistics as st
    from collections import Counter
    rows = json.load(open(OUT + "/rows.json"))
    for r in rows:
        ppl = [p for p in r["people"] if 0 <= p["x"] <= 540]
        r["r"] = max([p["r"] for p in ppl], default=None)
        r["size"] = size_class(r["r"]); r["n"] = len(ppl)
    out = []
    P = out.append
    tot = sum(r["len"] for r in rows)
    P("shots %d, %.1f s, mean %.2f s; sizes %s" % (len(rows), tot, tot / len(rows), dict(Counter(r["size"] for r in rows))))
    secs = Counter()
    for r in rows:
        secs[r["size"]] += r["len"]
    P("seconds by size: " + ", ".join("%s %.1f" % kv for kv in secs.most_common()))
    for n in range(1, 9):
        rs = [r for r in rows if r["scene"] == n]
        P("scene %d: %d shots %.1f s, sizes %s, fg in %d" % (n, len(rs), sum(r["len"] for r in rs), dict(Counter(r["size"] for r in rs)),
                                                             sum(r["fg"] >= 0.02 for r in rs)))
    run, prev = 0, None
    for r in rows:
        run = run + 1 if (r["size"] == prev and r["size"] != "INS") else 1
        prev = r["size"]
        if run == 3:
            P("GV1 run of 3+ %s from before %s (scene %d)" % (r["size"], r["shot"], r["scene"]))
    fgshare = sum(r["fg"] >= 0.02 for r in rows) / float(len(rows))
    P("GD1 foreground in %.0f%% of shots" % (100 * fgshare))
    two = [r["shot"] for r in rows if r["n"] >= 2 and r["size"] in ("MS", "MCU") and r["fg"] < 0.02]
    P("GD1 two or more people at MS/MCU, nothing in front: %d shots: %s" % (len(two), " ".join(two)))
    for r in rows:
        ppl = [p for p in r["people"] if 0 <= p["x"] <= 540]
        if len(ppl) >= 3 and max(p["feet"] for p in ppl) - min(p["feet"] for p in ppl) <= 6 and not r["overlap"]:
            P("GD2 line-up %s: %d people on one line" % (r["shot"], len(ppl)))
    sc = {}
    for r in rows:
        for p in r["people"]:
            sc.setdefault(p["name"], []).append((p["r"], r["shot"]))
    P("face radius per rig (min / median / max px): " + "; ".join("%s %d/%d/%d" % (k, min(x for x, _ in v), st.median(x for x, _ in v), max(x for x, _ in v)) for k, v in sc.items()))
    P(">= 2.5 s: " + " ".join("%s %.1f" % (r["shot"], r["len"]) for r in rows if r["len"] >= 2.5))
    P("<= 0.4 s: %d shots" % sum(r["len"] <= 0.4 for r in rows))
    open(OUT + "/report.txt", "w").write("\n".join(out)); print("\n".join(out))


if __name__ == "__main__":
    {"collect": collect, "report": report}[sys.argv[1]]()
