"""OFFICE NOIR 3: the boxing scene drawn out for review, v2 (v1 pinned: animatic v15, before the fixes): animatic v17,
after film v21 and v22. The plan is now the real empty ring with each camera's frame drawn on it (the set is a flat
drawing seen from the front: a camera is a crop, it has no lens position); the continuity chart says why somebody is not
in a picture (out of frame, gone out) instead of marking it red.
v1: the boxing scene as it stands in animatic v15, drawn out for review (no change to the film).
Makes, in office-noir-3/ring_analysis_v1/: 1_timeline.png (shots, lines, blows, motion, loudness), 2_plan.png (the
ring from above with the camera set-ups), 3_continuity.png (who is where on screen in every shot, and the states).
The frame sheets block_A..D are cut from the animatic by the same shot times."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Circle

OUT = "../office-noir-3/ring_analysis_v2/"
VID = "../office-noir-3/on3_animatic_v17.mp4"
m = json.load(open("on3_animatic_timing_v17.json"))
T0 = next(a[1] for a in m["shots"] if a[0] == "5.1a"); T1 = next(a[1] + a[2] for a in m["shots"] if a[0] == "7.5")
LEN_ = T1 - T0
SH = [(a[0], a[1], a[2]) for a in m["shots"] if T0 - 0.01 <= a[1] < T1]
LINES = [l for l in m["lines"] if T0 <= l[0] < T1]
BLOCKS = [("A  įžanga", "5.1a", "5.1c"), ("B  pirmas raundas", "5.2a", "5.6"), ("C  kampas ir detektyvas", "6.1", "6.4"), ("D  paskutinis raundas", "7.1", "7.5")]
KIND = {"5.1a": "W", "5.1a2": "C", "5.1b": "I", "5.1c": "M", "5.2a": "W", "5.2": "W", "5.3": "I", "5.4": "I", "5.4b": "I", "5.5": "X", "5.6": "I",
        "6.1": "M", "6.2": "I", "6.2a": "I", "6.2b": "W", "6.2c": "M", "6.3": "M", "6.4": "X", "7.1": "M", "7.2": "X", "7.2b": "W", "7.3": "X",
        "7.4": "I", "7.4b": "I", "7.4c": "I", "7.5": "C"}
COL = {"W": "#4c78a8", "M": "#72b7b2", "C": "#f58518", "I": "#b0b0b0", "X": "#9d7cc2"}
NAME = {"W": "platus planas (visas ringas)", "M": "vidutinis (kampas, du veikėjai)", "C": "stambus planas", "I": "intarpas (ne ringe / detalė)", "X": "keli planai viename kadre"}
def _st(n):
    return next(a[1] for a in m["shots"] if a[0] == n)


def _en(n):
    return next(a[1] + a[2] for a in m["shots"] if a[0] == n)


BLOWS = [(_st("5.2") + 0.8, "Kliento smūgis\nsustoja ore"), (_st("5.5") + 0.67, "roboto smūgis:\njis krenta"), (_st("7.2") + 1.3, "Kliento trys\nsmūgiai"), (_st("7.5") + 0.78, "roboto smūgis\n(kilpa)")]
FIGHT = [(_st("5.2"), _en("5.2")), (_st("5.5") + 0.25, _en("5.5")), (_st("7.2"), _en("7.2b")), (_st("7.5"), _en("7.5"))]      # two fighters acting on each other
WHAT = {"5.1a": "ringas, Sofía neša ROUND 1 per visą priekį", "5.1a2": "Sofía stambiai", "5.1b": "planas virš ringo, pirštinė", "5.1c": "chalatas užstringa; gongas; atgal",
        "5.2a": "abu centre; robotas; jo žvilgsnis", "5.2": "jis muša, smūgis sustoja (priartinta)", "5.3": "roboto akimis: APPROVAL", "5.4": "Mama neskaito, ranka leidžiasi",
        "5.4b": "mygtukas", "5.5": "varnelė; pirštinės; smūgis; krenta", "5.6": "iš viršaus: guli, skaičiuoja, Pam tempia", "6.1": "Pam: kempinė, pleistras", "6.2": "padalytas: robotas / Mama",
        "6.2a": "Dono siluetas duryse", "6.2b": "Donas ateina, blykstės", "6.2c": "Donas lipa per virvę", "6.3": "aplankas su nuotrauka; lupa", "6.4": "CASE CLOSED; Donas išeina; žvilgsnis",
        "7.1": "jis atsistoja (LAST ROUND)", "7.2": "jis muša robotą (trys smūgiai)", "7.2b": "teisėjas: Break!", "7.3": "jis siekia plano", "7.4": "suskilęs ekranas laukia", "7.4b": "mygtukas",
        "7.4c": "varnelė; Approved.", "7.5": "smūgis į veidą"}


def start(name):
    return next(s for n, s, d in SH if n == name)


def end(name):
    return next(s + d for n, s, d in SH if n == name)


def timeline():
    import subprocess, glob, os, tempfile
    from PIL import Image
    d_ = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(T0), "-t", str(LEN_), "-i", VID, "-vf", "fps=30,scale=90:160", d_ + "/%05d.png"], check=True)
    prev, mot = None, []
    for f_ in sorted(glob.glob(d_ + "/*.png")):
        a_ = np.asarray(Image.open(f_).convert("L"), dtype=np.float32); mot.append(0 if prev is None else float(np.abs(a_ - prev).mean())); prev = a_
    mot = np.array(mot); cut = mot > 22
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(T0), "-t", str(LEN_), "-i", VID, "-ac", "1", "-ar", "8000", "-f", "f32le", d_ + "/a.raw"], check=True)
    au = np.fromfile(d_ + "/a.raw", dtype=np.float32)
    db = np.array([20 * np.log10(np.sqrt((au[i:i + 1600] ** 2).mean() + 1e-12) + 1e-6) for i in range(0, len(au) - 1600, 1600)])
    mm = mot.copy(); mm[cut] = np.nan
    for i in np.where(cut)[0]:
        mm[max(0, i - 1):i + 2] = np.nan
    k = 9; pad = np.pad(mm, k // 2, mode="edge")
    sm = np.array([np.nanmean(pad[i:i + k]) if np.isfinite(pad[i:i + k]).any() else 0 for i in range(len(mm))])
    t = T0 + np.arange(len(mot)) / 30
    fig, ax = plt.subplots(5, 1, figsize=(26, 15), sharex=True, gridspec_kw={"height_ratios": [1.5, 2.2, 1.6, 1.3, 1.0], "hspace": 0.12})
    a = ax[0]
    for n, s, d in SH:
        a.add_patch(Rectangle((s, 0), d, 1, fc=COL[KIND[n]], ec="white", lw=1.5))
        a.text(s + d / 2, 0.5, n, ha="center", va="center", fontsize=10 if d > 0.8 else 7.5, rotation=0 if d > 1.0 else 90, color="black", weight="bold")
    for lab, s0, s1 in BLOCKS:
        x0, x1 = start(s0), end(s1)
        a.add_patch(Rectangle((x0, 1.08), x1 - x0, 0.42, fc="#222222", ec="white", lw=2))
        a.text((x0 + x1) / 2, 1.29, "%s   %.1f s" % (lab, x1 - x0), ha="center", va="center", color="white", fontsize=13, weight="bold")
    a.set_ylim(0, 1.55); a.set_yticks([]); a.set_title("Bokso scena animatike v17 (po pataisų): %d:%04.1f – %d:%04.1f (%.1f s, 26 kadrai; v15 buvo 43,1 s). Kadrai pagal plano tipą" % (T0 // 60, T0 % 60, T1 // 60, T1 % 60, LEN_) + "", loc="left", fontsize=15, weight="bold")
    a.legend(handles=[Rectangle((0, 0), 1, 1, fc=COL[k_]) for k_ in "WMCIX"], labels=[NAME[k_] for k_ in "WMCIX"], ncol=5, loc="upper right", bbox_to_anchor=(1, 1.42), frameon=False, fontsize=10)
    a = ax[1]
    for n, s, d in SH:
        a.axvline(s, color="#dddddd", lw=1)
        a.text(s + 0.05, 0.03, WHAT[n], rotation=90, va="bottom", ha="left", fontsize=8.5, color="#333333")
    WHOC = {"N": "#333333", "SOFIA": "#c2185b", "PAM": "#00796b", "ROBOT": "#5d4037", "MOM": "#6a1b9a", "DON": "#1565c0", "REFEREE": "#ef6c00"}
    for i, (s, e, who, txt, key) in enumerate(LINES):
        y = 0.93 - 0.11 * (i % 3)
        a.add_patch(Rectangle((s, y - 0.04), e - s, 0.08, fc=WHOC[who], ec="none", alpha=0.9))
        a.text(s, y + 0.05, ("pasakotojas" if who == "N" else who.title()) + ": " + txt, fontsize=8.5, color=WHOC[who], va="bottom")
    a.set_ylim(0, 1.08); a.set_yticks([]); a.set_ylabel("kas vyksta /\nkas kalba", fontsize=11)
    a = ax[2]
    a.fill_between(t, 0, sm, color="#4c78a8", alpha=0.55, lw=0); a.plot(t, sm, color="#2a4d77", lw=1.2)
    for x0, x1 in FIGHT:
        a.axvspan(x0, x1, color="#e45756", alpha=0.18)
    for x, lab in BLOWS:
        a.annotate(lab, (x, np.nanmax(sm) * 0.78), ha="center", fontsize=9.5, color="#b71c1c", weight="bold")
        a.plot([x], [np.nanmax(sm) * 0.70], marker="*", ms=18, color="#e45756")
    a.set_ylabel("judesys kadre\n(pikselių pokytis,\nbe montažo šuolių)", fontsize=10); a.set_ylim(0, np.nanmax(sm) * 1.05)
    a.text(T0 + 0.1, np.nanmax(sm) * 0.93, "raudonai: kovotojai veikia vienas kitą (%.1f s iš %.1f s = %d %%; v15: 7,3 s iš 43,1 s = 17 %%)" % (sum(b - a_ for a_, b in FIGHT), LEN_, round(100 * sum(b - a_ for a_, b in FIGHT) / LEN_)), fontsize=11, color="#b71c1c")
    a = ax[3]
    cuts = t[cut]
    cps = np.array([((cuts >= x - 1.5) & (cuts < x + 1.5)).sum() / 3.0 for x in t])
    a.fill_between(t, 0, cps, color="#9d7cc2", alpha=0.6, lw=0)
    for x in cuts:
        a.axvline(x, color="#5e3c99", lw=0.6, alpha=0.6, ymax=0.15)
    a.set_ylabel("montažo šuoliai\nper sekundę\n(3 s langas)", fontsize=10)
    a.text(T0 + 0.1, cps.max() * 0.85, "iš viso %d šuoliai, vidutiniškai kas %.1f s" % (len(cuts), LEN_ / len(cuts)), fontsize=11, color="#5e3c99")
    a = ax[4]
    td = T0 + np.arange(len(db)) * 0.2
    a.fill_between(td, -45, db, color="#54a24b", alpha=0.6, lw=0); a.set_ylim(-45, -5); a.set_ylabel("garsas, dB\n(juodraštinis\nmiksas)", fontsize=10)
    a.set_xlim(T0, T1); a.set_xticks(np.arange(int(T0) + 1, int(T1) + 1, 1)); a.set_xticklabels(["%d:%02d" % (x // 60, x % 60) for x in range(int(T0) + 1, int(T1) + 1)], fontsize=8.5)
    for a_ in ax:
        for lab, s0, s1 in BLOCKS[1:]:
            a_.axvline(start(s0), color="black", lw=1.6, ls="--")
        for sp in ("top", "right"):
            a_.spines[sp].set_visible(False)
    fig.savefig(OUT + "1_timeline.png", dpi=100, bbox_inches="tight", facecolor="white"); plt.close(fig)


def plan():
    """The real empty ring, seen wider than any shot, with each camera's frame drawn on it and the home places marked."""
    import cairo
    import film_on3 as fm
    from PIL import Image, ImageDraw, ImageFont
    rg = fm.rg
    wide = (332, 1150, 0.60)
    s_ = rg.frame(wide, [], [], near=False, hats=False)
    arr = np.ndarray((960, 540, 4), np.uint8, s_.get_data())[:, :, :3][:, :, ::-1]
    K = 3
    im = Image.fromarray(arr.copy()).resize((540 * K, 960 * K)).crop((0, 250 * K, 540 * K, 760 * K))
    W, H = im.size
    canvas = Image.new("RGB", (W + 900, H + 150), "white"); canvas.paste(im, (0, 110)); d = ImageDraw.Draw(canvas)
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26); f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 23)
    f0 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)

    def P(x, y):
        fx, fy = rg.to_frame(wide, x, y)
        return fx * K, (fy - 250) * K + 110
    cams = [("R1 bendras", (332, 1140, 0.9), "#1f77b4", "5.1a; 6.4 išėjimas"), ("5.5 platus", (318, 1130, 1.0), "#17becf", "5.5 kritimas"),
            ("R2 centras", (412, 1100, 1.25), "#2ca02c", "5.2a, 5.2, 7.2 galas, 7.2b"), ("7.3", (335, 1130, 1.5), "#9467bd", "7.3 siekia plano"),
            ("R3 jo kampas", (200, 1160, 1.7), "#ff7f0e", "5.1c"), ("5.2 priartinimas", (384, 1185, 1.9), "#d62728", "5.2 sustojęs smūgis"),
            ("jo kampas arti", (205, 1165, 2.2), "#8c564b", "6.1, 7.1; 6.3 (2,0); 6.4 žvilgsnis (2,1)"), ("R4 roboto kampas", (560, 1250, 2.0), "#e377c2", "6.2 viršus"),
            ("7.2 vidutinis", (430, 1240, 2.3), "#7f7f7f", "7.2 smūgiai")]
    y_leg = 130
    d.text((20, 30), "Ringas, kaip jis nupieštas, ir kiekvienos kameros kadras ant jo (kamera = iškarpa: centras ir didinimas)", font=f0, fill="black")
    for i, (lab, (cx, cy, z), col, shots) in enumerate(cams):
        x0, y0 = P(cx - 270 / z, cy - 480 / z); x1, y1 = P(cx + 270 / z, cy + 480 / z)
        for w_ in range(5):
            d.rectangle((x0 + w_, max(112, y0) + w_, x1 - w_, min(H + 108, y1) - w_), outline=col)
        d.rectangle((x0, max(112, y0), x0 + 14 * len(lab) + 16, max(112, y0) + 34), fill=col); d.text((x0 + 8, max(112, y0) + 3), lab, font=f2, fill="white")
        d.rectangle((W + 30, y_leg, W + 70, y_leg + 30), fill=col)
        d.text((W + 84, y_leg - 2), "%s  (×%.2f)" % (lab, z), font=f1, fill="black"); d.text((W + 84, y_leg + 30), shots, font=f2, fill="#333333"); y_leg += 84
    F = rg.F
    for lab, x, col in (("Pam A", 228, "#00796b"), ("Pam B–D", 176, "#00796b"), ("Klientas: kampas", 130, "#d32f2f"), ("Klientas: kova", 290, "#d32f2f"), ("Robotas", 466, "#5d4037"), ("Teisėjas", 546, "#ef6c00")):
        px, py = P(x, F + 18)
        d.polygon([(px, py), (px - 14, py + 26), (px + 14, py + 26)], fill=col)
        tw = d.textlength(lab, font=f2); d.rectangle((px - tw / 2 - 5, py + 28, px + tw / 2 + 5, py + 58), fill="white"); d.text((px - tw / 2, py + 30), lab, font=f2, fill=col)
    d.text((W + 30, y_leg + 10), "Ne ringo piešinyje (atskiri intarpai):", font=f1, fill="black")
    for j, tx in enumerate(("5.1b, 7.3 galas: planas iš apačios", "5.1c vidurys: gongas", "5.3: roboto akimis", "5.4, 5.4b, 7.4b: Mamos kabinetas, mygtukas",
                             "5.5 pradžia: varnelė; jo akimis; smūgis stambiai", "5.6: iš viršaus", "6.2 apačia: Mama", "6.2a–b: durys, praėjimas", "6.3 galas: lupa", "7.4, 7.4c: ekranas", "7.5: smūgis stambiai")):
        d.text((W + 30, y_leg + 50 + 32 * j), "• " + tx, font=f2, fill="#333333")
    canvas.save(OUT + "2_plan.png")


