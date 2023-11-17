from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=1) #セッション有効期限1分

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
            error = 'ログインに失敗しました。'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    session.pop('username', None)
    return render_template('logout.html', username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
