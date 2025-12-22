"""
groq_client.py

Groq LLM client wrapper.
This module abstracts all interaction with the Groq API
and handles provider-side failures gracefully.
"""

import os
from typing import List, Dict

from groq import Groq, GroqError
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API key (required)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY not found in environment variables. "
        "Please set it in your .env file."
    )

# Model configuration
# Use a STABLE Groq model and allow override via .env
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# Initialize Groq client once (singleton-style)
_client = Groq(api_key=GROQ_API_KEY)


def generate_response(
    messages: List[Dict[str, str]],
    temperature: float = 0.3,
    max_tokens: int = 1024,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate a response from the Groq-hosted LLM.

    This function is designed to NEVER crash the application.
    If the LLM fails (e.g., model deprecation, network issue),
    a safe fallback response is returned.
    """
    try:
        completion = _client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content.strip()

    except GroqError:
        # Graceful fallback to keep conversation alive
        return (
            "Thanks for the information. 👍\n\n"
            "Let’s continue. Could you please provide the next required detail?"
        )

    except Exception:
        # Catch-all safety net (never crash the app)
        return (
            "Sorry, I ran into a temporary issue. 🙏\n\n"
            "Please try again or continue with the next detail."
        )
