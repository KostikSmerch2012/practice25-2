"""Точка входа CLI — этап 5 (визуализация)."""

import sys

from src.builder import build_dependency_graph
from src.config import load_config, success_code
from src.graph import print_graph, print_reverse_graph
from src.reverse import build_reverse_graph
from src.visualize import render_visualization


def main(argv=None):
    """Строит граф, визуализирует его и печатает."""
    args = load_config(argv)
    graph, cycles, versions = _select_graph(args)
    render_visualization(args, graph, versions)
    return success_code()


def _select_graph(args):
    """Выбирает прямой или обратный граф и печатает его."""
    if args.reverse_deps:
        graph, cycles, versions = build_reverse_graph(args)
        print_reverse_graph(graph, cycles, versions)
        return graph, cycles, versions
    graph, cycles, versions = build_dependency_graph(args)
    print_graph(graph, cycles, versions)
    return graph, cycles, versions


if __name__ == "__main__":
    sys.exit(main())
