from flask import Flask, render_template
from flask import request, redirect, session
import os, json, datetime
import app4_login # ログイン管理
import app4_data # データ入出力

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' # セッション情報を暗号化するためのキー

@app.route('/')
def index():
    if not app4_login.is_login():
        return redirect('/login')
    return render_template('index.html',
        user=app4_login.get_user(),
        data=app4_data.load_data())

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/check_login', methods=['POST'])
def check_login():
    user, pw = None, None
    if 'user' in request.form:
        user = request.form['user']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (user is None) or (pw is None):
        return redirect('/login')
    if not app4_login.login(user, pw):
        return show_msg('ログインに失敗しました')
    return redirect('/')

@app.route('/logout')
def logout():
    app4_login.logout()
    return show_msg('ログアウトしました')

@app.route('/write', methods=['POST'])
def write():
    if not app4_login.is_login():
        return redirect('/login')
    bbs = request.form.get('bbs', '')
    if bbs == '':
        return show_msg('書込みが空でした。')
    app4_data.save_data_append(
        user=app4_login.get_user(),
        text=bbs)
    return redirect('/')

def show_msg(msg):
    return render_template('msg.html', msg=msg)

app.run(port=8000, debug=True)
