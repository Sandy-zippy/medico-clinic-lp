// QA for the 20 Nov Meta angle + CTA changes. Endpoint mocked: nothing reaches the live Sheet.
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://127.0.0.1:8910/';
const SHOTS = process.argv[3] || '/tmp/claude-0/-home-user/1b550076-7689-5cc9-b825-1a0299e3b33e/scratchpad/shots';
const CASES = [
  ['lease_medical', '?v=medical&a=space', "Don't sign the lease until we've walked the unit.", 'Opening a medical clinic?', null, 7],
  ['m1_medical_motion', '?v=medical&a=oneroof', 'Design, permits and build. One team, one roof.', 'Opening a medical clinic?', null, 7],
  ['contractor_dental', '?v=dental&a=dentalclinic', 'Any contractor can build an office. We only build clinics.', 'Building out a dental office?', 'Dental', 6],
  ['m2_dental_motion', '?v=dental&a=everyop', 'Every op planned: plumbing, power and imaging.', 'Building out a dental office?', 'Dental', 6],
  ['firstanimal_vet', '?v=vet&a=firstvet', "Is this your contractor's first animal hospital? With Medico, it isn't.", 'Building a vet clinic?', 'Veterinary', 6],
  ['m3_vet_motion', '?v=vet&a=firstvet', "Is this your contractor's first animal hospital? With Medico, it isn't.", 'Building a vet clinic?', 'Veterinary', 6],
  ['ameya_vet_1', '?v=vet&a=vetrooms', 'Every room has its own rules. We know them.', 'For veterinarians', 'Veterinary', 6],
  ['ameya_vet_2', '?v=vet&a=fourvet', 'Four animal hospitals. One contractor.', 'For veterinarians', 'Veterinary', 6],
  ['ameya_vet_3', '?v=vet&a=vetkennels', "A vet clinic isn't an office with kennels added.", 'For veterinarians', 'Veterinary', 6],
  ['ameya_vet_4', '?v=vet&a=catcondo', "Yes, we've built a cat condo.", 'For veterinarians', 'Veterinary', 6],
  ['google_dental (unchanged)', '?v=dental&utm_source=google', 'Build your dental office with a team that specializes in healthcare.', 'Dental clinic design', 'Dental', 6],
  ['plain (unchanged)', '', 'Build your medical clinic with a team that specializes in healthcare.', 'Medical clinic design', null, 7],
];
(async () => {
  let bad = 0; const ok = (c, m) => { if (!c) bad++; console.log((c ? 'PASS ' : 'FAIL ') + m); };
  require('fs').mkdirSync(SHOTS, { recursive: true });
  const b = await chromium.launch();
  for (const [name, qs, h1, eb, ty, n] of CASES) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const pg = await ctx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(String(e)));
    await pg.route('https://script.google.com/**', r => r.fulfill({ status: 200, body: '{"success":true}', headers: { 'Access-Control-Allow-Origin': '*' } }));
    await pg.goto(BASE + 'index.html' + qs + (qs ? '&' : '?') + 'utm_source=facebook&utm_content=' + name + '&fbclid=QA', { waitUntil: 'networkidle' });
    const r = await pg.evaluate(() => ({
      h1: document.querySelector('[data-v="h1"]').textContent.trim(), eb: document.querySelector('[data-v="eyebrow"]').textContent.trim(),
      ty: (document.querySelector('input[name="clinic_type"]:checked') || {}).value || null, count: document.querySelector('#fcount').textContent.trim(),
      img: document.querySelector('[data-v="img"]').currentSrc.split('/').pop(), img_ok: document.querySelector('[data-v="img"]').naturalWidth > 0,
      title: document.querySelector('.f-title').textContent, url: location.search, land: (document.querySelector('input[name="landing_url"]') || {}).value || '',
      stick: document.querySelector('#stick .btn').textContent }));
    ok(r.h1 === h1, `${name}: h1 "${r.h1}"`);
    ok(r.eb.startsWith(eb), `${name}: eyebrow "${r.eb}"`);
    ok(ty === null || r.ty === ty, `${name}: clinic type ${r.ty}`);
    ok(r.count === `Step 1 of ${n}`, `${name}: ${r.count}`);
    ok(r.img_ok, `${name}: hero photo loads (${r.img})`);
    ok(/cta=[ab]/.test(r.land) && /utm_content=/.test(r.land), `${name}: landing_url carries cta + utm_content`);
    await pg.screenshot({ path: `${SHOTS}/${name.replace(/\W+/g, '_')}.png` });
    ok(!errs.length, `${name}: no JS errors ${errs.join('|')}`);
    await ctx.close();
  }
  // CTA a and b, and a full mocked submit on each
  for (const k of ['a', 'b']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const pg = await ctx.newPage(); let body = null;
    await pg.route('https://script.google.com/**', r => { body = JSON.parse(r.request().postData()); r.fulfill({ status: 200, body: '{"success":true}', headers: { 'Access-Control-Allow-Origin': '*' } }); });
    await pg.goto(BASE + `index.html?v=vet&a=firstvet&cta=${k}&utm_source=facebook&utm_content=qa_${k}&fbclid=QA${k}`, { waitUntil: 'networkidle' });
    const t = await pg.textContent('.f-title'); ok(k === 'a' ? /Book your no-cost/.test(t) : /Will this space work/.test(t), `CTA ${k}: form title "${t}"`);
    const tap = a => pg.click(`.step:not([hidden]) label.opt:has-text("${a}")`);
    for (const a of ['New clinic', 'I already have a location', '1,500-3,000 sq. ft.', '3-6 months', 'Metro Vancouver']) { await tap(a); await pg.waitForTimeout(450); }
    ok((await pg.textContent('#fcount')).trim() === 'Step 6 of 6', `CTA ${k}: reached contact step in 6`);
    const btn = (await pg.textContent('#fnext')).trim(); ok(k === 'a' ? btn === 'Book My Site Assessment' : btn === 'Check My Space', `CTA ${k}: submit "${btn}"`);
    await pg.fill('#nm', 'Qa Tester'); await pg.fill('#ph', '604-555-0199'); await pg.fill('#em', 'qa@example.com');
    await pg.click('label.opt:has-text("Clinic owner / practitioner")');
    await Promise.all([pg.waitForURL(/thank-you/, { timeout: 8000 }).catch(() => {}), pg.click('#fnext')]);
    ok(!!body && body.clinic_type === 'Veterinary' && /cta=/.test(body.landing_url) && body.utm_content === `qa_${k}`, `CTA ${k}: sent clinic_type=${body && body.clinic_type}, landing_url has cta, utm_content ok`);
    ok(/thank-you/.test(pg.url()), `CTA ${k}: lands on thank-you page`);
    await ctx.close();
  }
  await b.close(); console.log(bad ? `FAIL ${bad}` : 'ALL PASS'); process.exit(bad ? 1 : 0);
})();
