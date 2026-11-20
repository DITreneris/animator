"""OFFICE NOIR 3: the whole film as one board (20 Nov), for the whole-board cold test with the loop question.
Every beat in order, drawn by the modules that staged it: 01 the punch (ring_rough2 7.5), 02 the street, 03 the alley,
04 the arena door and her office, 05 the ring (stills from the moving rough), 06-07 the corner and the end, 08 awake.
board() -> [(shot, surface)]. sheets(d) -> numbered sheets of twelve, a phone-size sheet, and the single frames."""
import os
import cairo
import ring_rough_on3 as rr
import ring_rough2_on3 as rr2
import street_casts_on3 as stc
import alley_on3 as al
import door_on3 as dr
import office_on3_v5 as of
import garage_on3_v3 as ga

R5 = (tuple(rr.SHOTS), dict(rr.FN))                        # beat 05's own table, before ring_rough2 borrows the renderer


def _rough(shots, fn):
    out = []
    for name, dur in shots:
        for u in ((0.3, 0.85) if dur >= 1.8 else (0.55,)):
            out.append((name, fn[name](round(u * dur * 30) / 30)))
    return out


def board():
    K = dict(cards="deck", v4=True)
    b = [("1.1", rr2.shot_75(0.6)), ("1.1", rr2.shot_75(0.80))]
    b += [("2", f) for f in stc.frames()]
    b += [("3", f) for f in al.frames()]
    b += [("4.1", dr.behind(1.0)), ("4.2", dr.face((0.2, -0.9))), ("4.2", dr.face((-0.7, 0.9))), ("4.2", dr.face((0.2, -0.9), glove=1.0, push=0.45)),
          ("4.3", of.over(0.0, show=True, **K)), ("4.3", of.over(1.0, show=True, **K)),
          ("4.4", of.reverse(0, 0, **K)), ("4.4", of.reverse(1, 0, **K)), ("4.4", of.reverse(1, 1, turn=0, **K)),
          ("4.4", of.reverse(1, 1, turn=0.35, **K)), ("4.4", of.reverse(1, 1, turn=1.0, eyes=(0.3, 0.9), **K)),
          ("4.4b", of.tower_insert(1.0, v5=True)), ("4.4c", dr.react()), ("4.4c", dr.react(True))]
    b += _rough(*R5)
    b += _rough(rr2.SHOTS[:-1], rr2.FN)
    b += [("7.5", rr2.shot_75(0.6)), ("7.5", rr2.shot_75(0.80))]
    b += [("8.1", ga.f81()), ("8.2", ga.f82()), ("8.3", ga.f83()), ("8.4", ga.f84()), ("8.5", ga.f85())]
    return b


def _sheet(tiles, first, out, w, cols):
    h = int(w * 960 / 540); rows = -(-len(tiles) // cols)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * (w + 6) + 6, rows * (h + 30) + 6); c = cairo.Context(s)
    c.set_source_rgb(0.13, 0.13, 0.15); c.paint()
    for i, f in enumerate(tiles):
        x, y = 6 + (i % cols) * (w + 6), 26 + (i // cols) * (h + 30)
        c.save(); c.translate(x, y); c.scale(w / 540, w / 540); c.set_source_surface(f, 0, 0); c.paint(); c.restore()
        c.set_source_rgb(1, 1, 1); c.select_font_face("sans", 0, 1); c.set_font_size(16); c.move_to(x + 2, y - 7); c.show_text(str(first + i))
    s.write_to_png(out)


def sheets(d, per=12):
    os.makedirs(d, exist_ok=True)
    fs = [f for _, f in board()]
    for i, f in enumerate(fs):
        f.write_to_png(os.path.join(d, "frame_%02d.png" % (i + 1)))
    for j in range(0, len(fs), per):
        _sheet(fs[j:j + per], j + 1, os.path.join(d, "sheet_%d.png" % (j // per + 1)), 320, 6)
    _sheet(fs, 1, os.path.join(d, "sheet_small.png"), 150, 13)
    return len(fs)


if __name__ == "__main__":
    import sys
    print(sheets(sys.argv[1]))
