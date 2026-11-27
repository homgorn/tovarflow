"""Local configuration loader.

The API key is read from the environment or a gitignored .env file. It is never written to
logs, reports or the knowledge base. Use tools/openchamber_secret (private card) if you need
to ask the owner for a key; never ask for it in chat.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get(name: str, default: str | None = None) -> str | None:
    example = load_env(ROOT / ".env.example")
    return os.environ.get(name) or load_env().get(name) or example.get(name) or default


def qparser_config() -> dict:
    use_mock = str(get("USE_MOCK", "0")).lower() in ("1", "true", "yes")
    base_url = get("QPARSER_MOCK_URL" if use_mock else "QPARSER_BASE_URL",
                   "http://127.0.0.1:8765/api/v1" if use_mock else "https://q-parser.ru/api/v1")
    key = "mock" if use_mock else get("QPARSER_API_KEY")
    if not use_mock and (not key or key.startswith("replace_with")):
        raise RuntimeError(
            "QPARSER_API_KEY is missing. Copy .env.example to .env and paste the key from "
            "https://q-parser.ru/my/profile, or set USE_MOCK=1 for local development."
        )
    return {"base_url": base_url, "api_key": key, "use_mock": use_mock}


def redact(value: str | None) -> str:
    if not value:
        return "(none)"
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "*" * (len(value) - 8) + value[-4:]
