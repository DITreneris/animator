# "I learned to code for THIS?" - Me + My AI episode. 25 s, 750 frames.
import sys,os,subprocess,math,random,cairo
import numpy as np
import v,v8,v9,chars,titles
from v import *
chars.install()
ENDING=os.environ.get('ENDING','A')
POL=os.environ.get('POLISH')=='1'
NOTAG=os.environ.get('NOTAG')=='1'   # no burned-in chip, TODAY clear of the edge, ends on the board meeting
def push(c,f,keys):
    """Camera push-in. keys: (frame, k, fx, fy, tx, ty): world point (fx,fy) shown at (tx,ty), scaled k. Smooth between keys."""
    if f<=keys[0][0]:p=keys[0][1:]
    elif f>=keys[-1][0]:p=keys[-1][1:]
    else:
        for a,b in zip(keys,keys[1:]):
            if a[0]<=f<b[0]:
                t=(f-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);p=[lerp(x,y,t) for x,y in zip(a[1:],b[1:])];break
    k,fx,fy,tx,ty=p
    c.translate(tx,ty);c.scale(k,k);c.translate(-fx,-fy)
def screen(fn):
    def g(c,*a,**kw):
        c.save();c.identity_matrix();r=fn(c,*a,**kw);c.restore();return r
    return g
