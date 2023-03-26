from flask import Flask

app = Flask(__name__)

@app.route('/projects/')
def projects():
    return 'プロジェクトページ'

@app.route("/about")
def about():
    return 'サイトについて'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)