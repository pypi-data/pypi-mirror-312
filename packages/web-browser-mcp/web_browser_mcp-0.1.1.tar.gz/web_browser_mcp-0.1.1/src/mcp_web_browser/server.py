from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from .config import Settings
from pydantic import BaseModel, AnyUrl
from mcp.types import Resource

settings = Settings()
app = FastAPI(
    title=settings.APP_NAME,
    description="MCP server for web browsing with BeautifulSoup4",
    version="0.1.0",
)


class WebPageRequest(BaseModel):
    url: str
    selectors: Optional[Dict[str, str]] = None


class WebPageResponse(BaseModel):
    url: str
    title: Optional[str] = None
    content: Dict[str, Any]
    status_code: int


@app.get("/resources")
async def list_resources() -> List[Resource]:
    """List available web browsing resources."""
    return [
        Resource(
            uri=AnyUrl("web://browser/capabilities"),
            name="Web Browser Capabilities",
            mimeType="application/json",
            description="Available web browsing features and settings",
        )
    ]


@app.get("/resource/{uri:path}")
async def read_resource(uri: AnyUrl) -> Dict[str, Any]:
    """Read a specific web browsing resource."""
    if str(uri) == "web://browser/capabilities":
        return {
            "features": ["content_extraction", "link_discovery", "metadata_capture"],
            "supported_selectors": ["css", "xpath"],
            "timeout": settings.REQUEST_TIMEOUT,
            "user_agent": settings.USER_AGENT,
        }
    raise HTTPException(status_code=404, detail=f"Resource not found: {uri}")


@app.post("/parse", response_model=WebPageResponse)
async def parse_webpage(request: WebPageRequest):
    async with aiohttp.ClientSession() as session:
        try:
            headers = {"User-Agent": settings.USER_AGENT}
            timeout = aiohttp.ClientTimeout(total=settings.REQUEST_TIMEOUT)
            async with session.get(
                request.url, headers=headers, timeout=timeout
            ) as response:
                if response.status >= 400:
                    raise HTTPException(
                        status_code=400,
                        detail=f"HTTP {response.status}: Failed to fetch webpage",
                    )

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                result = {
                    "text": soup.get_text(strip=True),
                    "links": [
                        {"text": link.text.strip(), "href": link.get("href")}
                        for link in soup.find_all("a", href=True)
                    ],
                }

                if request.selectors:
                    for key, selector in request.selectors.items():
                        elements = soup.select(selector)
                        result[key] = [elem.get_text(strip=True) for elem in elements]

                return WebPageResponse(
                    url=request.url,
                    title=soup.title.string if soup.title else None,
                    content=result,
                    status_code=response.status,
                )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=400, detail="Request timed out while fetching webpage"
            )
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=400, detail=str(e))


async def main():
    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())
