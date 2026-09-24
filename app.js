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
  }

  // Selecting an answer clears the step's error. It does not auto-jump (brief: Continue after selecting).
  form.addEventListener("change", e => {
    if (e.target.type !== "radio") return;
    (e.target.closest(".field") || e.target.closest(".step")).classList.remove("bad");
    if (e.target.name === "region") $("#outside").hidden = e.target.value !== "Outside BC and Alberta";
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
    if (ENDPOINT.startsWith("TODO")) { msg.textContent = "Preview only: the form is not connected yet, nothing was sent."; return; }
    next.disabled = true; next.textContent = "Sending";
    try {
      const r = await fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
      if (!r.ok) throw new Error(r.status);
      form.hidden = true; const t = $("#thanks"); t.hidden = false; t.focus();
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
  new IntersectionObserver(([e]) => {
    const show = !e.isIntersecting && e.boundingClientRect.top < 0;
    bar.classList.toggle("on", show); document.body.classList.toggle("has-stick", show);
  }).observe(target);
})();
