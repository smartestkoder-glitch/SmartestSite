from flask import Flask, url_for, redirect, request, jsonify
from flask import render_template
import psycopg2

conn = psycopg2.connect(
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
                "name": row[0],
                "category": row[1],
                "description": row[2],
                "text": row[3],
                "likes": row[4],
                "author": row[5],
            })
    return ans
#add_fanfic(123, 123, "desc", "text", 111, "author")
print(get_all_fanfics())