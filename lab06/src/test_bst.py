"""
Комплексные модульные тесты для верификации корректности работы бинарного дерева поиска.
"""

import unittest
from typing import List, Optional, Any


# =================== ВСТРОЕННЫЕ РЕАЛИЗАЦИИ ===================

class BinaryTreeNode:
    """Узел бинарного дерева поиска."""
    
    def __init__(self, node_value: Any):
        self.node_value = node_value
        self.left_child = None
        self.right_child = None


class BinarySearchTree:
    """Реализация структуры бинарного дерева поиска."""
    
    def __init__(self):
        self.root_element = None
    
    def add_element(self, value: Any) -> None:
        """Добавление нового элемента в дерево."""
        if self.root_element is None:
            self.root_element = BinaryTreeNode(value)
        else:
            self._add_element_iteratively(value)
    
    def _add_element_iteratively(self, value: Any) -> None:
        """Итеративная реализация добавления элемента."""
        current = self.root_element
        parent = None
        
        while current is not None:
            parent = current
            if value < current.node_value:
                current = current.left_child
            elif value > current.node_value:
                current = current.right_child
            else:
                return  # Элемент уже существует
        
        new_node = BinaryTreeNode(value)
        if value < parent.node_value:
            parent.left_child = new_node
        else:
            parent.right_child = new_node
    
    def contains(self, value: Any) -> bool:
        """Проверка наличия элемента в дереве."""
        return self._search_recursively(self.root_element, value)
    
    def _search_recursively(self, current_node: Optional[BinaryTreeNode], 
                           value: Any) -> bool:
        """Рекурсивный поиск элемента."""
        if current_node is None:
            return False
        if value == current_node.node_value:
            return True
        elif value < current_node.node_value:
            return self._search_recursively(current_node.left_child, value)
        else:
            return self._search_recursively(current_node.right_child, value)
    
    def remove(self, value: Any) -> None:
        """Удаление элемента из дерева."""
        self.root_element = self._remove_recursively(self.root_element, value)
    
    def _remove_recursively(self, current_node: Optional[BinaryTreeNode],
                           value: Any) -> Optional[BinaryTreeNode]:
        """Рекурсивное удаление элемента."""
        if current_node is None:
            return None
        
        if value < current_node.node_value:
            current_node.left_child = self._remove_recursively(
                current_node.left_child, value
            )
        elif value > current_node.node_value:
            current_node.right_child = self._remove_recursively(
                current_node.right_child, value
            )
        else:
            if current_node.left_child is None and current_node.right_child is None:
                return None
            elif current_node.left_child is None:
                return current_node.right_child
            elif current_node.right_child is None:
                return current_node.left_child
            else:
                min_node = self._find_minimum_node(current_node.right_child)
                current_node.node_value = min_node.node_value
                current_node.right_child = self._remove_recursively(
                    current_node.right_child, min_node.node_value
                )
        
        return current_node
    
    def _find_minimum_node(self, start_node: BinaryTreeNode) -> BinaryTreeNode:
        """Поиск узла с минимальным значением."""
        current = start_node
        while current.left_child is not None:
            current = current.left_child
        return current
    
    def find_min(self) -> Optional[BinaryTreeNode]:
        """Поиск минимального элемента."""
        if self.root_element is None:
            return None
        
        current = self.root_element
        while current.left_child is not None:
            current = current.left_child
        return current
    
    def find_max(self) -> Optional[BinaryTreeNode]:
        """Поиск максимального элемента."""
        if self.root_element is None:
            return None
        
        current = self.root_element
        while current.right_child is not None:
            current = current.right_child
        return current
    
    def is_valid(self) -> bool:
        """Проверка корректности структуры BST."""
        return self._validate_recursively(self.root_element, float('-inf'), float('inf'))
    
    def _validate_recursively(self, current_node: Optional[BinaryTreeNode],
                            lower_bound: float, upper_bound: float) -> bool:
        """Рекурсивная проверка BST-инвариантов."""
        if current_node is None:
            return True
        
        if current_node.node_value <= lower_bound or current_node.node_value >= upper_bound:
            return False
        
        left_valid = self._validate_recursively(
            current_node.left_child, lower_bound, current_node.node_value
        )
        right_valid = self._validate_recursively(
            current_node.right_child, current_node.node_value, upper_bound
        )
        
        return left_valid and right_valid
    
    def height(self) -> int:
        """Вычисление высоты дерева."""
        return self._compute_height_recursively(self.root_element)
    
    def _compute_height_recursively(self, current_node: Optional[BinaryTreeNode]) -> int:
        """Рекурсивное вычисление высоты."""
        if current_node is None:
            return -1
        left_height = self._compute_height_recursively(current_node.left_child)
        right_height = self._compute_height_recursively(current_node.right_child)
        return max(left_height, right_height) + 1
    
    def size(self) -> int:
        """Подсчет количества элементов в дереве."""
        return self._count_nodes_recursively(self.root_element)
    
    def _count_nodes_recursively(self, current_node: Optional[BinaryTreeNode]) -> int:
        """Рекурсивный подсчет узлов."""
        if current_node is None:
            return 0
        left_count = self._count_nodes_recursively(current_node.left_child)
        right_count = self._count_nodes_recursively(current_node.right_child)
        return left_count + right_count + 1
    
    def to_list_inorder(self) -> List[Any]:
        """Возвращает элементы дерева в отсортированном порядке."""
        result = []
        self._inorder_traversal(self.root_element, result)
        return result
    
    def _inorder_traversal(self, current_node: Optional[BinaryTreeNode],
                          result: List[Any]) -> None:
        """In-order обход дерева."""
        if current_node is not None:
            self._inorder_traversal(current_node.left_child, result)
            result.append(current_node.node_value)
            self._inorder_traversal(current_node.right_child, result)


