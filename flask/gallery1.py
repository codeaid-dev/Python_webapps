from flask import Flask, render_template, request
import os

app = Flask(__name__)

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
