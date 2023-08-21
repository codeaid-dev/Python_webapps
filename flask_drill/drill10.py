from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/drill10', methods=['GET','POST'])
def index():
    genotype = ['AA','AO','BB','BO','AB','OO']
    if request.method == 'POST':
        mom = request.form['mother']
        dad = request.form['father']
        child = []
        for m in mom:
            for d in dad:
                child.append(f'{m}{d}')
        blood = []
        for ch in child:
            if ch == 'AA' or ch == 'AO' or ch == 'OA':
                blood.append('A型')
            elif ch == 'BB' or ch == 'BO' or ch == 'OB':
                blood.append('B型')
            elif ch == 'OO':
                blood.append('O型')
            else:
                blood.append('AB型')
        msg = 'と'.join(set(blood))
        msg = '子の血液型は'+msg+'の可能性があります。'
    else:
        msg = None
        mom = 'AA'
        dad = 'AA'

    return render_template('drill10.html', genotype=genotype, selectm=mom, selectf=dad, msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)