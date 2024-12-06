# Web Intelligence MCP Server

Transform your AI applications with advanced web browsing capabilities. This Model Context Protocol (MCP) server empowers AI systems to intelligently navigate, extract, and analyze web content with precision and reliability.

## Overview

The Web Intelligence MCP server bridges the gap between AI systems and web content, enabling sophisticated web browsing capabilities through a robust, production-ready API. By leveraging the power of BeautifulSoup4 and modern async processing, it provides AI applications with the ability to understand and extract structured information from any webpage.

## Key Features

The server provides enterprise-grade capabilities for web content processing:

- Intelligent content extraction with customizable CSS selectors
- High-performance asynchronous processing
- Comprehensive metadata capture including titles, links, and structured content
- Robust error handling and timeout management
- Production-ready security features
- Cross-platform compatibility

## Integration with Claude and AI Applications

Seamlessly integrate web browsing capabilities into your AI workflows by adding this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "web-intelligence": {
      "module": "web-browser-mcp",
      "env": {
        "REQUEST_TIMEOUT": "30"
      }
    }
  }
}
```

## Enterprise-Ready Features

Our implementation focuses on reliability and security:

- Configurable timeout and retry mechanisms
- Comprehensive error handling
- Rate limiting and resource protection
- Detailed logging and monitoring capabilities
- Production-grade async processing
- Cross-origin request security

## API Example

Extract structured content from web pages with precision:

```python
response = requests.post(
    "http://localhost:8000/parse",
    json={
        "url": "https://example.com",
        "selectors": {
            "article_content": "article.main-content",
            "headlines": "h1.headline",
            "metadata": ".meta-tags"
        }
    }
)

structured_content = response.json()
```

## Development and Testing

We maintain high standards for code quality and testing:

```bash
# Set up development environment
uv venv
source .venv/bin/activate
uv pip install -e ".[test]"

# Run comprehensive test suite
python -m pytest
```

## Security Considerations

The server implements industry-standard security practices:

- Input validation and sanitization
- Secure request handling
- Timeout controls
- Rate limiting
- Error handling without information exposure

## Production Deployment

Deploy with confidence using our production-ready configuration:

```bash
python -m mcp_web_browser.cli --workers 4 --log-level warning
```

## Contributing

We welcome contributions that enhance the server's capabilities. Please review our contributing guidelines and code of conduct.

## License

This project is licensed under the MIT License, providing flexibility for both personal and commercial use.

---

*Empower your AI applications with intelligent web browsing capabilities. Start integrating today.*