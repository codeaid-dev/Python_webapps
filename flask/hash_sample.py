from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import random, string, hashlib, os
import json
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(seconds=30) #セッション有効期限30秒
SALT = 'uMoJL3h90SenH7:r' #パスワード保存時に使用するソルト値

def to_hash(password):
    password += SALT #SALTを加える
    text = password.encode('utf-8')
    hash = hashlib.sha256(text).hexdigest()
    return hash

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
    #password = to_hash(request.form['password'])
    password = generate_password_hash(request.form['password'])
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
        #password = to_hash(request.form['password'])
        for user in json_dict:
            if user == username:
                if check_password_hash(json_dict[user], request.form['password']):
                #if password == json_dict[user]:
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