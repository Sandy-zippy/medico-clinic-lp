# 22 Oct: explicit ?a= angle applies on top of a keyword variant ?v=; a Meta angle (utm_content) never does. Chromium + WebKit.
import asyncio, sys
from playwright.async_api import async_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8910/index.html"
D0 = "Your clinic design is $0 when Medico builds it."
CASES = [  # query, expected h1, expected eyebrow startswith, expected checked clinic type
  ("", None, None, None),
  ("?v=dental", "Build your dental office with a team that specializes in healthcare.", "Dental clinic design", "Dental"),
  ("?v=dental&a=design0&utm_source=google", D0, "Dental clinic design", "Dental"),
  ("?v=medical&a=design0", D0, "Clinic design + construction", None),
  ("?a=design0", D0, "Clinic design + construction", None),
  ("?v=physio", "Build your physiotherapy clinic with a team that specializes in healthcare.", "Physiotherapy clinic design", "Physiotherapy / Chiropractic"),
  ("?v=physio&a=design0", D0, "Physiotherapy clinic design", "Physiotherapy / Chiropractic"),
  ("?v=pharmacy&a=design0", D0, "Pharmacy design", "Pharmacy"),
  ("?v=vet", "Build your veterinary clinic with a team that specializes in healthcare.", "Veterinary clinic design", "Veterinary"),
  ("?v=dental&utm_content=6920259118079", "Build your dental office with a team that specializes in healthcare.", "Dental clinic design", "Dental"),
  ("?utm_content=6924515235479", "Opening a new clinic? Get the plan right before you build.", "Opening a new clinic?", None)]
async def main():
    bad = 0
    async with async_playwright() as p:
        for eng in (p.chromium, p.webkit):
            b = await eng.launch(); pg = await b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            base_h1 = None
            for qs, h1, eb, ty in CASES:
                await pg.goto(BASE + qs, wait_until="networkidle")
                r = await pg.evaluate("""()=>({h1:document.querySelector('[data-v="h1"]').textContent.trim(),
                  eb:document.querySelector('[data-v="eyebrow"]').textContent.trim(),
                  ty:(document.querySelector('input[name="clinic_type"]:checked')||{}).value||null})""")
                if qs == "": base_h1 = r["h1"]; ok = True
                else: ok = r["h1"] == h1 and r["eb"].startswith(eb) and (ty is None or r["ty"] == ty)
                bad += not ok; print(eng.name, "OK " if ok else "BAD", qs or "(none)", r)
            print(eng.name, "js errors", errs); bad += bool(errs); await b.close()
    print("PASS" if not bad else f"FAIL {bad}"); sys.exit(bool(bad))
asyncio.run(main())
