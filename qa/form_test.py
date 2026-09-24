# Walks the form like a visitor on a phone. One-tap steps auto-advance; the contact step validates inline;
# the (not yet connected) submit lands on the thank-you page, which greets the visitor by name.
import asyncio
from playwright.async_api import async_playwright
BASE = "http://127.0.0.1:8910/"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844})
        ok = lambda c, m: print(("PASS " if c else "FAIL ") + m)
        count = lambda: pg.text_content("#fcount")
        tap = lambda a: pg.click(f'.step:not([hidden]) label.opt:has-text("{a}")')
        await pg.goto(BASE + "index.html?gclid=TEST123", wait_until="networkidle")
        ok(not await pg.is_visible("#fnext"), "no Continue button on one-tap steps")
        await tap("New clinic"); await pg.wait_for_timeout(500)
        ok((await count()).strip() == "Step 2 of 7", "tapping an answer auto-advances")
        ok(await pg.eval_on_selector_all("input[name=clinic_type]", "e=>e.length") == 11, "11 clinic types")
        ok(await pg.eval_on_selector_all("#ci, input[name=city]", "e=>e.length") == 0, "no City field (region covers it)")
        for a in ["I already have a location", "Optometry / Eye care", "1,500-3,000 sq. ft.", "3-6 months"]:
            await tap(a); await pg.wait_for_timeout(450)
        ok((await count()).strip() == "Step 6 of 7", "reaches region step by taps alone")
        await tap("Outside BC and Alberta"); await pg.wait_for_timeout(450)
        ok((await count()).strip() == "Step 6 of 7" and await pg.is_visible("#outside") and await pg.is_visible("#fnext"),
           "out-of-area pick stays put, shows the note and a Continue")
        await tap("Calgary area"); await pg.wait_for_timeout(450)
        ok((await count()).strip() == "Step 7 of 7", "in-area pick auto-advances")
        ok(await pg.evaluate("document.querySelectorAll('.step:not([hidden]) .field.bad').length") == 0, "contact step opens with NO red errors")
        await pg.click("#fback"); await pg.wait_for_timeout(200); await pg.click("#fback"); await pg.wait_for_timeout(200)
        ok(await pg.is_checked("input[value='3-6 months']"), "Back keeps the earlier answer")
        await tap("3-6 months"); await pg.wait_for_timeout(450); await tap("Calgary area"); await pg.wait_for_timeout(450)
        ok((await count()).strip() == "Step 7 of 7", "re-tapping the kept answer moves forward again")
        await pg.fill("#em", "bad"); await pg.click("#nm")
        ok(await pg.is_visible("#em ~ .err"), "inline email error on blur")
        await pg.fill("#nm", "Priya Sharma"); await pg.fill("#ph", "123 456 7890"); await pg.fill("#em", "p@example.com")
        await pg.click("#fnext")
        ok(await pg.is_visible("#ph ~ .err"), "junk phone 123-456-7890 rejected")
        ok(await pg.is_visible(".role .err"), "role required")
        ok(await pg.get_attribute("#lead", "data-grade") is None, "nothing submitted while invalid")
        await pg.fill("#ph", "403 555 1234"); await pg.click("label.opt:has-text('Clinic owner')")
        await pg.click("#fnext"); await pg.wait_for_url("**/thank-you.html", timeout=5000)
        ok(pg.url.endswith("thank-you.html"), "submit lands on the thank-you page")
        await pg.wait_for_timeout(600)
        ok("Thanks, Priya." in (await pg.text_content("#tyh")), "thank-you greets the visitor by first name")
        ok(await pg.is_visible("#preview"), "thank-you says nothing was sent (preview)")
        ok("Optometry / Eye care" in (await pg.text_content("#mine")) and "Calgary area" in (await pg.text_content("#mine")), "thank-you echoes their project")
        ok(await pg.eval_on_selector("#types > :first-child", "e=>e.dataset.type") == "optometry", "their clinic type is first and marked")
        # grade C path
        await pg.goto(BASE + "index.html", wait_until="networkidle")
        for a in ["Renovation", "I haven't started looking yet", "Dental", "I don't know yet", "Not sure yet"]:
            await tap(a); await pg.wait_for_timeout(450)
        await tap("Outside BC and Alberta"); await pg.click("#fnext"); await pg.wait_for_timeout(300)
        await pg.fill("#nm", "T L"); await pg.fill("#ph", "416 555 1234"); await pg.fill("#em", "t@example.com")
        await pg.click("label.opt:has-text('Practice manager')")
        grade = await pg.evaluate("""() => new Promise(r => { const f=document.getElementById('lead');
          new MutationObserver(()=>r(f.dataset.grade)).observe(f,{attributes:true}); document.getElementById('fnext').click(); })""")
        ok(grade == "C", "outside BC/AB grades C (still allowed to send)")
        await pg.wait_for_url("**/thank-you.html", timeout=5000)
        # sticky CTA
        await pg.goto(BASE + "index.html", wait_until="networkidle")
        await pg.evaluate("window.scrollTo(0, 5000)"); await pg.wait_for_timeout(400)
        ok(await pg.eval_on_selector("#stick", "e=>e.classList.contains('on')"), "sticky CTA shows after the form")
        await b.close()
asyncio.run(main())
