
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()


def generate(exerciseData):
    api_key = os.environ.get("GEMINI_API_KEY_FEEDBACK")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY_FEEDBACK environment variable is not set")

    client = genai.Client(api_key=api_key)
    prompt = f"""
The user is doing the exercise: {exerciseData['exercise']}.
Left angle: {exerciseData['left_angle']:.1f}°, Right angle: {exerciseData['right_angle']:.1f}°.
Left wrist above shoulder: {exerciseData['left_wrist_above_shoulder']}, Right wrist above shoulder: {exerciseData['right_wrist_above_shoulder']}.
Correct form: {exerciseData['correct_form']}.
Give concise, clear feedback to help the user correct their form if needed.
"""

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    output_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
    ):
        output_text += getattr(chunk, "text", getattr(chunk, "delta", ""))

    return output_text


# from google import genai
# import os
# from dotenv import load_dotenv
# load_dotenv()

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_FEEDBACK"))

# def getFeedback(exerciseData):
#     # prompt = f"""
#     # The user is doing the exercise: {exerciseData['exercise']}.
#     # Left angle: {exerciseData['left_angle']:.1f}°, Right angle: {exerciseData['right_angle']:.1f}°.
#     # Left wrist above shoulder: {exerciseData['left_wrist_above_shoulder']}, Right wrist above shoulder: {exerciseData['right_wrist_above_shoulder']}.
#     # Correct form: {exerciseData['correct_form']}.
#     # Give concise, clear feedback to help the user correct their form if needed.
#     # """
#     prompt = f"""What's today's date?"""

#     try:
#         response = client.generate_text(
#             model="gemini-2.5-flash",
#             prompt=prompt,
#             temperature=0.7,
#             max_output_tokens=150
#         )
#         print( response.text)
#     except Exception as e:
#         print("Error generating feedback:", e)
#         return ""

