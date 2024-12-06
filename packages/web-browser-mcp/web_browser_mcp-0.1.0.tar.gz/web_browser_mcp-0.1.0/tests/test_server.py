import pytest
import asyncio  # noqa: F401
from fastapi.testclient import TestClient
import aiohttp
from mcp_web_browser.config import Settings
from mcp_web_browser.server import create_app
from aioresponses import aioresponses


@pytest.fixture
def settings():
    return Settings(DEBUG=True)


@pytest.fixture
async def app(settings):
    return await create_app(settings)


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mock:
        yield mock


@pytest.mark.asyncio
async def test_successful_webpage_parsing(client, mock_aioresponse):
    test_html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Main Heading</h1>
                <p>Test paragraph</p>
                <a href="https://example.com/link1">Link 1</a>
                <a href="https://example.com/link2">Link 2</a>
            </body>
        </html>
    """

    mock_aioresponse.get("http://example.com", status=200, body=test_html)

    response = client.post(
        "/parse",
        json={
            "url": "http://example.com",
            "selectors": {"headings": "h1", "paragraphs": "p"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "http://example.com"
    assert data["title"] == "Test Page"
    assert "Main Heading" in data["content"]["headings"]
    assert "Test paragraph" in data["content"]["paragraphs"]
    assert len(data["content"]["links"]) == 2


@pytest.mark.asyncio
async def test_timeout_handling(client, mock_aioresponse):
    mock_aioresponse.get(
        "http://example.com", exception=aiohttp.ServerTimeoutError("Request timed out")
    )

    response = client.post(
        "/parse", json={"url": "http://example.com", "selectors": {"headings": "h1"}}
    )

    assert response.status_code == 400
    assert "timed out" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_http_error_handling(client, mock_aioresponse):
    mock_aioresponse.get("http://example.com", status=404, body="Not Found")

    response = client.post(
        "/parse", json={"url": "http://example.com", "selectors": {"headings": "h1"}}
    )

    assert response.status_code == 400
    assert "404" in response.json()["detail"]
