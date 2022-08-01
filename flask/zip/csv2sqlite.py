import sqlite3, csv

FILE_SQLITE = 'zip.db'

conn = sqlite3.connect(FILE_SQLITE)
conn.execute('''
CREATE TABLE IF NOT EXISTS zip (
    zip_id INTEGER PRIMARY KEY,
    code TEXT,
    pref TEXT,
    city TEXT,
    addr TEXT
)
''')

conn.execute('DELETE FROM zip')

def read_csv(fname):
    c = conn.cursor()
    f = open(fname, encoding='cp932')
    reader = csv.reader(f)
    for row in reader:
        code = row[2]
        pref = row[6]
        city = row[7]
        addr = row[8]
        if addr == '以下に掲載がない場合':
            addr = ''
        print(code, pref, city, addr)
        c.execute(
            'INSERT INTO zip (code,pref,city,addr) ' +
            'VALUES (?,?,?,?)',
            [code,pref,city,addr])
    f.close()
    conn.commit()

read_csv('KEN_ALL.csv')
conn.close()
print('ok')