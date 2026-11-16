# v3.4 polish layer (V34=1): camera push-ins on the key beats, punch line back on the final image,
# a readable 2024 APPROVE button, a flash when the robot grabs the button, eased arm moves.
# Picture only: timing, voices and audio are unchanged. Without V34=1 nothing here is installed.
import os,math
import v9,titles,chars
from v import *
V34=os.environ.get('V34')=='1'
V35=os.environ.get('V35')=='1'   # v3.5 fixes on top of v3.4 (implies V34): skin hand on the 2024 pat, later payoff push, clearer dog, pat rests on the hair
if V35:V34=True
def ease_ob(t):
    """Small wind-up at the start, overshoot at the end (softened easeInOutBack)."""
    t=cl(t);c2=1.2*1.525
    return (2*t)**2*((c2+1)*2*t-c2)/2 if t<.5 else ((2*t-2)**2*((c2+1)*(2*t-2)+c2)+2)/2
def push(c,f,keys):
    """keys: (frame, k, fx, fy, tx, ty): world point (fx,fy) shown at screen (tx,ty), scaled k. Smoothstep between keys."""
    if f<=keys[0][0]:p=keys[0][1:]
    elif f>=keys[-1][0]:p=keys[-1][1:]
    else:
        for a,b in zip(keys,keys[1:]):
            if a[0]<=f<b[0]:
                t=(f-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);p=[lerp(x,y,t) for x,y in zip(a[1:],b[1:])];break
    k,fx,fy,tx,ty=p
    c.translate(tx,ty);c.scale(k,k);c.translate(-fx,-fy)
WIDE=(1,540,960,540,960)
CAM={
 'A':[(0,)+WIDE,(20,1.3,600,1400,540,1420)],                                   # opening: his face on the ground
 'C':[(148,)+WIDE,(154,1.25,560,1330,540,1250),(168,1.25,560,1330,540,1250),(176,)+WIDE],   # first APPROVE press
 'E':[(390,)+WIDE,(398,1.3,560,1100,540,1050)],                                # "Did you read it?" / "Approve."
 'F':[(466,)+WIDE,(472,1.4,420,1010,480,1000),(478,1.4,420,1010,480,1000),     # "...Approve." on his face
      (482,1.5,640,1330,540,1250),(500,1.5,640,1330,540,1250),(510,)+WIDE],   # the robot grabs the button
 'G':[(652,)+WIDE,(664,1.3,650,1100,600,1180)],                               # payoff: pats, ball in his mouth
}
if V35:CAM['G']=[(668,)+WIDE,(680,1.3,650,1100,600,1180)]   # v3.5: push only once he has run fully back into frame
CAPTION_AT=684 if V35 else 676
FLASH={155:.35,485:.55}   # first press (2024), the robot's grab (2026)
def screen(fn):
    def g(c,*a,**k):
        c.save();c.identity_matrix();r=fn(c,*a,**k);c.restore();return r
    return g
def C34(c,f):
    """2024 scene: as v9.C, with a bigger, readable APPROVE button and an eased press."""
    r=f-75;v9.room(c);v9.desk(c,1290)
    pat=r<52;tap=72<=r<92;press=1 if 80<=r<86 else 0
    rb=abs(math.sin(r*.5))*10 if r>=90 else 0
    ry=v9.bot(c,760,1290,.6,walk=0,glow=.55 if pat else 1,eye=(0,-4) if pat else (0,0),bob=rb)
    v9.button(c,560,1400,1.45,press)
    gx,gy=360,880
    v9.torso(c,gx,gy+150*1.25,1.5)
    if pat:
        p=abs(math.sin(r*.45))*16
        if V35:   # v3.5: sleeve, then a skin-coloured hand on the robot's head (was a navy disc)
            limb(c,[(gx+112,gy+215),(gx+250,gy+110),(760,ry-62+p)],52,NAVY);ell(c,760,ry-70+p,32,30);fs(c,SKIN,7)
        else:v9.rarm(c,[(gx+112,gy+215),(gx+250,gy+110),(760,ry-70+p)],52,NAVY)
    elif r<72 or r>=92:
        v9.rarm(c,[(gx+112,gy+215),(gx+190,gy+330),(gx+150,gy+380)],52,NAVY)
    else:
        k=ease_ob((r-72)/8) if r<86 else 1-cl((r-86)/6)
        v9.rarm(c,[(gx+112,gy+215),(lerp(gx+190,520,k),lerp(gx+330,1265,k)),(lerp(gx+150,560,k),lerp(gx+380,1318+press*22,k))],52,NAVY)
    if r>=46:v9.rarm(c,[(gx-112,gy+215),(gx-230,gy+260),(gx-150,gy+120)],52,NAVY)
    v9.guyhead(c,gx,gy,1.35,'happy',0)
    if r>=46:v9.sandwich(c,gx-120,gy+100,1.3,bite=r>70)
    if 55<=r<88:v9.holo(c,760,ry-200,'HELP?',max(.02,back((r-55)/4)))
    if r>=90:
        for i in range(3):
            a=r*.3+i*2;ell(c,760+math.cos(a)*120,ry-20+math.sin(a)*60,8,8);c.set_source_rgb(*YEL);c.fill()
    v9.sub(c,f,81,122,"WHO'S A GOOD BOY?")
