import json
from openai import OpenAI, OpenAIError
from sqlmodel import Session
from app.core.config import settings
from app.schemas.chat import ChatMessage
from app.services.book_search import search_books

SEARCH_BOOKS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_books",
        "description": "Search the library's book database using optional filters.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Book title to search for"},
                "author": {"type": "string", "description": "Author name to search for"},
                "category": {"type": "string", "description": "Book category/genre"},
                "year": {"type": "integer", "description": "Publication year"},
                "available": {"type": "boolean", "description": "Whether the book is currently available"},
            },
            "required": [],
        },
    },
}


class AIServiceError(Exception):
    """Raised when the AI service fails to generate a response."""
    pass


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

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except (OpenAIError, json.JSONDecodeError, TypeError, Exception):
        return {}




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

    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    if history:
        for m in history:
            messages.append({"role": m.role, "content": m.content})

    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return completion.choices[0].message.content
    except OpenAIError:
        raise AIServiceError("AI service is currently unavailable. Please try again later.")
    except Exception:
        raise AIServiceError("AI service is currently unavailable. Please try again later.")


def _execute_search_books_tool(session: Session, arguments: dict) ->list[dict]:
    books = search_books(
        session,
        title=arguments.get("title"),
        author=arguments.get("author"),
        category=arguments.get("category"),
        year=arguments.get("year"),
        available=arguments.get("available"),
    )
    return [
        {
            "id": b.id, "title": b.title, "author": b.author,
            "category": b.category, "year": b.year, "available": b.available,
        }
        for b in books
    ]

def generate_ai_response_with_tools(
        session: Session,
        message: str,
        history: list[ChatMessage] |  None = None,
) -> str:
    client = get_openai_client()

    system_prompt = (
        "You are a helpful library assistant. When the user asks about books, "
        "use the search_books tool to find relevant books before answering. "
        "Only use information retruned by the tool - never invent books, "
        "authors, years, or available. If the tool return no result, "
        "tell the user no relevant books ware found."
    )

    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    if history:
        for m in history:
            messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=[SEARCH_BOOKS_TOOL],
            tool_choice="auto"
        )
        response_message = completion.choices[0].message

        if response_message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in response_message.tool_calls
                ],
            })

            for tool_call in response_message.tool_calls:
                arguments = json.loads(tool_call.function.arguments)
                result = _execute_search_books_tool(session, arguments)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })

            follow_up = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            return follow_up.choices[0].message.content

        return response_message.content

    except OpenAIError:
        raise AIServiceError("AI service is currently unavailable. Please try again later.")
    except Exception:
        raise AIServiceError("AI service is currently unavailable. Please try again later.")