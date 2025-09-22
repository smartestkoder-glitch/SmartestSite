from flask import Flask, url_for, redirect, request, jsonify, flash
from flask import render_template
import psycopg2

conn = psycopg2.connect(#Моя бдшка, убедительная просьба не ломать :) P.S: я только под конец понял, что можно было использовать ORM(sqlalchemy). Так что использовал psycopg2
    host="103.88.241.137",
    database="fanfics",
    user="gen_user",
    password=r"t1Xf@hqowFyQMS"

)

def add_fanfic(name: str, category: str, description: str, text: str, like: int, author: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO fanfics (name, category, description, text, likes, author) VALUES (%s, %s, %s, %s, %s, %s);",
            (name, category, description, text, like, author)
        )
        conn.commit()

def add_likes(id):
    likesS = 0

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM fanfics WHERE id=%s;", (id,))
        rows = cur.fetchall()

        likesS = rows[0][5]+1

    print(likesS)
    print(id)
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE fanfics SET likes = %s WHERE id = %s",
            (likesS, id)
        )
        conn.commit()

def edit_fanfic(id: int, name: str, category: str, description: str, text: str, author: str):


    with conn.cursor() as cur:
        cur.execute(
            "UPDATE fanfics SET name = %s,category = %s,description = %s,text = %s,author = %s WHERE id = %s",
            (name, category, description, text, author, id)
        )
        conn.commit()

def get_all_fanfics():
    ans = []
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM fanfics;")
        rows = cur.fetchall()
        for row in rows:
            ans.append({
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "description": row[3],
                "text": row[4],
                "likes": row[5],
                "author": row[6],
            })
    return ans

def delete_fanfic(id):


    with conn.cursor() as cur:
        cur.execute("DELETE FROM fanfics WHERE id=%s;", (id,))
        conn.commit()




app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("home"))
# функция вызовется, когда пользователь в браузере наберет АДРЕСХОСТА/ (зайдет на главную страницу сайта)
@app.route('/home')
def home():
    return render_template("page.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/find')
def find():
    return render_template("find.html")

@app.route('/create')
def create():
    return render_template("create.html")

@app.route("/like/<int:id>")
def likes(id):
    add_likes(int(id))
    return redirect(url_for("find"))

@app.route("/delete/<int:id>")
def delete(id):
    delete_fanfic(int(id))
    return redirect(url_for("find"))



@app.route('/search', methods=['POST'])
def send_text():
    user_text = request.form.get('user_text')
    print(user_text)

    return jsonify(
        {
            "search_value": user_text,
            "all_data": get_all_fanfics()
        })

@app.route('/create', methods=['POST'])
def add_fanfic_site():
    name_fanfic = request.form.get("name_fanfic")
    text_fanfic = request.form.get("text_fanfic")
    author_fanfic = request.form.get("author_fanfic")
    description_fanfic = request.form.get("description_fanfic")
    category_fanfic = request.form.get("category_fanfic")
    #redirect(url_for("find"))
    print(str(name_fanfic), str(category_fanfic), str(description_fanfic), str(text_fanfic), 0, str(author_fanfic))
    if len(name_fanfic)<1 or len(text_fanfic)<1 or len(author_fanfic)<1 or len(category_fanfic)<1: return render_template("redirect_to_find_alert.html", message="Вы не указали обязательное(ые) поле(я)!")
    else:
        try:
            add_fanfic(str(name_fanfic), str(category_fanfic), str(description_fanfic), str(text_fanfic), 0, str(author_fanfic))
            return render_template("redirect_to_find_alert.html", message="Фанфик успешно создан!")
        except Exception as e:
            return render_template("redirect_to_find_alert.html", message=f"Ошибка при создании записи! Скорее всего неверный тип данных. Ошибка: {e}")

@app.route('/edit/<int:id>', methods=['POST'])#
def edit_fanfic_site_confirm(id):
    name_fanfic = request.form.get("name_fanfic")
    text_fanfic = request.form.get("text_fanfic")
    author_fanfic = request.form.get("author_fanfic")
    description_fanfic = request.form.get("description_fanfic")
    category_fanfic = request.form.get("category_fanfic")
    #redirect(url_for("find"))
    print(name_fanfic, category_fanfic, description_fanfic, text_fanfic, 0, author_fanfic)
    if len(name_fanfic)<1 or len(text_fanfic)<1 or len(author_fanfic)<1 or len(category_fanfic)<1: return render_template("redirect_to_find_alert.html", message="Вы не указали обязательное(ые) поле(я)!")
    else:
        try:
            edit_fanfic(id, str(name_fanfic), str(category_fanfic), str(description_fanfic), str(text_fanfic), str(author_fanfic))
            return render_template("redirect_to_find_alert.html", message="Фанфик успешно изменен!")
        except Exception as e:
            return render_template("redirect_to_find_alert.html", message=f"Ошибка при изменении записи(база данных)! Ошибка: {e}")

@app.route('/edit/<int:id>')
def edit_fanfic_site(id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM fanfics WHERE id = %s;", (id,))
        rows = cur.fetchall()[0]
    return render_template("edit.html", id=id, name=rows[1], text=rows[4], description=rows[3], category=rows[2], author=rows[6])




app.run(debug=True)
