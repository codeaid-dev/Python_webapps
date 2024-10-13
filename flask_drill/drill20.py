from flask import Flask, render_template, request, make_response
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/drill20', methods=['GET','POST'])
def index():
    result = ''
    question = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    corrects = []
    if request.method == 'POST':
        if 'question' in request.form:
            chars = int(request.form['chars'])
            for i in range(chars):
                correct = random.choice(question)
                corrects.append(correct)
                question = question.replace(correct,'')
            response = make_response(render_template('drill20-2.html',corrects=corrects, question=question))
            max_age = 60 * 10 #10分
            expires = int(datetime.now().timestamp())+max_age
            response.set_cookie('corrects',value=','.join(corrects),max_age=max_age,expires=expires)
            response.set_cookie('question',value=question,max_age=max_age,expires=expires)
            response.set_cookie('start',value=str(datetime.now().timestamp()),max_age=max_age,expires=expires)
            return response

        elif 'answer' in request.form:
            question = request.cookies.get('question')
            corrects = request.cookies.get('corrects').split(',')
            spend = datetime.now().timestamp()-float(request.cookies.get('start'))
            answers = list(map(str.upper,request.form['answer'].split(',')))
            print(answers,corrects)
            if set(corrects) == set(answers):
                result = f'正解です。[{",".join(corrects)}]'
            else:
                result = f'不正解です。正解は[{",".join(corrects)}]'
            return render_template('drill20-2.html',result=result,corrects=corrects, question=question,exec_time=int(spend))
    else:
        return render_template('drill20-1.html')

if __name__ == '__main__':
    app.run(port='8000', debug=True)