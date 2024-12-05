"""Library-wide configuration"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from dotenv import load_dotenv

PREFIX = "LSEG_ANALYTICS_"
AUTH_PREFIX = f"{PREFIX}AUTH_"
HEADERS_PREFIX = "HTTP_HEADER_"
DEFAULT_SPACE = "Anonymous"


@dataclass
class AuthConfig:
    """Configuration object"""

    client_id: str
    client_secret: str
    token_endpoint: str

    scopes: Optional[List[str]] = None


@dataclass
class Config:
    """Configuration object"""

    base_url: str
    username: Optional[str] = None
    headers: Optional[Dict] = None

    auth: Optional[AuthConfig] = None


def load_config() -> Config:
    """Create configuration object from the environment variables"""

    load_dotenv()

    headers = {
        key.split(HEADERS_PREFIX).pop().replace("_", "-"): value
        for key, value in os.environ.items()
        if key.startswith(HEADERS_PREFIX)
    }

    auth = None
    if os.getenv(f"{AUTH_PREFIX}CLIENT_ID") and os.getenv(f"{AUTH_PREFIX}CLIENT_SECRET"):
        auth = AuthConfig(
            client_id=os.getenv(f"{AUTH_PREFIX}CLIENT_ID"),
            client_secret=os.getenv(f"{AUTH_PREFIX}CLIENT_SECRET"),
            token_endpoint=os.getenv(
                f"{AUTH_PREFIX}TOKEN_ENDPOINT", "https://login.ciam.refinitiv.com/as/token.oauth2"
            ),
            scopes=os.getenv(f"{AUTH_PREFIX}SCOPES", "trapi").split(","),
        )

    return Config(
        base_url=os.getenv(f"{PREFIX}BASE_URL", "https://api.analytics.lseg.com"),
        username=os.getenv(f"{PREFIX}USERNAME"),
        headers=headers,
        auth=auth,
    )
