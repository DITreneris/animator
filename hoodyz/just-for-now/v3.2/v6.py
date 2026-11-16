import sys,os,subprocess,math,random,cairo
import v
from v import *
GRAY=(.72,.72,.76);BROWN=(.25,.13,.09)
TAPE=hx('ffd84a');BOXC=hx('b98a58')
def old(c,x,y,s,expr='calm',gaze=0,soot=False,**k):
    v.HAIR=GRAY;v.BEARD=True;v.GAZE=gaze
    head(c,x,y,s,expr,**k)
    v.HAIR=BROWN;v.BEARD=False;v.GAZE=0
    if soot:
        r=random.Random(2)
        for i in range(5):
            ell(c,x+r.uniform(-85,85)*s,y+r.uniform(-60,-20)*s,r.uniform(14,26)*s,r.uniform(8,14)*s);c.set_source_rgba(.35,.33,.33,.3);c.fill()
def glass(c,x,y,s):
    limb(c,[(x+50*s,y+55*s),(x+105*s,y+115*s)],15*s,hx('8a5a2e'))
    ell(c,x,y,70*s,70*s);c.set_source_rgba(.75,.93,1,.35);c.fill_preserve();c.set_source_rgb(*INK);c.set_line_width(13*s);c.stroke()
    ell(c,x,y,70*s,70*s);c.set_source_rgb(*YEL);c.set_line_width(5*s);c.stroke()
    c.move_to(x-38*s,y-22*s);c.line_to(x-14*s,y-42*s);c.set_source_rgba(1,1,1,.8);c.set_line_width(6*s);c.stroke()
def tester(c,x,y,s,tape=0,eye=(0,0),glassy=True):
    robot(c,x,y,s,eye=eye)
    if glassy: glass(c,x+95*s,y+15*s,1.15*s)
    if tape:
        limb(c,[(x-60*s,y+130*s),(x-135*s,y+75*s)],22*s,WHITE)
        c.save();c.translate(x-150*s,y+55*s);c.rotate(-.4);rr(c,-14*s,-62*s,30*s,124*s,5*s);fs(c,TAPE,max(3,5*s));c.restore()
def boxfront(c,x,y,w,h,peel=0,rot=0,crack=0):
    c.save();c.translate(x,y);c.rotate(rot);k=w/200;c.scale(k,k*(h/w))
    rr(c,-100,-100,200,200,12);fs(c,BOXC,8)
    c.restore();c.save();c.translate(x,y);c.rotate(rot);c.scale(k,k)
    hh=100*h/w
    rr(c,-74,-hh+16,148,hh*.95,6);fs(c,hx('1f3f55'),5)
    txt(c,'TEMP',0,-hh+46,40,WHITE,lw=0);txt(c,'FIX',0,-hh+88,40,WHITE,lw=0)
    if peel<1:
        x0=lerp(-108,108,peel);rr(c,x0,hh-58,108-x0,44,4);fs(c,TAPE,5)
        for i in range(5):
            xx=lerp(x0,108,(i+.5)/5);c.move_to(xx,hh-52);c.line_to(xx-6,hh-20);c.set_source_rgba(.75,.55,.1,.8);c.set_line_width(3);c.stroke()
    if peel>0 and peel<1:
        x0=lerp(-108,108,peel);c.move_to(x0,hh-58);c.line_to(x0-34,hh-108);c.line_to(x0-4,hh-122);c.line_to(x0+30,hh-58);c.close_path();fs(c,TAPE,5)
    if crack:
        c.move_to(-30,-hh);c.line_to(-8,-hh*.4);c.line_to(-30,0);c.line_to(10,hh*.5);c.set_source_rgba(*INK,cl(crack));c.set_line_width(6);c.stroke()
    c.restore()
