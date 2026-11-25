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
        """Mermaid содержит узлы и рёбра."""
        graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
        text = build_mermaid(graph)
        self.assertIn("flowchart TD", text)
        self.assertIn("A --> B", text)
        self.assertIn("A --> C", text)

    def test_save_svg_and_mmd(self):
        """SVG и MMD сохраняются на диск."""
        graph = {"A": ["B"], "B": []}
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch(
                "src.svg_out.OUTPUT_DIR",
                tmp,
            ):
                save_mermaid_file("flowchart TD\n  A --> B")
                path = save_svg_graph("A", graph)
                self.assertTrue(os.path.isfile(path))
                mmd = os.path.join(tmp, MMD_FILE)
                self.assertTrue(os.path.isfile(mmd))

    def test_ascii_tree_print(self):
        """ASCII-дерево печатается без ошибок."""
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        with mock.patch("builtins.print") as mocked:
            print_ascii_tree("A", graph)
            self.assertTrue(mocked.called)


if __name__ == "__main__":
    unittest.main()