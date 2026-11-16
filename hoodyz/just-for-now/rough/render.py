import sys,os,subprocess,math,random,cairo
import v,v6
from v import *
from v6 import tester,glass,piece,bublines,TAPE
G1=(.72,.72,.76);G0=(.25,.13,.09)
PTOP=1280;GROUND=1500
v6.TOP=PTOP
v6.PIECES[2]=(25,-455,560,230,hx('37507a'),'HEADQUARTERS');v6.PIECES[3]=(0,-630,560,120,hx('f3e3bf'),'THE WHOLE COMPANY')
def guyhead(c,x,y,s,expr='calm',age=0,gaze=0,soot=False):
    v.HAIR=tuple(lerp(a,b,cl(age)) for a,b in zip(G0,G1));v.BEARD=age>.35;v.GAZE=gaze
    head(c,x,y,s,expr)
    v.HAIR=G0;v.BEARD=False;v.GAZE=0
def guy(c,x,y,s,expr='calm',age=0,arms=0,gaze=0,point=False,trophy=False):
    torso(c,x,y+150*s,1.2*s)
    if point:
        limb(c,[(x+90*s,y+180*s),(x+190*s,y+150*s),(x+250*s,y+190*s)],44*s,NAVY);ell(c,x+262*s,y+198*s,26*s,26*s);fs(c,SKIN,7)
    if arms:
        for q in(-1,1):
            limb(c,[(x+q*88*s,y+175*s),(x+q*170*s,y+110*s),(x+q*170*s,y+30*s)],44*s,NAVY);ell(c,x+q*170*s,y+10*s,28*s,28*s);fs(c,SKIN,7)
    guyhead(c,x,y,s*1.08,expr,age,gaze)
def smiley(c,x,y,r):
    ell(c,x,y,r,r);c.set_source_rgb(*INK);c.set_line_width(max(3,r*.12));c.stroke()
    for q in(-1,1):ell(c,x+q*r*.35,y-r*.25,r*.11,r*.14);c.set_source_rgb(*INK);c.fill()
    c.arc(x,y+r*.05,r*.5,.3,math.pi-.3);c.set_source_rgb(*INK);c.stroke()
def pillar(c,cx,cy,s,gap=0,peel=0,tape=1,face=1,lean=0,upper=True):
    # one cracked pillar in two halves, held only by the tape
    c.save();c.translate(cx,cy);c.scale(s,s)
    col=hx('9aa3b2')
    c.move_to(-95,110);c.line_to(95,110);c.line_to(95,12+gap/2);c.line_to(35,28+gap/2);c.line_to(-20,6+gap/2);c.line_to(-95,22+gap/2);c.close_path();fs(c,col,8)
    if upper:
        c.save();c.rotate(lean)
        c.move_to(-95,-110);c.line_to(95,-110);c.line_to(95,-6-gap/2);c.line_to(35,10-gap/2);c.line_to(-20,-12-gap/2);c.line_to(-95,4-gap/2);c.close_path();fs(c,col,8)
        c.restore()
    if tape and peel<1:
        h=66+gap;x0=lerp(-118,118,peel)
        rr(c,x0,-h/2+4,118-x0,h,5);fs(c,TAPE,6)
        for i in range(6):
            xx=lerp(x0,118,(i+.5)/6);c.move_to(xx,-h/2+12);c.line_to(xx-5,h/2-4);c.set_source_rgba(.78,.58,.1,.7);c.set_line_width(3);c.stroke()
        if peel==0 and face:smiley(c,0,4,26*face)
        if peel>0:
            c.move_to(x0,-h/2+4);c.line_to(x0-34,-h/2-60);c.line_to(x0+2,-h/2-72);c.line_to(x0+30,-h/2+4);c.close_path();fs(c,TAPE,5)
    c.restore()
def stack(c,n,th=0,top=None,cx=540):
    top=PTOP if top is None else top
    if n==0:
        piece(c,cx,top-52,380,100,hx('f3e3bf'),'THE WHOLE COMPANY',th,32);return
    P=v6.PIECES[:min(n,3)]
    for (px,py,w,h,col,l) in P:
        x=cx+px*math.cos(th)-py*math.sin(th);y=top+px*math.sin(th)+py*math.cos(th)
        piece(c,x,y,w,h,col,l,th,42)
    py=P[-1][1]-P[-1][3]/2-60
    x=cx-py*math.sin(th);y=top+py*math.cos(th)
    sw,ss=[(0,0),(370,32),(450,40),(560,50)][n];piece(c,x,y,sw,int(sw*.21),hx('f3e3bf'),'THE WHOLE COMPANY',th,ss)
