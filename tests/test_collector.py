"""Тесты сборщика прямых зависимостей."""

import os
import sys
import unittest
from unittest import mock

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.collector import (
    build_nuspec_url,
    collect_direct_deps,
    print_deps,
)
from src.config import build_parser, validate_config


def _load_args(argv):
    """Собирает и валидирует аргументы CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return validate_config(args)


class TestCollector(unittest.TestCase):
    """Проверка URL, test-mode и вывода."""

    def test_build_nuspec_url(self):
        """URL строится в нижнем регистре."""
        url = build_nuspec_url(
            "https://api.nuget.org/v3-flatcontainer/",
            "Serilog.Sinks.File",
            "5.0.0",
        )
        expected = (
            "https://api.nuget.org/v3-flatcontainer/"
            "serilog.sinks.file/5.0.0/"
            "serilog.sinks.file.nuspec"
        )
        self.assertEqual(url, expected)

    def test_test_mode_direct_deps(self):
        """Прямые зависимости из тестового файла."""
        path = os.path.join(
            ROOT,
            "fixtures",
            "repo_simple.txt",
        )
        args = _load_args(
            [
                "--package",
                "A",
                "--repo",
                path,
                "--version",
                "1.0.0",
                "--test-mode",
            ]
        )
        deps = collect_direct_deps(args)
        self.assertEqual(
            deps,
            [("B", ""), ("C", "")],
        )

    def test_test_mode_leaf(self):
        """Лист без зависимостей даёт пустой список."""
        path = os.path.join(
            ROOT,
            "fixtures",
            "repo_simple.txt",
        )
        args = _load_args(
            [
                "--package",
                "D",
                "--repo",
                path,
                "--version",
                "1.0.0",
                "--test-mode",
            ]
        )
        deps = collect_direct_deps(args)
        self.assertEqual(deps, [])

    def test_nuget_mode_uses_fetch(self):
        """В обычном режиме вызывается загрузка .nuspec."""
        fixture = os.path.join(
            ROOT,
            "fixtures",
            "sample.nuspec",
        )
        with open(fixture, encoding="utf-8") as handle:
            text = handle.read()
        args = _load_args(
            [
                "--package",
                "Serilog.Sinks.File",
                "--repo",
                "https://api.nuget.org/v3-flatcontainer",
                "--version",
                "5.0.0",
            ]
        )
        with mock.patch(
            "src.collector.fetch_text",
            return_value=text,
        ) as mocked:
            deps = collect_direct_deps(args)
        mocked.assert_called_once()
        ids = [item[0] for item in deps]
        self.assertEqual(ids, ["Serilog", "System.IO"])

    def test_print_deps(self):
        """Печать списка зависимостей не падает."""
        with mock.patch("builtins.print") as mocked:
            print_deps([("Serilog", "2.10.0")])
            print_deps([])
            self.assertTrue(mocked.called)


if __name__ == "__main__":
    unittest.main()
