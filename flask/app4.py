from flask import Flask, render_template
from flask import request, redirect
from datetime import timedelta
import app4auth #ログイン管理
import app4data #データ入出力

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分

@app.route('/')
def index():
    if not app4auth.is_login():
        return redirect('/login')
    return render_template('app4.html',
        user=app4auth.get_user(),
        data=app4data.load_data())

@app.route('/login')
def login():
    return render_template('app4auth.html')

@app.route('/check_login', methods=['POST'])
def check_login():
    user, password = None, None
    if 'user' in request.form:
        user = request.form['user']
    if 'password' in request.form:
        password = request.form['password']
    if (user is None) or (password is None):
        return redirect('/login')
    if not app4auth.login(user, password):
        return show_msg('ログインに失敗しました')
    return redirect('/')

@app.route('/logout')
def logout():
    app4auth.logout()
    return show_msg('ログアウトしました')

@app.route('/write', methods=['POST'])
def write():
    if not app4auth.is_login():
        return redirect('/login')
    bbs = request.form.get('bbs', '')
    if bbs == '':
        return show_msg('書込みが空でした。')
    app4data.save_data_append(
        user=app4auth.get_user(),
        text=bbs)
    return redirect('/')

def show_msg(msg):
    return render_template('msg.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)