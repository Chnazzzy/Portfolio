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
const rightArm = document.querySelector(".robot-side.front .robot-arm.right");

if (contactButton && contactSystem) {
    contactButton.addEventListener("click", () => {
        const isOpen = contactSystem.classList.toggle("active");
        if (rightArm) {
            rightArm.classList.toggle("raised", isOpen);
        }
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
const bubbles = 12;

for(let i=0;i<bubbles;i++){
    const bubble=document.createElement("div");
    bubble.className="bubble";

    bubble.style.left=Math.random()*100+"%";
    bubble.style.top=Math.random()*100+"%";

    const size=Math.random()*80+40;
    bubble.style.width=size+"px";
    bubble.style.height=size+"px";

    bubble.style.animationDelay=Math.random()*8+"s";

    document.body.appendChild(bubble);
}