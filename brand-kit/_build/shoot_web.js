// Screenshot web/index.html in dark + light at 1440 and 390 wide. Usage: node shoot_web.js <kit> <outdir>
const { chromium } = require('playwright');
const path = require('path');
const kit = path.resolve(process.argv[2]); const out = path.resolve(process.argv[3]);
(async () => {
  const b = await chromium.launch();
  for (const scheme of ['dark', 'light']) for (const w of [1440, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: w > 500 ? 900 : 844 }, deviceScaleFactor: 1, colorScheme: scheme, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    await p.route('**/api/lead', (r) => r.fulfill({ status: 200, body: '{}' }));
    await p.goto('http://127.0.0.1:8765/web/index.html');
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(500);
    await p.screenshot({ path: path.join(out, `web-${scheme}-${w}.png`), fullPage: true });
    const sw = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
    console.log(scheme, w, 'scrollWidth/innerWidth', sw);
    if (scheme === 'dark' && w === 1440) {
      // exercise the form + toggle
      await p.fill('#email', 'test@example.com'); await p.click('button[type=submit]');
      await p.waitForTimeout(200); console.log('status:', await p.textContent('#form-status'));
      await p.click('#theme-toggle'); console.log('theme after toggle', await p.evaluate(() => [document.documentElement.dataset.theme, localStorage.getItem('nova-theme')]));
      await p.focus('#email'); await p.keyboard.press('Tab');
      await p.screenshot({ path: path.join(out, 'web-toggled-focus.png') });
    }
    await ctx.close();
  }
  await b.close();
})();
