from flask import Flask, render_template, request
import json, os

app = Flask(__name__)

filepath = 'data/meal.json'

@app.route('/drill17', methods=['GET','POST'])
def index():
    if os.path.exists(filepath) and os.path.getsize(filepath)!=0:
        with open(filepath, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    else:
        data = {}

    if request.method == 'POST':
        temp = {}
        record_date = request.form['date']
        temp['breakfast'] = request.form['breakfast']
        temp['lunch'] = request.form['lunch']
        temp['dinner'] = request.form['dinner']
        data[record_date] = temp
        with open(filepath, 'w', encoding='utf-8') as fh:
            json.dump(data,fh,sort_keys=True,ensure_ascii=False,indent=2)

    return render_template('drill17.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)