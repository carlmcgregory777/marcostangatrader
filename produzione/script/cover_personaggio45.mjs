import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
import B from './brand.mjs';
const [title,sub,num,img,out]=process.argv.slice(2);
const b64=fs.readFileSync(img).toString('base64');
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.setContent(`<html><head><style>@import url('https://fonts.googleapis.com/css2?${B.googleFonts}&display=swap');
*{margin:0}body{width:1080px;height:1350px;background:${B.bg};position:relative;overflow:hidden;font-family:${B.textFont};color:#fff}
.glow{position:absolute;width:1300px;height:1300px;border-radius:50%;background:radial-gradient(${B.primary}77,transparent 62%);left:-110px;top:350px}
.pic{position:absolute;left:0;right:0;bottom:0;height:860px;background:url(data:image/png;base64,${b64}) center top/cover no-repeat;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 22%)}
.tag{position:absolute;left:90px;top:95px;font-family:'${B.monoFont}';font-size:34px;color:${B.accent};letter-spacing:3px}
h1{position:absolute;left:90px;right:90px;top:150px;font-family:${B.titleFont};font-weight:${B.titleWeight||400};text-transform:uppercase;font-size:calc(118px*${B.titleScale||1});line-height:.98;text-shadow:0 8px 40px #000}
h1 em{font-style:normal;color:${B.accent}}
.num{position:absolute;right:90px;top:80px;font-family:${B.titleFont};font-size:60px;color:#fff;background:${B.primary};padding:2px 22px;border-radius:12px}
.sub{position:absolute;left:90px;right:90px;bottom:70px;font-size:42px;font-weight:700;text-shadow:0 4px 20px #000}
.sub span{background:${B.primary};padding:4px 14px;border-radius:10px}
</style></head><body><div class=glow></div><div class=pic></div><div class=tag>// ${B.tag}</div><div class=num>${num}</div><h1>${title}</h1><div class=sub><span>${sub}</span></div></body></html>`,{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready); await p.screenshot({path:out,type:'jpeg',quality:93}); await b.close();
