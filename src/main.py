"""Точка входа CLI — этап 3 (основные операции)."""

import sys

from src.builder import build_dependency_graph
from src.config import load_config, success_code
from src.graph import print_graph


def main(argv=None):
    """Читает CLI, строит граф DFS и печатает результат."""
    args = load_config(argv)
    graph, cycles = build_dependency_graph(args)
    print_graph(graph, cycles)
    return success_code()


if __name__ == "__main__":
    sys.exit(main())
