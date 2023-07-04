from flask import Flask, request, render_template
import random

app = Flask(__name__)

@app.route('/drill12', methods=['GET','POST'])
def index():
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!@#$%^&*()_+-=[]\{\};:,.<>?'
    if request.method == 'POST' and 'generate' in request.form:
        digit = request.form['digit']
        if digit.isdigit() and 8<=int(digit)<=32:
            digit = int(digit)
            char = random.choice(list(lower))
            char += random.choice(list(upper))
            char += random.choice(list(numbers))
            char += random.choice(list(symbols))
            password = char
            for i in range(digit-len(char)):
                password += random.choice(list(lower+upper+numbers+symbols))
            password = ''.join(random.sample(password, len(password)))
            error = None
        else:
            password = None
            error = '桁数は8~32の整数を入力してください。'
    else:
        password = None
        error = None

    return render_template('drill12.html', password=password, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)