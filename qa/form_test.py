# Walks the form like a visitor: error on empty step, answers persist through Back, inline email error, preview guard on submit.
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844})
        await pg.goto("http://127.0.0.1:8910/index.html?gclid=TEST123", wait_until="networkidle")
        ok = lambda c, m: print(("PASS " if c else "FAIL ") + m)
        await pg.click("#fnext"); ok(await pg.is_visible(".step:not([hidden]) .step-err"), "empty step shows an error")
        answers = ["New clinic", "I already have a location", "Dental", "1,500-3,000 sq. ft.", "3-6 months"]
        for a in answers:
            await pg.click(f".step:not([hidden]) label.opt:has-text('{a}')"); await pg.click("#fnext")
        ok((await pg.text_content("#fcount")).strip() == "Step 6 of 6", "reaches contact step")
        for _ in range(5): await pg.click("#fback")
        ok(await pg.is_checked("input[value='New clinic']"), "Back keeps step 1 answer")
        for _ in range(5): await pg.click("#fnext")
        ok(await pg.is_checked("input[value='3-6 months']"), "answers survive back and forth")
        await pg.fill("#em", "bad"); await pg.click("#ci")
        ok(await pg.is_visible("#em ~ .err"), "inline email error on blur")
        await pg.fill("#fn", "Test"); await pg.fill("#ln", "Lead"); await pg.fill("#ph", "604 555 1234"); await pg.fill("#em", "t@example.com"); await pg.fill("#ci", "Surrey")
        await pg.click("#fnext")
        ok("Preview only" in (await pg.text_content("#fmsg")), "submit blocked by preview guard, nothing sent")
        ok(await pg.eval_on_selector("input[name=gclid]", "e=>e.value") == "TEST123", "gclid captured into the form")
        await pg.goto("http://127.0.0.1:8910/index.html", wait_until="networkidle")
        await pg.evaluate("window.scrollTo(0, 5000)"); await pg.wait_for_timeout(400)
        ok(await pg.eval_on_selector("#stick", "e=>e.classList.contains('on')"), "sticky CTA shows after the form")
        await pg.click("#stick .btn"); await pg.wait_for_timeout(900)
        ok(await pg.eval_on_selector("#start", "e=>e.getBoundingClientRect().top < innerHeight && e.getBoundingClientRect().bottom > 0"), "sticky CTA scrolls to the form")
        await b.close()
asyncio.run(main())