def boxback(c,x,y,w,h,flip=1):
    # doodle on the back of the box, no words
    k=w/200
    c.save();c.translate(x,y);c.scale(k*flip,k)
    hh=100*h/w
    rr(c,-100,-hh,200,hh*2,12);fs(c,BOXC,8)
    c.save();c.translate(0,-18)
    # curly hair loops
    c.set_source_rgb(*BROWN);c.set_line_width(7)
    for i in range(11):
        a_=math.pi*.98+i*(math.pi*1.04)/10
        ell(c,math.cos(a_)*50,-6+math.sin(a_)*46,17,15);c.stroke()
    c.set_source_rgb(*INK);c.set_line_width(6)
    c.move_to(-46,-6);c.curve_to(-54,50,-22,66,0,66);c.curve_to(22,66,54,50,46,-6);c.stroke()
    for q in(-1,1):ell(c,q*20,14,6,8);c.fill()
    c.arc(-8,36,8,.2,math.pi-.1);c.new_sub_path();c.arc(8,36,8,.1,math.pi-.2);c.stroke()
    for p_ in((-26,44),(-16,54),(16,54),(26,44),(0,58)):ell(c,p_[0],p_[1],2.5,2.5);c.fill()
    # hoodie and strings
    c.set_source_rgb(*NAVY);c.set_line_width(7)
    c.move_to(-60,110);c.curve_to(-58,80,-30,70,-8,70);c.move_to(60,110);c.curve_to(58,80,30,70,8,70);c.stroke()
    c.set_line_width(5);c.move_to(-8,72);c.line_to(-9,100);c.move_to(8,72);c.line_to(9,100);c.stroke()
    c.restore();c.restore()
# tower pieces: cx, cy (from box top, upward), w, h, colour, label
PIECES=[(0,-70,250,140,hx('2e9a5a'),'PAYROLL'),(-10,-240,380,200,hx('c2553d'),'OFFICE'),(25,-480,560,280,hx('37507a'),'HEADQUARTERS'),(0,-690,620,140,hx('f3e3bf'),'THE WHOLE COMPANY')]
TOP=1380
def piece(c,x,y,w,h,col,label,rot,ls):
    c.save();c.translate(x,y);c.rotate(rot)
    rr(c,-w/2,-h/2,w,h,10);fs(c,col)
    if label=='PAYROLL':   # v3.2: a cash bundle, not a building
        rr(c,-w/2+10,-h/2+10,w-20,h-20,8);c.set_source_rgba(1,1,1,.18);c.fill()
        for q in(-1,1):   # $ marks in the corners, clear of the label
            ell(c,q*(w/2-24),-h/2+24,14,14);c.set_source_rgba(1,1,1,.4);c.fill()
            txt(c,'$',q*(w/2-24),-h/2+26,22,hx('1d6b3c'),lw=0)
        c.rectangle(-w*.18,-h/2,w*.08,h);c.set_source_rgba(1,.9,.5,.8);c.fill()
    elif label!='THE WHOLE COMPANY':
        for i in range(int(w/72)):
            for j in range(max(1,int(h/66))):
                rr(c,-w/2+18+i*70,-h/2+14+j*58,42,34,4)
                c.set_source_rgba(1,.9,.5,.55 if (i+j)%3 else .22);c.fill()
    txt(c,label,0,0,ls,(.55,.08,.13) if label=='THE WHOLE COMPANY' else WHITE,lw=0 if label=='THE WHOLE COMPANY' else ls*.16)
    c.restore()
def tower(c,th=0,cx=540):
    c.save();c.translate(cx,TOP);c.rotate(th)
    # wires
    for dx in(-90,-40,40,90):
        c.move_to(dx,0);c.curve_to(dx*1.4,-60,dx,-90,dx*1.2,-120);c.set_source_rgb(*INK);c.set_line_width(7);c.stroke()
    c.restore()
    for (px,py,w,h,col,l) in PIECES:
        x=cx+px*math.cos(th)-py*math.sin(th);y=TOP+px*math.sin(th)+py*math.cos(th)
        piece(c,x,y,w,h,col,l,th,50 if l=='THE WHOLE COMPANY' else 42)
