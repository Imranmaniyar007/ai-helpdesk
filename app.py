from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart AI assistant. Answer any question."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = str(e)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()