# 14 Oct: the thank-you page re-sends the Google Ads conversion with the form page's transaction_id (backstop for hits
# the redirect cut off), once per tab, never for junk. Serve first: python3 -m http.server 8910
import asyncio, json, re
from playwright.async_api import async_playwright
BASE, HOOK = "http://127.0.0.1:8910/", "https://hook.test/lead"
CONV = "() => (window.dataLayer||[]).filter(a => a[0]==='event' && a[1]==='conversion').map(a => a[2].transaction_id)"

async def run(p, junk=False):
    b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844})
    for pat in ("**/connect.facebook.net/**", "**/googletagmanager.com/**", "**/clarity.ms/**"): await pg.route(pat, lambda r: r.abort())
    async def patch(r):
        resp = await r.fetch(); await r.fulfill(response=resp, body=re.sub(r'const ENDPOINT = "[^"]*"', f'const ENDPOINT = "{HOOK}"', await resp.text()))
    await pg.route("**/app.js", patch)
    await pg.route(HOOK, lambda r: r.fulfill(status=200, body=json.dumps({"success": True, "junk": junk})))
    await pg.goto(BASE + "index.html?gclid=TESTG&utm_source=google", wait_until="load")
    for a in ["New clinic", "I already have a location", "Dental", "1,500-3,000 sq. ft.", "3-6 months", "Calgary area"]:
        await pg.click(f'.step:not([hidden]) label.opt:has-text("{a}")'); await pg.wait_for_timeout(450)
    await pg.fill("#nm", "Priya Sharma"); await pg.fill("#ph", "(403) 555-1234"); await pg.fill("#em", "p@example.com")
    await pg.click("label.opt:has-text('Clinic owner')"); await pg.click("#fnext")
    await pg.wait_for_url("**/thank-you.html", timeout=8000); await pg.wait_for_timeout(500)
    first = await pg.evaluate(CONV)
    await pg.reload(); await pg.wait_for_timeout(500)
    second = await pg.evaluate(CONV)
    await b.close(); return first, second

async def main():
    async with async_playwright() as p:
        f, s = await run(p); jf, js = await run(p, junk=True)
    ok = lambda c, msg: print(("PASS " if c else "FAIL ") + msg)
    ok(len(f) == 1 and f[0], f"lead: thank-you re-sends the conversion with a transaction_id ({f})")
    ok(s == [], f"lead: a refresh does not send it again ({s})")
    ok(jf == [] and js == [], "junk: no conversion on thank-you")
asyncio.run(main())
