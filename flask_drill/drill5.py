from flask import Flask, request, render_template
import random

app = Flask(__name__)

@app.route('/drill5', methods=['GET','POST'])
def index():
    nums = [1,2,3,4,5,6]
    colors = ['赤','黒']
    num, color, bet, msg = None,None,None,None
    if request.method == 'POST':
        com_num = random.choice(nums)
        com_color = random.choice(colors)
        num = int(request.form['nums'])
        color = request.form['colors']
        bet = int(request.form['bets'])
        result = 0
        if bet == 1:
            bet_str = '数字と色の組み合わせ'
            if com_num == num and com_color == color:
                result = 100
        elif bet == 2:
            bet_str = '数字のみ'
            if com_num == num:
                result = 50
        else:
            bet_str = '色のみ'
            if com_color == color:
                result = 20
        msg = f'あなたの選択：数字({num}) 色({color}) 賭ける種類({bet_str})<br>'
        msg += f'コンピューターの選択：数字({com_num}) 色({com_color})<br>'
        msg += f'結果：{result}点'
    #else:
    #    msg = None
    return render_template('drill5.html', num=num,color=color,bet=bet,msg=msg)

if __name__ == '__main__':
    app.run(port='8000', debug=True)