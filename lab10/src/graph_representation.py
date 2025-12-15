"""
graph_representation.py
Реализация двух представлений графов:
1. Матрица смежности (Adjacency Matrix)
2. Список смежности (Adjacency List)
"""

class AdjacencyMatrix:
    """
    Представление графа в виде матрицы смежности.
    
    Свойства:
    - Память: O(V²)
    - Проверка наличия ребра: O(1)
    - Получение соседей вершины: O(V)
    """
    
    def __init__(self, vertices=0, directed=False):
        """
        Инициализация матрицы смежности.
        
        Args:
            vertices: количество вершин (по умолчанию 0)
            directed: ориентированный граф (True) или неориентированный (False)
        """
        self.directed = directed
        self.vertices = vertices
        self.matrix = [[0] * vertices for _ in range(vertices)]
    
    def add_edge(self, u, v, weight=1):
        """
        Добавление ребра между вершинами u и v.
        
        Сложность: O(1)
        
        Args:
            u: начальная вершина
            v: конечная вершина
            weight: вес ребра (по умолчанию 1)
        """
        if 0 <= u < self.vertices and 0 <= v < self.vertices:
            self.matrix[u][v] = weight
            if not self.directed:
                self.matrix[v][u] = weight
    
    def remove_edge(self, u, v):
        """
        Удаление ребра между вершинами u и v.
        
        Сложность: O(1)
        """
        if 0 <= u < self.vertices and 0 <= v < self.vertices:
            self.matrix[u][v] = 0
            if not self.directed:
                self.matrix[v][u] = 0
    
    def has_edge(self, u, v):
        """
        Проверка наличия ребра между вершинами u и v.
        
        Сложность: O(1)
        
        Returns:
            True если ребро существует, иначе False
        """
        if 0 <= u < self.vertices and 0 <= v < self.vertices:
            return self.matrix[u][v] != 0
        return False
    
    def get_neighbors(self, vertex):
        """
        Получение всех соседей вершины.
        
        Сложность: O(V)
        
        Returns:
            Список пар (сосед, вес)
        """
        neighbors = []
        if 0 <= vertex < self.vertices:
            for v in range(self.vertices):
                if self.matrix[vertex][v] != 0:
                    neighbors.append((v, self.matrix[vertex][v]))
        return neighbors
    
    def print_matrix(self):
        """Вывод матрицы смежности."""
        print("Матрица смежности:")
        for row in self.matrix:
            print(" ".join(str(val) for val in row))
    
    def get_edge_count(self):
        """Подсчет количества ребер."""
        count = 0
        for i in range(self.vertices):
            for j in range(self.vertices):
                if self.matrix[i][j] != 0:
                    count += 1
        if not self.directed:
            count //= 2
        return count


class AdjacencyList:
    """
    Представление графа в виде списка смежности.
    
    Свойства:
    - Память: O(V + E)
    - Проверка наличия ребра: O(deg(V))
    - Получение соседей вершины: O(1) в среднем
    """
    
    def __init__(self, vertices=0, directed=False):
        """
        Инициализация списка смежности.
        
        Args:
            vertices: количество вершин
            directed: ориентированный граф (True) или неориентированный (False)
        """
        self.directed = directed
        self.vertices = vertices
        self.adj_list = [[] for _ in range(vertices)]
    
    def add_edge(self, u, v, weight=1):
        """
        Добавление ребра между вершинами u и v.
        
        Сложность: O(1) в среднем
        
        Args:
            u: начальная вершина
            v: конечная вершина
            weight: вес ребра (по умолчанию 1)
        """
        if 0 <= u < self.vertices and 0 <= v < self.vertices:
            self.adj_list[u].append((v, weight))
            if not self.directed:
                self.adj_list[v].append((u, weight))
    
    def remove_edge(self, u, v):
        """
        Удаление ребра между вершинами u и v.
        
        Сложность: O(deg(u) + deg(v))
        """
        if 0 <= u < self.vertices:
            self.adj_list[u] = [edge for edge in self.adj_list[u] if edge[0] != v]
        
        if not self.directed and 0 <= v < self.vertices:
            self.adj_list[v] = [edge for edge in self.adj_list[v] if edge[0] != u]
    
    def has_edge(self, u, v):
        """
        Проверка наличия ребра между вершинами u и v.
        
        Сложность: O(deg(u))
        
        Returns:
            True если ребро существует, иначе False
        """
        if 0 <= u < self.vertices:
            for neighbor, _ in self.adj_list[u]:
                if neighbor == v:
                    return True
        return False
    
    def get_neighbors(self, vertex):
        """
        Получение всех соседей вершины.
        
        Сложность: O(1) для доступа к списку
        
        Returns:
            Список пар (сосед, вес)
        """
        if 0 <= vertex < self.vertices:
            return self.adj_list[vertex]
        return []
    
    def print_list(self):
        """Вывод списка смежности."""
        print("Список смежности:")
        for i in range(self.vertices):
            neighbors = self.adj_list[i]
            print(f"{i}: {neighbors}")
    
    def get_edge_count(self):
        """Подсчет количества ребер."""
        count = 0
        for edges in self.adj_list:
            count += len(edges)
        if not self.directed:
            count //= 2
        return count


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("ПРЕДСТАВЛЕНИЯ ГРАФОВ")
    print("=" * 60)
    
    # Создание графа с 5 вершинами (неориентированный)
    print("\n1. Матрица смежности:")
    g1 = AdjacencyMatrix(5, directed=False)
    
    # Добавление ребер
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 3)
    g1.add_edge(2, 3)
    g1.add_edge(3, 4)
    
    g1.print_matrix()
    print(f"Количество ребер: {g1.get_edge_count()}")
    print(f"Соседи вершины 3: {g1.get_neighbors(3)}")
    print(f"Есть ли ребро 1-3? {g1.has_edge(1, 3)}")
    print(f"Есть ли ребро 0-4? {g1.has_edge(0, 4)}")
    
    print("\n2. Список смежности:")
    g2 = AdjacencyList(5, directed=False)
    
    # Добавление ребер (те же самые)
    g2.add_edge(0, 1)
    g2.add_edge(0, 2)
    g2.add_edge(1, 3)
    g2.add_edge(2, 3)
    g2.add_edge(3, 4)
    
    g2.print_list()
    print(f"Количество ребер: {g2.get_edge_count()}")
    print(f"Соседи вершины 3: {g2.get_neighbors(3)}")
    print(f"Есть ли ребро 1-3? {g2.has_edge(1, 3)}")
    print(f"Есть ли ребро 0-4? {g2.has_edge(0, 4)}")