# Proves motion never strands content: every animated element ends at opacity 1 once its section is shown,
# and with reduced motion nothing is hidden at all. Also saves mid-animation frames to eyeball the 3D.
import asyncio, pathlib
from playwright.async_api import async_playwright
URL = "http://127.0.0.1:8910/index.html"; OUT = pathlib.Path(__file__).parent / "shots"
HIDDEN = """() => { const bad=[]; document.querySelectorAll('main *, .stack *').forEach(e=>{ const r=e.getBoundingClientRect();
  if(!r.width||!r.height) return; if(e.closest('[hidden]')||e.closest('.sr')) return;
  const o=+getComputedStyle(e).opacity; if(o<0.99) bad.push((e.className?.baseVal??e.className)+'|'+e.tagName+'|'+o.toFixed(2)); }); return bad.slice(0,15); }"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in [(1440, 900), (390, 844)]:
            pg = await b.new_page(viewport={"width": w, "height": h}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL, wait_until="networkidle")
            await pg.wait_for_timeout(2600)
            await pg.add_style_tag(content="html{scroll-behavior:auto!important}")  # smooth scroll made the probe outrun itself
            for sel in ["[data-anim]", "[data-count]"]:
                for el in await pg.query_selector_all(sel):
                    await el.evaluate("e=>e.scrollIntoView({block:'center'})"); await pg.wait_for_timeout(250)
            await pg.wait_for_timeout(3500)
            bad = await pg.evaluate(HIDDEN)
            cnt = await pg.eval_on_selector("[data-count]", "e=>e.textContent")
            anim = await pg.evaluate("document.documentElement.className")
            print(w, "html:", anim, "| stranded:", bad or "none", "| counter:", cnt, "| errors:", errs or "none")
        ctx = await b.new_context(reduced_motion="reduce", viewport={"width": 1440, "height": 900}); pg = await ctx.new_page()
        await pg.goto(URL, wait_until="networkidle"); await pg.wait_for_timeout(300)
        print("reduced-motion html:", repr(await pg.evaluate("document.documentElement.className")), "| hidden:", await pg.evaluate(HIDDEN) or "none")
        # mid-animation frames
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto(URL, wait_until="domcontentloaded"); await pg.wait_for_timeout(700); await pg.screenshot(path=str(OUT/"mid_hero.png"))
        await pg.goto(URL, wait_until="networkidle")
        for name, sel, t in [("plan", "[data-anim=iso]", 500), ("map", "[data-anim=map]", 450), ("sheet", "[data-anim=sheet]", 450), ("pf", ".pf", 350), ("stages", "[data-anim=stages]", 1100)]:
            await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(200)
            await pg.eval_on_selector(sel, "e=>e.scrollIntoView({block:'center'})"); await pg.wait_for_timeout(t)
            await pg.screenshot(path=str(OUT/f"mid_{name}.png"))
        await b.close()
asyncio.run(main())
