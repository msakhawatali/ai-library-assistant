from unittest.mock import patch
from app.services.ai_service import get_openai_client


def test_get_openai_client_returns_client_instance():
    client = get_openai_client()
    assert client is not None
    assert client.api_key is not None


@patch("app.services.ai_service.settings")
def test_client_uses_configured_api_key(mock_settings):
    mock_settings.openai_api_key = "test-key-123"
    client = get_openai_client()
    assert client.api_key == "test-key-123"