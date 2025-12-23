"""
handlers.py

Stage-specific handlers that process user input,
update conversation state, and generate responses.
"""

from typing import Dict

from chatbot.state import ConversationState
from chatbot.controller import check_exit, advance_stage
from chatbot.validator import validate_and_extract
from llm.groq_client import generate_response
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.tech_prompts import TECH_QUESTION_PROMPT
from utils.constants import (
    STAGE_GREETING,
    STAGE_INFO_COLLECTION,
    STAGE_TECH_QUESTIONS,
    STAGE_CLOSING,
    FIELD_LABELS,
)


def handle_user_input(user_input: str, state: ConversationState) -> str:
    """
    Main entry point for processing user input.
    Returns the assistant's response text.
    """

    # Global exit handling (works at any stage)
    if check_exit(user_input, state):
        return _handle_closing(state)

    # Stage-based routing
    if state.stage == STAGE_GREETING:
        return _handle_greeting(state)

    if state.stage == STAGE_INFO_COLLECTION:
        return _handle_info_collection(user_input, state)

    if state.stage == STAGE_TECH_QUESTIONS:
        return _handle_tech_questions(state)

    if state.stage == STAGE_CLOSING:
        return _handle_closing(state)

    return "Sorry, something went wrong. Please try again."


# -------------------------
# Stage Handlers
# -------------------------

def _handle_greeting(state: ConversationState) -> str:
    """
    Handle the greeting stage.
    """
    advance_stage(state)
    return (
        "Hello! 👋 I’m TalentScout, your AI hiring assistant.\n\n"
        "I’ll start by collecting some basic information for initial screening.\n\n"
        "Let’s begin — what’s your **full name**?"
    )


def _handle_info_collection(user_input: str, state: ConversationState) -> str:
    """
    Handle structured candidate information collection
    using deterministic, clear prompts (no LLM).
    """

    # Extract and validate data from user input
    extracted: Dict[str, object] = validate_and_extract(
        user_input=user_input,
        candidate=state.candidate,
    )

    # Update candidate profile
    for field, value in extracted.items():
        setattr(state.candidate, field, value)

    # If all required fields are collected, move to tech questions
    if state.candidate.is_complete():
        advance_stage(state)
        return (
            "Thanks for sharing your details! ✅\n\n"
            "Now I’ll ask you a few technical questions based on your tech stack."
        )

    # Ask explicitly for the next missing field (ChatGPT-style UX)
    next_field = state.candidate.next_missing_field()
    next_field_label = FIELD_LABELS.get(next_field, next_field)

    return f"Got it 👍 Could you please provide your **{next_field_label}**?"


def _handle_tech_questions(state: ConversationState) -> str:
    """
    Generate technical interview questions based on the tech stack.
    This is the ONLY stage where the LLM is used.
    """

    prompt = TECH_QUESTION_PROMPT.format(
        tech_stack=", ".join(state.candidate.tech_stack or []),
        desired_position=state.candidate.desired_position,
        years_experience=state.candidate.years_experience,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    advance_stage(state)
    return generate_response(messages)


def _handle_closing(state: ConversationState) -> str:
    """
    Gracefully end the conversation.
    """
    state.exit_flag = True
    return (
        "Thank you for your time! 🙏\n\n"
        "Your responses have been recorded. Our recruitment team will "
        "reach out to you regarding the next steps.\n\n"
        "Have a great day!"
    )
