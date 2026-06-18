/**
 * gsap-init.js
 * All GSAP + ScrollTrigger animations for the portfolio.
 *
 * Strategy:
 *  1. Hero terminal boot sequence (typewriter, runs once on page load)
 *  2. ScrollTrigger fadeInUp on every .reveal-up element
 *  3. Skill bar width animation triggered on scroll
 *  4. Nav shrink on scroll (pure JS, no GSAP needed)
 *  5. Mobile nav hamburger toggle
 */

document.addEventListener("DOMContentLoaded", () => {

  // ── Guard: GSAP may not be loaded in older browsers ─────────
  if (typeof gsap === "undefined") return;

  // Register ScrollTrigger plugin
  gsap.registerPlugin(ScrollTrigger);


  // ── 1. Hero Terminal Boot Sequence ──────────────────────────
  const terminalBody = document.getElementById("terminal-body");
  if (terminalBody) {

    const lines = [
      { text: "$ python run.py",                  cls: "terminal__line--cmd"  },
      { text: " * Environment : development",      cls: "terminal__line--info" },
      { text: " * Booting Flask 3.0.3...",         cls: "terminal__line"       },
      { text: " * Loading SQLAlchemy models...",   cls: "terminal__line"       },
      { text: " * Registering blueprints...",      cls: "terminal__line"       },
      { text: " * Running on http://0.0.0.0:5000", cls: "terminal__line--ok"   },
      { text: " * Ready. Press CTRL+C to quit.",   cls: "terminal__line--ok"   },
    ];

    let lineIndex = 0;
    let charIndex  = 0;

    // Create cursor element
    const cursor = document.createElement("span");
    cursor.className = "terminal__cursor";
    terminalBody.appendChild(cursor);

    // Current line element being typed
    let currentLineEl = null;

    function typeNextChar() {
      if (lineIndex >= lines.length) {
        // Boot complete — remove cursor after a brief pause
        setTimeout(() => cursor.remove(), 1200);

        // Animate hero copy in after terminal finishes
        gsap.to(".hero__copy .reveal-up", {
          opacity: 1,
          y: 0,
          duration: 0.55,
          stagger: 0.13,
          ease: "power2.out",
        });
        return;
      }

      const line = lines[lineIndex];

      // Create a new line element on first char of each line
      if (charIndex === 0) {
        currentLineEl = document.createElement("div");
        currentLineEl.className = `terminal__line ${line.cls}`;
        terminalBody.insertBefore(currentLineEl, cursor);
      }

      // Append next character
      currentLineEl.textContent = line.text.slice(0, charIndex + 1);
      charIndex++;

      if (charIndex < line.text.length) {
        // Continue typing this line — vary speed slightly for realism
        const delay = line.text[charIndex - 1] === " " ? 40 : 28;
        setTimeout(typeNextChar, delay);
      } else {
        // Line complete — move to next after a short pause
        lineIndex++;
        charIndex = 0;
        setTimeout(typeNextChar, lineIndex === 1 ? 300 : 120);
      }
    }

    // Small initial delay so the page renders first
    setTimeout(typeNextChar, 500);
  }


  // ── 2. ScrollTrigger fadeInUp on .reveal-up ─────────────────
  //    Elements inside the hero copy are handled by the boot
  //    sequence above; we skip them here via :not(.hero__copy *)
  const revealEls = gsap.utils.toArray(".reveal-up:not(.hero__copy .reveal-up)");

  revealEls.forEach((el) => {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.6,
      ease: "power2.out",
      scrollTrigger: {
        trigger: el,
        start: "top 88%",   // fires when element top is 88% down the viewport
        once: true,          // only trigger once — no re-animation on scroll up
      },
    });
  });


  // ── 3. Skill bar width animation ────────────────────────────
  //    CSS sets width to 0 via animations.css; GSAP animates to --fill
  const skillBars = document.querySelectorAll(".skill-bar__fill");

  skillBars.forEach((bar) => {
    const targetWidth = getComputedStyle(bar).getPropertyValue("--fill").trim();

    gsap.to(bar, {
      width: targetWidth,
      duration: 1.0,
      ease: "power2.out",
      scrollTrigger: {
        trigger: bar,
        start: "top 90%",
        once: true,
      },
    });
  });


  // ── 4. Nav shadow on scroll (no GSAP needed) ────────────────
  const header = document.getElementById("site-header");
  if (header) {
    window.addEventListener("scroll", () => {
      header.classList.toggle("scrolled", window.scrollY > 20);
    }, { passive: true });
  }


  // ── 5. Mobile hamburger toggle ───────────────────────────────
  const burger   = document.getElementById("nav-burger");
  const navLinks = document.getElementById("nav-links");

  if (burger && navLinks) {
    burger.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("open");
      burger.setAttribute("aria-expanded", isOpen);
    });

    // Close nav when a link is tapped on mobile
    navLinks.querySelectorAll(".nav__link").forEach((link) => {
      link.addEventListener("click", () => navLinks.classList.remove("open"));
    });
  }


  // ── 6. Flash message auto-dismiss ────────────────────────────
  document.querySelectorAll(".flash").forEach((flash) => {
    setTimeout(() => {
      gsap.to(flash, {
        opacity: 0, x: 20, duration: 0.3, ease: "power2.in",
        onComplete: () => flash.remove(),
      });
    }, 4000);
  });

});
