"""
Модуль бинарного дерева поиска.
Реализация BST на основе узлов с основными операциями.
"""


class TreeNode:
    """Узел бинарного дерева поиска."""

    def __init__(self, value):
        """Инициализация узла с заданным значением."""
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Бинарное дерево поиска."""

    def __init__(self):
        """Инициализация пустого дерева."""
        self.root = None

    def insert(self, value):
        """
        Вставка элемента в BST.
        Сложность: в среднем O(log n), в худшем O(n).
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_iterative(value)

    def _insert_iterative(self, value):
        """Итеративная вставка для избежания переполнения стека."""
        current = self.root
        parent = None

        # Находим место для вставки
        while current is not None:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return  # Значение уже существует

        # Создаем новый узел
        new_node = TreeNode(value)

        # Вставляем в нужное место
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

    def search(self, value):
        """
        Поиск элемента в BST.
        Сложность: в среднем O(log n), в худшем O(n).
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """Рекурсивная вспомогательная функция для поиска."""
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value):
        """
        Удаление элемента из BST.
        Сложность: в среднем O(log n), в худшем O(n).
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        """Рекурсивная вспомогательная функция для удаления."""
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Найден узел для удаления
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Находим минимальный элемент в правом поддереве
                min_node = self._find_min_node(node.right)
                node.value = min_node.value
                node.right = self._delete_recursive(node.right, min_node.value)

        return node

    def _find_min_node(self, node):
        """Вспомогательная функция для поиска минимального узла."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_min(self, node=None):
        """
        Поиск минимального элемента в поддереве.
        Сложность: O(h), где h - высота дерева.
        """
        if node is None:
            if self.root is None:
                return None
            node = self.root

        min_node = self._find_min_node(node)
        return min_node

    def find_max(self, node=None):
        """
        Поиск максимального элемента в поддереве.
        Сложность: O(h), где h - высота дерева.
        """
        if node is None:
            if self.root is None:
                return None
            node = self.root

        current = node
        while current.right is not None:
            current = current.right
        return current

    def is_valid_bst(self):
        """
        Проверка, является ли дерево корректным BST.
        Сложность: O(n).
        """
        return self._is_valid_recursive(self.root, float('-inf'),
                                        float('inf'))

    def _is_valid_recursive(self, node, min_val, max_val):
        """Рекурсивная проверка корректности BST."""
        if node is None:
            return True

        if node.value <= min_val or node.value >= max_val:
            return False

        return (self._is_valid_recursive(node.left, min_val, node.value) and
                self._is_valid_recursive(node.right, node.value, max_val))

    def height(self, node=None):
        """
        Вычисление высоты дерева/поддерева.
        Сложность: O(n).
        """
        if node is None:
            if self.root is None:
                return 0
            node = self.root

        return self._height_recursive(node)

    def _height_recursive(self, node):
        """Рекурсивное вычисление высоты."""
        if node is None:
            return -1
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return max(left_height, right_height) + 1

    def size(self):
        """
        Количество элементов в дереве.
        Сложность: O(n).
        """
        return self._size_recursive(self.root)

    def _size_recursive(self, node):
        """Рекурсивный подсчет количества элементов."""
        if node is None:
            return 0
        return (self._size_recursive(node.left) +
                self._size_recursive(node.right) + 1)

    def to_list_inorder(self):
        """Возвращает список элементов в порядке in-order."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Рекурсивный in-order обход."""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def visualize(self, node=None, level=0, prefix="Root: "):
        """
        Текстовая визуализация дерева.
        """
        if node is None:
            node = self.root
            if node is None:
                print("Дерево пустое")
                return

        if level == 0:
            print(f"{prefix}{node.value}")

        indent = "    " * level
        if node.left is not None:
            print(f"{indent}    L: {node.left.value}")
            self.visualize(node.left, level + 1, "    ")
        if node.right is not None:
            print(f"{indent}    R: {node.right.value}")
            self.visualize(node.right, level + 1, "    ")