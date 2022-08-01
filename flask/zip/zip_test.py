import sqlite3

code = input('ZIP code >>')

conn = sqlite3.connect('zip.db')

c = conn.cursor()
res = c.execute('SELECT * FROM zip WHERE code=?', [code])
for row in res:
    print(row)