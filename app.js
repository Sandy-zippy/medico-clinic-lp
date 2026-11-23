// Medico landing page. No dependencies. Jobs: capture click IDs, run the 6-step form, sticky mobile CTA.

// Lead destination: Apps Script web app (../leads-backend) -> Sheet + email + Monday. Set "TODO..." to disable sending.
const ENDPOINT = "https://script.google.com/macros/s/AKfycbx1g_WrKHgaOzbo_6C-hdKMbKo81CJuiCEla1V_m6XKL_YZjwhYQIjCXXA0zledpht5Jw/exec";

const TRACK = ["gclid", "wbraid", "gbraid", "fbclid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "utm_id"];
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

// 0. CTA test (Sandy 20 Nov: "test different CTAs"). Each visitor gets CTA a or b at random, kept for 90 days.
// The pick goes into the URL (?cta=) before attribution() reads it, so the Sheet's landing_url column shows which
// CTA every lead saw. ?cta=a|b in the link forces one (QA). Clarity and GA4 get it too.
const CTA = {
  a: { title: "Book your site assessment", submit: "Book My Site Assessment", btn: "Book My Site Assessment" },
  b: { title: "Will this space work as a clinic? Ask us.", submit: "Check My Space", btn: "Check My Space" }
};
const ctaKey = (function () {
  const q = new URLSearchParams(location.search); let k = (q.get("cta") || "").toLowerCase();
  if (!CTA[k]) { try { k = localStorage.getItem("medico_cta") || ""; } catch (e) {} }
  if (!CTA[k]) k = Math.random() < 0.5 ? "a" : "b";
  try { localStorage.setItem("medico_cta", k); } catch (e) {}
  if (q.get("cta") !== k) { q.set("cta", k); try { history.replaceState(null, "", location.pathname + "?" + q + location.hash); } catch (e) {} }
  return k;
})();

// 1. Click identifiers, last touch wins: a visit that arrives with any click id or UTM replaces what was stored,
// so a Google lead is never credited to an older Meta click (or the reverse). Kept 90 days in localStorage so a
// visitor who comes back later still carries the id that Google/Meta need to match the lead.
(function attribution() {
  const p = new URLSearchParams(location.search), DAY = 864e5;
  let stored = {};
  try { stored = JSON.parse(localStorage.getItem("medico_attrib") || "{}"); } catch (e) {}
  if (!stored.t || Date.now() - stored.t > 90 * DAY) stored = {};
  const fresh = TRACK.some(k => p.get(k));
  const out = fresh ? { landing_url: location.href, referrer: document.referrer, t: Date.now() }
    : { landing_url: stored.landing_url || location.href, referrer: stored.referrer || document.referrer, t: stored.t || Date.now() };
  for (const k of TRACK) { const v = fresh ? p.get(k) : stored[k]; if (v) out[k] = v; }
  try { localStorage.setItem("medico_attrib", JSON.stringify(out)); } catch (e) {}
  // 30 Oct: share the ad source with medicoconstruction.com, so a visitor who goes on to the main website's
  // form is still tagged (the WordPress snippet "Medico ad source" reads mc_src). Same rules as the site snippet.
  if (fresh) {
    const s = out.gclid || out.wbraid || out.gbraid || out.utm_source === "google" ? "Google Ads"
      : out.fbclid || /facebook|instagram|meta/.test(out.utm_source || "") ? "Meta ads" : out.utm_source || "Other";
    const c = { s, c: out.utm_campaign || "", k: out.utm_term || "", l: location.host + location.pathname + location.search.replace(/[?&](gclid|fbclid|wbraid|gbraid)=[^&]*/g, "").slice(0, 120), d: new Date().toISOString().slice(0, 10) };
    document.cookie = "mc_src=" + encodeURIComponent(JSON.stringify(c)) + ";domain=.medicoconstruction.com;path=/;max-age=7776000;SameSite=Lax;Secure";
  }
  if (typeof clarity === "function") {  // filter recordings by channel in Clarity
    clarity("set", "channel", out.gclid || out.wbraid || out.gbraid || out.utm_source === "google" ? "google"
      : out.fbclid || /facebook|instagram|meta/.test(out.utm_source || "") ? "meta" : out.utm_source || "direct");
    if (out.utm_id) clarity("set", "campaign_id", out.utm_id);
    clarity("set", "cta", ctaKey);
  }
  const form = $("#lead");
  for (const [k, v] of Object.entries(out)) {
    if (k === "t") continue;
    const i = document.createElement("input"); i.type = "hidden"; i.name = k; i.value = v; form.appendChild(i);
  }
})();

// 1b. Keyword variants. The Google ad groups link to ?v=medical|dental|optometry|pharmacy|vet (campaign spec v3).
// Each swaps the words a searcher typed into the hero, the section 5 headline and the cost question, shows a
// real project of that type, and pre-selects the clinic type. Unknown or missing ?v= stays medical.
const VARIANTS = {
  dental: { title: "Dental Office Construction in BC | Medico Construction & Design",
    eyebrow: "Dental clinic design + construction | British Columbia",
    h1: "Build your dental office with a team that specializes in healthcare.",
    img: ["/assets/img/hero-dental.webp", "", 1024, 683], alt: "Operatory at Chilliwack Dental, built by Medico",
    cap: "<b>Chilliwack Dental</b> · Chilliwack, BC · Dental clinic",
    diff: "A dental office isn't a standard commercial build.", faq1: "How much does it cost to build a dental office?", type: "Dental" },
  optometry: { title: "Optometry Clinic Construction in BC | Medico Construction & Design",
    eyebrow: "Optometry clinic design + construction | British Columbia",
    h1: "Build your optometry clinic with a team that specializes in healthcare.",
    img: ["/assets/img/hero-optometry.webp", "/assets/img/hero-optometry-960.webp 960w, /assets/img/hero-optometry.webp 1600w", 1600, 1066],
    alt: "Reception at White Rock Optometry, built by Medico", cap: "<b>White Rock Optometry</b> · White Rock, BC · Optometry clinic",
    diff: "An optometry clinic isn't a standard commercial build.", faq1: "How much does it cost to build an optometry clinic?", type: "Optometry / Eye care" },
  pharmacy: { title: "Pharmacy Construction in BC | Medico Construction & Design",
    eyebrow: "Pharmacy design + construction | British Columbia",
    h1: "Build your pharmacy with a team that specializes in healthcare.",
    img: ["/assets/img/hero-pharmacy.webp", "/assets/img/hero-pharmacy-960.webp 960w, /assets/img/hero-pharmacy.webp 1600w", 1600, 1066],
    alt: "Aisles at Optima Pharmacy, built by Medico", cap: "<b>Optima Pharmacy</b> · Surrey, BC · Pharmacy",
    diff: "A pharmacy isn't a standard commercial build.", faq1: "How much does it cost to build a pharmacy?", type: "Pharmacy" },
  vet: { title: "Veterinary Clinic Construction in BC | Medico Construction & Design",
    eyebrow: "Veterinary clinic design + construction | British Columbia",
    h1: "Build your veterinary clinic with a team that specializes in healthcare.",
    img: ["/assets/img/pf-6.webp", "", 800, 533], alt: "Coquitlam Animal Hospital interior, built by Medico",
    cap: "<b>Coquitlam Animal Hospital</b> · Coquitlam, BC · Veterinary",
    diff: "A veterinary clinic isn't a standard commercial build.", faq1: "How much does it cost to build a veterinary clinic?", type: "Veterinary" },
  // 4 Nov category expansion (Sandy). Z8000 wording is the live site's own claim (medicoconstruction.com/csa-z8000-standard).
  compounding: { title: "Compounding Pharmacy Construction in BC | Medico Construction & Design",
    eyebrow: "Compounding pharmacy + clean room construction | British Columbia",
    h1: "Build your compounding pharmacy with a team that specializes in healthcare.",
    img: ["/assets/img/hero-compounding.webp", "/assets/img/hero-compounding-960.webp 960w, /assets/img/hero-compounding.webp 1440w", 1440, 960],
    alt: "Dispensary at Humble Compounding Pharmacy, built by Medico", cap: "<b>Humble Compounding Pharmacy</b> · Langley, BC · 1,600 sq ft",
    diff: "A compounding pharmacy isn't a standard commercial build.", faq1: "How much does it cost to build a compounding pharmacy?", type: "Pharmacy" },
  surgical: { title: "Healthcare Facility Construction to CSA Z8000 in BC | Medico Construction & Design",
    eyebrow: "Surgical + specialty clinic construction to CSA Z8000 | British Columbia",
    h1: "Build your healthcare facility with a contractor that designs to CSA Z8000.",
    img: ["/assets/img/hero-surgical.webp", "/assets/img/hero-surgical-960.webp 960w, /assets/img/hero-surgical.webp 1440w", 1440, 960],
    alt: "Waiting room at Surrey Ophthalmic Surgeons, built by Medico", cap: "<b>Surrey Ophthalmic Surgeons</b> · White Rock, BC · Surgical clinic",
    diff: "A surgical or specialty facility isn't a standard commercial build.", faq1: "How much does it cost to build a surgical clinic?", type: "Specialist Clinic" },
  // No fertility project yet, so it keeps the default hero and caption (no IVF experience claimed).
  fertility: { title: "Fertility Clinic Construction in BC | Medico Construction & Design",
    eyebrow: "Fertility + IVF clinic construction | British Columbia",
    h1: "Build your fertility clinic with a team that specializes in healthcare.",
    diff: "A fertility clinic isn't a standard commercial build.", faq1: "How much does it cost to build a fertility clinic?", type: "Specialist Clinic" },
  // 23 Oct (go B): physio search ad group. No physio project photo cleared, so it keeps the default hero and caption.
  physio: { title: "Physiotherapy Clinic Construction in BC | Medico Construction & Design",
    eyebrow: "Physiotherapy clinic design + construction | British Columbia",
    h1: "Build your physiotherapy clinic with a team that specializes in healthcare.",
    diff: "A physiotherapy clinic isn't a standard commercial build.", faq1: "How much does it cost to build a physiotherapy clinic?", type: "Physiotherapy / Chiropractic" }
};
// Meta angle match (1 Oct 2026, Clarity: 57% of mobile visitors left on the first screen). Every Meta ad landed on the
// generic "Build your medical clinic" hero, whatever its promise. The ad id arrives as utm_content, so the hero
// continues the ad's own headline. ?a= sets an angle by hand. Claims only from the offer doc: site assessment
// (never "free"/"no-cost", Sandy 23 Nov), 100+ clinics. ($0 design fee offer retired by Sandy 9 Nov 2026.)
// 20 Nov (Sandy: "make sure the creative is matching with the lander"): one angle per Meta creative, so the first
// screen repeats the ad's own headline, names the projects the ad shows and shows a photo of the same type.
// own: the angle's eyebrow wins over a ?v= variant's. img/cap: hero photo for that ad. type: clinic type to pre-select.
const ANGLES = {
  space: { eyebrow: "Opening a medical clinic? | British Columbia", h1: "Don't sign the lease until we've walked the space.", own: 1, type: "Medical / Family Practice",
    offer: "<b>Get a site assessment.</b> We check plumbing, barrier-free entry, room count and permits before you commit." },
  oneroof: { eyebrow: "Opening a medical clinic? | British Columbia", h1: "Design, permits and build. One team, one roof.", own: 1,
    offer: "<b>Start with a site assessment.</b> Then one team designs it, gets the permits and builds it, like Harvard Place Medical Clinic.",
    img: ["/assets/img/exp-1.webp", "", 900, 600], alt: "Reception and waiting area at Harvard Place Medical Clinic, built by Medico",
    cap: "<b>Harvard Place Medical Clinic</b> · Vancouver, BC · Medical clinic", type: "Medical / Family Practice" },
  dentalclinic: { eyebrow: "Building out a dental office? | British Columbia", h1: "Any contractor can build an office. We build clinics.", own: 1,
    offer: "<b>Plumbing, power and imaging planned around every op.</b> Start with a site assessment of your space. No obligation.", img: ["/assets/img/ad-sp.webp", "/assets/img/ad-sp-960.webp 960w, /assets/img/ad-sp.webp 1600w", 1600, 1066], alt: "Reception at Smile Plus Dentistry, designed and built by Medico", cap: "<b>Smile Plus Dentistry</b> · Surrey, BC · Dental clinic", type: "Dental" },
  everyop: { eyebrow: "Building out a dental office? | British Columbia", h1: "Every op planned: plumbing, power and imaging.", own: 1,
    offer: "<b>Water and vacuum at every chair, power for the equipment, room for imaging.</b> Start with a site assessment. No obligation.", img: ["/assets/img/ad-sp.webp", "/assets/img/ad-sp-960.webp 960w, /assets/img/ad-sp.webp 1600w", 1600, 1066], alt: "Reception at Smile Plus Dentistry, designed and built by Medico", cap: "<b>Smile Plus Dentistry</b> · Surrey, BC · Dental clinic", type: "Dental" },
  firstvet: { eyebrow: "Building a vet clinic? | British Columbia", h1: "Is this your contractor's first animal hospital? With Medico, it isn't.", own: 1,
    offer: "<b>We've built animal hospitals across BC</b>, including Woodland Veterinary Clinic. Start with a site assessment. No obligation.",
    img: ["/assets/img/hero-woodland-front.webp", "/assets/img/hero-woodland-front-960.webp 960w, /assets/img/hero-woodland-front.webp 1600w", 1600, 1067],
    alt: "Woodland Veterinary Clinic storefront, Vancouver, built by Medico", pos: "50% 0%", cap: "<b>Woodland Veterinary Clinic</b> · Vancouver, BC · Veterinary", type: "Veterinary" },
  vetrooms: { eyebrow: "For veterinarians | British Columbia", h1: "Every room has its own rules. We know them.", own: 1,
    offer: "<b>Kennels, treatment, procedures and imaging</b> each need their own plumbing, electrical and layout. Start with a site assessment. No obligation.", type: "Veterinary" },
  fourvet: { eyebrow: "For veterinarians | British Columbia", h1: "Four animal hospitals. One contractor.", own: 1,
    offer: "<b>Coquitlam Animal Hospital, Paws on Fraser, Marine &amp; Fraser Veterinary Clinic, EPIC Veterinary Hospital.</b> Your clinic won't be our first. Start with a site assessment. No obligation.", type: "Veterinary" },
  vetkennels: { eyebrow: "For veterinarians | British Columbia", h1: "A vet clinic isn't an office with kennels added.", own: 1,
    offer: "<b>We plan it around how you treat patients:</b> procedure lighting, kennel banks, space around the table. Start with a site assessment. No obligation.", type: "Veterinary" },
  catcondo: { eyebrow: "For veterinarians | British Columbia", h1: "Yes, we've built a cat condo.", own: 1,
    offer: "<b>Custom millwork for the things only animal hospitals need.</b> Start with a site assessment of your space. No obligation.",
    img: ["/assets/img/ad-epic15.webp", "/assets/img/ad-epic15-960.webp 960w, /assets/img/ad-epic15.webp 1600w", 1600, 1066], alt: "Cat condo millwork at EPIC Veterinary Hospital, built by Medico", cap: "<b>EPIC Veterinary Hospital</b> \u00b7 Richmond, BC \u00b7 Veterinary", type: "Veterinary" },
  // 24 Nov 2026 (Sandy: every creative matches its lander): one angle per round-2 static (261123_*), headline = the
  // ad's own headline, photo = the same Medico clinic the ad shows. V2a and V2b share v_number (CTA test is in the ad).
  d_space: { eyebrow: "Dentists looking at a new space | British Columbia", h1: "The space looks perfect. Will it work for your operatories?", own: 1,
    offer: "<b>Find out before you sign.</b> A Medico project specialist looks at your space and flags what could change your layout, cost or opening plans. No obligation.",
    img: ["/assets/img/ad-sp.webp", "/assets/img/ad-sp-960.webp 960w, /assets/img/ad-sp.webp 1600w", 1600, 1066], alt: "Reception at Smile Plus Dentistry, designed and built by Medico", cap: "<b>Smile Plus Dentistry</b> \u00b7 Surrey, BC \u00b7 Dental clinic", type: "Dental" },
  d_equip: { eyebrow: "Dentists planning a build out | British Columbia", h1: "Pick your equipment, then plan the rooms.", own: 1,
    offer: "<b>Room layouts built around your workflow and equipment</b>, with plumbing and electrical planned around treatment requirements. Talk it through with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-sp.webp", "/assets/img/ad-sp-960.webp 960w, /assets/img/ad-sp.webp 1600w", 1600, 1066], alt: "Reception at Smile Plus Dentistry, designed and built by Medico", cap: "<b>Smile Plus Dentistry</b> \u00b7 Surrey, BC \u00b7 Dental clinic", type: "Dental" },
  d_quote: { eyebrow: "Dentists comparing contractor quotes | British Columbia", h1: "Will this quote still hold halfway through the build?", own: 1,
    offer: "<b>With Medico, your quote doesn't move on you mid-project.</b> We lock in fixed pricing with our suppliers upfront. Talk through your space and plans with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-sp.webp", "/assets/img/ad-sp-960.webp 960w, /assets/img/ad-sp.webp 1600w", 1600, 1066], alt: "Reception at Smile Plus Dentistry, designed and built by Medico", cap: "<b>Smile Plus Dentistry</b> \u00b7 Surrey, BC \u00b7 Dental clinic", type: "Dental" },
  d_faq: { eyebrow: "For dentists | British Columbia", h1: "Have you built a dental clinic? Yes: Smile Plus Dentistry.", own: 1,
    offer: "<b>2,840 sq. ft., designed and built by Medico.</b> We specialize in healthcare, with 100+ clinics built. Talk through your space and plans with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-sp.webp", "/assets/img/ad-sp-960.webp 960w, /assets/img/ad-sp.webp 1600w", 1600, 1066], alt: "Reception at Smile Plus Dentistry, designed and built by Medico", cap: "<b>Smile Plus Dentistry</b> \u00b7 Surrey, BC \u00b7 Dental clinic", type: "Dental" },
  m_lease: { eyebrow: "Doctors negotiating a clinic lease | British Columbia", h1: "Negotiating a lease? Bring Medico in before you sign.", own: 1,
    offer: "<b>We can help identify issues</b> that could affect layout, construction cost or your opening timeline. Talk through your space and plans with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-cs02.webp", "/assets/img/ad-cs02-960.webp 960w, /assets/img/ad-cs02.webp 1600w", 1600, 1066], alt: "Reception at Cornerstone Pediatric, built by Medico", cap: "<b>Cornerstone Pediatric</b> \u00b7 Langley, BC \u00b7 Medical clinic", type: "Medical / Family Practice" },
  m_privacy: { eyebrow: "Family doctors opening a clinic | British Columbia", h1: "Will patients hear the next exam room?", own: 1,
    offer: "<b>Exam rooms designed with privacy in mind</b>, before construction begins. Get a site assessment: a Medico project specialist flags what could change your layout, cost or opening plans. No obligation.",
    img: ["/assets/img/ad-cs09.webp", "/assets/img/ad-cs09-960.webp 960w, /assets/img/ad-cs09.webp 1600w", 1600, 1066], alt: "Exam room at Cornerstone Pediatric, built by Medico", cap: "<b>Cornerstone Pediatric</b> \u00b7 Langley, BC \u00b7 Medical clinic", type: "Medical / Family Practice" },
  m_small: { eyebrow: "Doctors with under 1,500 sq. ft. | British Columbia", h1: "Can 1,000 sq. ft. really fit a clinic?", own: 1,
    offer: "<b>Cornerstone Pediatric is a 1,000 sq. ft. clinic</b>, planned for patient flow from check-in through consultation. Get a site assessment of your space. No obligation.",
    img: ["/assets/img/ad-cs01.webp", "/assets/img/ad-cs01-960.webp 960w, /assets/img/ad-cs01.webp 1600w", 1600, 1066], alt: "Reception at Cornerstone Pediatric, a 1,000 sq. ft. clinic built by Medico", cap: "<b>Cornerstone Pediatric</b> \u00b7 Langley, BC \u00b7 Medical clinic", type: "Medical / Family Practice" },
  m_layout: { eyebrow: "Doctors planning a clinic | British Columbia", h1: "There's no best clinic layout. There's the one that fits.", own: 1,
    offer: "<b>Your patients, your staff, your space.</b> We design it with you, then build it. Talk through your plans with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-cs03.webp", "/assets/img/ad-cs03-960.webp 960w, /assets/img/ad-cs03.webp 1600w", 1600, 1066], alt: "Reception at Cornerstone Pediatric, built by Medico", cap: "<b>Cornerstone Pediatric</b> \u00b7 Langley, BC \u00b7 Medical clinic", type: "Medical / Family Practice" },
  o_lane: { eyebrow: "Optometrists setting up exam lanes | British Columbia", h1: "How long does your exam lane need to be?", own: 1,
    offer: "<b>It depends on your space and your equipment.</b> We assess the space with you before you commit. Talk it through with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-mo01.webp", "/assets/img/ad-mo01-960.webp 960w, /assets/img/ad-mo01.webp 1600w", 1600, 1066], alt: "Inside Mishe Optometry, built by Medico", cap: "<b>Mishe Optometry</b> \u00b7 Surrey, BC \u00b7 Optometry clinic", type: "Optometry / Eye care" },
  o_quote: { eyebrow: "For optometrists | British Columbia", h1: "Don't pick your contractor by the lowest quote.", own: 1,
    offer: "<b>Start with one who has built optometry clinics before. Medico has</b>, including Mishe Optometry and White Rock Optometry. Talk through your space with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-wr07.webp", "/assets/img/ad-wr07-960.webp 960w, /assets/img/ad-wr07.webp 1600w", 1600, 1066], alt: "Frame display cases at White Rock Optometry, built by Medico", cap: "<b>White Rock Optometry</b> \u00b7 White Rock, BC \u00b7 Optometry clinic", type: "Optometry / Eye care" },
  o_tworoads: { eyebrow: "Optometrists planning a build out | British Columbia", h1: "Two ways to build out an optometry clinic.", own: 1,
    offer: "<b>Coordinate a designer, an engineer and a contractor yourself, or have Medico design it, handle the permits and build it.</b> Get a site assessment of your space. No obligation.",
    img: ["/assets/img/ad-mo05.webp", "/assets/img/ad-mo05-960.webp 960w, /assets/img/ad-mo05.webp 1600w", 1600, 1066], alt: "Frame display at Mishe Optometry, built by Medico", cap: "<b>Mishe Optometry</b> \u00b7 Surrey, BC \u00b7 Optometry clinic", type: "Optometry / Eye care" },
  v_space: { eyebrow: "Vets looking at a space | British Columbia", h1: "Will this space work as a vet hospital?", own: 1,
    offer: "<b>Before you commit to it, Medico can look at the layout, plumbing and electrical with you.</b> Talk through your space with a Medico project specialist. No obligation.",
    img: ["/assets/img/ad-ca04.webp", "/assets/img/ad-ca04-960.webp 960w, /assets/img/ad-ca04.webp 1600w", 1600, 1066], alt: "Inside Coquitlam Animal Hospital, built by Medico", cap: "<b>Coquitlam Animal Hospital</b> \u00b7 Coquitlam, BC \u00b7 Veterinary", type: "Veterinary" },
  v_number: { eyebrow: "Vets planning a clinic or hospital | British Columbia", h1: "Know your number before you start.", own: 1,
    offer: "<b>Whatever your number is, we've likely already worked with it.</b> We'll give you a real one, not a guess, and fixed supplier pricing keeps it steady. No obligation.",
    img: ["/assets/img/ad-ca03.webp", "/assets/img/ad-ca03-960.webp 960w, /assets/img/ad-ca03.webp 1600w", 1600, 1066], alt: "Reception at Coquitlam Animal Hospital, built by Medico", cap: "<b>Coquitlam Animal Hospital</b> \u00b7 Coquitlam, BC \u00b7 Veterinary", type: "Veterinary" },
  v_quote: { eyebrow: "Vets getting contractor quotes | British Columbia", h1: "Does your quote cover what a vet hospital needs?", own: 1,
    offer: "<b>Imaging and specialized-room requirements, plumbing and electrical planned around treatment.</b> Medico accounts for them early. No obligation.",
    img: ["/assets/img/ad-ca04.webp", "/assets/img/ad-ca04-960.webp 960w, /assets/img/ad-ca04.webp 1600w", 1600, 1066], alt: "Inside Coquitlam Animal Hospital, built by Medico", cap: "<b>Coquitlam Animal Hospital</b> \u00b7 Coquitlam, BC \u00b7 Veterinary", type: "Veterinary" },
  v_size: { eyebrow: "Vets planning a new clinic | British Columbia", h1: "How big should a vet clinic be?", own: 1,
    offer: "<b>Big enough for your exam rooms, treatment rooms and staff rooms.</b> Medico lays it out around your workflow from the first plan. Get a site assessment. No obligation.",
    img: ["/assets/img/ad-ca05.webp", "/assets/img/ad-ca05-960.webp 960w, /assets/img/ad-ca05.webp 1600w", 1600, 1066], alt: "Inside Coquitlam Animal Hospital, built by Medico", cap: "<b>Coquitlam Animal Hospital</b> \u00b7 Coquitlam, BC \u00b7 Veterinary", type: "Veterinary" },
  expand: { eyebrow: "Clinic expansion + renovation | British Columbia", h1: "Expanding your clinic? Plan it around your patients.",
    offer: "<b>Adding rooms or a second location?</b> Start with a site assessment. No obligation." },
  design0: { eyebrow: "Clinic design + construction | British Columbia", h1: "Design and build your clinic with one team.",
    offer: "<b>Layout, permit drawings and construction, planned together.</b> Start with a site assessment of your space. No obligation." },
  newclinic: { eyebrow: "Opening a new clinic? | British Columbia", h1: "Opening a new clinic? Get the plan right before you build.",
    offer: "<b>Before you sign, approve a layout or start construction:</b> get a site assessment. No obligation." },
  plan: { eyebrow: "Still planning your clinic build? | British Columbia", h1: "Know what your clinic involves before you build.",
    offer: "<b>Not sure of the budget yet?</b> Start with a site assessment of the space, your clinic type and equipment. No obligation." }
};
const DESIGN_HERO = {
  medical: ["Medical clinic design and build, by one team.", "Medical Clinic Design + Build in BC | Medico Construction & Design"],
  dental: ["Dental office design and build, by one team.", "Dental Office Design + Build in BC | Medico Construction & Design"],
  pharmacy: ["Pharmacy and vet clinic design, built by the same team.", "Pharmacy + Vet Clinic Design in BC | Medico Construction & Design"],
  vet: ["Vet clinic design and build, by one team.", "Veterinary Clinic Design + Build in BC | Medico Construction & Design"]
};
const AD_ANGLE = { "6920259109079": "space", "6920259104679": "expand", "6920259118079": "design0", "6920255191679": "design0",
  "6920252908279": "newclinic", "6920246652279": "newclinic",
  // 4 Oct province split (cold_bc / cold_ab ad sets), same creatives as above
  "6921084383679": "space", "6921084405079": "space", "6921084385079": "expand", "6921084408279": "expand",
  "6921084388079": "design0", "6921084409079": "design0", "6921084391879": "newclinic", "6921084410679": "newclinic",
  // 7 Oct Ameya tests
  "6921574931679": "newclinic", "6921575292079": "plan",
  "6921981111079": "plan", "6921981128879": "space",
  // 10 Oct format-split campaign (medico_lead_format)
  "6922449404479": "space", "6922449406479": "newclinic", "6922449427079": "space", "6922449446479": "newclinic", "6922449462679": "plan",
  // 20 Oct Ameya creatives (opening/expanding); the 2 drawings ads keep the default hero
  "6924515235479": "newclinic", "6924515274479": "newclinic", "6924515310879": "newclinic", "6924515391679": "newclinic", "6924515495879": "newclinic", "6924515554879": "newclinic" };
