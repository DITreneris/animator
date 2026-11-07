import json,math,random,subprocess,sys,os
from functools import lru_cache
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__))
P=json.load(open(os.path.join(HERE,'plan.json')))
W,H=P['size']; FONT=os.environ.get('FONT',os.path.join(HERE,'..','fonts','Anton-Regular.ttf'))
INK=(14,14,20); WHITE=(250,250,245); GOLD=(255,212,0); RED=(255,45,70); GREEN=(43,255,136)
def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def clamp(x,a=0,b=1): return max(a,min(b,x))
def eo(p): p=clamp(p); return 1-(1-p)**3
def back(p):
    p=clamp(p); c=1.9; return 1+(c+1)*(p-1)**3+c*(p-1)**2
@lru_cache(maxsize=600)
def font(sz): return ImageFont.truetype(FONT,max(8,sz))
@lru_cache(maxsize=1500)
def txt(s,sz,col,st=0,sh=0,a=255):
    f=font(sz); l,t,r,b=f.getbbox(s,stroke_width=st); pad=sh+4
    im=Image.new('RGBA',(r-l+2*pad,b-t+2*pad),(0,0,0,0)); d=ImageDraw.Draw(im)
    if sh: d.text((pad-l+sh,pad-t+sh),s,font=f,fill=INK+(255,),stroke_width=st,stroke_fill=INK+(255,))
    d.text((pad-l,pad-t),s,font=f,fill=col+(255,),stroke_width=st,stroke_fill=INK+(255,))
    if a<255: im.putalpha(im.getchannel('A').point(lambda v:v*a//255))
    return im
def put(img,s,x,y,sz,col,st=0,sh=0,a=255,anchor='c',rot=0):
    t=txt(s,int(sz),col,st,sh,int(a))
    if rot: t=t.rotate(rot,expand=True,resample=Image.BICUBIC)
    px=int(x-(t.width/2 if anchor=='c' else 0)); py=int(y-t.height/2)
    img.paste(t,(px,py),t)
def slam(n,n0,dur=6,big=.85):
    if n<n0: return None
    p=(n-n0)/dur
    return 1+big*(1-eo(p)) if p<1 else 1
# backgrounds
def mkbg(c1,c2):
    yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/W)**2+((yy-H/2)/H)**2)/.72
    d=np.clip(d,0,1)[...,None]; a=np.array(c1)*(1-d)+np.array(c2)*d
    a+=np.random.default_rng(3).normal(0,1.6,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))
BG=mkbg((30,30,44),(9,9,14)); BGR=mkbg((86,10,24),(18,4,8))
@lru_cache(maxsize=24)
def bg(q):
    return BG if q==0 else BGR if q==10 else Image.blend(BG,BGR,q/10)
# particles
R=random.Random(11)
BURST=[(R.uniform(-1,1),R.uniform(-1,1),R.uniform(500,1700),R.uniform(0,6.3),R.uniform(-9,9),R.choice([0,0,1,2]),R.uniform(.7,1.4)) for _ in range(150)]
RAIN=[(R.uniform(0,W),R.uniform(0,1),R.uniform(.4,.9),R.uniform(0,6.3),R.uniform(-3,3),R.uniform(.5,1.1)) for _ in range(26)]
def quad(d,x,y,w,h,a,fill):
    c,s=math.cos(a),math.sin(a)
    d.polygon([(x+c*u-s*v,y+s*u+c*v) for u,v in ((-w,-h),(w,-h),(w,h),(-w,h))],fill=fill)
def burst(img,n,n0):
    d=ImageDraw.Draw(img); t=(n-n0)/30
    for vx,vy,sp,ph,rv,k,z in BURST:
        m=math.hypot(vx,vy)+.01
        x=W/2+vx/m*sp*t; y=860+vy/m*sp*t-300*t+1500*t*t
        a=ph+rv*t
        if k==0: quad(d,x,y,44*z,22*z,a,(46,200,110)); quad(d,x,y,12*z,12*z,a,(210,255,220))
        elif k==1: quad(d,x,y,20*z,20*z*abs(math.cos(a*2))+3,0,GOLD)
        else: quad(d,x,y,12*z,7*z,a,WHITE)
def rain(img,n):
    d=ImageDraw.Draw(img)
    for x,y0,v,ph,rv,z in RAIN:
        y=((y0+v*n/30)%1.1)*H*1.0-60; a=ph+rv*n/30; xx=x+30*math.sin(ph+n/12)
        quad(d,xx,y,46*z,23*z,a,(32,120,74)); quad(d,xx,y,13*z,13*z,a,(52,170,105))
