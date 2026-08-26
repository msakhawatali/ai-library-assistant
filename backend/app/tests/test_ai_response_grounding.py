from unittest.mock import patch, MagicMock
from app.services.ai_service import generate_ai_response


@patch("app.services.ai_service.get_openai_client")
def test_prompt_instructs_model_to_use_only_provided_context(mock_get_client):
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "response"
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    book_context = [{
        "id": 1, "title": "Learn Python", "author": "Guido",
        "category": "Programming", "year": 2020, "available": True,
    }]
    generate_ai_response("Do you have Python books?", book_context=book_context)

    sent_messages = mock_client.chat.completions.create.call_args.kwargs["messages"]
    system_message = sent_messages[0]["content"]

    assert "Learn Python" in system_message
    assert "never invent" in system_message.lower() or "do not invent" in system_message.lower()


@patch("app.services.ai_service.get_openai_client")
def test_prompt_handles_no_matching_books(mock_get_client):
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "response"
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    generate_ai_response("Do you have anything?", book_context=[])

    sent_messages = mock_client.chat.completions.create.call_args.kwargs["messages"]
    system_message = sent_messages[0]["content"]

    assert "no relevant books" in system_message.lower() or "no book" in system_message.lower()