class TreeTraversal:
    """Методы обхода деревьев."""
    
    @staticmethod
    def inorder_recursive(node: Optional[BinaryTreeNode], 
                         result: Optional[List[Any]] = None) -> List[Any]:
        """Рекурсивный in-order обход."""
        if result is None:
            result = []
        
        if node is not None:
            TreeTraversal.inorder_recursive(node.left_child, result)
            result.append(node.node_value)
            TreeTraversal.inorder_recursive(node.right_child, result)
        
        return result
    
    @staticmethod
    def preorder_recursive(node: Optional[BinaryTreeNode],
                          result: Optional[List[Any]] = None) -> List[Any]:
        """Рекурсивный pre-order обход."""
        if result is None:
            result = []
        
        if node is not None:
            result.append(node.node_value)
            TreeTraversal.preorder_recursive(node.left_child, result)
            TreeTraversal.preorder_recursive(node.right_child, result)
        
        return result
    
    @staticmethod
    def postorder_recursive(node: Optional[BinaryTreeNode],
                           result: Optional[List[Any]] = None) -> List[Any]:
        """Рекурсивный post-order обход."""
        if result is None:
            result = []
        
        if node is not None:
            TreeTraversal.postorder_recursive(node.left_child, result)
            TreeTraversal.postorder_recursive(node.right_child, result)
            result.append(node.node_value)
        
        return result
    
    @staticmethod
    def inorder_iterative(root: Optional[BinaryTreeNode]) -> List[Any]:
        """Итеративный in-order обход."""
        result = []
        stack = []
        current = root
        
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left_child
            
            current = stack.pop()
            result.append(current.node_value)
            current = current.right_child
        
        return result
    
    @staticmethod
    def level_order_traversal(root: Optional[BinaryTreeNode]) -> List[Any]:
        """Обход дерева в ширину (BFS)."""
        if root is None:
            return []
        
        result = []
        queue = [root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.node_value)
            
            if node.left_child is not None:
                queue.append(node.left_child)
            if node.right_child is not None:
                queue.append(node.right_child)
        
        return result


# =================== ТЕСТОВЫЕ КЛАССЫ ===================

