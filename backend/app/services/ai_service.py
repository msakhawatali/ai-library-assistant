import json
from openai import OpenAI
from app.core.config import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


def extract_search_filters(message: str) -> dict:
    client = get_openai_client()

    system_prompt = (
        "Extract book search filters from the user's message. "
        "Return ONLY a JSON object with these optional keys: "
        "title, author, category, year (integer), available (boolean). "
        "Only include keys that are clearly mentioned in the message. "
        "If no filters can be identified, return an empty JSON object {}."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        response_format={"type": "json_object"},
    )

    try:
        filters = json.loads(completion.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        filters = {}

    return filters




def generate_ai_response(message: str, book_context: list[dict] | None = None) -> str:
    client = get_openai_client()
    if book_context:
        context_text = "\n".join(
            f"- {b['title']} by {b['author']} ({b['category']}, {b['year']}) "
            f"{'Available' if b['available'] else 'Not available'}"
            for b in book_context
        )
        system_prompt = (
            "You are a helpful library assistant. Use the following book information "
            "to answer the user's question. If no relevant books are listed, say so.\n\n"
            f"Available books:\n{context_text}"
        )
    else:
        system_prompt = (
            "You are a helpful library assistant. No matching books were found "
            "in the library for this query."
        )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    )
    return completion.choices[0].message.content