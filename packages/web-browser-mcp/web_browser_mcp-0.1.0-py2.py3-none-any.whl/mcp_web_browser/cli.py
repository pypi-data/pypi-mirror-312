import click
import uvicorn
from .config import Settings

@click.command()
@click.option('--host', default=None, help='Host address to bind to')
@click.option('--port', default=None, type=int, help='Port to bind to')
@click.option('--workers', default=None, type=int, help='Number of worker processes')
@click.option('--log-level', default=None, 
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']), 
              help='Logging level')
@click.option('--reload/--no-reload', default=None, help='Enable auto-reload')
def main(host, port, workers, log_level, reload):
    """Run the MCP web browser server using uvicorn within the uv-managed environment."""
    settings = Settings()
    
    # Override settings with command line arguments if provided
    if host:
        settings.HOST = host
    if port:
        settings.PORT = port
    if log_level:
        settings.LOG_LEVEL = log_level
    if reload is not None:
        settings.RELOAD = reload

    config = uvicorn.Config(
        "mcp_web_browser.server:create_app",
        factory=True,
        host=settings.HOST,
        port=settings.PORT,
        workers=workers or 1,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.RELOAD,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )
    
    server = uvicorn.Server(config=config)
    server.run()

if __name__ == '__main__':
    main()