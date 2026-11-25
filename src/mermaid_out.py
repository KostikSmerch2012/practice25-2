"""Текст диаграммы Mermaid для графа зависимостей."""

from src.constants import EMPTY_COUNT


def build_mermaid(graph):
    """Возвращает текст flowchart TD для графа."""
    lines = ["flowchart TD"]
    if len(graph) == EMPTY_COUNT:
        lines.append("  empty[нет данных]")
        return "\n".join(lines)
    nodes = set(graph.keys())
    for vals in graph.values():
        for item in vals:
            nodes.add(item)
    for name in sorted(nodes):
        mid = mermaid_node_id(name)
        lines.append(f'  {mid}["{name}"]')
    for src, dsts in graph.items():
        sid = mermaid_node_id(src)
        for dst in dsts:
            did = mermaid_node_id(dst)
            lines.append(f"  {sid} --> {did}")
    return "\n".join(lines)


def print_mermaid(graph):
    """Печатает блок Mermaid на экран."""
    text = build_mermaid(graph)
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