"""Тесты разбора .nuspec."""

import os
import sys
import unittest

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.nuspec import parse_nuspec_deps


class TestNuspec(unittest.TestCase):
    """Проверка извлечения зависимостей из XML."""

    def test_sample_dedupes_groups(self):
        """Дубли из разных group схлопываются."""
        path = os.path.join(
            ROOT,
            "fixtures",
            "sample.nuspec",
        )
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        deps = parse_nuspec_deps(text)
        ids = [item[0] for item in deps]
        self.assertEqual(ids, ["Serilog", "System.IO"])
        self.assertEqual(deps[0][1], "2.10.0")
        self.assertEqual(deps[1][1], "4.3.0")

    def test_empty_dependencies(self):
        """Пакет без зависимостей даёт пустой список."""
        path = os.path.join(
            ROOT,
            "fixtures",
            "empty_deps.nuspec",
        )
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        deps = parse_nuspec_deps(text)
        self.assertEqual(deps, [])

    def test_flat_dependencies(self):
        """Поддержка dependency без group."""
        text = (
            '<?xml version="1.0"?>'
            "<package><metadata><dependencies>"
            '<dependency id="Foo" version="1.2.3"/>'
            "</dependencies></metadata></package>"
        )
        deps = parse_nuspec_deps(text)
        self.assertEqual(deps, [("Foo", "1.2.3")])

    def test_empty_text_fails(self):
        """Пустой текст .nuspec — ошибка."""
        with self.assertRaises(ValueError):
            parse_nuspec_deps("   ")


if __name__ == "__main__":
    unittest.main()
