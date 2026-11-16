import numpy as np,wave,subprocess
sr=44100;D=24.0;N=int(sr*D);rng=np.random.default_rng(3)
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
def blip():return sq(1400,.06,20,.3)+sq(2100,.06,25,.3)*.6
# music: (start,end,root,arp,gain,soft)
SEC=[(0,2,33,[0,3,7,12],1,0),(2.5,7,38,[0,4,7,11],.6,1),(7,10.5,36,[0,4,7,12],.9,0),(10.5,14.5,33,[0,3,7,10],.9,0),(14.5,17.6,31,[0,3,7,10],.8,0),(20.1,24,38,[0,4,7,12],.9,0)]
for a,b,r,ar,g,soft in SEC:
    t=a;k=0
    while t<b-1e-6:
        if not soft and k%2==0:add(m,t,kick(),.9*g)
        if k%4==2:add(m,t,hp(noise(.14,24)),.22*g)
        add(m,t,hp(hp(noise(.04,120))),.06*g)
        add(m,t,sq(midi(r+(12 if k%8 in(3,6) else 0)),.23,6),.15*g)
        add(m,t,sq(midi(r+24+ar[k%4]),.2,10,.25),.07*g)
        t+=.25;k+=1
# hook
for i in range(8):add(fx,i*.25,kick(.7)*.8);add(fx,i*.25+.02,noise(.08,30),.18)
add(fx,0,noise(2,1)*.0,.0)
for i in range(4):add(fx,.4+i*.4,sweep(600,350,.08,20),.12)   # ball bounces
r=sweep(1400,90,.5,0,'sq');add(fx,2,r*np.linspace(.4,.9,len(r)),.16);n=noise(.5,0);add(fx,2,hp(n)*np.linspace(.3,.7,len(n)),.18)
yc=lambda t:(add(fx,t,kick(.6)),add(fx,t,noise(.05,60),.25))
for t in(2.5,7.0,10.5,17.57):yc(t)
# 2024
for t in(2.9,3.2,3.5,3.8):add(fx,t,sweep(500,700,.06,25),.12)    # pats
for t in(4.4,4.75,5.6):add(fx,t,lp(noise(.12,18),5),.35)            # munch
add(fx,4.33,blip(),.18);add(fx,5.17,click(),.7);add(fx,5.25,chime(),.12)
for t in(5.6,5.75,5.9,6.05,6.2):add(fx,t,sq(1600,.03,40,.3),.06)
# 2025
add(fx,7.4,blip(),.18);add(fx,8.33,click(),.5);add(fx,8.6,sweep(120,420,.35,4),.45);add(fx,8.6,kick(1.6));add(fx,8.65,sweep(500,1500,.3,3),.12)
for i in range(4):add(fx,9.5+i*.25,kick(.7)*.8)
# 2026
add(fx,10.5,blip(),.18);add(fx,11.2,click(),.7)
for i in range(11):add(fx,11.25+i*.067,sweep(300,900,.07,12),.12);add(fx,11.45+i*.067,kick(.4))
t=11.5;k=0
while t<14.5:
    if not 13.15<t<13.95:add(fx,t,click(),.6)
    t+=max(.09,.45-k*.03);k+=1
for t in(11.63,11.97,12.3):add(fx,t,sq(900,.08,15,.3),.12)
# late 2026
add(fx,14.5,blip(),.18);add(fx,15.75,click(),.7);add(fx,15.95,sweep(300,180,.25,6),.15)
t=16.1
while t<17.5:add(fx,t,click(),.5);t+=.1
add(fx,16.77,sq(300,.12,10,.5),.14);add(fx,16.95,sq(220,.16,8,.5),.14)
sq_=sweep(900,1300,.6,0)*np.sin(2*np.pi*7*T(.6))*.5;add(fx,17.3,sq_,.1);add(fx,17.3,lp(noise(.8,2),12),.4)
# 2027
for t in(18.3,18.6,18.9,19.2):add(fx,t,sweep(400,560,.07,25),.12)
add(fx,19.53,sweep(700,500,.18,6),.14)
add(fx,19.9,sweep(300,1600,.3,2),.22);add(fx,19.9,noise(.25,8),.15)
for i in range(9):add(fx,20.3+i*.11,lp(noise(.05,40),3),.4)
for i,n_ in enumerate((72,76,79,84)):add(fx,20.27+i*.12,sq(midi(n_),.2,8,.3),.07)
add(fx,21.33,lp(noise(.25,10),20),.6);add(fx,21.4,sweep(420,180,.5,4),.07)
for i in range(7):add(fx,21.95+i*.14,lp(noise(.04,40),3),.3)
for t in(22.95,23.2,23.45):add(fx,t,sweep(400,560,.07,25),.12)
add(fx,23.05,chime(),.1)
for n,t in(('wait',.2),('good',2.72),('read',13.2),('appr',14.1),('appr2',15.65),('rgood',18.2)):add(vo,t,load(n),.85)
w=int(.03*sr);e=np.clip(np.convolve(np.abs(vo),np.ones(w)/w,'same')*14,0,1)
out=m*(1-.72*e)+fx*(1-.2*e)+vo*1.3
rt=lp(noise(D,0),60)[:N];out+=rt*.01
out=np.tanh(out);out=out/np.abs(out).max()*.9
f=wave.open('mix.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
