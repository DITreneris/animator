import sys,os,subprocess,math,random,cairo
import v,v6,v8
from v import *
from v8 import guyhead
from v6 import tester
JEANS=hx('34508a');SHOE=hx('2a2a33');BROWN=hx('a0663a');DARK=hx('6b4022')
GROUND=1520
# ---------- text ----------
YEARS=[(0,'2025'),(75,'2024'),(210,'2025'),(315,'2026'),(527,'2027')]
def topbar(c,f):
    if 60<=f<75:return
    cur=[y for y in YEARS if y[0]<=f][-1];d=f-cur[0]
    c.rectangle(0,150,W,108);c.set_source_rgba(.04,.05,.09,.88);c.fill()
    txt(c,'ME + MY AI',655,204,62,WHITE,lw=0,align='r')
    k=abs(math.cos(min(1,d/6)*math.pi)) if d<6 and cur[0]>0 else 1
    c.save();c.translate(690,204);c.scale(1,max(.06,k));txt(c,cur[1],0,0,62,YEL,lw=0,align='l');c.restore()
def sub(c,f,a,b,t,size=78):
    if a<=f<b:txt(c,t,540,1715,size,WHITE,lw=size*.2,scale=max(.02,back((f-a)/4)))
def holo(c,x,y,text,k=1):
    if k<=.02:return
    lines=text.split('|');c.save();c.translate(x,y);c.scale(k,k)
    c.select_font_face('Lilita One');c.set_font_size(64)
    w=max(c.text_extents(l).width for l in lines)+70;h=len(lines)*70+34
    c.move_to(-16,h/2-4);c.line_to(0,h/2+34);c.line_to(16,h/2-4);c.close_path();fs(c,hx('0b1020'),6)
    rr(c,-w/2,-h/2,w,h,26);fs(c,hx('0b1020'),7)
    for i,l in enumerate(lines):txt(c,l,0,-(len(lines)-1)*35+i*70,64,BLUE,lw=0)
    c.restore()
# ---------- props ----------
def ball(c,x,y,r=24,rot=0):
    ell(c,x,y,r,r);fs(c,hx('d7f25a'),max(3,r*.22))
    c.save();c.translate(x,y);c.rotate(rot);c.arc(-r*1.1,0,r*.85,-.9,.9);c.set_source_rgb(1,1,1);c.set_line_width(r*.14);c.stroke()
    c.arc(r*1.1,0,r*.85,math.pi-.9,math.pi+.9);c.stroke();c.restore()
def button(c,x,y,s=1,press=0):
    c.save();c.translate(x,y);c.scale(s,s)
    rr(c,-120,-10,240,80,16);fs(c,hx('22252e'))
    c.save();c.translate(0,press*16);ell(c,0,-14,82,38);fs(c,RED,8);ell(c,-22,-24,24,10);c.set_source_rgba(1,1,1,.5);c.fill();c.restore()
    rr(c,-96,22,192,40,8);fs(c,YEL,5);txt(c,'APPROVE',0,42,34,INK,lw=0)
    c.restore()
