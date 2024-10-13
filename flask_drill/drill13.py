from flask import Flask, render_template, request, make_response, redirect, url_for
from datetime import datetime
import random

app = Flask(__name__)

national_flags = {'ベルギー':'images/Belgium.png',
                  'ブルガリア':'images/Bulgaria.png',
                  'デンマーク':'images/Denmark.png',
                  'フィンランド':'images/Finland.png',
                  'ドイツ':'images/Germany.png',
                  'ハンガリー':'images/Hungary.png',
                  'イタリア':'images/Italy.png',
                  'モナコ':'images/Monaco.png',
                  'ポーランド':'images/Poland.png',
                  'スウェーデン':'images/Sweden.png'}

@app.route('/drill13', methods=['GET','POST'])
def index():
    if request.method == 'POST' and 'answer' in request.form:
        question = request.cookies.get('question')
        if question == None:
            return redirect(url_for('index'))
        qflag = national_flags[question]
        answer = request.form['kotae']
        if question == answer:
            result = '正解！！'
        else:
            result = f'不正解（正解：{question}）'
    else:
        question = random.choice(list(national_flags))
        qflag = national_flags[question]
        answer = ''
        result = None
    response = make_response(render_template('drill13.html', qflag=qflag, result=result, answer=answer))
    max_age = 60 * 1
    expires = int(datetime.now().timestamp())+max_age
    response.set_cookie('question', value=question, max_age=max_age, expires=expires)
    return response

if __name__ == '__main__':
    app.run(port='8000', debug=True)