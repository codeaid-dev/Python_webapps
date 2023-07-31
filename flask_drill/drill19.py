from flask import Flask, render_template, request
import json, os, re, hashlib
from werkzeug.security import generate_password_hash

app = Flask(__name__)

filepath = 'data/users.json'
SALT = 'hMLfe:i32n5j#Aiz'

def password_hash(password):
    code = password + SALT
    code = code.encode('utf-8')
    return hashlib.sha256(code).hexdigest()

@app.route('/drill19', methods=['GET','POST'])
def index():
    result = {}
    result['error'] = []
    if os.path.exists(filepath) and os.path.getsize(filepath)!=0:
        with open(filepath, 'r', encoding='utf-8') as fh:
            users = json.load(fh)
    else:
        users = {}
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        if username in users.keys():
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
            #users[username] = [email,password_hash(password)]
            users[username] = [email,generate_password_hash(password)]
            with open(filepath, 'w', encoding='utf-8') as fh:
                json.dump(users, fh, sort_keys=True, ensure_ascii=False, indent=2)
            result['success'] = '登録しました。'

    return render_template('drill19.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)