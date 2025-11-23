import json

def build_prompt(user_prefs: dict, preset_exercises: list):
    """
    Builds a strict prompt that ensures Gemini:
    - selects only ONE exercise from the provided list
    - returns valid JSON only
    - avoids adding extra text or hallucinated exercises
    """

    # Safety checks (optional)
    assert isinstance(user_prefs, dict), "user_prefs must be a dictionary"
    assert isinstance(preset_exercises, list), "preset_exercises must be a list"
    

    # Convert structures to pretty JSON
    user_prefs_json = json.dumps(user_prefs, indent=2)
    preset_exercises_json = json.dumps(preset_exercises, indent=2)

    # Construct prompt
    prompt = (
        "You are an assistant helping to select the most suitable next exercise "
        "for a fitness app based on the user's accessibility/exercise preferences.From the user preferences, please prioritize accomodating for disabilities and accessibility needs.\n\n"
        
        "For the selected exercise, provide:\n"
        "Tip: a short personalized tip for the user, considering:\n"
        "- accessibility needs\n"
        "- health conditions\n"
        "- fitness level\n"
        "- preferences\n"
        "The tip should be actionable and safe.\n"

        "USER PREFERENCES:\n"
        f"{user_prefs_json}\n\n"

        "Allowed Exercises (choose ONLY from these):\n"
        f"{preset_exercises_json}\n\n"

        "RULES:\n"
        "1. You MUST select exactly ONE exercise from the allowed list.\n"
        "2. You MUST return ONLY valid JSON — no backticks, no markdown, no explanations.\n"
        "3. Your JSON output must follow this structure:\n"
        '{ "exercise_id": "<id from allowed list>", "exercise_name": "<name from allowed list>", "reason": "<brief reason>", "tip": "<personalized tip>"}\n\n'
        "4. Do NOT create new exercises or modify existing ones.\n"
        "5. Do NOT include anything outside the JSON object.\n\n"
        "6. Do NOt recommend excersises that are already seen from userpreferences.\n\n"
        "Return ONLY the JSON object."
    )

    return prompt
