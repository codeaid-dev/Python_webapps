from fileinput import filename
from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id+5}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    #/projectsでアクセスすると/projects/にリダイレクトされる
    #そのため、/projectsと/projects/は/projects/にアクセスする
    return 'The project page'

@app.route('/about')
def about():
    #/aboutのみでアクセスできる
    #/about/でアクセスするとエラーとなる
    return 'The about page'

@app.route('/login')
def login():
    return 'login'

@app.route('/thanks/')
@app.route('/thanks/<name>')
def thanks(name=None):
    return render_template('thanks.html', name=name)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('show_post', post_id='55')) #post_idには整数に変換できるデータを代入
    print(url_for('show_subpath', subpath='<script>alert("bad")</script>')) #subpathはエスケープしてパスとなる
    print(url_for('projects'))
    print(url_for('static', filename='style.css')) #static/style.cssファイルが存在する必要がある

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
