import cairo, math, random, subprocess, sys, os
W,H,FPS=1080,1920,30
INK=(.07,.08,.13); WHITE=(1,1,1); NAVY=(.11,.15,.27); SKIN=(1,.87,.76); HAIR=(.25,.13,.09)
BLUE=(.2,.75,1); YEL=(1,.84,.15); RED=(.95,.2,.25); GREEN=(.15,.8,.42); GREY=(.62,.65,.72)
hx=lambda h:tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
cl=lambda t:max(0,min(1,t)); lerp=lambda a,b,t:a+(b-a)*t
oe=lambda t:1-(1-cl(t))**3
def back(t):
    t=cl(t);k=2.2;return 1+(k+1)*(t-1)**3+k*(t-1)**2
def noise(f,k=0): return random.Random(f*7919+k).uniform(-1,1)
def rr(c,x,y,w,h,r):
    c.new_sub_path();c.arc(x+w-r,y+r,r,-math.pi/2,0);c.arc(x+w-r,y+h-r,r,0,math.pi/2);c.arc(x+r,y+h-r,r,math.pi/2,math.pi);c.arc(x+r,y+r,r,math.pi,1.5*math.pi);c.close_path()
def fs(c,fill,lw=8,st=INK):
    c.set_source_rgb(*fill)
    if lw: c.fill_preserve();c.set_source_rgb(*st);c.set_line_width(lw);c.stroke()
    else: c.fill()
def ell(c,x,y,a,b):
    c.save();c.translate(x,y);c.scale(a,b);c.new_sub_path();c.arc(0,0,1,0,2*math.pi);c.restore()
def limb(c,pts,w,col):
    c.set_line_cap(cairo.LINE_CAP_ROUND);c.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw,cc in((w+14,INK),(w,col)):
        c.move_to(*pts[0])
        for p in pts[1:]:c.line_to(*p)
        c.set_source_rgb(*cc);c.set_line_width(lw);c.stroke()
