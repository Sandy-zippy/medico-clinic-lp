# The thank-you page fires Meta's Lead once, with the landing page's event_id, and never for a Google click (6 Oct audit:
# the redirect cancelled the landing-page pixel on about half the leads). Serve first: python3 -m http.server 8910
import asyncio, json, re
from playwright.async_api import async_playwright
BASE, HOOK = "http://127.0.0.1:8910/", "https://hook.test/lead"

async def run(p, query, reload=False):
    b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844}); calls = []
    await pg.expose_function("__fbq", lambda a: calls.append((pg.url.split("/")[-1].split("?")[0], a)))
    await pg.add_init_script("window.fbq=function(){window.__fbq(JSON.parse(JSON.stringify(Array.from(arguments))))};window.fbq.loaded=1")
    for pat in ("**/connect.facebook.net/**", "**/googletagmanager.com/**", "**/clarity.ms/**"): await pg.route(pat, lambda r: r.abort())
    async def patch(r):
        resp = await r.fetch(); await r.fulfill(response=resp, body=re.sub(r'const ENDPOINT = "[^"]*"', f'const ENDPOINT = "{HOOK}"', await resp.text()))
    await pg.route("**/app.js", patch)
    await pg.route(HOOK, lambda r: r.fulfill(status=200, body=json.dumps({"success": True})))
    await pg.goto(BASE + "index.html" + query, wait_until="load")
    for a in ["New clinic", "I already have a location", "Dental", "1,500-3,000 sq. ft.", "3-6 months", "Calgary area"]:
        await pg.click(f'.step:not([hidden]) label.opt:has-text("{a}")'); await pg.wait_for_timeout(450)
    await pg.fill("#nm", "Priya Sharma"); await pg.fill("#ph", "(403) 555-1234"); await pg.fill("#em", "p@example.com")
    await pg.click("label.opt:has-text('Clinic owner')"); await pg.click("#fnext")
    await pg.wait_for_url("**/thank-you.html", timeout=8000); await pg.wait_for_timeout(800)
    if reload: await pg.reload(); await pg.wait_for_timeout(800)
    await b.close()
    return [(page, (c[3] or {}).get("eventID") if len(c) > 3 else None) for page, c in calls if c[:2] == ["track", "Lead"]]

async def main():
    async with async_playwright() as p:
        m = await run(p, "?fbclid=TESTFB&utm_source=facebook", reload=True)
        g = await run(p, "?gclid=TESTG&utm_source=google")
    ok = lambda c, msg: print(("PASS " if c else "FAIL ") + msg)
    ty = [e for page, e in m if page == "thank-you.html"]
    ok(len(ty) == 1, f"Meta visitor: one Lead on thank-you even after a refresh ({len(ty)})")
    ok(len({e for _, e in m}) == 1 and None not in {e for _, e in m}, "Meta visitor: every Lead carries the same event_id")
    ok(not g, "Google visitor: no Meta Lead anywhere")
asyncio.run(main())
