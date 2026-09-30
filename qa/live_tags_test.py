# LIVE site check (never submits the form): the real Google tag and Meta pixel load, Google sets its click cookie
# from a gclid, and every ?v= variant renders its own H1. conversion_test.py blocks gtag.js on purpose, so a dead
# tag URL (AW-716871487 returned 404 on 30 Sep 2026) is only caught here. Usage: python3 qa/live_tags_test.py [base]
import asyncio, sys
from playwright.async_api import async_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "https://build.medicoconstruction.com/"
async def main():
    ok = lambda c, m: print(("PASS " if c else "FAIL ") + m) or c
    r = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        tags = {}
        pg.on("response", lambda res: tags.__setitem__(res.url.split("?")[0], res.status) if "googletagmanager.com/gtag/js" in res.url or "fbevents.js" in res.url else None)
        await pg.goto(BASE + "?gclid=TESTGCLID&utm_source=google", wait_until="networkidle"); await pg.wait_for_timeout(2500)
        r.append(ok(any("gtag/js" in u and s == 200 for u, s in tags.items()), f"Google tag loads 200 {tags}"))
        r.append(ok(any("fbevents" in u and s == 200 for u, s in tags.items()), "Meta pixel loads 200"))
        ck = {c["name"] for c in await pg.context.cookies()}
        r.append(ok("_gcl_aw" in ck, "Google set _gcl_aw from the gclid"))
        r.append(ok("_fbp" in ck, "Meta set _fbp"))
        for v, word in [("dental", "dental"), ("optometry", "optometry"), ("pharmacy", "pharmacy"), ("vet", "veterinary"), ("medical", "medical")]:
            await pg.goto(BASE + f"?v={v}", wait_until="domcontentloaded"); await pg.wait_for_timeout(600)
            r.append(ok(word in (await pg.text_content("h1")).lower(), f"?v={v} H1 says {word}"))
        await b.close()
    raise SystemExit(0 if all(r) else 1)
asyncio.run(main())
