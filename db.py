import pymysql.cursors
from datetime import date

requestSQLIfUserExist = """SELECT NomUtilisateur FROM utilisateur WHERE Mail = %s"""

requestSQLInsertUser = """INSERT INTO utilisateur (Mail, MotDePasse, NomUtilisateur, DateCreation) 
                       VALUES (%s, %s, %s, %s)"""

requestSQLLoginUser = """SELECT UtilisateurID, MotDePasse, NomUtilisateur FROM utilisateur WHERE Mail = %s"""

requestSQLInfoUser = """SELECT NomUtilisateur FROM utilisateur WHERE UtilisateurID = %s"""

requestSQLPostUser = """SELECT post.PostID, post.NomPost, post.ContenuPost, post.DatePost FROM post INNER JOIN utilisateur as user
                     ON user.UtilisateurID = post.UtilisateurID WHERE user.UtilisateurID = %s
                     ORDER BY DatePost DESC LIMIT 0, 10"""

requestSQLAddPost = """INSERT INTO post (UtilisateurID, NomPost, ContenuPost, DatePost) VALUES (%s, %s, %s, %s)"""

requestSQLDeletePost = """DELETE FROM post WHERE UtilisateurID = %s AND PostID = %s"""

requestSQLInsertFollower = """INSERT INTO Followers (Follower_id, Followed_id) 
                       VALUES (%s, %s)"""

requestSQLDeleteFollower = """Delete FROM Followers WHERE Follower_id = %s 
                        AND Followed_id = %s"""

requestSQLIfFollowerExist = """SELECT Followed_id FROM Followers WHERE Follower = %s"""


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


def get_info_user_by_id(id_user):
    if id_user > 0:
        try:
            with connectionDB.cursor() as cursor:
                cursor.execute(requestSQLInfoUser, id_user)
                if cursor.rowcount != 0:
                    result = cursor.fetchone()
                    cursor.close()
                    return result
                else:
                    return None
        except pymysql.Error as e:
            cursor.close()
            return None


def get_post_user_by_id(id_user):
    if id_user > 0:
        try:
            with connectionDB.cursor() as cursor_post_user:
                cursor_post_user.execute(requestSQLPostUser, id_user)
                if cursor_post_user.rowcount != 0:
                    result_post = cursor_post_user.fetchall()
                    cursor_post_user.close()
                    return result_post
                else:
                    return None
        except pymysql.Error as e:
            cursor_post_user.close()
            return None


def get_account_if_exist(email):
    try:
        with connectionDB.cursor() as cursor:
            cursor.execute(requestSQLLoginUser, email)
            if cursor.rowcount != 0:
                result_user = cursor.fetchone()
                cursor.close()
                return result_user
            else:
                cursor.close()
                return None
    except pymysql.Error as e:
        cursor.close()
        return None


def register_account(email, password_hash, username):
    if get_account_if_exist(email) is None:
        try:
            with connectionDB.cursor() as cursor:
                cursor.execute(requestSQLInsertUser, (email, password_hash, username, date.today()))

                connectionDB.commit()
                cursor.close()
                return True

        except pymysql.Error as e:
            cursor.close()
            return False
    else:
        return False


def add_post(id_user, name_post, content_post):
    if id_user > 0:
        try:
            with connectionDB.cursor() as cursor:
                cursor.execute(requestSQLAddPost, (id_user, name_post, content_post, date.today()))

                connectionDB.commit()  # On commit la transaction
                cursor.close()
                return True

        except pymysql.Error as e:
            print(e)
            cursor.close()
            return False
    else:
        return False


def delete_post(id_user, id_post):
    if id_user > 0 and id_post > 0:
        try:
            with connectionDB.cursor() as cursor:
                cursor.execute(requestSQLDeletePost, (id_user, id_post))

                connectionDB.commit()
                cursor.close()
                return True
        except pymysql.Error as e:
            print(e)
            cursor.close()
            return False
    else:
        return False
