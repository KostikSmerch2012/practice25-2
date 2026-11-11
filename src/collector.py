"""Сбор прямых зависимостей пакета NuGet."""

import sys
import xml.etree.ElementTree as etree

from src.constants import EMPTY_COUNT, EXIT_ERROR
from src.http_fetch import fetch_text
from src.nuspec import parse_nuspec_deps


def collect_direct_deps(args):
    """Возвращает прямые зависимости по параметрам CLI."""
    if args.test_mode:
        return _from_test_repo(args.repo, args.package)
    return _from_nuget(
        args.repo,
        args.package,
        args.version,
    )


def build_nuspec_url(repo, package, version):
    """Строит URL .nuspec в NuGet flat container."""
    base = repo.rstrip("/")
    pkg = package.lower()
    ver = version.lower()
    return f"{base}/{pkg}/{ver}/{pkg}.nuspec"


def print_deps(deps):
    """Печатает прямые зависимости пакета на экран."""
    print("=== Прямые зависимости ===")
    if len(deps) == EMPTY_COUNT:
        print("(нет)")
    else:
        for pkg_id, version in deps:
            _print_one_dep(pkg_id, version)
    print("==========================")


def _print_one_dep(pkg_id, version):
    """Печатает одну зависимость в удобном виде."""
    if len(version) == EMPTY_COUNT:
        print(pkg_id)
    else:
        print(f"{pkg_id} {version}")


def _from_nuget(repo, package, version):
    """Загружает .nuspec из репозитория и разбирает его."""
    url = build_nuspec_url(repo, package, version)
    try:
        text = fetch_text(url)
        return parse_nuspec_deps(text)
    except etree.ParseError as err:
        _fail(f"некорректный .nuspec: {err}")
    except ValueError as err:
        _fail(str(err))


def _from_test_repo(path, package):
    """Читает прямые зависимости из тестового файла."""
    graph = _load_test_graph(path)
    key = package.strip().upper()
    if key not in graph:
        _fail(
            f"пакет {package} отсутствует "
            "в тестовом репозитории"
        )
    names = graph[key]
    return [(name, "") for name in names]


def _load_test_graph(path):
    """Загружает граф вида 'A: B C' из текстового файла."""
    graph = {}
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            _add_test_line(graph, raw)
    return graph


def _add_test_line(graph, raw):
    """Добавляет одну строку тестового репозитория."""
    line = raw.strip()
    if len(line) == EMPTY_COUNT:
        return
    if line.startswith("#"):
        return
    node, _, rest = line.partition(":")
    name = node.strip().upper()
    if len(name) == EMPTY_COUNT:
        return
    parts = rest.strip().split()
    deps = [item.upper() for item in parts]
    graph[name] = deps


def _fail(message):
    """Печатает ошибку и завершает процесс."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(EXIT_ERROR)