# who is where on the screen (L left third, C centre, R right; - not in the frame; ins = an insert without the ring), read from the frames
ROWS = ["Klientas", "Robotas", "Teisėjas", "Pam", "Sofía", "Donas", "Mama", "chalatas", "pleistras", "roboto veidas", "planas kadre"]
GRID = {
    "5.1a": ["L", "C", "R", "L", "R→L", "-", "-", "yra", "nėra", "piktas", "taip"], "5.1a2": ["-", "-", "-", "-", "C", "-", "-", "", "", "", "ne"],
    "5.1b": ["pirštinė", "-", "-", "-", "-", "-", "-", "", "", "", "taip"], "5.1c": ["L", "už kadro", "ins", "R→už jo→L", "išėjo", "-", "-", "yra→pusė→yra", "nėra", "", "taip"],
    "5.2a": ["L", "C", "R", "L kr.", "-", "-", "-", "yra", "nėra", "piktas", "taip"], "5.2": ["L", "C", "R", "L kr.", "-", "-", "-", "yra", "nėra", "piktas", "taip"],
    "5.3": ["C", "(jo akys)", "-", "-", "-", "-", "-", "yra", "nėra", "", "ne"], "5.4": ["-", "-", "-", "-", "-", "-", "C", "", "", "", ""],
    "5.4b": ["-", "-", "-", "-", "-", "-", "ranka", "", "", "", ""], "5.5": ["L (krenta)", "C→R", "R", "L", "-", "-", "-", "yra", "nėra", "varnelė", "taip"],
    "5.6": ["L (guli prie kampo)", "už kadro", "iš viršaus", "rankos", "-", "-", "-", "yra", "nėra", "", "ne"], "6.1": ["L", "-", "-", "C", "-", "-", "-", "yra", "uždeda", "", "kraštas"],
    "6.2": ["-", "C", "-", "-", "-", "-", "C", "", "", "šypsosi", "ne"], "6.2a": ["-", "-", "-", "-", "-", "C", "-", "", "", "", "ne"],
    "6.2b": ["-", "R kr.", "-", "-", "-", "C", "-", "", "", "APPROVAL", "taip"], "6.2c": ["L kr.", "-", "-", "-", "-", "C", "-", "yra", "yra", "", "taip"],
    "6.3": ["L", "-", "-", "-", "nuotr.", "R", "-", "yra", "yra", "", "taip"], "6.4": ["L", "R kr.", "C", "L kr.", "-", "C→durys (išeina)", "-", "yra", "yra", "", "taip"],
    "7.1": ["L→C", "-", "-", "-", "kortelė", "-", "-", "yra", "yra", "", "kraštas"], "7.2": ["L", "C", "R", "už kadro", "-", "išėjo", "-", "yra", "yra", "piktas→skilęs", "taip"],
    "7.2b": ["L", "C", "R→C", "už kadro", "-", "-", "-", "yra", "yra", "skilęs", "taip"], "7.3": ["C", "R kr.", "už kadro", "už kadro", "-", "-", "-", "yra", "yra", "skilęs", "taip"],
    "7.4": ["-", "C", "-", "-", "-", "-", "-", "", "", "APPROVAL", "ne"], "7.4b": ["-", "-", "-", "-", "-", "-", "ranka", "", "", "", ""],
    "7.4c": ["-", "C", "-", "-", "-", "-", "-", "", "", "varnelė", ""], "7.5": ["C", "pirštinė", "-", "-", "-", "-", "-", "yra", "yra", "", "ne"]}


