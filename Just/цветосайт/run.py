from flask import Flask, url_for, redirect, request, jsonify, flash, session
from flask import render_template
import psycopg2

app = Flask(__name__)
app.secret_key = "y-sloshniy-secret-key"



@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home")
def home():

    return render_template("index.html", backColor=session.get('back-color'), fontSize=session.get('font-size'), fontColor=session.get('font-color'))


@app.route('/change', methods=['POST'])
def send_text():



    back_color = request.form.get('back-color')
    font_size = request.form.get('font-size')
    font_color = request.form.get('font-color')
    session['back-color'] = back_color
    session['font-size'] = font_size
    session['font-color'] = font_color
    return redirect("/")



app.run(debug=True)