"""Prompt templates for the meeting copilot."""


def build_meeting_summary_prompt(content: str) -> str:
    """Build the prompt used to summarize meeting notes."""
    return f"""
You are an AI software workflow assistant.
Please read the meeting notes and generate the following:

1. Meeting summary
2. TODO list
3. API draft
4. Markdown knowledge note

Meeting notes:
{content}
"""
