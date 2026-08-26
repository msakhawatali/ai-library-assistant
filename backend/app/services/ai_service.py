import json
from openai import OpenAI
from app.core.config import settings
from app.schemas.chat import ChatMessage


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




def generate_ai_response(message: str, book_context: list[dict] | None = None, history: list[ChatMessage] | None = None,) -> str:
    client = get_openai_client()
    if book_context:
        context_text = "\n".join(
            f"- {b['title']} by {b['author']} ({b['category']}, {b['year']}) "
            f"{'Available' if b['available'] else 'Not available'}"
            for b in book_context
        )
        system_prompt = (
            "You are a helpful library assistant. Below is the ONLY book "
            "information you are allowed to use when answering.\n\n"
            f"Available books:\n{context_text}\n\n"
            "Rules you must follow strictly:\n"
            "1. Only use the book information provided above. Never invent "
            "or assume books, authors, categories, years, or availability "
            "that are not listed here.\n"
            "2. If one or more of the listed books match the user's "
            "question, answer using only that information.\n"
            "3. If none of the listed books match the user's question, "
            "clearly tell the user that no relevant books were found — "
            "do not make up a book to satisfy the question.\n"
            "4. If the user's question is unrelated to the library or "
            "books entirely, give a simple, helpful response without "
            "referencing or inventing any library data."
        )
    else:
        system_prompt = (
            "You are a helpful library assistant. No book context is "
            "available for this query. Do not invent or assume any book, "
            "author, category, year, or availability information. If the "
            "question is about the library, tell the user no relevant "
            "books were found. If the question is unrelated to the "
            "library, give a simple, helpful response."
        )

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        messages.extend({"role": m.role, "content": m.content} for m in history)

    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return completion.choices[0].message.content