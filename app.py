from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a smart AI assistant. Answer any question."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "Server AI error"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)