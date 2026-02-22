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


https: //u55120754.ct.sendgrid.net/ls/click?upn=u001.-2FoRrQDLcwuoGj7iRfngImFp4Rt5oCwN0sHTFZmnSGXMWaHk3y0JZ4mylX-2F0L3Lhik2eYFlC9wxeMBM9UJDH9aw-3D-3D_BtE_KE4d85m3OnJk3DaDsKCTGhbemyw-2BpBlLJgEIFR6jUPqYYje8oh3c9sbza0mKQpFrEJuJ8y2BLJf3SMZFSMOOFL8GJ1ba8CCcx2XRtDyryu1xBTB3fFzzrnL-2BBYGnuf4srTSZ61TRkk6-2FRmPl-2B5RgtWgcPSlq9xJNLTQ2KxinR1MoY6HScXABJRZOuo8OExAg7G97-2BKso9cxsPOS2RzlNJ69b-2FD2Tk8Ri9w2OttV42bOE3IfLpcCsKtLzKZ5RSteZzqYjDPAtCq6q7jT-2FP8pGXqQH2iSE8bBKWs2Zvo6YfLvncLowXNsFmy4YwZWKL50S4yDN7y0ZCHZ1T6DxgR9VCA-3D-3D
