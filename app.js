// Medico landing page. No dependencies. Jobs: capture click IDs, run the 6-step form, sticky mobile CTA.

// Lead destination is connected LAST, after design sign-off (Sandy, 24 Sep). Until then the form refuses to send.
const ENDPOINT = "TODO_LEAD_WEBHOOK";

const TRACK = ["gclid", "wbraid", "gbraid", "fbclid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

// 1. Click identifiers. URL wins; sessionStorage keeps them if the visitor navigates back.
(function attribution() {
  const p = new URLSearchParams(location.search);
  let stored = {};
  try { stored = JSON.parse(sessionStorage.getItem("medico_attrib") || "{}"); } catch (e) {}
  const out = { landing_url: stored.landing_url || location.href, referrer: stored.referrer || document.referrer };
  for (const k of TRACK) { const v = p.get(k) || stored[k]; if (v) out[k] = v; }
  try { sessionStorage.setItem("medico_attrib", JSON.stringify(out)); } catch (e) {}
  const form = $("#lead");
  for (const [k, v] of Object.entries(out)) {
    const i = document.createElement("input"); i.type = "hidden"; i.name = k; i.value = v; form.appendChild(i);
  }
})();

// 1b. Keyword variants. The Google ad groups link to ?v=medical|dental|optometry|pharmacy (campaign spec v3).
// Each swaps the words a searcher typed into the hero, the section 5 headline and the cost question, shows a
// real project of that type, and pre-selects the clinic type. Unknown or missing ?v= stays medical.
const VARIANTS = {
  dental: { title: "Dental Office Construction in BC & Alberta | Medico Construction & Design",
    eyebrow: "Dental clinic design + construction | BC & Alberta",
    h1: "Build your dental office with a team that specializes in healthcare.",
    img: ["assets/img/hero-dental.webp", "", 1024, 683], alt: "Operatory at Chilliwack Dental, built by Medico",
    cap: "<b>Chilliwack Dental</b> · Chilliwack, BC · Dental clinic",
    diff: "A dental office isn't a standard commercial build.", faq1: "How much does it cost to build a dental office?", type: "Dental" },
  optometry: { title: "Optometry Clinic Construction in BC & Alberta | Medico Construction & Design",
    eyebrow: "Optometry clinic design + construction | BC & Alberta",
    h1: "Build your optometry clinic with a team that specializes in healthcare.",
    img: ["assets/img/hero-optometry.webp", "assets/img/hero-optometry-960.webp 960w, assets/img/hero-optometry.webp 1600w", 1600, 1066],
    alt: "Reception at White Rock Optometry, built by Medico", cap: "<b>White Rock Optometry</b> · White Rock, BC · Optometry clinic",
    diff: "An optometry clinic isn't a standard commercial build.", faq1: "How much does it cost to build an optometry clinic?", type: "Optometry / Eye care" },
  pharmacy: { title: "Pharmacy Construction in BC & Alberta | Medico Construction & Design",
    eyebrow: "Pharmacy design + construction | BC & Alberta",
    h1: "Build your pharmacy with a team that specializes in healthcare.",
    img: ["assets/img/hero-pharmacy.webp", "assets/img/hero-pharmacy-960.webp 960w, assets/img/hero-pharmacy.webp 1600w", 1600, 1066],
    alt: "Aisles at Optima Pharmacy, built by Medico", cap: "<b>Optima Pharmacy</b> · Surrey, BC · Pharmacy",
    diff: "A pharmacy isn't a standard commercial build.", faq1: "How much does it cost to build a pharmacy?", type: "Pharmacy" }
};
(function variant() {
  const key = (new URLSearchParams(location.search).get("v") || "").toLowerCase();
  const v = VARIANTS[key]; if (!v) return;
  document.title = v.title;
  document.documentElement.dataset.variant = key;
  $("#pagev").value = key;
  for (const k of ["eyebrow", "h1", "diff", "faq1"]) { const el = $(`[data-v="${k}"]`); if (el) el.textContent = v[k]; }
  $('[data-v="cap"]').innerHTML = v.cap;
  const img = $('[data-v="img"]');
  img.src = v.img[0]; if (v.img[1]) img.srcset = v.img[1]; else img.removeAttribute("srcset");
  img.width = v.img[2]; img.height = v.img[3]; img.alt = v.alt;
  const t = $(`input[name="clinic_type"][value="${v.type}"]`); if (t) t.checked = true;
})();

// 2. The form. One question per step; answers live in the real inputs, so Back never clears anything.
(function form() {
  const form = $("#lead"), steps = $$(".step", form), bar = $("#fbar"), count = $("#fcount");
  const back = $("#fback"), next = $("#fnext"), msg = $("#fmsg");
  let i = 0;

  const t0 = Date.now();
  const emailOk = v => /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v.trim());
  // North American numbers only (BC/AB clinics): 10 digits after an optional leading 1, area code and
  // exchange can't start with 0 or 1. Stops "1234567890" style junk.
  const phoneOk = v => /^1?[2-9]\d{2}[2-9]\d{6}$/.test(v.replace(/\D/g, ""));
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
    next.textContent = last ? "Tell Us About My Clinic" : "Continue";
    next.type = last ? "submit" : "button";
    // One-tap steps have no Continue: tapping an answer moves on (Sandy, 24 Sep). The button only shows
    // on the contact step, or when the out-of-area note needs reading.
    next.hidden = tapOnly(s) && !outsidePicked(s);
    // Phones: a taller step can start above the screen after an auto-advance. Bring the card top back.
    const card = $("#start"), r = card.getBoundingClientRect();
    if (n > 0 && r.top < 0) scrollTo({ top: scrollY + r.top - 72, behavior: "smooth" });
  }
  const tapOnly = s => !$("input:not([type=radio]),textarea", s);
  const outsidePicked = s => !!$('input[value="Outside BC and Alberta"]:checked', s);

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
    if (opt.querySelector('input[value="Outside BC and Alberta"]')) return;
    clearTimeout(advancing);
    advancing = setTimeout(() => { if (stepOk(s, false)) go(i + 1); }, 260);
  });

  // Lead grade for the caller's pre-call briefing (never shown to the visitor, never used to block).
  // A: in area, has or is negotiating a space, opening within 12 months, decision-maker.
  // C: outside BC/AB, or no space + no date, or role Other. B: everything else.
  function grade(d) {
    const inArea = d.region && d.region !== "Outside BC and Alberta";
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
    form.dataset.grade = data.lead_grade; // exposed for the QA test only
    // The thank-you page reads these to greet the visitor by name and echo their project back.
    // sessionStorage, never the URL: a name in a URL leaks into analytics and referrers.
    const thanks = { name: (data.full_name || "").trim().split(/\s+/)[0], project_type: data.project_type,
      clinic_type: data.clinic_type, size: data.size, opening: data.opening, region: data.region,
      preview: ENDPOINT.startsWith("TODO") };
    const toThanks = () => { try { sessionStorage.setItem("medico_thanks", JSON.stringify(thanks)); } catch (e) {} location.href = "thank-you.html"; };
    // Not connected yet (Sandy: form destination comes last). Nothing is sent; the thank-you page says so.
    if (ENDPOINT.startsWith("TODO")) { toThanks(); return; }
    next.disabled = true; next.textContent = "Sending";
    try {
      const r = await fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
      if (!r.ok) throw new Error(r.status);
      toThanks();
    } catch (err) {
      msg.textContent = "That didn't send. Please try again, or call 604-644-4120.";
      next.disabled = false; next.textContent = "Tell Us About My Clinic";
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
