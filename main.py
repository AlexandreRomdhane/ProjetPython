from flask import Flask, session, redirect, url_for, request, render_template
from markupsafe import escape
import pymysql.cursors
import bcrypt
from email_validator import validate_email, EmailNotValidError
import re
from datetime import date

app = Flask(__name__)

app.secret_key = "OuiBiensurquecestsecretsinonsasersarien"

requestSQLIfUserExist = "SELECT NomUtilisateur FROM utilisateur WHERE Mail = %s"
requestSQLInsertUser = "INSERT INTO utilisateur (Mail, MotDePasse, NomUtilisateur, DateCreation) VALUES (%s, %s, %s, %s)"
requestSQLLoginUser = "SELECT UtilisateurID, MotDePasse, NomUtilisateur FROM utilisateur WHERE Mail = %s"

charLengthRegex = re.compile(r'(\w{8,})')
upperRegex = re.compile(r'[A-Z]+')


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
        return 'Tu es connecté en tant que %s' % escape(session['id'])
    return redirect(url_for('login'))


# Route pour s'enregistrer, GET pour avoir le formulaire et POST pour soumettre les données
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if not session.get('id') is None:
            return redirect(url_for('index'))
        else:
            return render_template('register.html')
    else:
        error = []  # Liste des erreurs a passer a la template
        try:
            # Valide l'adresse email si elle n'est pas valide une exception seras lancée (EmailNotValidError)
            error = check_password(request.form['password'])
            if len(request.form['user']) == 0:
                error.append("Le nom d'utilisateur ne doit pas être vide !")
            validate_email(request.form['email'])
            if len(error) == 0:  # Si il y a aucune erreur alors on continue
                with connectionDB.cursor() as cur:
                    # On regarde en base si le compte n'existe pas en fonction de l'adresse mail
                    cur.execute(requestSQLIfUserExist, request.form['email'])
                    if cur.rowcount == 0:  # Si aucun enregistrement ne correspond alors on crée le compte
                        with connectionDB.cursor() as cursorInsert:
                            # On enregistre l'utilisateur en base en hashant sont mot de passe
                            cursorInsert.execute(requestSQLInsertUser,
                                                 (request.form['email'],
                                                  bcrypt.hashpw(request.form['password'].encode('utf8'),
                                                  bcrypt.gensalt()),
                                                  request.form['user'],
                                                  date.today()))
                            connectionDB.commit()  # Permet de valider la transaction
                            return redirect(url_for('login'))  # Une fois finis on le redirige vers la page de connexion
                    else:
                        # Si l'adresse mail est déjà utilisée
                        # TODO Faire une fonction pour éviter de faire plusieurs fois le même traitement
                        error.append('Le compte existe déjà')
                        return render_template('register.html'
                                               , error=error
                                               , email=request.form['email'], user=request.form['user'])
            else:
                # TODO Faire une fonction pour éviter de faire plusieurs fois le même traitement
                return render_template('register.html'
                                       , error=error
                                       , email=request.form['email'], user=request.form['user'])
        except pymysql.Error as e:
            # En cas d'erreur voir sur internet pour mieux les gérer
            print(e)
            error.append('Une erreur SQL est arrivée')
            return render_template('register.html', error=error)
        except EmailNotValidError as e:
            error.append("L'adresse email n'est pas valide !")
            # TODO Faire une fonction pour éviter de faire plusieurs fois le même traitement
            return render_template('register.html'
                                   , error=error
                                   , email=request.form['email'], user=request.form['user'])


# Route pour se connecter, GET pour avoir le formulaire et POST pour soumettre les données
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = []
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
                        return redirect(url_for('index'))  # Page du fil d'actualité
                    else:
                        error.append("Le mot de passe ou l'adresse email n'est pas valide !")
                        return render_template('login.html', error=error, email=request.form['email'])
                else:
                    error.append("Le mot de passe ou l'adresse n'est pas valide !")
                    return render_template('login.html', error=error, email=request.form['email'])
        except pymysql.Error as e:
            # En cas d'erreur voir sur internet pour mieux les gérer
            print(e)
            error.append("Erreur SQL")
            return render_template('login.html', error=error, email=request.form['email'])
    else:
        if not session.get('id') is None:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


# Déconnexion du compte
@app.route("/logout")
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))


def check_password(password):
    val_ret = []
    if not charLengthRegex.findall(password):
        val_ret.append("Le mot de passe doit contenir au moins 8 caractères !")
    if not upperRegex.findall(password):
        val_ret.append("Le mot de passe doit contenir au moins une majuscule !")
    return val_ret
