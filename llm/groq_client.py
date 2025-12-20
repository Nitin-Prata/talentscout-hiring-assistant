"""
groq_client.py

Groq LLM client wrapper.
This module abstracts all interaction with the Groq API.
"""

import os
from typing import List, Dict

from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Environment variable name (fixed by design)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY not found in environment variables. "
        "Please set it in your .env file."
    )

# Model configuration
DEFAULT_MODEL = "llama3-70b-8192"

# Initialize Groq client once
_client = Groq(api_key=GROQ_API_KEY)


def generate_response(
    messages: List[Dict[str, str]],
    temperature: float = 0.3,
    max_tokens: int = 1024,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate a response from the Groq-hosted LLM.

    Args:
        messages: List of chat messages in OpenAI-compatible format.
        temperature: Controls randomness (lower = more deterministic).
        max_tokens: Maximum tokens in the response.
        model: Groq model name.

    Returns:
        Generated text response from the model.
    """

    completion = _client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return completion.choices[0].message.content.strip()
