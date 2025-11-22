import json
# Get user's exercise/accessibility preferences to use in the prompt

PREF_FILE = "user_preferences.json"

def save_preferences(prefs: dict):
    """Save user preferences to a JSON file."""
    with open(PREF_FILE, "w") as f:
        json.dump(prefs, f)

def load_preferences():
    """Load preferences if they exist."""
    try:
        with open(PREF_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}