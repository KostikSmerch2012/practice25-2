"""Сбор прямых зависимостей пакета NuGet."""

import sys
import xml.etree.ElementTree as etree

from src.constants import EMPTY_COUNT, EXIT_ERROR
from src.http_fetch import fetch_text
from src.nuspec import parse_nuspec_deps
from src.version_spec import resolve_version


def collect_direct_deps(args):
    """Возвращает прямые зависимости по параметрам CLI."""
    if args.test_mode:
        return _from_test_repo(args.repo, args.package)
    return fetch_nuget_deps(
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


def fetch_nuget_deps(repo, package, version):
    """Загружает .nuspec и возвращает список (id, version)."""
    url = build_nuspec_url(repo, package, version)
    try:
        text = fetch_text(url)
        return parse_nuspec_deps(text)
    except etree.ParseError as err:
        _fail(f"некорректный .nuspec: {err}")
    except ValueError as err:
        _fail(str(err))


def load_test_graph(path):
    """Загружает граф вида 'A: B C' из текстового файла."""
    graph = {}
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            _add_test_line(graph, raw)
    return graph


def make_test_provider(path, version=""):
    """Провайдер соседей и версий для --test-mode."""
    graph = load_test_graph(path)
    versions = {}
    for name in graph:
        versions[name] = version

    def get_neighbors(package):
        key = package.strip().upper()
        return list(graph.get(key, []))

    return get_neighbors, versions


def make_nuget_provider(repo, root_package, root_version):
    """Провайдер соседей для NuGet flat container."""
    versions = {root_package: root_version}

    def get_neighbors(package):
        return _nuget_neighbors(repo, package, versions)

    return get_neighbors, versions


def print_deps(deps):
    """Печатает прямые зависимости пакета на экран."""
    print("=== Прямые зависимости ===")
    if len(deps) == EMPTY_COUNT:
        print("(нет)")
    else:
        for pkg_id, version in deps:
            _print_one_dep(pkg_id, version)
    print("==========================")


def _nuget_neighbors(repo, package, versions):
    """Возвращает имена прямых зависимостей пакета NuGet."""
    version = versions.get(package)
    if version is None:
        return []
    try:
        deps = _safe_fetch_nuget(repo, package, version)
    except ValueError:
        return []
    names = []
    for dep_id, spec in deps:
        if dep_id not in versions:
            versions[dep_id] = resolve_version(spec)
        names.append(dep_id)
    return names


def _safe_fetch_nuget(repo, package, version):
    """Загрузка .nuspec без завершения всего процесса."""
    url = build_nuspec_url(repo, package, version)
    text = fetch_text(url)
    return parse_nuspec_deps(text)


def _print_one_dep(pkg_id, version):
    """Печатает одну зависимость в удобном виде."""
    if len(version) == EMPTY_COUNT:
        print(pkg_id)
    else:
        print(f"{pkg_id} {version}")


def _from_test_repo(path, package):
    """Читает прямые зависимости из тестового файла."""
    graph = load_test_graph(path)
    key = package.strip().upper()
    if key not in graph:
        _fail(
            f"пакет {package} отсутствует "
            "в тестовом репозитории"
        )
    names = graph[key]
    return [(name, "") for name in names]


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
