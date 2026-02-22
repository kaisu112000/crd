let clicking = true;

function autoClick() {
    if (!clicking) return;

    let verifyBox = document.getElementById("verifyBox");
    let humanCheck = document.getElementById("humanCheck");
    let mainBtn = document.getElementById("mainBtn");

    if (verifyBox.style.display === "block") {
        humanCheck.click();
    } else {
        mainBtn.click();
    }

    setTimeout(autoClick, 10); // speed control
}

autoClick();
