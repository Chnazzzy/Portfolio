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