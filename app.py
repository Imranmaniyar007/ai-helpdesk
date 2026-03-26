from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data["question"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a helpful IT helpdesk expert."},
            {"role":"user","content":question}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({"answer":answer})

if __name__ == "__main__":
    app.run(debug=True)