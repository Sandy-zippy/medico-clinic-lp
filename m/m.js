// Meta category pages: sticky bottom button on phones. Shown whenever the hero button is off screen (scrolled
// past, or below the fold on a short phone or inside Facebook's in-app browser), hidden while the form section or
// the final call-to-action is on screen, so it never covers the form.
(function () {
  const bar = document.getElementById("stick"); if (!bar || !("IntersectionObserver" in window)) return;
  let pastHero = false, formOn = false, finalOn = false;
  const sync = () => { const on = pastHero && !formOn && !finalOn; bar.classList.toggle("on", on); document.body.classList.toggle("has-stick", on); };
  const watch = (el, fn, t) => el && new IntersectionObserver(([e]) => { fn(e); sync(); }, { threshold: t || 0 }).observe(el);
  watch(document.querySelector(".hcta .btn"), e => { pastHero = e.intersectionRatio < 1; }, 1); // only a fully visible button counts
  watch(document.getElementById("book"), e => { formOn = e.isIntersecting; });
  watch(document.querySelector(".final"), e => { finalOn = e.isIntersecting; });
})();
