import { mountMarquee } from "./vendor/gl-marquee/dist/index.js";

const host = document.querySelector(".apcx-footer-banner");
const button = document.querySelector(".apcx-footer-motion");
const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
let controller;
let paused = motion.matches;
let visible = false;
let pageActive = true;
let generation = 0;

function unmount() {
  generation++;
  controller?.destroy();
  controller = undefined;
  delete host.dataset.ready;
}

async function mount() {
  unmount();
  if (!visible || !pageActive) return;
  const current = generation;
  controller = mountMarquee(host, {
    message: "Another Planet . Creative eXperience",
    fontWeight: 400,
    mode: "footer-banner",
    appearance: { background: "#f7f7f8", text: "#111111" },
    reducedMotion: paused,
  });
  await controller.ready;
  if (current !== generation) return;
  host.dataset.ready = "true";
  button.hidden = false;
  button.textContent = paused ? "Play animation" : "Pause animation";
}

if (host && button) {
  // Keep the long catalog page light: mount only near the footer and release
  // the official renderer's canvas, observers and GL resources when it leaves.
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      void mount();
    }, { rootMargin: "300px" });
    observer.observe(host);
  } else {
    visible = true;
    void mount();
  }
  button.addEventListener("click", () => {
    paused = !paused;
    void mount();
  });
  motion.addEventListener("change", () => {
    paused = motion.matches;
    void mount();
  });
  window.addEventListener("pagehide", () => {
    pageActive = false;
    unmount();
  });
  window.addEventListener("pageshow", () => {
    pageActive = true;
    if (!controller) void mount();
  });
}
