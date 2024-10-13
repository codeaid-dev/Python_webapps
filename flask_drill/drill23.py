from flask import Flask, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'Msd4EsJIk6AoVD3g' #セッション情報を暗号化するためのキー
app.permanent_session_lifetime = timedelta(minutes=10) #セッション有効期限10分

@app.route('/drill23', methods=['GET','POST'])
def index():
    username = ''
    password = ''
    error=''
    if 'username' in session:
        username = session['username']
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            if request.form['password'] == '1234':
                session['username'] = username
            else:
                error = 'ログイン失敗'
        if 'logout' in request.form:
            username = ''
            password = ''
            session.pop('username', None)

    return render_template('drill23.html',username=username,password=password,error=error)

if __name__ == '__main__':
    app.run(port='8000', debug=True)