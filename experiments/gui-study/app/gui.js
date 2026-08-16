#!/usr/bin/env node
// GUI driver: every command loads the real rendered page in a headless
// browser and interacts with it exactly like a human would (click, read
// text). It never calls the app's backend API directly.
const { chromium } = require('playwright');

const BASE_URL = process.env.GUI_APP_URL || 'http://127.0.0.1:8765';

async function withPage(fn) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  const result = await fn(page);
  await browser.close();
  return result;
}

async function readRows(page) {
  return page.$$eval('tr[data-row]', (trs) =>
    trs.map((tr) => {
      const cells = tr.querySelectorAll('td');
      return {
        sku: tr.getAttribute('data-row'),
        counted_qty: cells[1].textContent.trim(),
        expected_qty: cells[2].textContent.trim(),
        checked: !!tr.querySelector('[data-testid^="checked-mark"]'),
        decision_cell: cells[4].textContent.trim(),
      };
    })
  );
}

async function submitState(page) {
  const submitted = await page.$('[data-testid="submitted-banner"]');
  const submitBtn = await page.$('[data-testid="submit-btn"]');
  const submitEnabled = submitBtn ? await submitBtn.evaluate((b) => !b.disabled) : false;
  return { submitted: !!submitted, submit_enabled: submitEnabled };
}

async function main() {
  const [, , cmd, ...args] = process.argv;

  if (cmd === 'snapshot') {
    let offset = 0, limit = 20, unchecked = false;
    for (let i = 0; i < args.length; i++) {
      if (args[i] === '--offset') offset = parseInt(args[++i], 10);
      if (args[i] === '--limit') limit = parseInt(args[++i], 10);
      if (args[i] === '--unchecked-only') unchecked = true;
    }
    const out = await withPage(async (page) => {
      let rows = await readRows(page);
      if (unchecked) rows = rows.filter((r) => !r.checked || r.decision_cell === '(check first)');
      const total = rows.length;
      rows = rows.slice(offset, offset + limit);
      const subState = await submitState(page);
      return { total_matching: total, offset, limit, rows, ...subState };
    });
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  if (cmd === 'check') {
    const sku = args[0];
    await withPage(async (page) => {
      await page.click(`[data-testid="check-${sku}"]`);
      await page.waitForLoadState('networkidle');
    });
    const out = await withPage(async (page) => {
      const rows = await readRows(page);
      return rows.find((r) => r.sku === sku);
    });
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  if (cmd === 'mark') {
    const sku = args[0];
    const decision = args[1]; // "confirmed" or "flagged"
    const testid = decision === 'confirmed' ? `confirm-${sku}` : `flag-${sku}`;
    await withPage(async (page) => {
      await page.click(`[data-testid="${testid}"]`);
      await page.waitForLoadState('networkidle');
    });
    const out = await withPage(async (page) => {
      const rows = await readRows(page);
      return rows.find((r) => r.sku === sku);
    });
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  if (cmd === 'submit') {
    const out = await withPage(async (page) => {
      const submitBtn = await page.$('[data-testid="submit-btn"]');
      const enabled = submitBtn ? await submitBtn.evaluate((b) => !b.disabled) : false;
      if (!enabled) {
        return { ok: false, detail: 'submit button is disabled: not every row is checked and decided yet' };
      }
      await page.click('[data-testid="submit-btn"]');
      await page.waitForLoadState('networkidle');
      const submitted = await page.$('[data-testid="submitted-banner"]');
      return { ok: !!submitted, detail: submitted ? 'submitted' : 'submit did not go through' };
    });
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  if (cmd === 'reconcile-batch') {
    // Runs your own already-decided sku -> "confirmed"|"flagged" mapping
    // (read from a JSON file you write yourself) through the real page in
    // one browser session, instead of relaunching a browser per action.
    // You must have already decided each value by comparing counted_qty
    // to expected_qty from a snapshot; this command only clicks, it does
    // not decide anything for you.
    const fs = require('fs');
    const decisionsPath = args[0];
    if (!decisionsPath) {
      console.error('Usage: node gui.js reconcile-batch <decisions.json>');
      process.exit(1);
    }
    const decisions = JSON.parse(fs.readFileSync(decisionsPath, 'utf8'));
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    const log = [];
    let i = 0;
    for (const [sku, decision] of Object.entries(decisions)) {
      i++;
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
        page.click(`[data-testid="check-${sku}"]`),
      ]);
      const testid = decision === 'confirmed' ? `confirm-${sku}` : `flag-${sku}`;
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
        page.click(`[data-testid="${testid}"]`),
      ]);
      log.push({ sku, decision });
      if (i % 20 === 0) console.log(`... ${i}/${Object.keys(decisions).length} rows done`);
    }
    const submitBtn = await page.$('[data-testid="submit-btn"]');
    const enabled = submitBtn ? await submitBtn.evaluate((b) => !b.disabled) : false;
    let submitResult = { ok: false, detail: 'not attempted' };
    if (enabled) {
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
        page.click('[data-testid="submit-btn"]'),
      ]);
      const submitted = await page.$('[data-testid="submitted-banner"]');
      submitResult = { ok: !!submitted, detail: submitted ? 'submitted' : 'submit did not go through' };
    } else {
      submitResult = { ok: false, detail: 'submit button disabled: not every row is checked and decided yet' };
    }
    await browser.close();
    console.log(JSON.stringify({ rows_processed: log.length, submit: submitResult }, null, 2));
    return;
  }

  if (cmd === 'screenshot') {
    const path = args[0] || 'screenshot.png';
    await withPage(async (page) => {
      await page.screenshot({ path, fullPage: true });
    });
    console.log(JSON.stringify({ saved: path }));
    return;
  }

  console.error('Usage: node gui.js <snapshot|check|mark|submit|screenshot> [args]');
  process.exit(1);
}

main().catch((e) => {
  console.error(JSON.stringify({ error: String(e) }));
  process.exit(1);
});
