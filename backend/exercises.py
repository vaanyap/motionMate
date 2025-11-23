# Fixed set of exercises that Gemini must choose from
# Can add more exercises here at anytime

PRESET_EXERCISES = [
    {
        "id": "E1",
        "name": "Arms Up Stretch",
        "category": "flexibility",
        "difficulty": "easy",
        "equipment": [],
        "instructions": "Stand tall, raise both arms overhead, and straighten them above your head."
    },
    {
        "id": "E2",
        "name": "Bodyweight Squat",
        "category": "lower body strength",
        "difficulty": "medium",
        "equipment": [],
        "instructions": "Stand with feet shoulder-width apart and lower into a squat, keeping your back straight."
    },
    {
        "id": "E3",
        "name": "Forward Lunge",
        "category": "lower body strength",
        "difficulty": "medium",
        "equipment": [],
        "instructions": "Step forward with one foot, lower your body until both knees are bent, then push back to standing."
    },
    {
        "id": "E4",
        "name": "Plank",
        "category": "core strength",
        "difficulty": "medium",
        "equipment": [],
        "instructions": "Hold a straight-body position with your forearms and toes on the ground, keeping your core tight."
    },
    {
        "id": "E5",
        "name": "Toe Touch Stretch",
        "category": "flexibility",
        "difficulty": "easy",
        "equipment": [],
        "instructions": "Stand straight and bend forward at the hips to touch your toes while keeping your legs straight."
    },
    {
        "id": "E6",
        "name": "Cobra Stretch",
        "category": "flexibility",
        "difficulty": "easy",
        "equipment": [],
        "instructions": "Lie face down, place your palms under your shoulders on the ground, and lift your chest upward while keeping hips on the ground."
    },
    {
        "id": "E7",
        "name": "Tree Pose",
        "category": "balance",
        "difficulty": "medium",
        "equipment": [],
        "instructions": "Stand on one leg and place the other foot on your inner thigh or calf, bringing your hands together at your chest or overhead."
    }
]

def get_exercise_by_id(ex_id: str):
    """Return full exercise object by ID."""
    for ex in PRESET_EXERCISES:
        if ex["id"] == ex_id:
            return ex
    return None