from flask import (
    Flask, render_template,
    flash, request
)

app = Flask(__name__)
app.secret_key = 'sLd+i2-jIa=sWa38'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('username')
        age = request.form.get('password')
        if name and age:
            flash('登録できました', 'success')
            flash('サイトを利用可能です', 'success')
        else:
            flash('登録に失敗しました', 'error')
            flash('ユーザー名・パスワードを入力してください', 'error')

    return render_template('flash_sample.html')

if __name__ == '__main__':
    app.run(port='8000', debug=True)