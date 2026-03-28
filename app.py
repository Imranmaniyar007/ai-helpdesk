from flask import Flask, render_template, request, jsonify, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

HELPLINE = "992260XXXX"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("users.db")

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# ---------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()

        if user:
            login_user(User(username))
            return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# ---------- EXPERT BOT ----------
def expert_reply(msg, user):

    m = msg.lower()

    # remember last issue
    db = get_db()
    cur = db.cursor()

    # responses
    if "wifi" in m:
        reply = "🔧 Restart router, check cables, and reconnect WiFi."
    elif "slow" in m:
        reply = "⚡ Close background apps and disable startup programs."
    elif "heat" in m or "heating" in m:
        reply = "🌡 Clean laptop vents and use cooling pad."
    elif "battery" in m:
        reply = "🔋 Reduce brightness and close unused apps."
    elif "internet" in m:
        reply = "🌐 Check ISP connection or restart modem."
    elif "hang" in m:
        reply = "💻 System may be overloaded. Restart recommended."
    else:
        reply = f"❌ I cannot solve this.\n📞 Contact HelpDesk: {HELPLINE}"

    # save chat
    cur.execute("INSERT INTO chats(user, question, answer) VALUES(?,?,?)",
                (user, msg, reply))
    db.commit()

    return reply

# ---------- ROUTES ----------
@app.route("/")
@login_required
def home():
    return render_template("index.html", user=current_user.id)

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    message = request.json["message"]

    reply = expert_reply(message, current_user.id)

    return jsonify({"reply": reply})