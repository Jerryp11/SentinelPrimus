# src/ai_agent.py

from flask import Flask, request, jsonify
import openai
import re
import os

app = Flask(__name__)

# Load OpenAI API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple guardrail to detect basic prompt injection
def is_malicious_input(user_input):
    suspicious_patterns = [
        r"ignore previous", r"you are now", r"disregard instructions",
        r"pretend to be", r"system prompt", r"admin override"
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    return False

@app.route("/ask", methods=["POST"])
def ask_agent():
    data = request.get_json()
    user_input = data.get("message", "")

    if is_malicious_input(user_input):
        return jsonify({
            "status": "blocked",
            "message": "🚫 Request blocked due to policy violation."
        })

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message['content']
        return jsonify({"status": "success", "response": reply})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)