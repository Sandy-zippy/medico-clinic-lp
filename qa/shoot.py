# Screenshots per viewport-height frame after scrolling each into view; reports overflow, broken images, JS errors, section heights.
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8910/index.html"
OUT = pathlib.Path(__file__).parent / "shots"; OUT.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in [(1440, 900), (768, 1024), (390, 844)]:
            pg = await b.new_page(viewport={"width": w, "height": h})
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            await pg.goto(URL, wait_until="networkidle")
            H = await pg.evaluate("document.documentElement.scrollHeight")
            n = 0; y = 0
            while y < H and n < 25:
                await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(350)
                await pg.screenshot(path=str(OUT / f"w{w}_{n:02d}.png")); n += 1; y += h
            info = await pg.evaluate("""()=>({ovf: document.documentElement.scrollWidth - innerWidth,
              broken:[...document.images].filter(i=>i.complete && !i.naturalWidth).map(i=>i.src),
              secs:[...document.querySelectorAll('main > section, header, footer')].map(s=>[(s.className||s.tagName).split(' ').slice(-1)[0], Math.round(s.getBoundingClientRect().height)])})""")
            print(w, "height", H, "frames", n, "overflow", info["ovf"], "broken", info["broken"], "errors", errs); print("  ", info["secs"])
        await b.close()
asyncio.run(main())
