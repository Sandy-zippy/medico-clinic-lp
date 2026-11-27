// Meta category pages (m/<cat>/), v2 27 Nov 2026. app.js runs the form, tracking and ad angles; this file adds:
// 1) hero answers: a tap answers the form's first question in the real form (so form_step_2 fires as usual) and
//    takes the visitor to step 2; 2) sticky button on phones while neither the hero answers, the form nor the close
//    is on screen; 3) arrival classes for section motion; 4) gallery progress bar; 5) project count-up.
(function () {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  $$("[data-answer]").forEach(b => b.addEventListener("click", () => {
    const opt = $(`#lead input[name="project_type"][value="${b.dataset.answer}"]`);
    if (!opt) return;
    b.classList.add("on");
    opt.closest("label").click();                       // app.js auto-advances to step 2 and logs form_step_2
    if (typeof clarity === "function") clarity("event", "hero_answer");
    setTimeout(() => { $("#start").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); }, 120);
    // keyboard and screen-reader users land on the next question (app.js advances after 260 ms)
    setTimeout(() => {
      const q = $$("#lead .step").find(s => !s.hidden && s.offsetParent);
      const f = q && $("input:not([type=hidden]),button", q);
      if (f) f.focus({ preventScroll: true });
    }, 450);
  }));

  if (!("IntersectionObserver" in window)) { $$(".arrive").forEach(s => s.classList.add("in")); return; }

  const bar = $("#stick");
  let heroOn = true, formOn = false, finalOn = false;
  const sync = () => { const on = !heroOn && !formOn && !finalOn; bar.classList.toggle("on", on); document.body.classList.toggle("has-stick", on); };
  const watch = (el, fn) => el && new IntersectionObserver(([e]) => { fn(e.isIntersecting); sync(); }).observe(el);
  watch($(".quick"), v => heroOn = v);
  watch($("#book"), v => formOn = v);
  watch($(".final"), v => finalOn = v);

  // Arrival: a section gets .in once a quarter of it is on screen (or it's already on screen at load).
  const arr = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); arr.unobserve(e.target); } }), { threshold: .25 });
  $$(".arrive").forEach(s => arr.observe(s));

  const gal = $(".gal"), gb = $(".galbar i");
  if (gal && gb) {
    const upd = () => { const max = gal.scrollWidth - gal.clientWidth; const vis = gal.clientWidth / gal.scrollWidth;
      gb.style.setProperty("--p", `${Math.min(100, (vis + (max ? gal.scrollLeft / max : 0) * (1 - vis)) * 100)}%`); };
    gal.addEventListener("scroll", upd, { passive: true }); addEventListener("resize", upd); upd();
  }

  const cnt = $(".count");
  if (cnt && !reduce) {
    const m = cnt.dataset.to.match(/^(\d+)(.*)$/);
    if (m) new IntersectionObserver(([e], o) => {
      if (!e.isIntersecting) return; o.disconnect();
      const to = +m[1], t0 = performance.now(), d = 1100;
      const step = t => { const k = Math.min(1, (t - t0) / d); cnt.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))) + (k === 1 ? m[2] : "");
        if (k < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }, { threshold: .6 }).observe(cnt);
  }
})();
