from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/drill7', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        color = 0
        colors = request.form.getlist('colors')
        print(colors)
        if 'red' in colors:
            color += 1
        if 'green' in colors:
            color += 2
        if 'blue' in colors:
            color += 4
        if color == 1:
            make = '赤'
        elif color == 2:
            make = '緑'
        elif color == 3:
            make = '黄'
        elif color == 4:
            make = '青'
        elif color == 5:
            make = 'マゼンタ'
        elif color == 6:
            make = 'シアン'
        elif color == 7:
            make = '白'
        else:
            make = '黒'
        msg = f'作れる色は：{make}'
    else:
        msg = None
        colors = []

    return render_template('drill7.html', msg=msg, colors=colors)

if __name__ == '__main__':
    app.run(port='8000', debug=True)