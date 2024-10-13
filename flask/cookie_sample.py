from flask import Flask, render_template, redirect, url_for
from flask import request, make_response
from datetime import datetime

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    count = request.cookies.get('count')
    if count is None:
        count = 1
    else:
        count = int(count)
        count += 1
    if 'clear' in request.form:
        max_age = 0
        expires = int(datetime.now().timestamp()) #すぐ削除
        response = make_response(redirect(url_for('index')))
    else:
        max_age = 20
        expires = int(datetime.now().timestamp())+20 #20秒
        response = make_response(render_template('cookie.html', count=count))
    response.set_cookie('count',
                        value=str(count),
                        max_age=max_age,
                        expires=expires)
    return response

if __name__ == '__main__':
    app.run(port='8000', debug=True)
