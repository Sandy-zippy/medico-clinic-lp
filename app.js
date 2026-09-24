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

  const emailOk = v => /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v.trim());
  const phoneOk = v => v.replace(/\D/g, "").length >= 10;
  function fieldOk(el) {
    if (!el.required) return true;
    if (el.type === "email") return emailOk(el.value);
    if (el.type === "tel") return phoneOk(el.value);
    return el.value.trim() !== "";
  }
  function stepOk(s, show) {
    const radios = $$("input[type=radio]", s);
    if (radios.length) {
      const ok = radios.some(r => r.checked);
      if (show) s.classList.toggle("bad", !ok);
      return ok;
    }
    let first = null;
    for (const el of $$("input,textarea", s)) {
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
  form.addEventListener("change", e => { if (e.target.type === "radio") e.target.closest(".step").classList.remove("bad"); });
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
    if (stepOk(steps[i], true)) go(i + 1);
  });
  back.addEventListener("click", () => go(i - 1));

  form.addEventListener("submit", async e => {
    e.preventDefault();
    msg.textContent = "";
    if (!stepOk(steps[i], true)) return;
    if (form.website.value) return; // honeypot
    if (ENDPOINT.startsWith("TODO")) { msg.textContent = "Preview only: the form is not connected yet, nothing was sent."; return; }
    const data = Object.fromEntries(new FormData(form).entries());
    delete data.website;
    data.submitted_at = new Date().toISOString();
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
