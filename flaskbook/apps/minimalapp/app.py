from flask import Flask, render_template, url_for, request, redirect, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message

app = Flask(__name__)
# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
# flask-debugtoolbarを使う
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)
# Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
print(os.environ.get("MAIL_PASSWORD"))
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
# flask-mail拡張を登録する
mail = Mail(app)

@app.route('/')
def index():
    return "Hello, Flaskbook!"

@app.route('/hello/<name>', methods=['GET', 'POST'], endpoint='hello-endpoint')
def hello(name):
    return f"Hello, {name}!"

@app.route('/name/<name>')
def show_name(name):
    return render_template('index.html', name=name)

with app.test_request_context():
    # /
    print(url_for('index'))
    # /hello/world
    print(url_for('hello-endpoint', name='world'))
    # /name/ichiro?page=1
    print(url_for('show_name', name='ichiro', page='1'))

with app.test_request_context("/users?updated=true"):
    # trueが出力される
    print(request.args.get("updated"))

@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))
    response.set_cookie("flaskbook key", "flaskbook value")
    session["username"] = "ichiro"
    return response

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        # 入力チェック
        is_valid = True
        if not username:
            flash("ユーザー名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # メールを送る
        send_email(email, "問い合わせありがとうございました。", "contact_mail", username=username, description=description)

        # contactエンドポイントへリダイレクトする
        flash("問い合わせ内容はメールにて送信しました。問い合わせありがとうございます。")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
