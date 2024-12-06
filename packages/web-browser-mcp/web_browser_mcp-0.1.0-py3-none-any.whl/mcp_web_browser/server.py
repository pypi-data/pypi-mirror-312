from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from typing import Optional, Dict, Any
from .config import Settings
from pydantic import BaseModel

class WebPageRequest(BaseModel):
    url: str
    selectors: Optional[Dict[str, str]] = None

class WebPageResponse(BaseModel):
    url: str
    title: Optional[str] = None
    content: Dict[str, Any]
    status_code: int

async def create_app(settings: Optional[Settings] = None) -> FastAPI:
    if settings is None:
        settings = Settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="MCP server for web browsing with BeautifulSoup4",
        version="0.1.0"
    )

    @app.post("/parse", response_model=WebPageResponse)
    async def parse_webpage(request: WebPageRequest):
        async with aiohttp.ClientSession() as session:
            try:
                headers = {"User-Agent": settings.USER_AGENT}
                timeout = aiohttp.ClientTimeout(total=settings.REQUEST_TIMEOUT)
                async with session.get(
                    request.url, 
                    headers=headers, 
                    timeout=timeout
                ) as response:
                    if response.status >= 400:
                        raise HTTPException(
                            status_code=400,
                            detail=f"HTTP {response.status}: Failed to fetch webpage"
                        )
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    result = {
                        "text": soup.get_text(strip=True),
                        "links": [{
                            "text": link.text.strip(),
                            "href": link.get('href')
                        } for link in soup.find_all('a', href=True)]
                    }
                    
                    if request.selectors:
                        for key, selector in request.selectors.items():
                            elements = soup.select(selector)
                            result[key] = [elem.get_text(strip=True) for elem in elements]
                    
                    return WebPageResponse(
                        url=request.url,
                        title=soup.title.string if soup.title else None,
                        content=result,
                        status_code=response.status
                    )
            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=400,
                    detail="Request timed out while fetching webpage"
                )
            except aiohttp.ClientError as e:
                raise HTTPException(status_code=400, detail=str(e))
    
    return app