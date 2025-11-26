# ai_engine.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Hämtar OPENAI_API_KEY från .env
client = OpenAI()

SYSTEM_PROMPT = """
You are The Archivist, an ancient philosopher and historian who has lived
for centuries in a timeless library.

Style:
- Speak like a calm, reflective philosopher.
- Occasionally use phrases like "in those days", "in that age", "as time would have it".
- But always keep bullet points short, clear and factual.

Output:
- Only bullet points starting with '- '.
- 3 to 7 bullets.
- English only.
"""


def get_ai_facts(query: str) -> list[str]:
    """
    Takes a free-text query like '1989', 'The fall of the Berlin Wall',
    'Napoleon', 'The Matrix', etc. Returns a list of bullet-point strings.
    """
    prompt = f"User query: {query}\n\nRemember: return only bullet points."

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    # Hämta texten ur första output
    text = response.output[0].content[0].text

    # Dela upp i rader, filtrera bort tomma
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Om modellen inte var snäll och började med '-' på varje rad, fixa:
    bullets = []
    for line in lines:
        if not line.startswith("-"):
            line = "- " + line.lstrip("• ").strip()
        bullets.append(line)

    return bullets
