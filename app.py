from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

HELPLINE = "992260XXXX"

def get_bot_reply(msg):

    m = msg.lower()

    # NETWORK
    if "wifi" in m or "internet" in m or "network" in m:
        return "Restart router, forget network and reconnect. Also check network drivers."

    elif "no signal" in m:
        return "Move closer to router or check LAN cable connection."

    # PERFORMANCE
    elif "slow" in m or "lag" in m or "hang" in m:
        return "Disable startup apps, uninstall unused software and restart system."

    elif "freeze" in m:
        return "Press Ctrl + Shift + Esc and end heavy tasks."

    # HEATING
    elif "heat" in m or "heating" in m or "hot" in m:
        return "Clean laptop vents, use cooling pad and avoid soft surfaces."

    # BATTERY
    elif "battery" in m or "drain" in m:
        return "Reduce brightness, turn off Bluetooth/Wifi when not needed."

    elif "not charging" in m:
        return "Check charger cable and power socket."

    # INPUT DEVICES
    elif "mouse" in m or "touchpad" in m:
        return "Reconnect device or update touchpad driver."

    elif "keyboard" in m:
        return "Clean keyboard and check language settings."

    # DISPLAY
    elif "screen" in m or "display" in m:
        return "Restart PC and update graphics driver."

    elif "black screen" in m:
        return "Force restart and reconnect display cable."

    # SOUND
    elif "sound" in m or "audio" in m or "speaker" in m:
        return "Check volume mixer and reinstall audio driver."

    # STORAGE
    elif "storage" in m or "disk full" in m:
        return "Delete temporary files and run disk cleanup."

    # SOFTWARE
    elif "install" in m or "software" in m:
        return "Run installer as administrator."

    elif "virus" in m or "malware" in m:
        return "Run full antivirus scan immediately."

    # FALLBACK
    else:
        return f"I am unable to resolve this issue. Please contact HelpDesk at {HELPLINE}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    reply = get_bot_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()