RES=[(180,1515,.42),(850,1480,-.5),(600,1450,.12),(400,1525,-.08)]
def fallen(c,t):
    # t frames after collapse; pieces drop from the tower to rest
    for i,(px,py,w,h,col,l) in enumerate(PIECES):
        sx,sy=540+px,TOP+py;ex,ey,er=RES[i];T=(16+i*3)
        delay=(3-i)*1.5;u=cl((t-delay)/T) if t>delay else 0
        x=lerp(sx,ex,u);y=sy+(ey-sy)*u*u;rot=er*oe(u)+(.06*(1-u) if u<1 else 0)
        piece(c,x,y,w,h,col,l,rot,50 if i==3 else 42)
def scene(c):
    bg(c,hx('f9cf7a'),hx('e8743b'));rays(c,WHITE,0,540,1000,.07)
    r=random.Random(4)
    for i in range(6):
        x=i*210-30;h=r.randint(60,190);c.rectangle(x,1500-h,170,h+10);c.set_source_rgba(.55,.25,.18,.25);c.fill()
    c.rectangle(0,1500,W,450);c.set_source_rgb(*hx('6a3f2d'));c.fill_preserve();c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
def caption(c):txt(c,'DAY 900',540,235,92,YEL,lw=17)
def oldguy(c,x,y,s,expr,armup=0,gaze=0,soot=False,point=False):
    torso(c,x,y+150*s,1.2*s)
    if point:
        limb(c,[(x+90*s,y+180*s),(x+190*s,y+150*s),(x+250*s,y+190*s)],44*s,NAVY);ell(c,x+262*s,y+198*s,26*s,26*s);fs(c,SKIN,7)
    if armup:
        for q in(-1,1):
            limb(c,[(x+q*88*s,y+175*s),(x+q*170*s,y+110*s),(x+q*170*s,y+30*s)],44*s,NAVY);ell(c,x+q*170*s,y+10*s,28*s,28*s);fs(c,SKIN,7)
    old(c,x,y,s*1.08,expr,gaze=gaze,soot=soot)
def bublines(c,lines,sz=88,y=620,h=240,w=860,tx=540):
    bubble(c,lines,sz,x=tx,y=y,w=w,h=h,hl=())
def S5a(c,f):
    scene(c);tower(c);boxfront(c,540,1440,150,120)
    oldguy(c,190,1140,.95,'focus',point=True)
    tester(c,850,1300,.5)
    if f>=2:bublines(c,['WHO MADE','THIS GARBAGE?!'],92,y=420,h=236)
    caption(c)
def S5b(c,f):
    r=f-36
    bg(c,hx('f9cf7a'),hx('e8743b'));rays(c,WHITE,f,540,1000,.1)
    fl=math.cos(cl(r/12)*math.pi)
    w=580;h=480
    limb(c,[(470,1420),(300,1230),(255,1170)],30,WHITE);limb(c,[(610,1420),(780,1230),(825,1170)],30,WHITE)
    tester(c,540,1370,.75,eye=(0,-10),glassy=False)
    if fl>0: boxfront(c,540,930,max(4,w*fl),h)
    else: boxback(c,540,930,w,h,flip=max(.03,-fl))
    ell(c,255,1160,30,30);fs(c,WHITE,7);ell(c,825,1160,30,30);fs(c,WHITE,7)
def S5c(c,f):
    r=f-54
    bg(c,hx('f9cf7a'),hx('d9713f'));rays(c,WHITE,f,540,1000,.07)
    gz=0 if r<14 else min(16,(r-14)*4)
    oldguy(c,540,500,1.5,'small',gaze=gz)
    # sweat
    ph=(f/12)%1;ell(c,790,430+ph*90,18,26);fs(c,hx('58c7ff'),6)
    boxback(c,540,1210,560,470)
    k=oe((r-8)/9)
    hx0=lerp(1320,560,k)
    limb(c,[(1280,1330),(hx0+120,1260)],70,NAVY);ell(c,hx0,1215,150,118);fs(c,SKIN,8)
    for i in range(3):
        c.move_to(hx0-120,1165+i*44);c.line_to(hx0-36,1165+i*44);c.set_source_rgb(*hx('d9a98a'));c.set_line_width(6);c.stroke()
    if r>=20:txt(c,'*cough*',835,700,70,INK,lw=0,rot=-.06)