F=lambda s:int(round(s*30))
# ---------- voice placements (seconds) ----------
VO=[('this',1.35,'g'),('done',5.7,'r'),('answer',7.3,'g'),('hired',9.8,'h'),('andme',11.2,'g'),('charger',12.3,'h'),('fired',18.4,'g')]
VO+=[('worse',19.87,'h'),('promo',20.67,'h')] if ENDING=='A' else [('still',19.87,'h')]
if ENDING=='B2':VO=[x for x in VO if x[0]!='fired' and x[0]!='still']+[('news',18.4,'g'),('still',20.05,'h')]
N=750
def env(who):
    e=np.zeros(N);sr=16000;hop=sr//30
    for n,t,w in VO:
        if w!=who:continue
        x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'vo/v_{n}.wav','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
        r=np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(len(x)//hop)]);r=r/(r.max()+1e-9)
        for i,val in enumerate(r):
            if F(t)+i<N:e[F(t)+i]=max(e[F(t)+i],val)
    return e
EG,EH,ER=env('g'),env('h'),env('r')
chars.talk=lambda f:EG[f] if f<N and EG[f]>.12 else 0
# ---------- expression tables ----------
chars.GUY=[(0,9,'calm',0),(9,22,'shock',0),(22,40,'deadpan',0),(40,90,'offended',0),
 (105,172,'deadpan',0),(172,184,'shock',16),(184,210,'sideeye',16),
 (210,252,'happy',0),(252,294,'proud',0),(294,316,'happy',0),(316,336,'shock',0),(336,362,'sheepish',0),(362,386,'calm',0),(386,420,'deadpan',0),
 (420,462,'proud',0),(462,486,'shock',0),(486,540,'sheepish',0),
 (540,552,'calm',0),(552,590,'sheepish',0),(590,610,'shock',0),(610,680,'deadpan',0),(680,728,'deadpan',0),(728,750,'calm',0)]
HART=[(0,294,'calm'),(294,330,'happy'),(330,369,'calm'),(369,420,'happy'),(540,556,'calm'),(556,596,'sheepish'),(596,750,'deadpan')]
if ENDING=='B2':   # B2: hopeful question, polite HR smile while stalling
    chars.GUY=[r for r in chars.GUY if not(540<=r[0]<728)]+[(540,552,'calm',0),(552,600,'happy',0),(600,632,'calm',0),(632,728,'deadpan',0)]
    chars.GUY.sort()
    HART=HART[:5]+[(556,750,'calm')]
def bot_emote(f):
    for a,b,e in((168,210,'happy'),(252,294,'love'),(294,330,'happy'),(420,462,None),(462,540,'love'),(676,750,'happy')):
        if a<=f<b:return e
    return None
CUR=lambda:chars.CURF
# ---------- shared drawing ----------
def topbar(c,f,years,today):
    if 90<=f<105:return
    cur=[y for y in years if y[0]<=f][-1];d=f-cur[0]
    B0,BH=titles.BAR_Y,titles.BAR_H
    c.rectangle(0,B0,W,BH);c.set_source_rgba(.04,.05,.09,.92);c.fill()
    c.rectangle(0,B0+BH-6,W,6);c.set_source_rgb(*YEL);c.fill()
    cy=B0+BH/2-2
    txt(c,'ME + MY AI',560,cy,86,WHITE,lw=0,align='r')
    k=abs(math.cos(min(1,d/6)*math.pi)) if d<6 and cur[0]>0 else 1
    c.save();c.translate(760,cy);c.scale(1,max(.06,k))
    rr(c,-150,-52,300,104,26);c.set_source_rgb(*YEL);c.fill();txt(c,cur[1],0,0,90,INK,lw=0);c.restore()
    if today:txt(c,'TODAY',985,cy,40,RED,lw=0) if NOTAG else txt(c,'TODAY',1012,cy,44,RED,lw=0)
YEARS=[(0,'2026'),(105,'2024'),(210,'2025'),(420,'2026'),(540,'2026')]
@screen
def sub(c,f,a,b,t,y,size=84):
    if not a<=f<b:return
    k=max(.02,back((f-a)/4))
    c.save();c.translate(540,y);c.scale(k,k)
    c.select_font_face('Lilita One');c.set_font_size(size);w=c.text_extents(t).width
    rr(c,-w/2-40,-size*.72,w+80,size*1.44,size*.4);c.set_source_rgba(.04,.05,.09,.78);c.fill()
    txt(c,t,0,0,size,WHITE,lw=size*.12);c.restore()
def window(c,x,y,w,h,k,title,dark=False):
    """App window popup (what's on a laptop screen)."""
    c.save();c.translate(x,y);c.scale(k,k)
    rr(c,-w/2,-h/2,w,h,26);fs(c,hx('1b2030') if dark else WHITE,8)
    c.save();rr(c,-w/2,-h/2,w,h,26);c.clip();c.rectangle(-w/2,-h/2,w,56);c.set_source_rgb(*hx('dfe4ee') if not dark else hx('2c3348'));c.fill();c.restore()
    for i,col in enumerate(('ff5f57','febc2e','28c840')):ell(c,-w/2+36+i*32,-h/2+28,10,10);c.set_source_rgb(*hx(col));c.fill()
    txt(c,title,0,-h/2+28,30,hx('66707f') if not dark else hx('9aa6c2'),lw=0)
    c.restore()
def stamp(c,x,y,lines,k,rot=-.12,col=RED,size=110):
    if k<=.02:return
    c.save();c.translate(x,y);c.rotate(rot);c.scale(k,k)
    c.select_font_face('Lilita One');c.set_font_size(size);w=max(c.text_extents(l).width for l in lines)+80;h=len(lines)*size*1.05+50
    rr(c,-w/2,-h/2,w,h,22);c.set_source_rgba(1,1,1,.88);c.fill_preserve();c.set_source_rgb(*col);c.set_line_width(16);c.stroke()
    for i,l in enumerate(lines):txt(c,l,0,-(len(lines)-1)*size*.525+i*size*1.05,size,col,lw=0)
    c.restore()
def slam(r):   # stamp scale: big -> 1
    return 0 if r<0 else lerp(2.6,1,cl(r/5))
# ---------- characters ----------
GSKIN=hx('f3c4a2');HHAIR=hx('7a2e1c');GLASS=hx('e0245e');TEAL=hx('1f8a8a')
def hart_head(c,x,y,s,f,blink_seed=3):
    row=[r for r in HART if r[0]<=f<r[1]];expr=row[0][2] if row else 'calm'
    op=EH[f] if f<N and EH[f]>.12 else 0
    c.save();c.translate(x,y);c.scale(s,s)
    # bob haircut behind
    rr(c,-128,-120,256,250,110);fs(c,HHAIR,10)
    rr(c,-100,-72,200,178,84);fs(c,GSKIN)
    # fringe
    c.save();rr(c,-100,-72,200,178,84);c.clip()
    c.move_to(-110,-80);c.curve_to(-60,-150,90,-150,120,-60);c.line_to(120,-30);c.curve_to(60,-40,-20,-10,-110,-20);c.close_path();c.set_source_rgb(*HHAIR);c.fill();c.restore()
    c.move_to(-100,-20);c.curve_to(-20,-10,60,-40,104,-30);c.set_source_rgb(*INK);c.set_line_width(7);c.stroke()
    sv=chars.SKIN;chars.SKIN=GSKIN
    gz=18 if ENDING=='B2' and 652<=f<676 else 0   # B2: glances toward the bridge before the tilt
    chars.face(c,expr,gz,chars.blinking(f,blink_seed) and not gz,op)
    chars.SKIN=sv
    for q in(-1,1):ell(c,q*42,8,40,36);c.set_source_rgb(*GLASS);c.set_line_width(9);c.stroke()
    c.move_to(-4,4);c.line_to(4,4);c.stroke()
    c.restore()
def hart_body(c,x,y,s,coat=False):
    c.save();c.translate(x,y);c.scale(s,s)
    if coat:
        rr(c,-104,-30,208,200,70);fs(c,hx('c9b38f'))
        for i in range(3):c.move_to(-96,30+i*50);c.curve_to(-30,42+i*50,30,42+i*50,96,30+i*50);c.set_source_rgba(*INK,.35);c.set_line_width(5);c.stroke()
        # striped scarf
        rr(c,-86,-46,172,52,26);fs(c,RED,7)
        for i in range(-3,4):c.rectangle(i*24-6,-44,12,48);c.set_source_rgb(*WHITE);c.fill()
        rr(c,30,-10,46,120,18);fs(c,RED,7)
    else:
        rr(c,-92,-30,184,190,60);fs(c,TEAL)
        c.move_to(-34,-28);c.line_to(0,50);c.line_to(34,-28);c.close_path();fs(c,WHITE,6)
        for q in(-1,1):c.move_to(q*40,-26);c.line_to(q*8,60);c.line_to(q*52,70);c.set_source_rgb(*INK);c.set_line_width(6);c.stroke()
    c.restore()
def robot(c,x,y,s,emote=None,walk=None,seed=0):
    chars.robot2(c,x,y,s,emote=emote,walk=walk,seed=seed)
def hrobot(c,x,y,s,emote=None,seed=5):
    """Ms. Hart's robot: grey, with a red bow (matches her glasses)."""
    sv=chars.WHITE;chars.WHITE=hx('b9bfcc');chars.robot2(c,x,y,s,emote=emote,seed=seed);chars.WHITE=sv
    c.save();c.translate(x,y+92*s);c.scale(s,s)
    c.move_to(0,0);c.line_to(-46,-26);c.line_to(-46,26);c.close_path();c.move_to(0,0);c.line_to(46,-26);c.line_to(46,26);c.close_path();fs(c,GLASS,6)
    ell(c,0,0,12,12);fs(c,GLASS,5);c.restore()
def guyhead(c,x,y,s,age=.15,tongue=False):
    v8.guyhead(c,x,y,s,'calm',age)
    if tongue:ell(c,x+22*s,y+80*s,12*s,10*s);fs(c,hx('ff7a8c'),max(3,5*s))
def pigeon(c,x,y,s,flap=0,peck=0,flip=1):
    c.save();c.translate(x,y);c.scale(s*flip,s)
    for q in(-1,1):limb(c,[(q*12,40),(q*14,70)],7,hx('e88a8a'))
    ell(c,0,10,58,40);fs(c,hx('9aa2b1'),7)
    a=math.sin(flap)*1.1 if flap else 0
    c.save();c.translate(10,0);c.rotate(-a);ell(c,22,6,40,20);fs(c,hx('6f7788'),6);c.restore()
    c.move_to(50,14);c.line_to(86,4);c.line_to(84,26);c.close_path();fs(c,hx('6f7788'),6)
    hy=-30+peck*30
    ell(c,-38,hy+18,22,26);c.set_source_rgb(*hx('6fbf8f'));c.fill()
    ell(c,-44,hy,26,24);fs(c,hx('9aa2b1'),7)
    ell(c,-50,hy-4,6,6);c.set_source_rgb(*INK);c.fill();ell(c,-52,hy-6,2,2);c.set_source_rgb(1,1,1);c.fill()
    c.move_to(-68,hy+2);c.line_to(-84,hy+8);c.line_to(-68,hy+12);c.close_path();fs(c,hx('f0a33a'),4)
    c.restore()
def charger(c,x,y,s,rot=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    for q in(-1,1):c.rectangle(q*12-4,-48,8,18);c.set_source_rgb(*GREY);c.fill()
    rr(c,-34,-32,68,60,14);fs(c,WHITE,6)
    c.move_to(4,-18);c.line_to(-8,2);c.line_to(2,2);c.line_to(-4,18);c.line_to(10,-4);c.line_to(0,-4);c.close_path();c.set_source_rgb(*YEL);c.fill()
    c.restore()
def cord(c,a,b,sag=80,lw=8):
    c.move_to(*a);c.curve_to(a[0]+(b[0]-a[0])*.3,a[1]+sag,b[0]-(b[0]-a[0])*.3,b[1]+sag,*b)
    c.set_source_rgb(*INK);c.set_line_width(lw+6);c.stroke_preserve();c.set_source_rgb(*WHITE);c.set_line_width(lw);c.stroke()
# ---------- London: Tower Bridge world. Bottom view shows world y 1600..3520, top view 0..1920 ----------
def bridge_world(c,f,cam,tent_open=0,hart=False,popup=None,pigeon_on=None,laptop_ping=0,board=True):
    c.set_source_rgb(*hx('1e1846'));c.paint()
    wx,wy,k=lerp(540,320,cam),lerp(2560,560,cam),lerp(1,1.55,cam)
    c.save();c.translate(540,960);c.scale(k,k);c.translate(-wx,-wy)
    g=cairo.LinearGradient(0,0,0,3520)
    for st,col in((0,'1e1846'),(.45,'4b2f6e'),(.66,'e0718a'),(.74,'ffb27a'),(1,'ffb27a')):g.add_color_stop_rgb(st,*hx(col))
    c.set_source(g);c.rectangle(0,0,W,3520);c.fill()
    for i in range(30):
        sx=(noise(i,11)*.5+.5)*W;sy=(noise(i,12)*.5+.5)*1200
        ell(c,sx,sy,3,3);c.set_source_rgba(1,1,1,.55);c.fill()
    # skyline
    rnd=random.Random(5)
    x=-20
    while x<W:
        w=rnd.randint(60,130);h=rnd.randint(80,260);c.rectangle(x,2560-h,w,h+10);c.set_source_rgb(*hx('3b2a52'));c.fill()
        for j in range(4):
            if rnd.random()<.6:c.rectangle(x+12+j*24,2560-h+30,10,14);c.set_source_rgba(1,.85,.5,.8);c.fill()
        x+=w+rnd.randint(0,20)
    c.move_to(150,2560);c.line_to(240,2110);c.line_to(330,2560);c.close_path();c.set_source_rgb(*hx('34264a'));c.fill()   # generic glass spire
    # river
    c.rectangle(0,2560,W,620);c.set_source_rgb(*hx('1f4b5e'));c.fill()
    for i in range(18):
        yy=2590+i*32;xx=(noise(i,21)*.5+.5)*W+math.sin(f*.08+i)*30
        rr(c,xx-60,yy,120,7,4);c.set_source_rgba(1,.8,.55,.35);c.fill()
    # suspension chain (blue/white)
    for lw,col in((40,INK),(30,hx('6fa8e8')),(10,WHITE)):
        c.move_to(-60,1960);c.curve_to(200,1880,420,1300,620,1060);c.set_source_rgb(*col);c.set_line_width(lw);c.stroke()
    # road deck
    c.rectangle(-10,2000,640,120);fs(c,hx('2b3348'),8)
    c.rectangle(-10,1984,640,26);fs(c,hx('6fa8e8'),7)
    for i in range(16):c.rectangle(i*40,1940,8,44);c.set_source_rgb(*hx('6fa8e8'));c.fill()
    c.rectangle(-10,1934,640,10);c.set_source_rgb(*hx('6fa8e8'));c.fill()
    # high walkway (blue lattice)
    c.rectangle(-10,700,640,170);fs(c,hx('4f86c6'),8)
    c.save();c.rectangle(0,716,630,138);c.clip()
    for i in range(-1,12):
        c.move_to(i*70,716);c.line_to(i*70+70,854);c.move_to(i*70+70,716);c.line_to(i*70,854)
    c.set_source_rgb(*WHITE);c.set_line_width(9);c.stroke();c.restore()
    c.rectangle(-10,690,640,22);fs(c,hx('6fa8e8'),7)
    # tower
    tx0,tx1=600,1060
    c.rectangle(tx0,420,tx1-tx0,2240);fs(c,hx('d8c6a0'),10)
    for yy in range(500,2600,70):c.move_to(tx0,yy);c.line_to(tx1,yy);c.set_source_rgba(*INK,.12);c.set_line_width(4);c.stroke()
    def arch(cx,y,w,h,col):
        c.move_to(cx-w/2,y+h);c.line_to(cx-w/2,y+w*.5);c.curve_to(cx-w/2,y+w*.1,cx-w*.1,y,cx,y-w*.25);c.curve_to(cx+w*.1,y,cx+w/2,y+w*.1,cx+w/2,y+w*.5);c.line_to(cx+w/2,y+h);c.close_path();fs(c,col,7)
    for yy in(560,1100,1500):
        for cx in(700,830,960):arch(cx,yy,70,160,hx('3a3550'))
    arch(830,2150,250,500,hx('2a2540'))   # the big road arch
    for q in(tx0,tx1):
        c.rectangle(q-40,300,80,2360);fs(c,hx('cbb790'),8)
        c.move_to(q-52,300);c.line_to(q,150);c.line_to(q+52,300);c.close_path();fs(c,hx('4a5a78'),8)
        ell(c,q,140,10,10);c.set_source_rgb(*YEL);c.fill()
    c.move_to(tx0+40,420);c.line_to(830,230);c.line_to(tx1-40,420);c.close_path();fs(c,hx('4a5a78'),8)
    c.rectangle(tx0-10,2600,tx1-tx0+20,80);fs(c,hx('a89a7e'),8)
    # board meeting on top of the walkway
    if board:boardroom(c,f)
    # embankment
    c.rectangle(-10,3180,W+20,400);c.set_source_rgb(*hx('595665'));c.fill()
    c.rectangle(-10,3160,W+20,30);fs(c,hx('8a8696'),7)
    for i in range(12):c.move_to(i*100,3190);c.line_to(i*100-60,3520);c.set_source_rgba(0,0,0,.15);c.set_line_width(4);c.stroke()
    c.save();c.translate(0,1600);camp(c,f,tent_open,hart,None,pigeon_on,laptop_ping);c.restore()
    c.restore()
    if popup:screen(popup)(c)
def tent(c,x,y,w,h,col,open_=0,sign=False,sign_now=True):
    c.move_to(x-w/2,y);c.curve_to(x-w/2,y-h*1.2,x+w/2,y-h*1.2,x+w/2,y);c.close_path();fs(c,col,9)
    c.move_to(x,y-h*.9);c.line_to(x,y);c.set_source_rgba(*INK,.4);c.set_line_width(5);c.stroke()
    for q in(-1,1):c.move_to(x+q*w*.25,y-h*.85);c.curve_to(x+q*w*.35,y-h*.6,x+q*w*.4,y-h*.3,x+q*w*.42,y);c.stroke()
    if open_>0:
        oh=h*.82*open_
        c.move_to(x-w*.26,y);c.curve_to(x-w*.26,y-oh*1.15,x+w*.26,y-oh*1.15,x+w*.26,y);c.close_path();fs(c,hx('1c1a26'),7)
def tent_sign(c,x,y,w,h):
    if True:
        c.save();c.translate(x-w*.3,y-60);c.rotate(-.12);c.scale(.8,.8)
        rr(c,-120,-42,240,84,8);fs(c,hx('f5e6c5'),6)
        txt(c,'HEAD OF',0,-15,32,INK,lw=0);txt(c,'HIRING',0,20,34,INK,lw=0)
        for q in(-1,1):c.save();c.translate(q*112,-38);c.rotate(q*.6);c.rectangle(-22,-9,44,18);c.set_source_rgba(1,.9,.6,.85);c.fill();c.restore()
        c.restore()
def camp(c,f,tent_open,hart,popup,pigeon_on,laptop_ping):
    # fairy lights over his tent
    tent(c,250,1600,440,330,hx('f08a24'))
    for i in range(11):
        t=i/10;px=lerp(40,470,t);py=1390-math.sin(t*math.pi)*170+30
        on=(i+f//8)%3!=0
        ell(c,px,py,9,9);c.set_source_rgba(*((1,.85,.3) if i%2 else (1,.4,.6)),1 if on else .35);c.fill()
    # her tent
    hx_=790
    tent(c,hx_,1610,380,300,hx('3aa17e'),tent_open,sign=False)
    if hart and tent_open>.5:
        e=oe((tent_open-.5)*2)
        c.save();c.rectangle(hx_-110,1200,220,410);c.clip()
        hart_body(c,hx_,1450+(1-e)*180,1.0,coat=True)
        hart_head(c,hx_,1320+(1-e)*180,.95,chars.CURF)
        c.restore()
    tent_sign(c,hx_,1610,380,300)
    # crates, mug
    rr(c,470,1520,90,70,8);fs(c,hx('a0663a'),6)
    # the guy, sitting cross-legged in front of his tent
    gx=300
    ell(c,gx,1560,170,48);fs(c,hx('34508a'),8)
    for q in(-1,1):ell(c,gx+q*120,1572,40,24);fs(c,hx('2a2a33'),6)
    chars.torso2(c,gx,1330,1.05)
    guyhead(c,gx,1170,1.02,.2)
    # laptop on his lap (back of lid)
    ping=laptop_ping
    c.save();c.translate(gx,1480);c.rotate(-.04)
    rr(c,-120,-110,240,150,14);fs(c,hx('9aa3b5'),7)
    txt(c,'</>',0,-36,48,hx('5b6478'),lw=0)
    if ping:ell(c,0,-110,140*ping,30*ping);c.set_source_rgba(1,.2,.25,.25*(1-ping));c.fill()
    c.restore()
    for q in(-1,1):ell(c,gx+q*126,1450,24,24);fs(c,SKIN,6)
    if pigeon_on:pigeon(c,*pigeon_on)
    if popup:popup(c)
def boardroom(c,f):
    # top of the walkway, world y 690. Two robots, banner, CEO mugs, a pigeon nest on our robot.
    for px in(70,560):c.rectangle(px-6,330,12,360);fs(c,hx('6b4022'),5)
    c.save();c.translate(315,380);c.rotate(math.sin(f*.1)*.01)
    rr(c,-240,-50,480,100,10);fs(c,hx('ffd84a'),7);txt(c,'BOARD MEETING',0,0,58,INK,lw=0);c.restore()
    robot(c,170,520,.62,emote=bot_emote(f),seed=2)
    hrobot(c,460,520,.62,emote='happy' if f>=676 else 'love')
    # nest + pigeon on our robot's head
    ell(c,170,452,74,24);fs(c,hx('8a5a2e'),6)
    for i in range(7):c.move_to(110+i*20,440+(i%2)*8);c.line_to(130+i*20,462-(i%2)*8);c.set_source_rgb(*hx('5a3a1e'));c.set_line_width(4);c.stroke()
    pigeon(c,175,412,.55,flap=0,flip=1)
    # table
    rr(c,40,620,550,30,8);fs(c,hx('6b4022'),7)
    for lx in(80,550):c.rectangle(lx-8,650,16,42);c.set_source_rgb(*INK);c.fill()
    for mx,lab in((250,'CEO'),(380,'CEO')):
        rr(c,mx-34,560,68,62,10);fs(c,WHITE,6);txt(c,lab,mx,592,26,INK,lw=0)
        c.arc(mx+40,590,16,-1.3,1.3);c.set_source_rgb(*INK);c.set_line_width(7);c.stroke()
    if (f//10)%2==0:
        if ENDING!='B2':
            for i,(x0,dx) in enumerate(((250,30),(360,-30))):txt(c,'beep',x0+dx,320+i*0,36,BLUE,lw=6)
    if ENDING=='B2':   # the robots visibly still talking: same 01 / <3 / 10 bubbles as the 2025 interview
        idx,t=f//12,(f%12)/12
        x=lerp(250,380,t) if idx%2==0 else lerp(380,250,t)
        v9.holo(c,x,525-math.sin(t*math.pi)*50,['01','<3','10'][idx%3],.6)
def rain(c,f,a=.35):
    rnd=random.Random(1)
    for i in range(70):
        x=rnd.uniform(0,W+300);y0=rnd.uniform(0,H);sp=rnd.uniform(28,40)
        y=(y0+f*sp)%H;xx=x-(f*sp*.25)%300
        c.move_to(xx,y);c.line_to(xx-7,y+34);c.set_source_rgba(.85,.9,1,a);c.set_line_width(3);c.stroke()
# ---------- scenes ----------
def app_popup(f,num=847,a=0,submit=6,reject=9):
    def p(c):
        k=max(.02,back((f-a)/5)) if f>=a else 0
        if k<=0:return
        window(c,540,700,760,330,k,'apply.jobs')
        c.save();c.translate(540,700);c.scale(k,k)
        txt(c,f'APPLICATION #{num}',0,-50,64,INK,lw=0)
        pr=submit<=f<submit+3
        rr(c,-140,30+pr*4,280,80,40);fs(c,GREEN,7);txt(c,'SUBMIT',0,70+pr*4,46,WHITE,lw=0)
        if f<submit+2:   # cursor
            mx,my=lerp(260,60,cl(f/submit)),lerp(140,80,cl(f/submit))
            c.move_to(mx,my);c.line_to(mx,my+50);c.line_to(mx+14,my+38);c.line_to(mx+34,my+38);c.close_path();fs(c,WHITE,5)
        c.restore()
        if f>=reject:
            if f<reject+3:c.rectangle(0,0,W,H);c.set_source_rgba(1,.1,.2,.18);c.fill()
            stamp(c,540,700,['REJECTED'],slam(f-reject)*k,-.1,size=120)
    return p
def hookview(c,f,r):
    pig=None
    if r>=18:
        k=oe((r-18)/12);px=lerp(1150,330,k);py=lerp(500,1345,k)-math.sin(k*math.pi)*120
        pig=(px,py,.6,r*.9 if k<1 else 0,(math.sin(r*.4)>.6)*.4 if k>=1 else 0,1)
    bridge_world(c,f,0,popup=app_popup(r,a=-8),pigeon_on=pig)
    rain(c,f)
def A(c,f):
    if POL:c.save();push(c,f,[(40,1,540,960,540,960),(50,1.4,300,1180,420,1250)])
    hookview(c,f,f)
    if POL:c.restore()
    sub(c,f,40,90,'I LEARNED TO CODE FOR THIS?',950,72)
    loc(c)
@screen
def loc(c):
    c.save();c.translate(70,410);rr(c,0,-34,250,68,34);c.set_source_rgba(.04,.05,.09,.78);c.fill()
    ell(c,38,-4,14,14);c.set_source_rgb(*RED);c.fill();c.move_to(26,2);c.line_to(38,26);c.line_to(50,2);c.close_path();c.fill()
    txt(c,'LONDON',150,0,44,WHITE,lw=0);c.restore()
def Brew(c,f):
    r=f-90;bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    t=['2026','2025','2024','2024'][min(3,r//4)]
    for dx,cc in((-12,(0,1,1)),(12,(1,0,.55))):txt(c,t,540+dx,900,260,cc,lw=0,alpha=.9)
    txt(c,t,540,900,260,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,560);c.line_to(x,620);c.line_to(x+90,680);c.close_path();c.set_source_rgb(*YEL);c.fill()
    for yy in range(0,H,6):c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
HELLO='print("Hello Wor'
def C(c,f):
    r=f-105;v9.room(c)
    # book
    c.save();c.translate(150,1110);c.rotate(-.05);rr(c,-105,-140,210,280,10);fs(c,hx('ff6a2b'),8)
    for i,l in enumerate(('LEARN','TO CODE','IN 30','DAYS')):txt(c,l,0,-80+i*54,44 if i<3 else 40,WHITE,lw=7)
    c.restore()
    # guy
    j=noise(f//3,7)*3
    chars.torso2(c,380,1150,1.3)
    guyhead(c,380,930+j,1.25,0,tongue=r<67)
    # robot on the desk, typing a blur
    rb=abs(math.sin(r*.9))*6 if r<63 else abs(math.sin(r*.5))*14
    robot(c,800,1100-rb,.6,emote=bot_emote(f),seed=4)
    if r<63:
        for i in range(4):c.move_to(700+i*60,1230);c.line_to(730+i*60,1200);c.set_source_rgba(*INK,.5);c.set_line_width(5);c.stroke()
    v9.desk(c,1250)
    rr(c,250,1110,260,150,12);fs(c,hx('9aa3b5'),7);txt(c,'</>',380,1180,46,hx('5b6478'),lw=0)
    rr(c,700,1180,200,90,10);fs(c,hx('9aa3b5'),6)
    for q in(-1,1):ell(c,380+q*150,1255+(abs(math.sin(r*.5+q))*8 if r<67 else 0),28,22);fs(c,SKIN,6)
    # his screen
    window(c,320,560,560,200,1,'my_first_code.py',dark=True)
    n=min(len(HELLO),int(r/4.2))
    txt(c,HELLO[:n]+('|' if (f//8)%2 else ''),80,580,50,hx('8ff7ff'),lw=0,align='l')
    # robot's screen: code blur -> app done
    window(c,760,820,480,250,1,'robot_app',dark=r<63)
    if r<63:
        for i in range(6):
            w=(noise(i+f,9)*.5+.5)*300+60;c.rectangle(560,760+i*28,w,12);c.set_source_rgba(*((.56,.97,1) if i%2 else (.5,1,.45)),.8);c.fill()
    else:
        k=max(.02,back((r-63)/5))
        c.save();c.translate(760,850);c.scale(k,k);txt(c,'APP DONE!',0,-10,70,GREEN,lw=10);txt(c,'100%',0,60,40,INK,lw=0);c.restore()
        for b,(bx,by,col) in enumerate(((600,700,YEL),(930,690,hx('ff5c8a')),(1000,900,BLUE))):
            d=r-63-b*4
            if 0<=d<26:
                for i in range(10):
                    a=i/10*2*math.pi;rad=d*5
                    ell(c,bx+math.cos(a)*rad,by+math.sin(a)*rad,7,7);c.set_source_rgba(*col,1-d/26);c.fill()
    sub(c,f,F(5.7),210,'DONE!',1430,96)
def office_bg(c,scroll=0):
    bg(c,hx('e5edf8'),hx('aebfd8'))
    for i in range(-1,5):
        x=90+i*330-scroll%330;rr(c,x,380,240,300,12);fs(c,hx('cde6ff'),6)
    c.rectangle(0,1500,W,420);c.set_source_rgb(*hx('8fa1bd'));c.fill()
    c.rectangle(0,1496,W,10);c.set_source_rgb(*INK);c.fill()
def D(c,f):
    r=f-210
    if POL:push(c,f,[(334,1,540,960,540,960),(342,1.6,190,1214,360,1150),(360,1.6,190,1214,360,1150),(370,1.2,380,1250,540,1200)])
    office_bg(c)
    # Ms. Hart behind the desk, her robot on the desk
    hart_body(c,660,1170,1.0)
    hart_head(c,660,1010,.95,f)
    hrobot(c,900,1218,.55,emote='love' if 252<=f<294 else ('happy' if 294<=f<420 else None))
    # her arm: handshake (f 290-330), then hands the charger (f 362-386)
    hand=None
    if 286<=f<334:k=oe((f-286)/8);hand=(lerp(720,545,k),lerp(1250,1400,k)+math.sin(f*.9)*8*(f>=294))
    elif 360<=f<392:k=oe((f-360)/10)*(1-oe((f-384)/8));hand=(lerp(720,370,k),lerp(1250,1240,k))
    v9.desk(c,1330)
    # nameplate
    rr(c,520,1380,380,90,12);fs(c,hx('f5e6c5'),7);txt(c,'HEAD OF HIRING',710,1425,44,INK,lw=0)
    # the guy + his robot
    gy=1700
    hy=v9.guyfull(c,190,gy,.9,'calm',.1,arms=None)
    hold=f>=376
    for q in(-1,1):
        if q==1 and (236<=f<262):limb(c,[(190+80,hy+170),(330,hy+150),(380,hy+150)],38,NAVY);ell(c,392,hy+150,22,22);fs(c,SKIN,6)   # points at robot
        elif q==1 and (336<=f<356):limb(c,[(190+80,hy+170),(250,hy+250),(215,hy+200)],38,NAVY);ell(c,205,hy+190,22,22);fs(c,SKIN,6)   # points at himself
        elif q==1 and hold:limb(c,[(190+80,hy+170),(300,hy+260),(330,hy+260)],38,NAVY);ell(c,340,hy+262,22,22);fs(c,SKIN,6)
        else:limb(c,[(190+q*80,hy+170),(190+q*100,hy+300)],38,NAVY);ell(c,190+q*102,hy+316,22,22);fs(c,SKIN,6)
    ry=v9.bot(c,440,gy,.78,walk=0,bob=abs(math.sin(r*.6))*8 if 252<=f<294 else 0)
    if 286<=f<334:
        limb(c,[(720,1250),(640,1330),hand],32,TEAL);ell(c,hand[0],hand[1],24,22);fs(c,GSKIN,6)
        v9.rarm(c,[(440+50,ry+100),(520,ry+40),(hand[0]-8,hand[1]+14)],24)
    # charger: in her hand, then in his, cord to the robot
    if 360<=f<392 and hand and f<376:charger(c,hand[0],hand[1]-10,1.5 if POL else .9,-.3)
    if hand and 360<=f<392:limb(c,[(720,1250),hand],32,TEAL);ell(c,hand[0],hand[1],22,22);fs(c,GSKIN,6)
    if hold:
        cord(c,(340,hy+290),(440-60,ry+60),90);charger(c,340,hy+262,1.35 if POL else .9,0)
    # robots beeping at each other
    if 252<=f<294 and POL:   # one big bubble at a time, like the board meeting
        idx,t=(f-252)//12,((f-252)%12)/12
        a_,b_=((470,1380),(905,1120)) if idx%2==0 else ((905,1120),(470,1380))
        v9.holo(c,lerp(a_[0],b_[0],t),lerp(a_[1],b_[1],t)-math.sin(t*math.pi)*110,['01','<3','10'][idx%3],1.0)
    elif 252<=f<294:
        for i in range(3):
            d=(r-42-i*6)%18
            v9.holo(c,lerp(470,860,d/18),lerp(1300,1120,d/18)-math.sin(d/18*math.pi)*120,['01','<3','10'][i],.55)
    if 294<=f<330:stamp(c,420,800,['HIRED'],slam(f-298)*.9,-.08,GREEN,110)
    sub(c,f,F(7.3),F(8.6),'MY AI WILL ANSWER.',580)
    sub(c,f,F(9.8),F(11.0),"YOU'RE HIRED!",580)
    sub(c,f,F(11.2),F(12.2),'AND ME?',580)
    sub(c,f,F(12.3),420,"YOU'RE THE CHARGER GUY.",580,78)
def E(c,f):
    r=f-420;office_bg(c,scroll=min(r,42)*6)
    # pad + sign
    px=780
    c.save();c.translate(px,1500);ell(c,0,0,170,34);fs(c,hx('22252e'),7)
    on=f>=462
    if on:
        for i in range(3):
            d=((r-42)*2+i*20)%60;ell(c,0,0,170+d*3,34+d*.6);c.set_source_rgba(.2,.75,1,.6*(1-d/60));c.set_line_width(8);c.stroke()
    c.restore()
    c.rectangle(px+150,1090,14,410);c.set_source_rgb(*INK);c.fill()
    c.save();c.translate(px+157,1010);rr(c,-110,-110,220,200,26);fs(c,hx('22252e'),8)
    c.move_to(18,-84);c.line_to(-46,6);c.line_to(-4,6);c.line_to(-22,74);c.line_to(46,-18);c.line_to(4,-18);c.close_path();fs(c,YEL,6)
    c.restore()
    txt(c,'WIRELESS',px+157,1150,40,INK,lw=10,st=WHITE)
    # robot walks onto the pad
    k=oe(r/42);rx=lerp(460,px,k)
    ry=v9.bot(c,rx,1500 if r<42 else 1500-abs(math.sin(r*.3))*0,.8,walk=r*.5 if r<42 else None)
    # the guy trails behind with the cable
    gx=lerp(120,330,k)
    hy=v9.guyfull(c,gx,1610,.85,'calm',.2,arms=None,run=r*.5 if r<42 else None)
    limb(c,[(gx-75,hy+160),(gx-95,hy+280)],36,NAVY);ell(c,gx-97,hy+296,21,21);fs(c,SKIN,6)
    hand=(gx+150,hy+240)
    limb(c,[(gx+75,hy+160),(gx+130,hy+250),hand],36,NAVY)
    plug=(rx-60,ry+90)
    if f<466:cord(c,hand,plug,60)
    elif POL and f>=500:
        w=oe((f-500)/34);end=(lerp(hand[0]+120,hand[0]+30,w),lerp(1600,hand[1]+50,w))
        cord(c,hand,end,lerp(160,30,w))
        rr(c,end[0]-14,end[1]-10,28,20,5);fs(c,WHITE,5)
        for i in range(int(1+w*3)):ell(c,hand[0]+4,hand[1]+28,30+i*6,16+i*3);c.set_source_rgb(*INK);c.set_line_width(12);c.stroke_preserve();c.set_source_rgb(*WHITE);c.set_line_width(6);c.stroke()
        for i in range(2):
            d=(f-500+i*17)%34;hx0,hy0=rx+60-i*120+math.sin(d*.3)*12,ry-150-d*5
            c.save();c.translate(hx0,hy0);c.scale(1.6,1.6);c.move_to(0,16);c.curve_to(-26,-4,-14,-24,0,-10);c.curve_to(14,-24,26,-4,0,16);c.close_path()
            c.set_source_rgba(1,.36,.54,1-d/34);c.fill_preserve();c.set_source_rgba(*INK,1-d/34);c.set_line_width(4);c.stroke();c.restore()
    else:
        d=f-466;fall=oe(d/10);end=(lerp(plug[0],hand[0]+120,fall),lerp(plug[1],1600,fall))
        cord(c,hand,end,lerp(60,160,fall))
        rr(c,end[0]-14,end[1]-10,28,20,5);fs(c,WHITE,5)
    charger(c,*hand,.85,.2)
    ell(c,hand[0],hand[1],21,21);fs(c,SKIN,6)
    if on and r<70:txt(c,'bloop',rx+150,ry-190,52,BLUE,lw=9,scale=back((r-42)/5))
    if f>=486:shake(c,f,486,26,10)
    stamp(c,540,760,['POSITION','ELIMINATED'],slam(f-486),-.1,RED,104)
def Fz(c,f):
    r=f-540
    # camera: hold at the camp, tilt up at f676-694, hold, tilt down 728-750
    if f<676:cam=0
    elif f<694:cam=oe((f-676)/18)
    elif f<728 or NOTAG:cam=1
    else:cam=1-oe((f-728)/22)
    hart_out=f<676
    op=0 if not hart_out else cl((f-541)/(21 if POL else 12))
    popup=app_popup(f-750,num=847,a=-10,submit=99,reject=999) if f>=740 and not NOTAG else None
    if POL:c.save();push(c,f,[(548,1,540,960,540,960),(566,1.3,545,1380,540,1380),(664,1.3,545,1380,540,1380),(676,1,540,960,540,960)])
    bridge_world(c,f,cam,tent_open=op,hart=hart_out,popup=popup)
    if POL:c.restore()
    rain(c,f,.35*(1-cam*.6))
    if ENDING=='B2':
        y1,y2=(700,815) if POL else (860,975)
        sub(c,f,F(18.4),F(19.95),'ANY NEWS ON',y1,80);sub(c,f,F(18.4),F(19.95),'MY APPLICATION?',y2,80)
        sub(c,f,F(20.05),676,'MY AI IS STILL TALKING',y1,80);sub(c,f,F(20.05),676,'WITH YOUR AI.',y2,80)
    else:sub(c,f,F(18.4),F(19.75),'THEY FIRED YOU TOO?',950,76)
    if ENDING=='B2':pass
    elif ENDING=='A':
        sub(c,f,F(19.87),F(20.6),'WORSE.',950,90)
        sub(c,f,F(20.67),676,'OUR AIs PROMOTED',860,80);sub(c,f,F(20.67),676,'EACH OTHER.',975,80)
    else:
        sub(c,f,F(19.87),676,'MY AI IS STILL TALKING',950,72);sub(c,f,F(19.87),676,'WITH YOUR AI.',1060,72)
    if cam>.9 and f<728 and not NOTAG:titles.badge(c)
    if f>=744 and not NOTAG:loc(c)
    if NOTAG and ENDING=='B2':   # the punch line stays on the final image
        sub(c,f,694,750,'MY AI IS STILL TALKING',1380,80);sub(c,f,694,750,'WITH YOUR AI.',1495,80)
SC=[('a',0,90,A),('b',90,105,Brew),('c',105,210,C),('d',210,420,D),('e',420,540,E),('f',540,750,Fz)]
def draw(f):
    chars.CURF=f
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
    for n,a,b,fn in SC:
        if a<=f<b:
            c.save();fn(c,f);c.restore();break
    topbar(c,f,YEARS,f<90 or f>=540)
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
        only=sys.argv[2:]
        for n,a,b,fn in SC:
            if only and n not in only:continue
            out=f'{ENDING}_{n}.mp4' if n=='f' else f'{n}.mp4'
            if POL:out='p'+out
            if NOTAG:out='n'+out
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 14 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{out}'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{out}',out);print(out,flush=True)
