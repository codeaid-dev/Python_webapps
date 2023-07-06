from flask import Flask, render_template, request
import random, csv

app = Flask(__name__)

@app.route('/drill15', methods=['GET','POST'])
def index():
    with open('data/kencho.csv', 'r') as f:
        data = csv.reader(f)
        ques, ans = [row for row in data]
        questions = dict(zip(ques,ans))
    if request.method == 'POST' and 'answer' in request.form:
        answer = request.form['kotae']
        question = request.form['question']
        if questions[question] == answer:
            result = '正解！！'
        else:
            result = f'不正解（正解：{questions[question]}）'
    else:
        question = random.choice(list(questions))
        answer = ''
        result = None
    return render_template('drill15.html', result=result, question=question, answer=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)