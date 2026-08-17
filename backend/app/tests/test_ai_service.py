from unittest.mock import patch

from openai import OpenAI

from app.services.ai_service import get_openai_client


def test_get_openai_client_returns_client():
    client = get_openai_client()

    assert isinstance(client, OpenAI)


@patch("app.services.ai_service.settings")
def test_get_openai_client_uses_configured_api_key(mock_settings):
    mock_settings.openai_api_key = "test-key-123"

    client = get_openai_client()

    assert client.api_key == "test-key-123" 