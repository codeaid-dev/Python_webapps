from flask import Flask, render_template, request
import random

app = Flask(__name__)

hand = [None] * 5

def check_hand(hand):
    count = {i: hand.count(i) for i in set(hand)}  
    values = list(count.values())
    
    if 4 in values:
        return "フォーカード"
    elif 3 in values and 2 in values:
        return "フルハウス"
    elif values.count(2) == 2:
        return "ツーペア"
    elif 3 in values:
        return "スリーカード"
    elif 2 in values:
        return "ワンペア"
    else:
        return "ノーハンド"

@app.route('drill11/', methods=['GET', 'POST'])
def index():
    global hand
    if request.method == 'POST':
        button_id = request.form.get('button_id')
        if button_id is not None:
            button_index = int(button_id)
            if hand[button_index] is None:  
                hand[button_index] = random.randint(1, 5)

        hand_type = check_hand(hand) if None not in hand else " "
    else:
        hand = [None] * 5
        hand_type = ""

    return render_template('drill11_other.html', hand=hand, hand_type=hand_type)

if __name__ == '__main__':
    app.run(debug=True)