(function variant() {
  // Google keyword pages (/g/<slug>/, built by tools/gpages.py) carry their own title, eyebrow and h1 in the HTML.
  const G = document.documentElement.dataset.gv;
  const key = (G || new URLSearchParams(location.search).get("v") || "").toLowerCase();
  const v = VARIANTS[key]; if (!v) return;
  if (!G) document.title = v.title;
  document.documentElement.dataset.variant = key;
  $("#pagev").value = key;
  for (const k of G ? ["diff", "faq1"] : ["eyebrow", "h1", "diff", "faq1"]) { const el = $(`[data-v="${k}"]`); if (el) el.textContent = v[k]; }
  if (!v.img) { const t = $(`input[name="clinic_type"][value="${v.type}"]`); if (t) t.checked = true; return; }
  $('[data-v="cap"]').innerHTML = v.cap;
  const img = $('[data-v="img"]');
  img.src = v.img[0]; if (v.img[1]) img.srcset = v.img[1]; else img.removeAttribute("srcset");
  img.width = v.img[2]; img.height = v.img[3]; img.alt = v.alt;
  const t = $(`input[name="clinic_type"][value="${v.type}"]`); if (t) t.checked = true;
})();

// Runs after variant(). A Meta angle (from utm_content) never overrides a keyword variant (?v=), but an explicit ?a=
// does (22 Oct: the Clinic Design search campaign sends ?v=dental&a=design0, so designer-shoppers read "design is $0"
// over the dental photo and clinic type); the variant keeps its more specific eyebrow.
(function angle() {
  if (document.documentElement.dataset.gv) return;
  const q = new URLSearchParams(location.search), a = ANGLES[(q.get("a") || AD_ANGLE[q.get("utm_content")] || "").toLowerCase()];
  if (!a || (q.get("v") && !q.get("a"))) return;
  const vk = (q.get("v") || "").toLowerCase();
  if (!VARIANTS[vk] || a.own) $('[data-v="eyebrow"]').textContent = a.eyebrow;
  if (a.img) {
    const img = $('[data-v="img"]'); img.src = a.img[0];
    if (a.img[1]) img.srcset = a.img[1]; else img.removeAttribute("srcset");
    img.width = a.img[2]; img.height = a.img[3]; img.alt = a.alt; $('[data-v="cap"]').innerHTML = a.cap;
    if (a.pos) img.style.objectPosition = a.pos;  // keep the clinic's sign in frame
  }
  if (a.type) { const t = $(`input[name="clinic_type"][value="${a.type}"]`); if (t) t.checked = true; }
  // 16 Nov: design searches ("pharmacy design", "dental clinic interior design") read the generic design0 hero and a
  // "Construction" title, and Google scored their landing page below average. Echo the searched words instead.
  const D = a === ANGLES.design0 && DESIGN_HERO[vk];
  $('[data-v="h1"]').textContent = D ? D[0] : a.h1; if (D) document.title = D[1];
  $('[data-v="offer"]').innerHTML = a.offer;
})();

