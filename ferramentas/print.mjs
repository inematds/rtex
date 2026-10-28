// print de página 540x960 @2x pelo Playwright (o chrome --screenshot com virtual-time-budget travou em páginas do GitHub, 28/10/2026)
// uso: node ferramentas/print.mjs <url> <saida.png>
import { chromium } from 'playwright';
const [, , url, saida] = process.argv;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, locale: 'en-US' });
await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
await p.waitForTimeout(3500);
await p.screenshot({ path: saida });
await b.close();
console.log('ok', saida);
