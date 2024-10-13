from flask import Flask, request
import sqlite3, os, json

base_path = os.path.dirname(os.path.abspath(__file__))
db_path = base_path + '/zip.db'
form_path = base_path + '/zipform.html'

app = Flask(__name__)

@app.route('/')
def index():
    with open(form_path) as f:
        return f.read()

@app.route('/api')
def api():
    q = request.args.get('q', '')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT pref,city,addr FROM zip WHERE code=?', [q])
    items = c.fetchall()
    conn.close()
    res = []
    for i, r in enumerate(items):
        pref,city,addr = r[0],r[1],r[2]
        res.append(pref + city + addr)
        print(q, ':', pref + city + addr)
    return json.dumps(res)

if __name__ == '__main__':
    app.run(port='8000', debug=True)
