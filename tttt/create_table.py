# import sqlite3

# def connect_db():
#     return sqlite3.connect('base_de_donnees.db')
# con = connect_db()
# cur = con.cursor()

# # cur.execute('''CREATE TABLE users (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     name VARCHAR,
# #     email VARCHAR UNIQUE,
# #     password VARCHAR
# #     );''')

# cur.execute('''CREATE TABLE Produit (
# IdProduit INT NOT NULL PRIMARY KEY,
# NomProduit VARCHAR(20),
# CatProduit VARCHAR(20),
# PrixUnitaire FLOAT
# );''')

# # cur.execute('''CREATE TABLE Magasin(
# # IdMagasin INT NOT NULL PRIMARY KEY ,
# # NomMagasin VARCHAR(20),
# # AdresseMagasin VARCHAR(50),
# # Telephone VARCHAR(16),
# # mail VARCHAR(20)
# # );''')

# cur.execute('''CREATE TABLE Stock (
# Idstock INT NOT NULL PRIMARY KEY ,
# Quantitestock INT ,
# IdProduit INT NOT NULL,
# IdMagasin INT NOT NULL,
# FOREIGN KEY  (IdProduit) REFERENCES Produit (IdProduit),
# FOREIGN KEY (IdMagasin) REFERENCES Magasin (id)
# );''')

# cur.execute('''CREATE TABLE Vente (
# IdVente INT NOT NULL PRIMARY KEY,
# Quantitevendu INT ,
# Prixtotal FLOAT,
# Datevente DATE,
# IdProduit INT NOT NULL,
# IdMagasin INT NOT NULL,
# FOREIGN KEY  (IdProduit) REFERENCES Produit (IdProduit),
# FOREIGN KEY (IdMagasin) REFERENCES Magasin (id)
# );''')

# con.close()