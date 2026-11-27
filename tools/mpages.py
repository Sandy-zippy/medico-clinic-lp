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
    ("rooms", "Room count", "How many rooms the unit really fits once circulation is planned."),
    ("permit", "Permits", "What the city is likely to ask for, so your opening date is realistic."),
]

CATS = {
"vet": dict(
    type="Veterinary", noun="animal hospital", nouns="vet clinics",
    title="Veterinary Clinic Design + Construction in BC | Medico",
    eyebrow="For veterinarians | British Columbia",
    h1="Your animal hospital won't be our first.",
    offer="<b>Treatment, surgery, imaging, wards and exam rooms</b>, designed and built by Medico. Start with a site assessment of your unit. No obligation.",
    hero=("v-hero", "Treatment area at Woodland Veterinary Clinic, Vancouver, built by Medico", "<b>Woodland Veterinary Clinic</b> · Vancouver, BC · 2,200 sq ft"),
    count="6", countlab="animal hospitals built",
    rooms_h="Every room in a vet hospital has its own rules.",
    rooms_p="These are rooms we designed and built. Each one needs its own plumbing, power, layout and finishes, planned before construction starts.",
    rooms=[
        ("v-treat", "Treatment", "Wet tables, sinks, power and storage where your team actually works.", "Paws on Fraser Veterinary Hospital"),
        ("v-surg", "Surgery", "Procedure lighting, room for equipment and a room that's easy to keep clean.", "Paws on Fraser Veterinary Hospital"),
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
        ("How much does it cost to build a vet clinic?", "It depends on the unit, its existing plumbing and power, how many exam, treatment and ward areas you need, imaging, and finishes. A site assessment is the fastest way to get a real number for your unit, not a guess."),
        ("How big should a vet clinic be?", "Big enough for your exam rooms, treatment, surgery, wards, imaging and staff areas, with room for how your team moves between them. We lay it out around your workflow from the first plan."),
        ("Should I talk to Medico before signing a lease?", "Yes. Drains, power and ventilation decide where treatment, surgery and wards can go. We can flag problems before you commit to a unit."),
        ("Can you renovate a clinic that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),

"dental": dict(
    type="Dental", noun="dental office", nouns="dental clinics",
    title="Dental Office Design + Construction in BC | Medico",
    eyebrow="For dentists | British Columbia",
    h1="Any contractor can build an office. We build dental clinics.",
    offer="<b>Water, air and vacuum at every chair, power for the equipment, room for imaging.</b> Start with a site assessment of your unit. No obligation.",
    hero=("d-hero", "Reception at Smile Plus Dentistry, Surrey, designed and built by Medico", "<b>Smile Plus Dentistry</b> · Surrey, BC · 2,840 sq ft"),
    count="100+", countlab="healthcare projects built",
    rooms_h="A dental office is built around the operatory.",
    rooms_p="These are rooms we designed and built. The services behind the walls are planned before the first wall goes up.",
    rooms=[
        ("d-op", "Operatories", "Chair, delivery unit and cabinetry placed around how you and your assistant work.", "Chilliwack Dental"),
        ("d-op2", "Services to every chair", "Water, air, vacuum and power routed to each op and planned with your equipment.", "Smile Plus Dentistry"),
        ("d-steri", "Sterilization", "A clean-to-dirty workflow with sinks, counters and room for equipment.", "Chilliwack Dental"),
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
    proj_h="Dental clinics, and the healthcare projects around them.",
    quotes=[("They genuinely cared about our project and spent time and attention to ensure we had a beautiful, well-made clinic.", "Dr. C.Y.", "Clinic owner", "")],
    faq=[
        ("How much does it cost to build a dental office?", "It depends on the unit, the number of operatories, your equipment, imaging, the mechanical room and finishes. A site assessment is the fastest way to get a real number for your unit, not a guess."),
        ("When should I pick my equipment?", "Early. Chairs, compressors, vacuum and imaging decide where plumbing and power go. We plan the rooms around the equipment you choose."),
        ("Should I talk to Medico before signing a lease?", "Yes. Floor drains, slab work, power and ventilation can change your layout and cost. We can flag problems before you commit to a unit."),
        ("Can you renovate a practice that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),

"optometry": dict(
    type="Optometry / Eye care", noun="optometry clinic", nouns="eye care clinics",
    title="Optometry Clinic Design + Construction in BC | Medico",
    eyebrow="For optometrists | British Columbia",
    h1="16 eye care clinics built. Yours won't be our first.",
    offer="<b>Exam lanes, pretest, dispensary and frame display</b>, designed and built by Medico. Start with a site assessment of your unit. No obligation.",
    hero=("o-hero", "Reception and dispensary at White Rock Optometry, built by Medico", "<b>White Rock Optometry</b> · White Rock, BC · 4,492 sq ft"),
    count="16", countlab="eye care clinics built",
    rooms_h="An optometry clinic is a clinic and a store.",
    rooms_p="These are rooms we designed and built. Exam lanes, pretest and the dispensary each need their own planning.",
    rooms=[
        ("o-lane", "Exam lanes", "Lane length and layout planned around your unit and your equipment.", "Mishe Optometry"),
        ("o-exam", "Exam rooms", "Chair, stand and instruments placed for how you examine.", "White Rock Optometry"),
        ("o-frames", "Frame display", "Lit cases and drawers that sell frames and lock them up.", "White Rock Optometry"),
        ("o-wall", "Dispensary", "Frame walls, fitting tables and storage in one selling area.", "Mishe Optometry"),
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
        ("How much does it cost to build an optometry clinic?", "It depends on the unit, the number of lanes, your equipment, the dispensary and finishes. A site assessment is the fastest way to get a real number for your unit, not a guess."),
        ("How long does an exam lane need to be?", "It depends on your equipment and whether you use mirrors or a screen. We check it against your unit before you commit."),
        ("Should I talk to Medico before signing a lease?", "Yes. Lane length, power and storefront decide whether a unit works. We can flag problems before you commit to a unit."),
        ("Can you renovate a clinic that's still operating?", "Some projects can be phased to reduce disruption. We assess access, safety and sequencing first and plan the right approach with you."),
    ]),

"medical": dict(
    type="Medical / Family Practice", noun="medical clinic", nouns="medical clinics",
    title="Medical Clinic Design + Construction in BC | Medico",
    eyebrow="For doctors | British Columbia",
    h1="We build clinics, not offices. More than 100 of them.",
    offer="<b>Exam rooms, reception, treatment and patient flow</b>, designed and built by Medico. Start with a site assessment of your unit. No obligation.",
    hero=("m-hero", "Waiting room and reception at Babylon by TELUS Health, Victoria, built by Medico", "<b>Babylon by TELUS Health</b> · Victoria, BC · 1,475 sq ft"),
    count="100+", countlab="clinics built",
    rooms_h="A medical clinic isn't an office with exam tables.",
    rooms_p="These are rooms we designed and built. Privacy, plumbing and patient flow are planned before construction starts.",
    rooms=[
        ("m-exam", "Exam rooms", "Sinks, power, storage and the exam table placed for how you see patients.", "Axis Primary Care"),
        ("m-exam2", "Privacy", "Exam rooms designed so patients can't hear the next room.", "Cornerstone Pediatric"),
        ("m-recep", "Reception", "Check-in that sees the door and the waiting room.", "Harvard Place Medical Clinic"),
        ("m-hero", "Waiting", "A waiting room patients remember for the right reasons.", "Babylon by TELUS Health"),
        ("m-treat", "Treatment", "Treatment areas with the services and room they need.", "Crescent Health Clinic"),
        ("m-small", "Small units", "A full clinic in 1,000 sq ft, planned for flow from check-in to consult.", "Cornerstone Pediatric"),
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
        ("How much does it cost to build a medical clinic?", "It depends on the unit, the number of exam rooms, existing plumbing and power, accessibility work and finishes. A site assessment is the fastest way to get a real number for your unit, not a guess."),
        ("How many exam rooms fit in my unit?", "It depends on the shape of the unit, where plumbing can go and how patients move through. We plan it with you before you commit."),
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


def angles_for(ctype):
    """The Meta ad angles (?a=) from app.js, as JSON, for an inline script that applies them before first paint.
    app.js applies the same angle again after load (same values), so the two can never disagree."""
    import json, subprocess
    js = open(os.path.join(ROOT, "app.js")).read()
    lit = js[js.index("const ANGLES = ") + len("const ANGLES = "):js.index("const DESIGN_HERO")].strip().rstrip(";")
    data = json.loads(subprocess.check_output(["node", "-e", f"process.stdout.write(JSON.stringify({lit}))"]))
    keep = {k: {f: v[f] for f in ("eyebrow", "h1", "offer", "img", "alt", "cap", "pos") if f in v}
            for k, v in data.items() if v.get("type") in (ctype, None)}
    return json.dumps(keep, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")


def ad_angle_map():
    """app.js AD_ANGLE (Meta ad id in utm_content -> angle), so ads without ?a= get their angle before first paint too."""
    import json, subprocess
    js = open(os.path.join(ROOT, "app.js")).read()
    lit = js[js.index("const AD_ANGLE = ") + len("const AD_ANGLE = "):].split("};", 1)[0] + "}"
    return json.dumps(json.loads(subprocess.check_output(["node", "-e", f"process.stdout.write(JSON.stringify({lit}))"])), separators=(",", ":"))


# ---------------------------------------------------------------------------------------------------------------
# v2 (27 Nov 2026 PM), rebuilt with the HQ landing-page chain (landing-page-build + sabri-structure, direct-response,
# copy-engine module-landing-page + gate-icp-language, impeccable). Build log: medico/lp-meta-2026-11-27/BUILD-LOG.md.
# Evidence that set the structure: Clarity, 143 Facebook sessions on the old page, 81% never scrolled and 19% reached
# section 2. So the first screen carries the whole job: the ad's own photo and headline, who it is for, and the first
# form question as one-tap answers. Everything below the fold is for the 1 in 5 who scroll.
# ---------------------------------------------------------------------------------------------------------------

# Buyer's own nouns per category (research_notes/Clinic buyer voice by stage). Callout = A1 / hero slot 1.
V2 = {
"vet": dict(
    callout="For vets building or moving a clinic",
    pin_img=("v-treat", "Treatment room at Paws on Fraser Veterinary Hospital, built by Medico"),
    pins_h="Where vet builds go wrong",
    pins_sub="Three problems we check for on every vet site assessment, shown in a treatment room we built.",
    pins=[  # x%, y% on the photo, the named failure (buyer's words), what we check
        (31, 61, "Floor drains in the wrong place", "We plan drains around your wet tables, tubs and runs before the slab is cut."),
        (25, 17, "Not enough power for the equipment", "We check the unit's power against your surgery, X-ray and lab equipment."),
        (90, 9, "Barking and odour through the walls", "We plan walls and ventilation so noise and odour stay inside the clinic."),
    ],
    gal_h="Vet hospitals we've built", gal_n="6", gal_unit="animal hospitals in BC",
    quotes=["nn", "cy", "manjeet"],
    faq_first=("How much does it cost to build a vet clinic?", "It depends on the unit, its drains and power, how many exam, treatment and ward areas you need, imaging and finishes. A site assessment is how you get a real number for your unit, not a guess."),
),
"dental": dict(
    callout="For dentists building or moving a practice",
    pin_img=("d-op", "Operatory at Chilliwack Dental, built by Medico"),
    pins_h="Where dental builds go wrong",
    pins_sub="Three problems we check for on every dental site assessment, shown in an operatory we built.",
    pins=[
        (62, 82, "Plumbing that misses the chairs", "We route water, air and vacuum to every operatory, planned with your equipment."),
        (55, 40, "Equipment picked after the walls", "We plan rooms around the chairs, compressor and imaging you choose."),
        (34, 38, "No room for sterilization flow", "We lay out clean-to-dirty flow with sinks and counters where your team works."),
    ],
    gal_h="Dental offices we've built", gal_n="100+", gal_unit="healthcare projects in BC",
    quotes=["nn", "cy", "manjeet"],
    faq_first=("How much does it cost to build a dental office?", "It depends on the unit, the number of operatories, your equipment, imaging, the mechanical room and finishes. A site assessment is how you get a real number for your unit, not a guess."),
),
"optometry": dict(
    callout="For optometrists building a clinic",
    pin_img=("o-lane", "Exam lane at Mishe Optometry, Surrey, built by Medico"),
    pins_h="Where optometry builds go wrong",
    pins_sub="Three problems we check for on every optometry site assessment, shown in an exam lane we built.",
    pins=[
        (76, 74, "Lanes too short for your equipment", "We measure lane length against your chart, mirrors or screen before you sign."),
        (68, 30, "Instruments with no power or room", "We place power, data and room for your pretest and exam instruments."),
        (10, 66, "No plumbing for the edger", "We plan sinks and plumbing for your lab and exam rooms."),
    ],
    gal_h="Eye care clinics we've built", gal_n="16", gal_unit="eye care clinics in BC",
    quotes=["gupta", "petreman", "mishe"],
    faq_first=("How much does it cost to build an optometry clinic?", "It depends on the unit, the number of lanes, your equipment, the dispensary and finishes. A site assessment is how you get a real number for your unit, not a guess."),
),
"medical": dict(
    callout="For doctors building or moving a clinic",
    pin_img=("m-exam", "Exam room at Axis Primary Care, Surrey, built by Medico"),
    pins_h="Where clinic builds go wrong",
    pins_sub="Three problems we check for on every clinic site assessment, shown in an exam room we built.",
    pins=[
        (57, 44, "Exam rooms with no sink", "We plan plumbing for the rooms that need sinks, before you sign the lease."),
        (25, 18, "Walls patients can hear through", "We build exam room walls for privacy, so the next room can't hear."),
        (88, 36, "Fewer rooms than you planned", "We lay out your exam room count against the real shape of the unit."),
    ],
    gal_h="Medical clinics we've built", gal_n="100+", gal_unit="clinics in BC",
    quotes=["nn", "cy", "manjeet"],
    faq_first=("How much does it cost to build a medical clinic?", "It depends on the unit, the number of exam rooms, its plumbing and power, accessibility work and finishes. A site assessment is how you get a real number for your unit, not a guess."),
),
}

# Real testimonials only. Sources: medicoconstruction.com/testimonials (copied verbatim 1 Nov 2026,
# website/content/testimonials.md) and the Google reviews already on the main page (index.html).
QUOTES = {
 "nn": ("Medico was able to articulate the scope of the project and clearly communicate areas he anticipated there would be difficulties.", "Dr. Navnirat Nibber", "Crescent Health Clinic, South Surrey", ""),
 "cy": ("They genuinely cared about our project and spent time and attention to ensure we had a beautiful, well-made clinic.", "Dr. C.Y.", "Clinic owner", ""),
 "manjeet": ("They communicate well and keep you in the loop of the project and its progress.", "Manjeet B.", "Google review", "g"),
 "gupta": ("Team Medico knew exactly what we needed for our exam lanes, dispensary and how to maximize the use of our equipment.", "Dr. Gupta", "Optometrist", ""),
 "petreman": ("Medico Construction completed a full build out of my clinic from dirt floors to a finished optometry clinic and dispensary.", "Dr. Petreman", "Origins Optometry", ""),
 "mishe": ("Professional, efficient, and highly detail-oriented... the quality of workmanship exceeded our expectations.", "Mishe Optometry", "Surrey, BC, Google review", "g"),
}

PROOF_LINE = '<p class="proofline"><span class="pi"><svg class="gl" aria-hidden="true"><use href="#i-g"/></svg><b>5.0</b> on Google</span><span class="pi">BBB <b>A+</b></span><span class="pi"><b>{n}</b> {unit}</span></p>'


def page(key, c):
    v = V2[key]
    hk, halt, hcap = c["hero"]
    proof = PROOF_LINE.format(n=c["count"], unit=E(c["countlab"]))
    # Hero answers mirror the form's first question; a tap answers it in the real form (m/m.js), so the step
    # the visitor lands on is step 2 and the form_step_2 event fires exactly as it does inside the form.
    answers = "".join(f'<button type="button" class="ans" data-answer="{E(a)}">{E(a)}</button>'
                      for a in ("New clinic", "Renovation", "Expansion", "Relocation"))
    pi, palt = v["pin_img"]
    pins = "".join(f'<li class="pin" style="--x:{x}%;--y:{y}%" aria-hidden="true"><span>{n}</span></li>'
                   for n, (x, y, _, _) in enumerate(v["pins"], 1))
    pinlist = "".join(f'<li><span class="pn" aria-hidden="true">{n}</span><div><b>{E(t)}</b><p>{E(d)}</p></div></li>'
                      for n, (_, _, t, d) in enumerate(v["pins"], 1))
    cards = [(k, t, where) for k, t, _, where in c["rooms"]] + [(k, n, f"{city} · {sz}") for k, n, city, sz in c["projects"]]
    seen, gal = set(), []
    for k, t, sub in cards:
        if k in seen: continue
        seen.add(k)
        gal.append(f'<li class="gi">{img(k, f"{t}, {sub}, built by Medico", sizes="(max-width:700px) 78vw, 380px")}'
                   f'<p><b>{E(t)}</b><span>{E(sub)}</span></p></li>')
    gal = "\n".join(gal)
    quotes = "\n".join(
        f'<figure class="q"><div class="stars" aria-label="5 out of 5"><i></i></div><blockquote>"{E(QUOTES[q][0])}"</blockquote>'
        f'<figcaption>' + ('<svg class="gl" aria-hidden="true"><use href="#i-g"/></svg>' if QUOTES[q][3] else '')
        + f'<span><b>{E(QUOTES[q][1])}</b>{E(QUOTES[q][2])}</span></figcaption></figure>' for q in v["quotes"])
    faqs = [v["faq_first"]] + c["faq"][1:] + [("Why isn't there a price on this page?", "Because a clinic's cost is set by the unit you have, not by a list. After the site assessment you get a real number for your unit.")]
    faq = "\n".join(f'<details{" open" if n == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for n, (q, a) in enumerate(faqs))
    ask = lambda label="Book My Site Assessment": f'{proof}<a class="btn big" href="#start" data-goform>{label}</a>'
    return f'''<!doctype html>
<html lang="en-CA" data-mv="{key}" data-mtype="{E(c["type"])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(c["title"])}</title>
<meta name="description" content="{E(c["noun"].capitalize())} design and construction in British Columbia by Medico. Start with a site assessment of your unit.">
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/medico-favicon-192.png">
<link rel="preload" href="/assets/fonts/montserrat-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/opensans-400.woff2" as="font" type="font/woff2" crossorigin>
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

<section class="hero" aria-labelledby="h1">
  <div class="wrap hgrid">
    <figure class="hshot">
      <img data-v="img" data-src="/assets/m/{hk}-1280.webp" data-srcset="/assets/m/{hk}-720.webp 720w, /assets/m/{hk}-1280.webp 1280w" sizes="(max-width:900px) 100vw, 50vw" width="1280" height="853" alt="{E(halt)}" fetchpriority="high">
      <noscript><img src="/assets/m/{hk}-1280.webp" width="1280" height="853" alt="{E(halt)}"></noscript>
      <figcaption data-v="cap">{hcap}</figcaption>
    </figure>
    <div class="htext">
      <p class="callout">{E(v["callout"])}</p><span data-v="eyebrow" hidden></span>
      <h1 id="h1" data-v="h1">{E(c["h1"])}</h1>
      <p class="sub" data-v="offer">{c["offer"]}</p>
      <div class="quick" role="group" aria-labelledby="qlab">
        <p class="qlab" id="qlab">Book a site assessment. What are you planning?</p>
        <div class="answers">{answers}</div>
        <p class="qnote"><button type="button" class="linkish" data-answer="Still evaluating options">Not sure yet</button><span>4 more taps, then a Medico project specialist calls you.</span></p>
      </div>
      {proof}
    </div>
  </div>
</section>
<script>/* Ad angle before first paint, so the visitor never sees the default headline or photo flip to the ad's. */
(function(){{var A={angles_for(c["type"])},q=new URLSearchParams(location.search),D={ad_angle_map()},a=A[(q.get("a")||(q.get("v")?"":D[q.get("utm_content")])||"").toLowerCase()];
var $=function(s){{return document.querySelector('[data-v="'+s+'"]')}},im=$("img");
if(!a||!a.img){{im.srcset=im.dataset.srcset;im.src=im.dataset.src}}if(!a)return;
if(a.h1)$("h1").textContent=a.h1;if(a.offer)$("offer").innerHTML=a.offer;
if(a.img){{var i=im;i.src=a.img[0];i.alt=a.alt||"";if(a.pos)i.style.objectPosition=a.pos;$("cap").innerHTML=a.cap||""}}}})();</script>

<section class="sec pinsec arrive" aria-labelledby="pins-h">
  <div class="wrap">
    <div class="head"><h2 id="pins-h">{E(v["pins_h"])}</h2><p>{E(v["pins_sub"])}</p></div>
    <div class="pingrid">
      <figure class="pinshot">{img(pi, palt, sizes="(max-width:900px) 100vw, 640px")}<ol class="pins">{pins}</ol></figure>
      <ol class="pinlist">{pinlist}</ol>
    </div>
    <div class="ask">{ask("Book My Site Assessment")}</div>
  </div>
</section>

<section class="sec tint galsec arrive" aria-labelledby="gal-h">
  <div class="wrap">
    <div class="head"><h2 id="gal-h">{E(v["gal_h"])}</h2><p><b class="count" data-to="{v["gal_n"]}">{v["gal_n"]}</b> {E(v["gal_unit"])}, designed and built by Medico, from first drawing to handover. Swipe through the rooms.</p></div>
  </div>
  <ul class="gal" tabindex="0" aria-label="Rooms and clinics built by Medico">
{gal}
  </ul>
  <div class="wrap"><div class="galbar" aria-hidden="true"><i></i></div></div>
</section>

<section class="sec stepsec arrive" aria-labelledby="steps-h">
  <div class="wrap">
    <div class="head"><h2 id="steps-h">What happens after you tap</h2></div>
    <ol class="steps">
      <li><span class="sn">1</span><b>You answer 5 questions</b><p>About your unit, size and timing. About 60 seconds.</p></li>
      <li><span class="sn">2</span><b>A project specialist calls you</b><p>Someone from Medico talks your project through with you.</p></li>
      <li><span class="sn">3</span><b>We walk the unit with you</b><p>And flag what could change your layout, cost or opening date.</p></li>
    </ol>
    <div class="turnkey"><p>Then one company, start to finish:</p><ul><li>Design</li><li>Permits</li><li>Construction</li><li>Handover</li></ul></div>
  </div>
</section>

<section class="sec ink revsec arrive" aria-labelledby="rev-h">
  <div class="wrap">
    <div class="head"><h2 id="rev-h">What clinic owners say</h2><p>From Google reviews and Medico's own clients.</p></div>
    <div class="quotes">
{quotes}
    </div>
  </div>
</section>

<section class="sec tint formsec" id="book" aria-labelledby="book-h">
  <div class="wrap fgrid">
    <div class="fl">
      <h2 id="book-h">Tell us about your clinic</h2>
      <p class="lead">Five quick taps, then your contact details. About 60 seconds.</p>
      {proof}
      <p class="small">No obligation. Medico builds clinics across British Columbia.</p>
    </div>
    <div class="card formcard" id="start">
      <div class="f-top"><p class="f-title">Book your site assessment</p><p class="f-count" id="fcount" aria-live="polite">Step 1 of 6</p></div>
      <div class="f-bar" aria-hidden="true"><i id="fbar"></i></div>
      {FORM.replace('name="page" value="medical"', f'name="page" value="{key}"')}
      <div class="f-foot"><span>Takes about 60 seconds</span><a href="/privacy.html">Privacy policy</a></div>
    </div>
  </div>
</section>

<section class="sec faq" aria-labelledby="faq-h">
  <div class="wrap fq">
    <h2 id="faq-h">What owners ask us first</h2>
    <div>
{faq}
    </div>
  </div>
</section>

<section class="final" aria-labelledby="ps-h">
  <div class="wrap">
    <h2 id="ps-h" class="sr">In short</h2>
    <p class="ps"><b>P.S.</b> Five taps and a Medico project specialist calls you, then walks your unit with you. Every month a unit sits unbuilt is rent with no patients in it.</p>
    <div class="acts">{ask()}<a class="tel" href="tel:+16046444120">Prefer to talk? Call 604-644-4120</a></div>
  </div>
</section>

</main>

<footer class="foot">
  <div class="wrap">
    <img src="/assets/medico-logo.svg" width="273" height="57" alt="Medico Construction and Design">
    <span>Medico Construction &amp; Design. Licensed and insured. British Columbia.</span>
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
