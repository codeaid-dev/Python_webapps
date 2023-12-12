from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import os
import imghdr

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.secret_key = os.urandom(16)

def allowed_file(file, name=True):
    if name:
        return '.' in file and \
               file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    else:
        if '.' in file.filename and \
               file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            return imghdr.what(file.stream) in ALLOWED_EXTENSIONS
        else:
            return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # POST送信にファイルアップロードのデータがあるか確認
        if 'file' not in request.files:
            flash('ファイルデータがありません。')
            return redirect(request.url)
        file = request.files['file']
        # ファイルを選択せずアップロードしたときにはファイル名が空となる
        if file.filename == '':
            flash('ファイルが選択されていません。')
            return redirect(request.url)
        # ファイル名をチェックして画像ファイルか確認
        if file and allowed_file(file,name=False):
            filename = file.filename.rsplit('.', 1)[0] + '_' + datetime.now().strftime('%Y%m%d%H%M%S')
            filename += '.' + file.filename.rsplit('.', 1)[1]
            file.save(os.path.join('./static/images', filename))
            return redirect(url_for('gallery', page=1))
        else:
            flash('画像ファイルではありません。')
            return redirect(request.url)

    return render_template('upload3.html')

@app.route('/gallery/')
def gallery():
    kwargs = {}
    kwargs['page'] = int(request.args.get('page'))-1
    kwargs['msg'] = '画像はまだありません。'
    with os.scandir('./static/images') as it:
        entries = [entry.name for entry in it if entry.is_file() and allowed_file(entry.name)]
    entries.sort()
    cnt = len(entries)
    if cnt > 0:
        kwargs['msg'] = f'合計{cnt}枚の画像があります。'
        #2次元リストにページごとに画像ファイル名を格納
        kwargs['entries'] = [entries[i:i+2] for i in range(0,cnt,2)]
        kwargs['pages'] = len(kwargs['entries'])
    else:
        kwargs['pages'] = 0

    return render_template('gallery3.html', **kwargs)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    kwargs = {}
    kwargs['msg'] = '画像はまだありません。'
    with os.scandir('./static/images') as it:
        entries = [entry.name for entry in it if entry.is_file() and allowed_file(entry.name)]
    entries.sort()
    cnt = len(entries)
    if cnt > 0:
        kwargs['msg'] = f'合計{cnt}枚の画像があります。'
        kwargs['entries'] = entries

    if request.method == 'POST':
        if 'files' in request.form:
            files = request.form.getlist('files')
        for fn in files:
            os.remove('./static/images/'+fn)
        return redirect(request.url)

    return render_template('delete.html', **kwargs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)