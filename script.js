console.log("Lale.OS portfolio loaded");

// BOOT SCREEN
window.addEventListener("load", () => {
    const bootScreen = document.getElementById("bootScreen");

    if (bootScreen) {
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
    }
});


// CONTACT CARD
const contactButton = document.getElementById("contactButton");
const contactSystem = document.getElementById("contactSystem");

if (contactButton && contactSystem) {
    contactButton.addEventListener("click", () => {
        contactSystem.classList.toggle("active");
    });
}


// ABOUT WINDOW
const aboutScreen = document.getElementById("aboutScreen");
const aboutSystem = document.getElementById("aboutSystem");
const closeAbout = document.getElementById("closeAbout");

if (aboutScreen && aboutSystem) {
    aboutScreen.addEventListener("click", () => {
        aboutSystem.classList.add("active");
    });
}

if (closeAbout && aboutSystem) {
    closeAbout.addEventListener("click", () => {
        aboutSystem.classList.remove("active");
    });
}