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