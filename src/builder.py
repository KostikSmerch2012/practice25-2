"""Сборка полного графа зависимостей по конфигу CLI."""

from src.collector import make_nuget_provider, make_test_provider
from src.graph import build_graph_dfs


def build_dependency_graph(args):
    """Строит граф и список циклов по параметрам запуска."""
    root, provider = _make_root_and_provider(args)
    return build_graph_dfs(root, provider, args.filter)


def _make_root_and_provider(args):
    """Готовит корень обхода и функцию соседей."""
    if args.test_mode:
        root = args.package.strip().upper()
        provider = make_test_provider(args.repo)
        return root, provider
    root = args.package
    provider = make_nuget_provider(
        args.repo,
        args.package,
        args.version,
    )
    return root, provider
