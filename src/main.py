"""Точка входа CLI — этап 4 (доп. операции)."""

import sys

from src.builder import build_dependency_graph
from src.config import load_config, success_code
from src.graph import print_graph, print_reverse_graph
from src.reverse import build_reverse_graph


def main(argv=None):
    """Строит граф или обратные зависимости."""
    args = load_config(argv)
    if args.reverse_deps:
        graph, cycles = build_reverse_graph(args)
        print_reverse_graph(graph, cycles)
    else:
        graph, cycles = build_dependency_graph(args)
        print_graph(graph, cycles)
    return success_code()


if __name__ == "__main__":
    sys.exit(main())