from flask import Flask, url_for
from flask import render_template

app = Flask(__name__)

# функция вызовется, когда пользователь в браузере наберет АДРЕСХОСТА/ (зайдет на главную страницу сайта)
@app.route('/')
def index():
    # возвращаем HTML код, который увидит пользователь
    return """
        <html>
            <head>
                <title>Вупсень или пупсень?</title>
            </head>
            <body>
                <h1>Научись отличать Вупсеня от Пупсеня!</h1>
                <ul>
                    <li><a href="/vupsen">Это Вупсень!</a></li>
                    <li><a href="/pupsen">Это Пупсень!</a></li>
                </ul>
            </body>
        </html>
    """

# TODO: Сделай так, чтобы на странице выводилась картинка с Вупсенем из интернета
# PS. Для этого нужен тэг img: http://htmlbook.ru/html/img
@app.route('/vupsen')
def vupsen_page():
    #return render_template("vupsen.html") я изначально раскидал по файлам, а только потом прочитал задание и понял что так нельзя xD
    return f"""
    <img src="https://avatars.mds.yandex.net/get-yapic/63032/vJRscLqJzr5YyFW6p1JhmVprCU-1/orig" alt="Это пупсень" height="400" width="400">
    <br>
    <a href="/">Вернуться</a>
    """

# TODO: Здесь добавь страницу /pupsen, на которой будет картинка с пупсенем
@app.route('/pupsen')
def pupsen_page():
    return f"""
    <img src="https://avatars.mds.yandex.net/i?id=00cac9351a50c572d13a18c411903543_l-5221961-images-thumbs&n=13" alt="Это пупсень" height="400" width="400">
    
    <br>
    <a href="/">Вернуться</a>
    """
app.run(debug=True)
