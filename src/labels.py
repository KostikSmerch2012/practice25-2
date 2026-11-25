"""Подписи узлов графа: имя и версия пакета."""

from src.constants import EMPTY_COUNT


def format_label(name, versions):
    """Возвращает 'Name version' или только имя."""
    if versions is None:
        return name
    ver = versions.get(name, "")
    if ver is None or len(str(ver)) == EMPTY_COUNT:
        return name
    return f"{name} {ver}"


def node_list(graph):
    """Все имена пакетов из графа без дублей."""
    names = set(graph.keys())
    for deps in graph.values():
        for item in deps:
            names.add(item)
    return sorted(names)
