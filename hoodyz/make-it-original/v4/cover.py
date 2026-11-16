"""Cover thumbnail, 1080x1920. Title and faces inside the centre 1080x1440 that profile grids crop to."""
import cairo, film
from film import *
S = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(S)
stadium(c, 1.3, wide=True)
txt(c, 'MAKE IT', 540, 400, 150, fill=WHITE, lw=26); txt(c, 'ORIGINAL', 540, 560, 170, fill=YEL, lw=28)
hoodyz(c, 400, 1570, 1.08, 2026, 'rocking', 'air', 7, lean=-.05, head_rot=-.1)
robot_body(c, 850, 1090, .75, 'sideeye', (0, 0), 7)
lazy_cat(c, 820, 1540, 1.4, 0, 1.0, 7)
crowd(c, 1.3, 1700); dream_edge(c)
S.write_to_png('make_it_original_cover.png')
from PIL import Image
im = Image.open('make_it_original_cover.png'); im.crop((0, 240, 1080, 1680)).resize((270, 360)).save('cover_grid_check.png')
