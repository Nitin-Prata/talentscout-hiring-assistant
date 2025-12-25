"""
constants.py

Centralized constants used across the application.
Keeping these here avoids magic strings and hardcoding.
"""

# Conversation stages Finite State Machine
STAGE_GREETING = "GREETING"
STAGE_INFO_COLLECTION = "INFO_COLLECTION"
STAGE_TECH_STACK = "TECH_STACK"
STAGE_TECH_QUESTIONS = "TECH_QUESTIONS"
STAGE_CLOSING = "CLOSING"

ALL_STAGES = [
    STAGE_GREETING,
    STAGE_INFO_COLLECTION,
    STAGE_TECH_STACK,
    STAGE_TECH_QUESTIONS,
    STAGE_CLOSING,
]

# Keywords that immediately end the conversation
EXIT_KEYWORDS = {
    "exit",
    "quit",
    "bye",
    "goodbye",
    "stop",
    "end",
}

# Candidate information fields slot-filling order matters
REQUIRED_FIELDS = [
    "full_name",
    "email",
    "phone",
    "years_experience",
    "desired_position",
    "current_location",
    "tech_stack",
]

# Human-readable labels for UI / prompts
FIELD_LABELS = {
    "full_name": "Full Name",
    "email": "Email Address",
    "phone": "Phone Number",
    "years_experience": "Years of Experience",
    "desired_position": "Desired Position",
    "current_location": "Current Location",
    "tech_stack": "Tech Stack (languages, frameworks, tools)",
}
