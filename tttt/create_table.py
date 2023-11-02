import sqlite3

def connect_db():
    return sqlite3.connect('base_de_donnees.db')

con = connect_db()
cur = con.cursor()

cur.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR,
    email VARCHAR UNIQUE,
    password VARCHAR
    );''')

con.close()
