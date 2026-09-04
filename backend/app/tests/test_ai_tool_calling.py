from unittest.mock import patch, MagicMock
from app.services.ai_service import (
    generate_ai_response_with_tools,
    _execute_search_books_tool,
    SEARCH_BOOKS_TOOL,
)


def test_execute_search_books_tool_calls_search_service(session):
    from sqlmodel import delete
    from app.models.book import Book

    session.exec(delete(Book))
    session.commit()

    session.add(Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True))
    session.commit()

    result = _execute_search_books_tool(session, {"title": "python"})

    assert len(result) == 1
    assert result[0]["title"] == "Learn Python"


@patch("app.services.ai_service.get_openai_client")
def test_generate_ai_response_with_tools_executes_tool_when_requested(mock_get_client, session):
    from app.models.book import Book
    session.add(Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True))
    session.commit()

    mock_client = MagicMock()

    # Pehli response — model tool call maangta hai
    tool_call = MagicMock()
    tool_call.id = "call_1"
    tool_call.function.arguments = '{"title": "python"}'
    first_response = MagicMock()
    first_response.choices[0].message.tool_calls = [tool_call]

    # Dusri response — final natural language jawab
    second_response = MagicMock()
    second_response.choices[0].message.content = "Yes, we have Learn Python by Guido."
    second_response.choices[0].message.tool_calls = None

    mock_client.chat.completions.create.side_effect = [first_response, second_response]
    mock_get_client.return_value = mock_client

    result = generate_ai_response_with_tools(session, "Do you have Python books?")

    assert result == "Yes, we have Learn Python by Guido."
    assert mock_client.chat.completions.create.call_count == 2


@patch("app.services.ai_service.get_openai_client")
def test_generate_ai_response_with_tools_skips_tool_for_off_topic(mock_get_client, session):
    mock_client = MagicMock()
    response = MagicMock()
    response.choices[0].message.tool_calls = None
    response.choices[0].message.content = "I'm just a library assistant, but I'm doing well!"
    mock_client.chat.completions.create.return_value = response
    mock_get_client.return_value = mock_client

    result = generate_ai_response_with_tools(session, "How are you?")

    assert result == "I'm just a library assistant, but I'm doing well!"
    assert mock_client.chat.completions.create.call_count == 1