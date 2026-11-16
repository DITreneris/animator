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
SEC=[(0,2,33,[0,3,7,12]),(2.5,3.5,36,[0,4,7,12]),(3.5,4.5,34,[0,4,7,11]),(4.5,5.5,31,[0,3,7,10]),(5.5,7,29,[0,3,7,10]),(9,10.5,33,[0,3,7,12])]
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
add(fx,.25,sweep(180,60,.6,3,'sine'),.2)  # army turns
r=sweep(1400,90,.5);add(fx,2,r*np.linspace(.4,.9,len(r)),.18);n=noise(.5,0);add(fx,2,hp(n)*np.linspace(.3,.7,len(n)),.2)
for t in(2.5,3.5,4.5,5.5):add(fx,t,sweep(300,1000,.09,8,'sine'),.2)
for t in(7,7.23,7.47):add(fx,t,sq(1400,.04,40),.1)
add(fx,7.67,kick(.8));add(fx,7.67,noise(.09,30),.3)  # clipboard down
rn=noise(2.5,0);rn=np.convolve(rn,np.ones(9)/9,'same');add(fx,8,rn*np.minimum(1,np.linspace(2,0,len(rn))),.55)
cr=noise(1.6,1.4);add(fx,9.5,np.convolve(cr,np.ones(30)/30,'same'),1.2)  # crowd swell
add(fx,10.5,noise(.5,4),.06)
add(fx,11,sweep(300,900,.12,8,'sine'),.2)  # paper
add(fx,11,noise(.08,50),.2)
add(fx,13.67,sweep(600,1000,.12,8,'sine'),.2)  # thumb
add(fx,14.7,sweep(120,260,.3,3,'sine'),.16)
rt=np.convolve(noise(3.0,0),np.ones(60)/60,'same');add(fx,10.8,rt*np.minimum(1,np.minimum(np.linspace(0,8,len(rt)),np.linspace(8,0,len(rt)))),.09)  # room tone
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
for n,t,g in(('head',.02,1),('pop',2.55,1),('pro',3.55,1),('less',4.55,1),('first',5.55,1),('tail',13.75,1)):
    x=load(f'vo/v_{n}.wav');add(vo,t,x/np.abs(x).max(),.85*g)
ch=load('vo/v_chant.wav');ch=ch/np.abs(ch).max()
for dt,g in((0,.42),(.018,.34),(.04,.3),(.07,.24)):add(vo,9.0+dt,ch,g)
# duck music and fx by voice envelope
w=int(.03*sr);e=np.convolve(np.abs(vo),np.ones(w)/w,'same');e=np.clip(e*14,0,1)
a=np.exp(-1/(.012*sr));rl=np.exp(-1/(.2*sr));s=np.zeros(N);p=0
for i in range(N):
    p=max(e[i],p*rl) if e[i]>p else p*rl;s[i]=p
out=(m*(1-.72*s)+fx*(1-.35*s))*1.0+vo*1.25
out=np.tanh(out)/np.abs(np.tanh(out)).max()*.9
f=wave.open('mix.wav','wb');f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes());f.close()