def txt(c,s,x,y,size,fill=WHITE,lw=None,st=INK,rot=0,scale=1,align='c',alpha=1):
    if scale<=0.01:return
    c.save();c.select_font_face('Lilita One');c.set_font_size(size);e=c.text_extents(s)
    c.translate(x,y);c.rotate(rot);c.scale(scale,scale)
    ox=-e.width/2-e.x_bearing if align=='c' else (-e.x_bearing if align=='l' else -e.width-e.x_bearing)
    c.move_to(ox,size*.36);c.text_path(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    lw=size*.16 if lw is None else lw
    if lw: c.set_source_rgba(*st,alpha);c.set_line_width(lw);c.stroke_preserve()
    c.set_source_rgba(*fill,alpha);c.fill();c.restore()
def shades(c,x,y,s,rot=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    rr(c,-92,-28,84,58,22);rr(c,8,-28,84,58,22);c.set_source_rgb(.04,.04,.07);c.fill()
    c.set_source_rgb(.04,.04,.07);c.set_line_width(10);c.move_to(-10,-14);c.line_to(10,-14);c.stroke()
    c.move_to(-76,-12);c.line_to(-48,-12);c.move_to(24,-12);c.line_to(52,-12);c.set_source_rgba(1,1,1,.55);c.set_line_width(7);c.stroke()
    c.restore()
def robot(c,x,y,s,boss=False,walk=None,glow=1,rot=0,noshade=False):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s);c.set_line_cap(cairo.LINE_CAP_ROUND)
    if walk is not None:
        a=math.sin(walk)*26
        limb(c,[(-34,205),(-34-a,280)],34,WHITE);limb(c,[(34,205),(34+a,280)],34,WHITE)
    rr(c,-72,85,144,135,44);fs(c,WHITE)
    ell(c,0,150,30,30);fs(c,(.82,.86,.93),5)
    c.move_to(0,-90);c.line_to(0,-132);c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
    ell(c,0,-140,17,17);fs(c,BLUE,7)
    for q in(-1,1):
        ell(c,q*110,0,22,38);fs(c,GREY,8)
    rr(c,-108,-95,216,180,78);fs(c,WHITE)
    if not boss: rr(c,-82,-54,164,92,40);fs(c,hx('0b1020'),6)
    if boss:
        shades(c,0,-12,1.02)
        c.move_to(-16,52);c.curve_to(-6,62,22,60,38,44);c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
    else:
        for q in(-1,1):
            ell(c,q*36,-8,18,23*glow+1);c.set_source_rgb(*BLUE);c.fill()
    c.restore()
def head(c,x,y,s,expr='calm',cool=False,rot=0,f=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s)
    blobs=[(-92,-58,48),(-55,-104,54),(5,-122,58),(62,-100,52),(98,-52,44),(-108,-8,32),(112,-6,30),(-25,-132,36),(40,-136,32)]
    for b in blobs: ell(c,b[0],b[1],b[2],b[2])
    c.set_source_rgb(*INK);c.set_line_width(16);c.stroke()
    for q in(-1,1): ell(c,q*104,18,18,24);fs(c,SKIN,7)
    rr(c,-100,-72,200,178,84);fs(c,SKIN)
    # stubble
    rnd=random.Random(4);c.set_source_rgba(*HAIR,.5)
    for i in range(30):
        a=rnd.uniform(.2*math.pi,.8*math.pi);r=rnd.uniform(.88,1)
        ell(c,math.cos(a)*84*r,20+math.sin(a)*80*r,2,2);c.fill()
    for b in blobs: ell(c,b[0],b[1],b[2],b[2])
    c.set_source_rgb(*HAIR);c.fill()
    for bx,by,br in[(-72,-46,32),(-30,-58,33),(18,-62,32),(62,-46,30)]:
        ell(c,bx,by,br,br);c.fill()
    c.set_source_rgb(.43,.26,.18);c.set_line_width(5);c.arc(0,-108,50,-2.5,-1);c.stroke()
    if cool: shades(c,0,8,1)
    elif expr=='cry':
        for q in(-1,1):
            c.move_to(q*62,24);c.curve_to(q*50,0,q*20,0,q*12,24);c.set_source_rgb(*INK);c.set_line_width(9);c.stroke()
            for j in range(2):
                ph=((f/10+j*.5)%1);ell(c,q*(42+j*8),34+ph*90,10,16);fs(c,hx('58c7ff'),3)
    else:
        for q in(-1,1):
            ey=8
            if expr=='small': ell(c,q*42,ey,12,12);c.set_source_rgb(*INK);c.fill();continue
            ell(c,q*42,ey,23,27);c.set_source_rgb(*INK);c.fill();ell(c,q*34,ey-10,8,8);c.set_source_rgb(1,1,1);c.fill()
            if expr=='focus':
                c.move_to(q*72,-32);c.line_to(q*18,-14);c.set_source_rgb(*INK);c.set_line_width(10);c.stroke()
    c.set_source_rgb(*INK);c.set_line_width(6)
    if expr=='cry':
        ell(c,0,70,24,20);fs(c,hx('7a2230'),6)
    elif expr=='small':
        ell(c,0,72,11,14);fs(c,hx('7a2230'),5)
    else:
        c.arc(-11,62,11,.2,math.pi-.1);c.new_sub_path();c.arc(11,62,11,.1,math.pi-.2);c.stroke()
    c.restore()
def torso(c,x,y,s):
    c.save();c.translate(x,y);c.scale(s,s)
    rr(c,-92,-30,184,190,60);fs(c,NAVY)
    ell(c,0,-16,74,34);fs(c,hx('0b1020'),6)
    for q in(-1,1):
        c.move_to(q*16,0);c.line_to(q*18,56);c.set_source_rgb(.95,.95,.98);c.set_line_width(7);c.stroke()
    c.restore()
def pill(c,x,y,w,h,col,lw=8):
    rr(c,x-w/2,y-h/2,w,h,h/2);fs(c,col,lw)
def badge(c):
    c.save();rr(c,330,146,420,58,29);c.set_source_rgba(.04,.05,.1,.75);c.fill();c.restore()
    txt(c,'promptanatomy.app',540,175,34,lw=0)
def caption(c,year,title,col,f,f0):
    t=(f-f0)/8
    txt(c,year,540,330,150,YEL,scale=back(t),lw=24)
    t2=(f-f0-5)/8
    txt(c,title,540,470,98,col,scale=back(t2),rot=-.015,lw=18)
def rays(c,col,f,cx=540,cy=1000,a=.12):
    c.save();c.translate(cx,cy);c.rotate(f*.012)
    for i in range(12):
        c.move_to(0,0);th=i/12*2*math.pi;c.line_to(2400*math.cos(th),2400*math.sin(th));c.line_to(2400*math.cos(th+.26),2400*math.sin(th+.26));c.close_path()
    c.set_source_rgba(*col,a);c.fill();c.restore()
def bg(c,top,bot):
    g=cairo.LinearGradient(0,0,0,H);g.add_color_stop_rgb(0,*top);g.add_color_stop_rgb(1,*bot);c.set_source(g);c.paint()
def shake(c,f,f0,amp,dur=10):
    d=f-f0
    if 0<=d<dur:
        k=amp*(1-d/dur);c.translate(noise(f,1)*k,noise(f,2)*k)
def bubble(c,lines,size,x=540,y=500,w=900,h=None,hl=()):
    h=h or 380
    c.move_to(x-20,y+h/2-6);c.line_to(x+8,y+h/2+70);c.line_to(x+78,y+h/2-6);c.close_path();fs(c,WHITE)
    rr(c,x-w/2,y-h/2,w,h,56);fs(c,WHITE)
    c.move_to(x-14,y+h/2-4);c.line_to(x+70,y+h/2-4);c.set_source_rgb(1,1,1);c.set_line_width(12);c.stroke()
    n=len(lines);lh=size*1.12;y0=y-(n-1)*lh/2
    for i,l in enumerate(lines):
        txt(c,l,x,y0+i*lh,size,RED if i in hl else INK,lw=0)
def office(c,f,sw=0,z=1.0):
    bg(c,hx('10354f'),hx('0d2236'))
    c.save();c.translate(540,1000);c.scale(z,z);c.translate(-540,-1000)
    for i in range(6):
        c.rectangle(90+i*180,740,8,420);c.set_source_rgba(1,1,1,.05);c.fill()
    nod=math.sin(f*math.pi/15)*5
    robot(c,150,890+nod,.9);robot(c,930,890-nod,.9)
    robot(c,540,860,1.42,boss=True)
    # desk
    rr(c,-40,1080,1160,60,18);fs(c,hx('a9713f'))
    c.rectangle(30,1140,1020,430);c.set_source_rgb(*hx('7c4f2a'));c.fill_preserve();c.set_source_rgb(*INK);c.set_line_width(8);c.stroke()
    rr(c,190,1170,700,92,12);fs(c,hx('f5e6c5'),7)
    txt(c,'HEAD OF HUMAN RESOURCES',540,1216,46,INK,lw=0)
    # CV in robot hands
    rr(c,380,960,120,84,8);fs(c,WHITE,6)
    txt(c,'CV',440,1000,40,INK,lw=0)
    limb(c,[(450,1100),(430,1040)],24,WHITE);limb(c,[(640,1090),(620,1030)],24,WHITE)
    # guy from behind
    gx,gy=250,1480
    rr(c,gx-190,gy+90,380,420,120);fs(c,hx('2a3a6b'))
    ell(c,gx,gy+105,105,58);fs(c,hx('18213a'),7)
    for b in[(-90,-40,62),(-40,-95,66),(30,-100,66),(92,-45,60),(0,-20,105),(-60,40,62),(60,40,62)]: ell(c,gx+b[0],gy+b[1],b[2],b[2])
    c.set_source_rgb(*INK);c.set_line_width(16);c.stroke()
    for b in[(-90,-40,62),(-40,-95,66),(30,-100,66),(92,-45,60),(0,-20,105),(-60,40,62),(60,40,62)]: ell(c,gx+b[0],gy+b[1],b[2],b[2])
    c.set_source_rgb(*HAIR);c.fill()
    d=sw*(f%30)/30
    ell(c,gx+150,gy-90+d*60,20+sw*4,30+sw*5);fs(c,hx('58c7ff'),5)
    c.restore()
BL=['SAYS HERE YOU','USED TO BE','OUR BOSS?']
def s_open(c,f):
    t=f/90;z=1+.05*t
    if f>=78:c.translate(noise(f,1)*(f-78)*1.4,noise(f,2)*(f-78))
    office(c,f,1,z)
    bubble(c,BL,98,y=545,h=340,hl=(2,))
    txt(c,'2027',540,282,92,YEL,lw=17)
    if f>=48: txt(c,'hehe',150,750,52,WHITE,lw=9,rot=-.15,scale=back((f-48)/5));txt(c,'hehe',930,750,52,WHITE,lw=9,rot=.15,scale=back((f-52)/5))
    badge(c)
def s_rew(c,f):
    r=f-90
    bg(c,hx('24003f'),hx('050014'))
    for i in range(14):
        y=(noise(i,3)*.5+.5)*H+ r*noise(i,4)*40
        c.rectangle(0,y,W,noise(i,5)*22+26);c.set_source_rgba(*((.1,.9,1) if i%2 else (1,.15,.6)),.16);c.fill()
    y=['2027','2026','2025','2024'][min(3,r//7)]
    for dx,cc in((-16,(0,1,1)),(16,(1,0,.55))): txt(c,y,540+dx,900,290,cc,lw=0,alpha=.9)
    txt(c,y,540,900,290,WHITE,lw=0)
    for q in(0,1):
        x=350+q*110
        c.move_to(x+90,560);c.line_to(x,620);c.line_to(x+90,680);c.close_path();c.set_source_rgb(*YEL);c.fill()
    txt(c,'HOW DID THIS HAPPEN?',540,1170,70,YEL,lw=13)
    for yy in range(0,H,6):
        c.rectangle(0,yy,W,2);c.set_source_rgba(0,0,0,.14);c.fill()
    badge(c)
PL=[('You are a world-class expert.',132),('Think step by step.',157),('Please.',172),('I BEG YOU.',187)]
def s_24(c,f):
    bg(c,hx('ffd84a'),hx('ff9d2e'));rays(c,WHITE,f,540,1250,.16);shake(c,f,120,10,6)
    caption(c,'2024','PROMPT ENGINEER',WHITE,f,120)
    rr(c,90,590,900,330,40);fs(c,WHITE)
    for i,(l,st) in enumerate(PL):
        col,sz=(RED,84) if i==3 else (INK,54)
        txt(c,l,540,640+i*64+(14 if i==3 else 0),sz,col,lw=0,scale=back((f-st)/4))
    j=noise(f,7)*5;y=1240
    torso(c,540,y+60,1.3)
    head(c,540,y-90+j*.4,1.25,'focus')
    ell(c,720,y-190+(f%20)*2,17,25);fs(c,hx('58c7ff'),5)
    rr(c,250,y+160,580,350,30);fs(c,hx('8e94a6'))
    ell(c,540,y+330,42,42);c.set_source_rgb(*hx('b8bdcc'));c.fill()
    for q,ph in((-1,0),(1,1)):
        h=8*math.sin(f*1.6+ph*2)
        limb(c,[(540+q*120,y+90),(540+q*235,y+155+h)],52,NAVY);ell(c,540+q*235,y+160+h,28,24);fs(c,SKIN,7)
    badge(c)
ERR=[(210,'ERROR',230,800,.1,70),(225,'PROD IS DOWN',770,700,-.09,62),(240,'847 BUGS',765,960,.12,70),(247,'WHO DELETED THE DB?',440,650,-.04,54),(255,'NaN NaN',790,1105,-.08,58)]
def s_25(c,f):
    bg(c,hx('5a22d6'),hx('180b52'));shake(c,f,195,10,6)
    rnd=random.Random(9)
    cols=[hx(x) for x in('ff5fd2','47e6ff','7dff72','ffd84a','ff8a3d')]
    for i in range(26):
        y=rnd.randint(620,1500);w=rnd.randint(70,230);sp=rnd.uniform(4,10);x=(rnd.randint(0,1300)-f*sp)%1300-150
        rr(c,x,y,w,20,10);c.set_source_rgba(*rnd.choice(cols),.5);c.fill()
    caption(c,'2025','VIBE CODER',hx('8ff7ff'),f,195)
    for st,l,x,y,rot,sz in ERR:
        if f<st:continue
        c.save();c.translate(x,y);c.rotate(rot);k=max(.02,back((f-st)/5));c.scale(k,k)
        c.select_font_face('Lilita One');c.set_font_size(sz);w=c.text_extents(l).width+70
        rr(c,-w/2,-sz*.95,w,sz*1.9,18);fs(c,RED);txt(c,l,0,0,sz,WHITE,lw=0);c.restore()
    bob=abs(math.sin((f-195)*math.pi/15))*14
    ell(c,520,1420,350,210);fs(c,hx('2f7bea'))
    ell(c,430,1340,120,46);c.set_source_rgba(1,1,1,.17);c.fill()
    limb(c,[(590,1370),(790,1395),(890,1340)],60,hx('14151e'));ell(c,905,1315,50,36);fs(c,WHITE)
    limb(c,[(560,1420),(760,1460),(850,1450)],60,hx('14151e'));ell(c,875,1432,50,36);fs(c,WHITE)
    c.save();c.translate(490,1270);c.rotate(-.2);torso(c,0,0,1.25);c.restore()
    rr(c,560,1195,210,155,14);fs(c,hx('8e94a6'))
    limb(c,[(590,1300),(670,1355)],44,NAVY)
    head(c,455,1120+bob,1.25,cool=True,rot=-.13)
    if f>=240: txt(c,'vibes: immaculate',430,1570,70,YEL,lw=14,rot=-.03,scale=back((f-240)/5))
    badge(c)
def s_26(c,f):
    bg(c,hx('ff6a2b'),hx('c91e47'));rays(c,hx('ffd84a'),f,540,1000,.14);shake(c,f,270,10,6)
    caption(c,'2026','AI AGENT BOSS',WHITE,f,270)
    # marching
    y=1000
    rr(c,350,y+215,380,180,14);fs(c,hx('a9713f'))
    limb(c,[(505,y+100),(505,y+210)],52,hx('14151e'));limb(c,[(590,y+100),(590,y+210)],52,hx('14151e'))
    for x_ in(490,600): ell(c,x_,y+215,48,24);fs(c,WHITE)
    torso(c,545,y-30,1.1)
    arm=math.sin((f-270)*math.pi/7.5)*12
    limb(c,[(460,y),(310,y-70+arm),(205,y-90+arm)],46,NAVY);ell(c,195,y-95+arm,30,30);fs(c,SKIN,7)
    limb(c,[(630,y-10),(680,y+70),(640,y+95)],46,NAVY)
    hy=y-155
    # stolen shades state
    tl=330;tg=357
    cool=f<tl-6
    head(c,545,hy,1.1,cool=cool,expr='calm',f=f)
    # tiny thief
    tx=lerp(1020,700,oe((f-300)/22)) if f<tl else 700
    ty=y+150
    if f>=300 and f<tl: ty=lerp(y+150,hy-30,oe((f-308)/20)) if f>=308 else ty
    if f>=tl:
        # gets shades, runs off
        ru=(f-tl)/(tg-tl);tx=lerp(700,1120,ru);ty=lerp(hy-30,y+160,oe(ru*2.2))-abs(math.sin(f*.8))*18
    if f>=300:
        robot(c,tx,ty,.38,walk=f*.8,boss=f>=tl)
        if tl-6<=f<tl:
            k=(f-tl+6)/6;shades(c,lerp(545,tx,k),lerp(hy+9,ty-5,k),lerp(1.1,.39,k))
    for i in range(5):
        x=(1400-(f-270)*7+i*300)%1500-200;w=(f-270)*.55+i
        robot(c,x,1385-abs(math.sin(w))*14,.78,walk=w)
    if 276<=f<306: txt(c,'FASTER!',230,760,74,YEL,lw=14,rot=-.1,scale=back((f-276)/5))
    badge(c)
def s_hire(c,f):
    r=f-375
    if r>=30: shake(c,f,405,34,12)
    office(c,f,1,1.03)
    k=oe(r/8)
    y=lerp(1950,870,k)
    c.save();c.translate(540,y);c.rotate(-.025)
    rr(c,-430,-470,860,890,28);fs(c,hx('fbf8ee'),10)
    txt(c,'OFFER LETTER',0,-385,74,INK,lw=0)
    c.rectangle(-360,-325,720,8);c.set_source_rgb(*INK);c.fill()
    txt(c,'ROLE:',-360,-245,58,hx('66707f'),lw=0,align='l')
    txt(c,'PROMPT',-360,-165,104,INK,lw=0,align='l');txt(c,'ENGINEER',-360,-65,104,INK,lw=0,align='l')
    if r>=45:
        s=back((r-45)/6)
        txt(c,'PAY:',-360,40,58,hx('66707f'),lw=0,align='l')
        txt(c,'12 TOKENS/HOUR',0,130,88,RED,lw=0,scale=s)
    c.restore()
    if r>=30:
        s=lerp(3,1,cl((r-30)/4))
        c.save();c.translate(650,1190);c.rotate(-.2);c.scale(s,s)
        rr(c,-235,-85,470,170,18);c.set_source_rgb(*GREEN);c.set_line_width(16);c.stroke()
        txt(c,'HIRED',0,0,134,GREEN,lw=0);c.restore()
    badge(c)
def s_thx(c,f):
    bg(c,hx('ff8ebf'),hx('e8437e'));rays(c,WHITE,f,540,1050,.13)
    torso(c,540,1300,2.2)
    head(c,540,1030+noise(f//2,8)*6,2.3,'cry',f=f)
    txt(c,'THANK YOU, SIR.',540,430,108,WHITE,lw=20,scale=back((f-450)/6))
    badge(c)
def s_more(c,f):
    t=(f-480)/30;z=lerp(1.03,1.0,oe(t))
    office(c,f,1,z)
    bubble(c,['ONE MORE','THING...'],128,y=545,h=340)
    txt(c,'2027',540,282,92,YEL,lw=17)
    badge(c)
SC=[('a',0,90,s_open),('b',90,120,s_rew),('c',120,195,s_24),('d',195,270,s_25),('e',270,375,s_26),('f',375,450,s_hire),('g',450,480,s_thx),('h',480,510,s_more)]
def draw(f):
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H);c=cairo.Context(surf)
    for n,a,b,fn in SC:
        if a<=f<b: fn(c,f);break
    return surf
if __name__=='__main__':
    if sys.argv[1]=='frames':
        for f in map(int,sys.argv[2:]): draw(f).write_to_png(f'chk_{f:03d}.png')
    else:
        for n,a,b,fn in SC:
            if len(sys.argv)>2 and n not in sys.argv[2:]:continue
            p=subprocess.Popen(f'ffmpeg -y -v error -f rawvideo -pix_fmt bgra -s {W}x{H} -r 30 -i - -vf format=yuv420p -c:v libx264 -crf 17 -preset veryfast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -video_track_timescale 15360 tmp_{n}.mp4'.split(),stdin=subprocess.PIPE)
            for f in range(a,b):p.stdin.write(bytes(draw(f).get_data()))
            p.stdin.close();assert p.wait()==0;os.rename(f'tmp_{n}.mp4',f'{n}.mp4');print(n,flush=True)
