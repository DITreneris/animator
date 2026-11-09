import numpy as np,wave,subprocess,sys
E=sys.argv[1]
sr=44100;D=25.0;N=int(sr*D);rng=np.random.default_rng(3)
m=np.zeros(N);fx=np.zeros(N);vo=np.zeros(N)
def add(buf,t,x,g=1):
    idx=(int(t*sr)+np.arange(len(x)))%N;np.add.at(buf,idx,x*g)
T=lambda d:np.arange(int(d*sr))/sr
def kick(g=1):
    t=T(.22);return np.sin(2*np.pi*(48*t+(110/30)*(1-np.exp(-30*t))))*np.exp(-t*14)*g
def noise(d,dec):
    t=T(d);return rng.standard_normal(len(t))*np.exp(-t*dec)
hp=lambda x:np.diff(x,prepend=0)
lp=lambda x,n:np.convolve(x,np.ones(n)/n,'same')
def sq(fr,d,dec=4,duty=.5):
    t=T(d);return np.where((t*fr)%1<duty,1,-1)*np.exp(-t*dec)
midi=lambda n:440*2**((n-69)/12)
def sweep(a,b,d,dec=0,kind='sine'):
    t=T(d);fr=np.linspace(a,b,len(t));ph=np.cumsum(fr)/sr*2*np.pi
    return (np.sign(np.sin(ph)) if kind=='sq' else np.sin(ph))*np.exp(-t*dec)
def load(n):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'vo/v_{n}.wav','-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
    return x/np.abs(x).max()
def click():return hp(noise(.03,90))*.6+sq(1800,.03,60)*.2
def chime():return sweep(1200,1200,.3,8)+sweep(1800,1800,.3,7)*.6
def blip(f=1400):return sq(f,.06,20,.3)+sq(f*1.5,.06,25,.3)*.6
def thud(g=1):return kick(1.6*g)+lp(noise(.22,14),8)*.8*g
SEC=[(0,3,33,[0,3,7,10],.55,1),(3.5,7,40,[0,4,7,12],.9,0),(7,14,36,[0,4,7,11],.75,0),(14,16.2,38,[0,4,7,12],.8,0),(16.6,18,31,[0,3,7,10],.45,1),
     (18,22.5,33,[0,3,7,10],.3,1),(22.6,24.3,40,[0,4,7,12],.95,0),(24.3,25,33,[0,3,7,10],.55,1)]
import os
if os.environ.get('NOTAG')=='1':SEC=SEC[:-2]+[(22.6,25,40,[0,4,7,12],.95,0)]   # no loop: robots' music to the end
for a,b,r,ar,g,soft in SEC:
    t=a;k=0
    while t<b-1e-6:
        if not soft and k%2==0:add(m,t,kick(),.9*g)
        if not soft and k%4==2:add(m,t,hp(noise(.14,24)),.22*g)
        add(m,t,hp(hp(noise(.04,120))),.05*g)
        add(m,t,sq(midi(r+(12 if k%8 in(3,6) else 0)),.23,6),.15*g)
        add(m,t,sq(midi(r+24+ar[k%4]),.2,10,.25),.07*g)
        t+=.25;k+=1
# rain beds
for a,b in((0,3),(18,25)):
    r=lp(noise(b-a,0),6);r*=np.minimum(1,np.minimum(T(b-a)/.1,(b-a-T(b-a))/.1));add(fx,a,r,.06)
# hook
add(fx,.2,click(),.7);add(fx,.3,sweep(300,90,.45,3,'sq'),.12);add(fx,.3,thud(.6),.5)
for i in range(6):add(fx,.6+i*.07,lp(noise(.05,40),4),.35)       # wings
for t in(1.05,2.6):add(fx,t,sweep(420,330,.18,6)*(1+.5*np.sin(2*np.pi*30*T(.18))),.08)  # coo
r_=sweep(1400,90,.5,0,'sq');add(fx,3.0,r_*np.linspace(.4,.9,len(r_)),.16);n=noise(.5,0);add(fx,3.0,hp(n)*np.linspace(.3,.7,len(n)),.18)
# 2024
t=3.6
while t<5.5:add(fx,t,click(),.5);t+=.36
t=3.7
while t<5.6:add(fx,t,click(),.18);t+=.045
for i,t in enumerate((5.6,5.73,5.87)):add(fx,t,lp(noise(.3,10),3),.4);add(fx,t+.02,sweep(900+i*200,300,.25,6),.06)
add(fx,5.62,chime(),.12)
# 2025
add(fx,7.0,kick(.6));add(fx,7.0,noise(.05,60),.25)
rr_=np.random.default_rng(9)
t=8.4
while t<9.7:add(fx,t,blip(rr_.choice([900,1200,1500,1800,2200])),.14);t+=.09
add(fx,9.9,chime(),.14);add(fx,9.93,thud(.7),.6)
add(fx,12.05,sweep(1500,2400,.08,20),.15)        # plink
add(fx,13.7,sq(300,.14,8,.5),.08);add(fx,13.85,sq(240,.2,6,.5),.08)
# 2026 corridor
t=14.05
while t<15.4:add(fx,t,lp(noise(.06,40),6),.35);add(fx,t+.12,sq(1300,.03,50,.3),.04);t+=.25
add(fx,15.4,sweep(200,900,.35,5),.3);add(fx,15.45,sweep(600,1500,.3,6),.1)          # bloop
for i in range(4):add(fx,15.6+i*.09,lp(click(),6),.5-i*.1)                               # cable drop
add(fx,16.2,thud(1.2),.9);add(fx,16.2,lp(noise(.4,8),10),.6)
for i,n_ in enumerate((55,54,53,50)):add(fx,16.5+i*.28,sq(midi(n_),.3 if i<3 else .7,4,.5),.07)   # sad horn
# bridge
for i in range(10):add(fx,18.03+i*.045,sq(2400+i*80,.03,40,.3),.05);add(fx,18.03+i*.045,lp(noise(.03,60),2),.25)   # zip
add(fx,22.55,sweep(200,1200,.6,2),.12);add(fx,22.55,hp(noise(.6,3)),.12)                # whoosh up
t=23.1
while t<24.2:add(fx,t,blip(rr_.choice([1000,1300,1700,2100])),.12);t+=.14
add(fx,23.2,chime(),.08)
import os
NOTAG=os.environ.get('NOTAG')=='1'
if not NOTAG:
    add(fx,24.3,sweep(1200,200,.6,2),.12);add(fx,24.3,hp(noise(.6,3)),.12)                  # whoosh down
VO=[('this',1.35),('done',5.7),('answer',7.3),('hired',9.8),('andme',11.2),('charger',12.3),('fired',18.4)]
VO+=[('worse',19.87),('promo',20.67)] if E=='A' else [('still',19.87)]
if E=='B2':VO=[x for x in VO if x[0] not in('fired','still')]+[('news',18.4),('still',20.05)]
for n,t in VO:add(vo,t,load(n),.85)
w=int(.03*sr);e=np.clip(np.convolve(np.abs(vo),np.ones(w)/w,'same')*14,0,1)
out=m*(1-.72*e)+fx*(1-.25*e)+vo*1.3
out=np.tanh(out);out=out/np.abs(out).max()*.9
if NOTAG:fo=int(.35*sr);out[-fo:]*=np.linspace(1,0,fo)   # ends, doesn't loop: short fade
f=wave.open(f'mix_{E}{"_notag" if NOTAG else ""}.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
