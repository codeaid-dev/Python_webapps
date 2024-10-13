from flask import Flask, request, render_template
from datetime import date,timedelta

app = Flask(__name__)

@app.route('/drill2', methods=['GET','POST'])
def index():
    if request.method == 'POST' and 'date' in request.form:
        year,month,day = map(int, request.form['date'].split('-'))
        next = date(year,month,day) + timedelta(days=1)
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            leap_year = True
        else:
            leap_year = False

        if month == 4 or month == 6 or month == 9 or month == 11:
            month_length = 30
        elif month == 2:
            if leap_year:
                month_length = 29
            else:
                month_length = 28
        else:
            month_length = 31

        if day < month_length:
            day += 1
        else:
            day = 1
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
        #msg = f'次の日は「{year}年{month:02d}月{day:02d}日」'
        msg = f'次の日は「{next.year}年{next.month:02d}月{next.day:02d}日」'
    else:
        msg = None

    return render_template('drill2.html', msg=msg)

if __name__ == '__main__':
    app.run(port='8000', debug=True)