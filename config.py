from __future__ import annotations
import json
import os
from pathlib import Path


def config_path() -> Path:
    appdata = os.environ.get("APPDATA") or Path.home()
    p = Path(appdata) / "ExarotonRemote"
    p.mkdir(parents=True, exist_ok=True)
    return p / "config.json"


def _load() -> dict:
    try:
        with open(config_path()) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(data: dict):
    with open(config_path(), "w") as f:
        json.dump(data, f, indent=2)


def load_token() -> str | None:
    return _load().get("token")


def save_token(token: str):
    data = _load()
    data["token"] = token
    _save(data)


def load_favorites() -> set[str]:
    return set(_load().get("favorites", []))


def save_favorites(favorites: set[str]):
    data = _load()
    data["favorites"] = sorted(favorites)
    _save(data)
