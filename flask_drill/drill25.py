from flask import Flask, render_template, request
import re, hashlib
from werkzeug.security import generate_password_hash
import sqlite3
from contextlib import closing

app = Flask(__name__)

SALT = 'hMLfe:i32n5j#Aiz'

def password_hash(password):
    code = password + SALT
    code = code.encode('utf-8')
    return hashlib.sha256(code).hexdigest()

@app.route('/drill25', methods=['GET','POST'])
def index():
    try:
        with closing(sqlite3.connect('data/users.db')) as conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR(256) PRIMARY KEY,
                        email VARCHAR(256),
                        password VARCHAR(256)
                        )''')
    except sqlite3.Error as e:
        print(e)

    result = {}
    result['error'] = []
    users = []
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        try:
            with closing(sqlite3.connect('data/users.db')) as conn:
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
                with closing(sqlite3.connect('data/users.db')) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',(username,email,password))
                    conn.commit()
            except sqlite3.Error as e:
                print(e)

            result['success'] = '登録しました。'

    return render_template('drill25.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)