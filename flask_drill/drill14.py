from flask import Flask, request, render_template, make_response
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/drill14', methods=['GET','POST'])
def index():
    count = request.cookies.get('count')
    win = request.cookies.get('win')
    result = request.cookies.get('result')
    if request.method == 'POST' and 'pon' in request.form:
        if count:
            count = int(count)
            if count==5:
                count,win = 0,0
                result = ''
            count += 1
            you = request.form['you']
            com = random.choice(['ぐー','ちょき','ぱー'])
            print(you)
            if (you=='ぐー' and com=='ちょき') or (you=='ちょき' and com=='ぱー') or (you=='ぱー' and com=='ぐー'):
                result += f'{count}回目：あなたの勝ち（{you}：{com}）\n'
                win = int(win)
                win += 1
            elif (you=='ぐー' and com=='ぱー') or (you=='ちょき' and com=='ぐー') or (you=='ぱー' and com=='ちょき'):
                result += f'{count}回目：コンピューターの勝ち（{you}：{com}）\n'
            else:
                result += f'{count}回目：あいこ（{you}：{com}）\n'
            if count == 5:
                result += f'5戦中{win}勝です。'
            result = result.split('\n')
        else:
            count,win = 0,0
            result = []
    else:
        count,win = 0,0
        result = []
    response = make_response(render_template('drill14.html', result=result))
    max_age = 60 * 1
    expires = int(datetime.now().timestamp())+max_age
    response.set_cookie('count', value=str(count), max_age=max_age, expires=expires)
    response.set_cookie('win', value=str(win), max_age=max_age, expires=expires)
    response.set_cookie('result', value='\n'.join(result), max_age=max_age, expires=expires)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)