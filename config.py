import json
import os
from pathlib import Path


def config_path() -> Path:
    appdata = os.environ.get("APPDATA") or Path.home()
    p = Path(appdata) / "ExarotonRemote"
    p.mkdir(parents=True, exist_ok=True)
    return p / "config.json"


def load_token() -> str | None:
    try:
        with open(config_path()) as f:
            return json.load(f).get("token")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_token(token: str):
    with open(config_path(), "w") as f:
        json.dump({"token": token}, f)
