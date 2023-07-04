from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/drill4', methods=['GET','POST'])
def index():
    if request.method == 'POST' and 'measure' in request.form:
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / ((height/100)**2)
        if bmi < 16:
            result = '痩せすぎ'
        elif 16.0 <= bmi <= 16.99:
            result = '痩せ'
        elif 17.0 <= bmi <= 18.49:
            result = '痩せぎみ'
        elif 18.50 <= bmi <= 24.99:
            result = '普通体重'
        elif 25.0 <= bmi <= 29.99:
            result = '前肥満'
        elif 30.0 <= bmi <= 34.99:
            result = '肥満(1度)'
        elif 35.0 <= bmi <= 39.99:
            result = '肥満(2度)'
        else:
            result = '肥満(3度)'
        msg = f'BMI値：{bmi:.2f}　判定：{result}です。'
    else:
        msg = None
    return render_template('drill4.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)