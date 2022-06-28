import sqlite3, photo_file

# データベースを開く
def open_db():
    conn = sqlite3.connect(photo_file.DATA_FILE)
    conn.row_factory = dict_factory
    return conn

# SELECT句の結果を辞書型で獲得する
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# SQLを実行
def exec(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    db.commit()
    return c.lastrowid

# SQLのSELECT句を実行を想定（結果を取得する）
def select(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    return c.fetchall()