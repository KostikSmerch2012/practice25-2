"""Текст диаграммы Mermaid для графа зависимостей."""

from src.constants import EMPTY_COUNT
from src.labels import format_label, node_list


def build_mermaid(graph, versions=None):
    """Возвращает текст flowchart TD с версиями."""
    lines = ["flowchart TD"]
    if len(graph) == EMPTY_COUNT:
        lines.append("  empty[нет данных]")
        return "\n".join(lines)
    names = node_list(graph)
    for name in names:
        mid = mermaid_node_id(name)
        label = format_label(name, versions)
        lines.append(f'  {mid}["{label}"]')
    for src, dsts in graph.items():
        sid = mermaid_node_id(src)
        for dst in dsts:
            did = mermaid_node_id(dst)
            lines.append(f"  {sid} --> {did}")
    return "\n".join(lines)


def print_mermaid(graph, versions=None):
    """Печатает блок Mermaid на экран."""
    text = build_mermaid(graph, versions)
    print("=== Mermaid ===")
    print(text)
    print("===============")


def mermaid_node_id(name):
    """Безопасный идентификатор узла Mermaid."""
    parts = []
    for ch in name:
        if ch.isalnum():
            parts.append(ch)
        else:
            parts.append("_")
    result = "".join(parts)
    if len(result) == EMPTY_COUNT:
        return "node"
    return result
