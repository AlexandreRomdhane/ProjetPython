from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)

app.secret_key = "OuiBiensurquecestsecretsinonsasersarien"

visiteur = []


@app.route("/")
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        visiteur.append(session['username'])
        return redirect(url_for('index'))
    else:
        return '''
                <form method="post">
                    <p><input type=text name=username>
                    <p><input type=submit value=Login>
                </form>
            '''


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/visiteur")
def displayVisitor():
    result = ""
    for visitor in visiteur:
        result += visitor + ",\n"
    return result


@app.route("/user/<username>")
def show_user_profile(username):
    return "User %s" % escape(username)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return "Post %s" % post_id


@app.route("/projects/")
def projects():
    return "The project page"


@app.route("/about")
def about():
    return "The about page"


def doLogin():
    return "You'r connected !"


def showLoginForm():
    return "Login please !"
