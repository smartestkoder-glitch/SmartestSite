

function showAlert(alertStyle, text) {
    const warnBlock = document.getElementsByClassName("smart-warn")[0]

    warnBlock.classList.add("alert")
    warnBlock.classList.add("alert-"+alertStyle)
    warnBlock.textContent = text
}



export default {showAlert}