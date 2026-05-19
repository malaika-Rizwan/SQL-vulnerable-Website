/** Cursor glow — hands-on lab UI */
(function () {
  const glow = document.querySelector(".cursor-glow");
  const dot = document.querySelector(".cursor-dot");
  if (!glow || !dot) return;

  let x = 0;
  let y = 0;
  let gx = 0;
  let gy = 0;

  document.addEventListener("mousemove", (e) => {
    x = e.clientX;
    y = e.clientY;
    dot.style.left = x + "px";
    dot.style.top = y + "px";
  });

  function tick() {
    gx += (x - gx) * 0.12;
    gy += (y - gy) * 0.12;
    glow.style.left = gx + "px";
    glow.style.top = gy + "px";
    requestAnimationFrame(tick);
  }
  tick();

  document.querySelectorAll(".glow-card, .track-item, .glow-btn, .auth-glow-panel").forEach((el) => {
    el.addEventListener("mouseenter", () => document.body.classList.add("cursor-intense"));
    el.addEventListener("mouseleave", () => document.body.classList.remove("cursor-intense"));
  });
})();
