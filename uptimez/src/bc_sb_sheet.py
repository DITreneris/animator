"""THE BEST CANDIDATE: storyboard sheets for bc_sb.py (v3; bc_sb_sheet_v1.py and _v2.py are the earlier ones, kept).
One key frame per panel with its number, time span, what happens and the script rows it covers. v3 marks the panels
that were not in v2; every bubble and most cameras changed in v3 (the bubble pass), so those are not marked.
  python3 bc_sb_sheet.py <out dir>           two pages (sections 0-2, 3-6) and a phone-size strip
  python3 bc_sb_sheet.py <out dir> --video   also the silent storyboard: every shot held for its time, 540 x 960"""
import os, subprocess, sys
import cairo
from PIL import Image, ImageDraw, ImageFont
import bc_sb as B

V = "v4"
SECTION = ["COLD OPEN", "THE SMALL ONE", "THE NICE MACHO", "MOM", "THE VERDICT", "THE REVEAL", "THE FATHER"]
TINT = [(96, 104, 120), (196, 120, 40), (60, 132, 200), (24, 128, 120), (34, 150, 90), (200, 60, 60), (110, 84, 160)]
PHONE = ["08", "09", "27", "35", "42", "60"]              # the frames that must read at 360 x 640
MARK = {"new": ("NEW", (200, 50, 50))}
PAPER, NAVY = (247, 245, 238), (30, 40, 70)


def font(w, size):
    return ImageFont.truetype(os.path.expanduser("~/.fonts/Inter-%d.ttf" % w), size)


def still(shot, w):
    """One shot as a PIL image, w wide."""
    h = w * 16 // 9
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    B.frame(cairo.Context(surf), 0, 0, w, shot[4])
    return Image.frombuffer("RGBA", (w, h), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB")


def tc(t):
    return "%d:%04.1f" % (int(t // 60), t % 60)


def wrap(dr, text, f, width):
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if dr.textlength(t, font=f) <= width or not line:
            line = t
        else:
            out.append(line); line = word
    return out + [line]


def page(shots, title, out, cols=8, tw=236):
    th, gap, cap = tw * 16 // 9, 20, 124
    rows = (len(shots) + cols - 1) // cols
    W, H = cols * (tw + gap) + 28, rows * (th + cap) + 124
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    dr.text((24, 22), title, font=font(700, 30), fill=NAVY)
    dr.text((24, 66), "Red tag: a panel that was not in v2.  Every bubble is new: beside the face or just above the "
                      "speaker's head, one speaker to a panel, inside the safe zones (qa_bc.py: clean).  Lines: script v5.",
            font=font(400, 16), fill=(90, 90, 90))
    fn, fs, fr, fm = font(700, 19), font(700, 12), font(400, 15), font(400, 12)
    for i, sh in enumerate(shots):
        x = 24 + (i % cols) * (tw + gap); y = 108 + (i // cols) * (th + cap)
        im.paste(still(sh, tw), (x, y))
        dr.rectangle((x, y, x + tw, y + th), outline=(30, 30, 30), width=2)
        if sh[7] in MARK:
            word, col = MARK[sh[7]]
            wd = dr.textlength(word, font=fs)
            dr.rectangle((x, y + th - 22, x + wd + 16, y + th), fill=col)       # bottom left: the bubbles are at the top
            dr.text((x + 8, y + th - 18), word, font=fs, fill=(255, 255, 255))
        dr.text((x, y + th + 7), sh[0], font=fn, fill=NAVY)
        dr.text((x + 44, y + th + 11), "%s - %s  ·  %.1f s" % (tc(sh[2]), tc(sh[3]), sh[3] - sh[2]), font=fr, fill=(60, 60, 60))
        tag = SECTION[sh[1]]
        twd = dr.textlength(tag, font=fs)
        dr.rounded_rectangle((x + tw - twd - 14, y + th + 92, x + tw, y + th + 112), 4, fill=TINT[sh[1]])
        dr.text((x + tw - twd - 7, y + th + 95), tag, font=fs, fill=(255, 255, 255))
        for j, line in enumerate(wrap(dr, sh[5], fr, tw)[:3]):
            dr.text((x, y + th + 34 + j * 18), line, font=fr, fill=(40, 40, 40))
        dr.text((x, y + th + 96), "script " + sh[6], font=fm, fill=(120, 120, 120))
    im.save(out)


def phone(out):
    by = {s[0]: s for s in B.SHOTS}
    im = Image.new("RGB", (len(PHONE) * 372 + 12, 664), (20, 22, 28))
    for i, n in enumerate(PHONE):
        im.paste(still(by[n], 360), (12 + i * 372, 12))
    im.save(out)


def video(out, tmp="/tmp/bc_sb_video"):
    """The silent storyboard: one encoded file per shot (a held still), joined without re-encoding."""
    os.makedirs(tmp, exist_ok=True)
    f = font(700, 20)
    names = []
    for sh in B.SHOTS:
        im = still(sh, 540)
        dr = ImageDraw.Draw(im, "RGBA")
        label = "%s  %s" % (sh[0], tc(sh[2]))
        wd = dr.textlength(label, font=f)
        dr.rounded_rectangle((540 - wd - 30, 918, 530, 950), 6, fill=(20, 22, 28, 170))
        dr.text((540 - wd - 20, 922), label, font=f, fill=(255, 255, 255, 235))
        png = os.path.join(tmp, "s%s.png" % sh[0]); im.save(png)
        n = int(round(sh[3] * 30)) - int(round(sh[2] * 30))
        part, done = os.path.join(tmp, "s%s.part.mp4" % sh[0]), os.path.join(tmp, "s%s.mp4" % sh[0])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", png, "-vf",
                        "format=yuv420p,loop=-1:1,trim=end_frame=%d" % n, "-c:v", "libx264", "-crf", "18", "-preset",
                        "veryfast", "-pix_fmt", "yuv420p", part], check=True)
        os.replace(part, done); names.append(done)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join("file '%s'\n" % n for n in names))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", out], check=True)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "."
    a = [s for s in B.SHOTS if s[1] <= 2]; b = [s for s in B.SHOTS if s[1] >= 3]
    head = "THE BEST CANDIDATE  ·  STORYBOARD %s  ·  %d panels, %.0f s  ·  " % (V, len(B.SHOTS), B.DURATION)
    page(a, head + "1 of 2: cold open, the small one, the nice macho", os.path.join(d, "bc_storyboard_%s_1.png" % V))
    page(b, head + "2 of 2: Mom, the verdict, the reveal, the father", os.path.join(d, "bc_storyboard_%s_2.png" % V))
    phone(os.path.join(d, "bc_storyboard_phone_%s.png" % V))
    if "--video" in sys.argv:
        video(os.path.join(d, "bc_storyboard_silent_%s.mp4" % V))
