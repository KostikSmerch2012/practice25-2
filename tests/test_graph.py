"""Тесты итеративного DFS и фильтрации."""

import os
import sys
import unittest

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.builder import build_dependency_graph
from src.config import build_parser, validate_config
from src.graph import build_graph_dfs, filter_names


def _load_args(argv):
    """Собирает и валидирует аргументы CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return validate_config(args)


def _fixture(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(ROOT, "fixtures", name)


class TestGraph(unittest.TestCase):
    """Проверка графа, циклов и --filter."""

    def test_simple_transitive(self):
        """Алмаз A->B,C->D собирается целиком."""
        args = _load_args(
            [
                "--package",
                "A",
                "--repo",
                _fixture("repo_simple.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
            ]
        )
        graph, cycles = build_dependency_graph(args)
        self.assertEqual(graph["A"], ["B", "C"])
        self.assertEqual(graph["B"], ["D"])
        self.assertEqual(graph["C"], ["D"])
        self.assertEqual(graph["D"], [])
        self.assertEqual(cycles, [])

    def test_chain_transitive(self):
        """Цепочка A-B-C-D обходится транзитивно."""
        args = _load_args(
            [
                "--package",
                "A",
                "--repo",
                _fixture("repo_chain.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
            ]
        )
        graph, cycles = build_dependency_graph(args)
        self.assertEqual(
            set(graph.keys()),
            {"A", "B", "C", "D"},
        )
        self.assertEqual(cycles, [])

    def test_cycle_detected(self):
        """Цикл A->B->C->A не зацикливает обход."""
        args = _load_args(
            [
                "--package",
                "A",
                "--repo",
                _fixture("repo_cycle.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
            ]
        )
        graph, cycles = build_dependency_graph(args)
        self.assertIn("A", graph)
        self.assertIn("B", graph)
        self.assertIn("C", graph)
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0], ("C", "A"))

    def test_filter_skips_packages(self):
        """Пакеты с подстрокой фильтра не анализируются."""
        args = _load_args(
            [
                "--package",
                "A",
                "--repo",
                _fixture("repo_simple.txt"),
                "--version",
                "1.0.0",
                "--test-mode",
                "--filter",
                "B",
            ]
        )
        graph, cycles = build_dependency_graph(args)
        self.assertEqual(graph["A"], ["C"])
        self.assertNotIn("B", graph)
        self.assertIn("C", graph)
        self.assertIn("D", graph)
        self.assertEqual(cycles, [])

    def test_filter_names_helper(self):
        """Вспомогательная фильтрация имён."""
        names = ["Serilog", "System.IO", "Newtonsoft"]
        result = filter_names(names, "System")
        self.assertEqual(result, ["Serilog", "Newtonsoft"])

    def test_dfs_with_dict_provider(self):
        """DFS работает с простым словарём соседей."""
        data = {"A": ["B"], "B": ["A"]}

        def get_neighbors(name):
            return list(data.get(name, []))

        graph, cycles = build_graph_dfs(
            "A",
            get_neighbors,
            "",
        )
        self.assertEqual(graph["A"], ["B"])
        self.assertEqual(graph["B"], ["A"])
        self.assertEqual(cycles, [("B", "A")])


if __name__ == "__main__":
    unittest.main()
