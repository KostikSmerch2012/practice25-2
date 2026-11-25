"""Построение графа зависимостей итеративным DFS."""

from src.constants import EMPTY_COUNT


def is_filtered(name, filt):
    """True, если пакет нужно исключить по --filter."""
    if filt is None:
        return False
    if len(filt) == EMPTY_COUNT:
        return False
    return filt.lower() in name.lower()


def filter_names(names, filt):
    """Оставляет пакеты, не попадающие под фильтр."""
    result = []
    for name in names:
        if is_filtered(name, filt):
            continue
        result.append(name)
    return result


def build_graph_dfs(root, get_neighbors, filt=""):
    """Строит граф DFS без рекурсии; возвращает (граф, циклы)."""
    graph = {}
    cycles = []
    if is_filtered(root, filt):
        return graph, cycles

    root_deps = filter_names(get_neighbors(root), filt)
    graph[root] = list(root_deps)
    frames = [[root, 0, root_deps]]
    on_path = {root}

    while len(frames) > EMPTY_COUNT:
        _dfs_step(frames, on_path, graph, cycles, get_neighbors, filt)
    return graph, cycles


def _dfs_step(frames, on_path, graph, cycles, get_neighbors, filt):
    """Один шаг итеративного DFS по стеку кадров."""
    node, idx, neighs = frames[-1]
    if idx >= len(neighs):
        frames.pop()
        on_path.discard(node)
        return

    frames[-1][1] = idx + 1
    child = neighs[idx]
    if child in on_path:
        cycles.append((node, child))
        return
    if child in graph:
        return

    child_deps = filter_names(get_neighbors(child), filt)
    graph[child] = list(child_deps)
    on_path.add(child)
    frames.append([child, 0, child_deps])


def invert_adjacency(forward):
    """Строит обратный граф: кто зависит от пакета."""
    reverse = {}
    for src, dsts in forward.items():
        _ensure_adj_node(reverse, src)
        for dst in dsts:
            _ensure_adj_node(reverse, dst)
            if src not in reverse[dst]:
                reverse[dst].append(src)
    return reverse


def _ensure_adj_node(adj, name):
    """Добавляет пустой список соседей для узла."""
    if name not in adj:
        adj[name] = []


def print_reverse_graph(graph, cycles):
    """Печатает обратные зависимости и циклы."""
    print("=== Обратные зависимости ===")
    if len(graph) == EMPTY_COUNT:
        print("(пусто)")
    else:
        for node in graph:
            _print_edges(node, graph[node])
    print("===========================")
    _print_cycles(cycles)


def print_graph(graph, cycles):
    """Печатает граф зависимостей и найденные циклы."""
    print("=== Граф зависимостей ===")
    if len(graph) == EMPTY_COUNT:
        print("(пусто)")
    else:
        for node in graph:
            _print_edges(node, graph[node])
    print("=========================")
    _print_cycles(cycles)


def _print_edges(node, deps):
    """Печатает рёбра одного узла."""
    if len(deps) == EMPTY_COUNT:
        print(f"{node} ->")
        return
    joined = ", ".join(deps)
    print(f"{node} -> {joined}")


def _print_cycles(cycles):
    """Печатает информацию о циклических зависимостях."""
    print("=== Циклы ===")
    if len(cycles) == EMPTY_COUNT:
        print("(нет)")
    else:
        for src, dst in cycles:
            print(f"{src} -> {dst}")
    print("=============")
