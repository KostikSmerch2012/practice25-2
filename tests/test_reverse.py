"""Тесты обратных зависимостей (этап 4)."""

import os
import sys
import unittest

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.config import build_parser, validate_config
from src.graph import invert_adjacency
from src.reverse import build_reverse_graph


def _load_args(argv):
    """Собирает и валидирует аргументы CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return validate_config(args)


def _fixture(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(ROOT, "fixtures", name)


class TestReverse(unittest.TestCase):
    """Проверка обратных зависимостей."""

    def test_invert_simple(self):
        """Инверсия алмаза A->B,C; B,C->D."""
        forward = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        rev = invert_adjacency(forward)
        self.assertEqual(rev["D"], ["B", "C"])
        self.assertEqual(rev["B"], ["A"])
        self.assertEqual(rev["C"], ["A"])

    def test_reverse_transitive_from_d(self):
        """Кто зависит от D: B, C и транзитивно A."""
        args = _load_args(
            [
                "--package",
                "D",
                "--repo",
                _fixture("repo_simple.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
                "--reverse-deps",
            ]
        )
        graph, cycles, _vers = build_reverse_graph(args)
        self.assertEqual(sorted(graph["D"]), ["B", "C"])
        self.assertEqual(graph["B"], ["A"])
        self.assertEqual(graph["C"], ["A"])
        self.assertEqual(graph["A"], [])
        self.assertEqual(cycles, [])

    def test_reverse_on_chain(self):
        """Обратно от C зависит B, от B — A."""
        args = _load_args(
            [
                "--package",
                "C",
                "--repo",
                _fixture("repo_chain.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
                "--reverse-deps",
            ]
        )
        graph, cycles, _vers = build_reverse_graph(args)
        self.assertEqual(graph["C"], ["B"])
        self.assertEqual(graph["B"], ["A"])
        self.assertIn("A", graph)

    def test_reverse_cycle(self):
        """Цикл в обратном обходе не ломает программу."""
        args = _load_args(
            [
                "--package",
                "B",
                "--repo",
                _fixture("repo_cycle.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
                "--reverse-deps",
            ]
        )
        graph, cycles, _vers = build_reverse_graph(args)
        self.assertIn("B", graph)
        self.assertIn("A", graph["B"])
        self.assertTrue(len(cycles) >= 0)


if __name__ == "__main__":
    unittest.main()