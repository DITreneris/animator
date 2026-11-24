"""ONE STAR: the four new gates (gates-v2-plan.md, Tomas 23 Nov), report only until calibrated.
  python3 gates_os.py collect   -> /tmp/os_gates/log.json (every drawing: faces, camera, hands) and per-shot frames
  python3 gates_os.py report    -> GV, GP, GH (and GD when its markers exist): an OK/FAIL table, sheets, exit 1 on a FAIL
  python3 gates_os.py selftest  -> each rule on its planted fault (must FAIL) and on a clean case (must pass)"""
import json
import os
import sys
import importlib

OUT = os.environ.get("GATES_OUT", "/tmp/os_gates")
MODS = ["cs_scene%d" % i for i in range(1, 7)]
CAMS = []
PORT = []


def _cam_used(shot, cams):
    """the camera the drawing used: v19's override when it is on (it calls the real S itself)."""
    v19 = sys.modules.get("cs_v19")
    if v19 is not None and v19.ON[0] and v19.LAST[0] is not None:
        cam = v19.LAST[0]; v19.LAST[0] = None
        return list(cam)
    return list(cams[-1]) if cams else None


def collect():
    import cs_film_v7 as v
    import cs_board
    import fs_storyboard as sb
    import cs_hands as ch
    import cs_scene1 as s1
    v.setup(); s1.HI[0] = 1
    if os.environ.get("V19"):
        import cs_v19
        cs_v19.install()
    os.makedirs(OUT, exist_ok=True)
    real_S = cs_board.S

    def S(k, cam, *a, **kw):
        CAMS.append(tuple(cam))
        return real_S(k, cam, *a, **kw)
    real_port = sb.fs.portrait                                # the wall portrait draws the Client's rig too: its head is
                                                              # not a person in the room, so it is kept apart

    def portrait(*a, **kw):
        had = sb.HEADS.get("client")
        out = real_port(*a, **kw)
        if sb.HEADS.get("client") is not had:
            PORT.append(sb.HEADS.get("client"))
            if had is None:
                sb.HEADS.pop("client", None)
            else:
                sb.HEADS["client"] = had
        return out
    sb.fs.portrait = portrait
    log = []
    for mn in MODS:
        m = importlib.import_module(mn)
        for mod_ in list(sys.modules.values()):                       # every module that imported S by name
            if getattr(mod_, "S", None) is real_S:
                mod_.S = S
        for shot, nd, fn in m.SHOTS:
            for d in range(nd):
                CAMS.clear(); PORT.clear()
                surf = m.draw(fn, d)
                if d in (0, nd // 2, nd - 1):
                    surf.write_to_png("%s/%s_d%02d.png" % (OUT, shot, d))
                log.append({"scene": mn, "shot": shot, "d": d, "n": nd,
                            "heads": {k_: list(v_) for k_, v_ in sb.HEADS.items()},
                            "cam": _cam_used(shot, CAMS),
                            "hands": [list(h) for h in ch.LOG]})
        print(mn, "done", len(log))
    json.dump(log, open(OUT + "/log.json", "w"))




# ---------------------------------------------------------------------------------------------------------------------------
DPS = 12
BANDS = (("CU", 120), ("MCU", 95), ("MS", 64), ("WS", 0))   # the biggest face's radius at 540 (cs_frame: medium >= 64)
ANGLE = {"4.2": "top", "4.3w": "top"}                         # the rest are at eye level (set by hand: the rig has no tilt)
PROPS = {                                                    # the protect list's props and the shots that show them alone
    "the post (phone)": ("1.2", "1.4b"), "the AI site plan": ("3.4",), "the taped plan, the hole at 7": ("4.2",),
    "the 7 strip": ("4.3c", "4.3s"), "PAM's number": ("5.2", "5.3"), "the UPDATE": ("6.2", "6.3b")}
LIMITS = {"run": 2, "classes": 3, "still_s": 4.0, "mean": (1.2, 3.0), "pair": 0.03, "cut": 0.08, "jump": 0.20}


def size_class(r):
    if r is None:
        return "INS"
    for name, lo in BANDS:
        if r >= lo:
            return name


def shots(log):
    out = []
    for e in log:
        if not out or out[-1]["shot"] != e["shot"]:
            out.append({"shot": e["shot"], "scene": e["scene"], "rows": []})
        out[-1]["rows"].append(e)
    for s in out:
        rs = sorted(max(v[2] for v in e["heads"].values()) for e in s["rows"] if e["heads"])
        s["r"] = rs[len(rs) // 2] if rs else None
        s["size"] = size_class(s["r"])
        s["angle"] = ANGLE.get(s["shot"], "eye")
        s["len"] = len(s["rows"]) / float(DPS)
        cams = [tuple(e["cam"]) for e in s["rows"] if e["cam"]]
        s["move"] = "static" if len(set(cams)) <= 1 else "move"
        s["first"], s["last"] = s["rows"][0], s["rows"][-1]
    return out


def gv(sh, lim=LIMITS):
    f = []
    run = 1
    for a, b in zip(sh, sh[1:]):
        same = (a["size"], a["angle"]) == (b["size"], b["angle"]) and b["size"] != "INS"
        run = run + 1 if same else 1
        if run > lim["run"]:
            f.append(("GV1 run", b["shot"], "%d cuts in a row at %s/%s" % (run, b["size"], b["angle"])))
    for sc in sorted(set(s["scene"] for s in sh)):
        cl = set(s["size"] for s in sh if s["scene"] == sc)
        people = len([s for s in sh if s["scene"] == sc and s["size"] != "INS"])
        if len(cl) < min(lim["classes"], people + 1):                  # calibrated: one people shot + inserts = 2 sizes

            f.append(("GV2 classes", sc, "only %s" % ",".join(sorted(cl))))
    if sh[0]["size"] not in ("WS",) and not any(s["size"] == "WS" for s in sh[:3]):
        f.append(("GV3 wide", sh[0]["shot"], "no wide in the first three shots"))
    names = set(s["shot"] for s in sh)
    for prop, ins in PROPS.items():
        if not any(i in names for i in ins):
            f.append(("GV4 insert", prop, "no insert (%s cut)" % "/".join(ins)))
    for a, b in zip(sh, sh[1:]):                              # a jump cut: same camera, nearly the same framing
        ca, cb = a["last"]["cam"], b["first"]["cam"]
        ha, hb = a["last"]["heads"], b["first"]["heads"]
        common = [n for n in ha if n in hb]
        if not common or a["scene"] != b["scene"]:             # a different subject or another scene is a cut, not a jump
            continue
        moved = max(abs(ha[n][0] - hb[n][0]) / 540.0 + abs(ha[n][1] - hb[n][1]) / 960.0 for n in common)
        if moved > lim["jump"]:
            continue
        if ca and cb and a["size"] == b["size"] and a["size"] != "INS":
            dz = abs(ca[2] - cb[2]) / max(ca[2], cb[2])
            dx = abs(ca[0] - cb[0]) * cb[2] / 540.0
            dy = abs(ca[1] - cb[1]) * cb[2] / 960.0
            if dz < lim["jump"] and dx < lim["jump"] and dy < lim["jump"]:
                f.append(("GV6 jump", "%s>%s" % (a["shot"], b["shot"]), "framing %.0f%% / %.0f%% / zoom %.0f%%" % (dx * 100, dy * 100, dz * 100)))
    for s in sh:
        if s["move"] == "static" and s["len"] > lim["still_s"]:
            f.append(("GV7 still", s["shot"], "%.1f s with no camera move" % s["len"]))
    mean = sum(s["len"] for s in sh) / len(sh)
    if not lim["mean"][0] <= mean <= lim["mean"][1]:
        f.append(("GV7 mean", "film", "mean shot %.2f s" % mean))
    for a, b in zip(sh, sh[1:]):                              # screen direction: who is left of whom, kept across a cut
        if a["scene"] != b["scene"]:
            continue
        ha, hb = a["last"]["heads"], b["first"]["heads"]
        common = [n for n in ha if n in hb and 0 <= ha[n][0] <= 540 and 0 <= hb[n][0] <= 540]
        for i, p in enumerate(common):
            for q in common[i + 1:]:
                if (ha[p][0] - ha[q][0]) * (hb[p][0] - hb[q][0]) < 0:
                    f.append(("GV8 direction", "%s>%s" % (a["shot"], b["shot"]), "%s and %s swap sides" % (p, q)))
    return f, mean


def gp(sh, log, lim=LIMITS):
    f = []
    import itertools
    import statistics
    ratios = {}
    for e in log:                                             # the film's own canon: each pair's median head ratio
        hs = {n: v for n, v in e["heads"].items() if 0 <= v[0] <= 540 and v[2] >= 30}   # a 15 px head is +-7 % per pixel
        for p, q in itertools.combinations(sorted(hs), 2):
            ratios.setdefault((p, q), []).append((hs[p][2] / hs[q][2], e["shot"], e["d"]))
    canon = {k: statistics.median(r for r, _, _ in v) for k, v in ratios.items() if len(v) >= 6}
    seen = set()
    for (p, q), v in ratios.items():
        if (p, q) not in canon:
            continue
        for r, shot, d in v:
            dev = r / canon[(p, q)] - 1
            if abs(dev) > lim["pair"] and (p, q, shot) not in seen:
                seen.add((p, q, shot))
                f.append(("GP1 pair", shot, "%s/%s %+.0f%% from the film's ratio (d%d)" % (p, q, dev * 100, d)))
    unit = {}                                                 # GP2/GP6: a face's size over the camera's zoom is the rig's
    for e in log:                                             # scale; it must not change from shot to shot (lesson 604)
        if not e["cam"]:
            continue
        for n, v in e["heads"].items():
            if 0 <= v[0] <= 540 and v[2] >= 20:
                unit.setdefault(n, []).append((v[2] / e["cam"][2], e["shot"]))
    for n, v in unit.items():
        med = statistics.median(u for u, _ in v)
        bad = {}
        for u, shot in v:
            if abs(u / med - 1) > lim["cut"]:
                bad.setdefault(shot, []).append(u / med - 1)
        for shot, ds in bad.items():
            f.append(("GP2 scale", shot, "%s drawn %+.0f%% off the film's scale (%d drawings)" % (n, 100 * statistics.median(ds), len(ds))))
    ms = [s["r"] for s in sh if s["size"] in ("MS", "MCU")]
    msr = statistics.median(ms) if ms else 80
    for s in sh:
        if s["size"] == "CU" and s["r"] < 1.5 * msr:
            f.append(("GP3 close", s["shot"], "close-up face %d < 1.5x the medium %d" % (s["r"], msr)))
    return f


ADJ = {frozenset(x) for x in (("quiet", "grab"), ("grab", "palm"), ("quiet", "relax"), ("quiet", "fist"),
                              ("fist", "point"), ("grab", "grip"), ("quiet", "point"))}   # a change one step apart is not a pop


def gh(sh):
    f = []
    for s in sh:                                              # GH5: a hand changes shape with no drawing in between
        prev = None
        for e in s["rows"]:
            cur = {h[0]: h[1] for h in e["hands"] if h[0] >= 0}
            if prev:
                for i, g in cur.items():
                    if i in prev and prev[i] != g and "held" not in (g, prev[i]) and frozenset((g, prev[i])) not in ADJ:
                        f.append(("GH5 pop", s["shot"], "hand %d %s -> %s at d%d" % (i, prev[i], g, e["d"])))
            prev = cur
    return f


def gd(sh, rows, lim=LIMITS):
    f = []
    size = {s["shot"]: s["size"] for s in sh}
    by = {}
    for r in rows:
        by.setdefault(r["shot"], []).append(r)
    withfg = 0
    for shot, rs in by.items():
        mid = rs[len(rs) // 2]
        n = len(mid["people"])
        has = max(r["fg"] for r in rs) >= 0.02
        withfg += has
        if n >= 2 and size.get(shot) in ("MS", "MCU") and not has:
            f.append(("GD1 foreground", shot, "%d people at %s, nothing in front (fg %.1f%%)" % (n, size[shot], 100 * max(r["fg"] for r in rs))))
        if n >= 3:
            feet = [p["feet"] for p in mid["people"]]
            if max(feet) - min(feet) <= 6 and not mid["overlap"]:
                f.append(("GD2 line-up", shot, "%d people on one line (feet %d-%d), none overlapping" % (n, min(feet), max(feet))))
        for p in mid["people"]:
            if p["flat"] > 0.6:
                f.append(("GD6 flat", shot, "%s: one colour is %.0f%% of the body" % (p["name"], 100 * p["flat"])))
    share = withfg / float(max(1, len(by)))
    if share < 0.4:
        f.append(("GD1 share", "film", "a foreground layer in %.0f%% of shots (< 40%%)" % (100 * share)))
    moving = [s["shot"] for s in sh if s["move"] == "move" and max(r["fg"] for r in by.get(s["shot"], [{"fg": 0}])) < 0.02]
    if moving:                                                # a move needs a layer that moves faster (cs_v19.PARALLAX)
        f.append(("GD4 parallax", ",".join(moving), "the camera moves with nothing in front to move faster"))
    return f, share


def report():
    log = json.load(open(OUT + "/log.json"))
    sh = shots(log)
    fv, mean = gv(sh)
    fp = gp(sh, log)
    fh = gh(sh)
    fd, share = gd(sh, json.load(open(OUT + "/depth.json"))) if os.path.exists(OUT + "/depth.json") else ([], 0)
    lines = ["| Shot | Size | Face r | Angle | Move | s |", "|---|---|---|---|---|---|"]
    for s in sh:
        lines.append("| %s | %s | %s | %s | %s | %.2f |" % (s["shot"], s["size"], s["r"] and int(s["r"]), s["angle"], s["move"], s["len"]))
    out = ["# One Star v7: gates GV, GP, GH (report only)", "", "Shots: %d, mean %.2f s" % (len(sh), mean), ""] + lines + [""]
    for name, ff in (("GV shot variety", fv), ("GP proportions", fp), ("GD depth and volume", fd), ("GH hands", fh)):
        out.append("## %s: %s (%d)" % (name, "PASS" if not ff else "FAIL", len(ff)))
        out += ["- **%s** %s: %s" % x for x in ff] + [""]
    open(OUT + "/report.md", "w").write("\n".join(out))
    print("\n".join(out))
    return 1 if (fv or fp or fh or fd) else 0


def selftest():
    """each rule on a planted fault (must FAIL) and on a clean film (must pass)."""
    def row(shot, scene, size_r, cam, heads=None, n=12, hands=None):
        return [{"scene": scene, "shot": shot, "d": d, "n": n, "heads": heads or ({"don": [270, 400, size_r]} if size_r else {}),
                 "cam": cam, "hands": hands or []} for d in range(n)]
    clean = row("a", "s", 50, (100, 0, 1.0)) + row("b", "s", 80, (300, 0, 2.0)) + row("c", "s", 130, (500, 0, 3.0)) + row("d", "s", None, None)
    bad = row("a", "s", 80, (100, 0, 2.0)) + row("b", "s", 80, (102, 0, 2.0)) + row("c", "s", 80, (300, 0, 2.0))
    ok = True
    fv, _ = gv(shots(clean), dict(LIMITS, mean=(0, 99)))
    ok &= not [x for x in fv if x[0] in ("GV1 run", "GV2 classes", "GV6 jump")]
    fv, _ = gv(shots(bad), dict(LIMITS, mean=(0, 99)))
    ok &= any(x[0] == "GV1 run" for x in fv) and any(x[0] == "GV6 jump" for x in fv) and any(x[0] == "GV2 classes" for x in fv)
    pair = row("p", "s", None, (0, 0, 1), heads={"don": [100, 400, 80], "client": [300, 400, 88]}, n=10) + \
        row("q", "s", None, (0, 0, 1), heads={"don": [100, 400, 80], "client": [300, 400, 104]}, n=2)
    ok &= any(x[0] == "GP1 pair" and x[1] == "q" for x in gp(shots(pair), pair))
    pop = row("h", "s", 80, (0, 0, 1), hands=None)
    pop[3]["hands"] = [[0, "quiet", 0, 0, 10]]; pop[4]["hands"] = [[0, "palm", 0, 0, 10]]
    ok &= any(x[0] == "GH5 pop" for x in gh(shots(pop)))
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def _arr(surf):
    import numpy as np
    surf.flush()
    a = np.ndarray((surf.get_height(), surf.get_stride() // 4), np.uint32, surf.get_data())[:, :surf.get_width()]
    return a.copy()


def _ptr(surf):
    import numpy as np
    return np.frombuffer(surf.get_data(), np.uint8).__array_interface__["data"][0]


def collect_depth():
    """GD: for the first, middle and last drawing of every shot, each person's own pixels (the change their drawing
    made), what was drawn over them afterwards, and the final picture's colours. The two-pass grip is off here (it
    draws the hands only; the planes don't change)."""
    import numpy as np
    from scipy import ndimage
    import cs_film_v7 as v
    import fs_storyboard as sb
    import cs_scene1 as s1
    v.setup(); s1.HI[0] = 1; s1.GRIP[0] = False
    snaps = []
    plant = os.environ.get("GD_PLANT")                        # selftest: a desk edge drawn over the bottom of this shot
    only = os.environ.get("GD_SHOTS")                         # R2: only these shots, under v19
    if os.environ.get("V19"):
        import cs_v19
        cs_v19.install()

    inport = [False]
    real_port = sb.fs.portrait

    def portrait(*a, **kw):                                   # the wall portrait's Client is a picture, not a person
        inport[0] = True
        try:
            return real_port(*a, **kw)
        finally:
            inport[0] = False
    sb.fs.portrait = portrait

    def hook(when, name, k):
        if inport[0]:
            return
        t = k.c.get_target()
        if not hasattr(t, "get_data") or t.get_width() != 540:
            return
        snaps.append((when, name, _arr(t), _ptr(t)))
    sb.PERSON_HOOK[0] = hook
    rows = []
    sheet = []
    for mn in MODS:
        m = importlib.import_module(mn)
        for shot, nd, fn in m.SHOTS:
            if plant and shot != plant:
                continue
            if only and shot not in only.split(","):
                continue
            for d in sorted(set((0, nd // 2, nd - 1))):
                snaps.clear()
                fn_ = fn
                if plant == shot:
                    def fn_(k, d_, fn=fn):
                        fn(k, d_)
                        k.c.set_source_rgb(0.45, 0.30, 0.20); k.c.rectangle(0, 800, 540, 160); k.c.fill()
                out_s = m.draw(fn_, d)
                fin = _arr(out_s)
                fp = _ptr(out_s)
                snaps[:] = [x[:3] for x in snaps if x[3] == fp]          # scene4's dry pass draws on another surface
                people = []
                for i in range(0, len(snaps) - 1, 2):
                    (w0, n0, a0), (w1, n1, a1) = snaps[i], snaps[i + 1]
                    if (w0, w1) != ("pre", "post") or n0 != n1:
                        continue
                    own = a0 != a1
                    if own.sum() < 0.004 * own.size:
                        continue
                    people.append((n0, own, a1))
                masks = [o for _, o, _ in people]
                fg = np.zeros(fin.shape, bool)
                if people:                                    # drawn after the last person, touching the frame's edge,
                    anyp = np.zeros(fin.shape, bool)          # and covering a person: the foreground layer
                    for o in masks:
                        anyp |= o
                    late = fin != people[-1][2]
                    lab, _ = ndimage.label(late)
                    edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); edge.discard(0)
                    hit = set(np.unique(lab[late & anyp])); hit.discard(0)
                    big = {i for i in edge if (lab == i).sum() >= 0.01 * lab.size}   # or big enough to be a layer
                    keep = list(edge & (hit | big))
                    if keep:
                        fg |= np.isin(lab, keep)
                per = []
                for j, (n, own, after) in enumerate(people):
                    later = (fin != after) & own
                    others = np.zeros_like(own)
                    for o in masks[j + 1:]:
                        others |= o
                    occl = later & ~others
                    lab, _ = ndimage.label(ndimage.binary_dilation(occl, iterations=2))
                    edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
                    edge.discard(0)
                    fgj = fg & own
                    ys = np.nonzero(own.any(1))[0]
                    vis = own & ~later
                    cols, cnt = np.unique(fin[vis], return_counts=True) if vis.any() else ([], [0])
                    per.append({"name": n, "area": float(own.mean()), "feet": int(ys.max()), "top": int(ys.min()),
                                "x": float(np.nonzero(own.any(0))[0].mean()),
                                "flat": float(max(cnt) / max(1, vis.sum())), "fg": float(fgj.sum() / max(1, own.sum()))})
                ov = []
                for p in range(len(masks)):
                    for q in range(p + 1, len(masks)):
                        if (masks[p] & masks[q]).sum() > 30:
                            ov.append([people[p][0], people[q][0]])
                rows.append({"shot": shot, "scene": mn, "d": d, "fg": float(fg.mean()), "people": per, "overlap": ov})
                if d == nd // 2:
                    img = np.zeros(fin.shape + (3,), np.uint8)
                    rgb = np.stack([(fin >> 16) & 255, (fin >> 8) & 255, fin & 255], -1).astype(np.uint8)
                    pm = np.zeros(fin.shape, bool)
                    for o in masks:
                        pm |= o
                    img[:] = rgb
                    img[~pm & ~fg] = (0.55 * rgb[~pm & ~fg] + 0.45 * np.array([90, 140, 230])).astype(np.uint8)   # bg cool
                    img[fg] = (0.45 * rgb[fg] + 0.55 * np.array([240, 90, 60])).astype(np.uint8)                  # fg warm
                    sheet.append((shot, img))
        print(mn, "depth done")
    sb.PERSON_HOOK[0] = None
    json.dump(rows, open(OUT + ("/depth_plant.json" if plant else ("/depth_r2.json" if only else "/depth.json")), "w"))
    if plant:
        print("planted", plant, "fg", [round(r["fg"], 3) for r in rows])
        return 0 if all(r["fg"] >= 0.02 for r in rows) else 1
    from PIL import Image, ImageDraw
    W, H = 180, 320
    cols = 11
    m_ = Image.new("RGB", (cols * W, ((len(sheet) + cols - 1) // cols) * (H + 18)), (245, 243, 238)); dr = ImageDraw.Draw(m_)
    for i, (shot, img) in enumerate(sheet):
        x, y = (i % cols) * W, (i // cols) * (H + 18)
        m_.paste(Image.fromarray(img).resize((W - 4, H)), (x, y + 16)); dr.text((x + 4, y + 2), shot, fill=(0, 0, 0))
    m_.save(OUT + ("/depth_sheet_r2.png" if only else "/depth_sheet.png"))


if __name__ == "__main__":
    sys.exit({"collect": collect, "depth": collect_depth, "report": report, "selftest": selftest}[sys.argv[1]]() or 0)
