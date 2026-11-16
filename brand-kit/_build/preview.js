// Build preview.png contact sheet. Usage: node preview.js <kit> <web-shots-dir>
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const kit = path.resolve(process.argv[2]); const shots = path.resolve(process.argv[3]);
const svg = (n) => fs.readFileSync(path.join(kit, 'logo/svg', n), 'utf8').replace(/ width="[^"]+" height="[^"]+"/, '');
const img = (p) => 'data:image/png;base64,' + fs.readFileSync(p).toString('base64');
const CW = ['dark', 'light', 'on-red', 'mono-black', 'mono-white'];
const tileBg = { dark: '#0A0607', light: '#F7F3F0', 'on-red': '#FF4B2B', 'mono-black': '#F7F3F0', 'mono-white': '#4A3B3D' };
const cell = (kind, cw, h) => `<figure><div class="t" style="background:${tileBg[cw]};height:${h}px">${svg(`nova-${kind}-${cw}.svg`)}</div><figcaption>${kind} · ${cw}</figcaption></figure>`;
const row = (kind, h) => `<div class="row five">${CW.map((c) => cell(kind, c, h)).join('')}</div>`;
const small = (bg, cw) => `<div class="smalls" style="background:${bg}">${[['16', 16], ['24', 24], ['48', 32], ['48', 48]].map(([t, s]) => `<span style="width:${s}px;height:${s}px">${svg(`nova-mark-small-${t}-${cw}.svg`)}</span>`).join('')}<em>16/24/32/48</em></div>`;
const sw = [['Ink', '#0A0607'], ['Ignition', '#FF4B2B'], ['Ignition Deep', '#C42A0E'], ['Bone', '#F4EDE8'], ['Paper', '#F7F3F0'], ['Ember', '#FFB547'], ['Ember Deep', '#8A5300']];
const ico = kit + '/icons/';
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#EFE8E3;font-family:'JetBrains Mono',monospace;color:#0A0607;padding:40px;width:1600px;box-sizing:border-box}
h1{font:700 28px 'Space Grotesk',sans-serif;letter-spacing:.16em;margin:0 0 4px}h2{font:400 11px 'JetBrains Mono';letter-spacing:.2em;text-transform:uppercase;color:#C42A0E;margin:36px 0 12px}
p.s{margin:0;font-size:12px;color:#5E504C}
.row{display:grid;gap:12px}.five{grid-template-columns:repeat(5,1fr)}
figure{margin:0}.t{display:flex;align-items:center;justify-content:center;border:1px solid #C9BBB4;padding:0}.t svg{height:100%;width:100%}
figcaption{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#5E504C;margin-top:6px}
.smalls{display:flex;align-items:flex-end;gap:18px;padding:16px;border:1px solid #C9BBB4}.smalls span{display:block}.smalls svg{width:100%;height:100%;display:block}.smalls em{font-style:normal;font-size:10px;color:#8E7D79;margin-left:auto}
.icons{display:flex;gap:20px;align-items:flex-end;flex-wrap:wrap}.icons img{display:block;border:1px solid #C9BBB4}.ic{display:flex;flex-direction:column;gap:6px;font-size:10px;color:#5E504C}
.mask{position:relative}.mask::after{content:'';position:absolute;left:10%;top:10%;width:80%;height:80%;border-radius:50%;border:1px dashed #FFB547}
.sw{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}.sw div{height:70px;border:1px solid #C9BBB4}.sw span{font-size:10px;display:block;margin-top:6px}
.web{display:grid;grid-template-columns:1fr 1fr 195px 195px;gap:12px;align-items:start}.web img{width:100%;display:block;border:1px solid #C9BBB4}
</style></head><body>
<h1>NOVA</h1><p class="s">The Nova Agency · brand kit contact sheet · logo/svg masters (with built-in clear space)</p>
<h2>Horizontal</h2>${row('horizontal', 120)}
<h2>Stacked</h2>${row('stacked', 230)}
<h2>Mark</h2>${row('mark', 140)}
<h2>Wordmark</h2>${row('wordmark', 90)}
<h2>Small-size marks (actual pixels)</h2><div class="row five">${small('#0A0607', 'dark')}${small('#F7F3F0', 'light')}${small('#FF4B2B', 'on-red')}${small('#F7F3F0', 'mono-black')}${small('#4A3B3D', 'mono-white')}</div>
<h2>Icons &amp; social</h2><div class="icons">
<div class="ic"><img src="${img(kit + '/logo/png/../../_build/.ico/ico-16.png')}" style="width:16px;border:0">ico 16</div>
<div class="ic"><img src="${img(kit + '/_build/.ico/ico-32.png')}" style="border:0">ico 32</div>
<div class="ic"><img src="${img(kit + '/_build/.ico/ico-48.png')}" style="border:0">ico 48</div>
<div class="ic"><img src="${img(ico + 'apple-touch-icon.png')}">apple-touch 180</div>
<div class="ic"><img src="${img(ico + 'icon-192.png')}">icon-192</div>
<div class="ic"><div class="mask"><img src="${img(ico + 'icon-512-maskable.png')}" style="width:256px"></div>maskable (dashed = 80% safe-zone circle)</div>
<div class="ic"><img src="${img(kit + '/social/avatar-dark-400.png')}" style="width:200px;border-radius:50%">avatar-dark</div>
<div class="ic"><img src="${img(kit + '/social/avatar-light-400.png')}" style="width:200px;border-radius:50%">avatar-light</div>
</div>
<h2>Colour</h2><div class="sw">${sw.map(([n, h]) => `<figure><div style="background:${h}"></div><span>${n} ${h}</span></figure>`).join('')}</div>
<h2>Holding page · dark / light · 1440 and 390</h2><div class="web">
<img src="${img(shots + '/web-dark-1440.png')}"><img src="${img(shots + '/web-light-1440.png')}"><img src="${img(shots + '/web-dark-390.png')}"><img src="${img(shots + '/web-light-390.png')}"></div>
</body></html>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
  await p.setContent(html); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(kit, 'preview.png'), fullPage: true }); await b.close(); console.log('preview ok');
})();