class TestBinarySearchTree(unittest.TestCase):
    """Тесты для бинарного дерева поиска."""
    
    def setUp(self):
        """Инициализация тестового окружения."""
        self.tree = BinarySearchTree()
    
    def test_insert_and_search_operations(self):
        """Тестирование операций вставки и поиска."""
        # Вставка элементов
        self.tree.add_element(50)
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.tree.add_element(20)
        self.tree.add_element(40)
        self.tree.add_element(60)
        self.tree.add_element(80)
        
        # Проверка наличия добавленных элементов
        self.assertTrue(self.tree.contains(50))
        self.assertTrue(self.tree.contains(30))
        self.assertTrue(self.tree.contains(70))
        self.assertTrue(self.tree.contains(20))
        self.assertTrue(self.tree.contains(40))
        self.assertTrue(self.tree.contains(60))
        self.assertTrue(self.tree.contains(80))
        
        # Проверка отсутствия недобавленных элементов
        self.assertFalse(self.tree.contains(10))
        self.assertFalse(self.tree.contains(90))
        self.assertFalse(self.tree.contains(55))
    
    def test_inorder_traversal_functionality(self):
        """Тестирование корректности in-order обхода."""
        self.tree.add_element(50)
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.tree.add_element(20)
        self.tree.add_element(40)
        self.tree.add_element(60)
        self.tree.add_element(80)
        
        result = self.tree.to_list_inorder()
        self.assertEqual(result, [20, 30, 40, 50, 60, 70, 80])
    
    def test_delete_operation(self):
        """Тестирование операции удаления элементов."""
        # Создание тестового дерева
        values = [50, 30, 70, 20, 40, 60, 80]
        for value in values:
            self.tree.add_element(value)
        
        # Удаление листа
        self.tree.remove(20)
        self.assertFalse(self.tree.contains(20))
        self.assertEqual(self.tree.to_list_inorder(), [30, 40, 50, 60, 70, 80])
        
        # Удаление узла с одним потомком
        self.tree.remove(30)
        self.assertFalse(self.tree.contains(30))
        self.assertEqual(self.tree.to_list_inorder(), [40, 50, 60, 70, 80])
        
        # Удаление узла с двумя потомками
        self.tree.remove(50)
        self.assertFalse(self.tree.contains(50))
        result = self.tree.to_list_inorder()
        self.assertEqual(result, [40, 60, 70, 80])
    
    def test_find_min_max_operations(self):
        """Тестирование поиска минимального и максимального элементов."""
        self.tree.add_element(50)
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.tree.add_element(20)
        self.tree.add_element(40)
        self.tree.add_element(60)
        self.tree.add_element(80)
        
        min_node = self.tree.find_min()
        self.assertIsNotNone(min_node)
        self.assertEqual(min_node.node_value, 20)
        
        max_node = self.tree.find_max()
        self.assertIsNotNone(max_node)
        self.assertEqual(max_node.node_value, 80)
    
    def test_validity_check(self):
        """Тестирование проверки корректности BST."""
        # Корректное дерево
        self.tree.add_element(50)
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.assertTrue(self.tree.is_valid())
        
        # Создание некорректного дерева вручную
        invalid_tree = BinarySearchTree()
        invalid_tree.root_element = BinaryTreeNode(50)
        invalid_tree.root_element.left_child = BinaryTreeNode(60)  # Нарушение свойства BST
        invalid_tree.root_element.right_child = BinaryTreeNode(70)
        
        self.assertFalse(invalid_tree.is_valid())
    
    def test_height_computation(self):
        """Тестирование вычисления высоты дерева."""
        # Пустое дерево
        self.assertEqual(self.tree.height(), -1)
        
        # Дерево с одним элементом
        self.tree.add_element(50)
        self.assertEqual(self.tree.height(), 0)
        
        # Дерево с несколькими элементами
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.assertEqual(self.tree.height(), 1)
        
        self.tree.add_element(20)
        self.tree.add_element(40)
        self.assertEqual(self.tree.height(), 2)
    
    def test_size_computation(self):
        """Тестирование подсчета количества элементов."""
        self.assertEqual(self.tree.size(), 0)
        
        self.tree.add_element(50)
        self.assertEqual(self.tree.size(), 1)
        
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.assertEqual(self.tree.size(), 3)
        
        self.tree.add_element(20)
        self.tree.add_element(40)
        self.tree.add_element(60)
        self.tree.add_element(80)
        self.assertEqual(self.tree.size(), 7)
    
    def test_traversal_methods(self):
        """Тестирование различных методов обхода."""
        self.tree.add_element(50)
        self.tree.add_element(30)
        self.tree.add_element(70)
        self.tree.add_element(20)
        self.tree.add_element(40)
        self.tree.add_element(60)
        self.tree.add_element(80)
        
        # In-order
        inorder_result = TreeTraversal.inorder_recursive(self.tree.root_element)
        self.assertEqual(inorder_result, [20, 30, 40, 50, 60, 70, 80])
        
        # Pre-order
        preorder_result = TreeTraversal.preorder_recursive(self.tree.root_element)
        self.assertEqual(preorder_result, [50, 30, 20, 40, 70, 60, 80])
        
        # Post-order
        postorder_result = TreeTraversal.postorder_recursive(self.tree.root_element)
        self.assertEqual(postorder_result, [20, 40, 30, 60, 80, 70, 50])
        
        # Итеративный in-order
        iterative_result = TreeTraversal.inorder_iterative(self.tree.root_element)
        self.assertEqual(iterative_result, [20, 30, 40, 50, 60, 70, 80])
        
        # Level-order (BFS)
        level_order_result = TreeTraversal.level_order_traversal(self.tree.root_element)
        self.assertEqual(level_order_result, [50, 30, 70, 20, 40, 60, 80])