def S6a(c,f):
    r=f-90
    bg(c,hx('f9cf7a'),hx('e8743b'));rays(c,WHITE,f,540,1000,.08)
    pl=cl((r-4)/18)
    sh=noise(f,1)*pl*3;c.translate(sh,0)
    boxfront(c,450,1120,600,560,peel=pl,crack=cl((r-16)/8))
    c.save();tester(c,800,720,.85,tape=0,eye=(-12,14));c.restore()
    x0=lerp(150,750,pl)
    limb(c,[(780,880),(x0+60,1190),(x0+20,1300)],32,WHITE);ell(c,x0+10,1305,30,30);fs(c,WHITE,7)
def wob(r):
    if r<18:return .05*math.sin(r*.7)*(1-r/18*.75)*min(1,r/4)
    return 0
def S6b(c,f):
    r=f-114;scene(c)
    th=wob(r)
    boxfront(c,540,1440,150,120,peel=1,crack=1);tower(c,th)
    oldguy(c,190,1140,.95,'small',armup=1)
    tester(c,850,1310,.5,tape=1,eye=(-8,6),glassy=False)
def S6c(c,f):
    r=f-138
    k=max(0,10-r);c.translate(noise(f,1)*k*3,noise(f,2)*k*3)
    scene(c)
    oldguy(c,190,1140,.95,'small',armup=1)
    tester(c,850,1310,.5,tape=1,eye=(-8,6),glassy=False)
    rr(c,465,1460,150,40,6);fs(c,BOXC,6)
    fallen(c,r)
    rr_=random.Random(6)
    for i in range(30):
        ang=rr_.uniform(0,6.28);d=r*rr_.uniform(10,30)
        size=30+r*rr_.uniform(6,14);ell(c,540+math.cos(ang)*d,1380+math.sin(ang)*d*.6,size,size*.8)
        c.set_source_rgba(.9,.84,.72,min(.9,r*.07));c.fill()
    if r>14:
        c.rectangle(0,0,W,H);c.set_source_rgba(.9,.84,.72,cl((r-14)/8));c.fill()
LINE={'back':['SHOULD I','PUT IT BACK?'],'passed':['TEST','PASSED.']}
VAR=os.environ.get('VAR','back')
def S6d(c,f):
    r=f-162
    scene(c);fallen(c,99)
    oldguy(c,160,1090,.95,'small',soot=True)
    tester(c,570,1200,.95,tape=1,eye=(0,0),glassy=False)
    if r>=6:
        k=max(.02,back((r-6)/4));c.save();c.translate(540,680);c.scale(k,k);c.translate(-540,-680)
        bublines(c,LINE[VAR],104,y=680,h=280,w=760);c.restore()
    a=1-cl(r/14)
    if a>0:
        c.rectangle(0,0,W,H);c.set_source_rgba(.9,.84,.72,a);c.fill()
SC=[('a',0,36,S5a),('b',36,54,S5b),('c',54,90,S5c),('d',90,114,S6a),('e',114,138,S6b),('f',138,162,S6c),('g',162,207,S6d)]
def draw(f):
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
    for n,a,b,fn in SC:
        if a<=f<b:fn(c,f);break
    return s
if __name__=='__main__':
    if sys.argv[1]=='frames':
        fs_=list(map(int,sys.argv[2:]))
        for f in fs_:draw(f).write_to_png(f'chk_{f:03d}.png')
        from PIL import Image
        S=Image.new('RGB',(5*360,((len(fs_)+4)//5)*640))
        for i,f in enumerate(fs_):S.paste(Image.open(f'chk_{f:03d}.png').convert('RGB').resize((360,640)),((i%5)*360,(i//5)*640))
        S.save('sheet.png')
    else:
        for n,a,b,fn in SC:
            if len(sys.argv)>2 and n not in sys.argv[2:]:continue
            o=f'{n}_{VAR}' if n=='g' else n
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 17 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{o}.mp4'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{o}.mp4',f'{o}.mp4');print(o,flush=True)
