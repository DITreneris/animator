import numpy as np,wave,subprocess
sr=44100;D=28.5;N=int(sr*D);rng=np.random.default_rng(3)
m=np.zeros(N);fx=np.zeros(N);vo=np.zeros(N)
def add(buf,t,x,g=1):
    i=int(t*sr);x=x[:max(0,N-i)];buf[i:i+len(x)]+=x*g
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
SEC=[(0,2.5,33,[0,3,7,12],1),(3,6,36,[0,4,7,12],.8),(6,10,41,[0,4,7,11],1),(10,11.8,36,[0,4,7,12],.8),(13,14.25,33,[0,3,7,10],1),(21.5,23.1,36,[0,4,7,12],.55),(25,28.5,29,[0,3,7,10],.75)]
for a,b,r,ar,g in SEC:
    t=a;k=0
    while t<b-1e-6:
        if k%2==0:add(m,t,kick(),.9*g)
        if k%4==2:add(m,t,hp(noise(.14,24)),.28*g)
        add(m,t,hp(hp(noise(.04,120))),.07*g)
        add(m,t,sq(midi(r+(12 if k%8 in(3,6) else 0)),.23,6),.17*g)
        add(m,t,sq(midi(r+24+ar[k%4]),.2,10,.25),.07*g)
        t+=.25;k+=1
def creak(d,f=95):
    t=T(d);return np.sin(2*np.pi*(f*t+8*np.sin(2*np.pi*3*t)))*np.exp(-t*1.2)
add(fx,0,kick(1.2));add(fx,0,creak(.9),.2)
for i in range(4):add(fx,.05+i*.17,hp(noise(.08,40)),.28)   # tiptoe drum
add(fx,.2,sweep(200,1500,.5,0),.1);n=noise(.5,0);add(fx,.2,hp(n)*np.linspace(.2,.8,len(n)),.16)   # crash zoom
add(fx,.8,kick(1.5));add(fx,.8,noise(.15,14),.35)   # smash cut
sl=lp(noise(.5,5),4);add(fx,1.33,sl,.5);add(fx,1.75,kick(1.2))   # slide stop
r=sweep(1400,90,.5,0,'sq');add(fx,2.5,r*np.linspace(.4,.9,len(r)),.18);n=noise(.5,0);add(fx,2.5,hp(n)*np.linspace(.3,.7,len(n)),.2)
add(fx,3.2,hp(noise(.4,3))*(np.sin(2*np.pi*40*T(.4))>0),.3)   # tape
add(fx,4.2,sweep(600,1200,.1,8,'sq'),.08)  # marker squeak / thumb
add(fx,4.9,sweep(700,1100,.14,6),.2)
for t in(7,8,8.83):add(fx,t,sweep(1200,1800,.14,5),.2);add(fx,t,kick(.7))
for t in(7.4,8.33,9.17):add(fx,t,noise(.08,30),.25)
for i,n_ in enumerate((72,76,79,84)):add(fx,10.05+i*.13,sq(midi(n_),.22,7,.3),.09)
add(fx,11.5,kick(.8));add(fx,11.83,creak(1.0,80),.34)
add(fx,14.28,sweep(900,700,.25,6),.13)
add(fx,15.4,kick(.6));add(fx,15.4,noise(.05,50),.2)
add(fx,15.92,hp(lp(noise(.1,20),6)),.7);add(fx,16.1,hp(lp(noise(.1,24),6)),.5)
p=hp(noise(.8,0))*np.linspace(.4,1,int(.8*sr));add(fx,17,p*(np.sin(2*np.pi*43*T(.8))>0),.34)
add(fx,18,creak(.5),.26)
add(fx,18.5,kick(1.8));add(fx,18.5,lp(noise(1.2,2.6),8),1.0);add(fx,18.5,sweep(120,35,.8,3),.7)
for dt in(.18,.36,.55):add(fx,18.5+dt,kick(1.1));add(fx,18.5+dt,noise(.1,25),.25)
add(fx,19.32,sweep(1300,1250,.5,7),.14)
add(fx,24,kick(1.4));add(fx,24,sweep(70,35,1.6,1),.7);n=noise(1,0);add(fx,24,hp(n)*np.linspace(.8,.05,len(n)),.2)  # pull-back
add(fx,25,kick(1.3))
add(fx,26.65,kick(1.0));add(fx,26.65,noise(.1,30),.3)  # giant trophy
add(fx,27.05,sweep(90,60,.18,8),.7);add(fx,27.22,sweep(80,55,.18,8),.6)  # giant cough
add(fx,27.5,sweep(500,900,.15,8),.14)
add(fx,21.07,sweep(200,1500,.12,0),.34);add(fx,21.07,kick(1.2));add(fx,21.07,noise(.08,40),.3)  # POP
for n,t in(('dont',.86),('now',3.4),('fri1',6.05),('garbage',13.05),('back',19.6),('fix',21.87),('fri2',23.22),('boss',25.05)):
    add(vo,t,load(n),.85)
w=int(.03*sr);e=np.clip(np.convolve(np.abs(vo),np.ones(w)/w,'same')*14,0,1)
out=m*(1-.72*e)+fx*(1-.25*e)+vo*1.25
out=np.tanh(out);out=out/np.abs(out).max()*.9
f=wave.open('mix.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
