import sqlite3
def connect_db():
    return sqlite3.connect('base_de_donnees.db')
con = connect_db()
cur = con.cursor()
cur.execute("SELECT * FROM magasin WHERE id = ?", (3,))
data = cur.fetchall()
data=data[0]
print(data[2])

