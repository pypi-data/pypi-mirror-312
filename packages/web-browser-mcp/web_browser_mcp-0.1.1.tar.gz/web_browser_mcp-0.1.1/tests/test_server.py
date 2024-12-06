import pytest
from fastapi.testclient import TestClient
from mcp_web_browser.server import app
from unittest.mock import patch
from unittest.mock import AsyncMock


@pytest.fixture
def client():
    return TestClient(app)


def test_list_resources(client):
    response = client.get("/resources")
    assert response.status_code == 200
    resources = response.json()
    assert len(resources) == 1
    assert resources[0]["uri"] == "web://browser/capabilities"
    assert resources[0]["mimeType"] == "application/json"


def test_read_resource(client):
    response = client.get("/resource/web://browser/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert "features" in data
    assert isinstance(data["timeout"], int)
    assert isinstance(data["user_agent"], str)


def test_parse_webpage(client):
    mock_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <a href="https://test.com">Test Link</a>
            <div class="content">Test Content</div>
        </body>
    </html>
    """

    with patch("aiohttp.ClientSession.get") as mock_get:
        # Create a mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value=mock_html)

        # Set up the context manager to return our mock response
        mock_get.return_value.__aenter__.return_value = mock_response

        response = client.post(
            "/parse",
            json={"url": "https://test.com", "selectors": {"content": ".content"}},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Page"
        assert "Test Link" in str(data["content"]["text"])
