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
const aboutButton = document.getElementById("aboutButton");

function openAbout(){
    if(aboutSystem){
        document.querySelector(".robot-page")
        .scrollIntoView({
            behavior:"smooth"
        });

        setTimeout(()=>{
            aboutSystem.classList.add("active");
        },700);
    }
}

if(aboutScreen){
    aboutScreen.addEventListener("click", openAbout);
}

if(aboutButton){
    aboutButton.addEventListener("click", openAbout);
}

if(closeAbout && aboutSystem){
    closeAbout.addEventListener("click",()=>{
        aboutSystem.classList.remove("active");
    });
}