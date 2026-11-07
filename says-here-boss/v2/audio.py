import numpy as np,wave,subprocess,sys
sr=44100;D=15.0;N=int(sr*D);m=np.zeros(N);fx=np.zeros(N);vo=np.zeros(N);rng=np.random.default_rng(3)
def add(buf,t,x,g=1):
    idx=(int(t*sr)+np.arange(len(x)))%N;np.add.at(buf,idx,x*g)
T=lambda d:np.arange(int(d*sr))/sr
def kick(g=1):
    t=T(.22);return np.sin(2*np.pi*(48*t+(110/30)*(1-np.exp(-30*t))))*np.exp(-t*14)*g
def noise(d,dec):
    t=T(d);return rng.standard_normal(len(t))*np.exp(-t*dec)
hp=lambda x:np.diff(x,prepend=0)
def sq(fr,d,dec=4,duty=.5):
    t=T(d);return np.where((t*fr)%1<duty,1,-1)*np.exp(-t*dec)
midi=lambda n:440*2**((n-69)/12)
def sweep(a,b,d,dec=0,kind='sq'):
    t=T(d);fr=np.linspace(a,b,len(t));ph=np.cumsum(fr)/sr*2*np.pi
    return (np.sign(np.sin(ph)) if kind=='sq' else np.sin(ph))*np.exp(-t*dec)
SEC=[(0,3,33,[0,3,7,12]),(3.5,5,36,[0,4,7,12]),(5,6.5,41,[0,4,7,11]),(6.5,8.5,38,[0,3,7,10]),(8.5,11,33,[0,3,7,12]),(11,11.5,36,[0,4,7,12]),(11.5,13,33,[0,3,7,12]),(13.5,15,33,[0,3,7,12])]
for a,b,r,ar in SEC:
    t=a;k=0
    while t<b-1e-6:
        if k%2==0:add(m,t,kick(),.9)
        if k%4==2:add(m,t,hp(noise(.14,24)),.28)
        add(m,t,hp(hp(noise(.04,120))),.07)
        add(m,t,sq(midi(r+(12 if k%8 in(3,6) else 0)),.23,6),.17)
        add(m,t,sq(midi(r+24+ar[k%4]),.2,10,.25),.075)
        t+=.25;k+=1
add(fx,0,kick(1.1))
# shades slide on the hook
add(fx,.02,sweep(900,300,.35,3,'sine'),.09)
# rewind
r=sweep(1400,90,.5);add(fx,3,r*np.linspace(.4,.9,len(r)),.18);n=noise(.5,0);add(fx,3,hp(n)*np.linspace(.3,.7,len(n)),.2)
t=3.5;rr=np.random.default_rng(5)
while t<4.95:add(fx,t,hp(noise(.025,160)),.2);t+=rr.uniform(.04,.09)
for t in(3.73,4.23,4.53,4.83):add(fx,t,sweep(500,1000,.07,10),.14)
for t in(5.2,5.6,6.0):add(fx,t,sq(165,.18,6),.18);add(fx,t+.08,sq(120,.16,8),.18)
for k in range(4):add(fx,6.5+k*.5,hp(noise(.08,40)),.25)
add(fx,7.25,sweep(500,2400,.18,0,'sine'),.24);add(fx,7.43,sweep(2400,380,.32,3,'sine'),.26)
add(fx,8.5,noise(.3,10),.14)
add(fx,9,kick(1.7));add(fx,9,noise(.35,16),.45);add(fx,9,sweep(120,40,.5,5,'sine'),.65)
for i,n_ in enumerate((62,61,60,59)):
    d=.25 if i<3 else .55;t=T(d);v=1+.02*np.sin(2*np.pi*6*t)
    add(fx,9.5+i*.25,np.sign(np.sin(2*np.pi*midi(n_)*v*t))*np.minimum(1,(d-t)*12),.1)
add(fx,12.6,sweep(1800,3200,.3,5,'sine'),.09)   # sparkle
add(fx,13,hp(noise(.3,9))*1,.45);add(fx,13,sweep(1200,150,.22,4),.14)  # record scratch
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
TT='vo/'
for n,t,g in(('r1',.05,1.0),('g1',2.52,1.0),('g2b',10.97,1.0),('r2b',11.55,1.0),('r3',13.55,1.0)):
    x=load(TT+f'v_{n}.wav');add(vo,t,x/np.abs(x).max(),.85*g)
# duck music and fx by voice envelope
w=int(.03*sr);e=np.convolve(np.abs(vo),np.ones(w)/w,'same');e=np.clip(e*14,0,1)
a=np.exp(-1/(.012*sr));rl=np.exp(-1/(.2*sr));s=np.zeros(N);p=0
for i in range(N):
    p=max(e[i],p*rl) if e[i]>p else p*rl;s[i]=p
out=(m*(1-.72*s)+fx*(1-.35*s))*1.0+vo*1.25
out=np.tanh(out)/np.abs(np.tanh(out)).max()*.9
f=wave.open('mix.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
