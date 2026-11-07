const cv=document.getElementById('c'),c=cv.getContext('2d'),W=1080,H=1920,INK='#16131c';
let S=11;const rnd=()=>{S|=0;S=S+0x6D2B79F5|0;let t=Math.imul(S^S>>>15,1|S);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296},rr=(a,b)=>a+(b-a)*rnd();
function smooth(p,closed){const o=[],n=p.length,g=i=>closed?p[(i+n)%n]:p[Math.max(0,Math.min(n-1,i))],end=closed?n:n-1;for(let i=0;i<end;i++){const a=g(i-1),b=g(i),d=g(i+1),e=g(i+2),seg=Math.max(4,Math.hypot(d[0]-b[0],d[1]-b[1])/10|0);for(let k=0;k<seg;k++){const t=k/seg,t2=t*t,t3=t2*t,f=j=>.5*(2*b[j]+(d[j]-a[j])*t+(2*a[j]-5*b[j]+4*d[j]-e[j])*t2+(3*b[j]-a[j]-3*d[j]+e[j])*t3);o.push([f(0),f(1)])}}if(!closed)o.push(p[n-1]);return o}
function wob(q,a){const ph=rr(0,9),ph2=rr(0,9);return q.map(([x,y],i)=>[x+a*Math.sin(i*.17+ph)+a*.4*Math.sin(i*.53+ph2),y+a*Math.cos(i*.14+ph2)+a*.4*Math.sin(i*.47+ph)])}
function ink(q,w=9,col=INK){const n=q.length;const ph=rr(0,9);for(let i=0;i<n-1;i++){const k=w*(.72+.34*Math.sin(i*.09+ph))*Math.min(1,(i+1)/5*.7+.3)*Math.min(1,(n-i)/5*.7+.3);c.beginPath();c.lineWidth=k;c.lineCap='round';c.strokeStyle=col;c.moveTo(q[i][0],q[i][1]);c.lineTo(q[i+1][0],q[i+1][1]);c.stroke()}}
function shape(p,{fill=null,closed=true,w=9,off=[5,4],col=INK,wa=2.4,two=true}={}){const q=smooth(p,closed);if(fill){c.beginPath();wob(q,1.5).forEach(([x,y],i)=>i?c.lineTo(x+off[0],y+off[1]):c.moveTo(x+off[0],y+off[1]));c.closePath();c.fillStyle=fill;c.fill()}if(closed)q.push(q[0],q[1]);if(w){ink(wob(q,wa),w,col);if(two)ink(wob(q,wa*1.4),w*.42,col)}}
const oval=(x,y,a,b,n=14)=>[...Array(n)].map((_,i)=>{const t=i/n*6.283;return[x+a*Math.cos(t),y+b*Math.sin(t)]});
const line=(p,w=9,col=INK)=>shape(p,{closed:false,w,col,two:false});
// fixed paper and fixed hair path, so only the lines boil
const PAPER=document.createElement('canvas');PAPER.width=W;PAPER.height=H;(()=>{const g=PAPER.getContext('2d');g.fillStyle='#f5efdf';g.fillRect(0,0,W,H);for(let i=0;i<9000;i++){g.fillStyle=`rgba(90,70,40,${rr(.015,.06)})`;g.fillRect(rr(0,W),rr(0,H),rr(1,3),rr(1,3))}g.fillStyle='#b4663f';g.fillRect(0,1640,W,280);g.fillStyle='rgba(60,25,10,.28)';for(let i=0;i<50;i++)g.fillRect(rr(0,W),rr(1660,1910),rr(50,180),3)})();
const HAIR=[];(()=>{const cols=['#6d3fd0','#7f55e0','#5a31b2'];for(let i=0;i<58;i++){const a=rr(-3.5,.35),r=rr(50,230),cx=Math.cos(a)*r*.95,cy=Math.sin(a)*r*.8,pts=[];let x=cx,y=cy;for(let k=0;k<5;k++){pts.push([x,y]);x+=rr(-60,60);y+=rr(-60,48)}HAIR.push({pts,w:rr(11,22),col:cols[i%3]})}for(let i=0;i<16;i++){const a=rr(-3.4,.2),r=rr(150,250),cx=Math.cos(a)*r*.95,cy=Math.sin(a)*r*.8;HAIR.push({pts:[[cx,cy],[cx+rr(-40,40),cy+rr(-46,36)],[cx+rr(-62,62),cy+rr(-60,36)]],w:7,col:INK})}})();
const SKIN='#f4bd92',TEAL='#22b8ad';
function coder(o){const hx=540,hy=640;
 // body and neck
 shape([[260,1920],[330,1240],[430,1090],[650,1090],[760,1240],[820,1920]],{fill:TEAL,w:14});
 line([[470,1100],[454,1280]],8,'#fff8e6');line([[610,1100],[628,1280]],8,'#fff8e6');
 c.save();c.globalAlpha=.45;for(let i=0;i<9;i++){const y=1340+i*62;line([[340,y],[540,y+rr(-8,8)],[780,y]],6,'#148c84')}c.restore();
 shape([[474,1020],[468,1120],[614,1120],[606,1020]],{fill:SKIN,w:11});
 // head
 shape([[352,620],[432,450],[640,446],[744,610],[748,850],[666,1046],[430,1052],[346,860]],{fill:SKIN,w:15});
 // hair: rises with shock
 c.save();c.translate(548,440+(o.hairLift||0)*-1);c.scale(1+(o.hairS||0),1+(o.hairS||0)*1.4);for(const h of HAIR)ink(wob(smooth(h.pts,false),1.6),h.w*1.35,h.col);c.restore();
 // eyes
 const sz=[o.eyeL,o.eyeR],sp=Math.max(0,(o.eyeL-66)*.85),ex=[[446-sp,700],[644+sp,684]];
 ex.forEach(([x,y],i)=>{const r=sz[i]*(i?1.14:1);shape(oval(x,y,r,r*1.12,12),{fill:'#fffdf5',w:9,off:[1,1]});const pr=(o.pup||19)*(i?1.1:1);c.fillStyle=INK;c.beginPath();c.arc(x+o.px*r*.48,y+o.py*r*.42,pr,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.arc(x+o.px*r*.48-pr*.3,y+o.py*r*.42-pr*.34,pr*.3,0,7);c.fill()});
 // glasses, slipping and cracked
 const gr=o.gRot||0,gd=o.gDrop||0;c.save();c.translate(545,690+gd);c.rotate(gr);for(const[i,[x,y]]of ex.entries()){const r=sz[i]*(i?1.14:1)+24;shape(oval(x-545,y-690,r,r*1.1,12),{w:10,wa:1.3})}line([[-20-sp*.0,-6],[8,-10]],20,'#fff8e6');line([[-16,-18],[6,8]],5);
 if(o.crack){const[x,y]=[99+sp,-6];line([[x,y],[x+34,y-44],[x+22,y-68]],5);line([[x,y],[x-44,y+24],[x-68,y+52]],5);line([[x,y],[x+48,y+28]],5)}c.restore();
 // brows
 const by=o.brow||0;line([[376,600-by],[446,582-by],[516,598-by]],22);line([[566,590-by],[648,566-by],[728,586-by]],22);
 // mouth
 const mx=545,my=880;
 if(o.mouth==='grin'){shape([[388,842],[470,866],[620,862],[706,830],[688,958],[620,1012],[468,1014],[408,958]],{fill:'#6d1f35',w:13,off:[0,0]});shape([[394,848],[470,870],[620,866],[700,836],[690,884],[620,906],[470,908],[404,890]],{fill:'#fffdf5',w:8,off:[0,0],two:false});for(const x of[466,516,566,616])line([[x,872],[x+4,906]],5);shape(oval(548,982,56,20,9),{fill:'#ef6d86',w:6,off:[0,0],two:false})}
 if(o.mouth==='frozen'){shape([[396,860],[470,876],[620,872],[698,850],[680,916],[620,944],[468,944],[414,916]],{fill:'#fffdf5',w:11,off:[0,0]});for(const x of[456,510,566,622])line([[x,878],[x,942]],5);line([[396,904],[698,902]],5)}
 if(o.mouth==='flat'){line([[452,900],[548,906],[644,894]],15)}
 if(o.mouth==='jaw'){const a=o.jaw,w=118,t=862,b=t+a;
  // long throat, tongue, lower jaw
  shape([[mx-w,t],[mx-w,t],[mx+w,t],[mx+w,t],[mx+w-4,b],[mx+w-4,b],[mx-w+4,b],[mx-w+4,b]],{fill:'#5a1730',w:14,off:[0,0]});
  shape([[mx-w+10,t+4],[mx-w+10,t+4],[mx+w-10,t+4],[mx+w-10,t+4],[mx+w-14,t+34],[mx+w-14,t+34],[mx-w+14,t+34],[mx-w+14,t+34]],{fill:'#fffdf5',w:7,off:[0,0],two:false});
  if(a>90)shape([[mx-62,t+Math.max(60,a*.12)],[mx+62,t+Math.max(60,a*.12)],[mx+72,b-40],[mx,b-14],[mx-72,b-40]],{fill:'#ef6d86',w:9,off:[0,0]});
  if(a>200)line([[mx,t+90],[mx+6,b-70]],6,'#b83b58');
  shape([[mx-w-18,b-6],[mx-w-18,b-6],[mx+w+18,b-6],[mx+w+18,b-6],[mx+w+6,b+60],[mx,b+78],[mx-w-6,b+60]],{fill:SKIN,w:13,off:[0,0]});
  shape([[mx-w+6,b-24],[mx-w+6,b-24],[mx+w-6,b-24],[mx+w-6,b-24],[mx+w-6,b],[mx+w-6,b],[mx-w+6,b],[mx-w+6,b]],{fill:'#fffdf5',w:6,off:[0,0],two:false})}
 // sweat
 if(o.sweat){shape([[770,640],[752,700],[772,724],[792,700]],{fill:'#7ed4ff',w:6,off:[0,0],two:false})}
}
function laptop(p){shape([[780,1400],[780,1400],[970,1378],[970,1378],[988,1520],[988,1520],[798,1542],[798,1542]],{fill:'#b6bdca',w:11});shape([[768,1548],[768,1548],[1012,1516],[1012,1516],[1016,1548],[1016,1548],[772,1582],[772,1582]],{fill:'#8a92a2',w:10});const f=p%2?12:0;shape([[790,1402],[778,1320-f],[820,1356],[838,1262+f],[880,1340],[924,1284-f],[944,1362],[966,1380]],{fill:'#ff8a1f',w:9});shape([[828,1396],[824,1356],[860,1378],[880,1324+f],[914,1390]],{fill:'#ffe066',w:0})}
function hands(p){ // cutaway: what he sees
 c.fillStyle='rgba(120,70,30,.14)';const f=p%2?6:0;
 shape([[-40,1190],[150,1090],[320,1000],[370,1100],[220,1210],[-40,1330]],{fill:'#e7ecf3',w:13});
 shape(oval(390,1000,88,76,10),{fill:'#d99a6c',w:12});
 shape([[300,860],[338,780],[458,780],[498,860],[534,988],[470,1090],[320,1090],[258,988]],{fill:'#d9b06e',w:13});shape([[338,780],[360,716],[446,716],[458,780]],{fill:'#c49a5c',w:10});
 c.save();c.translate(394,944);c.rotate(-.05);c.font='170px Marker';c.textAlign='center';c.textBaseline='middle';c.fillStyle=INK;c.fillText('$',0,0);c.restore();
 shape([[1120,1460],[900,1400],[770,1320],[720,1400],[860,1520],[1120,1600]],{fill:'#ff7a3d',w:13});
 shape(oval(700,1310,84,72,10),{fill:'#f7c7a6',w:12});
 shape(oval(680,1190,86,86,14),{fill:'#ffc914',w:13});c.save();c.translate(680,1192);c.font='92px Marker';c.textAlign='center';c.textBaseline='middle';c.fillStyle=INK;c.fillText('$',0,0);c.restore();
 for(const[a,b,d,e]of[[240,700,190,640],[540,700,590,630],[620,1070,590,1020],[790,1080,830,1020],[860,1190,930,1190]])line([[a,b],[d,e]],10);
}
function cap(s,x,y,sz,col){c.font=sz+'px Marker';c.textAlign='center';c.textBaseline='middle';c.lineJoin='round';c.lineWidth=26;c.strokeStyle=INK;c.strokeText(s,x,y);c.fillStyle=col;c.fillText(s,x,y)}
window.frame=p=>{S=1000+(p>>1)*97;c.setTransform(1,0,0,1,0,0);
 let sx=0,sy=0;const quake=(f,a)=>{if(p>=f&&p<f+5){const k=a*(1-(p-f)/5);sx+=k*(p%2?1:-1);sy+=k*(p%2?-.7:.8)}};quake(28,10);quake(31,16);quake(34,46);
 c.translate(sx,sy);c.drawImage(PAPER,-60,-60,W+120,H+120);
 if(p>=8&&p<14){hands(p);return}
 const bob=p<8?(p%4<2?0:-14):0;const o={eyeL:66,eyeR:66,px:0,py:0,pup:21,mouth:'grin',brow:0,sweat:false};
 if(p>=14){o.mouth='frozen';o.px=1;o.py=.1}
 if(p>=18){o.eyeL=92;o.eyeR=92;o.pup=18;o.brow=38}
 if(p>=21){o.eyeL=118;o.eyeR=124;o.pup=13;o.brow=72;o.hairS=.1;o.crack=1;o.gRot=.04}
 if(p>=24){o.mouth='flat';o.sweat=true}
 if(p>=28){o.mouth='jaw';o.jaw=110;o.gRot=.07;o.gDrop=10}
 if(p>=31)o.jaw=310,o.hairS=.16,o.gRot=.11,o.gDrop=22;
 if(p>=34){o.jaw=584;o.gRot=.17;o.gDrop=36;o.brow=92;o.hairS=.16;o.eyeL=128;o.eyeR=136;o.pup=11}
 if(p===34)o.jaw=606;if(p===35)o.jaw=572;
 // talking: jaw only trembles, eyes stay on the cash
 if(p>=38&&p<60)o.jaw=584+(p%3==0?-12:p%3==1?7:0);
 c.save();c.translate(0,bob+165);coder(o);c.restore();laptop(p);
 if(p>=34&&p<40)for(const[a,b,d,e]of[[300,1650,190,1600],[340,1700,180,1720],[760,1650,880,1596],[730,1710,900,1726]])line([[a,b],[d,e]],11);
 c.font='88px Marker';const L1='WAIT, YOU GUYS',L2='ARE GETTING PAID?',l1=c.measureText(L1).width,a1=c.measureText('WAIT, ').width,l2=c.measureText(L2).width,a2=c.measureText('ARE GETTING ').width,x1=540-l1/2,x2=540-l2/2;
 const part=(t,x,y,col)=>{c.font='88px Marker';c.textAlign='left';c.textBaseline='middle';c.lineJoin='round';c.lineWidth=24;c.strokeStyle=INK;c.strokeText(t,x,y);c.fillStyle=col;c.fillText(t,x,y)};
 if(p>=38)part('WAIT,',x1,226,'#fff');if(p>=46)part('YOU GUYS',x1+a1,226,'#fff');if(p>=52)part('ARE GETTING',x2,336,'#fff');if(p>=57)part('PAID?',x2+a2,336,'#ffc914');
};
window.shot=p=>{frame(p);return cv.toDataURL('image/jpeg',.95)};
