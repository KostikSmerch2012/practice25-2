"""Разбор прямых зависимостей из XML .nuspec."""

import xml.etree.ElementTree as et

from src.constants import EMPTY_COUNT


def parse_nuspec_deps(text):
    """Возвращает список пар (id, version) без дублей."""
    if text is None or len(text.strip()) == EMPTY_COUNT:
        raise ValueError("пустой ответ .nuspec")
    root = et.fromstring(text)
    deps = []
    seen = set()
    for node in root.iter():
        if _local_name(node.tag) != "dependency":
            continue
        item = _read_dependency(node)
        if item is None:
            continue
        key = item[0].lower()
        if key in seen:
            continue
        seen.add(key)
        deps.append(item)
    return deps


def _local_name(tag):
    """Извлекает локальное имя XML-тега без namespace."""
    if tag.startswith("{"):
        return tag.rsplit("}", 1)[-1]
    return tag


def _read_dependency(node):
    """Читает атрибуты id и version узла dependency."""
    pkg_id = node.attrib.get("id", "").strip()
    version = node.attrib.get("version", "").strip()
    if len(pkg_id) == EMPTY_COUNT:
        return None
    return (pkg_id, version)
