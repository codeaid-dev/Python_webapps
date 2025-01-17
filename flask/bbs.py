from flask import Flask, render_template
from flask import request, redirect
from datetime import timedelta
import bbs_auth #ログイン管理
import bbs_data #データ入出力

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分

@app.route('/')
def index():
    if not bbs_auth.is_login():
        return redirect('/login')
    return render_template('bbs.html',
        user=bbs_auth.get_user(),
        data=bbs_data.load_data())

@app.route('/login')
def login():
    return render_template('bbs_auth.html')

@app.route('/check_login', methods=['POST'])
def check_login():
    user, password = None, None
    if 'user' in request.form:
        user = request.form['user']
    if 'password' in request.form:
        password = request.form['password']
    if (user is None) or (password is None):
        return redirect('/login')
    if not bbs_auth.login(user, password):
        return show_msg('ログインに失敗しました')
    return redirect('/')

@app.route('/logout')
def logout():
    bbs_auth.logout()
    return show_msg('ログアウトしました')

@app.route('/write', methods=['POST'])
def write():
    if not bbs_auth.is_login():
        return redirect('/login')
    bbs = request.form.get('bbs', '')
    if bbs == '':
        return show_msg('書込みが空でした。')
    bbs_data.save_data_append(
        user=bbs_auth.get_user(),
        text=bbs)
    return redirect('/')

def show_msg(msg):
    return render_template('msg.html', msg=msg)

if __name__ == '__main__':
    app.run(port='8000', debug=True)