// 2. The form. One question per step; answers live in the real inputs, so Back never clears anything.
(function form() {
  const form = $("#lead"), bar = $("#fbar"), count = $("#fcount");
  // 20 Nov: a dental or vet ad already told us the clinic type (pre-selected above), so that question is skipped:
  // 6 steps instead of 7. The answer is still sent (hidden fieldsets stay in the form data).
  const steps = $$(".step", form).filter(s => !($('input[name="clinic_type"]', s) && $('input[name="clinic_type"]:checked', s)));
  $$(".step", form).forEach(s => { if (!steps.includes(s)) s.hidden = true; });
  const C = CTA[ctaKey];
  $(".f-title").textContent = C.title;
  $$("a.btn[data-goform]:not(.ghost)").forEach(b => { b.textContent = C.btn; });
  const back = $("#fback"), next = $("#fnext"), msg = $("#fmsg");
  let i = 0;

  const t0 = Date.now();
  const emailOk = v => /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v.trim());
  // North American numbers only (BC clinics): 10 digits after an optional leading 1, area code and
  // exchange can't start with 0 or 1. Stops "1234567890" style junk.
  // Also rejects one repeated digit and toll-free area codes (1 Oct: "8888888888" got through as an A lead).
  const phoneOk = v => { const d = v.replace(/\D/g, "").replace(/^1(?=\d{10}$)/, "");
    return /^[2-9]\d{2}[2-9]\d{6}$/.test(d) && !/^(\d)\1+$/.test(d) && !/^8(00|33|44|55|66|77|88)/.test(d); };
  function fieldOk(el) {
    if (!el.required) return true;
    if (el.type === "email") return emailOk(el.value);
    if (el.type === "tel") return phoneOk(el.value);
    return el.value.trim() !== "";
  }
  function stepOk(s, show) {
    let first = null;
    // Radio groups: a whole-step question (the step shows the error) or a group inside a field (the field does).
    const groups = [...new Set($$("input[type=radio]", s).map(r => r.name))];
    for (const name of groups) {
      const ok = $$(`input[name="${name}"]`, s).some(r => r.checked);
      const holder = $(`input[name="${name}"]`, s).closest(".field") || s;
      if (show) holder.classList.toggle("bad", !ok);
      if (!ok && !first) first = $(`input[name="${name}"]`, s);
    }
    for (const el of $$("input:not([type=radio]),textarea", s)) {
      const ok = fieldOk(el);
      if (show) el.closest(".field").classList.toggle("bad", !ok);
      if (!ok && !first) first = el;
    }
    if (show && first) first.focus();
    return !first;
  }
  function go(n) {
    i = Math.max(0, Math.min(steps.length - 1, n));
    steps.forEach((s, k) => { s.hidden = k !== i; s.classList.remove("in", "bad"); });
    const s = steps[i];
    void s.offsetWidth; s.classList.add("in");
    count.textContent = `Step ${i + 1} of ${steps.length}`;
    bar.style.width = `${((i + 1) / steps.length) * 100}%`;
    back.hidden = i === 0;
    const last = i === steps.length - 1;
    next.textContent = last ? C.submit : "Continue";
    next.type = last ? "submit" : "button";
    // One-tap steps have no Continue: tapping an answer moves on (Sandy, 24 Sep). The button only shows
    // on the contact step, or when the out-of-area note needs reading.
    next.hidden = tapOnly(s) && !outsidePicked(s);
    // Phones: a taller step can start above the screen after an auto-advance. Bring the card top back.
    const card = $("#start"), r = card.getBoundingClientRect();
    if (n > 0 && r.top < 0) scrollTo({ top: scrollY + r.top - 72, behavior: "smooth" });
    // Form funnel (6 Oct CRO audit: form-start and drop-off step were unmeasured). Once per step reached;
    // step 2 = answered the first question = form started. Clarity filters sessions by it, GA4 counts it.
    if (n > 0 && !reached.has(i)) {
      reached.add(i);
      if (typeof clarity === "function") clarity("event", `form_step_${i + 1}`);
      if (typeof gtag === "function") gtag("event", "form_progress", { send_to: "G-HSJ06CG134", step: i + 1, cta: ctaKey });
    }
  }
  const reached = new Set();
  const tapOnly = s => !$("input:not([type=radio]),textarea", s);
  const outsidePicked = s => !!$('input[value="Outside BC"]:checked', s);

  form.addEventListener("change", e => {
    if (e.target.type !== "radio") return;
    (e.target.closest(".field") || e.target.closest(".step")).classList.remove("bad");
    if (e.target.name === "region") { $("#outside").hidden = !outsidePicked(steps[i]); next.hidden = !outsidePicked(steps[i]); }
  });

  // Auto-advance on a tap or click of an answer (also re-tapping the answer already chosen after Back).
  // Keyboard users move with arrows and press Enter, so arrow keys never jump steps.
  let advancing = null;
  form.addEventListener("click", e => {
    const opt = e.target.closest(".opt"); const s = steps[i];
    if (!opt || !tapOnly(s) || i === steps.length - 1) return;
    if (opt.querySelector('input[value="Outside BC"]')) return;
    clearTimeout(advancing);
    advancing = setTimeout(() => { if (stepOk(s, false)) go(i + 1); }, 260);
  });

  // Lead grade for the caller's pre-call briefing (never shown to the visitor, never used to block).
  // A: in area, has or is negotiating a space, opening within 12 months, decision-maker.
  // C: outside BC, or no space + no date, or role Other. B: everything else.
  function grade(d) {
    const inArea = d.region && d.region !== "Outside BC";
    const space = ["I already have a location", "I'm negotiating a lease or purchase"].includes(d.space_stage);
    const soon = ["Within 3 months", "3-6 months", "6-12 months"].includes(d.opening);
    const vague = d.space_stage === "I haven't started looking yet" && ["12+ months", "Not sure yet"].includes(d.opening);
    const decider = d.role && d.role !== "Other";
    if (!inArea || vague || d.role === "Other") return "C";
    if (space && soon && decider) return "A";
    return "B";
  }
  // Inline validation on blur, and live once a field has been flagged.
  form.addEventListener("focusout", e => {
    const f = e.target.closest?.(".field"); if (!f || !e.target.value) return;
    f.classList.toggle("bad", !fieldOk(e.target));
  });
  form.addEventListener("input", e => {
    const f = e.target.closest?.(".field"); if (f && f.classList.contains("bad")) f.classList.toggle("bad", !fieldOk(e.target));
  });
  form.addEventListener("keydown", e => {
    if (e.key === "Enter" && e.target.tagName === "INPUT" && i < steps.length - 1) { e.preventDefault(); next.click(); }
  });
  next.addEventListener("click", e => {
    if (next.type === "submit") return;
    // go() flips this button to type=submit on the last step. Without preventDefault the SAME click then
    // submits the empty contact step and paints every field red on arrival.
    e.preventDefault();
    if (stepOk(steps[i], true)) go(i + 1);
  });
  back.addEventListener("click", () => go(i - 1));

  form.addEventListener("submit", async e => {
    e.preventDefault();
    msg.textContent = "";
    if (!stepOk(steps[i], true)) return;
    if (form.website.value) return; // honeypot
    const data = Object.fromEntries(new FormData(form).entries());
    delete data.website;
    data.submitted_at = new Date().toISOString();
    data.seconds_on_form = Math.round((Date.now() - t0) / 1000); // under ~8 s is almost always a bot
    data.lead_grade = grade(data);
    // Meta dedup + match keys for the server-side Lead event. event_id is shared with the browser fbq Lead below.
    data.event_id = "lead_" + data.submitted_at;
    const ck = n => (document.cookie.match("(?:^|; )" + n + "=([^;]*)") || [])[1] || "";
    data.fbp = ck("_fbp");
    data.gcl_aw = ck("_gcl_aw"); // Google's own click cookie: survives when the gclid URL param is gone
    data.fbc = ck("_fbc") || (data.fbclid ? `fb.1.${Date.now()}.${data.fbclid}` : "");
    data.user_agent = navigator.userAgent;
    form.dataset.grade = data.lead_grade; // exposed for the QA test only
    // The thank-you page reads these to greet the visitor by name and echo their project back.
    // sessionStorage, never the URL: a name in a URL leaks into analytics and referrers.
    const thanks = { name: (data.full_name || "").trim().split(/\s+/)[0], project_type: data.project_type,
      clinic_type: data.clinic_type, size: data.size, opening: data.opening, region: data.region,
      preview: ENDPOINT.startsWith("TODO") };
    // The browser Lead also fires on the thank-you page (same event_id, Meta dedups). 6 Oct audit: the redirect below
    // left the landing page within ~1 s and cancelled the pixel request on about half the leads, so the browser
    // event (the one carrying IP, cookies and the click id natively) was missing. Google-click leads never get it.
    const fromGoogle = (data.gclid || data.wbraid || data.gbraid || data.utm_source === "google") && !data.fbclid;
    thanks.meta_eid = fromGoogle ? "" : data.event_id;
    // Advanced matching for the thank-you Lead (23 Oct audit: Meta credited ~55% of real leads). Hashed here, so only
    // SHA-256 values sit in sessionStorage; the pixel accepts pre-hashed keys.
    if (thanks.meta_eid) try {
      const sha = async s => s ? [...new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)))].map(b => b.toString(16).padStart(2, "0")).join("") : "";
      const ph = (data.phone || "").replace(/\D/g, ""), nm = (data.full_name || "").trim().toLowerCase().split(/\s+/);
      thanks.am = { em: await sha((data.email || "").trim().toLowerCase()), ph: await sha(ph.length === 10 ? "1" + ph : ph),
        fn: await sha(nm[0] || ""), ln: await sha(nm.length > 1 ? nm[nm.length - 1] : ""), country: await sha("ca") };
      Object.keys(thanks.am).forEach(k => thanks.am[k] || delete thanks.am[k]);
    } catch (e) {}
    const toThanks = () => { try { sessionStorage.setItem("medico_thanks", JSON.stringify(thanks)); } catch (e) {} location.href = "/thank-you.html"; };
    // Not connected yet (Sandy: form destination comes last). Nothing is sent; the thank-you page says so.
    if (ENDPOINT.startsWith("TODO")) { toThanks(); return; }
    next.disabled = true; next.textContent = "Sending";
    try {
      const r = await fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data) });
      // text/plain skips the CORS preflight Apps Script can't answer; the script parses the JSON body itself.
      const res = r.ok ? await r.json() : {};
      if (!res.success) throw new Error(r.status);
      // Junk the backend caught (fake name/number): saved for review, but never fed to Google or Meta as a conversion.
      if (res.junk) { thanks.meta_eid = ""; delete thanks.am; toThanks(); return; }
      // Google Ads lead: fires only after the destination accepted the lead, never on the thank-you pageload
      // (refreshes, direct visits and bots would count). Enhanced conversions: gtag hashes email + phone itself.
      // transaction_id = submit time, so a double submit counts once.
      // Meta's browser Lead fires ONCE, on the thank-you page (meta_eid above; never for Google-click leads).
      // 10 Oct: firing it here as well made Meta count the 6 Oct lead twice: two browser events with one
      // event_id are not deduplicated against each other, only browser against server.
      if (typeof clarity === "function") { clarity("event", "lead"); clarity("set", "lead_grade", data.lead_grade); }
      let went = false; const go2 = () => { if (!went) { went = true; toThanks(); } };
      if (typeof gtag === "function") {
        const digits = data.phone.replace(/\D/g, "").replace(/^1/, "");
        gtag("set", "user_data", { email: data.email.trim().toLowerCase(), phone_number: "+1" + digits });
        // 14 Oct: Google missed 1 lead in 4 (8 Oct lead had a gclid, no conversion). beacon keeps the hit alive through
        // the redirect; the thank-you page re-sends it with the same transaction_id as a backstop (Google counts it once).
        thanks.gads_tid = data.submitted_at;
        gtag("event", "conversion", { send_to: "AW-716871487/0XCcCLGxyIsdEL-u6tUC", transaction_id: data.submitted_at, transport_type: "beacon", event_callback: go2 });
        gtag("event", "generate_lead", { send_to: "G-HSJ06CG134", lead_grade: data.lead_grade, clinic_type: data.clinic_type, region: data.region, cta: ctaKey, transport_type: "beacon" });
      }
      setTimeout(go2, 2000); // ad blockers never call back
    } catch (err) {
      msg.textContent = "That didn't send. Please try again, or call 604-644-4120.";
      next.disabled = false; next.textContent = C.submit;
    }
  });

  // Every contextual CTA scrolls to the form and focuses the current question.
  $$("[data-goform]").forEach(a => a.addEventListener("click", e => {
    e.preventDefault();
    $("#start").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    setTimeout(() => $("input,button", steps[i])?.focus({ preventScroll: true }), 500);
  }));

  go(0);
})();

// 3. Sticky mobile CTA: appears once the form has scrolled out of view, hides while the form is on screen.
(function sticky() {
  const bar = $("#stick"), target = $("#start");
  if (!bar || !("IntersectionObserver" in window)) return;
  // Shown once the form is above the screen; hidden again while the final call-to-action (which has the
  // same button) is on screen, so the two never stack.
  let pastForm = false, finalOn = false;
  const sync = () => { const show = pastForm && !finalOn; bar.classList.toggle("on", show); document.body.classList.toggle("has-stick", show); };
  new IntersectionObserver(([e]) => { pastForm = !e.isIntersecting && e.boundingClientRect.top < 0; sync(); }).observe(target);
  const fin = $(".final"); if (fin) new IntersectionObserver(([e]) => { finalOn = e.isIntersecting; sync(); }).observe(fin);
})();
