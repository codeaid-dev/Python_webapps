from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta
import random, string

app = Flask(__name__)
#app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) #セッション情報を暗号化するためのキー
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
    app.run(host='0.0.0.0', debug=True)
