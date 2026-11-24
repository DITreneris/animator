"""Neutral mute-test sheets of the fight: python3 mutesheets.py OUTDIR"""
import sys, os
out = sys.argv[1]; sys.argv = ['x']
import fight as F
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24); os.makedirs(out, exist_ok=True)
def sheet(fr, w, name, cols):
    h = int(w * 1920 / 1080); rows = -(-len(fr) // cols); S = Image.new('RGB', (cols * w, rows * h), 'white'); d = ImageDraw.Draw(S)
    for i, f in enumerate(fr):
        F.frame(f).write_to_png('_t.png'); x, y = (i % cols) * w, (i // cols) * h; S.paste(Image.open('_t.png').convert('RGB').resize((w, h)), (x, y))
        d.rectangle([x, y, x + 150, y + 32], fill='black'); d.text((x + 6, y + 3), f'{i + 1}  {f / 30:.2f}s', fill='white', font=font)
    S.save(os.path.join(out, name), quality=88)
fr = list(range(0, F.NF, 4)); h = (len(fr) + 1) // 2
sheet(fr[:h], 400, 'a.jpg', 6); sheet(fr[h:], 400, 'b.jpg', 6); sheet(list(range(0, F.NF, 8)), 270, 'phone.jpg', 9)
os.remove('_t.png')
