const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2], b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(out, 'deck.html')); await p.evaluate(() => document.fonts.ready);
  fs.mkdirSync(path.join(out, 'mockups'), { recursive: true });
  const names = { 18: 'letterhead', 19: 'business-cards', 20: 'id-card', 21: 'app-mobile', 22: 'website', 23: 'signage', 24: 'fleet-merch-social' };
  const s = await p.$$('.slide');
  for (const [n, nm] of Object.entries(names)) await s[n - 1].screenshot({ path: path.join(out, 'mockups', `${String(n).padStart(2, '0')}-${nm}.png`) });
  await b.close();
})();