def dog_lie35(c,x,gy,s):
    """v3.5: a lying dog that reads at phone size: outline, lighter muzzle, floppy ear, eye, red collar, tail."""
    BROWN,DARK=v9.BROWN,v9.DARK
    c.move_to(x+80*s,gy-22*s);c.curve_to(x+120*s,gy-26*s,x+140*s,gy-50*s,x+128*s,gy-62*s);c.set_source_rgb(*INK);c.set_line_width(18*s);c.stroke_preserve();c.set_source_rgb(*BROWN);c.set_line_width(10*s);c.stroke()
    ell(c,x+22*s,gy-30*s,78*s,32*s);fs(c,BROWN,7)
    ell(c,x+30*s,gy-16*s,52*s,12*s);c.set_source_rgba(1,.9,.75,.55);c.fill()
    for q in(0,1):ell(c,x-60*s+q*28*s,gy-8*s,26*s,12*s);fs(c,BROWN,5)
    hx_,hy=x-48*s,gy-52*s
    ell(c,hx_,hy,42*s,36*s);fs(c,BROWN,7)
    ell(c,hx_-36*s,hy+12*s,24*s,17*s);fs(c,hx('d9a066'),5);ell(c,hx_-56*s,hy+6*s,8*s,7*s);c.set_source_rgb(*INK);c.fill()
    c.save();c.translate(hx_+18*s,hy+6*s);c.rotate(.35);ell(c,0,0,15*s,32*s);fs(c,DARK,5);c.restore()
    c.arc(hx_-14*s,hy-8*s,8*s,math.pi*.15,math.pi*.85);c.set_source_rgb(*INK);c.set_line_width(5*s);c.stroke()   # happy closed eye
    c.save();c.translate(hx_+26*s,hy+26*s);c.rotate(-.9);rr(c,-26*s,-7*s,52*s,14*s,6*s);fs(c,RED,4);c.restore()   # collar
    return (hx_+30*s,hy+30*s)
def install():
    if not V34:return
    if V35:
        _dog,_rarm=v9.dog,v9.rarm
        def dog(c,x,gy,s,pose='sit',*a,**k):
            if 540<=chars.CURF<720 and pose=='lie':   # payoff: bigger, clearer, out of the button area
                X,GY=620,gy+30;chars.shadow(c,X+10,GY,120);return dog_lie35(c,X,GY,s*1.25)   # in front of him, not under his feet
            return _dog(c,x,gy,s,pose,*a,**k)
        def rarm(c,pts,w,*a):
            if 540<=chars.CURF<720 and pts and abs(pts[-1][0]-770)<1 and w==56:   # the robot's pat rests on top of his hair
                pts=list(pts[:-1])+[(770,pts[-1][1]-50)]
            return _rarm(c,pts,w,*a)
        v9.dog,v9.rarm=dog,rarm
    _qsub=v9.sub
    def sub(c,f,a,b,t,*x,**k):
        if f<60:   # opening: lifted clear of his face in the push-in
            y0=titles.SUB_Y;titles.SUB_Y=1220;r=titles.sub(c,f,a,b,t,*x,**k);titles.SUB_Y=y0;return r
        if 315<=f<540:   # office: above the zoomed-in desk and button, in the open wall space
            y0=titles.SUB_Y;titles.SUB_Y=540;r=titles.sub(c,f,a,b,t,*x,**k);titles.SUB_Y=y0;return r
        return _qsub(c,f,a,b,t,*x,**k)
    v9.sub=screen(sub);v9.badge=screen(v9.badge)
    for i,(n,a,b,fn) in enumerate(v9.SC):
        if n=='C':fn=C34
        def wrapped(c,f,fn=fn,n=n):
            c.save()
            if n in CAM:push(c,f,CAM[n])
            fn(c,f);c.restore()
            if f in FLASH:c.rectangle(0,0,W,H);c.set_source_rgba(1,1,1,FLASH[f]);c.fill()
            if n=='G' and f>=CAPTION_AT:   # the punch line back on the final image
                y0=titles.SUB_Y;titles.SUB_Y=860;titles.sub(c,f,CAPTION_AT,720,"WHO'S A GOOD BOY?");titles.SUB_Y=y0
        v9.SC[i]=(n,a,b,wrapped)
