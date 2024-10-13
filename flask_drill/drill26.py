from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
import re, hashlib
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from contextlib import closing

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分
basepath = os.path.dirname(__file__)
filepath = basepath+'/data/users.db'

SALT = 'hMLfe:i32n5j#Aiz'

def password_hash(password):
    code = password + SALT
    code = code.encode('utf-8')
    return hashlib.sha256(code).hexdigest()

@app.route('/drill26', methods=['GET','POST'])
def index():
    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR(256) PRIMARY KEY,
                        email VARCHAR(256),
                        password VARCHAR(256)
                        )''')
    except sqlite3.Error as e:
        print(e)

    if 'username' in session:
        username = session['username']
        return render_template('drill26-main.html',username=username)
    else:
        return redirect(url_for('login'))

@app.route('/drill26/login', methods=['GET','POST'])
def login():
    error = ''
    users = []
    if 'username' in session:
        username = session['username']
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with closing(sqlite3.connect(filepath)) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username=?',(username,))
                users = cur.fetchall()
        except sqlite3.Error as e:
            print(e)

        if users:
            #if user[0][2] == password_hash(password):
            if not check_password_hash(users[0][2],password):
                error = 'パスワードが違います。'
        else:
            error = 'ユーザー名が存在しましせん。'

        if not error:
            session['username'] = username
            return redirect(url_for('index'))
    
    return render_template('drill26-login.html',error=error)

@app.route('/drill26/logout')
def logout():
    username = session['username']
    session.pop('username', None)
    return render_template('drill26-logout.html', username=username)

@app.route('/drill26/signup', methods=['GET','POST'])
def signup():
    result = {}
    result['error'] = []
    users = []
    if 'username' in session:
        username = session['username']
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        try:
            with closing(sqlite3.connect(filepath)) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username=?',(username,))
                users = cur.fetchall()
        except sqlite3.Error as e:
            print(e)

        for user in users:
            if username in user:
                result['error'].append('登録済みのユーザーです。')
        comp = re.compile('[\w\-.]+@[\w\-.]+\.[a-zA-Z]+')
        m = re.match(comp,email)
        if m == None:
            result['error'].append('無効なメールアドレスです。')
        password = request.form['password']
        comp = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\W_])[\w\W]{8,32}$')
        m = re.match(comp,password)
        if m == None:
            result['error'].append('パスワードは8~32文字で大小文字英字数字記号をそれぞれ1文字以上含める必要があります。')
        if not result['error']:
            #password = password_hash(password)
            password = generate_password_hash(password)
            try:
                with closing(sqlite3.connect(filepath)) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',(username,email,password))
                    conn.commit()
            except sqlite3.Error as e:
                print(e)

            result['success'] = '登録しました。'

    return render_template('drill26-signup.html', result=result)

if __name__ == '__main__':
    app.run(port='8000', debug=True)