from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/user/<username>')
def show_user(username):
    return f'ユーザー名 {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'投稿番号 {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'サブパス {escape(subpath)}'

if __name__ == '__main__':
    app.run(port='8000', debug=True)