def continuity():
    names = [n for n, s, d in SH]
    fig, ax = plt.subplots(figsize=(27, 9.5))
    for j, n in enumerate(names):
        ax.text(j + 0.5, len(ROWS) + 0.45, n, ha="center", va="center", fontsize=11, weight="bold")
        ax.text(j + 0.5, len(ROWS) + 0.12, "%d:%04.1f" % (start(n) // 60, start(n) % 60), ha="center", va="center", fontsize=8, color="#666666")
        for i, r in enumerate(ROWS):
            v = GRID[n][i]; y = len(ROWS) - 1 - i
            fc = "white"
            if v in ("", "-"):
                fc = "#f2f2f2"
            elif "NĖRA" in v or "TIKRINTI" in v:
                fc = "#ffb3b3"
            elif v.startswith("už kadro") or v.startswith("išėjo"):
                fc = "#e6e6e6"
            elif v.startswith("L"):
                fc = "#cfe2f3"
            elif v.startswith("R"):
                fc = "#fde2c5"
            elif v.startswith("C"):
                fc = "#e3f1d8"
            ax.add_patch(Rectangle((j, y), 1, 1, fc=fc, ec="#bbbbbb", lw=0.8))
            ax.text(j + 0.5, y + 0.5, v if v != "-" else "", ha="center", va="center", fontsize=8.2 if len(v) < 9 else 6.6, color="#b71c1c" if "NĖRA" in v else "black")
    for i, r in enumerate(ROWS):
        ax.text(-0.15, len(ROWS) - 1 - i + 0.5, r, ha="right", va="center", fontsize=12, weight="bold")
    for lab, s0, s1 in BLOCKS:
        j0, j1 = names.index(s0), names.index(s1) + 1
        ax.add_patch(Rectangle((j0, len(ROWS) + 0.75), j1 - j0, 0.5, fc="#222222", ec="white", lw=2)); ax.text((j0 + j1) / 2, len(ROWS) + 1.0, lab, color="white", ha="center", va="center", fontsize=12, weight="bold")
        ax.plot([j0, j0], [0, len(ROWS) + 0.75], color="black", lw=2)
    ax.plot([0, len(names)], [4, 4], color="black", lw=1.5)
    ax.text(0, -0.5, "L, C, R: kairė, centras, dešinė ekrano dalis. „už kadro“ = veikėjas ringe stovi savo vietoje, bet ši kamera jo neaprėpia (ne klaida). „išėjo“ = išėjimas parodytas anksčiau. Raudona = klaida arba tikrinti (v2: raudonų nebėra). „kr.“ = prie kadro krašto.",
            fontsize=11, va="top")
    ax.set_xlim(-2.2, len(names)); ax.set_ylim(-1.2, len(ROWS) + 1.4); ax.axis("off")
    ax.set_title("Nuoseklumas po pataisų (animatikas v17): kas kur ekrane kiekviename kadre, ir būsenos", loc="left", fontsize=16, weight="bold")
    fig.savefig(OUT + "3_continuity.png", dpi=100, bbox_inches="tight", facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    timeline(); plan(); continuity()
