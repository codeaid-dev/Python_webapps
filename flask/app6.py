from flask import Flask, render_template
from flask import request, make_response
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    count = request.cookies.get('count')
    if count is None:
        count = 0
    else:
        count = int(count)
    count += 1
    response = make_response(render_template('cookies.html', count=count))
    max_age = 60 * 10 #10分
    expires = int(datetime.now().timestamp())+max_age
    response.set_cookie('count', value=str(count), max_age=max_age, expires=expires)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
