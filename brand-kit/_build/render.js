// Render PNGs, icons and social avatars from the generated SVGs.
// Usage: node render.js <brand-kit dir>   (needs the playwright package + its chromium)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const KIT = path.resolve(process.argv[2] || path.join(__dirname, '..'));
const SVG = path.join(KIT, 'logo/svg');
const INK = '#0A0607', PAPER = '#F7F3F0';
const FRAME = 'M50 4 L96 50 L50 96 L4 50 Z';
const STAR = 'M50 22 C52.5 40 60 47.5 78 50 C60 52.5 52.5 60 50 78 C47.5 60 40 52.5 22 50 C40 47.5 47.5 40 50 22 Z';
const STAR16 = 'M50 20 C52.5 40 60 47.5 80 50 C60 52.5 52.5 60 50 80 C47.5 60 40 52.5 20 50 C40 47.5 47.5 40 50 20 Z';

const dataUri = (svg) => 'data:image/svg+xml;base64,' + Buffer.from(svg).toString('base64');
const viewBox = (svg) => svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);

// Mark tile: square of `size`, background `bg` (or transparent), mark box = frac * size.
function tile(size, frac, bg, frame, star, sw = 4.5, starD = STAR) {
  const m = 100 * frac, o = (100 - m) / 2, k = frac;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="${size}" height="${size}">` +
    (bg ? `<rect width="100" height="100" fill="${bg}"/>` : '') +
    `<g transform="translate(${o} ${o}) scale(${k})"><path d="${FRAME}" fill="none" stroke="${frame}" stroke-width="${sw}" stroke-linejoin="miter"/>` +
    `<path d="${starD}" fill="${star}"/></g></svg>`;
}

async function shot(page, svg, w, h, out) {
  // SVGs with a full-bleed background rect: paint the page that colour too, so edge pixels stay opaque.
  const bgm = svg.match(/^<svg[^>]*>(?:<title[^>]*>[^<]*<\/title>)?<rect width="[^"]+" height="[^"]+" fill="([^"]+)"/);
  const bg = bgm ? bgm[1] : 'transparent';
  // Rasterise at the output size (not the SVG's intrinsic size) to avoid resampling.
  svg = svg.replace(/^<svg([^>]*?) width="[^"]+" height="[^"]+"/, `<svg$1 width="${w}" height="${h}"`)
    .replace(/^<svg /, '<svg preserveAspectRatio="none" ');
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<!doctype html><html><body style="margin:0;background:${bg}">` +
    `<img id="i" src="${dataUri(svg)}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
  await page.waitForFunction(() => document.getElementById('i').complete);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await page.screenshot({ path: out, omitBackground: !bgm, clip: { x: 0, y: 0, width: w, height: h } });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });

  // 1. Logo PNGs: every lockup x colourway at 512 / 1024 / 2048 wide.
  for (const f of fs.readdirSync(SVG).filter((n) => /^nova-(horizontal|stacked|mark|wordmark)-[a-z-]+\.svg$/.test(n))) {
    const svg = fs.readFileSync(path.join(SVG, f), 'utf8');
    const [, , vw, vh] = viewBox(svg);
    for (const w of [512, 1024, 2048]) {
      const h = Math.round((w * vh) / vw);
      await shot(page, svg, w, h, path.join(KIT, 'logo/png', `${f.replace('.svg', '')}-${w}.png`));
    }
  }

  // 2. Icons.
  const I = path.join(KIT, 'icons');
  const IGN = '#FF4B2B';
  await shot(page, tile(180, 0.62, INK, IGN, IGN), 180, 180, path.join(I, 'apple-touch-icon.png'));
  await shot(page, tile(192, 0.62, INK, IGN, IGN), 192, 192, path.join(I, 'icon-192.png'));
  await shot(page, tile(512, 0.62, INK, IGN, IGN), 512, 512, path.join(I, 'icon-512.png'));
  await shot(page, tile(512, 0.60, INK, IGN, IGN), 512, 512, path.join(I, 'icon-512-maskable.png'));
  // ICO source frames (Ignition mark, transparent, size-tuned strokes) - combined by make_ico.py.
  const tmp = path.join(__dirname, '.ico');
  await shot(page, tile(16, 1, null, IGN, IGN, 12, STAR16), 16, 16, path.join(tmp, 'ico-16.png'));
  await shot(page, tile(32, 1, null, IGN, IGN, 7), 32, 32, path.join(tmp, 'ico-32.png'));
  await shot(page, tile(48, 1, null, IGN, IGN, 7), 48, 48, path.join(tmp, 'ico-48.png'));
  await shot(page, tile(32, 1, null, IGN, IGN, 7), 32, 32, path.join(I, 'favicon-32.png'));

  // 3. Social avatars: mark ~50% of width, centred.
  for (const s of [400, 1080]) {
    await shot(page, tile(s, 0.5, INK, IGN, IGN), s, s, path.join(KIT, 'social', `avatar-dark-${s}.png`));
    await shot(page, tile(s, 0.5, PAPER, INK, '#D92E10'), s, s, path.join(KIT, 'social', `avatar-light-${s}.png`));
  }
  fs.copyFileSync(path.join(KIT, 'social/avatar-dark-400.png'), path.join(KIT, 'social/avatar-dark.png'));
  fs.copyFileSync(path.join(KIT, 'social/avatar-light-400.png'), path.join(KIT, 'social/avatar-light.png'));

  // 4. Small tight light mark for the email signature (56px = 2x, displayed at 28px).
  await shot(page, tile(56, 1, null, INK, '#D92E10', 7), 56, 56, path.join(KIT, 'logo/png', 'nova-mark-small-light-56.png'));

  await browser.close();
  console.log('rendered');
})();
