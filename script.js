console.log("Lale portfolio loaded");
// ================================
// BOOT SCREEN
// ================================

window.addEventListener("load", () => {

    const bootScreen = document.getElementById("bootScreen");

    if (bootScreen) {

        setTimeout(() => {

            bootScreen.classList.add("hidden");

        }, 2200);

    }

});
const contactBtn = document.getElementById("contactBtn");
const contactSystem = document.getElementById("contactSystem");


if(contactBtn && contactSystem){

    contactBtn.addEventListener("click",()=>{

        contactSystem.classList.add("active");

    });

}
// ================================
// ABOUT ME SCREEN
// ================================

document.addEventListener("DOMContentLoaded", () => {

    const mainScreen = document.getElementById("mainScreen");
    const aboutSystem = document.getElementById("aboutSystem");
    const closeAbout = document.getElementById("closeAbout");


    console.log("About system:", aboutSystem);
    console.log("Main screen:", mainScreen);


    if(mainScreen && aboutSystem){

        mainScreen.addEventListener("click", () => {

            aboutSystem.classList.add("active");

        });

    }


    if(closeAbout && aboutSystem){

        closeAbout.addEventListener("click", () => {

            aboutSystem.classList.remove("active");

        });

    }

});