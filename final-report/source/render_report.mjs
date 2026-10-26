// node source/render_report.mjs [path-to-puppeteer-core-module] [review-output-directory]
// Install puppeteer-core outside the report repository. CHROME_PATH can override Chrome.
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
const { default: puppeteer } = await import(process.argv[2] || 'puppeteer-core');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const stem = '항공기_정비요청_Agent_최종결과보고서';
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
});
try {
  const page = await browser.newPage();
  await page.setViewport({width:1000,height:900,deviceScaleFactor:1});
  await page.goto(new URL(`file://${root}/${stem}.html`).href, {waitUntil:'networkidle0'});
  await page.evaluate(() => document.fonts.ready);
  const missing = await page.evaluate(() => [...document.images].filter(i=>!i.complete || !i.naturalWidth).map(i=>i.src));
  if (missing.length) throw new Error(`Unloaded images: ${missing.join(', ')}`);
  await page.pdf({
    path:path.join(root,`${stem}.pdf`), preferCSSPageSize:true, printBackground:true,
    displayHeaderFooter:true, headerTemplate:'<span></span>',
    footerTemplate:'<div style="font-size:8px;color:#64748b;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  if (process.argv[3]) {
    await fs.mkdir(process.argv[3],{recursive:true});
    for (const name of ['system-architecture','processing-flow','data-mcp-state','langgraph']) {
      await page.goto(new URL(`file://${root}/images/current/${name}.svg`).href);
      const svg=await page.$('svg');
      await svg.screenshot({path:path.join(process.argv[3],`${name}.png`)});
    }
  }
  console.log('PDF rendered; all image references loaded.');
} finally {
  await browser.close();
}