def world(c,rubble=False):
    bg(c,hx('f9cf7a'),hx('e8743b'));rays(c,WHITE,0,540,1000,.07)
    r=random.Random(4)
    for i in range(6):
        x=i*210-30;h=r.randint(60,190);c.rectangle(x,GROUND-h,170,h+10);c.set_source_rgba(.55,.25,.18,.25);c.fill()
    if rubble:
        for (x,y,w,h,rt,col) in ((930,1430,190,90,.3,'5b6d8c'),(790,1465,180,70,-.3,'c2553d'),(1000,1470,170,70,.1,'37507a')):
            c.save();c.translate(x,y);c.rotate(rt);rr(c,-w/2,-h/2,w,h,8);fs(c,hx(col),6);c.restore()
    c.rectangle(-10,GROUND,W+20,460);c.set_source_rgb(*hx('6a3f2d'));c.fill_preserve();c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
def cap(c,t):txt(c,t,540,225,88,YEL,lw=16)
def thumb(c,x,y,k=1):
    c.save();c.translate(x,y);c.scale(k,k);rr(c,-12,-82,30,70,14);fs(c,WHITE,7);rr(c,-38,-30,76,66,22);fs(c,WHITE,7);c.restore()
def trophy(c,x,y,s):
    c.save();c.translate(x,y);c.scale(s,s)
    gold=hx('f5c518')
    rr(c,-55,70,110,28,6);fs(c,hx('6b4a2b'),6);rr(c,-14,30,28,44,4);fs(c,gold,6)
    c.move_to(-58,-70);c.line_to(58,-70);c.curve_to(58,0,24,32,0,32);c.curve_to(-24,32,-58,0,-58,-70);c.close_path();fs(c,gold,7)
    for q in(-1,1):
        c.arc(q*62,-40,22,0,2*math.pi);c.set_source_rgb(*INK);c.set_line_width(7);c.stroke()
    c.restore()
def scr(c,f,a,k=3,n=8):
    d=f-a
    if 0<=d<n:c.translate(noise(f,1)*(n-d)*k,noise(f,2)*(n-d)*k)
def A(c,f):
    world(c);stack(c,3);pillar(c,540,1390,1,gap=26)
    guy(c,190,1140,.95,'small',age=1,arms=1)
    r=oe(f/10);tx=lerp(860,800,r)
    limb(c,[(tx-40,1360),(lerp(790,680,r),1410)],22,WHITE);ell(c,lerp(780,672,r),1412,18,18);fs(c,WHITE,6)
    tester(c,tx,1300,.5,eye=(-8,6))
    bublines(c,["DON'T","TOUCH THAT!"],96,y=395,h=210);cap(c,'DAY 900')
