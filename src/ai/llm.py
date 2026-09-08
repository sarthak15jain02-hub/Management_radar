"""Small Gemini wrapper used by enrichment and the analyst chat."""
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def generate(
    instructions: str,
    input_text: str,
    max_output_tokens: int = 700,
    response_schema: dict | None = None,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to .env before using the AI features."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""SYSTEM INSTRUCTIONS:
{instructions}

USER REQUEST:
{input_text}
"""

    interaction = client.interactions.create(
        model=MODEL,
        input=prompt,
    )

    return interaction.output_text.strip()