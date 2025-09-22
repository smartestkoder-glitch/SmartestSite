from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template
import psycopg2

conn = psycopg2.connect(#Моя бдшка, убедительная просьба не ломать :)
    host="103.88.241.137",
    database="fanfics",
    user="gen_user",
    password=r"t1Xf@hqowFyQMS"

)

def add_fanfic(name: int, category: int, description: str, text: str, likes: int, author: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO fanfics (name, category, description, text, likes, author) VALUES (%s, %s, %s, %s, %s, %s);",
            (name, category, description, text, likes, author)           # важно: кортеж (title,)
        )
        conn.commit()          # фиксируем изменения

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


app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("home"))
# функция вызовется, когда пользователь в браузере наберет АДРЕСХОСТА/ (зайдет на главную страницу сайта)
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/find')
def find():
    return render_template("find.html")

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/search', methods=['POST'])
def send_text():
    user_text = request.form.get('user_text')
    print(user_text)

    return jsonify(
        {
            "search_value": user_text,
            "all_data": get_all_fanfics()
        })
@app.route('/test')
def test():
    return render_template("test.html")
app.run(debug=True)
