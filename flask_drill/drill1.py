from flask import Flask, request, url_for, render_template
import random

app = Flask(__name__)

@app.route('/drill1', methods=['GET','POST'])
def index():
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        uranai = random.randint(1,10)
        if 1 == uranai:
            result = '今日は最高'
        elif 2 <= uranai <= 4:
            result = '今日はそこそこ'
        elif 5 <= uranai <= 8:
            result = '今日はまぁまぁ'
        else:
            result = '今日は最悪・・・'
        msg = f'{name}さんの運勢「{result}」'
    else:
        msg = None
    return render_template('drill1.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)