from flask import Flask, request, jsonify
from prompt_builder import build_prompt
from exercises import PRESET_EXERCISES
from gemini_api import generate
from preferences import save_preferences

app = Flask(__name__)

@app.route("/recommend_exercise", methods=["POST"])
def recommend_exercise():
    try:
        user_profile = request.get_json()  # receives JSON from frontend
        print("Received user profile:", user_profile)
        save_preferences(user_profile)
        data = generate()
        
        # Use jsonify to properly return JSON response
        return jsonify(data), 200
        
    except Exception as e:
        print(f"Error in recommend_exercise: {str(e)}")
        return jsonify({
            "exercise_name": "Error",
            "tip": f"Failed to generate recommendation: {str(e)}"
        }), 500

@app.route("/get_info", methods=["GET"])
def get_info():
    return jsonify({"info": "MotionMimic+ backend is running"}), 200

if __name__ == "__main__":
    app.run(port=5000)  # run backend on localhost:5000