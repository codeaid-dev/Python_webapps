from flask import Flask, request
import os, json, hashlib, sqlite3

app = Flask(__name__)
base_path = os.path.dirname(__file__)
json_path = base_path + '/users.json'
db_path = base_path + '/users.db'

# データベースにテーブルを作成
def create_db():
    con = sqlite3.connect(db_path)
    con.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name TEXT NOT NULL PRIMARY KEY,
        pass TEXT NOT NULL
    )
    ''')
    con.commit()
    con.close()

# データベースを開く
def open_db():
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    return con

# SELECT句の結果を辞書型で獲得する
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# SQLを実行
def exec(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    db.commit()
    result = c.lastrowid
    c.close()
    return result

# SQLのSELECT句を実行を想定（結果を取得する）
def select(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    result = c.fetchall()
    c.close()
    return result

HASH_SALT = 'f0XFlh:Z5xp%@0?POsmNG@:@mkHkL3:S'

def password_hash(password):
    key = password + HASH_SALT
    key_b = key.encode('utf-8')
    return hashlib.sha256(key_b).hexdigest()

def load_users_json():
    if os.path.exists(json_path):
        with open(json_path, 'rt') as fp:
            return json.load(fp)
    return {}

def load_users_sqlite(id, password):
    if os.path.exists(db_path):
        result = select('SELECT * FROM users WHERE name=? AND pass=?', id, password_hash(password))
        if len(result) != 0:
            print(result)
            return result[0]
    return {}

def add_user(id, password, sv):
    if sv == 1:
        users = load_users_json()
        if id in users:
            return False
        users[id] = password_hash(password)
        with open(json_path, 'wt', encoding='utf-8') as fp:
            json.dump(users, fp)

    else:
        users = load_users_sqlite(id, password)
        if len(users) != 0:
            return False
        exec('INSERT INTO users (name, pass) VALUES (?,?)', id, password_hash(password))
    return True

def check_login(id, password, sv):
    if sv == 1:
        users = load_users_json()
        if id not in users:
            return False
        result = (password_hash(password) == users[id])
    else:
        users = load_users_sqlite(id, password)
        if len(users) == 0:
            return False
        result = True

    return result

@app.route('/')
def index():
    create_db()
    return f'''
    <html><meta charset="utf-8"><body>
    <h3>ユーザー登録</h3> {get_form('/register', '登録')} <hr>
    <h3>ユーザーログイン</h3> {get_form('/login', 'ログイン')}
    </body></html>
    '''

def get_form(action, caption):
    return f'''
    <form action="{action}" method="post">
    ID:<br>
    <input type="text" name="id"><br>
    パスワード:<br>
    <input type="password" name="pw"><br>
    保存先:<br>
    <input type="radio" name="sv" value="1" checked>JSON
    <input type="radio" name="sv" value="2">SQLite<br><br>
    <button type="submit">{caption}</button>
    </form>
    '''

@app.route('/register', methods=['POST'])
def register():
    id = request.form.get('id')
    pw = request.form.get('pw')
    sv = request.form.get('sv')
    if id == '':
        return '<h1>失敗:IDが空です。</h1>'
    if add_user(id, pw, sv):
        return '<h1>登録に成功</h1><a href="/">戻る</a>'
    else:
        return '<h1>登録に失敗</h1>'

@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    sv = request.form.get('sv')
    if id == '':
        return '<h1>失敗:IDが空です。</h1>'
    if check_login(id, pw, sv):
        return '<h1>ログインに成功</h1>'
    else:
        return '<h1>失敗</h1>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
