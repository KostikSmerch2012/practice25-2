"""Разбор строки версии из .nuspec зависимости."""

from src.constants import EMPTY_COUNT


def resolve_version(spec):
    """Возвращает конкретную версию из диапазона NuGet."""
    if spec is None:
        return ""
    text = str(spec).strip()
    if len(text) == EMPTY_COUNT:
        return ""
    cleaned = _strip_range_chars(text)
    parts = cleaned.replace(",", " ").split()
    if len(parts) == EMPTY_COUNT:
        return text
    return parts[0]


def _strip_range_chars(text):
    """Убирает скобки диапазона версий NuGet."""
    result = text
    for char in "[]()":
        result = result.replace(char, " ")
    return result
