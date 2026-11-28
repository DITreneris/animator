"""The cups' sheet (da_cups): every hold on the real rigs, big and at film size, each checked by the hand gate.
python3 da_cup_sheet.py -> ../the-double-agent/da_cup_sheet_v1.png"""
import os, sys, math, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import da_layouts as L, da_cups as cu, da_hand_gate as g, da_anim_s1 as A, da_anim_s3 as C, hands_v4 as hv, da_arms, kit
from da_layouts import dp, pm, rig_hands
from kit import Ctx
VER = 2


def pam(k, x, f, sc, jobs, face="neutral", look=(0, 0)):
    return rig_hands(k, lambda kk, a4: C.pam_held(kk, x, f, sc, a4, face, look, mug=False), sc, jobs, sex="f", skin=L.FEMALE)


def don(k, x, f, sc, jobs, face="neutral", look=(0, 0)):
    return rig_hands(k, lambda kk, a4: dp.don(kk, x, f, sc, a4, face, look, hands=False), sc, jobs)


def holds(k, x, f, sc, which):
    """one hold at (x, f) at rig scale sc (Pam's; Don's is sc*0.6/0.54)."""
    u = sc / 0.54
    ms, cs = cu.MUG_FLOOR * u, cu.CUP_FLOOR * u
    ds_ = sc * 0.6 / 0.54
    MT, ST = (x + 42 * u, f - 88 * u), (x - 42 * u, f - 84 * u)       # the wrists: the forearm rising to the vessel
    if which == "handle":
        pam(k, x, f, sc, {1: cu.by_handle(MT, ms, out=-1)})
    elif which == "palm":
        pam(k, x, f, sc, {-1: cu.on_palm(ST, cs, out=1)})
    elif which == "both":
        pam(k, x, f, sc, {1: cu.by_handle(MT, ms, out=-1), -1: cu.on_palm(ST, cs, out=1)})
    elif which == "cradle":
        base = (x + 4 * u, f - 96 * u)                                 # the mug at her chest: handle in one hand, the
        hT = (base[0] + 20.3 * ms - 1.1 * cu.hand_w(sc, "f") * 0.0, base[1] - 15 * ms)   # other palm under its base
        got = {}
        pam(k, x, f, sc, {1: cu.by_handle((x + 30 * u, f - 96 * u), ms, out=-1, got=got)})
        return got
    elif which == "jug":
        got = {}
        pam(k, x, f, sc, {1: cu.by_handle((x + 40 * u, f - 104 * u), 0.75 * u, kind="jug", tilt_jug=0.9, got=got, out=-1)})
        mx, my = x + 104 * u, f - 56 * u
        c = k.c; c.set_source_rgb(0.5, 0.45, 0.4); c.set_line_width(2); c.move_to(x + 70 * u, my); c.line_to(x + 150 * u, my); c.stroke()
        cu.mug(k, mx, my, ms, handle=1, state="rest")
        cu.stream(k, got["lip"], (mx, my), ms)
    elif which == "gift":
        don(k, x, f, ds_, {1: cu.on_palm((x + 50 * u, f - 100 * u), ms, kind="gift", out=-1)}, face="grin", look=(1, 0))
    elif which == "handover":                                          # one drawing he has it on his palm (the cell before);
        px = x + 110 * u                                               # the next she has its handle and his hand is back
        dx = x - 50 * u                                                # at his own side, open: a clear gap to the mug
        don(k, dx, f + 6 * u, ds_, {1: dict(T=(dx + 40 * u, f - 96 * u), pose="PALM", out=-1, reach=True)},
            face="grin", look=(1, 0))
        pam(k, px, f, sc, {-1: cu.by_handle((px - 42 * u, f - 88 * u), ms, kind="gift", out=1)}, face="hopeful", look=(-1, 0.4))
    elif which == "blue":
        pam(k, x, f, sc, {1: cu.by_handle(MT, ms, kind="blue", out=-1)}, face="doubt")
    elif which == "take":                                              # his fingers behind its wall, his thumb across its front
        import hand_lib_v4 as hl
        hs = sc * 0.66 / 0.54
        w = cu.hand_w(hs)
        base = (x + 42 * u + cu.HC * ms + 0.2 * w, f - 88 * u + 15 * ms + 1)      # where her hold will put the mug (measured below)
        probe = {}
        g.paused().__enter__()
        try:
            import cairo as _c
            kk = Ctx(_c.Context(_c.ImageSurface(_c.FORMAT_RGB24, 8, 8)), 0)
            pam(kk, x, f, sc, {1: cu.by_handle(MT, ms, got=probe, out=-1)})
        finally:
            g._IN_REDRAW[0] -= 1
        bx, by = probe["base"]
        gx, gy = bx + 6 * ms, by - 15 * ms
        skin = (0.80, 0.66, 0.54)
        kit.cut(k, [(gx + 80 * u, gy - 0.5 * w), (gx + 0.5 * w, gy - 0.46 * w), (gx + 0.5 * w, gy + 0.46 * w), (gx + 80 * u, gy + 0.5 * w)],
                skin, lw=2)                                           # his forearm, into the hand
        kit.cut(k, [(gx + 80 * u, gy - 0.66 * w), (gx + 52 * u, gy - 0.62 * w), (gx + 52 * u, gy + 0.62 * w), (gx + 80 * u, gy + 0.66 * w)],
                (0.97, 0.97, 0.95), lw=2)
        hl.draw_lr(k, "GRAB", gx + 0.86 * w, gy, (-1, 0), w, skin, 1)   # before her mug: the fingers go behind it
        pam(k, x, f, sc, {1: cu.by_handle(MT, ms, out=-1)}, face="doubt", look=(1, 0))
        cu.thumb_on_body(k, bx, by, ms, 1, w, skin)


