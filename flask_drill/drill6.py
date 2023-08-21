from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/drill6', methods=['GET','POST'])
def index():
    if request.method == 'POST' and 'split' in request.form:
        total = int(request.form['total'])
        people = int(request.form['people'])
        fraction = int(request.form['fraction'])
        result = [{'person':'参加者','number':people-1,'price':0},
                  {'person':'代表','number':1,'price':0},
                  {'person':'合計','number':people,'price':0}]
        surplus = (total//people)%100
        if surplus == 0:
            result[0]['price'] = total // people
            result[1]['price'] = total // people
        elif fraction == 1:
            price = total // people
            result[0]['price'] = (price//100)*100
            result[1]['price'] = total - result[0]['price']*(people-1)
        else:
            price = total // people
            result[0]['price'] = (price//100)*100+100
            result[1]['price'] = total - result[0]['price']*(people-1)
        result[2]['price'] = total
    else:
        result = None
        fraction = None

    return render_template('drill6.html', data=result, fraction=fraction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)