
from flask import Flask,url_for,render_template,request,flash,redirect,abort,session
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='clés_flash'
session={'user':''}

def connect_db():
    return sqlite3.connect('base_de_donnees.db')

@app.route('/',methods=['GET', 'POST'])
def connexion():
    if session['user']:
        return redirect(url_for('magasin'))
    else:
        reg='Connectez-vous'
        if request.method == 'POST':
            email = request.form['email']
            pwd = request.form['Password1']
            con = connect_db()
            cur = con.cursor()
            cur.execute(f''' SELECT * FROM users WHERE email ='{email}'
                        ''')
            data = cur.fetchall()
            con.close()
            if data: 
                data=data[0]
                if check_password_hash(data[3],pwd):
                    flash("email succès !", 'info')
                    session['user']=f'{data[2]}'
                    return redirect(url_for('magasin'))
                else:
                    flash("password incorrect!", 'info')
            else:
                flash("vous n'avez pas de compte !", 'info')
        return render_template('form.html',reg=reg)

@app.route('/deconnexion',methods=['GET','POST'])
def deconnexion():
    session['user']=''
    return redirect(url_for('connexion'))

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    if session['user']:
        return redirect(url_for('magasin'))
    else:
        inscrip='Registration'
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
        return render_template('form.html',inscrip=inscrip)

@app.route('/ajout/<string:type>', methods=['GET', 'POST'])
def ajout(type):
    if session['user']:
        if type=='produit':
            if request.method == 'POST':
                IdProduit=request.form['nom']
                NomProduit = request.form['Adresse']
                CatProduit = request.form["Téléphone"]
                PrixUnitaire = request.form["email"]
                
                con = connect_db()
                cur = con.cursor()
                cur.execute('''
                    INSERT INTO Produit (IdProduit,NomProduit, CatProduit, PrixUnitaire)
                    VALUES ( ?, ?,?, ?)
                ''', (IdProduit,NomProduit, CatProduit, PrixUnitaire))
                con.commit()
                con.close()
                flash("Votre produit a été ajouté avec succès !", 'info')
                return redirect(url_for('produit'))
            produit='produit'
            titre='Ajouter un nouveau Produit'
            entete=['IdProduit :','NomProduit :','CatProduit :','PrixUnitaire :']
            interieur=['IdProduit','NomProduit','CatProduit','PrixUnitaire']
            data=''
            return render_template('ajout.html',data=data,entete=entete,interieur=interieur,titre=titre,produit=produit)
        else:
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
            magasin='magasin'
            titre='Ajouter un nouveau Magasin'
            entete=['Nom :','Adresse :','Téléphone :','Email :']
            interieur=['Nom','Adresse','Téléphone','Email']
            data=''
            return render_template('ajout.html',data=data,entete=entete,interieur=interieur,titre=titre,magasin=magasin)
    else:
        return redirect(url_for('connexion'))

@app.route('/magasin', methods=['GET', 'POST'])
def magasin():
    if session['user']:
        cat='magasin'
        entete=['Id','Nom','Adresse','Téléphones','Mail','Action']
        titre='liste des magasins'
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM magasin")
        data = cur.fetchall()
        con.close()
        return render_template('table.html', data=data,entete=entete,titre=titre,cat=cat)
    else:
        return redirect(url_for('connexion'))

@app.route('/produit', methods=['GET', 'POST'])
def produit():
    if session['user']:
        cat='produit'
        entete=['IdProduit','NomProduit','CatProduit','PrixUnitaire','Action']
        titre='liste des Produit'
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM Produit")
        data = cur.fetchall()
        con.close()
        return render_template('table.html', data=data,entete=entete,titre=titre,cat=cat)
    else:
        return redirect(url_for('connexion'))

@app.route('/modifier/<int:item_id>/<string:type>', methods=['GET', 'POST'])
def modifier(item_id,type):
    if session['user']:
        if type=='produit':
            item_id=int(item_id)
            produit='produit'
            con = connect_db()
            cur = con.cursor()    
            cur.execute("SELECT * FROM produit WHERE IdProduit = ?", (item_id,))
            data = cur.fetchall()
            data=data[0]
            titre='Ajouter un nouveau Produit'
            entete=['IdProduit :','NomProduit :','CatProduit :','PrixUnitaire :']
            interieur=['IdProduit','NomProduit','CatProduit','PrixUnitaire']
            if request.method == 'POST':
                IdProduit=request.form['nom']
                NomProduit = request.form['Adresse']
                CatProduit = request.form["Téléphone"]
                PrixUnitaire = request.form["email"]
                cur.execute(f'''
                        UPDATE produit
                        SET (IdProduit,NomProduit, CatProduit, PrixUnitaire)={(IdProduit,NomProduit, CatProduit, PrixUnitaire)}
                        WHERE IdProduit = {item_id}
                        ''',)
                con.commit()
                con.close()
                flash(f" Le Magasin numero {item_id} a été modifieé avec succès !", 'info')
                return redirect(url_for('magasin'))
            return render_template('ajout.html', data=data,entete=entete,interieur=interieur,titre=titre,produit=produit)
        else:
            item_id=int(item_id)
            magasin='magasin'
            con = connect_db()
            cur = con.cursor()    
            cur.execute("SELECT * FROM magasin WHERE id = ?", (item_id,))
            data = cur.fetchall()
            data=data[0]
            titre='Ajouter un nouveau Magasin'
            entete=['Nom :','Adresse :','Téléphone :','Email :']
            interieur=['Nom','Adresse','Téléphone','Email']
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
            return render_template('ajout.html', data=data,entete=entete,interieur=interieur,titre=titre,magasin=magasin)
    else:
        return redirect(url_for('connexion'))

@app.route('/supprimer/<int:item_id>/<string:type>', methods=['GET', 'POST'])
def supprimer(item_id,type):
    if session['user']:
        if type=='produit':
            produit='produit'
            if request.method == 'POST':
               item_id=int(item_id)
               con = connect_db()
               cur = con.cursor()
               cur.execute(f"DELETE FROM produit WHERE IdProduit ={item_id};")
               con.commit()
               flash(f" Le Magasin numero {item_id} a été supprimer avec succès !", 'info')
               return redirect(url_for('produit'))
            return render_template('supprimer.html',produit=produit)
        else:
            magasin='magasin'
            if request.method == 'POST':
               item_id=int(item_id)
               con = connect_db()
               cur = con.cursor()
               cur.execute(f"DELETE FROM magasin WHERE id ={item_id};")
               con.commit()
               flash(f" Le Magasin numero {item_id} a été supprimer avec succès !", 'info')
               return redirect(url_for('magasin'))
            return render_template('supprimer.html',magasin=magasin)
    else:
        return redirect(url_for('connexion'))

if __name__ == "__main__":
    app.run(debug=True)