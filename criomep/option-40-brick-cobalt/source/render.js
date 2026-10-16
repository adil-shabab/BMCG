// node render.js <outdir> [--pdf] — screenshots each slide; optionally prints PDF and logo PNGs
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(out, 'deck.html'));
  await page.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.join(out, 'preview'), { recursive: true });
  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++)
    await slides[i].screenshot({ path: path.join(out, 'preview', `slide-${String(i + 1).padStart(2, '0')}.png`) });
  if (process.argv.includes('--pdf')) {
    await page.pdf({ path: path.join(out, 'presentation.pdf'), width: '1440px', height: '810px', printBackground: true, preferCSSPageSize: true });
    const lp = await browser.newPage({ deviceScaleFactor: 4 });
    for (const f of fs.readdirSync(path.join(out, 'logo')).filter(f => f.endsWith('.svg'))) {
      const svg = fs.readFileSync(path.join(out, 'logo', f), 'utf8');
      await lp.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
      const el = await lp.$('svg');
      await el.screenshot({ path: path.join(out, 'logo', f.replace('.svg', '.png')), omitBackground: true });
    }
  }
  await browser.close();
})();