CELLS = [("handle", "by the handle: CUP_GRIP"), ("palm", "cup and saucer on the palm: SAUCER_SUPPORT"),
         ("both", "3.3: her mug and his cup"), ("jug", "3.2: the jug by its handle, pouring"),
         ("blue", "2.4: her old blue mug"), ("gift", "2.4: Don presents the gift on his palm"),
         ("handover", "2.4: the next drawing: she has its handle, his hand away"),
         ("take", "3.3: the Client's hand takes it by its body")]


def build():
    da_arms.setup(); hv.enable(); g.install(); A._SETUP.append(1); cu.install()
    CW, CH = 540, 700
    W, H = 4 * CW, 2 * CH + 70
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c0 = cairo.Context(surf)
    c0.set_source_rgb(0.97, 0.95, 0.92); c0.paint()
    c0.select_font_face(kit.FONT); c0.set_source_rgb(0.1, 0.1, 0.1); c0.set_font_size(26)
    c0.move_to(30, 44); c0.show_text("THE CUPS · The Double Agent (15) · v%d: one mug size per space, three holds, each checked by the gate" % VER)
    res = []
    with L.ds.no_badges(), L.don_legs(), L.sofia_lib_hands(), L.face_guard():
        for i, (w_, cap) in enumerate(CELLS):
            cell = cairo.ImageSurface(cairo.FORMAT_RGB24, CW, CH); c = cairo.Context(cell); k = Ctx(c, 0)
            c.set_source_rgb(0.97, 0.95, 0.92); c.paint(); c.select_font_face(kit.FONT)
            g.reset()
            holds(k, 200, 600, 1.15, w_)                                # big (each cell its own frame: the gate
            fl = [q for q in g.check() if q.startswith(("VESSEL", "AIR", "POLE", "WRIST", "LEGACY"))]   # reads frames)
            res.append((w_, fl))
            if w_ != 'handover':                                        # (no room in that cell: its film size is the gift cell's)
                holds(k, *((440, 600) if w_ != 'jug' else (440, 680)), 0.54, w_)
            c.set_source_rgb(0.1, 0.1, 0.1); c.set_font_size(17); c.move_to(14, 640); c.show_text(cap)
            c.set_font_size(14); c.set_source_rgb(*((0.1, 0.5, 0.2) if not fl else (0.8, 0.1, 0.1)))
            c.move_to(14, 664); c.show_text("gate: PASS" if not fl else "gate: " + fl[0][:60])
            c0.set_source_surface(cell, (i % 4) * CW, 70 + (i // 4) * CH); c0.paint()
    out = os.path.join(HERE, "..", "the-double-agent", "da_cup_sheet_v%d.png" % VER)
    surf.write_to_png(out)
    for r in res:
        print(r)
    print("wrote", out)


if __name__ == "__main__":
    build()
