from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/drill3', methods=['GET','POST'])
def index():
    seiza = ['山羊座','水瓶座','魚座','牡羊座','牡牛座','双子座','蟹座','獅子座','乙女座','天秤座','蠍座','射手座']
    date = [19,18,20,19,20,21,22,22,22,23,22,21]
    if request.method == 'POST':
        month = int(request.form['month'])
        day = int(request.form['day'])
        if month == 2 and day >= 30:
            day = 29
        elif month in [4,6,9,11] and day >= 31:
            day = 30
        if date[month-1] >= day:
            msg = f'{month}月{day}日は{seiza[month-1]}です'
        else:
            msg = f'{month}月{day}日は{seiza[month%12]}です'
    else:
        msg = None
    return render_template('drill3.html', msg=msg)

if __name__ == '__main__':
    app.run(port='8000', debug=True)