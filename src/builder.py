"""Сборка полного графа зависимостей по конфигу CLI."""

from src.collector import make_nuget_provider, make_test_provider
from src.graph import build_graph_dfs


def build_dependency_graph(args):
    """Строит граф, циклы и словарь версий."""
    root, provider, versions = _make_root_and_provider(args)
    graph, cycles = build_graph_dfs(root, provider, args.filter)
    return graph, cycles, versions


def _make_root_and_provider(args):
    """Готовит корень обхода, соседей и версии."""
    if args.test_mode:
        root = args.package.strip().upper()
        pair = make_test_provider(args.repo, args.version)
        provider, versions = pair
        return root, provider, versions
    root = args.package
    pair = make_nuget_provider(
        args.repo,
        args.package,
        args.version,
    )
    provider, versions = pair
    return root, provider, versions
