"""
info_prompts.py

Prompts used for collecting candidate information
in a structured, step-by-step manner.
"""

INFO_COLLECTION_PROMPT = """
You are collecting candidate information for an initial screening.

The following information has already been collected:
{collected_fields}

Ask the candidate politely for the next missing field:
{next_field_label}

Guidelines:
- Ask only ONE clear question.
- Do not repeat already collected information.
- Do not ask multiple fields at once.
- Keep the tone professional and friendly.
"""
