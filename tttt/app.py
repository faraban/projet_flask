
from flask import Flask,url_for,render_template,request,flash,redirect
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='clés_flash'
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

def connect_db():
    return sqlite3.connect('base_de_donnees.db')

class Utilisateur(UserMixin):
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    # Vous devrez implémenter des méthodes pour récupérer l'utilisateur par ID et éventuellement pour vérifier les mots de passe.


@app.route('/',methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
          # Vérifiez les informations d'authentification ici (par exemple, vérifiez le nom d'utilisateur et le mot de passe)
        # Si l'authentification réussit, créez un objet Utilisateur et connectez l'utilisateur
        utilisateur = Utilisateur(id=1, nom='utilisateur_test')
        login_user(utilisateur)
        flash('Connexion réussie', 'success')
        nom = request.form['nom']
        email = request.form['email']
        return redirect(url_for('magasin'))
    return render_template('connexion.html')

@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Déconnexion réussie', 'info')
    return redirect(url_for('connexion'))

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