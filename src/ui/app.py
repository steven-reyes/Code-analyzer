# src/ui/app.py

from flask import Flask, render_template, request, jsonify
from src.chatgpt_integration import ChatGPTClient
from src.utils.project_analyzer import analyze_project

app = Flask(__name__)
chatgpt_client = ChatGPTClient()

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    project_path = request.form.get("project_path", "")
    analysis_results = analyze_project(project_path)
    return jsonify(analysis_results)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    response = chatgpt_client.send_message(
        user_message, context="You are ChatGPT-01. Provide code analysis help."
    )
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
