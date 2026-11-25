"""Тесты Mermaid, SVG и ASCII-дерева."""

import os
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, ROOT)

from src.ascii_tree import print_ascii_tree
from src.constants import MMD_FILE, OUTPUT_DIR, SVG_FILE
from src.mermaid_out import build_mermaid, mermaid_node_id
from src.svg_out import save_mermaid_file, save_svg_graph


class TestVisualize(unittest.TestCase):
    """Проверка визуализации этапа 5."""

    def test_mermaid_node_id(self):
        """Точки в имени заменяются на подчёркивания."""
        self.assertEqual(
            mermaid_node_id("Serilog.Sinks.File"),
            "Serilog_Sinks_File",
        )

    def test_build_mermaid_simple(self):
        """Mermaid содержит узлы, версии и рёбра."""
        graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
        vers = {"A": "1.0.0", "B": "2.0.0", "C": "1.1.0", "D": "3.0.0"}
        text = build_mermaid(graph, vers)
        self.assertIn("flowchart TD", text)
        self.assertIn('A["A 1.0.0"]', text)
        self.assertIn("A --> B", text)
        self.assertIn("A --> C", text)

    def test_save_svg_and_mmd(self):
        """SVG и MMD сохраняются, в SVG есть версия."""
        graph = {"A": ["B"], "B": []}
        vers = {"A": "1.0.0", "B": "2.0.0"}
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch(
                "src.svg_out.OUTPUT_DIR",
                tmp,
            ):
                save_mermaid_file("flowchart TD\n  A --> B")
                path = save_svg_graph("A", graph, vers)
                self.assertTrue(os.path.isfile(path))
                with open(path, encoding="utf-8") as handle:
                    body = handle.read()
                self.assertIn("A 1.0.0", body)
                mmd = os.path.join(tmp, MMD_FILE)
                self.assertTrue(os.path.isfile(mmd))

    def test_ascii_tree_print(self):
        """ASCII-дерево печатается с версиями."""
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        vers = {"A": "1.0.0", "B": "2.0.0"}
        with mock.patch("builtins.print") as mocked:
            print_ascii_tree("A", graph, vers)
            self.assertTrue(mocked.called)


if __name__ == "__main__":
    unittest.main()