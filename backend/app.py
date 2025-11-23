from flask import Flask, request, jsonify
from prompt_builder import build_prompt
from exercises import PRESET_EXERCISES
from gemini_api import generate

app = Flask(__name__)

@app.route("/recommend_exercise", methods=["POST"])
def recommend_exercise():
    user_profile = request.json  # receives JSON from frontend
    prompt = build_prompt(user_profile, PRESET_EXERCISES)
    response = generate(prompt)
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)  # run backend on localhost:5000