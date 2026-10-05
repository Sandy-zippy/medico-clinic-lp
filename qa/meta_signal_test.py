# Meta's Lead event fires only for visitors Google did not bring (5 Oct audit: Meta could claim Google leads).
# Serve the folder first: python3 -m http.server 8910
import asyncio, json, re
from playwright.async_api import async_playwright
BASE, HOOK = "http://127.0.0.1:8910/", "https://hook.test/lead"

async def run(p, query):
    b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844})
    calls = []
    await pg.expose_function("__fbq", lambda a: calls.append(a))
    await pg.add_init_script("window.fbq=function(){window.__fbq(JSON.parse(JSON.stringify(Array.from(arguments))))}")
    await pg.route("**/connect.facebook.net/**", lambda r: r.abort())
    await pg.route("**/googletagmanager.com/**", lambda r: r.abort())
    async def patch(r):
        resp = await r.fetch(); await r.fulfill(response=resp, body=re.sub(r'const ENDPOINT = "[^"]*"', f'const ENDPOINT = "{HOOK}"', await resp.text()))
    await pg.route("**/app.js", patch)
    await pg.route(HOOK, lambda r: r.fulfill(status=200, body=json.dumps({"success": True})))
    await pg.goto(BASE + "index.html" + query, wait_until="load")
    for a in ["New clinic", "I already have a location", "Dental", "1,500-3,000 sq. ft.", "3-6 months", "Calgary area"]:
        await pg.click(f'.step:not([hidden]) label.opt:has-text("{a}")'); await pg.wait_for_timeout(450)
    await pg.fill("#nm", "Priya Sharma"); await pg.fill("#ph", "(403) 555-1234"); await pg.fill("#em", "p@example.com")
    await pg.click("label.opt:has-text('Clinic owner')"); await pg.click("#fnext"); await pg.wait_for_timeout(1500)
    await b.close()
    return [c for c in calls if c[:2] == ["track", "Lead"]]

async def main():
    async with async_playwright() as p:
        g = await run(p, "?gclid=TEST123&utm_source=google")
        m = await run(p, "?fbclid=TESTFB&utm_source=facebook")
        d = await run(p, "")
    ok = lambda c, msg: print(("PASS " if c else "FAIL ") + msg)
    ok(not g, "Google visitor: no Meta Lead")
    ok(len(m) == 1, "Meta visitor: one Meta Lead")
    ok(len(d) == 1, "direct visitor: one Meta Lead")
asyncio.run(main())
