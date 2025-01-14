from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta
import os
#from base64 import b64encode

app = Flask(__name__)
#app.secret_key = b64encode(os.urandom(16)).decode() #セッション情報を暗号化するためのキー
app.secret_key = 'sLd+i2-jIa=sWa38' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(seconds=30) #セッション有効期限30秒

@app.route('/')
def index():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('session.html',username=username)

@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == '1234':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'パスワードが違います。'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port='8000', debug=True)
