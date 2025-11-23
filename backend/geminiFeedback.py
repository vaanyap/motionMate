
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json



load_dotenv()


def generate(exerciseData, user_profile):
    api_key = os.environ.get("GEMINI_API_KEY_FEEDBACK")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY_FEEDBACK environment variable is not set")

    client = genai.Client(api_key=api_key)
    frame_info = "\n".join([f"- {key.replace('_', ' ').capitalize()}: {value}" 
                            for key, value in exerciseData.items()])

    prompt = f"""
        User Profile:
        {json.dumps(user_profile, indent=2)}

        Current Exercise Frame:
        {frame_info}
        Instructions for the model:
        - Keep feedback **stable**. Only adjust advice if posture meaningfully changes.
        - If the user does not continue with the excersice, gently nudge them to resume.
        - User details are in user_profile.
        - Feedback must be **short, calm, and encouraging**.
        - Do NOT introduce new concepts or shuffle advice unless posture actually changed.
        - If form is good, mention to keep it up and be encouraging.
        - If form needs correction, give **only 1–2 simple corrections**.
        - Avoid overreacting to slight noise in angles.
        - With specific disabilities, add more liniency in feedback.
        - Feel free to suggest easier verion of the exercise if user is struggling, given the user profile history.

        Now give concise, clear, and stable feedback for this frame.
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

