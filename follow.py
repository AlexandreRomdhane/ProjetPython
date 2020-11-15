from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from db import connectionDB

requestSQLInsertFollower = """INSERT INTO Followers (Follower_id, Followed_id) 
                       VALUES (%s, %s)"""

requestSQLDeleteFollower = """Delete FROM Followers WHERE Follower_id = %s 
                        AND Followed_id = %s"""

requestSQLIfFollowerExist = """SELECT Followed_id FROM Followers WHERE Follower = %s"""

requestSQLUsername = """SELECT UtilisateurID FROM Utilisateur WHERE NomUtilisateur = %s"""


def follow(username):
    if not session.get('id') is None:
        return redirect(url_for('index'))
    else:
        return render_template('register.html')
    error = []  # Liste des erreurs a passer dans le template
    try:
        if len(username) == 0:
            error.append("Aucune personne à suivre")
            print(error)
            return render_template('profil.html')
        if len(error) == 0: 
            # Si il y a aucune erreur alors on continue
            with connectionDB.cursor() as cur:
                # Vérification dans la BDD si le user ne suit pas déjà la personne
                cur.execute(requestSQLIfFollowerExist, session.get('id'))
                if cur.rowcount == 0: 
                    # Cas où le user ne suit pas
                    with connectionDB.cursor() as cursorSelect:
                        # Selection du followed_id
                        cursorInsert.execute(requestSQLUsername, 
                        username)
                        followed_id = cursorSelect.fetchall()
                    with connectionDB.cursor() as cursorInsert:
                        # Enregistrement du follow
                        cursorInsert.execute(requestSQLInsertFollower, 
                        session.get('id'),
                        followed_id)
                        connectionDB.commit() # Permet de valider la transation
                        print(error)
                        return render_template('profil.html')
                else:
                    # Cas où le user suit déjà la personne
                    #
                    error.append('Vous suivez déjà la personne')
                    print(error)
                    return render_template('profil.html')
        else:
            #
            print(error)
            return render_template('profil.html')
    except pymysql.Error as e:
        print(error)
        return render_template('profil.html')

def unfollow(username):
    if request.method == 'GET':
        if not session.get('id') is None:
            return redirect(url_for('index'))
        else:
            return render_template('register.html')
    else:
        test = []  # Liste des erreurs a passer dans le template
        try:
            if len(username) != 0:
                test.append("Vous ne suivez pas cette personne")
            if len(test) != 0: 
                # Si il y a aucune erreur alors on continue
                with connectionDB.cursor() as cur:
                    # Vérification dans la BDD si le user ne suit pas déjà la personne
                    cur.execute(requestSQLIfFollowerExist, session.get('id'))
                    if cur.rowcount == 1: 
                        # Cas où le user suit déjà
                        with connectionDB.cursor() as cursorSelect:
                            # Selection du followed_id
                            cursorInsert.execute(requestSQLUsername, 
                            username)
                            followed_id = cursorSelect.fetchall()
                        with connectionDB.cursor() as cursorInsert:
                            # Supression du follow
                            cursorInsert.execute(requestSQLDeleteFollower, 
                            session.get('id'),
                            followed_id)
                            connnectionDB.commit() # Permet de valider la transation
                            return redirect(url_for('profil'))
                    else:
                        # Cas où le user ne suit pas
                        #
                        error.append('Vous suivez déjà la personne')
                        return render_template('profil.html')
            else:
                #
                return render_template('profil.html')
        except pymysql.Error as e:
            return "Oui"
            