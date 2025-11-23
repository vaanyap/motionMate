# Install the following dependencies to run the code: pip install google-genai

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompt_builder import build_prompt
from preferences import load_preferences
from exercises import PRESET_EXERCISES

load_dotenv()

def generate():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.5-flash"

    user_prefs = load_preferences()
    preset_exercises = PRESET_EXERCISES

    prompt_text = build_prompt(user_prefs, preset_exercises)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_text),
            ],
        ),
    ]
    
    generate_content_config = {
        # "thinkingConfig": {"thinkingLevel": "LOW"},
    }

    full_response = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        chunk_text = getattr(chunk, "text", getattr(chunk, "delta", ""))
        print(chunk_text, end="")
        full_response += chunk_text
        
    # --- Convert the response string into a structured dict ---
    try:
        # Clean the response - remove markdown code blocks if present
        cleaned_response = full_response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]  # Remove ```json
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # Remove ```
        cleaned_response = cleaned_response.strip()
        
        # Parse the JSON
        response_data = json.loads(cleaned_response)
        
        # Extract the specific fields your frontend expects
        data = {
            "exercise_name": response_data.get("exercise_name", "Unknown Exercise"),
            "tip": response_data.get("tip", "No tip available"),
            "exercise_id": response_data.get("exercise_id", ""),
            "reason": response_data.get("reason", ""),
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {full_response}")
        # Fallback: wrap raw text in a dict
        data = {
            "exercise_name": "Custom Exercise",
            "tip": full_response,
            "exercise_id": "",
            "reason": "AI response could not be parsed",
            "backup_exercise": {
                "exercise_name": "Walking",
                "reason": "Safe fallback option"
            }
        }

    return data

if __name__ == "__main__":
    result = generate()
    print("\n\nFinal structured data:")
    print(json.dumps(result, indent=2))