"""Perfect Trip cover: the Paris photo (Hoody pushed back to an annoyed extra, MY AI in front with the spire on its fingertip)
with the title. It tells "pushed out" without giving the ending away. Writes cover_v2.png."""
import os, sys, cairo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import trip_photos as TP
from kit import txt, WHITE, YEL
S = cairo.ImageSurface(cairo.FORMAT_RGB24, 1080, 1920); c = cairo.Context(S)
_stamp = TP.P.stamp; TP.P.stamp = lambda *a, **k: None          # the title takes the stamp's place on the cover
TP.paris(c, 0); TP.P.stamp = _stamp
c.save(); c.translate(540, 470); c.rotate(-.05)
txt(c, 'PERFECT', 0, 0, 150, YEL, lw=14); txt(c, 'TRIP', 0, 150, 180, WHITE, lw=16)
c.restore()
S.write_to_png(os.path.join(HERE, 'cover_v2.png'))   # v2+: the v1 cover stays untouched; print('cover ok')
