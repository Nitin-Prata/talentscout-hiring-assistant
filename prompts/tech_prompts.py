"""
tech_prompts.py

Prompts used to generate technical interview questions
based on the candidate's declared tech stack.
"""

TECH_QUESTION_PROMPT = """
The candidate has declared the following tech stack:
{tech_stack}

Their desired role is:
{desired_position}

Their years of experience:
{years_experience}

Task:
Generate 3 to 5 technical interview questions for EACH technology listed.

Guidelines:
- Questions should assess practical understanding.
- Start from basic to intermediate difficulty.
- Avoid yes/no questions.
- Do NOT include explanations or answers.
- Do NOT include technologies not listed.

Format the output as:
Technology Name:
1. Question
2. Question
3. Question
"""
