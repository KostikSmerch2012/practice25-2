"""Обратные зависимости: DFS по инвертированному графу."""

import sys

from src.builder import build_dependency_graph
from src.collector import load_test_graph
from src.constants import EXIT_ERROR
from src.graph import build_graph_dfs, invert_adjacency


def build_reverse_graph(args):
    """Возвращает обратный граф и циклы для --package."""
    if args.test_mode:
        return _reverse_from_test(args)
    return _reverse_from_nuget(args)


def _reverse_from_test(args):
    """Обратные зависимости из полного тестового файла."""
    forward = load_test_graph(args.repo)
    root = args.package.strip().upper()
    if root not in forward:
        _fail(
            f"пакет {args.package} отсутствует "
            "в тестовом репозитории"
        )
    reverse = invert_adjacency(forward)
    return _dfs_reverse(root, reverse, args.filter)


def _reverse_from_nuget(args):
    """Обратные зависимости внутри построенного NuGet-графа."""
    forward, _ = build_dependency_graph(args)
    reverse = invert_adjacency(forward)
    root = args.package
    return _dfs_reverse(root, reverse, args.filter)


def _dfs_reverse(root, reverse, filt):
    """Запускает DFS по обратному графу."""

    def get_neighbors(name):
        return list(reverse.get(name, []))

    return build_graph_dfs(root, get_neighbors, filt)


def _fail(message):
    """Печатает ошибку и завершает процесс."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(EXIT_ERROR)