class TestEdgeCases(unittest.TestCase):
    """Тестирование граничных случаев и особых сценариев."""
    
    def test_empty_tree_behavior(self):
        """Тестирование поведения пустого дерева."""
        empty_tree = BinarySearchTree()
        self.assertFalse(empty_tree.contains(10))
        self.assertEqual(empty_tree.height(), -1)
        self.assertEqual(empty_tree.size(), 0)
        self.assertEqual(empty_tree.to_list_inorder(), [])
        self.assertIsNone(empty_tree.find_min())
        self.assertIsNone(empty_tree.find_max())
        # Пустое дерево считается корректным BST
        self.assertTrue(empty_tree.is_valid())
    
    def test_single_element_tree(self):
        """Тестирование дерева с единственным элементом."""
        single_tree = BinarySearchTree()
        single_tree.add_element(42)
        
        self.assertTrue(single_tree.contains(42))
        self.assertFalse(single_tree.contains(10))
        self.assertEqual(single_tree.height(), 0)
        self.assertEqual(single_tree.size(), 1)
        
        min_node = single_tree.find_min()
        max_node = single_tree.find_max()
        
        self.assertIsNotNone(min_node)
        self.assertIsNotNone(max_node)
        self.assertEqual(min_node.node_value, 42)
        self.assertEqual(max_node.node_value, 42)
        self.assertTrue(single_tree.is_valid())
    
    def test_duplicate_values_handling(self):
        """Тестирование обработки дублирующихся значений."""
        duplicate_tree = BinarySearchTree()
        duplicate_tree.add_element(50)
        duplicate_tree.add_element(50)  # Дубликат
        duplicate_tree.add_element(30)
        duplicate_tree.add_element(30)  # Дубликат
        
        # BST не должен содержать дубликатов
        self.assertEqual(duplicate_tree.size(), 2)
        self.assertEqual(duplicate_tree.to_list_inorder(), [30, 50])
    
    def test_nonexistent_element_deletion(self):
        """Тестирование удаления несуществующего элемента."""
        test_tree = BinarySearchTree()
        test_tree.add_element(50)
        test_tree.add_element(30)
        test_tree.add_element(70)
        
        # Удаление несуществующего элемента не должно вызывать ошибок
        test_tree.remove(100)
        self.assertEqual(test_tree.size(), 3)
        self.assertEqual(test_tree.to_list_inorder(), [30, 50, 70])


# =================== ЗАПУСК ТЕСТОВ ===================

def run_all_tests():
    """Запуск всех тестов с детальной статистикой."""
    test_loader = unittest.TestLoader()
    
    # Загрузка тестовых наборов
    bst_tests = test_loader.loadTestsFromTestCase(TestBinarySearchTree)
    edge_case_tests = test_loader.loadTestsFromTestCase(TestEdgeCases)
    
    # Объединение тестовых наборов
    complete_test_suite = unittest.TestSuite([bst_tests, edge_case_tests])
    
    # Запуск тестов
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_results = test_runner.run(complete_test_suite)
    
    # Вывод статистики
    print("\n" + "=" * 60)
    print("СТАТИСТИКА ВЫПОЛНЕНИЯ ТЕСТОВ")
    print("=" * 60)
    print(f"Всего тестов: {test_results.testsRun}")
    
    successful_tests = test_results.testsRun - len(test_results.failures) - len(test_results.errors)
    print(f"Успешно пройдено: {successful_tests}")
    print(f"Сбоев: {len(test_results.failures)}")
    print(f"Ошибок: {len(test_results.errors)}")
    
    if test_results.wasSuccessful():
        print("\n✓ Все тесты успешно пройдены!")
    else:
        print("\n✗ Обнаружены проблемы в тестах")
    
    return test_results.wasSuccessful()


def quick_demonstration():
    """Быстрая демонстрация работы бинарного дерева."""
    print("Быстрая демонстрация бинарного дерева поиска:")
    print("=" * 50)
    
    demo_tree = BinarySearchTree()
    demo_values = [50, 30, 70, 20, 40, 60, 80]
    
    print("Добавляем элементы:", demo_values)
    for value in demo_values:
        demo_tree.add_element(value)
    
    print(f"\nКоличество элементов: {demo_tree.size()}")
    print(f"Высота дерева: {demo_tree.height()}")
    print(f"Минимальное значение: {demo_tree.find_min().node_value}")
    print(f"Максимальное значение: {demo_tree.find_max().node_value}")
    print(f"Отсортированные элементы: {demo_tree.to_list_inorder()}")
    print(f"Корректность структуры: {'Да' if demo_tree.is_valid() else 'Нет'}")
    
    # Поиск элементов
    search_tests = [40, 90, 60]
    for value in search_tests:
        found = demo_tree.contains(value)
        print(f"Поиск {value}: {'Найден' if found else 'Не найден'}")


if __name__ == "__main__":
    # Быстрая демонстрация
    quick_demonstration()
    
    # Запрос на запуск тестов
    print("\n" + "=" * 60)
    run_tests = input("Запустить полный набор тестов? (y/n): ")
    
    if run_tests.lower() == 'y':
        success = run_all_tests()
        exit_code = 0 if success else 1
        exit(exit_code)
    else:
        print("Тестирование отменено.")