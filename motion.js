// Medico landing page motion. Progressive: without this file (or with reduced motion) every element
// is already in its final, visible state. The CSS only hides things under html.anim, which is set here.
(function () {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;
  const root = document.documentElement;
  root.classList.add("anim");

  // 1. Hero load sequence: next frame so the hidden state paints first, then the stagger runs.
  requestAnimationFrame(() => requestAnimationFrame(() => root.classList.add("loaded")));

  // 2. Scroll reveals. Each [data-anim] block gets .in once, when a fifth of it is on screen.
  // A block the reader has already scrolled past (top above the viewport) is revealed too, so a fast
  // flick can never leave a section stuck in its hidden start state.
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting && e.boundingClientRect.top > 0) return;
    e.target.classList.add("in");
    io.unobserve(e.target);
  }), { threshold: 0.2, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll("[data-anim]").forEach(el => io.observe(el));
  // Safety net for jump-scrolls (a jump from below the screen to above it crosses no threshold, so the
  // observer never fires): after scrolling settles, reveal every block whose top is above the fold line.
  let t;
  addEventListener("scroll", () => {
    clearTimeout(t);
    t = setTimeout(() => document.querySelectorAll("[data-anim]:not(.in)").forEach(el => {
      if (el.getBoundingClientRect().top < innerHeight) { el.classList.add("in"); io.unobserve(el); }
    }), 120);
  }, { passive: true });

  // 3. Pointer tilt on the hero photo and portfolio tiles. Desktop pointers only; max 4 degrees (3 on stage cards).
  if (matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll("[data-tilt], .pf figure, .stage").forEach(el => {
      const max = el.matches(".stage") ? 3 : 4;
      el.addEventListener("pointermove", e => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.setProperty("--rx", `${(-y * max).toFixed(2)}deg`);
        el.style.setProperty("--ry", `${(x * max).toFixed(2)}deg`);
      });
      el.addEventListener("pointerleave", () => { el.style.setProperty("--rx", "0deg"); el.style.setProperty("--ry", "0deg"); });
    });
  }
})();
