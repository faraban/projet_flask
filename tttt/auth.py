
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user


@login_required
@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Déconnexion réussie', 'info')
    return redirect(url_for('connexion'))

from . import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
     return User.get(user_id)




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         login_user(user)
#         flash('Logged in successfully.')
#         next = request.args.get('next')
#         if not url_has_allowed_host_and_scheme(next, request.host):
#             return abort(400)
#         return redirect(next or url_for('index'))
#     return render_template('login.html', form=form)

# @app.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')
#     user = User.query.filter_by(email=email).first() # if this returns a user, t
#     if user: # if a user is found, we want to redirect back to signup page so us
#         return redirect(url_for('auth.signup'))
#     # create a new user with the form data. Hash the password so the plaintext v
#     new_user = User(email=email, name=name, password=generate_password_hash(pass))

#     db.session.add(new_user)
#     db.session.commit()
#     return redirect(url_for('auth.login'))

# @app.route('/login', methods=['POST'])
# def login_post():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False
#     user = User.query.filter_by(email=email).first()
#     # check if the user actually exists
#     # take the user-supplied password, hash it, and compare it to the hashed pas
#     if not user or not check_password_hash(user.password, password):
#         flash('Please check your login details and try again.')
#         return redirect(url_for('auth.login')) # if the user doesn't exist or pa
#     # if the above check passes, then we know the user has the right credentials
#     return redirect(url_for('main.profile'))

# class Utilisateur(UserMixin):
#     def __init__(self, id, nom):
#         self.id = id
#         self.nom = nom

#     # Vous devrez implémenter des méthodes pour récupérer l'utilisateur par ID et éventuellement pour vérifier les mots de passe.
