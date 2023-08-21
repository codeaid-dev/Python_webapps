from flask import Flask, render_template, request
import csv,os,re

app = Flask(__name__)
filepath = 'data/survey.csv'

@app.route('/drill22', methods=['GET','POST'])
def index():
    programlist = ['PHP','JavaScript','Python','Java','C/C++','C#','Ruby']
    pclist = ['デスクトップPC','ノートPC']
    makerlist = ['Lenovo','DELL','HP','Apple','Dynabook','NEC','VAIO','ASUS','自作PC','その他']
    programdict = {k:'' for k in programlist}
    pcdict = {pclist[0]:'checked',pclist[1]:''}
    makerdict = {k:'' for k in makerlist}
    vals = ['','','',programdict,pcdict,makerdict,'']
    errors = []
    normal = ''
    survey = []
    if os.path.exists(filepath) and os.path.getsize(filepath)!=0:
        with open(filepath, 'r') as f:
            data = csv.reader(f)
            for s in data:
                survey.append(s)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        program = request.form.getlist('program')
        pc = request.form['pc']
        maker = request.form['maker']
        comments = request.form['comments']
        for s in survey:
            if email in s:
                errors.append('このメールアドレスはすでに回答済みです。')
        if not maker:
            errors.append('PCメーカーを選択してください。')
        comp = re.compile('[\w\-.]+@[\w\-.]+\.[a-zA-Z]+')
        m = re.match(comp,email)
        if m == None:
            errors.append('正しいメールアドレスを入力してください。')
        if not errors:
            if survey:
                survey.append([name,email,age,'|'.join(program),pc,maker,comments])
            else:
                survey.append(['名前','メールアドレス','年齢','興味のあるプログラミング言語','学習に使っているパソコン','パソコンメーカー','コメント'])
                survey.append([name,email,age,'|'.join(program),pc,maker,comments])
            with open(filepath, 'w') as f:
                out = csv.writer(f)
                out.writerows(survey)
                normal = '送信しました。'
        programdict = {k:'checked' if k in program else '' for k in programlist}
        pcdict = {k:'checked' if pc == k else '' for k in pclist}
        makerdict = {k:'selected' if maker == k else '' for k in makerlist}
        vals = [name,email,age,programdict,pcdict,makerdict,comments]

    return render_template('drill22.html',vals=vals,errors=errors,normal=normal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)