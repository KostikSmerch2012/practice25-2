"""Тесты разбора версий NuGet."""

import os
import sys
import unittest

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.version_spec import resolve_version


class TestVersionSpec(unittest.TestCase):
    """Проверка извлечения конкретной версии."""

    def test_exact_version(self):
        """Обычная версия без диапазона."""
        self.assertEqual(resolve_version("2.10.0"), "2.10.0")

    def test_range_lower_bound(self):
        """Из диапазона берётся нижняя граница."""
        self.assertEqual(
            resolve_version("[2.10.0, )"),
            "2.10.0",
        )

    def test_empty(self):
        """Пустая строка даёт пустой результат."""
        self.assertEqual(resolve_version(""), "")
        self.assertEqual(resolve_version(None), "")


if __name__ == "__main__":
    unittest.main()
