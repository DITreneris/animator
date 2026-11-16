"""Key poses for review, one per shot, on one desk geography and one water trajectory.
Usage: python3 stills.py 01 07 ..  ->  still_01.png ..   |   python3 stills.py sheet  ->  key_poses.png"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cairo
import undo as U
from undo import R, K, Sh, A, DESK, W, H

AI_X, AI_GY, AI_S = 850, 1207, .9            # MY AI behind the desk, behind the cat: the chest disc just above the cat's back
HOODY_X, HOODY_SEAT = 190, 1330
GLASS_X = 300                                # the glass pivots on its base's right corner
CAT_L = (790, DESK + 4, .85)                 # the cat facing the glass (drinking, watching)
CAT_R = (630, DESK + 4, .85)                 # the cat facing MY AI (pressing with its paw)
DISC = (AI_X, AI_GY - 130 * AI_S); DISC_R = 46 * AI_S
K.FACES['realise'] = ('open', ('worried', 'worried'), 'flat')
K.FACES['defeat'] = ('half', ('flat', 'flat'), 'flat')

def _mouth07():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4); c = cairo.Context(s)
    return U.cat(c, *CAT_L, face=-1, head_up=.45, lap=1.0, tail_to=(DISC[0] + 20, DISC[1] + 22))
END = _mouth07()                              # where every spill is headed: the fountain's landing point
def path(tip, end=END):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4); lip = U.glass(cairo.Context(s), GLASS_X, DESK, tip=tip)
    return U.arc_pts(lip, end, 990)

def wide_cam(c): c.translate(540, 1100); c.scale(1.15, 1.15); c.translate(-520, -1060)
def close_cam(c, cx, cy, k): c.translate(540, 1060); c.scale(k, k); c.translate(-cx, -cy)

def hoody(c, f, expr='shock', rot=.22, arms=('rest', 'out'), gaze=0, phone=False):
    hands, _ = R.hoody(c, HOODY_X, HOODY_SEAT, 1.0, expr=expr, pose='sit', arms=arms, rot=rot, f=f, blink=False, gaze=gaze)
    if phone: U.phone(c, hands[0][0] + 10, hands[0][1] - 30, 1.0, rot=-.25)

def scene(c, f, cam, pill, hoody_kw, glass_tip, water=None, rewind=0.0, rim=False, ghost_dx=0, ghost_kw=None,
          chev=None, cat_kw=None, ai_kw=None, glow=0.0, press=0.0, counter=None, thumb=False, cam_kw=()):
    c.save(); cam(c, *cam_kw)
    U.room(c)
    A.myai(c, AI_X, AI_GY, AI_S, **(ai_kw or dict(eye='open', arms=('down', 'down'))))
    U.undo_disc(c, AI_X, AI_GY, AI_S, glow=glow, press=press)
    if thumb: U.thumb_up(c, AI_X, AI_GY, AI_S)
    if ghost_dx: U.ghost(c, lambda c: hoody(c, f, **(ghost_kw or hoody_kw)), ghost_dx, op=.28)
    if rim: U.cyan_rim(c, lambda c: hoody(c, f, **hoody_kw), width=9)
    else: hoody(c, f, **hoody_kw)
    if chev: U.chevrons(c, *chev, .9, n=2)
    U.desk_front(c)
    U.laptop(c, 500, DESK)
    if rewind > 0: U.cyan_rim(c, lambda c: U.glass(c, GLASS_X, DESK, tip=glass_tip, fill=.6 - .5 * glass_tip / 1.1), width=7)
    else: U.glass(c, GLASS_X, DESK, tip=glass_tip, fill=.6 - .5 * glass_tip / 1.1)
    mouth = U.cat(c, *(cat_kw.pop('at', CAT_L)), f=f, **cat_kw) if cat_kw else None
    if water:
        pts, frac = water
        pts = pts[:max(3, int(len(pts) * frac))]
        U.water(c, pts, f, rewind=rewind, pulse=1.0)
        if rewind > 0 and len(pts) > 10:
            i = len(pts) // 2; U.chevrons(c, *pts[i], .7, n=2, ang=math.atan2(pts[i + 1][1] - pts[i - 1][1], pts[i + 1][0] - pts[i - 1][0]))
    if counter: U.counter(c, 560, 850, counter, k=.85)
    c.restore()
    Sh.topbar(c, pill)
    return mouth

PAW_ON = (DISC[0] - DISC_R + 10, DISC[1] + 8)

def s01(c, f=0):   # the spill: eyes on his phone, the glass mid-tip, water heading right; the cat already watching
    scene(c, f, wide_cam, 'HIS DRINK', dict(expr='shock', rot=.04, arms=('chin', 'out'), phone=True), .8,
          water=(path(.8), .55), cat_kw=dict(face=-1, eyes='track', look=-3))
def s02(c, f=0):   # the miracle: MY AI presses its chest; the spill runs backwards
    scene(c, f, wide_cam, 'HIS DRINK', dict(expr='shock', rot=.04, arms=('chin', 'out'), phone=True), .45,
          water=(path(.45), .22), rewind=1, rim=True, chev=(60, 960), cat_kw=dict(face=-1, eyes='track', look=-3),
          ai_kw=dict(eye='focus', arms=('chest', 'down')), glow=1, press=.7)
def s03(c, f=0):   # discovery, close: its eyes on the glowing button, a paw starting to rise
    scene(c, f, close_cam, 'HIS DRINK', dict(expr='happy', rot=0, arms=('rest', 'rest')), 0,
          cat_kw=dict(at=CAT_R, face=1, eyes='track', look=4, head_up=.3, paw_to=(730, 1160)), glow=.7,
          ai_kw=dict(eye='happy', arms=('down', 'down')), cam_kw=(740, 1110, 2.1))
def s04(c, f=0):   # the experiment: a sneaky grab while looking away - TAP - the glass snaps back to the table
    scene(c, f, wide_cam, 'HIS DRINK', dict(expr='smug', rot=.02, arms=('rest', 'out'), gaze=-24), 0,
          rim=True, ghost_dx=40, chev=(60, 960), rewind=1, cat_kw=dict(at=CAT_R, face=1, eyes='content', paw_to=PAW_ON),
          ai_kw=dict(eye='happy', arms=('down', 'down')), glow=1, press=.8, counter=3)
def s05(c, f=0):   # the fight: he lunges for the paw, tips the glass; the water shoots towards the cat; ears up
    scene(c, f, wide_cam, 'HIS DRINK', dict(expr='shock', rot=.3, arms=('rest', 'out')), .95,
          water=(path(.95), .62), cat_kw=dict(at=CAT_R, face=1, look_back=True, eyes='wide', ears_up=True),
          ai_kw=dict(eye='happy', arms=('down', 'down')), glow=.4, counter=3)
def s06(c, f=0):   # revelation, close: a tap while the water is in the air; it flies back; the tongue meets it
    s_ = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4)
    kw = dict(at=CAT_R, face=1, look_back=True, eyes='content', lids=.3, head_up=.35, lap=.9, paw_to=PAW_ON)
    tongue = U.cat(cairo.Context(s_), *CAT_R, **{k: v for k, v in kw.items() if k != 'at'})
    scene(c, f, close_cam, 'HIS DRINK', dict(expr='shock', rot=.3, arms=('rest', 'out')), .95,
          water=(path(.95, tongue), 1.0), rewind=1, rim=True, cat_kw=kw,
          ai_kw=dict(eye='happy', arms=('down', 'down')), glow=1, press=.8, counter=4, cam_kw=(640, 1100, 1.9))
def s07(c, f=0):   # the human fountain: tail on the button, the arc back and forth, ITS DRINK
    scene(c, f, wide_cam, 'ITS DRINK', dict(expr='shock', rot=.22), 1.05, water=(path(1.05), 1.0), rewind=1, rim=True,
          ghost_dx=-50, ghost_kw=dict(expr='shock', rot=.08), chev=(120, 900),
          cat_kw=dict(face=-1, head_up=.45, lap=1.0, tail_to=(DISC[0] + 20, DISC[1] + 22)),
          ai_kw=dict(eye='happy', arms=('offer', 'down'), tilt=-6), glow=1, press=.6, counter=9)
def s07b(c, f=0):  # the false escape: the cat pauses, time runs forward; he catches the glass, sets it upright - relief
    scene(c, f, wide_cam, 'ITS DRINK', dict(expr='hopeful', rot=.12, arms=('rest', 'out'), gaze=10), 0,
          cat_kw=dict(face=-1, head_up=.3, lap=0, lids=.8, tail_to=(DISC[0] + 40, DISC[1] - 60)),
          ai_kw=dict(eye='happy', arms=('offer', 'down'), tilt=-6), glow=.3, counter=11)
def s08(c, f=0):   # the look, close two-shot: he finds its eyes; it swallows, indifferent; his face drops into defeat
    scene(c, f, close_cam, 'ITS DRINK', dict(expr='defeat', rot=.22, gaze=26), 1.05, water=(path(1.05), 1.0), rewind=1,
          cat_kw=dict(face=-1, head_up=.25, eyes='track', look=-4, tail_to=(DISC[0] + 20, DISC[1] + 22)),
          ai_kw=dict(eye='happy', arms=('offer', 'down'), tilt=-6), glow=1, counter=12, cam_kw=(500, 1110, 1.6))
def s09(c, f=0):   # success: MY AI's proud thumb; Hoody stares at the robot, exhausted; one more lap
    scene(c, f, wide_cam, 'ITS DRINK', dict(expr='defeat', rot=.22, gaze=34), 1.05, water=(path(1.05), 1.0),
          cat_kw=dict(face=-1, head_up=.45, lap=1.0, tail_to=(DISC[0] + 20, DISC[1] + 22)),
          ai_kw=dict(eye='happy', arms=(None, 'down'), tilt=-8), thumb=True, glow=.6, counter=14)

SHOTS = {'01': s01, '02': s02, '03': s03, '04': s04, '05': s05, '06': s06, '07': s07, '07b': s07b, '08': s08, '09': s09}
def render(k):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); SHOTS[k](c, 0); return s
if __name__ == '__main__':
    keys = list(SHOTS) if sys.argv[1:] == ['sheet'] else sys.argv[1:]
    surfs = {k: render(k) for k in keys}
    for k, s in surfs.items(): s.write_to_png(os.path.join(HERE, f'still_{k}.png'))
    if sys.argv[1:] == ['sheet']:                                            # 5 x 2 contact sheet at 0.4
        sw, sh = int(W * .4), int(H * .4); out = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw * 5 + 60, sh * 2 + 150); c = cairo.Context(out)
        c.set_source_rgb(1, 1, 1); c.paint()
        for i, k in enumerate(keys):
            x, y = 10 + (i % 5) * (sw + 10), 60 + (i // 5) * (sh + 70)
            c.save(); c.translate(x, y); c.scale(.4, .4); c.set_source_surface(surfs[k]); c.paint(); c.restore()
            U.txt(c, k.replace('07b', '07 false escape'), x + sw / 2, y - 26, 34, U.NAVY, lw=0)
        out.write_to_png(os.path.join(HERE, 'key_poses.png'))
    print('ok', *keys)