def B(c,f):
    r=f-75;bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    t=['DAY 900','DAY 500','DAY 60','DAY 1'][min(3,r//4)]
    for dx,cc in((-12,(0,1,1)),(12,(1,0,.55))):txt(c,t,540+dx,900,190,cc,lw=0,alpha=.9)
    txt(c,t,540,900,190,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,560);c.line_to(x,620);c.line_to(x+90,680);c.close_path();c.set_source_rgb(*YEL);c.fill()
    for yy in range(0,H,6):
        c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
def C(c,f):
    r=f-90;world(c,rubble=True);stack(c,0)
    t=cl((r-6)/14);fc=cl((r-34)/8)
    pillar(c,540,1390,1,gap=0,peel=0,tape=(t>0),face=fc)
    guy(c,200,1160,.95,'calm',age=0)
    hx0=lerp(320,500,t) if r<34 else 500
    limb(c,[(290,1330),(hx0,1395)],40,NAVY);ell(c,hx0+6,1395,24,24);fs(c,SKIN,6)
    robot(c,860,1280,.72)
    limb(c,[(915,1370),(975,1320)],20,WHITE);thumb(c,985,1305,.75)
    cap(c,'DAY 1')
    if r>=6:bublines(c,['JUST FOR NOW.'],92,y=760,h=170,tx=430,w=660)
DATES=[(222,'DAY 14','FRIDAY'),(250,'DAY 60','NEXT FRIDAY'),(275,'DAY 200','NEXT FRIDAY')]
def D(c,f):
    r=f-180;world(c)
    n=0 if r<30 else 1 if r<60 else 2 if r<85 else 3
    k=cl(r/120);g=k*26
    if r in(30,60,85):c.translate(0,0)
    wob=math.sin(f*.5)*.006*k
    stack(c,n,wob,top=PTOP-g/2);pillar(c,540,1390,1,gap=g)
    guy(c,190,1150,.95,'calm',age=k*.75)
    ph=(f/12)%1;ell(c,310,1050+ph*60,13,19);fs(c,hx('58c7ff'),4)
    if r<42:bublines(c,["I'LL FIX IT","FRIDAY."],96,y=395,h=210,w=700)
    for a,dd,fr in DATES:
        if a<=f<a+28 or (a==DATES[-1][0] and f>=a):
            s=max(.02,back((f-a)/5))
            c.save();c.translate(540,320);c.rotate(-.03);c.scale(s,s)
            rr(c,-300,-125,600,250,20);fs(c,WHITE,9);rr(c,-300,-125,600,74,20);fs(c,RED,9)
            txt(c,dd,0,-88,48,WHITE,lw=0);txt(c,fr,0,38,92 if len(fr)<8 else 76,INK,lw=0);c.restore()
def E_(c,f):
    r=f-300;world(c);placed=r>=45
    g=26+(8 if r>=55 else 0)
    stack(c,3,top=PTOP-g/2);pillar(c,540,1390,1,gap=g)
    if placed:trophy(c,735,1400,1.0)
    guy(c,190,1150,.95,'happy' if r<55 else 'small',age=.8)
    robot(c,880,1240,.7,boss=True)
    if not placed:
        tx=lerp(760,390,cl(r/14));trophy(c,tx,1270,.85)
    if r<55:
        s=max(.02,back(r/5));c.save();c.translate(540,300);c.scale(s,s)
        rr(c,-400,-105,800,210,22);fs(c,hx('f5c518'),9)
        txt(c,'MOST RELIABLE',0,-40,74,INK,lw=0);txt(c,'SYSTEM',0,44,74,INK,lw=0);c.restore()
    elif r>=55:
        ph=(f/12)%1;ell(c,320,1060+ph*60,13,19);fs(c,hx('58c7ff'),4);txt(c,'CREEEAK',860,1090,58,RED,lw=10,rot=.08)
def F1(c,f):
    world(c);stack(c,3,top=PTOP-17);pillar(c,540,1390,1,gap=34);trophy(c,735,1400,1)
    guy(c,190,1140,.95,'focus',age=1,point=True);tester(c,860,1310,.5)
    bublines(c,['WHO MADE','THIS GARBAGE?!'],92,y=395,h=210);cap(c,'DAY 900')
def closeup(c,peel=0,face=1,gap=34):
    bg(c,hx('f9cf7a'),hx('d9713f'));rays(c,WHITE,0,540,1000,.07)
    pillar(c,500,1230,3.0,gap=gap/3,peel=peel,face=face)
def F2(c,f):
    r=f-425;closeup(c)
    gz=0 if r<45 else min(16,(r-45)*4)
    guy(c,540,370,1.25,'small',age=1,gaze=gz)
    k=oe((r-24)/14);x=lerp(1250,510,k)
    limb(c,[(1300,1400),(x+120,1270)],64,NAVY)
    if r>=24:trophy(c,x,1215,2.05)
    ell(c,x+150,1260,44,44);fs(c,SKIN,7)
    ph=(f/12)%1;ell(c,750,300+ph*90,18,26);fs(c,hx('58c7ff'),6)
    if r>=52:txt(c,'*cough*',815,620,70,INK,lw=0,rot=-.06)
def G1_(c,f):
    r=f-510;pl=cl(r/24);closeup(c,peel=pl,face=0 if pl>0 else 1)
    tester(c,860,690,.85,eye=(-12,14))
    x0=lerp(150,780,pl);limb(c,[(830,860),(x0+70,1100),(x0+30,1210)],30,WHITE);ell(c,x0+20,1215,28,28);fs(c,WHITE,7)
def G2(c,f):
    r=f-540;world(c);trophy(c,735,1400,1)
    th=.045*math.sin(r*.8)*(1-r/15*.8)
    pillar(c,540,1390,1,gap=34,tape=0,lean=th*.8);stack(c,3,th,top=PTOP-17)
    guy(c,190,1140,.95,'small',age=1,arms=1);tester(c,860,1310,.5,tape=1,eye=(-8,6),glassy=False)
def dustclouds(c,r):
    rr_=random.Random(6)
    for i in range(30):
        ang=rr_.uniform(0,6.28);d=r*rr_.uniform(10,30);size=30+r*rr_.uniform(6,14)
        ell(c,540+math.cos(ang)*d,1380+math.sin(ang)*d*.6,size,size*.8);c.set_source_rgba(.9,.84,.72,min(.9,r*.07));c.fill()
def G3(c,f):
    r=f-555;scr(c,f,555,3,10);world(c);guy(c,190,1140,.95,'small',age=1,arms=1);tester(c,860,1310,.5,tape=1,eye=(-8,6),glassy=False)
    pillar(c,540,1390,1,gap=40,tape=0,upper=False);v6.fallen(c,r);dustclouds(c,r)
    if r>14:
        c.rectangle(0,0,W,H);c.set_source_rgba(.9,.84,.72,cl((r-14)/8));c.fill()
def G4(c,f):
    r=f-585;world(c);pillar(c,540,1390,1,gap=40,tape=0,upper=False);v6.fallen(c,99)
    guy(c,160,1120,.95,'small',age=1);tester(c,570,1190,.95,tape=1,glassy=False)
    if r>=6:
        k=max(.02,back((r-6)/4));c.save();c.translate(540,680);c.scale(k,k);c.translate(-540,-680)
        bublines(c,['SHOULD I','PUT IT BACK?'],104,y=680,h=280,w=760);c.restore()
    a=1-cl(r/12)
    if a>0:
        c.rectangle(0,0,W,H);c.set_source_rgba(.9,.84,.72,a);c.fill()
def tall(c,f,th=.022):
    stack(c,3,th,top=PTOP-17);pillar(c,540,1390,1,gap=34)
def H1(c,f):
    # POP: instant restore
    r=f-632;world(c);tall(c,f);trophy(c,735,1400,1)
    guy(c,160,1120,.95,'small',age=1);tester(c,850,1310,.5,glassy=False)
    if r<6:
        c.save();c.translate(540,1000);c.scale(1+r*.5,1+r*.5);c.rotate(.2)
        for i in range(8):
            c.rotate(math.pi/4);c.move_to(0,-340);c.line_to(46,-60);c.line_to(-46,-60);c.close_path()
        c.set_source_rgba(1,1,1,1-r/7);c.fill();c.restore()
        txt(c,'POP!',540,1000,230,YEL,lw=36,scale=max(.02,back(r/3)))
def H2(c,f):
    world(c);tall(c,f);trophy(c,735,1400,1)
    guy(c,160,1120,.95,'small',age=1);tester(c,850,1310,.5)
    bublines(c,['SO...','SHOULD WE FIX IT?'],88,y=395,h=210);v.badge(c)
def H3(c,f):
    r=f-695;bg(c,hx('f9cf7a'),hx('d9713f'));rays(c,WHITE,f,540,1000,.1)
    torso(c,540,1340,2.2);guyhead(c,540,1050,2.4,'calm',age=1)
    txt(c,'FRIDAY.',540,430,210,RED,lw=34,scale=max(.02,back(r/4)),rot=-.02);v.badge(c)
def H4(c,f):
    r=f-720;world(c);tall(c,f);trophy(c,735,1400,1)
    guy(c,190,1140,.95,'calm',age=1)
    x=lerp(860,800,oe(r/10));limb(c,[(x-40,1360),(lerp(790,680,oe(r/10)),1410)],22,WHITE);ell(c,lerp(780,672,oe(r/10)),1412,18,18);fs(c,WHITE,6)
    tester(c,x,1300,.5,eye=(-8,6));v.badge(c)
SC=[('A',0,75,A),('B',75,90,B),('C',90,180,C),('D',180,300,D),('E',300,390,E_),('F',390,425,F1),('Fb',425,510,F2),('Ga',510,540,G1_),('Gb',540,555,G2),('Gc',555,585,G3),('Gd',585,632,G4),('Ha',632,655,H1),('Hb',655,695,H2),('Hc',695,720,H3),('Hd',720,735,H4)]
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
        S=Image.new('RGB',(6*300,((len(fs_)+5)//6)*534))
        for i,f in enumerate(fs_):S.paste(Image.open(f'chk_{f:03d}.png').convert('RGB').resize((300,534)),((i%6)*300,(i//6)*534))
        S.save('sheet.png')
    else:
        for n,a,b,fn in SC:
            if len(sys.argv)>2 and n not in sys.argv[2:]:continue
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 17 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{n}.mp4'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{n}.mp4',f'{n}.mp4');print(n,flush=True)
