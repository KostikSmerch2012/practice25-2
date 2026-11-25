"""SVG-изображение графа зависимостей (stdlib)."""

import os
import xml.etree.ElementTree as ET

from src.constants import (
    MMD_FILE,
    NODE_DX,
    NODE_DY,
    NODE_R,
    OUTPUT_DIR,
    SVG_FILE,
    SVG_HEIGHT,
    SVG_WIDTH,
)


def save_mermaid_file(text):
    """Сохраняет .mmd в каталог output."""
    path = os.path.join(OUTPUT_DIR, MMD_FILE)
    _ensure_dir()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def save_svg_graph(root, graph):
    """Строит SVG и сохраняет в output/graph.svg."""
    _ensure_dir()
    path = os.path.join(OUTPUT_DIR, SVG_FILE)
    coords = _layout_positions(root, graph)
    svg = _build_svg_doc(coords, graph)
    ET.ElementTree(svg).write(
        path,
        encoding="utf-8",
        xml_declaration=True,
    )
    return path


def print_image_message(path):
    """Сообщает путь к файлу изображения."""
    print("=== Изображение графа ===")
    print(path)
    print("Откройте файл в браузере или просмотрщике.")
    print("==========================")


def _ensure_dir():
    """Создаёт каталог output при отсутствии."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _layout_positions(root, graph):
    """Раскладка узлов по уровням BFS."""
    levels = {root: 0}
    order = [root]
    idx = 0
    while idx < len(order):
        node = order[idx]
        idx += 1
        depth = levels[node]
        for child in graph.get(node, []):
            if child in levels:
                continue
            levels[child] = depth + 1
            order.append(child)
    per_level = {}
    for name, depth in levels.items():
        per_level.setdefault(depth, []).append(name)
    coords = {}
    for depth, names in per_level.items():
        for col, name in enumerate(names):
            x = 60 + col * NODE_DX
            y = 40 + depth * NODE_DY
            coords[name] = (x, y)
    return coords


def _build_svg_doc(coords, graph):
    """Собирает корневой элемент SVG."""
    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    svg = ET.Element("svg", xmlns=ns)
    svg.set("width", str(SVG_WIDTH))
    svg.set("height", str(SVG_HEIGHT))
    _add_edges(svg, ns, coords, graph)
    _add_nodes(svg, ns, coords)
    return svg


def _add_edges(svg, ns, coords, graph):
    """Рисует рёбра между узлами."""
    for src, dsts in graph.items():
        if src not in coords:
            continue
        x1, y1 = coords[src]
        for dst in dsts:
            if dst not in coords:
                continue
            x2, y2 = coords[dst]
            ET.SubElement(
                svg,
                "line",
                x1=str(x1),
                y1=str(y1 + NODE_R),
                x2=str(x2),
                y2=str(y2 - NODE_R),
                stroke="#333",
            )


def _add_nodes(svg, ns, coords):
    """Рисует узлы и подписи."""
    for name, (x, y) in coords.items():
        ET.SubElement(
            svg,
            "circle",
            cx=str(x),
            cy=str(y),
            r=str(NODE_R),
            fill="#eef",
            stroke="#333",
        )
        label = ET.SubElement(svg, "text", x=str(x - NODE_R), y=str(y + 4))
        label.text = name