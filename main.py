from flask import Flask, session, redirect, url_for, request
from markupsafe import escape
import pymysql.cursors
import bcrypt

app = Flask(__name__)

app.secret_key = "OuiBiensurquecestsecretsinonsasersarien"

requestSQLIfUserExist = "SELECT NomUtilisateur FROM utilisateur WHERE Mail = %s"
requestSQLInsertUser = "INSERT INTO utilisateur (Mail, MotDePasse, NomUtilisateur) VALUES (%s, %s, %s)"
requestSQLLoginUser = "SELECT UtilisateurID, MotDePasse, NomUtilisateur FROM utilisateur WHERE Mail = %s"


# Fonction qui renvoie la connexion a la base (interface)
def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='memecontainer',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


connectionDB = get_connection()  # Objet de la connexion MySQL


@app.route("/")
def index():
    if 'id' in session:
        return 'Logged in as %s' % escape(session['id'])
    return redirect(url_for('login'))


# Route pour s'enregistrer, GET pour avoir le formulaire et POST pour soumettre les données
# TODO Faire une vérif sur la force du mot de passe avant de l'enregistrer
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Formulaire d'enregistrement (a faire dans un template)
        return '''
                <form method="post">
                    <p><input type=text name=email>
                    <p><input type=password name=password>
                    <p><input type=text name=user>
                    <p><input type=submit value=Register>
                </form>
            '''
    else:
        try:
            with connectionDB.cursor() as cur:
                # On regarde en base si le compte n'existe pas en fonction de l'adresse mail
                cur.execute(requestSQLIfUserExist, request.form['email'])
                if cur.rowcount == 0:  # Si aucun enregistrement ne correspond alors on crée le compte
                    with connectionDB.cursor() as cursorInsert:
                        # On enregistre l'utilisateur en base en hashant sont mot de passe
                        cursorInsert.execute(requestSQLInsertUser,
                                             (request.form['email'],
                                              bcrypt.hashpw(request.form['password'].encode('utf8'), bcrypt.gensalt()),
                                              request.form['user']))
                        connectionDB.commit()  # Permet de valider la transaction
                        return redirect(url_for('login'))  # Une fois finis on le redirige vers la page de connexion
                else:
                    # Si l'adresse mail est déjà utilisée
                    return 'Le compte existe déjà'
        except pymysql.Error as e:
            # En cas d'erreur voir sur internet pour mieux les gérer
            print(e)
            return 'Erreur'


# Route pour se connecter, GET pour avoir le formulaire et POST pour soumettre les données
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Faire la vérification
        try:
            with connectionDB.cursor() as cursorLogin:
                # On récupère les informations de connexions de l'utilisateur qui tente de se connecter
                cursorLogin.execute(requestSQLLoginUser, request.form['email'])
                # On vérifie que son compte existe
                if cursorLogin.rowcount != 0:
                    result = cursorLogin.fetchone()  # On récupère qu'un seul enregistrement
                    if bcrypt.checkpw(request.form['password'].encode('utf8'), result['MotDePasse'].encode('utf8')):
                        # Le mot de passe est correcte
                        session['id'] = result['UtilisateurID']
                        return 'Tu es connecté !'
                    else:
                        return "Le mot de passe n'est pas correcte !"
                else:
                    return "Le compte n'existe pas !"
        except pymysql.Error as e:
            # En cas d'erreur voir sur internet pour mieux les gérer
            print(e)
            return "Erreur"
    else:
        if not session.get('id') is None:
            return redirect(url_for('index'))
        else:
            # Formulaire de connexion (a faire dans un template)
            return '''
                    <form method="post">
                        <p><input type=text name=email>
                        <p><input type=password name=password>
                        <p><input type=submit value=Login>
                    </form>
                '''


# Déconnexion du compte
@app.route("/logout")
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))
