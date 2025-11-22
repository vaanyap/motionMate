# Install the following dependencies to run the code: pip install google-genai

import os
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
    # Use a plain dict for config to avoid invalid Python syntax and keep the example simple
    generate_content_config = {
        # "thinkingConfig": {"thinkingLevel": "LOW"},
    }

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        # print defensively in case the stream chunk attribute differs
        print(getattr(chunk, "text", getattr(chunk, "delta", "")), end="")

if __name__ == "__main__":
    generate()