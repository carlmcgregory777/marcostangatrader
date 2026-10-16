// Storie del 16/10 per R6. Niente riquadri: spazio vuoto grande quanto lo sticker, con testo guida grigio che lo sticker copre.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const av = fs.readFileSync('/home/user/guidoio.social/produzione/brand/avatar-riferimento.jpg').toString('base64');
const css = `@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;900&display=swap');
*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;background:#0E0E0E;position:relative;overflow:hidden;font-family:Montserrat;color:#fff}
.logo{position:absolute;left:90px;top:205px;font-weight:900;font-size:46px}.logo i{font-style:normal;color:#FF6A13}
.av{position:absolute;right:90px;top:170px;width:300px;height:300px;border-radius:50%;border:12px solid #FF6A13;background:url(data:image/jpeg;base64,${av}) center 15%/cover}
.k{position:absolute;left:90px;font-weight:700;font-size:36px;letter-spacing:5px;color:#FF6A13}
h1{position:absolute;left:90px;right:60px;font-weight:900;font-size:92px;line-height:1.08;text-transform:uppercase}h1 em{font-style:normal;color:#FF6A13}
p{position:absolute;left:90px;right:90px;font-weight:500;font-size:44px;line-height:1.4;color:#D2D2D2}p b{color:#fff;font-weight:900}
.hint{position:absolute;left:90px;right:90px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:700;font-size:26px;line-height:1.35;color:#3d3d3d}`;
const S = {
 'storia1_sondaggio.jpg': `<div class=av></div><div class=k style="top:560px">DOMANDA VELOCE</div>
 <h1 style="top:630px">Ti è mai servito qualcuno <em>che guidasse</em> al posto tuo?</h1>
 <div class=hint style="top:1060px;height:330px">sticker SONDAGGIO<br>«Sì, mille volte» / «Mai pensato»</div>
 <p style="top:1420px">Stasera alle <b>19:30</b> ti dico le <b>5 volte</b> in cui serve davvero.</p>
 <div class=hint style="top:1590px;height:230px">sticker CONTO ALLA ROVESCIA<br>oggi 19:30</div>`,
 'storia2_quiz.jpg': `<div class=k style="top:420px">QUIZ · LA N°5 DEL REEL</div>
 <h1 style="top:490px">Dopo un esame <em>con sedazione</em> puoi tornare a casa guidando?</h1>
 <div class=hint style="top:920px;height:400px">sticker QUIZ<br>«Sì» / «No» (giusta: No)</div>
 <p style="top:1350px">Molti ospedali ti chiedono di venire <b>accompagnato</b>. Ti riporto a casa io, con la tua auto.</p>
 <div class=hint style="top:1600px;height:140px">sticker LINK<br>guidoio.netlify.app/link</div>`,
};
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
for (const [f, h] of Object.entries(S)) {
  await p.setContent(`<html><head><style>${css}</style></head><body><div class=logo>GUIDO IO<i>.</i></div>${h}</body></html>`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: f, type: 'jpeg', quality: 92 });
}
await b.close();
