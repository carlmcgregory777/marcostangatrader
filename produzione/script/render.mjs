import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { execSync } from 'child_process';
const [html,outdir,dur,mp4]=process.argv.slice(2); const FPS=30, N=Math.round(+dur*FPS);
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+html,{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready);
for(let i=0;i<N;i++){ await p.evaluate(t=>window.render(t),i/FPS); await p.screenshot({path:`${outdir}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92}); }
await b.close();
execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${outdir}/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart ${mp4}`);
