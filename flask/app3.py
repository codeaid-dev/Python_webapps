from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

MESSAGE = './message.txt'

@app.route('/')
def index():
    msg = '書き込みはありません。'
    if os.path.exists(MESSAGE):
        with open(MESSAGE, 'r' ,encoding='utf-8', newline='') as f:
            msg = f.read()
        #msg = msg.replace('\n', '<br>')

    return render_template('app3.html', msg=msg)

@app.route('/write', methods=['POST'])
def write():
    if 'msg' in request.form:
        msg = str(request.form['msg'])
        with open(MESSAGE, 'w',encoding='utf-8', newline='') as f:
            f.write(msg)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)