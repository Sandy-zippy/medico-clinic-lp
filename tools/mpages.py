#!/usr/bin/env python3
"""Build the Meta category landing pages: m/<cat>/index.html (27 Nov 2026).

Why: Clarity (24-27 Nov) showed Meta visitors on phones see the top 13% of the main page and leave after ~16 s.
The main page was built for Google searchers (form first). These pages are built for cold social traffic:
real photo of a finished clinic of that type first, then proof, then the room-by-room work, then the form.
Every photo is a real Medico project from the portfolio. The form, tracking and lead pipe are app.js, unchanged.

Run: python3 tools/mpages.py  (writes m/medical, m/dental, m/vet, m/optometry)
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

def img(key, alt, cls="", eager=False, sizes="(max-width:700px) 100vw, 50vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/m/{key}-1280.webp" srcset="/assets/m/{key}-720.webp 720w, /assets/m/{key}-1280.webp 1280w" '
            f'sizes="{sizes}" alt="{E(alt)}" {load}>')

# Shared copy. Claims only from the live page / site: 100+ clinics, 5.0 Google, BBB A+, licensed & insured,
# fixed supplier pricing, site assessment (never "free"), CSA Z8000 where it fits. No em dashes, no prices.
CHECKS = [
    ("plumb", "Plumbing", "Where water and drains can go, and what that means for your room layout."),
    ("power", "Electrical", "Whether the unit has the power your equipment needs, or needs an upgrade."),
    ("air", "Ventilation", "What the existing system can handle for the rooms you're planning."),
    ("door", "Barrier-free access", "Entry, washrooms and corridors that need to meet accessibility rules."),
    ("rooms", "Room count", "How many rooms the space really fits once circulation is planned."),
    ("permit", "Permits", "What the city is likely to ask for, so your opening date is realistic."),
]

CATS = {
"vet": dict(
    type="Veterinary", noun="animal hospital", nouns="vet clinics",
    title="Veterinary Clinic Design + Construction in BC | Medico",
    eyebrow="For veterinarians | British Columbia",
    h1="Your animal hospital won't be our first.",
    offer="<b>Treatment, surgery, imaging, wards and exam rooms</b>, designed and built by Medico. Start with a site assessment of your space. No obligation.",
    hero=("v-hero", "Treatment area at Woodland Veterinary Clinic, Vancouver, built by Medico", "<b>Woodland Veterinary Clinic</b> · Vancouver, BC · 2,200 sq ft"),
    count="6", countlab="animal hospitals built",
    rooms_h="Every room in a vet hospital has its own rules.",
    rooms_p="These are rooms we designed and built. Each one needs its own plumbing, power, layout and finishes, planned before construction starts.",
    rooms=[
        ("v-treat", "Treatment", "Wet tables, sinks, power and storage where your team actually works.", "Paws on Fraser Veterinary Hospital"),
        ("v-surg", "Surgery", "Procedure lighting, equipment space and a room that's easy to keep clean.", "Paws on Fraser Veterinary Hospital"),
        ("v-xray", "Imaging", "X-ray rooms planned early, with imaging requirements accounted for in the layout.", "Paws on Fraser Veterinary Hospital"),
        ("v-ward", "Wards and runs", "Kennel banks and runs laid out for daily cleaning and staff access.", "Coquitlam Animal Hospital"),
        ("v-exam", "Exam rooms", "Wall-mounted tables, storage and workstations sized to the room.", "Coquitlam Animal Hospital"),
        ("v-cat", "Custom millwork", "Including cat condos. Yes, we've built those too.", "EPIC Veterinary Hospital"),
    ],
    projects=[
        ("p-woodland", "Woodland Veterinary Clinic", "Vancouver, BC", "2,200 sq ft"),
        ("p-coquitlam", "Coquitlam Animal Hospital", "Coquitlam, BC", "3,229 sq ft"),
        ("p-paws", "Paws on Fraser Veterinary Hospital", "Vancouver, BC", "1,178 sq ft"),
        ("p-epic", "EPIC Veterinary Hospital", "Richmond, BC", "3,300 sq ft"),
        ("p-marine", "Marine Drive Vet Clinic", "Vancouver, BC", "1,400 sq ft"),
        ("p-vanvet", "Vancouver Veterinary", "Vancouver, BC", "1,500 sq ft"),
    ],
    proj_h="Animal hospitals we've built across BC.",
    quotes=[("They genuinely cared about our project and spent time and attention to ensure we had a beautiful, well-made clinic.", "Dr. C.Y.", "Clinic owner", "")],
    faq=[
        ("How much does it cost to build a vet clinic?", "It depends on the space, its existing plumbing and power, how many exam, treatment and ward areas you need, imaging, and finishes. A site assessment is the fastest way to get a real number for your space, not a guess."),
        ("How big should a vet clinic be?", "Big enough for your exam rooms, treatment, surgery, wards, imaging and staff areas, with room for how your team moves between them. We lay it out around your workflow from the first plan."),
        ("Should I talk to Medico before signing a lease?", "Yes. Drains, power and ventilation decide where treatment, surgery and wards can go. We can flag problems before you commit to a space."),
        ("Can you renovate a clinic that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),

"dental": dict(
    type="Dental", noun="dental office", nouns="dental clinics",
    title="Dental Office Design + Construction in BC | Medico",
    eyebrow="For dentists | British Columbia",
    h1="Any contractor can build an office. We build dental clinics.",
    offer="<b>Water, air and vacuum at every chair, power for the equipment, room for imaging.</b> Start with a site assessment of your space. No obligation.",
    hero=("d-hero", "Reception at Smile Plus Dentistry, Surrey, designed and built by Medico", "<b>Smile Plus Dentistry</b> · Surrey, BC · 2,840 sq ft"),
    count="100+", countlab="healthcare spaces built",
    rooms_h="A dental office is built around the operatory.",
    rooms_p="These are rooms we designed and built. The services behind the walls are planned before the first wall goes up.",
    rooms=[
        ("d-op", "Operatories", "Chair, delivery unit and cabinetry placed around how you and your assistant work.", "Chilliwack Dental"),
        ("d-op2", "Services to every chair", "Water, air, vacuum and power routed to each op and planned with your equipment.", "Smile Plus Dentistry"),
        ("d-steri", "Sterilization", "A clean-to-dirty workflow with sinks, counters and equipment space.", "Chilliwack Dental"),
        ("d-hall", "Patient flow", "Corridors and op entries that keep patients and staff moving.", "Chilliwack Dental"),
        ("d-desk", "Front desk", "Check-in, check-out and records, with sightlines to the waiting room.", "Chilliwack Dental"),
        ("d-staff", "Staff room", "Storage and a break room your team will actually use.", "Chilliwack Dental"),
    ],
    projects=[
        ("p-smile", "Smile Plus Dentistry", "Surrey, BC", "2,840 sq ft"),
        ("p-chill", "Chilliwack Dental", "Chilliwack, BC", "2,500 sq ft"),
        ("p-babylon", "Babylon by TELUS Health", "Victoria, BC", "Medical clinic"),
        ("p-axis", "Axis Primary Care", "Surrey, BC", "Medical clinic"),
    ],
    proj_h="Dental clinics, and the healthcare spaces around them.",
    quotes=[("They genuinely cared about our project and spent time and attention to ensure we had a beautiful, well-made clinic.", "Dr. C.Y.", "Clinic owner", "")],
    faq=[
        ("How much does it cost to build a dental office?", "It depends on the space, the number of operatories, your equipment, imaging, the mechanical room and finishes. A site assessment is the fastest way to get a real number for your space, not a guess."),
        ("When should I pick my equipment?", "Early. Chairs, compressors, vacuum and imaging decide where plumbing and power go. We plan the rooms around the equipment you choose."),
        ("Should I talk to Medico before signing a lease?", "Yes. Floor drains, slab work, power and ventilation can change your layout and cost. We can flag problems before you commit to a space."),
        ("Can you renovate a practice that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),

"optometry": dict(
    type="Optometry / Eye care", noun="optometry clinic", nouns="eye care clinics",
    title="Optometry Clinic Design + Construction in BC | Medico",
    eyebrow="For optometrists | British Columbia",
    h1="16 eye care clinics built. Yours won't be our first.",
    offer="<b>Exam lanes, pretest, dispensary and frame display</b>, designed and built by Medico. Start with a site assessment of your space. No obligation.",
    hero=("o-hero", "Reception and dispensary at White Rock Optometry, built by Medico", "<b>White Rock Optometry</b> · White Rock, BC · 4,492 sq ft"),
    count="16", countlab="eye care clinics built",
    rooms_h="An optometry clinic is a clinic and a store.",
    rooms_p="These are rooms we designed and built. Exam lanes, pretest and the dispensary each need their own planning.",
    rooms=[
        ("o-lane", "Exam lanes", "Lane length and layout planned around your space and your equipment.", "Mishe Optometry"),
        ("o-exam", "Exam rooms", "Chair, stand and instruments placed for how you examine.", "White Rock Optometry"),
        ("o-frames", "Frame display", "Lit cases and drawers that sell frames and lock them up.", "White Rock Optometry"),
        ("o-wall", "Dispensary", "Frame walls, fitting tables and storage in one selling space.", "Mishe Optometry"),
        ("o-pretest", "Pretest", "Room for the instruments you run before the exam.", "White Rock Optometry"),
        ("o-wait", "Waiting", "A calm waiting area that keeps patients near the dispensary.", "White Rock Optometry"),
    ],
    projects=[
        ("p-whiterock", "White Rock Optometry", "White Rock, BC", "4,492 sq ft"),
        ("p-mishe", "Mishe Optometry", "Surrey, BC", "1,000 sq ft"),
        ("p-mtp", "Mt. Pleasant Optometry", "Vancouver, BC", "About 4,300 sq ft"),
        ("p-optom", "Opto-mization NeuroVisual", "Victoria, BC", "6,600 sq ft"),
        ("p-integra", "Integra Eyecare Centre", "Vancouver, BC", "Optometry clinic"),
        ("p-clear", "ClearLight Eyecare", "North Vancouver, BC", "900 sq ft"),
        ("p-delta", "Delta Eye Care", "Delta, BC", "700 sq ft"),
        ("p-ccopt", "City Centre Optical", "Surrey, BC", "800 sq ft"),
    ],
    proj_h="Eye care clinics we've built across BC.",
    quotes=[
        ("Team Medico knew exactly what we needed for our exam lanes, dispensary and how to maximize the use of our equipment.", "Dr. Gupta", "Optometrist", ""),
        ("Medico Construction completed a full build out of my clinic from dirt floors to a finished optometry clinic and dispensary.", "Dr. Petreman", "Origins Optometry", ""),
        ("Professional, efficient, and highly detail-oriented... the quality of workmanship exceeded our expectations.", "Mishe Optometry", "Surrey, BC · Google review", "g"),
    ],
    faq=[
        ("How much does it cost to build an optometry clinic?", "It depends on the space, the number of lanes, your equipment, the dispensary and finishes. A site assessment is the fastest way to get a real number for your space, not a guess."),
        ("How long does an exam lane need to be?", "It depends on your equipment and whether you use mirrors or a screen. We check it against your space before you commit."),
        ("Should I talk to Medico before signing a lease?", "Yes. Lane length, power and storefront decide whether a unit works. We can flag problems before you commit to a space."),
        ("Can you renovate a clinic that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),

"medical": dict(
    type="Medical / Family Practice", noun="medical clinic", nouns="medical clinics",
    title="Medical Clinic Design + Construction in BC | Medico",
    eyebrow="For doctors | British Columbia",
    h1="We build clinics, not offices. More than 100 of them.",
    offer="<b>Exam rooms, reception, treatment and patient flow</b>, designed and built by Medico. Start with a site assessment of your space. No obligation.",
    hero=("m-hero", "Waiting room and reception at Babylon by TELUS Health, Victoria, built by Medico", "<b>Babylon by TELUS Health</b> · Victoria, BC · 1,475 sq ft"),
    count="100+", countlab="clinics built",
    rooms_h="A medical clinic isn't an office with exam tables.",
    rooms_p="These are rooms we designed and built. Privacy, plumbing and patient flow are planned before construction starts.",
    rooms=[
        ("m-exam", "Exam rooms", "Sinks, power, storage and the exam table placed for how you see patients.", "Axis Primary Care"),
        ("m-exam2", "Privacy", "Exam rooms designed so patients can't hear the next room.", "Cornerstone Pediatric"),
        ("m-recep", "Reception", "Check-in that sees the door and the waiting room.", "Harvard Place Medical Clinic"),
        ("m-hero", "Waiting", "A waiting room patients remember for the right reasons.", "Babylon by TELUS Health"),
        ("m-treat", "Treatment", "Treatment areas with the services and space they need.", "Crescent Health Clinic"),
        ("m-small", "Small spaces", "A full clinic in 1,000 sq ft, planned for flow from check-in to consult.", "Cornerstone Pediatric"),
    ],
    projects=[
        ("p-babylon", "Babylon by TELUS Health", "Victoria, BC", "1,475 sq ft"),
        ("p-harvard", "Harvard Place Medical Clinic", "Vancouver, BC", "Medical clinic"),
        ("p-axis", "Axis Primary Care", "Surrey, BC", "3,750 sq ft"),
        ("p-cc2", "CC2 Medical Clinic", "Surrey, BC", "2,050 sq ft"),
        ("p-pulse", "Pulse Medical Clinic", "Surrey, BC", "Medical clinic"),
        ("p-cornerstone", "Cornerstone Pediatric", "Langley, BC", "1,000 sq ft"),
    ],
    proj_h="Medical clinics we've built across BC.",
    quotes=[
        ("Medico was able to articulate the scope of the project and was able to clearly communicate areas he anticipated there would be difficulties.", "Dr. Navnirat Nibber", "Crescent Health Clinic", ""),
        ("They genuinely cared about our project and spent time and attention to ensure we had a beautiful, well-made clinic.", "Dr. C.Y.", "Clinic owner", ""),
    ],
    faq=[
        ("How much does it cost to build a medical clinic?", "It depends on the space, the number of exam rooms, existing plumbing and power, accessibility work and finishes. A site assessment is the fastest way to get a real number for your space, not a guess."),
        ("How many exam rooms fit in my space?", "It depends on the shape of the unit, where plumbing can go and how patients move through. We plan it with you before you commit."),
        ("Should I talk to Medico before signing a lease?", "Yes. Plumbing, power, accessible washrooms and permits can change your layout, cost and opening date. We can flag problems before you sign."),
        ("Can you renovate a clinic that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),
}

ICONS = {
 "plumb": '<path d="M7 3v6a5 5 0 0 0 10 0V3M12 14v7M8 21h8"/>',
 "power": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "air": '<path d="M3 8h11a3 3 0 1 0-3-3M3 12h16a3 3 0 1 1-3 3M3 16h7"/>',
 "door": '<circle cx="12" cy="4.5" r="1.8"/><path d="M12 7v6h5l2 6M12 10H8M7 13a5 5 0 1 0 6 6"/>',
 "rooms": '<path d="M3 4h18v16H3zM3 12h8M11 4v16M11 15h10"/>',
 "permit": '<path d="M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7"/>',
}

HEAD_TAGS = open(os.path.join(ROOT, "index.html")).read()
# Reuse the exact tracking block of the main page (Google tag, Meta pixel, Clarity), so nothing drifts.
TRACK = HEAD_TAGS[HEAD_TAGS.index("<!-- Google Ads tag"):HEAD_TAGS.index("</head>")]
FORM = HEAD_TAGS[HEAD_TAGS.index('<form id="lead"'):HEAD_TAGS.index("</form>") + len("</form>")]
SYMBOLS = HEAD_TAGS[HEAD_TAGS.index('<svg width="0"'):HEAD_TAGS.index("</svg>", HEAD_TAGS.index('<svg width="0"')) + 6]


def page(key, c):
    hk, halt, hcap = c["hero"]
    rooms = "\n".join(
        f'<figure class="room">{img(k, f"{t} at {where}, built by Medico", sizes="(max-width:700px) 50vw, 33vw")}'
        f'<figcaption><b>{E(t)}</b><span>{E(d)}</span><small>{E(where)}</small></figcaption></figure>'
        for k, t, d, where in c["rooms"])
    projects = "\n".join(
        f'<figure class="proj">{img(k, f"{n}, {city}, built by Medico", sizes="(max-width:700px) 50vw, 33vw")}'
        f'<figcaption><b>{E(n)}</b><span>{E(city)} · {E(sz)}</span></figcaption></figure>'
        for k, n, city, sz in c["projects"])
    quotes = "\n".join(
        f'<figure class="q"><blockquote>"{E(t)}"</blockquote><figcaption>'
        + ('<svg class="gl"><use href="#i-g"/></svg>' if g else '')
        + f'<span><b>{E(who)}</b>{E(sub)}</span></figcaption></figure>'
        for t, who, sub, g in c["quotes"])
    checks = "\n".join(
        f'<li><span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[i]}</svg></span>'
        f'<div><b>{E(t)}</b><span>{E(d)}</span></div></li>' for i, t, d in CHECKS)
    faq = "\n".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in c["faq"])
    proof = f'''<ul class="chips" aria-label="Ratings and credentials">
        <li><svg class="gl"><use href="#i-g"/></svg><span><b>5.0 <i aria-hidden="true">★★★★★</i></b>Google rating</span></li>
        <li><span class="bbb" aria-hidden="true">BBB</span><span><b>A+</b>BBB rating</span></li>
        <li><span class="ic"><svg><use href="#i-plan"/></svg></span><span><b>{c["count"]}</b>{E(c["countlab"])}</span></li>
      </ul>'''
    return f'''<!doctype html>
<html lang="en-CA" data-mv="{key}" data-mtype="{E(c["type"])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(c["title"])}</title>
<meta name="description" content="{E(c["noun"].capitalize())} design and construction in British Columbia by Medico. Start with a site assessment of your space.">
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/medico-favicon-192.png">
<link rel="preload" href="/assets/fonts/montserrat-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="/assets/m/{hk}-1280.webp" imagesrcset="/assets/m/{hk}-720.webp 720w, /assets/m/{hk}-1280.webp 1280w" imagesizes="(max-width:700px) 100vw, 50vw">
<link rel="stylesheet" href="/m/m.css">
{TRACK}</head>
<body>
{SYMBOLS}
<!-- Built by tools/mpages.py. Edit the script, not this file. -->
<header class="top">
  <div class="wrap">
    <a class="logo" href="#top" aria-label="Medico Construction and Design"><img src="/assets/medico-logo.svg" width="273" height="57" alt="Medico Construction and Design"></a>
    <a class="phone" href="tel:+16046444120" aria-label="Call Medico at 604-644-4120"><svg><use href="#i-phone"/></svg><span>604-644-4120</span></a>
  </div>
</header>

<main id="top">

<section class="hero">
  <div class="wrap hgrid">
    <figure class="hshot">
      <img data-v="img" src="/assets/m/{hk}-1280.webp" srcset="/assets/m/{hk}-720.webp 720w, /assets/m/{hk}-1280.webp 1280w" sizes="(max-width:900px) 100vw, 50vw" width="1280" height="853" alt="{E(halt)}" fetchpriority="high">
      <figcaption data-v="cap">{hcap}</figcaption>
    </figure>
    <div class="htext">
      <p class="eyebrow" data-v="eyebrow">{E(c["eyebrow"])}</p>
      <h1 data-v="h1">{E(c["h1"])}</h1>
      <p class="sub" data-v="offer">{c["offer"]}</p>
      <div class="hcta">
        <a class="btn big" href="#start" data-goform>Book My Site Assessment</a>
        <a class="tel" href="tel:+16046444120">or call 604-644-4120</a>
      </div>
      {proof}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head"><h2>{E(c["rooms_h"])}</h2><p>{E(c["rooms_p"])}</p></div>
    <div class="rooms">
{rooms}
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="head"><h2>{E(c["proj_h"])}</h2><p>Real clinics, designed and built by Medico. {c["count"]} {E(c["countlab"])}{"" if c["count"]=="100+" else ", and 100+ healthcare spaces in all"}.</p></div>
    <div class="projs">
{projects}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap sa">
    <div class="sa-l">
      <p class="eyebrow">Step one</p>
      <h2>What we check on your site assessment.</h2>
      <p class="lead">A Medico project specialist looks at your space with you and flags what could change your layout, cost or opening date. Before you sign a lease, approve a layout or start construction.</p>
      <a class="btn" href="#start" data-goform>Book My Site Assessment</a>
    </div>
    <ol class="checks">
{checks}
    </ol>
  </div>
</section>

<section class="sec ink">
  <div class="wrap">
    <div class="quotes">
{quotes}
    </div>
    <div class="bar">
      <div><b>Pricing that holds</b><span>We lock in fixed pricing with our suppliers upfront, so your quote doesn't move on you mid-project.</span></div>
      <div><b>A real number</b><span>Whatever your budget is, we've likely already worked with it. You get a real number, not a guess.</span></div>
      <div><b>Design, permits, build</b><span>Layout, permit drawings and construction under one roof, so nothing falls between trades.</span></div>
    </div>
  </div>
</section>

<section class="sec tint formsec" id="book">
  <div class="wrap fgrid">
    <div class="fl">
      <h2>Book your site assessment.</h2>
      <p class="lead">Five quick taps, then your contact details. Takes about 60 seconds.</p>
      <ol class="next">
        <li><span><b>You tell us</b> about the space, size and timeline.</span></li>
        <li><span><b>A Medico project specialist calls you</b> to talk it through.</span></li>
        <li><span><b>We look at the space with you</b> and flag what could change your plans.</span></li>
      </ol>
      <p class="small">No obligation. Medico builds in British Columbia.</p>
    </div>
    <div class="card formcard" id="start">
      <div class="f-top"><p class="f-title">Book your site assessment</p><p class="f-count" id="fcount" aria-live="polite">Step 1 of 6</p></div>
      <div class="f-bar" aria-hidden="true"><i id="fbar"></i></div>
      {FORM}
      <div class="f-foot"><span>Takes about 60 seconds</span><a href="/privacy.html">Privacy policy</a></div>
    </div>
  </div>
</section>

<section class="sec faq">
  <div class="wrap fq">
    <h2>Questions {E(c["noun"])} owners ask</h2>
    <div>
{faq}
    </div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2>Have a space in mind? Let's look at it together.</h2>
    <div class="acts"><a class="btn big" href="#start" data-goform>Book My Site Assessment</a><a class="tel" href="tel:+16046444120">Prefer to talk? Call 604-644-4120</a></div>
    <p class="trustline">Healthcare-focused · British Columbia · Licensed &amp; insured</p>
  </div>
</section>

</main>

<footer class="foot">
  <div class="wrap">
    <img src="/assets/medico-logo.svg" width="273" height="57" alt="Medico Construction and Design">
    <span>Medico Construction &amp; Design · Licensed &amp; insured · British Columbia</span>
    <a href="/privacy.html">Privacy policy</a>
  </div>
</footer>

<div class="stick" id="stick">
  <a class="btn" href="#start" data-goform>Book My Site Assessment</a>
  <a class="btn ghost call" href="tel:+16046444120" aria-label="Call Medico"><svg><use href="#i-phone"/></svg></a>
</div>

<script src="/app.js" defer></script>
<script src="/m/m.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    import sys
    # --qa DIR: a local preview copy without the Google/Meta/Clarity tags, so test visits never reach real analytics.
    qa = sys.argv[sys.argv.index("--qa") + 1] if "--qa" in sys.argv else None
    for key, c in CATS.items():
        out = page(key, c)
        if qa:
            out = out.replace(TRACK, "")
            d = os.path.join(qa, "m", key); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w").write(out); continue
        assert "—" not in out, f"em dash in {key}"
        d = os.path.join(ROOT, "m", key); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(out)
        print("wrote", d)
