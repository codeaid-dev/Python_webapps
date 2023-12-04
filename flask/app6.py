from flask import Flask, render_template, redirect, url_for
from flask import request, make_response
from datetime import datetime

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    count = request.cookies.get('count')
    if count is None:
        count = 0
    else:
        count = int(count)
    count += 1
    if 'clear' in request.form:
        max_age = 0 #すぐ削除
        count = 0
    else:
        max_age = 20 #20秒
    expires = int(datetime.now().timestamp())+max_age
    response = make_response(
        render_template('cookie.html', count=count))
    response.set_cookie('count',
                        value=str(count),
                        max_age=max_age,
                        expires=expires)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
