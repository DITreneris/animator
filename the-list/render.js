// Renders The List with headless Chromium (Playwright).
//   node render.js still          -> The_List_Still.png
//   node render.js check 0 120 …  -> check/p000.jpg … (single poses, 12 per second)
//   node render.js video          -> v.mp4 (204 poses at 12 per second, output 30 fps)
const {chromium}=require('playwright'),{spawn}=require('child_process'),fs=require('fs'),path=require('path');
const here=p=>path.join(__dirname,p),POSES=204;
(async()=>{
 const b=await chromium.launch(),pg=await b.newPage({viewport:{width:1080,height:1920}});
 pg.on('pageerror',e=>{console.error(e.message);process.exit(1)});
 await pg.goto('file://'+here('page.html'));await pg.evaluate(()=>document.fonts.load('90px Marker'));
 await pg.addScriptTag({path:here('lib.js')});
 const [mode,...rest]=process.argv.slice(2),b64=d=>Buffer.from(d.split(',')[1],'base64');
 if(mode==='still'){await pg.addScriptTag({path:here('still.js')});fs.writeFileSync(here('The_List_Still.png'),b64(await pg.evaluate(()=>window.draw())))}
 else{
  await pg.addScriptTag({path:here('anim.js')});
  if(mode==='check'){fs.mkdirSync(here('check'),{recursive:true});for(const n of rest.map(Number))fs.writeFileSync(here(`check/p${String(n).padStart(3,'0')}.jpg`),b64(await pg.evaluate(n=>window.vframe(n),n)))}
  else if(mode==='video'){
   const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-c:v','mjpeg','-framerate','12','-i','-','-vf','fps=30,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-crf','17','-preset','medium','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',here('v.tmp.mp4')],{stdio:['pipe','inherit','inherit']});
   for(let n=0;n<POSES;n++){if(!ff.stdin.write(b64(await pg.evaluate(n=>window.vframe(n),n))))await new Promise(r=>ff.stdin.once('drain',r))}
   ff.stdin.end();const code=await new Promise(r=>ff.on('close',r));if(code!==0)process.exit(code);fs.renameSync(here('v.tmp.mp4'),here('v.mp4'))}
  else{console.error('usage: node render.js still | check N… | video');process.exit(2)}}
 await b.close()})();
