import re, photo_file
from photo_sqlite import exec, select

# 新規アルバム作成
def album_new(user_id, args):
    name = args.get('name', '')
    if name == '': return 0
    album_id = exec(
        'INSERT INTO albums (name, user_id) VALUES (?,?)', name, user_id
    )
    return album_id

# 特定ユーザーのアルバム一覧
def get_albums(user_id):
    return select(
        'SELECT * FROM albums WHERE user_id=?', user_id
    )

# 特定のアルバム情報取得
def get_album(album_id):
    a = select(
        'SELECT * FROM albums WHERE album_id=?', album_id
    )
    if len(a) == 0: return None
    return a[0]

# アルバム名取得
def get_album_name(album_id):
    a = get_album(album_id)
    if a == None: return '未分類'
    return a['name']

# アップロードされたファイルを保存
def save_file(user_id, upfile, album_id):
    # JPEGファイルだけを許可
    if not re.search(r'\.(jpg|jpeg)$', upfile.filename):
        print('JPEGではない：', upfile.filename)
        return 0
    # アルバム未指定の場合、未分類アルバムを自動的につくる
    if album_id == 0:
        a = select(
            'SELECT * FROM albums '+'WHERE user_id=? AND name=?', user_id, '未分類'
        )
        if len(a) == 0:
            album_id = exec(
                'INSERT INTO albums '+'(user_id, name) VALUES (?,?)', user_id, '未分類'
            )
        else:
            album_id = a[0]['album_id']
    # ファイル情報を保存
    file_id = exec(
        '''INSERT INTO files (user_id, filename, album_id) VALUES (?,?,?)''',
        user_id, upfile.filename, album_id
    )
    # ファイルを保存
    upfile.save(photo_file.get_path(file_id))
    return file_id

# ファイルに関する情報を取得
def get_file(file_id, ptype):
    # データベースから基本情報を獲得
    a = select('SELECT * FROM files WHERE file_id=?', file_id)
    if len(a) == 0: return None
    p = a[0]
    p['path'] = photo_file.get_path(file_id)
    # サムネイル画像の指定であれば作成
    if ptype == 'thumb':
        p['path'] = photo_file.make_thumbnail(file_id, 300)
    return p

# ファイル一覧を取得
def get_files():
    a = select('SELECT * FROM files ' + 'ORDER BY file_id DESC LIMIT 50')
    for i in a:
        i['name'] = get_album_name(i['album_id'])
    return a

# アルバムに入っているファイルの一覧
def get_album_files(album_id):
    return select('SELECT * FROM files WHERE album_id=? ORDER BY file_id DESC', album_id)

# ユーザーのファイルの一覧
def get_user_files(user_id):
    a = select('SELECT * FROM files WHERE user_id=? ORDER BY file_id DESC LIMIT 50', user_id)
    for i in a:
        i['name'] = get_album_name(i['album_id'])
    return a