from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import hashlib, os
from base64 import b64encode, b64decode
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = b64encode(os.urandom(16)).decode() #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(seconds=30) #セッション有効期限30秒

def hash_password(password):
    salt = os.urandom(16) #16バイトのバイト列
    digest = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,10000)
    return b64encode(salt + digest).decode()

def verify_password(password, hash):
    b = b64decode(hash)
    salt, verify = b[:16], b[16:]
    digest = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,10000)
    return digest == verify

@app.route('/',methods=['GET','POST'])
def index():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('hash_sample.html',username=username)

@app.route('/signup', methods=['POST'])
def signup():
    if os.path.exists('hash_sample.json'):
        with open('hash_sample.json', 'r', encoding='utf-8') as fp:
            json_dict = json.load(fp)
    else:
        json_dict = {}
    username = request.form['username']
    #password = generate_password_hash(request.form['password'])
    password = hash_password(request.form['password'])
    json_dict[username] = password
    with open('hash_sample.json', 'w', encoding='utf-8') as fp:
        json.dump(json_dict, fp, sort_keys=True, ensure_ascii=False, indent=2)
    return render_template('hash_sample.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    username = ''
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if os.path.exists('hash_sample.json'):
            with open('hash_sample.json', 'r', encoding='utf-8') as fp:
                json_dict = json.load(fp)
        else:
            json_dict = {}
        username = request.form['username']
        for user in json_dict:
            if user == username:
                #if check_password_hash(json_dict[user], request.form['password']):
                if verify_password(request.form['password'], json_dict[user]):
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    error = 'ログイン失敗・パスワードが違います。'
                    break
        else:
            error = 'ログイン失敗・ユーザーが登録されていません。'
    return render_template('hash_sample.html', username=username, error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)