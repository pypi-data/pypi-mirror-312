import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from schwab.auth import easy_client

logger = logging.getLogger(__name__)


def get_schwab_client(config_file="~/.config/chucks/config.json"):
    """Easier easy client."""

    config_file_path = Path(config_file).expanduser()

    with open(config_file_path) as f:
        config = json.load(f)

    return easy_client(
        config.get("client_id"),
        config.get("client_secret"),
        config.get("redirect_uri"),
        Path.home().joinpath(".config/chucks/access_token.json"),
    )


def token_creation_date(schwab_client):
    """Get token creation date."""
    return datetime.ctime(
        datetime.now(tz=timezone.UTC) - timedelta(seconds=schwab_client.token_age())
    )
