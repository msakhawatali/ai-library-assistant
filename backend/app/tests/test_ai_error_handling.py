from unittest.mock import patch, MagicMock
from openai import APIError, APIConnectionError, RateLimitError
from app.services.ai_service import generate_ai_response, AIServiceError


@patch("app.services.ai_service.get_openai_client")
def test_generate_ai_response_raises_ai_service_error_on_openai_failure(mock_get_client):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = APIConnectionError(request=MagicMock())
    mock_get_client.return_value = mock_client

    try:
        generate_ai_response("Hello")
        assert False, "Expected AIServiceError to be raised"
    except AIServiceError as e:
        assert "unavailable" in str(e).lower()
        assert "APIConnectionError" not in str(e)  # internal exception details leak na ho


@patch("app.services.ai_service.get_openai_client")
def test_generate_ai_response_handles_unexpected_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = ValueError("some internal bug")
    mock_get_client.return_value = mock_client

    try:
        generate_ai_response("Hello")
        assert False, "Expected AIServiceError to be raised"
    except AIServiceError as e:
        assert "some internal bug" not in str(e)