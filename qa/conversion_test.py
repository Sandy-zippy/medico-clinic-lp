# Google Ads lead conversion: fires once after a successful send, with enhanced-conversion user data; never in preview
# mode (ENDPOINT set to TODO...) and never when the send fails. Serve the folder first: python3 -m http.server 8910
import asyncio, json, re
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8910/"
HOOK = "https://hook.test/lead"
SEND_TO = "AW-716871487/0XCcCLGxyIsdEL-u6tUC"

async def run(p, endpoint, status):
    b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844})
    pushed = []
    await pg.expose_function("__rec", lambda a: pushed.append(a))
    # Record every gtag() call; the real gtag.js is blocked so the 1.2 s fallback redirect is exercised too.
    await pg.add_init_script("window.dataLayer=[];window.dataLayer.push=function(a){try{window.__rec(JSON.parse(JSON.stringify(Array.from(a))))}catch(e){};return Array.prototype.push.call(this,a)}")
    await pg.route("**/googletagmanager.com/**", lambda r: r.abort())
    async def patch(r):  # swap the live Apps Script URL for a mock (or TODO = preview mode)
        resp = await r.fetch(); body = re.sub(r'const ENDPOINT = "[^"]*"', f'const ENDPOINT = "{endpoint or "TODO_OFF"}"', await resp.text())
        await r.fulfill(response=resp, body=body)
    await pg.route("**/app.js", patch)
    await pg.route("**/connect.facebook.net/**", lambda r: r.abort())
    async def hook(r):
        pushed.append(["post", json.loads(r.request.post_data or "{}")])
        await r.fulfill(status=status, body=json.dumps({"success": status == 200}), headers={"Access-Control-Allow-Origin": "*"})
    await pg.route(HOOK, hook)
    await pg.goto(BASE + "index.html?gclid=TEST123", wait_until="load")
    tap = lambda a: pg.click(f'.step:not([hidden]) label.opt:has-text("{a}")')
    for a in ["New clinic", "I already have a location", "Dental", "1,500-3,000 sq. ft.", "3-6 months", "Calgary area"]:
        await tap(a); await pg.wait_for_timeout(450)
    await pg.fill("#nm", "Priya Sharma"); await pg.fill("#ph", "(403) 555-1234"); await pg.fill("#em", " P@Example.com ")
    await pg.click("label.opt:has-text('Clinic owner')"); await pg.click("#fnext")
    try: await pg.wait_for_url("**/thank-you.html", timeout=4000); landed = True
    except Exception: landed = False
    await b.close()
    return pushed, landed

async def main():
    ok = lambda c, m: print(("PASS " if c else "FAIL ") + m) or c
    conv = lambda xs: [x for x in xs if x[:2] == ["event", "conversion"]]
    async with async_playwright() as p:
        pushed, landed = await run(p, HOOK, 200)
        c = conv(pushed); ud = [x for x in pushed if x[:2] == ["set", "user_data"]]
        r = [ok(len(c) == 1 and c[0][2]["send_to"] == SEND_TO and c[0][2].get("transaction_id"), "sent: exactly one conversion to the LP lead action"),
             ok(ud and ud[0][2] == {"email": "p@example.com", "phone_number": "+14035551234"}, "sent: enhanced-conversion email + E.164 phone"),
             ok(landed, "sent: lands on thank-you even with gtag.js blocked")]
        post = [x[1] for x in pushed if x[:1] == ["post"]][0]
        r.append(ok(post.get("event_id", "").startswith("lead_") and post.get("user_agent") and "fbp" in post,
                    "sent: Meta event_id + match keys go to the server for the CAPI Lead"))
        pushed, landed = await run(p, HOOK, 500)
        r.append(ok(not conv(pushed) and not landed, "send fails: no conversion, stays on the form"))
        pushed, landed = await run(p, None, 200)
        r.append(ok(not conv(pushed) and landed, "preview (ENDPOINT TODO): no conversion"))
    raise SystemExit(0 if all(r) else 1)

asyncio.run(main())
