# Screenshots each changed section at rest (after its entrance finishes), plus the last form step on a phone.
import asyncio, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / "shots"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h, items in [(1440, 900, [("exp", ".exp"), ("pf", ".pf"), ("trust", ".trust")]), (390, 844, [("map", ".map"), ("pf", ".pf"), ("exp", ".exp")])]:
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto("http://127.0.0.1:8910/index.html", wait_until="networkidle")
            await pg.add_style_tag(content="html{scroll-behavior:auto!important}")
            for n, s in items:
                await pg.eval_on_selector(s, "e=>e.scrollIntoView({block:'start'})"); await pg.wait_for_timeout(2500)
                await pg.screenshot(path=str(OUT / f"sec_{n}{w}.png"))
        pg = await b.new_page(viewport={"width": 390, "height": 844})
        await pg.goto("http://127.0.0.1:8910/index.html", wait_until="networkidle")
        for a in ["New clinic", "I already have a location", "Dental", "1,500-3,000 sq. ft.", "3-6 months", "Calgary area"]:
            await pg.click(f'.step:not([hidden]) label.opt:has-text("{a}")', timeout=5000); await pg.wait_for_timeout(450)
        await pg.eval_on_selector("#fnext", "e=>e.scrollIntoView({block:'end'})"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(OUT / "sec_laststep390.png"))
        await b.close()
asyncio.run(main())
