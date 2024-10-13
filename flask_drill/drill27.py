from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3,os,json
from contextlib import closing
from datetime import timedelta

app = Flask(__name__)
basepath = os.path.dirname(__file__)
filepath = basepath+'/data/product.db'
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分

@app.route('/drill27', methods=['GET','POST'])
def index():
    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = true")
            cur.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product VARCHAR(256) NOT NULL,
                        price INTEGER NOT NULL
                        )''')
            cur.execute('''CREATE TABLE IF NOT EXISTS oder (
                        customer VARCHAR(256) NOT NULL,
                        pid INTEGER,
                        quantity INTEGER NOT NULL,
                        FOREIGN KEY(pid) REFERENCES products(id)
                        )''')
            conn.commit()
    except sqlite3.Error as e:
        print(e)

    result = ''
    if request.method == 'POST':
        if 'regist' in request.form:
            product = request.form['product']
            price = int(request.form['price'])
            try:
                with closing(sqlite3.connect(filepath)) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO products (product, price) VALUES (?, ?)',(product,price))
                    conn.commit()
                    result = '登録しました。'
            except sqlite3.Error as e:
                print(e)
        if 'delete' in request.form:
            id = request.form['id']
            product = request.form['product']
            try:
                with closing(sqlite3.connect(filepath)) as conn:
                    cur = conn.cursor()
                    cur.execute('PRAGMA foreign_keys = true')
                    cur.execute('DELETE FROM products WHERE id=?',(id,))
                    conn.commit()
                    result = f'{id}:{product}を削除しました。'
            except sqlite3.Error as e:
                print(e)

    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM products')
            data = cur.fetchall()
    except sqlite3.Error as e:
        print(e)

    return render_template('drill27-main.html',data=data,result=result)

@app.route('/drill27/cart', methods=['GET','POST'])
def cart():
    total = 0
    cart = {}
    products = {}
    customer = ''
    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM products')
            data = cur.fetchall()
            for d in data:
                products[str(d[0])] = {'product':d[1],'price':d[2],'quantity':0,'subtotal':0}
    except sqlite3.Error as e:
        print(e)

    if 'cart' in session:
        cart = json.loads(session['cart'])
    if request.method == 'POST':
        if 'add_to_cart' in request.form:
            session['customer'] = request.form['customer']
            customer = session['customer']
            ids = request.form.getlist('product_id')
            for id in ids:
                products[id]['quantity'] = int(request.form[f'quantity{id}'])
                if id in cart:
                    cart[id]['quantity'] += products[id]['quantity']
                else:
                    cart[id] = products[id]
                cart[id]['subtotal'] = cart[id]['price']*cart[id]['quantity']
            for product in cart.values():
                total += product['subtotal']
            session['cart'] = json.dumps(cart)
        elif 'del_from_cart' in request.form:
            session.pop('customer', None)
            session.pop('cart', None)
            return redirect(url_for('index'))
        elif 'oder' in request.form and 'customer' in session:
            customer = session['customer']
            for id,product in cart.items():
                quantity = product['quantity']
                try:
                    with closing(sqlite3.connect(filepath)) as conn:
                        cur = conn.cursor()
                        cur.execute('INSERT INTO oder (customer, pid, quantity) VALUES (?, ?, ?)',(customer,id,quantity))
                        conn.commit()
                except sqlite3.Error as e:
                    print(e)
            session.pop('customer', None)
            session.pop('cart', None)
            return redirect(url_for('result', customer=customer))

    return render_template('drill27-cart.html', products=products, customer=customer, cart=cart, total=int(total*1.1))

@app.route('/drill27/result/<customer>', methods=['GET','POST'])
def result(customer):
    products = {}
    total = 0
    try:
        with closing(sqlite3.connect(filepath)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM oder WHERE customer=?', (customer,))
            data = cur.fetchall()
            for row in data:
                products[row[1]] = {'quantity':row[2]}
            for pid in products.keys():
                cur.execute('SELECT * FROM products WHERE id=?', (pid,))
                data = cur.fetchall()
                for row in data:
                    products[pid]['product'] = row[1]
                    products[pid]['price'] = row[2]
                    products[pid]['subtotal'] = products[pid]['quantity']*row[2]
            for val in products.values():
                total += val['subtotal']

    except sqlite3.Error as e:
        print(e)

    if request.method == 'POST':
        try:
            with closing(sqlite3.connect(filepath)) as conn:
                cur = conn.cursor()
                cur.execute('DELETE FROM oder WHERE customer=?', (customer,))
                conn.commit()
        except sqlite3.Error as e:
            print(e)
        return redirect(url_for('index'))

    return render_template('drill27-result.html', products=products, customer=customer, total=int(total*1.1))



if __name__ == '__main__':
    app.run(port='8000', debug=True)