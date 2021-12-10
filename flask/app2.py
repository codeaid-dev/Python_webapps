from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('app2.html')

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None or name == '':
        name = '名無し'
    return render_template('app2_hello.html', name=name)

app.run(port=8000, debug=True)
