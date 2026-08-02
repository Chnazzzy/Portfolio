console.log("Lale.OS portfolio loaded");

// ============================
// BOOT SCREEN — only plays once per browser tab session,
// not every time you navigate back to index.html
// ============================
window.addEventListener("load", () => {
    const bootScreen = document.getElementById("bootScreen");
    if (!bootScreen) return;

    const alreadyBooted = sessionStorage.getItem("laleBooted");

    if (alreadyBooted) {
        bootScreen.classList.add("hidden");
        bootScreen.style.display = "none";
        return;
    }

    sessionStorage.setItem("laleBooted", "true");

    setTimeout(() => {
        bootScreen.classList.add("hidden");

        const message = document.getElementById("robotMessage");
        if (message) {
            message.classList.add("show");
            setTimeout(() => {
                message.classList.remove("show");
            }, 3000);
        }
    }, 2200);
});


// ============================
// NIGHT MODE
// ============================
const nightModeToggle = document.getElementById("nightModeToggle");
const rootEl = document.documentElement;

function applyTheme(theme) {
    rootEl.setAttribute("data-theme", theme);
    if (nightModeToggle) {
        nightModeToggle.textContent = theme === "dark" ? "☀ Light" : "🌙 Night";
    }
}

applyTheme(localStorage.getItem("laleTheme") || "light");

if (nightModeToggle) {
    nightModeToggle.addEventListener("click", () => {
        const next = rootEl.getAttribute("data-theme") === "dark" ? "light" : "dark";
        localStorage.setItem("laleTheme", next);
        applyTheme(next);
    });
}


// ============================
// CONTACT CARD
// ============================
const contactButton = document.getElementById("contactButton");
const contactSystem = document.getElementById("contactSystem");
const rightArm = document.querySelector(".robot-side.front .robot-arm.right");

if (contactButton && contactSystem) {
    contactButton.addEventListener("click", () => {
        const isOpen = contactSystem.classList.toggle("active");
        if (rightArm) {
            rightArm.classList.toggle("raised", isOpen);
        }
    });
}


// ============================
// ABOUT WINDOW (opens instantly now, no scroll-wait delay)
// ============================
const aboutScreen = document.getElementById("aboutScreen");
const aboutSystem = document.getElementById("aboutSystem");
const closeAbout = document.getElementById("closeAbout");
const aboutButton = document.getElementById("aboutButton");

function openAbout() {
    if (aboutSystem) {
        aboutSystem.classList.add("active");
    }
}

if (aboutScreen) {
    aboutScreen.addEventListener("click", openAbout);
}

if (aboutButton) {
    aboutButton.addEventListener("click", openAbout);
}

if (closeAbout && aboutSystem) {
    closeAbout.addEventListener("click", () => {
        aboutSystem.classList.remove("active");
    });
}


// ============================
// ROBOT EYES FOLLOW THE MOUSE
// ============================
const eyes = document.querySelectorAll(".eye");

if (eyes.length) {
    const maxMove = 8;

    document.addEventListener("mousemove", (e) => {
        eyes.forEach((eye) => {
            const pupil = eye.querySelector(".pupil");
            if (!pupil) return;

            const rect = eye.getBoundingClientRect();
            const eyeCenterX = rect.left + rect.width / 2;
            const eyeCenterY = rect.top + rect.height / 2;

            const angle = Math.atan2(
                e.clientY - eyeCenterY,
                e.clientX - eyeCenterX
            );

            const moveX = Math.cos(angle) * maxMove;
            const moveY = Math.sin(angle) * maxMove;

            pupil.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
}
const aboutButton = document.querySelector(".about-button");
const aboutSystem = document.getElementById("aboutSystem");
const closeAbout = document.getElementById("closeAbout");

if (aboutButton) {
    aboutButton.addEventListener("click", (e) => {
        e.preventDefault();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

        setTimeout(() => {
            aboutSystem.classList.add("active");
        }, 400);
    });
}

if (closeAbout) {
    closeAbout.addEventListener("click", () => {
        aboutSystem.classList.remove("active");
    });
}