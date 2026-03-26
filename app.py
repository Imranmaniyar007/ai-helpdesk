from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Gemini Client (FREE)
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=user_message
        )

        reply = response.text

    except Exception as e:
        reply = "AI Error: " + str(e)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run()