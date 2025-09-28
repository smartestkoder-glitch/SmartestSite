import datetime
import uuid
import psycopg2
from sqlalchemy.dialects.postgresql import JSONB

class Database:
    class User:
        #Из списка, который возращается из БД делаем удобный объект(словарь)
        @staticmethod
        def to_normal_data(data):
            ans = []
            for zapic in data:
                ans.append({
                    "id": zapic[0],
                    "username": zapic[1],
                    "password": zapic[2],
                    "email": zapic[3],
                    "name": zapic[4],
                    "notes_id": zapic[5],
                    "reg_time": zapic[6],
                })
            return ans

        #Добавить запись
        @staticmethod
        def add(conn, username, password, email, name):
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password, email, name) VALUES (%s, %s, %s, %s);",
                    (username, password, email, name)
                )
                conn.commit()

        #Получить данные из базы данных
        class Get:
            @staticmethod
            def all(conn):
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM users"
                    )
                    result = cur.fetchall()
                    conn.commit()
                return Database.User.to_normal_data(result)

            @staticmethod
            def one(conn, user_id):
                with conn.cursor() as cur:
                    result = cur.execute(
                        "SELECT * FROM users WHERE id = %s", (user_id,)
                    )
                    result = cur.fetchall()
                conn.commit()
                ans = Database.User.to_normal_data(result)
                if len(ans) == 0: return []
                return ans[0]

            @staticmethod
            def one_username(conn, username):
                with conn.cursor() as cur:
                    result = cur.execute(
                        "SELECT * FROM users WHERE username = %s", (username,)
                    )
                    result = cur.fetchall()
                conn.commit()
                ans = Database.User.to_normal_data(result)
                if len(ans) == 0: return []
                return ans[0]

        #Изменить запись
        class Edit:
            @staticmethod
            def email(conn, user_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE users SET email = %s WHERE id = %s",
                        (value, user_id)
                    )
                    conn.commit()

            @staticmethod
            def name(conn, user_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE users SET name = %s WHERE id = %s",
                        (value, user_id)
                    )
                    conn.commit()

            @staticmethod
            def username(conn, user_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE users SET username = %s WHERE id = %s",
                        (value, user_id)
                    )
                    conn.commit()

            @staticmethod
            def password(conn, user_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE users SET password = %s WHERE id = %s",
                        (value, user_id)
                    )
                    conn.commit()


            class Notes:
                @staticmethod
                def add(conn, user_id, value):
                    with conn.cursor() as cur:

                        notes = Database.User.Get.one(conn, user_id)["notes_id"]
                        notes.append(value)
                        notes = str(list(set(notes)))#Сделал это чтобы повторов не было в заметках


                        cur.execute(
                            "UPDATE users SET notes_id = %s WHERE id = %s",
                            (notes, user_id)
                        )
                        conn.commit()

    class Notes:

        #Из списка, который возращается из БД делаем удобный объект(словарь)
        @staticmethod
        def to_normal_data(data):
            ans = []
            for zapic in data:
                ans.append({
                    "id": zapic[0],
                    "uuid": zapic[1],
                    "creator_id": zapic[2],
                    "name": zapic[3],
                    "text": zapic[4],
                    "delete": zapic[5],
                    "edit": zapic[6],
                    "delete_time": zapic[7],
                    "edited_time": zapic[8],
                    "created_time": zapic[9],
                })
            return ans

        #Добавить запись
        @staticmethod
        def add(conn, creator_id, name, text):
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO notes (uuid, creator_id, name, text) VALUES (%s, %s, %s, %s);",
                    (str(uuid.uuid4()), creator_id, name, text)
                )
                conn.commit()

        #Получить данные из базы данных
        class Get:
            @staticmethod
            def all(conn):
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM notes"
                    )
                    result = cur.fetchall()
                    conn.commit()
                return Database.User.to_normal_data(result)

            @staticmethod
            def one(conn, note_id):
                with conn.cursor() as cur:
                    result = cur.execute(
                        "SELECT * FROM notes WHERE id = %s", (note_id,)
                    )
                    result = cur.fetchall()
                conn.commit()
                return Database.User.to_normal_data(result)[0]

        #Изменить запись
        class Edit:
            @staticmethod
            def text(conn, note_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE notes SET text = %s WHERE id = %s",
                        (value, note_id)
                    )
                    conn.commit()

            @staticmethod
            def name(conn, note_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE notes SET name = %s WHERE id = %s",
                        (value, note_id)
                    )
                    conn.commit()

            @staticmethod
            def delete(conn, note_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE notes SET delete = %s WHERE id = %s",
                        (value, note_id)
                    )
                    conn.commit()

            @staticmethod
            def edit(conn, note_id, value):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE notes SET edit = %s WHERE id = %s",
                        (value, note_id)
                    )
                    conn.commit()

        #Для добавления текущего времени
        class Time:
            @staticmethod
            def edited(conn, note_id):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE notes SET edited_time = %s WHERE id = %s",
                        (datetime.datetime.now(), note_id)
                    )
                    conn.commit()

            @staticmethod
            def delete(conn, note_id):
                with conn.cursor() as cur:

                    cur.execute(
                        "UPDATE notes SET delete_time = %s WHERE id = %s",
                        (datetime.datetime.now(), note_id)
                    )
                    conn.commit()