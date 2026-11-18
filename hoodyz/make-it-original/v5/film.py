"""Make It Original v5: the loop. Everything up to 18.1 s is v4 (imported, not copied); the office tail is replaced by a
stadium bookend in frame 0's exact framing: the cat on HIS stage playing the riff with one lazy paw, old Hoody in the
front row playing air guitar, the cat yawning on the last note. The cut lands on frame 0, the year flips 2026 -> 1986,
and the riff carries straight through it. "NOW THAT'S ORIGINAL!" holds 1.2 s.
python3 film.py keys | t ... | seam | (no args: full render; needs fin.wav from mix5.py)"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(HERE, '..', 'v4'); sys.path.insert(0, V4)
_cwd = os.getcwd(); os.chdir(V4)
import film as F4                                  # v4's shots, timing and lip flap, unchanged
os.chdir(_cwd)
from film import A, G, D, R86, END, NF, FPS, W, H, SHOTS, KEY_T, NAMES, sub, guitar, lazy_cat, paw_motif, crowd, dream_edge
from cast import hoodyz, topbar_a, ell, YEL, cl, lerp, ss
from timeline import ONSETS
P2 = G['demo'] + 2.0                               # the cat's second pass: its last note ends exactly on the loop point

def paw_at(t, t0):
    paw, hit = 0.0, False
    for o in ONSETS:
        d = t - t0 - o
        if -.08 <= d < 0: paw = max(paw, 1 + d / .08)
        elif 0 <= d < .15: paw = max(paw, 1 - d / .15 * .7)
        if 0 <= d < .08: hit = True
    return paw, hit

def s19(c, t, f):  # (local time) frame 0's stadium, the same camera; the cat has his stage, he's in the crowd
    tg = t + D
    k = lerp(1.05, 1.0, cl((tg - G['back']) / .25)); A.cam(c, k, 540, 1060, 540, 1060)   # eases into frame 0's exact framing
    A.stadium(c, tg, wide=True, flash=A.note_hit(tg, P2))
    guitar(c, 400, 1420, 1.45, rot=0)
    paw, hit = paw_at(tg, P2)
    last = P2 + ONSETS[-1]
    yawn = math.sin(math.pi * cl((tg - last - .05) / .4)) if tg > last + .05 else 0
    tip = lazy_cat(c, 570, 1400, 1.5, paw, yawn, f)
    if hit: ell(c, tip[0], 1420, 60, 14); c.set_source_rgba(*YEL, .85); c.fill()
    paw_motif(c, tg, P2, 490, 830, 1.0, life=1.6)
    crowd(c, tg, 1600)
    bob = .07 * math.sin((tg - P2) / .25 * math.pi)                                    # old Hoody in the front row, air guitar, smug
    hoodyz(c, 880, 2190, .95, 2026, 'smuggrin', 'air', f, head_rot=-.06 + bob, lean=-.04)
    dream_edge(c)

F4.LATE[19] = s19
NAMES[19] = 'the stadium again: the cat on his stage, him in the crowd'
KEY_T[19] = 19.0

def subs(c, t, year):
    topbar_a(c, year)
    sub(c, t, G['drum'], G['drum'] + 1.4, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, G['ask'], G['ask'] + 1.7, 'MAKE SOMETHING|COMPLETELY ORIGINAL.')
    sub(c, t, G['know'], G['know'] + 1.12, 'PLAY SOMETHING WE KNOW.')
    sub(c, t, G['orig'], G['orig'] + 1.2, "NOW THAT'S ORIGINAL!")
F4.subs = subs

if __name__ == '__main__':
    a = sys.argv[1:]
    os.chdir(HERE)
    if a and a[0] == 'keys': F4.keys()
    elif a and a[0] == 'seam':                                   # the loop point: the last frame beside frame 0
        from PIL import Image
        im = Image.new('RGB', (1080, 960), 'white')
        for i, fr in enumerate((NF - 1, 0)): im.paste(F4.frame_img(fr).resize((540, 960)), (i * 540, 0))
        im.save('keys/seam.png'); Image.blend(F4.frame_img(NF - 1), F4.frame_img(0), .5).resize((540, 960)).save('keys/overlay_seam.png'); print('seam ok')
    elif a:
        for x in a: fr = int(round(float(x) * FPS)); F4.draw(fr).write_to_png(f'chk_{fr:03d}.png')
    else: F4.render('make_it_original_v5.mp4')
