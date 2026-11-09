"""Contact sheet of v5 (B) at phone size: frames at the given new-time seconds."""
import sys, cairo, engine_v, importlib
from PIL import Image
mod = importlib.import_module(sys.argv[1])
ts = [float(x) for x in sys.argv[3].split(",")]
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 540, 960)
cols = 6
rows = (len(ts) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 270, rows * 500), "white")
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
for i, t in enumerate(ts):
    engine_v.render(mod, int(round(t * 30)), surf)
    surf.write_to_png("/tmp/f.png")
    im = Image.open("/tmp/f.png").convert("RGB").resize((270, 480))
    sheet.paste(im, ((i % cols) * 270, (i // cols) * 500 + 20))
    d.text(((i % cols) * 270 + 5, (i // cols) * 500 + 3), f"{t:.2f}s", fill="black")
sheet.save(sys.argv[2])
