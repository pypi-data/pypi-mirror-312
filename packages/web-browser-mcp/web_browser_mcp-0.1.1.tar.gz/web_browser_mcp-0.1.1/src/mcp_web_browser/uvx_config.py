from dataclasses import dataclass
from typing import Optional


@dataclass
class UvxCustomConfig:
    """Custom UVX configuration with additional settings."""

    app_path: str = "mcp_web_browser.server:create_app"
    factory: bool = True
    workers: int = 4
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    reload: bool = False
    proxy_headers: bool = True
    forwarded_allow_ips: str = "*"


def get_uvx_config(
    host: Optional[str] = None,
    port: Optional[int] = None,
    workers: Optional[int] = None,
    log_level: Optional[str] = None,
    reload: Optional[bool] = None,
) -> UvxCustomConfig:
    """
    Create UVX configuration with optional overrides.
    """
    config = UvxCustomConfig()

    if host is not None:
        config.host = host
    if port is not None:
        config.port = port
    if workers is not None:
        config.workers = workers
    if log_level is not None:
        config.log_level = log_level
    if reload is not None:
        config.reload = reload

    return config
