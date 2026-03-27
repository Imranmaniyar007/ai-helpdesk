from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager()
login_manager.init_app(app)

HELPLINE = "992260XXXX"


# -------- DATABASE --------

def get_db():
    return sqlite3.connect("users.db")


class User(UserMixin):
    def __init__(self,id):
        self.id=id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# -------- LOGIN --------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        db=get_db()
        cur=db.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user=cur.fetchone()

        if user:
            login_user(User(username))
            return redirect("/")
    
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# -------- EXPERT BOT --------

def expert_reply(msg):

    m=msg.lower()

    if "wifi" in m:
        return "Restart router. Did this solve your issue?"

    elif "slow" in m:
        return "Disable startup apps. Also check disk space."

    elif "heat" in m:
        return "Clean vents and use cooling pad."

    else:
        return f"I cannot resolve. Contact HelpDesk {HELPLINE}"


# -------- CHAT --------

@app.route("/")
@login_required
def home():
    return render_template("index.html",user=current_user.id)


@app.route("/chat", methods=["POST"])
@login_required
def chat():

    message=request.json["message"]

    reply=expert_reply(message)

    db=get_db()
    cur=db.cursor()

    cur.execute("INSERT INTO chats VALUES(?,?,?)",(current_user.id,message,reply))
    db.commit()

    return jsonify({"reply":reply})