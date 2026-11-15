"""Storyboard sheet for tg_sb.py: one key frame per shot with its number, time and line. Writes
tg_storyboard_sheet_v3.png (needs the stills from engine_v.py)."""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

KEYS = [(0.25, "1", "0.0", "slap: \"Raises for everyone! Sign here.\""), (1.9, "1", "1.0", "pull up: banner, cast"),
        (3.2, "2", "2.6", "insert: the form"), (4.7, "3", "3.9", "SOFÍA: \"Still hoping for a raise?\""),
        (6.3, "3", "5.9", "PAM: \"I'm expecting.\""), (8.3, "4", "7.0", "DON: \"Boy or girl? HA!\""),
        (9.05, "4b", "8.8", "Sofía: one eyebrow"), (9.8, "5", "9.3", "TILT: POLICY VIOLATION."),
        (11.3, "6", "10.9", "Don freezes, taps"), (13.0, "7", "11.9", "PAM: \"A raise for saying...\""),
        (15.0, "7", "14.5", "DON (off): \"Now you're getting it.\""), (16.2, "7", "15.85", "PAM: \"No.\" pushes it back"),
        (17.8, "8a", "16.7", "tears a leg: \"You failed.\""), (19.0, "8b", "18.3", "SOFÍA: \"She refused...\""),
        (20.25, "8c", "19.9", "a bite instead of an answer"), (20.9, "8c", "20.45", "\"Same thing here.\""),
        (21.65, "8d", "21.4", "Sofía closes her eyes"), (22.5, "9", "21.9", "Pam rises"),
        (23.1, "9", "22.75", "pats her hair (blush)"), (24.4, "9", "23.6", "\"You're a walking policy violation.\""),
        (26.0, "10a", "25.3", "DON: \"HR. Back me up.\""), (27.0, "10b", "26.8", "scan: Pam, then Don"),
        (28.5, "10b", "28.05", "ACCURATE.  Don freezes mid-bite"), (29.15, "10c", "28.9", "Sofía: tiny smile"),
        (29.7, "11", "29.4", "TILT: one beat of collapse"), (31.3, "11", "30.0", "leg over the word: \"Sign it.\""),
        (32.05, "11", "31.7", "ROBOT (muffled): \"OK. SIGNED.\""), (32.95, "11b", "32.4", "the robot signs the form"),
        (34.0, "11b", "33.4", "100% SATISFACTION: loop")]


def v3(t):
    """v2 key times -> v3: +0.3 s after 4b, +0.6 s after 8d; the two stretched shots land on their emoji pops."""
    if 8.8 <= t < 9.3:
        return 9.2
    if 21.4 <= t < 21.9:
        return 22.0
    if t >= 21.9:
        return t + 0.6
    if t >= 9.3:
        return t + 0.3
    return t


def main(out):
    KEYS[:] = [(v3(t), n, "%.1f" % v3(float(t0)), cap) for t, n, t0, cap in KEYS]
    KEYS[6] = (KEYS[6][0], "4b", "8.8", "Sofía: eyebrow + eye-roll pop")
    KEYS[16] = (KEYS[16][0], "8d", "21.7", "Sofía: closes eyes + exhale pop")
    KEYS[18] = (KEYS[18][0], "9", KEYS[18][2], "pats her hair: blush + heart pop")
    frames = [str(int(round(t * 30))) for t, *_ in KEYS]
    d = "/tmp/tgsb_sheet"; os.makedirs(d, exist_ok=True)
    subprocess.run([sys.executable, os.path.abspath("engine_v.py"), "tg_sb"] + frames, cwd=d, check=True)
    cols, tw, th = 9, 250, 444
    rows = (len(KEYS) + cols - 1) // cols
    W, H = cols * (tw + 14) + 24, rows * (th + 70) + 110
    im = Image.new("RGB", (W, H), (247, 245, 238))
    dr = ImageDraw.Draw(im)
    fb = ImageFont.truetype(os.path.expanduser("~/.fonts/Inter-700.ttf"), 30)
    fs = ImageFont.truetype(os.path.expanduser("~/.fonts/Inter-700.ttf"), 17)
    fr = ImageFont.truetype(os.path.expanduser("~/.fonts/Inter-400.ttf"), 15)
    dr.text((24, 24), "RAISES FOR EVERYONE  ·  SILENT STORYBOARD v3  ·  35.0 s  ·  29 key frames, 18 shots", font=fb,
            fill=(30, 40, 70))
    for i, (t, n, t0, cap) in enumerate(KEYS):
        x = 24 + (i % cols) * (tw + 14); y = 90 + (i // cols) * (th + 70)
        f = os.path.join(d, "tg_sb_%03d.png" % int(round(t * 30)))
        im.paste(Image.open(f).convert("RGB").resize((tw, th)), (x, y))
        dr.rectangle((x, y, x + tw, y + th), outline=(30, 30, 30), width=2)
        dr.text((x, y + th + 6), "%s  ·  %ss" % (n, t0), font=fs, fill=(30, 40, 70))
        dr.text((x, y + th + 30), cap[:34], font=fr, fill=(60, 60, 60))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tg_storyboard_sheet_v3.png")
