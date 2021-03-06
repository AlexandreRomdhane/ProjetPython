import re
from flask import Flask, session, redirect, url_for, request, render_template, jsonify
import bcrypt
from email_validator import validate_email, EmailNotValidError
from follow import follow, unfollow
from markupsafe import escape


from db import get_info_user_by_id, get_account_if_exist_by_email, get_post_user_by_username, register_account, add_post, delete_post, get_account_if_exist_by_username

app = Flask(__name__)

app.secret_key = "OuiBiensurquecestsecretsinonsasersarien"

charLengthRegex = re.compile(r'(\w{8,})')
upperRegex = re.compile(r'[A-Z]+')


@app.route("/")
def index():
    if 'id' in session:
        return render_template('index.html')
        # return 'Tu es connecté en tant que %s' % escape(session['id'])
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
                password_hash = bcrypt.hashpw(request.form['password'].encode('utf8'),
                                              bcrypt.gensalt())
                if register_account(request.form['email'], password_hash, request.form['user']):
                    # Compte bien enregistré
                    return redirect(url_for('login'))  # Une fois finis on le redirige vers la page de connexion
                else:
                    error.append('Le compte existe déjà')
                    return render_template('register.html'
                                           , error=error
                                           , email=request.form['email'], user=request.form['user'])
            else:
                return render_template('register.html'
                                       , error=error
                                       , email=request.form['email'], user=request.form['user'])
        except EmailNotValidError as e:
            error.append("L'adresse email n'est pas valide !")
            return render_template('register.html'
                                   , error=error
                                   , email=request.form['email'], user=request.form['user'])


# Route pour se connecter, GET pour avoir le formulaire et POST pour soumettre les données
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = []
        # Faire la vérification
        result_user = get_account_if_exist_by_email(request.form['email'])
        if result_user is not None:  # Si l'utilisateur existe alors
            if bcrypt.checkpw(request.form['password'].encode('utf8'), result_user['MotDePasse'].encode('utf8')):
                # Le mot de passe est correcte
                session['id'] = result_user['UtilisateurID']
                return redirect(url_for('index'))  # Page du fil d'actualité
            else:
                # Le mot de passe ne correspond pas
                error.append("Le mot de passe ou l'adresse email n'est pas valide !")
                return render_template('login.html', error=error, email=request.form['email'])
        else:  # Si il n'existe pas alors
            error.append("Le mot de passe ou l'adresse n'est pas valide !")
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


@app.route("/profil/<username>")
def show_profil(username):
    if 'id' in session:
        if get_account_if_exist_by_username(username):
            result = get_info_user_by_id(session.get('id'))
            if result is not None:
                if username != result['NomUtilisateur']:
                    return render_template('profil.html', name=escape(username))
                else:
                    return render_template('profil.html', name=escape(username), same_user_than_profil=True)
            else:
                print("Erreur innatendue (id de session pas présent dans la base)")
                return redirect(url_for('login'))
        else:
            return render_template('not_found.html')
    else:
        return redirect(url_for('login'))


# L'utilisateur de la session va suivre l'utilisateur user
@app.route("/profil/<username>/follow")
def follow_user(username):
    return follow(username)


# L'utilisateur de la session va arrete de suivre l'utilsateur user
@app.route("/profil/<username>/unfollow")
def unfollow_user(username):
    return unfollow(username)


# API ne doit être appelé en POST et GET qu'avec le JS
@app.route('/api/post', methods=['GET', 'POST', 'DELETE'])
def post():
    response_json_post = {}
    if request.method == 'GET':
        all_post_user = get_post_user_by_username(request.args.get('username'))
        if all_post_user is not None:
            response_json_post = {'errors': False, 'message': '', 'post': all_post_user}
            return jsonify(response_json_post)
        else:
            response_json_post = {'errors': False, 'message': "Il n'y a aucun post", 'post': {}}
            return jsonify(response_json_post)
    elif request.method == 'POST':  # Post
        if add_post(session.get('id'), request.form['namePost'], request.form['contentPost']):
            response_json_post = {'errors': False, 'message': 'Le post a bien été crée !'}
            return jsonify(response_json_post)
        else:
            response_json_post = {'errors': True, 'message': 'Impossible de créer le post !'}
            return jsonify(response_json_post)
    elif request.method == 'DELETE':
        if delete_post(session.get('id'), int(request.form['postID'])):
            # Le post a bien été supprimé
            response_json_post = {'errors': False, 'message': 'Le post a bien été supprimé !'}
            return jsonify(response_json_post)
        else:
            response_json_post = {'errors': True, 'message': 'Impossible de supprimer le post !'}
            return jsonify(response_json_post)


@app.route("/api/user")
def get_user_by_session_id():
    if session.get('id') is not None:
        # print(session.get('id'))
        result_user = get_info_user_by_id(session.get('id'))

        if result_user is not None:
            response_json = {'errors': False, 'message': 'Utilisateur trouvé !',
                             'username': result_user['NomUtilisateur']}
            return response_json
        else:
            response_json = {'errors': True, 'message': 'Utilisateur non trouvé vérifiez l\'identifiant !',
                             'username': ''}
            return response_json
    else:
        response_json = {'errors': True, 'message': 'Une erreur c\'est produite lors de la récupération du cookie de '
                                                    'session !', 'username': ''}
        return response_json


def check_password(password):
    val_ret = []
    if not charLengthRegex.findall(password):
        val_ret.append("Le mot de passe doit contenir au moins 8 caractères !")
    if not upperRegex.findall(password):
        val_ret.append("Le mot de passe doit contenir au moins une majuscule !")
    return val_ret
