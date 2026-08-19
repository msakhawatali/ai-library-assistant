from openai import OpenAI
from app.core.config import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


client = get_openai_client()


def generate_ai_response(message: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # ya apna configured model
        messages=[{"role": "user", "content": message}],
    )
    return completion.choices[0].message.content