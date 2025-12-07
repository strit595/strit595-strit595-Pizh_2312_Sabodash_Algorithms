"""
Модуль обходов дерева.
Реализация различных методов обхода BST.
"""


class TreeTraversal:
    """Класс для реализации обходов дерева."""

    @staticmethod
    def inorder_recursive(node, result=None):
        """
        Рекурсивный in-order обход (левый-корень-правый).
        Сложность: O(n).
        """
        if result is None:
            result = []

        if node is not None:
            TreeTraversal.inorder_recursive(node.left, result)
            result.append(node.value)
            TreeTraversal.inorder_recursive(node.right, result)

        return result

    @staticmethod
    def preorder_recursive(node, result=None):
        """
        Рекурсивный pre-order обход (корень-левый-правый).
        Сложность: O(n).
        """
        if result is None:
            result = []

        if node is not None:
            result.append(node.value)
            TreeTraversal.preorder_recursive(node.left, result)
            TreeTraversal.preorder_recursive(node.right, result)

        return result

    @staticmethod
    def postorder_recursive(node, result=None):
        """
        Рекурсивный post-order обход (левый-правый-корень).
        Сложность: O(n).
        """
        if result is None:
            result = []

        if node is not None:
            TreeTraversal.postorder_recursive(node.left, result)
            TreeTraversal.postorder_recursive(node.right, result)
            result.append(node.value)

        return result

    @staticmethod
    def inorder_iterative(root):
        """
        Итеративный in-order обход с использованием стека.
        Сложность: O(n).
        """
        result = []
        stack = []
        current = root

        while current is not None or stack:
            # Добираемся до самого левого узла
            while current is not None:
                stack.append(current)
                current = current.left

            # Извлекаем из стека и обрабатываем
            current = stack.pop()
            result.append(current.value)

            # Переходим к правому поддереву
            current = current.right

        return result

    @staticmethod
    def level_order_traversal(root):
        """
        Обход дерева в ширину (BFS).
        Сложность: O(n).
        """
        if root is None:
            return []

        result = []
        queue = [root]

        while queue:
            node = queue.pop(0)
            result.append(node.value)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        return result

    @staticmethod
    def print_traversals(root, tree_name=""):
        """Печать всех обходов дерева."""
        print(f"\n=== Обходы дерева {tree_name} ===")
        print(f"In-order (рекурсивный): "
              f"{TreeTraversal.inorder_recursive(root)}")
        print(f"In-order (итеративный): "
              f"{TreeTraversal.inorder_iterative(root)}")
        print(f"Pre-order: {TreeTraversal.preorder_recursive(root)}")
        print(f"Post-order: {TreeTraversal.postorder_recursive(root)}")
        level_order = TreeTraversal.level_order_traversal(root)
        print(f"Level-order (BFS): {level_order}")