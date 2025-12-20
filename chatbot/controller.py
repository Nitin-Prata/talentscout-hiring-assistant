"""
controller.py

Implements the finite-state machine (FSM) that controls
the conversation flow for the hiring assistant.
"""

from utils.constants import (
    STAGE_GREETING,
    STAGE_INFO_COLLECTION,
    STAGE_TECH_STACK,
    STAGE_TECH_QUESTIONS,
    STAGE_CLOSING,
    EXIT_KEYWORDS,
)
from chatbot.state import ConversationState


def check_exit(user_input: str, state: ConversationState) -> bool:
    """
    Check if the user wants to exit the conversation.
    """
    if user_input.strip().lower() in EXIT_KEYWORDS:
        state.exit_flag = True
        state.stage = STAGE_CLOSING
        return True
    return False


def advance_stage(state: ConversationState) -> None:
    """
    Advance the conversation stage based on the current state
    and collected candidate information.
    """

    if state.stage == STAGE_GREETING:
        state.stage = STAGE_INFO_COLLECTION
        return

    if state.stage == STAGE_INFO_COLLECTION:
        # Move forward only when all required fields are collected
        if state.candidate.is_complete():
            state.stage = STAGE_TECH_QUESTIONS
        return

    if state.stage == STAGE_TECH_QUESTIONS:
        state.stage = STAGE_CLOSING
        return


def get_current_stage(state: ConversationState) -> str:
    """
    Returns the current stage of the conversation.
    """
    return state.stage