def rays(img,n,a=255):
    ov=Image.new('RGB',(W,H),(255,150,0)); d=ImageDraw.Draw(ov); c=(W/2,860); rr=2400; base=n*.025
    for i in range(14):
        t0=base+i*2*math.pi/14; t1=t0+math.pi/14
        d.polygon([c,(c[0]+rr*math.cos(t0),c[1]+rr*math.sin(t0)),(c[0]+rr*math.cos(t1),c[1]+rr*math.sin(t1))],fill=GOLD)
    return Image.blend(img,ov,a/255) if a<255 else ov
# table
CX=[170,390,610,830]; ROWY=[(410,510),(650,750),(890,990),(1210,1320)]
def ty(n):
    v=470
    for f,a,b in ((105,470,350),(150,350,220),(270,220,0)):
        if n>=f: v=a+(b-a)*eo((n-f)/8)
    return v
def table(img,n,S=1,TY=0,focus=None):
    TX=lambda x:540+(x-540)*S; TYY=lambda y:300+(y-300)*S+TY
    d=ImageDraw.Draw(img,'RGBA')
    for i,cx in enumerate(CX):
        s=slam(n,60+i*3,5,.4)
        if s: put(img,f'MONTH {i+1}',TX(cx),TYY(300),40*S*s,(170,170,185))
    # divider
    if n>=270:
        w=eo((n-270)/12); y=TYY(1125)
        d.rectangle([TX(60),y-4*S,TX(60)+(TX(960)-TX(60))*w,y+4*S],fill=WHITE+(255,))
    for r,row in enumerate(P['rows']):
        col=rgb(row['color']); ly,vy=ROWY[r]; active=row['label_f']<=n<row['f'][3]+15
        dim=255
        if n>=row['f'][3]+15 and n<360 and n>=270 and r<3: dim=95
        s=slam(n,row['label_f'],6,.6)
        if s is None: continue
        if active and S==1:
            d.rounded_rectangle([50,ly-65+TY,1000,vy+70+TY],26,fill=col+(30,))
        put(img,row['label'],TX(70),TYY(ly),74*S*s,col if dim==255 else tuple(c//2+40 for c in col),anchor='l')
        for i,v in enumerate(row['values']):
            f=row['f'][i]; sv=slam(n,f,6,1.1)
            if sv is None: continue
            c=WHITE
            if r==2: c=(120,120,135) if i<3 else GOLD
            if r==3: c=RED
            if dim!=255: c=tuple(x//2+15 for x in c)
            y=TYY(vy)
            if r==3: y+=int(26*S*(1-eo((n-f)/5))*-3)
            put(img,v,TX(CX[i]),y,(82 if r==3 else 90 if r==1 else 98 if v!='$600k' else 92)*S*sv,c,sh=int(5*S))
# character
@lru_cache(maxsize=300)
def head(brow,mouth,look,blink):
    Z=2;C=1000*Z; im=Image.new('RGBA',(C,C),(0,0,0,0)); d=ImageDraw.Draw(im)
    def e(x0,y0,x1,y1,**k): d.ellipse([x0*Z,y0*Z,x1*Z,y1*Z],**k)
    OUT=(20,18,28);SK=(244,190,146);HAIR=(112,72,196)
    # hair back+spikes
    pts=[(235,500),(215,350),(270,370),(255,250),(345,300),(370,175),(450,260),(530,155),(575,255),(680,185),(680,300),(770,270),(740,380),(795,370),(765,510)]
    d.polygon([(x*Z,y*Z) for x,y in pts],fill=HAIR,outline=OUT)
    # ears
    for x in (225,715): e(x,480,x+65,590,fill=SK,outline=OUT,width=10*Z)
    e(250,270,750,800,fill=SK,outline=OUT,width=10*Z)
    # fringe
    fr=[(500+250*math.cos(math.radians(a)),535+265*math.sin(math.radians(a))) for a in range(205,336,5)]+[(727,423),(670,345),(610,385),(550,330),(490,380),(420,330),(360,385),(310,345),(273,423)]
    d.polygon([(x*Z,y*Z) for x,y in fr],fill=HAIR)
    # cheeks
    for x in (300,620): e(x,590,x+80,640,fill=(240,150,130))
    # eyes
    for cx,sz in ((385,62),(615,70)):
        if blink:
            d.line([(cx-55)*Z,525*Z,(cx+55)*Z,525*Z],fill=OUT,width=12*Z)
        else:
            e(cx-sz,525-sz,cx+sz,525+sz,fill=(255,255,255),outline=OUT,width=7*Z)
            px=cx+look*sz*.42; e(px-24,501,px+24,549,fill=OUT); e(px-14,508,px-2,520,fill=(255,255,255))
    # glasses
    for cx,sz in ((385,88),(615,96)): e(cx-sz,525-sz,cx+sz,525+sz,outline=(30,30,40),width=11*Z)
    d.line([473*Z,515*Z,519*Z,515*Z],fill=(30,30,40),width=11*Z)
    d.line([297*Z,505*Z,250*Z,495*Z],fill=(30,30,40),width=10*Z); d.line([711*Z,505*Z,755*Z,495*Z],fill=(30,30,40),width=10*Z)
    # brows (one furrowed, one raised)
    b=brow/10
    d.line([310*Z,(420+4*b)*Z,455*Z,(428+8*b)*Z],fill=OUT,width=24*Z)
    d.line([545*Z,(405-35*b)*Z,705*Z,(385-50*b)*Z],fill=OUT,width=24*Z)
    # nose
    d.arc([478*Z,570*Z,530*Z,625*Z],20,170,fill=(190,120,90),width=8*Z)
    # mouth
    m=mouth/10
    mw=66; my=690
    d.polygon([(x*Z,y*Z) for x,y in [(500-mw,my+6),(500+mw,my-14),(500+mw*.7,my+22+52*m),(500-mw*.6,my+24+48*m)]],fill=(90,24,40),outline=OUT)
    d.polygon([(x*Z,y*Z) for x,y in [(500-mw+12,my+6),(500+mw-12,my-12),(500+mw-22,my+6),(500-mw+22,my+22)]],fill=(250,250,250))
    return im.resize((1000,1000),Image.LANCZOS)
BODY=None
def body():
    global BODY
    if BODY is None:
        Z=2;im=Image.new('RGBA',(1200*Z,1300*Z),(0,0,0,0));d=ImageDraw.Draw(im);OUT=(20,18,28);HO=(0,175,170)
        d.polygon([(x*Z,y*Z) for x,y in [(40,1300),(120,420),(330,250),(870,250),(1080,420),(1160,1300)]],fill=HO,outline=OUT,width=10*Z)
        d.ellipse([350*Z,150*Z,850*Z,420*Z],fill=(0,140,138),outline=OUT,width=10*Z)
        d.ellipse([470*Z,150*Z,730*Z,330*Z],fill=(40,40,50))
        d.line([520*Z,380*Z,500*Z,540*Z],fill=(245,245,245),width=14*Z); d.line([680*Z,380*Z,700*Z,540*Z],fill=(245,245,245),width=14*Z)
        BODY=im.resize((1200,1300),Image.LANCZOS)
    return BODY
def character(img,n):
    if n<360: return
    up=back((n-360)/10)
    z=1+.14*eo((n-405)/8)
    sh=(n>=405 and n<420)*14*math.sin((n-405)*1.4)*(1-(n-405)/15)
    tilt=-7+3*math.sin(n/22)+sh*.5
    brow=int(clamp(2+8*eo((n-378)/8),0,1)*10) if n<378 else 10
    brow=2 if n<378 else (7 if n<405 else 10)
    mouth=2 if n<378 else (5 if n<405 else 10)
    look=-1 if n<395 else (1 if n<425 else (-1 if n<445 else 1))
    blink=n in (370,371,399,436,437,484,485)
    h=head(brow,mouth,look,blink)
    S=.62*z
    hh=h.resize((int(1000*S),)*2,Image.BILINEAR).rotate(tilt,resample=Image.BICUBIC)
    Bb=body(); bw=int(1200*.66*z); bb=Bb.resize((bw,int(1300*.66*z)),Image.BILINEAR)
    base=1075+ (1-up)*900
    img.paste(bb,(int(540-bw/2),int(base+40)),bb)
    img.paste(hh,(int(540-hh.width/2),int(base-hh.height/2)),hh)
def caption(img,n):
    if n<378: return
    tag=n>=468
    if tag:
        s=slam(n,468,6,.5)
        put(img,'TAG A VIBE CODER',540,1470,132*s,WHITE,st=8,sh=9)
        return
    w1=[('WAIT,',378),('YOU GUYS ARE',390)]
    # lay out line 1 on full width so it does not jump
    f=font(112); full='WAIT, YOU GUYS ARE'; L=f.getlength(full); x0=540-L/2
    s=slam(n,378,5,.5); put(img,'WAIT,',x0,1405,112*s,WHITE,st=8,sh=8,anchor='l')
    if n>=390:
        s=slam(n,390,5,.35); put(img,'YOU GUYS ARE',x0+f.getlength('WAIT, '),1405,112*s,WHITE,st=8,sh=8,anchor='l')
    if n>=405:
        s=slam(n,405,6,.8); put(img,'GETTING PAID?',540,1540,132*s,GOLD,st=9,sh=9)
EV=[(n,10) for n in (0,15,30)]+[(45,18)]+[(r['label_f'],6) for r in P['rows'][:3]]+[(f,4) for f in P['rows'][0]['f']+P['rows'][1]['f']]+[(165,10),(180,12),(195,14),(225,46),(270,20)]+[(f,14+i*5) for i,f in enumerate(P['rows'][3]['f'])]+[(405,22),(450,20),(468,10)]
def shake(n):
    x=y=0
    for f,a in EV:
        if 0<=n-f<10:
            k=a*(1-(n-f)/10)**2; x+=k*math.sin((n-f)*2.3+f); y+=k*math.cos((n-f)*2.9+f*.7)
    return x,y
def frame(n):
    q=0
    if 285<=n<360: q=int(10*eo((n-285)/60))
    elif 360<=n: q=max(0,10-int((n-360)/4))
    img=bg(q).copy()
    zoom=1
    if n<60:
        rain(img,n)
        s=1.15-.15*eo(n/5); put(img,'WHO',540,600,330*s,WHITE,sh=12)
        if n>=15: put(img,'GETS',540,930,330*slam(n,15,5,.5),WHITE,sh=12)
        if n>=30:
            s=slam(n,30,5,.6)*(1+.07*eo((n-45)/5)); put(img,'PAID?',540,1270,350*s,GOLD,sh=12)
    elif n<225 or n>=270:
        if n<360:
            if 150<=n<225: zoom=1+.16*eo((n-165)/60)**2
            if 285<=n<360: zoom=1+.06*(n-285)/75
            table(img,n,1,ty(n))
        else:
            p=eo((n-360)/12); S=1-.42*p; TY=-90*p
            table(img,n,S,TY)
            character(img,n)
            caption(img,n)
            if n>=450:
                s=slam(n,450,6,1.1)
                t0=txt('TOTAL: -$800',int(120*s),RED)
                pl=Image.new('RGBA',(t0.width+70,t0.height+56),(0,0,0,0)); dd=ImageDraw.Draw(pl)
                dd.rounded_rectangle([3,3,pl.width-4,pl.height-4],24,fill=(250,245,235,255),outline=RED+(255,),width=10)
                pl.alpha_composite(t0,(35,28))
                pl=pl.rotate(-6,expand=True,resample=Image.BICUBIC)
                img.paste(pl,(int(540-pl.width/2),int(560-pl.height/2)),pl)
    else:
        # founder payoff: big $600K over sunburst
        table(img,n,1,ty(n))
        fade=255 if n<258 else int(255*(1-(n-258)/12))
        img=rays(img,n,fade)
        fly=eo((n-256)/12)
        s=slam(n,225,5,1.0)*(1+.05*math.sin((n-225)*.9))
        bx=540+(CX[3]-540)*fly; by=860+(ROWY[2][1]+220-860)*fly; sz=(280+(92-280)*fly)*s
        burst(img,n,225)
        put(img,'$600K' if fly<.8 else '$600k',bx,by,sz,GOLD if fly>.5 else WHITE,st=int(10*(1-fly)),sh=int(14*(1-fly)+3))
        if n<252:
            put(img,'FOUNDER',540,560,120*slam(n,225,5,.4),INK)
    x,y=shake(n)
    if zoom!=1 or x or y:
        a=1/zoom; cx,cy=W/2,860
        img=img.transform((W,H),Image.AFFINE,(a,0,cx-a*cx-x,0,a,cy-a*cy-y),resample=Image.BILINEAR)
    if n==225: img=Image.blend(img,Image.new('RGB',(W,H),WHITE),.6)
    return img
if __name__=='__main__':
    if sys.argv[1]=='check':
        os.makedirs(os.path.join(HERE,'check'),exist_ok=True)
        for n in map(int,sys.argv[2:]): frame(n).save(os.path.join(HERE,'check',f'f{n:03d}.jpg'),quality=88)
    else:
        os.makedirs(os.path.join(HERE,'scenes'),exist_ok=True)
        sc=P['scenes'][int(sys.argv[2])]; out=os.path.join(HERE,'scenes',f"{int(sys.argv[2]):02d}")
        ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-crf','17','-preset','veryfast','-g','30','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',out+'.tmp.mp4'],stdin=subprocess.PIPE)
        for n in range(sc['start'],sc['end']): ff.stdin.write(frame(n).tobytes())
        ff.stdin.close()
        if ff.wait()==0: os.rename(out+'.tmp.mp4',out+'.mp4')
