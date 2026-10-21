"""Тесты разбора и валидации конфигурации."""

import os
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.config import (  # noqa: E402
    build_parser,
    print_config,
    validate_config,
)


class TestConfig(unittest.TestCase):
    """Проверка параметров CLI этапа 1."""

    def test_parser_defaults(self):
        """Флаги по умолчанию выключены."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--package",
                "A",
                "--repo",
                "https://example.com",
                "--version",
                "1.0.0",
            ]
        )
        self.assertFalse(args.test_mode)
        self.assertFalse(args.ascii_tree)
        self.assertEqual(args.filter, "")

    def test_missing_package_exits(self):
        """Ошибка при отсутствии --package."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--repo",
                "https://example.com",
                "--version",
                "1.0.0",
            ]
        )
        with self.assertRaises(SystemExit):
            validate_config(args)

    def test_missing_repo_exits(self):
        """Ошибка при отсутствии --repo."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--package",
                "Serilog",
                "--version",
                "1.0.0",
            ]
        )
        with self.assertRaises(SystemExit):
            validate_config(args)

    def test_missing_version_exits(self):
        """Ошибка при отсутствии --version."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--package",
                "Serilog",
                "--repo",
                "https://example.com",
            ]
        )
        with self.assertRaises(SystemExit):
            validate_config(args)

    def test_invalid_url_exits(self):
        """Ошибка при пути без --test-mode."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--package",
                "Serilog",
                "--repo",
                "not-a-url",
                "--version",
                "1.0.0",
            ]
        )
        with self.assertRaises(SystemExit):
            validate_config(args)

    def test_test_mode_requires_file(self):
        """Ошибка, если тестовый файл не существует."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--package",
                "A",
                "--repo",
                "/no/such/file.txt",
                "--version",
                "1.0.0",
                "--test-mode",
            ]
        )
        with self.assertRaises(SystemExit):
            validate_config(args)

    def test_test_mode_ok(self):
        """Успешная валидация test-mode."""
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
        ) as handle:
            handle.write("A: B\nB:\n")
            path = handle.name
        try:
            parser = build_parser()
            args = parser.parse_args(
                [
                    "--package",
                    "A",
                    "--repo",
                    path,
                    "--version",
                    "1.0.0",
                    "--test-mode",
                    "--ascii-tree",
                    "--filter",
                    "XX",
                ]
            )
            validate_config(args)
            self.assertEqual(args.package, "A")
            self.assertTrue(args.ascii_tree)
            self.assertEqual(args.filter, "XX")
        finally:
            os.unlink(path)

    def test_print_config(self):
        """Печать ключ-значение не падает."""
        parser = build_parser()
        args = parser.parse_args(
            [
                "--package",
                "Serilog",
                "--repo",
                "https://api.nuget.org/v3-flatcontainer",
                "--version",
                "2.10.0",
            ]
        )
        validate_config(args)
        with mock.patch("builtins.print") as mocked:
            print_config(args)
            self.assertTrue(mocked.called)


if __name__ == "__main__":
    unittest.main()
