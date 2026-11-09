# Character polish layer: expressions, robot screen faces, blinks, breathing, lip flap, contact shadows.
import math,random,subprocess
import numpy as np
import v,v6,v8,v9
from v import ell,fs,rr,limb,txt,hx,INK,WHITE,SKIN,GREY,BLUE,RED,lerp,cl,shades
CURF=0
ROSE=(1,.55,.6)
# ---------- lip flap from the voice files (same placements as audio.py) ----------
def _env():
    sr=16000;n=int(24*30);e=np.zeros(n)
    for name,t in(('wait',.2),('good',2.72),('appr',14.1),('appr2',15.65)):
        x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'vo/v_{name}.wav','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
        hop=sr//30
        r=np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(len(x)//hop)])
        r=r/(r.max()+1e-9)
        f0=int(round(t*30))
        for i,val in enumerate(r):
            if f0+i<n:e[f0+i]=max(e[f0+i],val)
    return e
ENV=_env()
def talk(f):
    if f<len(ENV) and ENV[f]>.12:return ENV[f]
    if 127<=f<200 and (f//4)%2==0:return .35   # chewing the sandwich
    return 0
# ---------- timing maps ----------
GUY=[(0,60,'panic',0),(75,127,'adoring',0),(127,210,'happy',0),(210,258,'sideeye',-14),(258,285,'shock',0),(285,315,'panic',0),
     (315,345,'calm',0),(345,435,'deadpan',8),(435,469,'calm',0),(469,493,'sheepish',0),(493,501,'calm',0),(501,519,'sheepish',10),(519,540,'shock',0),
     (540,586,'sideeye',-12),(586,598,'offended',0),(598,608,'shock',18),(608,640,'happy',0),(640,720,'proud',0)]
BOT=[(0,60,'happy'),(75,127,'happy'),(157,210,'love'),(222,258,'wide'),(258,315,'happy'),(479,497,'happy'),(497,521,'nope'),(521,540,'happy'),
     (540,586,'love'),(586,600,'happy'),(600,620,'wide'),(620,686,'happy'),(686,720,'love')]
LEGACY={'small':'shock','focus':'offended','cry':'sheepish','calm':'calm','happy':'happy'}
def pick(tbl,f):
    for row in tbl:
        if row[0]<=f<row[1]:return row
    return None
def blinking(f,seed):
    w=f//84;o=random.Random(w*31+seed).randint(0,76);return o<=f%84<o+3
# ---------- shadows ----------
def shadow(c,x,y,w):
    ell(c,x,y,w,w*.16);c.set_source_rgba(.1,.12,.18,.18);c.fill()
# ---------- guy head ----------
def head2(c,x,y,s,expr='calm',cool=False,rot=0,f=0):
    row=pick(GUY,CURF);gaze=0
    if row:expr,gaze=row[2],row[3]
    else:expr=LEGACY.get(expr,expr)
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    HAIR=v.HAIR
    blobs=[(-92,-58,48),(-55,-104,54),(5,-122,58),(62,-100,52),(98,-52,44),(-108,-8,32),(112,-6,30),(-25,-132,36),(40,-136,32)]
    bob=math.sin(CURF*.5)*2
    for b in blobs: ell(c,b[0],b[1]+bob,b[2],b[2])
    c.set_source_rgb(*INK);c.set_line_width(16);c.stroke()
    for q in(-1,1): ell(c,q*104,18,18,24);fs(c,SKIN,7)
    rr(c,-100,-72,200,178,84);fs(c,SKIN)
    rnd=random.Random(4);c.set_source_rgba(*HAIR,.5)
    for i in range(30):
        a=rnd.uniform(.2*math.pi,.8*math.pi);r=rnd.uniform(.88,1)
        ell(c,math.cos(a)*84*r,20+math.sin(a)*80*r,2,2);c.fill()
    if v.BEARD:
        c.save();rr(c,-100,-72,200,178,84);c.clip();ell(c,0,112,104,66);c.set_source_rgb(*HAIR);c.fill()
        ell(c,0,66,40,24);c.set_source_rgb(*SKIN);c.fill();c.restore()
    for b in blobs: ell(c,b[0],b[1]+bob,b[2],b[2])
    c.set_source_rgb(*HAIR);c.fill()
    for bx,by,br in[(-72,-46,32),(-30,-58,33),(18,-62,32),(62,-46,30)]:ell(c,bx,by+bob*.5,br,br);c.fill()
    face(c,expr,gaze,blinking(CURF,int(x)%7),talk(CURF))
    c.restore()
def eye_open(c,q,gx,big=False,lid=0,narrow=False):
    ey=8
    if big:
        ell(c,q*42,ey,30,34);fs(c,WHITE,6);ell(c,q*42+gx*.6,ey,10,12);c.set_source_rgb(*INK);c.fill();return
    h=14 if narrow else 27
    ell(c,q*42+gx*.5,ey+(6 if narrow else 0),23,h);c.set_source_rgb(*INK);c.fill()
    ell(c,q*34+gx*.5,ey-8,7,7);c.set_source_rgb(1,1,1);c.fill()
    if lid:
        c.rectangle(q*42-30,ey-34,60,34*lid+2);c.set_source_rgb(*SKIN);c.fill()
        c.move_to(q*42-26,ey-34+34*lid);c.line_to(q*42+26,ey-34+34*lid);c.set_source_rgb(*INK);c.set_line_width(7);c.stroke()
def eye_closed(c,q,happy=True):
    if happy:c.move_to(q*62,22);c.curve_to(q*50,0,q*20,0,q*12,22)
    else:c.move_to(q*62,10);c.curve_to(q*50,18,q*22,18,q*14,10)
    c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
def brow(c,q,kind):
    if not kind:return
    if kind=='angry':c.move_to(q*74,-34);c.line_to(q*18,-12)
    elif kind=='worried':c.move_to(q*72,-22);c.line_to(q*20,-40)
    elif kind=='raised':c.move_to(q*72,-38);c.curve_to(q*56,-56,q*30,-56,q*18,-42)
    elif kind=='flat':c.move_to(q*70,-26);c.line_to(q*20,-26)
    c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
def mouth(c,kind,op):
    c.set_source_rgb(*INK);c.set_line_width(6)
    if op>0:
        h=8+op*26;ell(c,0,70,16+op*6,h/2+4);fs(c,hx('7a2230'),6);return
    if kind=='smile':c.arc(-11,62,11,.2,math.pi-.1);c.new_sub_path();c.arc(11,62,11,.1,math.pi-.2);c.stroke()
    elif kind=='grin':
        c.move_to(-30,60);c.curve_to(-20,96,20,96,30,60);c.close_path();fs(c,hx('7a2230'),6)
    elif kind=='o':ell(c,0,72,13,17);fs(c,hx('7a2230'),5)
    elif kind=='bigo':ell(c,0,74,22,28);fs(c,hx('7a2230'),6)
    elif kind=='flat':c.move_to(-18,68);c.line_to(18,68);c.stroke()
    elif kind=='frown':c.arc(0,84,18,math.pi+.5,2*math.pi-.5);c.stroke()
    elif kind=='wobble':c.move_to(-22,70);c.curve_to(-10,60,-4,80,6,68);c.curve_to(12,62,18,74,24,68);c.stroke()
def blush(c):
    for q in(-1,1):ell(c,q*62,44,18,10);c.set_source_rgba(*ROSE,.55);c.fill()
FACES={'calm':('open',None,'smile'),'adoring':('happy','raised','grin'),'happy':('happy',None,'grin'),'panic':('big','worried','bigo'),
'shock':('big','raised','o'),'offended':('narrow','angry','frown'),'deadpan':('half','flat','flat'),'sheepish':('open','worried','wobble'),
'sideeye':('half',None,'flat'),'proud':('happy','raised',None)}
def face(c,expr,gx,blink,op):
    e,b,m=FACES.get(expr,FACES['calm'])
    for q in(-1,1):
        brow(c,q,b)
        if e=='happy':eye_closed(c,q,True)
        elif blink:eye_closed(c,q,False)
        elif e=='big':eye_open(c,q,gx,big=True)
        elif e=='narrow':eye_open(c,q,gx,narrow=True)
        elif e=='half':eye_open(c,q,gx,lid=.5)
        else:eye_open(c,q,gx)
    if expr in('adoring','proud','happy'):blush(c)
    if m:mouth(c,m,op)
# ---------- robot ----------
def visor(c,emote,eye,glow,tw,blink):
    rr(c,-82,-54,164,92,40);fs(c,hx('0b1020'),6)
    c.set_source_rgb(*BLUE)
    if emote=='happy':
        for q in(-1,1):c.arc(q*36,4,18,math.pi+.2,2*math.pi-.2);c.set_line_width(10);c.stroke()
    elif emote=='love':
        for q in(-1,1):
            k=1+.08*math.sin(CURF*.6);c.save();c.translate(q*36,-6);c.scale(k,k)
            c.move_to(0,16);c.curve_to(-26,-4,-14,-24,0,-10);c.curve_to(14,-24,26,-4,0,16);c.set_source_rgb(*hx('ff5c8a'));c.fill();c.restore()
    elif emote=='wide':
        for q in(-1,1):ell(c,q*36,-8,22,28);c.set_source_rgb(*BLUE);c.fill();ell(c,q*30,-16,6,6);c.set_source_rgb(1,1,1);c.fill()
    elif emote=='nope':
        for q in(-1,1):c.move_to(q*36-16,-8);c.line_to(q*36+16,-8);c.set_line_width(10);c.stroke()
    elif blink:
        for q in(-1,1):c.move_to(q*36-16,-4);c.line_to(q*36+16,-4);c.set_line_width(8);c.stroke()
    else:
        for q in(-1,1):ell(c,q*36+eye[0],-8+eye[1],18,(23*glow+1)*(tw if q==1 else 1));c.fill()
def robot2(c,x,y,s,boss=False,walk=None,glow=1,rot=0,noshade=False,peek=0,eye=(0,0),tw=1,emote=None,seed=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    import cairo;c.set_line_cap(cairo.LINE_CAP_ROUND)
    if walk is not None:
        a=math.sin(walk)*26
        limb(c,[(-34,205),(-34-a,280)],34,WHITE);limb(c,[(34,205),(34+a,280)],34,WHITE)
    br=1+.015*math.sin(CURF*.16+seed)
    c.save();c.translate(0,85);c.scale(1,br);rr(c,-72,0,144,135,44);fs(c,WHITE);ell(c,0,65,30,30);fs(c,(.82,.86,.93),5);c.restore()
    wob=math.sin(CURF*.45+seed)*9
    c.move_to(0,-90);c.curve_to(0,-110,wob*.5,-122,wob,-132);c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
    ell(c,wob,-140,17,17);fs(c,BLUE,7)
    for q in(-1,1):ell(c,q*110,0,22,38);fs(c,GREY,8)
    rr(c,-108,-95,216,180,78);fs(c,WHITE)
    if boss:shades(c,0,-12,1.02)
    else:visor(c,emote,eye,glow,tw,emote in(None,'eyes') and blinking(CURF,seed+3))
    c.restore()
def hero_emote():
    row=pick(BOT,CURF);return row[2] if row else None
def torso2(c,x,y,s):
    c.save();c.translate(x,y);br=1+.02*math.sin(CURF*.16+x*.01);c.scale(1,br);c.translate(-x,-y);v.torso(c,x,y,s);c.restore()
# ---------- install into the existing scene modules ----------
def install():
    for m in(v8,v9):m.head=head2;m.torso=torso2
    v6.robot=lambda c,x,y,s,**k:robot2(c,x,y,s,seed=11,**k)
    v9.robot=lambda c,x,y,s,**k:robot2(c,x,y,s,emote=hero_emote() if s>=.95 else None,seed=int(x)%9,**k)
    def bot2(c,x,gy,s,walk=0,eye=(0,0),glow=1,bob=0):
        shadow(c,x,gy,110*s);y=gy-280*s-bob;robot2(c,x,y,s,walk=walk,eye=eye,glow=glow,emote=hero_emote());return y
    v9.bot=bot2
    og,od,on,odr=v9.guyfull,v9.dog,v9.neighbor,v9.dragged
    def guyfull2(c,x,gy,s,*a,**k):shadow(c,x,gy,100*s);return og(c,x,gy,s,*a,**k)
    def dog2(c,x,gy,s,*a,**k):shadow(c,x+20*s,gy,90*s);return od(c,x,gy,s,*a,**k)
    def nb2(c,x,gy,s,*a,**k):shadow(c,x,gy,90*s);return on(c,x,gy,s,*a,**k)
    def dr2(c,x,y,s,f,*a):shadow(c,x-170*s,y+70*s,330*s);return odr(c,x,y,s,f,*a)
    v9.guyfull,v9.dog,v9.neighbor,v9.dragged=guyfull2,dog2,nb2,dr2
