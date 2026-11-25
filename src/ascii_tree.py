"""ASCII-дерево зависимостей без рекурсии."""

from src.constants import EMPTY_COUNT


def print_ascii_tree(root, graph):
    """Печатает дерево от корня, если задан --ascii-tree."""
    print("=== ASCII-дерево ===")
    if root not in graph:
        print("(пусто)")
        print("====================")
        return
    print(root)
    _print_children(root, "", graph)
    print("====================")


def _print_children(node, prefix, graph):
    """Печатает детей узла через стек."""
    childs = graph.get(node, [])
    stack = []
    for idx in range(len(childs) - 1, -1, -1):
        stack.append(
            (
                childs[idx],
                prefix,
                idx == len(childs) - 1,
                {node},
            )
        )
    while len(stack) > EMPTY_COUNT:
        _pop_one_child(stack, graph)


def _pop_one_child(stack, graph):
    """Обрабатывает один элемент стека."""
    child, base, is_last, path = stack.pop()
    branch = "└── " if is_last else "├── "
    ext = "    " if is_last else "│   "
    if child in path:
        print(base + branch + child + " (цикл)")
        return
    print(base + branch + child)
    next_path = set(path)
    next_path.add(child)
    _push_grandkids(stack, child, base + ext, graph, next_path)


def _push_grandkids(stack, node, prefix, graph, path):
    """Добавляет детей узла на стек."""
    childs = graph.get(node, [])
    for idx in range(len(childs) - 1, -1, -1):
        stack.append(
            (
                childs[idx],
                prefix,
                idx == len(childs) - 1,
                path,
            )
        )