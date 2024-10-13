from flask import Flask, request, render_template
import random

app = Flask(__name__)

cards = [0]*5
@app.route('/drill11', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        for i in range(5):
            if f'btn{i+1}' in request.form and cards[i]==0:
                num = random.randint(1,5)
                while cards.count(num) >= 4:
                    num = random.randint(1,5)
                cards[i] = num
        print(cards)
        if not 0 in cards:
            hand = {}
            for n in cards:
                if n not in hand.keys():
                    hand[n] = cards.count(n)

            val = list(hand.values())
            if 4 in val:
                msg = 'フォーカード'
            elif 2 in val and 3 in val:
                msg = 'フルハウス'
            elif 3 in val:
                msg = 'スリーカード'
            elif val.count(2) == 2:
                msg = 'ツーペア'
            elif val.count(2) == 1:
                msg = 'ワンペア'
            else:
                msg = 'ノーハンド'
        else:
            msg = None
    else:
        for i in range(len(cards)):
            cards[i]=0
        msg = None

    return render_template('drill11.html', msg=msg, cards=cards)

if __name__ == '__main__':
    app.run(port='8000', debug=True)