import json
from pathlib import Path
from typing import Any

from app.config import settings


BASE_DIR = Path(__file__).resolve().parent
LOCALES_DIR = BASE_DIR / "locales"


def load_locale(language: str) -> dict[str, Any]:
    locale_file = LOCALES_DIR / f"{language}.json"

    if not locale_file.exists():
        locale_file = LOCALES_DIR / f"{settings.default_language}.json"

    if not locale_file.exists():
        locale_file = LOCALES_DIR / "en.json"

    with locale_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def t(key: str, language: str | None = None, **kwargs: Any) -> str:
    selected_language = language or settings.default_language
    messages = load_locale(selected_language)

    text = messages.get(key)

    if text is None:
        fallback_messages = load_locale("en")
        text = fallback_messages.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text
