// Meta category pages: sticky bottom button on phones. Shown once the hero button has scrolled away,
// hidden while the form section or the final call-to-action is on screen, so it never covers the form.
(function () {
  const bar = document.getElementById("stick"); if (!bar || !("IntersectionObserver" in window)) return;
  let pastHero = false, formOn = false, finalOn = false;
  const sync = () => { const on = pastHero && !formOn && !finalOn; bar.classList.toggle("on", on); document.body.classList.toggle("has-stick", on); };
  const watch = (el, fn) => el && new IntersectionObserver(([e]) => { fn(e); sync(); }).observe(el);
  watch(document.querySelector(".hcta"), e => { pastHero = !e.isIntersecting && e.boundingClientRect.top < 0; });
  watch(document.getElementById("book"), e => { formOn = e.isIntersecting; });
  watch(document.querySelector(".final"), e => { finalOn = e.isIntersecting; });
})();
