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
    """Launch the MCP web browser server with production-grade settings."""
    settings = Settings()
    
    config = uvicorn.Config(
        app="mcp_web_browser.server:create_app",
        factory=True,
        host=host or settings.HOST,
        port=port or settings.PORT,
        workers=workers or 4,
        log_level=(log_level or settings.LOG_LEVEL).lower(),
        reload=reload if reload is not None else settings.RELOAD,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )
    
    server = uvicorn.Server(config=config)
    server.run()

if __name__ == '__main__':
    main()