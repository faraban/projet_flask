
from flask import Flask,url_for,render_template,request,flash,redirect,abort 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user 
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='clés_flash'

def connect_db():
    return sqlite3.connect('base_de_donnees.db')
con = connect_db()
cur = con.cursor()

Login_Manager=LoginManager()
Login_Manager.login_view='connexion'
Login_Manager.init_app(app)

@Login_Manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/',methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        cur.execute(f''' SELECT * FROM users WHERE email ='{email}'
                       ''')
        data = cur.fetchall()
        con.close()
        if data: 
            data=data[0]
            if check_password_hash(data[3],pwd):
                flash("email succès !", 'info')
                login_user(email,remember=True)
                return redirect(url_for('magasin'))
            else:
                flash("password incorrect!", 'info')
        else:
            flash("vous n'avez pas de compte !", 'info')
    return render_template('connexion.html')

@app.route('/deconnection',methods=['GET','POST'])
@login_required
def deconnection():
    logout_user()
    return redirect(url_for('connexion'))

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    if request.method == 'POST':
        Nom = request.form['nom']
        Mail = request.form['email']
        pwd1= request.form['Password1']
        pwd2 = request.form["Password2"]
        
        if len(Nom)<=2:
            flash('Entrez votre Nom','info')
        elif len(Mail)<=12:
            flash('Entrez un mail correct','')
        elif pwd1!=pwd2:
            flash('Entrez le même pass','')
        elif len(pwd2) <8 :
              flash('Entrez un pass d\'aumoins 8 caractere','')
        else:
            con = connect_db()
            cur = con.cursor()
            cur.execute('''
                        INSERT INTO users (name, email, password)
                        VALUES ( ?, ?, ?)
                        ''', (Nom, Mail,generate_password_hash(pwd1)))
            con.commit()
            con.close()
            flash('Vous êtes enregistrer avec succès, connectez-vous','succès')
            return redirect(url_for('connexion'))
    return render_template('inscription.html')

@app.route('/ajout', methods=['GET', 'POST'])
@login_required
def ajout():
    if request.method == 'POST':
         Nom = request.form['nom']
         Adresse = request.form['Adresse']
         Téléphone = request.form["Téléphone"]
         Mail = request.form['email']
         con = connect_db()
         cur = con.cursor()
         cur.execute('''
            INSERT INTO magasin (Nom, Adresse, Téléphone, Mail)
            VALUES ( ?, ?, ?, ?)
         ''', (Nom, Adresse, Téléphone, Mail))
         con.commit()
         con.close()
         flash("Votre magasin a été enregistré avec succès !", 'info')
         return redirect(url_for('magasin'))
    data=''
    return render_template('ajout.html',data=data)

@app.route('/magasin', methods=['GET', 'POST'])
@login_required
def magasin():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM magasin")
    data = cur.fetchall()
    con.close()
    return render_template('magasin.html', data=data)

@app.route('/modifier/<int:item_id>', methods=['GET', 'POST'])
@login_required
def modifier(item_id):
    item_id=int(item_id)
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM magasin WHERE id = ?", (item_id,))
    data = cur.fetchall()
    data=data[0]
    if request.method == 'POST':
         Nom = request.form['nom']
         Adresse = request.form['Adresse']
         Téléphone = request.form["Téléphone"]
         Mail = request.form['email']
         cur.execute(f'''
                    UPDATE magasin
                    SET (Nom, Adresse, Téléphone, Mail)={(Nom, Adresse, Téléphone, Mail)}
                    WHERE id = {item_id}
                    ''',)
         con.commit()
         con.close()
         flash(f" Le Magasin numero {item_id} a été modifieé avec succès !", 'info')
         return redirect(url_for('magasin'))
    return render_template('ajout.html', data=data)

@app.route('/supprimer/<int:item_id>', methods=['GET', 'POST'])
@login_required
def supprimer(item_id):
    if request.method == 'POST':
        item_id=int(item_id)
        con = connect_db()
        cur = con.cursor()
        cur.execute(f"DELETE FROM magasin WHERE id ={item_id};")
        con.commit()
        con.close()
        flash(f" Le Magasin numero {item_id} a été supprimer avec succès !", 'info')
        return redirect(url_for('magasin'))
    return render_template('supprimer.html')

if __name__ == "__main__":
    app.run(debug=True)