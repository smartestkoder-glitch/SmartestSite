from flask import Flask, url_for, redirect, request, jsonify, flash, session
from flask import render_template
import psycopg2
from database.dbfunc import Database

connect = psycopg2.connect(
    host="103.88.241.137",
    database="zametki",
    user="smartest",
    password=r"sdfghjklwqazx"

)



app = Flask(__name__)

app.secret_key = "smartest2010gjhfdc"

@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    user = session.get("username")
    if not user: return redirect(url_for("login"))
    return render_template("home/index.html")



# region Вход

@app.route("/login")
def login():
    if session.get("username"): return redirect(url_for("home"))
    return render_template("login/index.html")

@app.route("/check_data_login", methods=["POST"])
def check_data_login():
    dataLogin = request.form.get("login")
    dataPass = request.form.get("pass")
    print(dataLogin)

    dataDB = Database.User.Get.one_username(connect, dataLogin)
    if len(dataDB) == 0 or dataDB["password"] != dataPass: return ["Неверный логин или пароль!"]
    return ["false"]

@app.route("/login", methods=["POST"])
def login_post():
    print("login")

    dataLogin = request.form.get("login")
    dataPass = request.form.get("pass")

    session["username"] = dataLogin

    return redirect(url_for("home"))

# endregion

# region Регистрация

@app.route("/register")
def register():
    if session.get("username"): return redirect(url_for("home"))
    return render_template("register/index.html")

@app.route("/check_data", methods=["POST"])
def check_data():
    dataLogin = request.form.get("login")
    dataEmail = request.form.get("email")

    dataDB = Database.User.Get.all(connect)
    for user in dataDB:
        if user["username"] == dataLogin:
            return ["Данный логин уже занят! Придумайте другой"]
        if user["email"] == dataEmail:
            return ["Данная почта уже занята!"]
    return ["false"]

@app.route("/register", methods=["POST"])
def register_post():
    dataName = request.form.get("name")
    dataLogin = request.form.get("login")
    dataPass = request.form.get("pass")
    dataEmail = request.form.get("email")

    Database.User.add(connect, dataLogin, dataPass, dataEmail, dataName)

    session["username"] = dataLogin

    return redirect(url_for("home"))

# endregion

@app.route("/leave")
def leave():
    session["username"] = ""
    return redirect(url_for("login"))

app.run(debug=True)
