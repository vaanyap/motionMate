# Fixed set of exercises that Gemini must choose from
# Can add more exercises here at anytime

PRESET_EXERCISES = [
    {
        "id": "E1",
        "name": "Seated Hamstring Stretch",
        "category": "flexibility",
        "difficulty": "easy",
        "equipment": [],
        "instructions": "Sit on the floor with legs extended and lean forward."
    },
    {
        "id": "E2",
        "name": "Wall Push-Up",
        "category": "upper body strength",
        "difficulty": "easy",
        "equipment": ["wall"],
        "instructions": "Stand arms-length from a wall and push your body away."
    },
    {
        "id": "E3",
        "name": "Chair Squat",
        "category": "lower body",
        "difficulty": "medium",
        "equipment": ["chair"],
        "instructions": "Stand and sit back down without using your hands."
    }
]

def get_exercise_by_id(ex_id: str):
    """Return full exercise object by ID."""
    for ex in PRESET_EXERCISES:
        if ex["id"] == ex_id:
            return ex
    return None