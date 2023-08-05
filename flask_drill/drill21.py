from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import json

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分

products = {
  '0':{'name':'商品1', 'price':1000, 'quantity':0, 'subtotal':0},
  '1':{'name':'商品2', 'price':2000, 'quantity':0, 'subtotal':0},
  '2':{'name':'商品3', 'price':3000, 'quantity':0, 'subtotal':0}
}

@app.route('/test', methods=['GET','POST'])
def index():
    total = 0
    cart = {}
    if 'cart' in session:
        cart = json.loads(session['cart'])
    if request.method == 'POST':
        if 'add_to_cart' in request.form:
            ids = request.form.getlist('product_id')
            for id in ids:
                products[id]['quantity'] = int(request.form[f'quantity{id}'])
                if id in cart:
                    cart[id]['quantity'] += products[id]['quantity']
                else:
                    cart[id] = products[id]
                cart[id]['subtotal'] = cart[id]['price']*cart[id]['quantity']
            for product in cart.values():
                print(cart)
                total += product['subtotal']
            session['cart'] = json.dumps(cart)
        elif 'del_from_cart' in request.form:
            session.pop('cart', None)
            return redirect(url_for('index'))

    return render_template('drill21.html', products=products, cart=cart, total=int(total*1.1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)