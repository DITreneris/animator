"""OFFICE NOIR 3: the boxing scene as it stands in animatic v15, drawn out for review (no change to the film).
Makes, in office-noir-3/ring_analysis_v1/: 1_timeline.png (shots, lines, blows, motion, loudness), 2_plan.png (the
ring from above with the camera set-ups), 3_continuity.png (who is where on screen in every shot, and the states).
The frame sheets block_A..D are cut from the animatic by the same shot times."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Circle

OUT = "../office-noir-3/ring_analysis_v1/"
m = json.load(open("on3_animatic_timing_v15.json"))
T0, T1 = 38.167, 81.267
SH = [(a[0], a[1], a[2]) for a in m["shots"] if T0 - 0.01 <= a[1] < T1]
LINES = [l for l in m["lines"] if T0 <= l[0] < T1]
BLOCKS = [("A  įžanga", "5.1a", "5.1c"), ("B  pirmas raundas", "5.2a", "5.6"), ("C  kampas ir detektyvas", "6.1", "6.4"), ("D  paskutinis raundas", "7.1", "7.5")]
KIND = {"5.1a": "W", "5.1a2": "C", "5.1b": "I", "5.1c": "M", "5.2a": "W", "5.2": "W", "5.3": "I", "5.4": "I", "5.4b": "I", "5.5": "X", "5.6": "I",
        "6.1": "M", "6.2": "I", "6.2a": "I", "6.2b": "W", "6.2c": "M", "6.3": "M", "6.4": "X", "7.1": "M", "7.2": "X", "7.2b": "W", "7.3": "X",
        "7.4": "I", "7.4b": "I", "7.4c": "I", "7.5": "C"}
COL = {"W": "#4c78a8", "M": "#72b7b2", "C": "#f58518", "I": "#b0b0b0", "X": "#9d7cc2"}
NAME = {"W": "platus planas (visas ringas)", "M": "vidutinis (kampas, du veikėjai)", "C": "stambus planas", "I": "intarpas (ne ringe / detalė)", "X": "keli planai viename kadre"}
BLOWS = [(47.75, "Kliento smūgis\nsustoja ore"), (52.55, "roboto smūgis:\njis krenta"), (71.0, "Kliento smūgis\npataiko"), (80.85, "roboto smūgis\n(kilpa)")]
FIGHT = [(46.9, 48.5), (52.4, 53.67), (70.13, 73.23), (79.97, 81.27)]      # two fighters acting on each other
WHAT = {"5.1a": "ringas, Sofía neša ROUND 1", "5.1a2": "Sofía stambiai", "5.1b": "planas virš ringo, pirštinė", "5.1c": "Pam nurengia; gongas; chalatas atgal",
        "5.2a": "abu centre; robotas; jo žvilgsnis", "5.2": "jis muša, smūgis sustoja", "5.3": "roboto akimis: APPROVAL", "5.4": "Mama: Approved.",
        "5.4b": "mygtukas", "5.5": "varnelė; smūgis; jis krenta", "5.6": "iš viršaus: guli, skaičiuoja", "6.1": "Pam: kempinė, pleistras", "6.2": "padalytas: robotas / Mama",
        "6.2a": "Dono siluetas duryse", "6.2b": "Donas ateina, blykstės", "6.2c": "Donas lipa per virvę", "6.3": "aplankas; nuotrauka", "6.4": "CASE CLOSED; planas; teisėjas",
        "7.1": "jis atsistoja (LAST ROUND)", "7.2": "jis muša robotą", "7.2b": "teisėjas: Break!", "7.3": "jis siekia plano", "7.4": "robotas laukia; Mama", "7.4b": "mygtukas",
        "7.4c": "varnelė", "7.5": "smūgis į veidą"}


def start(name):
    return next(s for n, s, d in SH if n == name)


def end(name):
    return next(s + d for n, s, d in SH if n == name)


def timeline():
    mot = np.load("/tmp/rb/motion.npy"); cut = np.load("/tmp/rb/cut.npy"); db = np.load("/tmp/rb/db.npy")
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
    a.set_ylim(0, 1.55); a.set_yticks([]); a.set_title("Bokso scena animatike v15: 0:38,2 – 1:21,3 (43,1 s, 26 kadrai). Kadrai pagal plano tipą", loc="left", fontsize=15, weight="bold")
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
    a.text(T0 + 0.1, np.nanmax(sm) * 0.93, "raudonai: kovotojai veikia vienas kitą (%.1f s iš 43,1 s = %d %%)" % (sum(b - a_ for a_, b in FIGHT), round(100 * sum(b - a_ for a_, b in FIGHT) / 43.1)), fontsize=11, color="#b71c1c")
    a = ax[3]
    cuts = t[cut]
    cps = np.array([((cuts >= x - 1.5) & (cuts < x + 1.5)).sum() / 3.0 for x in t])
    a.fill_between(t, 0, cps, color="#9d7cc2", alpha=0.6, lw=0)
    for x in cuts:
        a.axvline(x, color="#5e3c99", lw=0.6, alpha=0.6, ymax=0.15)
    a.set_ylabel("montažo šuoliai\nper sekundę\n(3 s langas)", fontsize=10)
    a.text(T0 + 0.1, cps.max() * 0.85, "iš viso %d šuoliai, vidutiniškai kas %.1f s" % (len(cuts), 43.1 / len(cuts)), fontsize=11, color="#5e3c99")
    a = ax[4]
    td = T0 + np.arange(len(db)) * 0.2
    a.fill_between(td, -45, db, color="#54a24b", alpha=0.6, lw=0); a.set_ylim(-45, -5); a.set_ylabel("garsas, dB\n(juodraštinis\nmiksas)", fontsize=10)
    a.set_xlim(T0, T1); a.set_xticks(np.arange(39, 82, 1)); a.set_xticklabels(["%d:%02d" % (x // 60, x % 60) for x in range(39, 82)], fontsize=8.5)
    for a_ in ax:
        for lab, s0, s1 in BLOCKS[1:]:
            a_.axvline(start(s0), color="black", lw=1.6, ls="--")
        for sp in ("top", "right"):
            a_.spines[sp].set_visible(False)
    fig.savefig(OUT + "1_timeline.png", dpi=100, bbox_inches="tight", facecolor="white"); plt.close(fig)


def plan():
    fig, ax = plt.subplots(figsize=(20, 14)); ax.set_aspect("equal")
    ax.add_patch(Rectangle((60, 0), 580, 300, fc="#eeeeee", ec="black", lw=3))                                   # the canvas
    for i in (12, 24, 36):
        ax.add_patch(Rectangle((60 - i, -i), 580 + 2 * i, 300 + 2 * i, fc="none", ec="#999999", lw=1))
    ax.text(350, 285, "RINGAS (schema iš viršaus; gylis sąlyginis, nes dekoracija piešta iš priekio)", ha="center", fontsize=12, color="#555555")
    for (x, y) in ((60, 0), (640, 0), (60, 300), (640, 300)):
        ax.add_patch(Circle((x, y), 9, fc="black"))
    pts = {"Pam\n(prie jo kampo)": (88, 60, "#00796b"), "taburetė": (165, 150, "#777777"), "KLIENTAS\n(kovos vieta)": (296, 110, "#d32f2f"),
           "teisėjas": (368, 215, "#ef6c00"), "ROBOTAS\n(kovos vieta)": (452, 110, "#5d4037"), "roboto kampas\n(laidas, tepalinė)": (600, 75, "#5d4037")}
    for lab, (x, y, c) in pts.items():
        ax.add_patch(Circle((x, y), 15, fc=c, ec="black", alpha=0.9)); ax.text(x + (26 if x < 100 else 0), y - (20 if x < 100 else 24), lab, ha="left" if x < 100 else "center", va="top", fontsize=11, color=c, weight="bold")
    ax.annotate("", (430, 110), (318, 110), arrowprops=dict(arrowstyle="<->", lw=2.5, color="#d32f2f")); ax.text(374, 132, "156 vienetai tarp jų", ha="center", fontsize=10, color="#d32f2f")
    ax.add_patch(Rectangle((290, 318), 160, 18, fc="white", ec="black", lw=2)); ax.text(370, 348, "PLANAS „10 GARAGES“ kabo virš ringo (prizas)", ha="center", fontsize=11, weight="bold")
    ax.add_patch(Circle((250, 235), 22, fc="#fff59d", ec="#999900", alpha=0.6)); ax.text(250, 235, "lempa", ha="center", va="center", fontsize=9)
    ax.add_patch(Rectangle((560, 360), 70, 22, fc="black")); ax.text(595, 392, "durys FIGHTERS\n(Donas ateina 6.2a–b)", ha="center", fontsize=10)
    ax.add_patch(Rectangle((40, 372), 620, 70, fc="#cccccc", ec="none")); ax.text(350, 407, "MINIA: trys eilės už ringo (siluetai, rankos, skrybėlės)", ha="center", va="center", fontsize=11)
    ax.add_patch(Rectangle((40, -120), 620, 34, fc="#cccccc", ec="none")); ax.text(350, -103, "pirma eilė: galvos kadro apačioje", ha="center", va="center", fontsize=10)
    ax.annotate("", (300, -62), (640, -62), arrowprops=dict(arrowstyle="->", lw=2.5, color="#c2185b")); ax.text(470, -52, "Sofíos takas su kortele (5.1a): iš dešinės į kairę, prieš virves", ha="center", fontsize=10, color="#c2185b")
    ax.annotate("", (470, 60), (590, 330), arrowprops=dict(arrowstyle="->", lw=2, color="#1565c0", ls="--")); ax.text(560, 215, "Dono kelias\n(6.2b–6.3);\nišėjimo nėra", fontsize=10, color="#1565c0")
    cams = [("R1 bendras", 332, 0.9, ["5.1a"], "#4c78a8"), ("R2 centras (≈1,1–1,3)", 385, 1.2, ["5.2a", "5.2", "5.5", "7.2", "7.2b", "6.4"], "#4c78a8"),
            ("R3 jo kampas (1,7–2,3)", 205, 2.0, ["5.1c", "6.1", "7.1", "6.3"], "#72b7b2"), ("R4 roboto kampas (2,0)", 560, 2.0, ["6.2", "7.2 pradžia"], "#72b7b2"),
            ("7.3 (1,5)", 335, 1.5, ["7.3"], "#9d7cc2")]
    for i, (lab, cx, z, shots, c) in enumerate(cams):
        half = 270 / z; y0 = -170 - 62 * i
        ax.add_patch(Polygon([(cx, y0), (cx - half, -8), (cx + half, -8)], fc=c, ec=c, alpha=0.10, lw=1.5))
        ax.plot([cx - half, cx + half], [y0, y0], color=c, lw=5, solid_capstyle="butt")
        ax.text(cx + half + 8, y0, "%s: %s" % (lab, ", ".join(shots)), va="center", fontsize=11, color="black", weight="bold")
    ax.text(700, 300, "NE RINGE:\n• Mamos kabinetas (5.4, 6.2 apačia, 7.4):\n  kita vieta, žaliuzės, mygtukas\n• roboto akimis (5.3)\n• iš viršaus (5.6): guli, teisėjo ranka\n• planas iš apačios (5.1b, 7.3 antra pusė)\n• stambūs: Sofía (5.1a2), smūgis (5.5, 7.5)",
            fontsize=11.5, va="top", bbox=dict(fc="#f5f5f5", ec="#999999"))
    ax.text(700, 90, "VISOS KAMEROS ŽIŪRI IŠ TOS PAČIOS PUSĖS\n(iš salės priekio). Klientas visada kairėje,\nrobotas dešinėje: krypties taisyklė nelaužoma.\n\nJuostos apačioje rodo, kokį ringo plotį\nmato kiekviena kamera.", fontsize=11.5, va="top", bbox=dict(fc="#fff8e1", ec="#999999"))
    ax.set_xlim(-60, 1010); ax.set_ylim(-480, 460); ax.axis("off")
    ax.set_title("Ringo planas ir kamerų pozicijos (kaip yra dabar)", loc="left", fontsize=16, weight="bold")
    fig.savefig(OUT + "2_plan.png", dpi=100, bbox_inches="tight", facecolor="white"); plt.close(fig)


# who is where on the screen (L left third, C centre, R right; - not in the frame; ins = an insert without the ring), read from the frames
ROWS = ["Klientas", "Robotas", "Teisėjas", "Pam", "Sofía", "Donas", "Mama", "chalatas", "pleistras", "roboto veidas", "planas kadre"]
GRID = {
    "5.1a": ["L", "C", "C", "L", "R→C", "-", "-", "yra", "nėra", "piktas", "taip"], "5.1a2": ["-", "-", "-", "-", "C", "-", "-", "", "", "", "ne"],
    "5.1b": ["pirštinė", "-", "-", "-", "-", "-", "-", "", "", "", "taip"], "5.1c": ["L", "-", "ins", "R", "-", "-", "-", "yra→nėra→yra", "nėra", "", "taip"],
    "5.2a": ["L", "C", "R", "L kr.", "-", "-", "-", "yra", "nėra", "piktas", "taip"], "5.2": ["L", "C", "R", "L kr.", "-", "-", "-", "yra", "nėra", "piktas", "taip"],
    "5.3": ["C", "(jo akys)", "-", "-", "-", "-", "-", "yra", "nėra", "", "ne"], "5.4": ["-", "-", "-", "-", "-", "-", "C", "", "", "", ""],
    "5.4b": ["-", "-", "-", "-", "-", "-", "ranka", "", "", "", ""], "5.5": ["L (krenta)", "C→R", "R", "-", "-", "-", "-", "yra", "nėra", "varnelė", "taip"],
    "5.6": ["C (guli)", "-", "ranka", "-", "-", "-", "-", "yra", "nėra", "", "ne"], "6.1": ["L", "-", "-", "C", "-", "-", "-", "yra", "uždeda", "", "kraštas"],
    "6.2": ["-", "C", "-", "-", "-", "-", "C", "", "", "šypsosi", "ne"], "6.2a": ["-", "-", "-", "-", "-", "C", "-", "", "", "", "ne"],
    "6.2b": ["-", "R kr.", "-", "-", "-", "C", "-", "", "", "APPROVAL", "taip"], "6.2c": ["L kr.", "-", "-", "-", "-", "C", "-", "yra", "yra", "", "taip"],
    "6.3": ["L", "-", "-", "-", "nuotr.", "R", "-", "yra", "yra", "", "taip"], "6.4": ["L", "R kr.", "C", "L kr.", "-", "C (nugara)", "-", "yra", "yra", "", "taip"],
    "7.1": ["L→C", "-", "-", "-", "kortelė", "-", "-", "yra", "yra", "", "kraštas"], "7.2": ["L", "C", "-", "NĖRA", "-", "NĖRA", "-", "yra", "yra", "piktas", "taip"],
    "7.2b": ["L", "C", "C", "NĖRA", "-", "-", "-", "yra", "yra", "piktas", "taip"], "7.3": ["C", "NĖRA", "NĖRA", "NĖRA", "-", "-", "-", "yra", "yra", "", "taip"],
    "7.4": ["-", "C", "-", "-", "-", "-", "C", "", "", "APPROVAL", "ne"], "7.4b": ["-", "-", "-", "-", "-", "-", "ranka", "", "", "", ""],
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
            elif "NĖRA" in v:
                fc = "#ffb3b3"
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
    ax.text(0, -0.5, "L, C, R: kairė, centras, dešinė ekrano dalis. Mėlyna / žalia / oranžinė = vieta ekrane. Raudona NĖRA = veikėjas turėtų būti kadre pagal ankstesnį kadrą, bet jo nėra. „kr.“ = prie kadro krašto. Pilka = kadre nėra ir neturi būti.",
            fontsize=11, va="top")
    ax.set_xlim(-2.2, len(names)); ax.set_ylim(-1.2, len(ROWS) + 1.4); ax.axis("off")
    ax.set_title("Nuoseklumas: kas kur ekrane kiekviename kadre, ir būsenos", loc="left", fontsize=16, weight="bold")
    fig.savefig(OUT + "3_continuity.png", dpi=100, bbox_inches="tight", facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    timeline(); plan(); continuity()
