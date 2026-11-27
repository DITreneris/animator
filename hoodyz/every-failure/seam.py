"""Loop gate: the last frame is frame 0 exactly (0 of 255). Exits 1 on any miss."""
import os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import animatic as AN
a = lambda f: np.frombuffer(AN.draw(f).get_data(), np.uint8).astype(int)
d = abs(a(0) - a(AN.NF - 1)).max()
print('SEAM', 'ok (0.000/255)' if d == 0 else f'FAIL: max diff {d}/255'); sys.exit(1 if d else 0)
