/**
 * gsap-init.js
 * All GSAP + ScrollTrigger animations for the portfolio.
 *
 * Strategy:
 *  1. Hero terminal boot sequence (typewriter, runs once on page load)
 *  2. ScrollTrigger fadeInUp on every .reveal-up element
 *  3. Skill bar width animation triggered on scroll
 *  4. Nav shrink on scroll (hide/show + shadow)
 *  5. Mobile nav hamburger toggle
 *  6. Flash message auto-dismiss
 *  7. Terminal 3D tilt on mousemove
 *  8. Stat counter animation on scroll
 *  9. Button magnetic hover + ripple
 *  10. Project card staggered entrance
 */

document.addEventListener("DOMContentLoaded", () => {

  // ── Guard: GSAP may not be loaded in older browsers ─────────
  if (typeof gsap === "undefined") return;

  // Register ScrollTrigger plugin
  gsap.registerPlugin(ScrollTrigger);


  // ═════════════════════════════════════════════════════════════
  //  1. HERO TERMINAL BOOT SEQUENCE
  // ═════════════════════════════════════════════════════════════
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

    const cursor = document.createElement("span");
    cursor.className = "terminal__cursor";
    terminalBody.appendChild(cursor);

    let currentLineEl = null;

    function typeNextChar() {
      if (lineIndex >= lines.length) {
        setTimeout(() => cursor.remove(), 1200);

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

      if (charIndex === 0) {
        currentLineEl = document.createElement("div");
        currentLineEl.className = `terminal__line ${line.cls}`;
        terminalBody.insertBefore(currentLineEl, cursor);
      }

      currentLineEl.textContent = line.text.slice(0, charIndex + 1);
      charIndex++;

      if (charIndex < line.text.length) {
        const delay = line.text[charIndex - 1] === " " ? 40 : 28;
        setTimeout(typeNextChar, delay);
      } else {
        lineIndex++;
        charIndex = 0;
        setTimeout(typeNextChar, lineIndex === 1 ? 300 : 120);
      }
    }

    setTimeout(typeNextChar, 500);
  }


  // ═════════════════════════════════════════════════════════════
  //  2. SCROLLTRIGGER FADEINUP ON .reveal-up
  // ═════════════════════════════════════════════════════════════
  const revealEls = gsap.utils.toArray(".reveal-up:not(.hero__copy .reveal-up)");

  revealEls.forEach((el) => {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.6,
      ease: "power2.out",
      scrollTrigger: {
        trigger: el,
        start: "top 88%",
        once: true,
      },
    });
  });


  // ═════════════════════════════════════════════════════════════
  //  3. SKILL BAR WIDTH ANIMATION
  // ═════════════════════════════════════════════════════════════
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


  // ═════════════════════════════════════════════════════════════
  //  4. NAV HIDE/SHOW ON SCROLL + SHADOW
  // ═════════════════════════════════════════════════════════════
  const header = document.getElementById("site-header");
  let lastScrollY = 0;
  let ticking = false;

  if (header) {
    window.addEventListener("scroll", () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const currentScrollY = window.scrollY;

          // Shadow
          header.classList.toggle("scrolled", currentScrollY > 20);

          // Hide on scroll down, show on scroll up (only after 100px)
          if (currentScrollY > 100) {
            if (currentScrollY > lastScrollY) {
              header.classList.add("nav--hidden");
            } else {
              header.classList.remove("nav--hidden");
            }
          } else {
            header.classList.remove("nav--hidden");
          }

          lastScrollY = currentScrollY;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }


  // ═════════════════════════════════════════════════════════════
  //  5. MOBILE HAMBURGER TOGGLE
  // ═════════════════════════════════════════════════════════════
  const burger   = document.getElementById("nav-burger");
  const navLinks = document.getElementById("nav-links");

  if (burger && navLinks) {
    burger.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("open");
      burger.setAttribute("aria-expanded", isOpen);
      burger.classList.toggle("nav__burger--open", isOpen);
    });

    navLinks.querySelectorAll(".nav__link").forEach((link) => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        burger.classList.remove("nav__burger--open");
      });
    });
  }


  // ═════════════════════════════════════════════════════════════
  //  6. FLASH MESSAGE AUTO-DISMISS
  // ═════════════════════════════════════════════════════════════
  document.querySelectorAll(".flash").forEach((flash) => {
    setTimeout(() => {
      gsap.to(flash, {
        opacity: 0, x: 20, duration: 0.3, ease: "power2.in",
        onComplete: () => flash.remove(),
      });
    }, 4000);
  });


  // ═════════════════════════════════════════════════════════════
  //  7. TERMINAL 3D TILT ON MOUSEMOVE
  // ═════════════════════════════════════════════════════════════
  const terminal = document.getElementById("hero-terminal");
  if (terminal && !window.matchMedia("(pointer: coarse)").matches) {
    const hero = document.querySelector(".hero");

    hero.addEventListener("mousemove", (e) => {
      const rect = terminal.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      const rotateX = ((e.clientY - centerY) / (rect.height / 2)) * -6;
      const rotateY = ((e.clientX - centerX) / (rect.width / 2)) * 6;

      gsap.to(terminal, {
        rotateX: rotateX,
        rotateY: rotateY,
        duration: 0.4,
        ease: "power2.out",
        transformPerspective: 1000,
      });
    });

    hero.addEventListener("mouseleave", () => {
      gsap.to(terminal, {
        rotateX: 0,
        rotateY: 0,
        duration: 0.6,
        ease: "power2.out",
      });
    });
  }


  // ═════════════════════════════════════════════════════════════
  //  8. STAT COUNTER ANIMATION ON SCROLL
  // ═════════════════════════════════════════════════════════════
  const statNumbers = document.querySelectorAll(".stat-card__number");

  statNumbers.forEach((stat) => {
    const finalText = stat.textContent.trim();
    const isNumeric = !isNaN(parseInt(finalText));

    if (!isNumeric) {
      // For "AI" or text stats — just fade in
      gsap.from(stat, {
        opacity: 0,
        scale: 0.5,
        duration: 0.6,
        ease: "back.out(1.7)",
        scrollTrigger: {
          trigger: stat,
          start: "top 85%",
          once: true,
        },
      });
      return;
    }

    const finalValue = parseInt(finalText);
    const suffix = finalText.replace(/[0-9]/g, "");

    ScrollTrigger.create({
      trigger: stat,
      start: "top 85%",
      once: true,
      onEnter: () => {
        const obj = { val: 0 };
        gsap.to(obj, {
          val: finalValue,
          duration: 1.5,
          ease: "power2.out",
          onUpdate: () => {
            stat.textContent = Math.round(obj.val) + suffix;
          },
          onComplete: () => {
            stat.textContent = finalText; // ensure exact final value
            gsap.to(stat, {
              scale: 1.05,
              duration: 0.15,
              yoyo: true,
              repeat: 1,
              ease: "power2.inOut",
            });
          },
        });
      },
    });
  });


  // ═════════════════════════════════════════════════════════════
  //  9. BUTTON MAGNETIC HOVER + RIPPLE
  // ═════════════════════════════════════════════════════════════
  const magneticBtns = document.querySelectorAll(".btn");

  magneticBtns.forEach((btn) => {
    // Magnetic effect (desktop only)
    if (!window.matchMedia("(pointer: coarse)").matches) {
      btn.addEventListener("mousemove", (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        gsap.to(btn, {
          x: x * 0.25,
          y: y * 0.25,
          duration: 0.3,
          ease: "power2.out",
        });
      });

      btn.addEventListener("mouseleave", () => {
        gsap.to(btn, {
          x: 0,
          y: 0,
          duration: 0.4,
          ease: "elastic.out(1, 0.5)",
        });
      });
    }

    // Ripple effect on click
    btn.addEventListener("click", (e) => {
      const rect = btn.getBoundingClientRect();
      const ripple = document.createElement("span");
      ripple.className = "btn__ripple";
      ripple.style.left = (e.clientX - rect.left) + "px";
      ripple.style.top = (e.clientY - rect.top) + "px";
      btn.appendChild(ripple);

      gsap.fromTo(ripple,
        { scale: 0, opacity: 0.6 },
        {
          scale: 4,
          opacity: 0,
          duration: 0.6,
          ease: "power2.out",
          onComplete: () => ripple.remove(),
        }
      );
    });
  });


  // ═════════════════════════════════════════════════════════════
  //  10. PROJECT CARD STAGGERED ENTRANCE
  // ═════════════════════════════════════════════════════════════
  const projectGrids = document.querySelectorAll(".project-grid");

  projectGrids.forEach((grid) => {
    const cards = grid.querySelectorAll(".project-card");

    gsap.from(cards, {
      opacity: 0,
      y: 40,
      duration: 0.6,
      stagger: 0.12,
      ease: "power2.out",
      scrollTrigger: {
        trigger: grid,
        start: "top 80%",
        once: true,
      },
    });
  });


  // ═════════════════════════════════════════════════════════════
  //  11. SKILL ROW STAGGERED ENTRANCE
  // ═════════════════════════════════════════════════════════════
  const skillRows = document.querySelectorAll(".skill-row");

  skillRows.forEach((row) => {
    const chips = row.querySelectorAll(".tag--skill");

    gsap.from(chips, {
      opacity: 0,
      scale: 0.8,
      duration: 0.4,
      stagger: 0.05,
      ease: "back.out(1.7)",
      scrollTrigger: {
        trigger: row,
        start: "top 85%",
        once: true,
      },
    });
  });

});