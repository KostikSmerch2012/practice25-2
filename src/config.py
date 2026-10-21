"""Разбор и проверка параметров командной строки."""

import argparse
import os
import sys

from src.constants import EXIT_ERROR, EXIT_OK


def build_parser():
    """Создаёт парсер опций CLI для варианта 25."""
    parser = argparse.ArgumentParser(
        description=(
            "Визуализация графа зависимостей NuGet"
        ),
    )
    _add_core_args(parser)
    _add_mode_args(parser)
    return parser


def _add_core_args(parser):
    """Добавляет основные параметры пакета и репозитория."""
    parser.add_argument(
        "--package",
        help="Имя анализируемого пакета",
    )
    parser.add_argument(
        "--repo",
        help=(
            "URL репозитория или путь к тестовому файлу"
        ),
    )
    parser.add_argument(
        "--version",
        help="Версия пакета",
    )
    parser.add_argument(
        "--filter",
        default="",
        help="Подстрока для фильтрации пакетов",
    )


def _add_mode_args(parser):
    """Добавляет флаги режимов работы."""
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым репозиторием",
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Вывод зависимостей в виде ASCII-дерева",
    )


def _fail(message):
    """Печатает ошибку и завершает процесс."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(EXIT_ERROR)


def validate_config(args):
    """Проверяет все настраиваемые параметры."""
    if not args.package:
        _fail("не задан параметр --package")
    if not args.repo:
        _fail("не задан параметр --repo")
    if not args.version:
        _fail("не задан параметр --version")

    package = args.package.strip()
    version = args.version.strip()
    repo = args.repo.strip()
    filt = args.filter if args.filter else ""

    if not package:
        _fail("имя пакета не может быть пустым")
    if not version:
        _fail("версия пакета не может быть пустой")
    if not repo:
        _fail("URL или путь репозитория пуст")

    if args.test_mode:
        _validate_test_repo(repo, package)
    else:
        _validate_url(repo)

    args.package = package
    args.version = version
    args.repo = repo
    args.filter = filt
    return args


def _validate_test_repo(path, package):
    """Проверяет путь к файлу тестового репозитория."""
    if not os.path.isfile(path):
        _fail(f"тестовый репозиторий не найден: {path}")
    if not package.isupper():
        _fail(
            "в test-mode имя пакета — "
            "заглавные латинские буквы"
        )


def _validate_url(repo):
    """Проверяет, что repo похож на URL репозитория."""
    lower = repo.lower()
    has_http = lower.startswith("http://")
    has_https = lower.startswith("https://")
    if not has_http and not has_https:
        _fail(
            "ожидался URL (http/https) "
            "или включите --test-mode"
        )


def print_config(args):
    """Выводит параметры в формате ключ-значение."""
    print("=== Параметры конфигурации ===")
    print(f"package={args.package}")
    print(f"repo={args.repo}")
    print(f"test_mode={args.test_mode}")
    print(f"version={args.version}")
    print(f"ascii_tree={args.ascii_tree}")
    print(f"filter={args.filter}")
    print("================================")


def load_config(argv=None):
    """Разбирает argv, валидирует и возвращает args."""
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_config(args)
    return args


def success_code():
    """Возвращает код успешного завершения."""
    return EXIT_OK
