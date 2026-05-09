"""Application configuration helpers."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# STEP 8: Load local environment variables before reading OPENAI_API_KEY.
load_dotenv(BASE_DIR / ".env")


def get_openai_api_key(required: bool = True) -> str | None:
    """Return the OpenAI API key loaded from the environment."""
    api_key = os.getenv("OPENAI_API_KEY")

    if required and not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to the project .env file."
        )

    return api_key


def is_openai_configured() -> bool:
    """Check whether the OpenAI API key is available."""
    return bool(get_openai_api_key(required=False))