def phone(c,x,y,s,press=0,rot=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    rr(c,-60,-110,120,220,20);fs(c,hx('22252e'),6);rr(c,-48,-92,96,184,10);c.set_source_rgb(*hx('eef3ff'));c.fill()
    ell(c,0,10,34,22*(1-press*.3));fs(c,RED,4);txt(c,'APPROVE',0,56,18,INK,lw=0);c.restore()
def sandwich(c,x,y,s,bite=0):
    c.save();c.translate(x,y);c.scale(s,s);c.rotate(-.3)
    c.move_to(-60,20);c.line_to(60,20);c.line_to(0,-50);c.close_path();fs(c,hx('f1c27d'),6)
    c.move_to(-50,10);c.line_to(50,10);c.set_source_rgb(*GREEN);c.set_line_width(8);c.stroke()
    if bite:ell(c,0,-40,18,16);c.set_source_rgb(*SKIN);c.fill()
    c.restore()
def paper(c,x,y,s=1,rot=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s);rr(c,-40,-52,80,104,4);fs(c,WHITE,5)
    for i in range(5):c.rectangle(-28,-36+i*16,56,5);c.set_source_rgb(*GREY);c.fill()
    c.restore()
def chair(c,x,y,s,spin=0):
    c.save();c.translate(x,y);c.scale(s,s)
    rr(c,-150,-260,300,300,40);fs(c,hx('3a3f4e'))
    rr(c,-170,30,340,60,20);fs(c,hx('3a3f4e'))
    c.rectangle(-12,90,24,90);c.set_source_rgb(*INK);c.fill()
    for i in range(3):
        a=spin+i*2.1;ell(c,math.cos(a)*120,190,26,22);fs(c,INK,0)
    c.restore()
# ---------- characters ----------
def guyfull(c,x,gy,s,expr='calm',age=0,run=None,arms='down',hand=None):
    hy=gy-540*s
    for q in(-1,1):
        sw=math.sin(run+(q>0)*math.pi)*70*s if run is not None else 0
        limb(c,[(x+q*38*s,hy+330*s),(x+q*38*s+sw*.5,hy+430*s),(x+q*40*s+sw,gy-14*s)],46*s,JEANS)
        ell(c,x+q*40*s+sw+q*10*s,gy-6*s,34*s,18*s);fs(c,SHOE,max(3,6*s))
    torso(c,x,hy+150*s,1.2*s)
    if arms=='down':
        for q in(-1,1):
            sw=-math.sin(run+(q>0)*math.pi)*60*s if run is not None else 0
            limb(c,[(x+q*88*s,hy+175*s),(x+q*112*s+sw,hy+300*s)],42*s,NAVY);ell(c,x+q*114*s+sw,hy+318*s,24*s,24*s);fs(c,SKIN,max(3,6*s))
    guyhead(c,x,hy,s*1.08,expr,age)
    return hy
def dragged(c,x,y,s,f,age=.3):
    c.save();c.translate(x,y);c.rotate(1.47+math.sin(f*.9)*.04);c.scale(s,s)
    for q in(-1,1):
        limb(c,[(q*38,330),(q*44,440),(q*50+math.sin(f*1.2+q)*20,520)],46,JEANS);ell(c,q*52,530,34,18);fs(c,SHOE,6)
    torso(c,0,150,1.2)
    for q in(-1,1):limb(c,[(q*80,175),(q*30,-40),(q*10,-180)],42,NAVY);ell(c,q*10,-196,26,26);fs(c,SKIN,6)
    guyhead(c,0,0,1.08,'small',age)
    c.restore()
    return (x+196*s,y)      # hands (rotated ~90 deg so up = right)
def rarm(c,pts,w,col=WHITE):
    limb(c,pts,w,col);ell(c,pts[-1][0],pts[-1][1],w*.85,w*.85);fs(c,col,max(3,w*.18))
def neighbor(c,x,gy,s,f,sip=0):
    hy=gy-680*s
    for q in(-1,1):
        limb(c,[(x+q*24*s,gy-250*s),(x+q*26*s,gy-14*s)],30*s,hx('30364a'));ell(c,x+q*30*s,gy-8*s,26*s,14*s);fs(c,SHOE,max(3,5*s))
    c.move_to(x-80*s,hy+120*s);c.line_to(x+80*s,hy+120*s);c.line_to(x+118*s,gy-230*s);c.line_to(x-118*s,gy-230*s);c.close_path();fs(c,hx('ffcf2e'),max(3,7*s))
    for i in range(3):ell(c,x,hy+170*s+i*70*s,7*s,7*s);c.set_source_rgb(*INK);c.fill()
    hx_=x+44*s+(1-sip)*40*s;hyy=hy+lerp(260,70,sip)*s
    limb(c,[(x+74*s,hy+140*s),(x+120*s,hy+250*s),(hx_,hyy)],30*s,hx('ffcf2e'))
    rr(c,hx_-18*s,hyy-46*s,36*s,52*s,6*s);fs(c,WHITE,max(3,5*s));c.rectangle(hx_-18*s,hyy-30*s,36*s,14*s);c.set_source_rgb(*hx('8a5a2e'));c.fill()
    limb(c,[(x-74*s,hy+140*s),(x-118*s,hy+260*s),(x-112*s,hy+330*s)],30*s,hx('ffcf2e'));ell(c,x-112*s,hy+340*s,18*s,18*s);fs(c,SKIN,max(3,5*s))
    for b in((-50,-40,40),(0,-62,46),(50,-40,40),(96,-6,30),(120,30,26)):ell(c,x+b[0]*s,hy+b[1]*s,b[2]*s,b[2]*s);c.set_source_rgb(*hx('3b2416'));c.fill()
    ell(c,x,hy,70*s,80*s);fs(c,hx('e8b48c'),max(3,7*s))
    for b in((-48,-50,30),(0,-70,36),(46,-52,30)):ell(c,x+b[0]*s,hy+b[1]*s,b[2]*s,b[2]*s);c.set_source_rgb(*hx('3b2416'));c.fill()
    for q in(-1,1):
        ell(c,x+q*26*s,hy+4*s,8*s,9*s);c.set_source_rgb(*INK);c.fill()
        c.move_to(x+q*40*s,hy-22*s);c.line_to(x+q*12*s,hy-26*s);c.set_line_width(5*s);c.stroke()
    c.move_to(x-16*s,hy+40*s);c.line_to(x+16*s,hy+40*s);c.set_line_width(5*s);c.stroke()
    return (x-112*s,hy+340*s)
def dog(c,x,gy,s,pose='sit',look=0,f=0):
    if pose=='sit':
        tw=math.sin(f*.6)*14*s
        c.move_to(x+60*s,gy-30*s);c.curve_to(x+95*s,gy-40*s,x+100*s+tw,gy-80*s,x+86*s+tw,gy-100*s);c.set_source_rgb(*INK);c.set_line_width(20*s);c.stroke()
        c.move_to(x+60*s,gy-30*s);c.curve_to(x+95*s,gy-40*s,x+100*s+tw,gy-80*s,x+86*s+tw,gy-100*s);c.set_source_rgb(*BROWN);c.set_line_width(12*s);c.stroke()
        ell(c,x+40*s,gy-34*s,44*s,34*s);fs(c,BROWN,max(3,6*s))
        ell(c,x+12*s,gy-70*s,42*s,56*s);fs(c,BROWN,max(3,6*s))
        for q in(0,1):limb(c,[(x-10*s+q*22*s,gy-70*s),(x-14*s+q*22*s,gy-6*s)],16*s,BROWN)
        hx_,hy=x-12*s,gy-138*s-look*14*s
        c.rectangle(x-28*s,gy-104*s,52*s,12*s);c.set_source_rgb(*RED);c.fill()
    else:
        c.move_to(x+70*s,gy-18*s);c.line_to(x+125*s,gy-12*s);c.set_source_rgb(*BROWN);c.set_line_width(12*s);c.stroke()
        ell(c,x+20*s,gy-28*s,72*s,28*s);fs(c,BROWN,max(3,6*s))
        for q in(0,1):ell(c,x-66*s,gy-8*s-q*4*s,24*s,10*s);fs(c,BROWN,max(3,5*s))
        hx_,hy=x-42*s,gy-50*s
    ell(c,hx_,hy,38*s,32*s);fs(c,BROWN,max(3,6*s))
    ell(c,hx_-34*s,hy+10*s,22*s,15*s);fs(c,BROWN,max(3,5*s));ell(c,hx_-52*s,hy+6*s,7*s,6*s);c.set_source_rgb(*INK);c.fill()
    c.save();c.translate(hx_+14*s,hy+4*s);c.rotate(.3);ell(c,0,0,13*s,28*s);fs(c,DARK,max(3,4*s));c.restore()
    if pose=='sit':ell(c,hx_-14*s,hy-8*s,5*s,6*s);c.set_source_rgb(*INK);c.fill()
    else:c.move_to(hx_-20*s,hy-6*s);c.line_to(hx_-8*s,hy-6*s);c.set_source_rgb(*INK);c.set_line_width(4*s);c.stroke()
    return (x-2*s,gy-98*s)
def bot(c,x,gy,s,walk=0,eye=(0,0),glow=1,bob=0):
    y=gy-280*s-bob;robot(c,x,y,s,walk=walk,eye=eye,glow=glow);return y
# ---------- places ----------
def park(c,f,scroll=0):
    g=cairo.LinearGradient(0,0,0,1200);g.add_color_stop_rgb(0,*hx('8fd0ff'));g.add_color_stop_rgb(1,*hx('fff0c8'));c.set_source(g);c.paint()
    ell(c,850,560,90,90);c.set_source_rgba(1,.95,.6,.9);c.fill()
    for i in range(7):
        x=(i*270-scroll*.45)%1890-260;y=1190
        c.rectangle(x-14,y-190,28,200);c.set_source_rgb(*hx('8a5a34'));c.fill()
        for dx,dy,r in((-60,-230,80),(40,-260,90),(0,-330,80),(70,-190,70),(-70,-170,60)):ell(c,x+dx,y+dy,r,r);c.set_source_rgb(*hx('5cb85c'));c.fill()
    g=cairo.LinearGradient(0,1180,0,H);g.add_color_stop_rgb(0,*hx('8fd16b'));g.add_color_stop_rgb(1,*hx('4f9e43'));c.set_source(g);c.rectangle(0,1180,W,H);c.fill()
    c.rectangle(0,1440,W,140);c.set_source_rgb(*hx('ead9b0'));c.fill()
    for i in range(8):
        x=(i*170-scroll)%1360-140;ell(c,x,1640,70,26);c.set_source_rgba(.25,.55,.25,.5);c.fill()
def room(c):
    bg(c,hx('ffe2b8'),hx('f0b37e'))
    rr(c,620,420,360,440,18);fs(c,hx('bfe6ff'));c.rectangle(795,420,10,440);c.set_source_rgb(*INK);c.fill()
    c.rectangle(60,560,360,16);c.set_source_rgb(*hx('8a5a34'));c.fill()
    for i in range(5):c.rectangle(80+i*44,470,32,90);c.set_source_rgb(*[RED,BLUE,GREEN,YEL,GREY][i]);c.fill()
def office(c):
    bg(c,hx('e5edf8'),hx('aebfd8'))
    for i in range(3):rr(c,90+i*330,380,240,300,12);fs(c,hx('cde6ff'),6)
def desk(c,y=1300):
    c.rectangle(-10,y,W+20,H-y+10);c.set_source_rgb(*hx('b77a45'));c.fill_preserve();c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
    c.rectangle(-10,y,W+20,24);c.set_source_rgb(*hx('d8955a'));c.fill()
# ---------- scenes ----------
def hookframe(c,f,t):
    sc=t*18;park(c,f,sc)
    nx=1350-t*16
    if -200<nx<1300:
        lh=neighbor(c,nx,1420,.55,f,sip=.3+.3*math.sin(t*.2))
        dc=dog(c,nx+90,1430,.6,'sit',look=1,f=f)
        c.move_to(*lh);c.curve_to(lh[0],lh[1]+60,dc[0],dc[1]+40,*dc);c.set_source_rgb(*INK);c.set_line_width(4);c.stroke()
    bx=1000+math.sin(t*.25)*30;by=1490-abs(math.sin(t*.32))*230;ball(c,bx,by,36,t*.4)
    ry=bot(c,800,GROUND,1.15,walk=t*.9,bob=abs(math.sin(t*.45))*30)
    for i in range(4):
        ell(c,160-i*60+(t*7%60),1505-i*4,40-i*6,24-i*4);c.set_source_rgba(.92,.86,.7,.8-i*.15);c.fill()
    hx_,hy_=dragged(c,560,1475,.82,f)
    col=(800,ry+92*1.15)
    c.move_to(hx_,hy_);c.curve_to(hx_+150,hy_+40,col[0]-200,col[1]+40,*col);c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
    speed(c,f,760,1200,WHITE) if False else None
def A(c,f):
    hookframe(c,f,f);sub(c,f,6,42,'WAIT!',110)
def B(c,f):
    r=f-60;bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+r*noise(i,4)*80
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    t=['2025','2025','2024','2024'][min(3,r//4)]
    for dx,cc in((-12,(0,1,1)),(12,(1,0,.55))):txt(c,t,540+dx,900,260,cc,lw=0,alpha=.9)
    txt(c,t,540,900,260,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110;c.move_to(x+90,560);c.line_to(x,620);c.line_to(x+90,680);c.close_path();c.set_source_rgb(*YEL);c.fill()
    for yy in range(0,H,6):c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
def C(c,f):
    r=f-75;room(c);desk(c,1290)
    pat=r<52;tap=72<=r<92;press=1 if 80<=r<86 else 0
    rb=abs(math.sin(r*.5))*10 if r>=90 else 0
    ry=bot(c,760,1290,.6,walk=0,glow=.55 if pat else 1,eye=(0,-4) if pat else (0,0),bob=rb)
    button(c,560,1372,.9,press)
    gx,gy=360,880
    torso(c,gx,gy+150*1.25,1.5)
    if pat:
        p=abs(math.sin(r*.45))*16
        rarm(c,[(gx+112,gy+215),(gx+250,gy+110),(760,ry-70+p)],52,NAVY)
    elif r<72 or r>=92:
        rarm(c,[(gx+112,gy+215),(gx+190,gy+330),(gx+150,gy+380)],52,NAVY)
    else:
        k=cl((r-72)/8) if r<86 else 1-cl((r-86)/6)
        rarm(c,[(gx+112,gy+215),(lerp(gx+190,520,k),lerp(gx+330,1250,k)),(lerp(gx+150,560,k),lerp(gx+380,1335+press*14,k))],52,NAVY)
    if r>=46:
        b=(r//14)%2==0 and r>60
        rarm(c,[(gx-112,gy+215),(gx-230,gy+260),(gx-150,gy+120)],52,NAVY)
    guyhead(c,gx,gy,1.35,'happy',0)
    if r>=46:sandwich(c,gx-120,gy+100,1.3,bite=r>70)
    if 55<=r<88:holo(c,760,ry-200,'HELP?',max(.02,back((r-55)/4)))
    if r>=90:
        for i in range(3):
            a=r*.3+i*2;ell(c,760+math.cos(a)*120,ry-20+math.sin(a)*60,8,8);c.set_source_rgb(*YEL);c.fill()
    sub(c,f,81,122,"WHO'S A GOOD BOY?")
def D(c,f):
    r=f-210
    if r>=75:hookframe(c,f,r-75+18);return
    if 48<=r<60:c.translate(noise(f,1)*(60-r)*2.2,noise(f,2)*(60-r)*2.2)
    park(c,f,r*4)
    s=.7 if r<48 else lerp(.7,1.15,cl(back((r-48)/8)))
    ry=bot(c,720,GROUND,s,walk=r*.5 if r<48 else 0,bob=0)
    hy=guyfull(c,300,GROUND,.8,'calm',.3,arms=None)
    rarm(c,[(300+70,hy+140),(300+140,hy+230),(300+190,hy+260)],34,NAVY)
    col=(720,ry+92*s)
    c.move_to(490,hy+260);c.curve_to(560,hy+300,col[0]-120,col[1]+60,*col);c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
    pr=1 if 40<=r<46 else 0
    rarm(c,[(300-70,hy+140),(300-150,hy+180),(300-90,hy+60)],34,NAVY)
    if r<48:phone(c,300-80,hy+10,.9,pr,-.2)
    else:
        k=cl((r-48)/16);phone(c,300-80+k*60,hy+10-math.sin(k*math.pi)*360-k*80,.9,0,-.2+k*6)
    if 12<=r<44:holo(c,720,ry-200*s-60,'MORE?',max(.02,back((r-12)/4)))
    if r>=48 and r<60:
        k=(r-48)/12;c.save();c.translate(720,ry);c.scale(1+k,1+k)
        for i in range(8):
            c.rotate(math.pi/4);c.move_to(0,-260);c.line_to(30,-160);c.line_to(-30,-160);c.close_path()
        c.set_source_rgba(1,1,1,1-k);c.fill();c.restore()
CROWD=[(120,700,.45),(330,660,.45),(750,660,.45),(960,700,.45),(110,960,.55),(980,960,.55),(260,860,.5),(820,860,.5),(560,620,.42),(440,760,.42),(660,760,.42)]
def crowd(c,f,r0,alpha=1,qs=False):
    for i,(x,y,s_) in enumerate(CROWD):
        d=r0-i*2
        if d<0:continue
        yy=(y-(1-cl(back(d/6)))*500 if d<6 else y)+math.sin(f*.35+i*1.3)*7
        dx=560-x;dy=1440-yy;n=math.hypot(dx,dy)
        robot(c,x,yy,s_,eye=(dx/n*10,dy/n*12),rot=dx/n*.18)
        paper(c,x+80*s_,yy+150*s_,s_*1.1,.2+math.sin(f*.5+i)*.25)
    if qs:
        for j,(i,t0) in enumerate(((1,0),(3,10),(6,20))):
            x,y,s_=CROWD[i]
            if r0>=t0+12 and r0<54:
                k=max(.02,back((r0-t0-12)/4));c.save();c.translate(x,y-150*s_-40);c.scale(k,k)
                ell(c,0,0,34,34);fs(c,WHITE,6);txt(c,'?',0,0,50,RED,lw=0);c.restore()
def officeguy(c,x,hy,s,age,expr='calm'):
    torso(c,x,hy+150*s,1.2*s);guyhead(c,x,hy,s*1.08,expr,age)
def E(c,f):
    r=f-315;office(c)
    if r>=22:crowd(c,f,r-22,qs=True)
    robot(c,170 if r>=22 else 800,880,1.0)
    officeguy(c,420,1010,1.05,.6)
    rate=0 if r<30 else (r-30)**1.5*.012
    pr=max(0,math.sin(rate*2*math.pi)) if r>=30 else (1 if 20<=r<26 else 0)
    rarm(c,[(420+92,1010+184),(520,1300),(560,1395+pr*16)],48,NAVY)
    desk(c,1380);button(c,560,1440,1,pr)
    if r<22:holo(c,800,640,'HIRE|HELP?',max(.02,back(r/4)))
    if r>=74:
        k=oe((r-74)/8);tx=lerp(1200,880,k)
        tester(c,tx,1180,.72)
        rarm(c,[(tx-40,1260),(tx-140,1100),(lerp(1100,650,k),960)],22)
        paper(c,lerp(1120,640,k),930,1.7,-.06)
    sub(c,f,315+80,315+106,'DID YOU READ IT?');sub(c,f,315+107,315+120,'APPROVE.')
def F(c,f):
    r=f-435;office(c);crowd(c,f,99)
    robot(c,820,820,1.35)
    roll=oe((r-84)/20)*-760 if r>=84 else 0
    gx=420+roll
    chair(c,gx,1300,1.05,spin=roll*.02)
    officeguy(c,gx,1010,1.05,.8,'small')
    hand=None
    if r<36:hand=(560,1395)
    elif r<58:hand=(560,1395+(16 if r<42 else 0))
    elif r<66:k=(r-58)/8;hand=(lerp(560,520,k),lerp(1395,1380,k))
    elif r<72:hand=(520,1380)
    else:k=cl((r-72)/10);hand=(lerp(520,gx+120,k),lerp(1380,1300,k))
    rarm(c,[(gx+92,1010+184),(lerp(gx+92,hand[0],.5)+20,1290),hand],48,NAVY)
    desk(c,1380)
    pr=0
    if r>=44:
        k=oe((r-44)/6);pr=max(0,math.sin(r*1.5))
        rarm(c,[(820-90,820+150),(lerp(1000,700,k),1200),(lerp(1100,560,k),1392+pr*16)],46)
    if 62<=r<86:
        k=cl((r-62)/6)*(1-cl((r-80)/6));push=cl((r-72)/10)
        rarm(c,[(1100,1500),(lerp(1100,640,k),1420),(lerp(1180,lerp(540,gx+150,push),k),lerp(1370,1300,push*k))],34)
    button(c,560,1440,1,pr if r>=44 else (1 if 36<=r<42 else 0))
    if r<32:holo(c,820,520,'CAN I|APPROVE?',max(.02,back(r/4)))
    sub(c,f,435+34,435+58,'...APPROVE.')
def closeface(c,f,r):
    park(c,f,0);c.rectangle(0,0,W,H);c.set_source_rgba(1,1,1,.25);c.fill()
    torso(c,540,1330,2.2)
    if r<12:guyhead(c,540,1050,2.4,'focus',1)
    else:
        v.HAIR=(.72,.72,.76);v.BEARD=True;v.GAZE=18
        head(c,540,1050,2.4,'small',rot=.12);v.HAIR=(.25,.13,.09);v.BEARD=False;v.GAZE=0
    if 10<=r<20:
        k=(r-10)/10;ball(c,lerp(-60,1140,k),lerp(560,420,k)-math.sin(k*math.pi)*80,40,r*.6)
        for i in range(3):ell(c,lerp(-60,1140,k)-60-i*50,lerp(560,420,k),20-i*5,8);c.set_source_rgba(1,1,1,.6-i*.15);c.fill()
def G(c,f):
    r=f-540
    if 46<=r<68:closeface(c,f,r-46);return
    park(c,f,0)
    nl=neighbor(c,930,1420,.55,f,sip=.5+.5*math.sin(r*.08))
    pose='sit' if r<98 else 'lie'
    dc=dog(c,930,1600,1.1,pose,look=1 if 68<=r<90 else 0,f=f if r<98 else 0)
    c.move_to(*nl);c.curve_to(nl[0],nl[1]+200,dc[0]+80,dc[1]-120,*dc);c.set_source_rgb(*INK);c.set_line_width(4);c.stroke()
    happy=r>=60
    ry=bot(c,360,1500,2.95,walk=0,eye=(0,-6) if happy else (14,8),glow=.55 if happy else 1,bob=abs(math.sin(r*.4))*12 if happy else 0)
    hyg=1495-540*.75
    if r<46:
        hy=guyfull(c,770,1495,.75,'calm',1)
        p=abs(math.sin(r*.42))*14
        rarm(c,[(360+200,ry+330),(680,ry+150),(770,hyg-135+p)],56)
    elif r<100:
        x=lerp(770,1300,cl((r-68)/26)**1.2)
        hy=guyfull(c,x,1495-abs(math.sin(r*.9))*18,.75,'happy',1,run=r*.9)
        for i in range(3):ell(c,x-80-i*55,1490,32-i*6,18-i*3);c.set_source_rgba(.92,.86,.7,.8-i*.2);c.fill()
        rarm(c,[(360+200,ry+330),(640,ry+200),(600,ry+120)],56)
        if r<84:k=(r-68)/16;ball(c,lerp(900,1250,k),lerp(900,1300,k)-math.sin(k*math.pi)*200,30,r*.4)
    else:
        k=cl((r-118)/24);x=lerp(1250,770,oe(k))
        hy=guyfull(c,x,1495-abs(math.sin(r*.7))*12*(1-k),.75,'happy',1,run=r*.7 if k<1 else None)
        ball(c,x,hy+62*.81+6,27,0)
        if r>=146:
            p=abs(math.sin((r-146)*.42))*14
            rarm(c,[(360+200,ry+330),(680,ry+150),(770,hyg-135+p)],56)
        else:rarm(c,[(360+200,ry+330),(640,ry+200),(600,ry+120)],56)
    if 98<=r<112:
        for i in range(3):ell(c,800+i*40,1560-(r-98)*4,10+i*3,8+i*2);c.set_source_rgba(1,1,1,.7-(r-98)*.05);c.fill()
    sub(c,f,546,586,"WHO'S A GOOD BOY?")
    if r>=120:badge(c)
SC=[('A',0,60,A),('B',60,75,B),('C',75,210,C),('D',210,315,D),('E',315,435,E),('F',435,540,F),('G',540,720,G)]
def draw(f):
    s=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(s)
    for n,a,b,fn in SC:
        if a<=f<b:
            c.save();fn(c,f);c.restore();break
    topbar(c,f)
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
