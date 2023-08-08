from flask import Flask, render_template, request, make_response, redirect, url_for, session
import sqlite3,os
from contextlib import closing

app = Flask(__name__)
basepath = os.path.dirname(__file__)
filepath = basepath+'/data/product.db'

@app.route('/drill24', methods=['GET','POST'])
def index():
    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product VARCHAR(256) NOT NULL,
                        price INTEGER NOT NULL
                        )''')
    except sqlite3.Error as e:
        print(e)

    result = ''
    if request.method == 'POST':
        product = request.form['product']
        price = int(request.form['price'])
        print(product, price)
        try:
            with closing(sqlite3.connect(filepath)) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO products (product, price) VALUES (?, ?)',(product,price))
                conn.commit()
                result = '登録しました。'
        except sqlite3.Error as e:
            print(e)

    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM products')
            data = cur.fetchall()
    except sqlite3.Error as e:
        print(e)

    return render_template('drill24.html',data=data,result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)