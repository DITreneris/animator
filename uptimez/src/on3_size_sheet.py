"""OFFICE NOIR 3: the characters' sizes beside each other: as the series has them (The Onboarding's own staging),
as the ring has them now, and as proposed. For Tomas's decision; no change to the film."""
import cairo, numpy as np
from kit import Ctx
import acts_ob as ao, client_ob as co, sofia_v4 as sf, mom_fs, cand_bc as cb
import film_on3 as f
import ring_on3 as rg, cast_on3 as ca, client_on3 as b, robot_on3 as r, motion_on3 as mo, sofia_on3 as so3, ring_rough_on3 as rr

W, H = 1900, 2130
CANON_CLIENT = 0.66 / 0.67                                   # The Onboarding stages him at 0.66 beside Pam at 0.67 (ob_anim.py)


def top(draw):
    S = cairo.ImageSurface(cairo.FORMAT_ARGB32, 900, 1300); c = cairo.Context(S); draw(Ctx(c, 0), 450, 1200)
    A = np.ndarray((1300, 900, 4), np.uint8, S.get_data())[:, :, 3] > 40
    ys = np.where(A.any(1))[0]
    return 1200 - ys[0]


def row(c, k, y, title, figs, ref, note):
    c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("DejaVu Sans", 0, 1); c.set_font_size(30); c.move_to(30, y - 590); c.show_text(title)
    c.select_font_face("DejaVu Sans", 0, 0); c.set_font_size(21); c.move_to(30, y - 556); c.show_text(note)
    c.set_source_rgb(0.62, 0.62, 0.62); c.rectangle(0, y, W, 44); c.fill()
    href = top(figs[ref][1])
    c.set_source_rgba(0.8, 0.1, 0.1, 0.55); c.set_line_width(2); c.set_dash([10, 8]); c.move_to(0, y - href); c.line_to(W, y - href); c.stroke(); c.set_dash([])
    n = len(figs)
    for i, (name, draw) in enumerate(figs):
        x = 190 + i * (W - 420) / max(1, n - 1)
        draw(k, x, y)
        h = top(draw)
        c.set_source_rgb(0.1, 0.1, 0.1); c.select_font_face("DejaVu Sans", 0, 1); c.set_font_size(22)
        t = "%s  %d %%" % (name, round(100 * h / href)); w = c.text_extents(t).width; c.move_to(x - w / 2, y + 31); c.show_text(t)


def sheet(path):
    S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S); k = Ctx(c, 0)
    c.set_source_rgb(0.86, 0.86, 0.86); c.paint()
    f.mo.CLOCK["shot"] = None
    s1 = 1.15
    canon = [("Don", lambda k, x, y: ao.don(k, x, y, s1, "stand")), ("Sofía", lambda k, x, y: sf.sofia(k, x, y, s1, "stand", "neutral", badge=False)),
             ("Pam", lambda k, x, y: ao.pam(k, x, y, s1, "stand")), ("Klientas", lambda k, x, y: co.client(k, x, y, s1 * CANON_CLIENT, "stand", "confident")),
             ("Mama", lambda k, x, y: mom_fs.mom(k, x, y, s1)), ("Barmenas / teisėjas", lambda k, x, y: cb.macho(k, x, y, s1 * ca.REL_REF))]
    row(c, k, 640, "1. Serija: kaip pastatyta „The Onboarding“", canon, 0, "Raudona linija = Dono ūgis (100 %). Klientas ten statomas 0,66 masteliu šalia Pam 0,67: „galva aukštesnis už Doną“.")
    s2 = 1.15 / 0.7
    SC = rg.SC * s2

    def ring(kc):
        return [("Donas (su skrybėle)", lambda k, x, y: mo.don(k, x, y, SC, "look", "squint", (0, 0), glass=False)),
                ("Sofía su kortele", lambda k, x, y: so3.sofia(k, x, y, 0.92 * s2 * (1.0 if kc is None else 0.74), "r_hips", "spotted", (0, 0))),
                ("Pam", lambda k, x, y: ca.pam_corner(k, x, y, SC, "p_stand", "neutral", (0, 0))),
                ("Klientas", lambda k, x, y: b.boxer(k, x, y, SC * (b.REL if kc is None else kc), rr.WALK, "hard", (0, 0))),
                ("Teisėjas", lambda k, x, y: ca.referee(k, x, y, SC * ca.REL_REF, "ref_stand", waistcoat=True)),
                ("Robotas", lambda k, x, y: r.robot(k, x, y, SC * r.REL * (1.0 if kc is None else kc / b.REL / 1.12), "r_wait", "furious", side=-1))]
    row(c, k, 1340, "2. Office Noir 3 dabar (ringas)", ring(None), 0, "Klientas pieštas masteliu 0,70 (client_on3.REL): 30 %% mažesnis, nei serijoje. Sofía su kortele priekyje piešta 0,92 prieš kitų 0,70.".replace("%%", "%"))
    row(c, k, 2040, "3. Siūloma: serijos proporcijos", ring(CANON_CLIENT), 0, "Klientas 0,985 (kaip serijoje), robotas auga kartu su juo, Sofía su kortele tokio pat mastelio kaip kiti.")
    S.write_to_png(path)


if __name__ == "__main__":
    sheet("../office-noir-3/on3_size_sheet_v1.png")
