function showAlert(alertStyle, text) {
    const warnBlock = document.getElementsByClassName("smart-warn")[0]

    warnBlock.classList.add("alert")
    warnBlock.role = "warn"
    warnBlock.classList.add("alert-" + alertStyle)
    warnBlock.textContent = text

    setTimeout(() => {
        warnBlock.classList.remove("alert")
        warnBlock.classList.remove("alert-" + alertStyle)
        warnBlock.textContent = ""
    }, 3000)
}

async function register() {
    alert("123")
    const textName = document.getElementsByName("name")[0].value
    const textLogin = document.getElementsByName("login")[0].value
    const textPass = document.getElementsByName("pass")[0].value
    const textEmail = document.getElementsByName("email")[0].value


    const textCheck = checkAll(textName, textLogin, textPass, textEmail)
    if (textCheck) return showAlert("danger", textCheck)

    const form = document.querySelector('#reg-form');
    const data = new FormData(form);

    fetch('/check_data', {
        method: 'POST',
        body: data
    })
        .then(dataa => dataa.json())
        .then(dt => {
            if (dt[0] !== "false") return showAlert("danger", dt)
            else return fetch('/register', {
                method: 'POST',
                body: data
            })
                .then(res => {
                    if (res.redirected) {
                        window.location.href = res.url;//Оказывается при пост запросе и редиректе после него, редирект надо делать тут xD а я минут 20 думал и не мог понять что он на главную не переводит)
                    }
                });
        });


}

function checkAll(name, login, pass, email) {
    const cName = checkName(name)
    const cLogin = checkLogin(login)
    const cPass = checkPass(pass)
    const cEmail = checkEmail(email)

    return (cName || cPass || cLogin || cEmail)
}

function checkName(name) {
    if (!name) {
        return "Введите имя!"
    }
    if (name.length <= 2) {
        return "Слишком короткое имя! Минимальная длина: 3"
    }
    return false
}

function checkLogin(name) {
    if (!name) {
        return "Введите логин!"
    }
    if (name.length <= 4) {
        return "Слишком короткий логин! Минимальная длина: 5"
    }
    return false
}

function checkPass(name) {
    if (!name) {
        return "Введите пароль!"
    }
    if (name.length <= 7) {
        return "Слишком короткий логин! Минимальная длина: 8"
    }
    return false
}

function checkEmail(name) {
    if (!name) {
        return "Введите почту!"
    }
    if (!name.includes("@")) {
        return "Почта указана неверно! Нету символа '@'"
    }
    if (!name.includes(".")) {
        return "Почта указана неверно! Нету символа '.'"
    }
    return false
}