import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
import B from './brand.mjs';
const [spec,out]=process.argv.slice(2); const S=JSON.parse(fs.readFileSync(spec,'utf8'));
const css=`@import url('https://fonts.googleapis.com/css2?${B.googleFonts}&display=swap');
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;background:${B.bg};color:#f4f3f7;font-family:'${B.textFont}',sans-serif;position:relative;overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:54px 54px}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(${B.primary}55,transparent 65%);right:-300px;top:-300px}
.wrap{position:absolute;inset:120px 88px 150px;display:flex;flex-direction:column;justify-content:center}
.tag{font-family:'${B.monoFont}';font-size:30px;color:${B.accent};letter-spacing:2px}
h1{font-family:'${B.titleFont}';font-weight:${B.titleWeight||400};text-transform:uppercase;font-size:calc(118px*${B.titleScale||1});line-height:1.0;margin-top:36px;letter-spacing:1px}h1 em,h2 em{font-style:normal;color:${B.accent}}
h2{font-family:'${B.titleFont}';font-weight:${B.titleWeight||400};text-transform:uppercase;font-size:calc(92px*${B.titleScale||1});line-height:1.02;margin-top:24px;letter-spacing:1px}
p{font-size:44px;line-height:1.32;margin-top:44px;color:#b3b0bd}p b{color:#ffffff}
.num{font-family:'${B.titleFont}';font-size:240px;color:${B.accent};line-height:1;opacity:.9}
.foot{position:absolute;left:88px;right:88px;bottom:70px;display:flex;justify-content:space-between;font-family:'${B.monoFont}';font-size:26px;color:#7d7a88}
.adv{position:absolute;top:40px;right:88px;font-family:'${B.monoFont}';font-size:24px;color:#7d7a88;border:2px solid #2c2838;padding:6px 14px;border-radius:8px}
.cta{margin-top:56px;display:inline-block;background:${B.primary};color:#ffffff;font-size:52px;font-weight:700;padding:22px 38px;border-radius:16px;align-self:flex-start}
.term{margin-top:56px;border:2px solid #2c2838;border-radius:18px;background:#13111b;padding:30px 36px;font-family:'${B.monoFont}';font-size:32px;line-height:1.9;color:#b3b0bd}.term .ok{color:${B.accent}}.term .ko{color:${B.alert}}.risk{font-size:30px;color:#8d8a98;margin-top:36px}`;
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const [i,s] of S.entries()){
 await p.setContent(`<html><head><style>${css}</style></head><body><div class=grid></div><div class=glow></div>${s.adv?'<div class=adv>ADV</div>':''}<div class=wrap>${s.html}</div><div class=foot><span><b style="font-family:${B.titleFont};font-size:34px;color:#fff;letter-spacing:2px">${B.mark}</b>&nbsp;&nbsp;@${B.handle}</span><span>${i+1}/${S.length}</span></div></body></html>`,{waitUntil:'networkidle'});
 await p.screenshot({path:`${out}/${String(i+1).padStart(2,'0')}.png`});
}
await b.close();
