from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="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")

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