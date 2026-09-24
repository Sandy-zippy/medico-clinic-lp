# Walks the form like a visitor: error on empty step, answers persist through Back, inline email error, preview guard on submit.
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844})
        await pg.goto("http://127.0.0.1:8910/index.html?gclid=TEST123", wait_until="networkidle")
        ok = lambda c, m: print(("PASS " if c else "FAIL ") + m)
        await pg.click("#fnext"); ok(await pg.is_visible(".step:not([hidden]) .step-err"), "empty step shows an error")
        answers = ["New clinic", "I already have a location", "Optometry / Eye care", "1,500-3,000 sq. ft.", "3-6 months", "Calgary area"]
        for a in answers:
            await pg.click(f".step:not([hidden]) label.opt:has-text(\"{a}\")"); await pg.click("#fnext")
        ok((await pg.text_content("#fcount")).strip() == "Step 7 of 7", "reaches contact step (7 steps)")
        ok(await pg.evaluate("document.querySelectorAll('.step:not([hidden]) .field.bad').length") == 0, "contact step opens with NO red errors")
        for _ in range(6): await pg.click("#fback")
        ok(await pg.is_checked("input[value='New clinic']"), "Back keeps step 1 answer")
        for _ in range(6): await pg.click("#fnext")
        ok(await pg.is_checked("input[value='Calgary area']"), "answers survive back and forth")
        await pg.fill("#em", "bad"); await pg.click("#ci")
        ok(await pg.is_visible("#em ~ .err"), "inline email error on blur")
        await pg.fill("#fn", "Test"); await pg.fill("#ln", "Lead"); await pg.fill("#ph", "123 456 7890"); await pg.fill("#em", "t@example.com"); await pg.fill("#ci", "Calgary")
        await pg.click("#fnext")
        ok(await pg.is_visible("#ph ~ .err"), "junk phone 123-456-7890 rejected")
        ok(await pg.is_visible(".role .err"), "role required on contact step")
        await pg.fill("#ph", "403 555 1234"); await pg.click("label.opt:has-text('Clinic owner')")
        await pg.click("#fnext")
        ok("Preview only" in (await pg.text_content("#fmsg")), "submit blocked by preview guard, nothing sent")
        ok(await pg.get_attribute("#lead", "data-grade") == "A", "in-area owner with a space opening in 3-6 months grades A")
        ok(await pg.eval_on_selector("input[name=gclid]", "e=>e.value") == "TEST123", "gclid captured into the form")
        # C grade + outside note
        await pg.goto("http://127.0.0.1:8910/index.html", wait_until="networkidle")
        for a in ["Renovation", "I haven't started looking yet", "Dental", "I don't know yet", "Not sure yet", "Outside BC and Alberta"]:
            await pg.click(f".step:not([hidden]) label.opt:has-text(\"{a}\")")
            if a.startswith("Outside"): ok(await pg.is_visible("#outside"), "outside-area note appears")
            await pg.click("#fnext")
        await pg.fill("#fn", "T"); await pg.fill("#ln", "L"); await pg.fill("#ph", "416 555 1234"); await pg.fill("#em", "t@example.com"); await pg.fill("#ci", "Toronto")
        await pg.click("label.opt:has-text('Practice manager')"); await pg.click("#fnext")
        ok(await pg.get_attribute("#lead", "data-grade") == "C", "outside BC/AB grades C (still allowed to send)")
        await pg.goto("http://127.0.0.1:8910/index.html", wait_until="networkidle")
        await pg.evaluate("window.scrollTo(0, 5000)"); await pg.wait_for_timeout(400)
        ok(await pg.eval_on_selector("#stick", "e=>e.classList.contains('on')"), "sticky CTA shows after the form")
        await pg.click("#stick .btn"); await pg.wait_for_timeout(900)
        ok(await pg.eval_on_selector("#start", "e=>e.getBoundingClientRect().top < innerHeight && e.getBoundingClientRect().bottom > 0"), "sticky CTA scrolls to the form")
        await b.close()
asyncio.run(main())
