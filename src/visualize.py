"""Визуализация графа: Mermaid, SVG, ASCII-дерево."""

from src.ascii_tree import print_ascii_tree
from src.mermaid_out import build_mermaid, print_mermaid
from src.svg_out import (
    print_image_message,
    save_mermaid_file,
    save_svg_graph,
)


def render_visualization(args, graph):
    """Печатает и сохраняет все виды визуализации."""
    print_mermaid(graph)
    text = build_mermaid(graph)
    mmd_path = save_mermaid_file(text)
    root = _visual_root(args)
    svg_path = save_svg_graph(root, graph)
    print_image_message(svg_path)
    print(f"Mermaid-файл: {mmd_path}")
    if args.ascii_tree:
        print_ascii_tree(root, graph)


def _visual_root(args):
    """Корень для раскладки и дерева."""
    if args.test_mode:
        return args.package.strip().upper()
    return args.package