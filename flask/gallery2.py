from flask import Flask, render_template, request, flash, redirect, url_for
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = os.urandom(16)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        if file and allowed_file(file.filename):
            file.save(os.path.join('./static/images', file.filename))
            return redirect(url_for('gallery', page=1))
        else:
            flash('画像ファイルではありません。')
            return redirect(request.url)

    return render_template('upload1.html')

@app.route('/gallery/')
def gallery():
    kwargs = {}
    kwargs['page'] = int(request.args.get('page'))-1
    kwargs['msg'] = '画像はまだありません。'
    with os.scandir('./static/images') as it:
        entries = [entry.name for entry in it if entry.is_file()]
    entries.sort()
    cnt = len(entries)
    if cnt > 0:
        kwargs['msg'] = f'合計{cnt}枚の画像があります。'
        #2次元リストにページごとに画像ファイル名を格納
        kwargs['entries'] = [entries[i:i+2] for i in range(0,cnt,2)]
        kwargs['pages'] = len(kwargs['entries'])
    else:
        kwargs['pages'] = 0

    return render_template('gallery1.html', **kwargs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
