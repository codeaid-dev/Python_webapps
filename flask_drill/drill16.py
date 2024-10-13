from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/drill16', methods=['GET','POST'])
def index():
    zips = []
    result = {'zip1':'','zip2':'','city':'','place':''}
    with open('data/27OSAKA.csv', 'r', encoding='shift-jis') as f:
        data = csv.reader(f)
        for row in data:
            zip = {}
            zip['zipcode'] = row[2]
            zip['city'] = row[7]
            zip['place'] = row[8]
            zips.append(zip)
    if request.method == 'POST' and 'ziptocity' in request.form:
        zip1 = request.form['zip1']
        zip2 = request.form['zip2']
        for zip in zips:
            if zip['zipcode'] == zip1+zip2:
                result['zip1'] = zip1
                result['zip2'] = zip2
                result['city'] = zip['city']
                result['place'] = zip['place'] if zip['place'] != '以下に掲載がない場合' else ''
                break
    elif request.method == 'POST' and 'citytozip' in request.form:
        city = request.form['city']
        place = request.form['place']
        for zip in zips:
            if zip['city'] == city and (zip['place'] == place or place == ''):
                result['zip1'] = zip['zipcode'][:3]
                result['zip2'] = zip['zipcode'][3:]
                result['city'] = city
                result['place'] = place
                break
    return render_template('drill16.html', result=result)

if __name__ == '__main__':
    app.run(port='8000', debug=True)