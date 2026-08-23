from unittest.mock import patch, MagicMock
from app.services.ai_service import extract_search_filters


@patch("app.services.ai_service.get_openai_client")
def test_extract_filters_returns_parsed_json(mock_get_client):
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '{"author": "Robert Martin"}'
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    filters = extract_search_filters("Show me books by Robert Martin")

    assert filters == {"author": "Robert Martin"}


@patch("app.services.ai_service.get_openai_client")
def test_extract_filters_returns_empty_dict_when_no_filters(mock_get_client):
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = '{}'
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    filters = extract_search_filters("Hello, how are you?")

    assert filters == {}


@patch("app.services.ai_service.get_openai_client")
def test_extract_filters_handles_invalid_json_gracefully(mock_get_client):
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "not valid json"
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    filters = extract_search_filters("some message")

    assert filters == {}