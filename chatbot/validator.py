"""
validator.py

Validates and extracts candidate information from user input.
This module is strictly rule-based (no LLM usage).
"""

import re
from typing import Dict

from pydantic import ValidationError

from chatbot.state import CandidateProfile


# Simple regex patterns
EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_REGEX = re.compile(r"\+?\d[\d\s\-]{8,15}")
NUMBER_REGEX = re.compile(r"\d+")


def validate_and_extract(
    user_input: str,
    candidate: CandidateProfile,
) -> Dict[str, object]:
    """
    Attempt to extract and validate candidate fields from user input.

    Returns a dictionary of {field_name: value} for valid fields only.
    """
    extracted: Dict[str, object] = {}
    text = user_input.strip()

    # Full name (only if not already set)
    if candidate.full_name is None and len(text.split()) >= 2:
        extracted["full_name"] = text

    # Email
    if candidate.email is None:
        match = EMAIL_REGEX.search(text)
        if match:
            try:
                extracted["email"] = match.group()
            except ValidationError:
                pass

    # Phone number
    if candidate.phone is None:
        match = PHONE_REGEX.search(text)
        if match:
            extracted["phone"] = match.group()

    # Years of experience
    if candidate.years_experience is None:
        nums = NUMBER_REGEX.findall(text)
        if nums:
            years = int(nums[0])
            if 0 <= years <= 60:
                extracted["years_experience"] = years

    # Desired position
    if candidate.desired_position is None:
        if any(word.lower() in text.lower() for word in ["developer", "engineer", "analyst", "scientist"]):
            extracted["desired_position"] = text

    # Current location
    if candidate.current_location is None:
        if "," in text or len(text.split()) <= 4:
            extracted["current_location"] = text

    # Tech stack
    if candidate.tech_stack is None:
        if "," in text:
            techs = [t.strip() for t in text.split(",") if t.strip()]
            if techs:
                extracted["tech_stack"] = techs

    return extracted
