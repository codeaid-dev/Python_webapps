from flask import Flask, render_template, request
import json, os, re

app = Flask(__name__)

filepath = 'data/users.json'

@app.route('/drill18', methods=['GET','POST'])
def index():
    result = {}
    if os.path.exists(filepath) and os.path.getsize(filepath)!=0:
        with open(filepath, 'r', encoding='utf-8') as fh:
            users = json.load(fh)
    else:
        users = {}
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        rm = re.compile('[\w\-.]+@[\w\-.]+\.[a-zA-Z]+')
        m = re.match(rm,email)
        if m != None:
            if username in users.keys():
                result['error'] = '登録済みのユーザーです。'
            else:
                users[username] = email
                with open(filepath, 'w', encoding='utf-8') as fh:
                    json.dump(users, fh, sort_keys=True, ensure_ascii=False, indent=2)
                result['success'] = '登録しました。'
        else:
            result['error'] = '無効なメールアドレスです。'

    return render_template('drill18.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)