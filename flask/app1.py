from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    menu = [
        {'item':'コーヒー', 'price':340},
        {'item':'パンケーキ', 'price':750},
        {'item':'クレープ', 'price':600},
    ]
    return render_template('app1.html', menu=menu)

if __name__ == '__main__':
    app.run(port='8000', debug=True)