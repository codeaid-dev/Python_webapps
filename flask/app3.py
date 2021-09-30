from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

MESSAGE = './message.txt'

@app.route('/')
def index():
    msg = '書き込みはありません。'
    if os.path.exists(MESSAGE):
        with open(MESSAGE, 'r') as f:
            msg = f.read()

    return render_template('app3.html', msg=msg)

@app.route('/write', methods=['POST'])
def write():
    if 'msg' in request.form:
        msg = str(request.form['msg'])
        with open(MESSAGE, 'w') as f:
            f.write(msg)
    return redirect('/')

app.run(port=8000, debug=True)
