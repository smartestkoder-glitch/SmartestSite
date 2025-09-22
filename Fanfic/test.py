from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template
import psycopg2

conn = psycopg2.connect(
    host="103.88.241.137",
    database="fanfics",
    user="gen_user",
    password=r"t1Xf@hqowFyQMS"

)

def add_likes(id):
    likesS = 0

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM fanfics WHERE id=%s;", (id,))
        rows = cur.fetchall()

        likesS = rows[0][0]

    print(likesS)
    print(id)
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE fanfics SET likes=%s WHERE id=%s",
            (likesS, id)           # важно: кортеж (title,)
        )
        conn.commit()
add_likes(2)