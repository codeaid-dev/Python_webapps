from flask import Flask, render_template
from flask import request, redirect
from datetime import timedelta
import app5auth #ログイン管理
import app4data #データ入出力

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分

@app.route('/')
def index():
    if not app5auth.is_login():
        return redirect('/login')
    return render_template('app4.html',
        user=app5auth.get_user(),
        data=app4data.load_data())

@app.route('/login')
def login():
    return render_template('app5auth.html')

@app.route('/check_login', methods=['POST'])
def check_login():
    user, password = None, None
    if 'user' in request.form:
        user = request.form['user']
    if 'password' in request.form:
        password = request.form['password']
    if (user is None) or (password is None):
        return redirect('/login')
    if not app5auth.login(user, password):
        return show_msg('ログインに失敗しました')
    return redirect('/')

@app.route('/logout')
def logout():
    app5auth.logout()
    return show_msg('ログアウトしました')

@app.route('/write', methods=['POST'])
def write():
    if not app5auth.is_login():
        return redirect('/login')
    bbs = request.form.get('bbs', '')
    if bbs == '':
        return show_msg('書込みが空でした。')
    app4data.save_data_append(
        user=app5auth.get_user(),
        text=bbs)
    return redirect('/')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user, password = None, None
        if 'user' in request.form:
            user = request.form['user']
        if 'password' in request.form:
            password = request.form['password']
        if (user is None) or (password is None):
            return show_msg('登録に失敗しました。')
        if not app5auth.add_user(user, password):
            return show_msg('登録済みユーザーです。')
        app5auth.login(user, password)
        return redirect('/')
    else:
        return render_template('app5signup.html')

def show_msg(msg):
    return render_template('msg.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)