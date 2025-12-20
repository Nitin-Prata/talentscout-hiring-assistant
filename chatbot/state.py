"""
state.py

Defines the conversation state and candidate data models.
This file acts as the single source of truth for the chatbot session.
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from utils.constants import (
    STAGE_GREETING,
    REQUIRED_FIELDS,
)


class CandidateProfile(BaseModel):
    """
    Structured candidate data collected during the conversation.
    Uses Pydantic for validation and type safety.
    """

    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    years_experience: Optional[int] = Field(default=None, ge=0, le=60)
    desired_position: Optional[str] = None
    current_location: Optional[str] = None
    tech_stack: Optional[List[str]] = None

    def is_complete(self) -> bool:
        """
        Check whether all required fields are filled.
        """
        for field in REQUIRED_FIELDS:
            if getattr(self, field) is None:
                return False
        return True

    def next_missing_field(self) -> Optional[str]:
        """
        Returns the next missing field in order.
        """
        for field in REQUIRED_FIELDS:
            if getattr(self, field) is None:
                return field
        return None


class ConversationState(BaseModel):
    """
    Holds the state of the ongoing conversation.
    """

    stage: str = STAGE_GREETING
    candidate: CandidateProfile = CandidateProfile()
    exit_flag: bool = False

    def reset(self) -> None:
        """
        Reset the conversation state.
        """
        self.stage = STAGE_GREETING
        self.candidate = CandidateProfile()
        self.exit_flag = False
