"""
graph_traversal.py
Реализация алгоритмов обхода графов:
1. Поиск в ширину (BFS)
2. Поиск в глубину (DFS) - рекурсивный и итеративный
"""

from collections import deque
from graph_representation import AdjacencyList


def bfs(graph, start_vertex):
    """
    Поиск в ширину (BFS).
    
    Сложность: O(V + E)
    
    Args:
        graph: граф (объект AdjacencyList)
        start_vertex: начальная вершина
    
    Returns:
        visited: список посещенных вершин в порядке обхода
        distances: расстояния от start_vertex до каждой вершины
        parents: родительские вершины для восстановления пути
    """
    visited = []
    distances = [-1] * graph.vertices  # -1 означает "не посещена"
    parents = [-1] * graph.vertices
    
    queue = deque([start_vertex])
    distances[start_vertex] = 0
    
    while queue:
        current = queue.popleft()
        visited.append(current)
        
        for neighbor, _ in graph.get_neighbors(current):
            if distances[neighbor] == -1:  # Не посещена
                distances[neighbor] = distances[current] + 1
                parents[neighbor] = current
                queue.append(neighbor)
    
    return visited, distances, parents


def bfs_shortest_path(graph, start, end):
    """
    Поиск кратчайшего пути в невзвешенном графе с помощью BFS.
    
    Сложность: O(V + E)
    
    Args:
        graph: граф
        start: начальная вершина
        end: конечная вершина
    
    Returns:
        path: список вершин кратчайшего пути
        distance: длина пути
    """
    if start == end:
        return [start], 0
    
    _, distances, parents = bfs(graph, start)
    
    if distances[end] == -1:
        return [], -1  # Пути нет
    
    # Восстановление пути
    path = []
    current = end
    while current != -1:
        path.append(current)
        current = parents[current]
    path.reverse()
    
    return path, distances[end]


def dfs_recursive(graph, start_vertex):
    """
    Поиск в глубину (DFS) - рекурсивная реализация.
    
    Сложность: O(V + E)
    
    Args:
        graph: граф
        start_vertex: начальная вершина
    
    Returns:
        visited: список посещенных вершин в порядке обхода
    """
    visited = []
    
    def dfs_util(vertex):
        visited.append(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs_util(neighbor)
    
    dfs_util(start_vertex)
    return visited


def dfs_iterative(graph, start_vertex):
    """
    Поиск в глубину (DFS) - итеративная реализация.
    
    Сложность: O(V + E)
    
    Args:
        graph: граф
        start_vertex: начальная вершина
    
    Returns:
        visited: список посещенных вершин в порядке обхода
    """
    visited = []
    stack = [start_vertex]
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            # Добавляем соседей в обратном порядке для соответствия рекурсивной версии
            neighbors = graph.get_neighbors(vertex)
            for neighbor, _ in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited


def dfs_with_timestamps(graph, start_vertex):
    """
    DFS с метками времени (время входа и выхода).
    
    Сложность: O(V + E)
    
    Args:
        graph: граф
        start_vertex: начальная вершина
    
    Returns:
        visited: посещенные вершины
        discovery_time: время обнаружения каждой вершины
        finish_time: время завершения обработки каждой вершины
    """
    visited = []
    discovery_time = [-1] * graph.vertices
    finish_time = [-1] * graph.vertices
    time = [0]  # Используем список для mutable времени
    
    def dfs_util(vertex):
        visited.append(vertex)
        discovery_time[vertex] = time[0]
        time[0] += 1
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs_util(neighbor)
        
        finish_time[vertex] = time[0]
        time[0] += 1
    
    dfs_util(start_vertex)
    return visited, discovery_time, finish_time


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("АЛГОРИТМЫ ОБХОДА ГРАФОВ")
    print("=" * 60)
    
    # Создание тестового графа
    print("\nСоздание графа (7 вершин):")
    graph = AdjacencyList(7, directed=False)
    
    # Добавление ребер
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for u, v in edges:
        graph.add_edge(u, v)
    
    graph.print_list()
    
    print("\n1. Поиск в ширину (BFS):")
    start = 0
    visited_bfs, distances, parents = bfs(graph, start)
    print(f"Обход BFS из вершины {start}: {visited_bfs}")
    print(f"Расстояния: {distances}")
    print(f"Родители: {parents}")
    
    # Поиск кратчайшего пути
    print(f"\nКратчайший путь от {start} до 6:")
    path, dist = bfs_shortest_path(graph, start, 6)
    print(f"Путь: {path}, Длина: {dist}")
    
    print("\n2. Поиск в глубину (DFS) - рекурсивный:")
    visited_dfs_rec = dfs_recursive(graph, start)
    print(f"Обход DFS рекурсивный: {visited_dfs_rec}")
    
    print("\n3. Поиск в глубину (DFS) - итеративный:")
    visited_dfs_iter = dfs_iterative(graph, start)
    print(f"Обход DFS итеративный: {visited_dfs_iter}")
    
    print("\n4. DFS с метками времени:")
    visited_time, discovery, finish = dfs_with_timestamps(graph, start)
    print(f"Вершины: {list(range(graph.vertices))}")
    print(f"Время входа: {discovery}")
    print(f"Время выхода: {finish}")