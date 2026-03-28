from flask import Flask, render_template, request, jsonify, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"   # 🔥 THIS FIXES REDIRECT

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

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()

        # check if user already exists
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        existing = cur.fetchone()

        if existing:
            return "User already exists!"

        # insert new user
        cur.execute("INSERT INTO users VALUES (?,?)", (username, password))
        db.commit()

        return redirect("/login")

    return render_template("signup.html")

# ---------- EXPERT BOT ----------
def expert_reply(msg, user):

    m = msg.lower()

    if "wifi" in m or "wi-fi" in m:
        return """📡 WIFI ISSUE SOLUTION:

1. Restart router (wait 10 sec)
2. Forget & reconnect WiFi
3. Check airplane mode OFF
4. Restart device
5. Try another device to confirm issue

👉 If still not working → ISP problem possible"""

    elif "slow" in m:
        return """🐢 LAPTOP SLOW FIX:

1. Close background apps (Task Manager)
2. Disable startup programs
3. Delete temp files (Disk Cleanup)
4. Check storage (keep 20% free)
5. Restart system

💡 Tip: Add SSD for huge speed boost"""

    elif "heat" in m or "heating" in m:
        return """🌡 HEATING ISSUE:

1. Clean air vents
2. Use cooling pad
3. Avoid bed/soft surface
4. Close heavy apps
5. Replace thermal paste (advanced)

⚠ Overheating can damage CPU"""

    elif "battery" in m:
        return """🔋 BATTERY DRAIN FIX:

1. Lower brightness
2. Turn off Bluetooth/WiFi when unused
3. Close background apps
4. Enable battery saver
5. Check battery health

💡 Replace battery if old"""

    elif "internet" in m or "network" in m:
        return """🌐 INTERNET ISSUE:

1. Restart modem
2. Check ISP connection
3. Reset network settings
4. Try LAN cable
5. Speed test

👉 Could be ISP downtime"""

    elif "hang" in m or "freeze" in m:
        return """💻 SYSTEM HANG:

1. Press Ctrl+Alt+Del
2. End heavy processes
3. Restart system
4. Scan for virus
5. Upgrade RAM if frequent"""

    elif "virus" in m or "malware" in m:
        return """🛡 VIRUS ALERT:

1. Run full antivirus scan
2. Delete suspicious files
3. Avoid unknown downloads
4. Keep system updated

⚠ Use trusted antivirus only"""

    elif "bluetooth" in m:
        return """📶 BLUETOOTH ISSUE:

1. Turn OFF/ON Bluetooth
2. Remove & reconnect device
3. Update drivers
4. Restart system"""

    elif "keyboard" in m:
        return """⌨ KEYBOARD ISSUE:

1. Check keys stuck
2. Restart system
3. Reinstall drivers
4. Try external keyboard"""

    elif "screen" in m:
        return """🖥 SCREEN ISSUE:

1. Adjust brightness
2. Check display cable
3. Update graphics driver
4. Restart device"""

    # SOUND
    elif "sound" in m or "audio" in m or "speaker" in m:
        return "Check volume mixer and reinstall audio driver."

    # STORAGE
    elif "storage" in m or "disk full" in m:
        return "Delete temporary files and run disk cleanup."

    # SOFTWARE
    elif "install" in m or "software" in m:
        return "Run installer as administrator."


    else:
        return f"""❌ I couldn't fully understand.

👉 Try asking:
• wifi not working  
• laptop slow  
• heating issue  
• battery draining  
• internet problem  

📞 Contact HelpDesk: {HELPLINE}"""

    return f"""❌ I couldn't fully understand.

👉 Try asking:
• wifi not working  
• laptop slow  
• heating issue  
• battery draining  
• internet problem  

📞 Contact HelpDesk: {HELPLINE}"""

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