# AI Library Assistant

A backend service for managing a library's book catalog, with an AI-powered
chat assistant that can answer natural-language questions about the
collection.

Built with **FastAPI**, **SQLModel**, **PostgreSQL**, and the **OpenAI API**.

---

## Features

- Full CRUD API for managing books (title, author, category, year, availability)
- AI chat assistant that understands natural-language questions about the library
- Automatic book search via OpenAI tool calling — no manual query building needed
- Per-conversation chat history so the assistant understands follow-up questions
- Input validation and safe, user-friendly error handling

---

## Tech Stack

| Layer          | Technology              |
|----------------|--------------------------|
| API framework  | FastAPI                 |
| ORM / models   | SQLModel                |
| Database       | PostgreSQL               |
| AI provider    | OpenAI API                |
| Testing        | pytest                   |

---

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── books.py       # Book CRUD endpoints
│   │       └── ai.py          # AI chat endpoints
│   ├── core/
│   │   └── config.py          # Environment/config loading
│   ├── db/
│   │   └── database.py        # DB engine/session setup
│   ├── models/
│   │   └── book.py            # Book SQLModel
│   ├── schemas/
│   │   ├── ai.py              # Chat request/response schemas
│   │   └── chat.py            # Conversation message schemas
│   ├── services/
│   │   ├── book_search.py     # Book search service
│   │   ├── ai_service.py      # OpenAI client + tool-calling chat logic
│   │   └── chat_history.py    # In-memory conversation history
│   └── tests/                 # pytest test suite
├── .env.example
└── pyproject.toml
```

---

## Setup

### 1. Install dependencies

```bash
cd backend
uv sync
```

*(or `pip install -e .` if you're not using `uv`)*

### 2. Configure environment variables

Copy `.env.example` to `.env` at the project root and fill in your values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/library_db
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/library_test_db
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the server

```bash
cd backend
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs
at `http://127.0.0.1:8000/docs`.

### 4. Run tests

```bash
cd backend
uv run pytest
```

---

## Book API

Standard CRUD endpoints for managing the library's book catalog.

| Method | Endpoint            | Description                  |
|--------|----------------------|-------------------------------|
| POST   | `/api/books`         | Create a new book             |
| GET    | `/api/books`         | List all books                |
| GET    | `/api/books/{id}`    | Get a single book by ID       |
| PATCH  | `/api/books/{id}`    | Update an existing book       |
| DELETE | `/api/books/{id}`    | Delete a book                 |

**Book fields:** `id`, `title`, `author`, `category`, `year`, `available`

---

## AI Chat API

The AI Library Assistant exposes a chat endpoint that lets users ask
questions about the library in natural language. When a question is about
books, the AI automatically searches the library database using the
`search_books` tool and answers using real data — it never invents books,
authors, or availability.

### Send a chat message

**`POST /api/ai/chat`**

**Request body**

| Field              | Type   | Required | Description                                                  |
|---------------------|--------|----------|----------------------------------------------------------------|
| `message`           | string | Yes      | The user's message. Must not be empty or whitespace-only.     |
| `conversation_id`   | string | Yes      | An identifier for the conversation. Used to track history.    |

**Response body**

| Field              | Type   | Description                                       |
|---------------------|--------|------------------------------------------------------|
| `response`          | string | The AI's natural-language reply.                     |
| `conversation_id`   | string | The same `conversation_id` sent in the request.       |

**Example request**

```json
POST /api/ai/chat
{
  "message": "Do you have any Python books?",
  "conversation_id": "conv-123"
}
```

**Example response**

```json
{
  "response": "Yes! We have 'Learn Python' by Guido, published in 2020, currently available.",
  "conversation_id": "conv-123"
}
```

Book-related questions (e.g. *"Show me books by Robert Martin"*,
*"Which programming books are available?"*) automatically trigger a search
of the library database via the `search_books` tool. Questions unrelated to
the library (e.g. *"How are you?"*) get a normal conversational reply
without querying the database.

Because conversation history is included with each request, you can ask
natural follow-up questions:

```json
{ "message": "What Python books are available?", "conversation_id": "conv-123" }
```
```json
{ "message": "Which one is better for beginners?", "conversation_id": "conv-123" }
```

**Error responses**

| Status | When it happens                                                                                                   |
|--------|------------------------------------------------------------------------------------------------------------------------|
| `422`  | `message` or `conversation_id` is empty, whitespace-only, or the message exceeds the maximum length.                  |
| `503`  | The AI service (OpenAI) is temporarily unavailable. The response includes a safe, user-friendly message — no internal error details, stack traces, or API keys are ever exposed. |

### Get conversation history

**`GET /api/ai/conversations/{conversation_id}/messages`**

Returns all messages exchanged in a given conversation, in chronological
order.

**Response body**

```json
{
  "messages": [
    { "role": "user", "content": "Do you have any Python books?" },
    { "role": "assistant", "content": "Yes! We have 'Learn Python' by Guido, published in 2020, currently available." }
  ]
}
```

If the conversation has no messages (or `conversation_id` is unknown),
`messages` is an empty list.

### How it works

```
User
  │
  ▼
POST /api/ai/chat
  │
  ▼
OpenAI  ──(decides if a book search is needed)──►  search_books tool
  │                                                      │
  │◄─────────────────(tool result)──────────────────────┘
  ▼
OpenAI  (generates final natural-language reply)
  │
  ▼
User
```

Conversation history is kept in memory per `conversation_id` and sent along
with each new message, so the assistant understands context across turns.

---

## Notes

- Conversation history is stored **in memory** and is not persisted across
  server restarts.
- User authentication is not implemented — this project focuses on the
  core book management and AI chat functionality.