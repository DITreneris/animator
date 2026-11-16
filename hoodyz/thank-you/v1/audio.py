import numpy as np,wave,subprocess,sys
sr=44100;D=14.5;N=int(sr*D);m=np.zeros(N);fx=np.zeros(N);vo=np.zeros(N);rng=np.random.default_rng(3)
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
SEC=[(0,5.5,33,[0,3,7,12]),(6,7.5,36,[0,4,7,12]),(7.5,8,33,[0,3,7,12]),(8,10,33,[0,3,7,10]),(10,11.5,29,[0,3,7,10]),(13.5,14.5,33,[0,3,7,12])]
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
add(fx,.05,sweep(90,260,.5,3,'sine'),.16)  # ray charge
add(fx,2,noise(.1,30),.3)
add(fx,2,sweep(1400,500,.18,6),.12)
r=sweep(1400,90,.5);add(fx,5.5,r*np.linspace(.4,.9,len(r)),.18);n=noise(.5,0);add(fx,5.5,hp(n)*np.linspace(.3,.7,len(n)),.2)
for i,t in enumerate((6,6.5,7)):add(fx,t,sweep(700+i*150,1200+i*150,.12,8,'sine'),.28)
add(fx,8.5,sweep(300,900,.5,1,'sine'),.08)
add(fx,10,sweep(250,1600,.14,0,'sine'),.28);add(fx,10,noise(.08,50),.3)
for t in(11.5,11.75,12,12.25):add(fx,t,sq(95,.08,20),.3)
add(fx,12.87,sweep(260,1400,.12,0,'sine'),.28);add(fx,12.87,noise(.06,50),.25)
add(fx,13.5,sweep(90,300,.9,1,'sine'),.16)
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
for n,t in(('r1',.05),('r2',2.08),('r3',3.55),('g1',7.53),('r4',8.05),('g2',10.1),('t1',12.1),('g3',13.6)):
    x=load(f'vo/v_{n}.wav');add(vo,t,x/np.abs(x).max(),.85)
# duck music and fx by voice envelope
w=int(.03*sr);e=np.convolve(np.abs(vo),np.ones(w)/w,'same');e=np.clip(e*14,0,1)
a=np.exp(-1/(.012*sr));rl=np.exp(-1/(.2*sr));s=np.zeros(N);p=0
for i in range(N):
    p=max(e[i],p*rl) if e[i]>p else p*rl;s[i]=p
out=(m*(1-.72*s)+fx*(1-.35*s))*1.0+vo*1.25
out=np.tanh(out)/np.abs(np.tanh(out)).max()*.9
f=wave.open('mix.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
