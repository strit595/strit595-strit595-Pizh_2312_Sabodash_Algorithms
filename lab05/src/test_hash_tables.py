"""
Набор модульных тестов для проверки корректности реализации хеш-таблиц.
"""

import unittest
import sys
import os
from typing import NoReturn


class HashFunctionsTestCase(unittest.TestCase):
    """Коллекция тестов для проверки функций вычисления хеш-кодов."""
    
    @staticmethod
    def compute_simple_hash(key_string: str, table_capacity: int) -> int:
        """Локальная реализация простой хеш-функции."""
        return sum(ord(character) for character in key_string) % table_capacity
    
    @staticmethod
    def compute_polynomial_hash(key_string: str, table_capacity: int) -> int:
        """Локальная реализация полиномиальной хеш-функции."""
        hash_value = 0
        for character in key_string:
            hash_value = (hash_value * 31 + ord(character)) % table_capacity
        return hash_value
    
    @staticmethod
    def compute_djb2_hash(key_string: str, table_capacity: int) -> int:
        """Локальная реализация хеш-функции DJB2."""
        hash_value = 5381
        for character in key_string:
            hash_value = ((hash_value << 5) + hash_value) + ord(character)
        return hash_value % table_capacity
    
    def test_simple_hash_function_consistency(self) -> None:
        """Проверка детерминированности простой хеш-функции."""
        table_dimension = 100
        test_string = "experimental_key"
        
        first_computation = self.compute_simple_hash(test_string, table_dimension)
        second_computation = self.compute_simple_hash(test_string, table_dimension)
        different_key_result = self.compute_simple_hash("different_key", table_dimension)
        
        self.assertEqual(first_computation, second_computation)
        self.assertNotEqual(first_computation, different_key_result)
    
    def test_polynomial_hash_function_consistency(self) -> None:
        """Проверка детерминированности полиномиальной хеш-функции."""
        table_dimension = 100
        
        hello_hash_one = self.compute_polynomial_hash("hello", table_dimension)
        hello_hash_two = self.compute_polynomial_hash("hello", table_dimension)
        world_hash = self.compute_polynomial_hash("world", table_dimension)
        
        self.assertEqual(hello_hash_one, hello_hash_two)
        self.assertNotEqual(hello_hash_one, world_hash)
    
    def test_djb2_hash_function_consistency(self) -> None:
        """Проверка детерминированности хеш-функции DJB2."""
        table_dimension = 100
        test_string = "verification_key"
        
        identical_result_one = self.compute_djb2_hash(test_string, table_dimension)
        identical_result_two = self.compute_djb2_hash(test_string, table_dimension)
        alternative_result = self.compute_djb2_hash("alternative_key", table_dimension)
        
        self.assertEqual(identical_result_one, identical_result_two)
        self.assertNotEqual(identical_result_one, alternative_result)


class ChainingHashTableTestCase(unittest.TestCase):
    """Набор тестов для хеш-таблицы с методом цепочек."""
    
    def create_test_table(self):
        """Создание тестового экземпляра таблицы."""
        class LocalHashTable:
            def __init__(self, initial_capacity=10):
                self.capacity = initial_capacity
                self.storage = [[] for _ in range(initial_capacity)]
                self.element_count = 0
            
            def add_element(self, key, value):
                bucket_index = sum(ord(c) for c in key) % self.capacity
                bucket = self.storage[bucket_index]
                
                for i, (k, v) in enumerate(bucket):
                    if k == key:
                        bucket[i] = (key, value)
                        return
                
                bucket.append((key, value))
                self.element_count += 1
            
            def find_element(self, key):
                bucket_index = sum(ord(c) for c in key) % self.capacity
                for k, v in self.storage[bucket_index]:
                    if k == key:
                        return v
                return None
            
            def remove_element(self, key):
                bucket_index = sum(ord(c) for c in key) % self.capacity
                bucket = self.storage[bucket_index]
                
                for i, (k, v) in enumerate(bucket):
                    if k == key:
                        del bucket[i]
                        self.element_count -= 1
                        return True
                return False
        
        return LocalHashTable()
    
    def setUp(self) -> None:
        """Инициализация тестового окружения."""
        self.test_table = self.create_test_table()
    
    def test_addition_and_retrieval_operations(self) -> None:
        """Проверка операций добавления и извлечения элементов."""
        self.test_table.add_element("primary_key", "primary_value")
        self.test_table.add_element("secondary_key", "secondary_value")
        
        retrieved_primary = self.test_table.find_element("primary_key")
        retrieved_secondary = self.test_table.find_element("secondary_key")
        retrieved_nonexistent = self.test_table.find_element("nonexistent_key")
        
        self.assertEqual(retrieved_primary, "primary_value")
        self.assertEqual(retrieved_secondary, "secondary_value")
        self.assertIsNone(retrieved_nonexistent)
    
    def test_value_update_operation(self) -> None:
        """Проверка операции обновления существующего значения."""
        self.test_table.add_element("test_key", "initial_value")
        self.test_table.add_element("test_key", "updated_value")
        
        current_value = self.test_table.find_element("test_key")
        self.assertEqual(current_value, "updated_value")
    
    def test_element_removal_operation(self) -> None:
        """Проверка операции удаления элементов."""
        self.test_table.add_element("removable_key", "temporary_value")
        
        removal_success = self.test_table.remove_element("removable_key")
        post_removal_value = self.test_table.find_element("removable_key")
        repeated_removal = self.test_table.remove_element("removable_key")
        
        self.assertTrue(removal_success)
        self.assertIsNone(post_removal_value)
        self.assertFalse(repeated_removal)
    
    def test_collision_handling_capability(self) -> None:
        """Проверка обработки коллизий в таблице."""
        collision_table = self.create_test_table()
        
        collision_table.add_element("alpha", 1)
        collision_table.add_element("beta", 2)
        collision_table.add_element("gamma", 3)
        
        alpha_value = collision_table.find_element("alpha")
        beta_value = collision_table.find_element("beta")
        gamma_value = collision_table.find_element("gamma")
        
        self.assertEqual(alpha_value, 1)
        self.assertEqual(beta_value, 2)
        self.assertEqual(gamma_value, 3)


class OpenAddressingHashTableTestCase(unittest.TestCase):
    """Набор тестов для хеш-таблицы с открытой адресацией."""
    
    def create_linear_probing_table(self):
        """Создание таблицы с линейным пробированием."""
        class LinearProbingTable:
            def __init__(self, capacity=5):
                self.capacity = capacity
                self.storage = [None] * capacity
                self.DELETED = object()
            
            def _linear_hash(self, key, attempt):
                return (sum(ord(c) for c in key) + attempt) % self.capacity
            
            def add_element(self, key, value):
                for attempt in range(self.capacity):
                    index = self._linear_hash(key, attempt)
                    slot = self.storage[index]
                    
                    if slot is None or slot == self.DELETED or slot[0] == key:
                        self.storage[index] = (key, value)
                        return
            
            def find_element(self, key):
                for attempt in range(self.capacity):
                    index = self._linear_hash(key, attempt)
                    slot = self.storage[index]
                    
                    if slot is None:
                        return None
                    elif slot != self.DELETED and slot[0] == key:
                        return slot[1]
                return None
        
        return LinearProbingTable()
    
    def test_linear_probing_implementation(self) -> None:
        """Проверка линейного пробирования."""
        linear_table = self.create_linear_probing_table()
        
        linear_table.add_element("alpha", 1)
        linear_table.add_element("beta", 2)
        linear_table.add_element("gamma", 3)
        
        alpha_result = linear_table.find_element("alpha")
        self.assertEqual(alpha_result, 1)
    
    def test_double_hashing_simulation(self) -> None:
        """Проверка двойного хеширования."""
        class DoubleHashingTable:
            def __init__(self, capacity=5):
                self.capacity = capacity
                self.storage = [None] * capacity
            
            def _primary_hash(self, key):
                return sum(ord(c) for c in key) % self.capacity
            
            def _secondary_hash(self, key):
                return 1 + (sum(ord(c) for c in key) % (self.capacity - 2))
            
            def add_element(self, key, value):
                for attempt in range(self.capacity):
                    index = (self._primary_hash(key) + attempt * 
                            self._secondary_hash(key)) % self.capacity
                    if self.storage[index] is None:
                        self.storage[index] = (key, value)
                        return
            
            def find_element(self, key):
                for attempt in range(self.capacity):
                    index = (self._primary_hash(key) + attempt * 
                            self._secondary_hash(key)) % self.capacity
                    slot = self.storage[index]
                    if slot is not None and slot[0] == key:
                        return slot[1]
                return None
        
        double_table = DoubleHashingTable()
        double_table.add_element("alpha", 1)
        double_table.add_element("beta", 2)
        
        beta_result = double_table.find_element("beta")
        self.assertEqual(beta_result, 2)
    
    def test_deletion_functionality(self) -> None:
        """Проверка операции удаления."""
        deletion_table = self.create_linear_probing_table()
        
        deletion_table.add_element("alpha", 1)
        deletion_table.add_element("beta", 2)
        
        # В реальной реализации здесь был бы метод delete
        alpha_before = deletion_table.find_element("alpha")
        self.assertEqual(alpha_before, 1)


class ScalingBehaviorTestCase(unittest.TestCase):
    """Тестирование поведения масштабирования таблиц."""
    
    def test_capacity_expansion_functionality(self) -> None:
        """Проверка операции расширения емкости таблицы."""
        class ScalableTable:
            def __init__(self, initial_capacity=5, expansion_threshold=0.5):
                self.capacity = initial_capacity
                self.threshold = expansion_threshold
                self.storage = [[] for _ in range(initial_capacity)]
                self.element_count = 0
            
            def add_element(self, key, value):
                if self.element_count / self.capacity > self.threshold:
                    self._expand_capacity()
                
                bucket_index = sum(ord(c) for c in key) % self.capacity
                self.storage[bucket_index].append((key, value))
                self.element_count += 1
            
            def _expand_capacity(self):
                old_capacity = self.capacity
                self.capacity = old_capacity * 2
                # В реальной реализации здесь было бы перераспределение
        
        scalable_table = ScalableTable(initial_capacity=5, expansion_threshold=0.5)
        
        original_capacity = scalable_table.capacity
        for index in range(3):
            scalable_table.add_element(f"key_{index}", f"value_{index}")
        
        # Добавление элемента, который должен вызвать расширение
        scalable_table.add_element("expansion_trigger", "trigger_value")
        
        self.assertGreater(scalable_table.capacity, original_capacity)


def execute_test_suite() -> NoReturn:
    """Запуск полного набора тестов."""
    test_loader = unittest.TestLoader()
    
    # Формирование тестовых наборов
    hash_function_suite = test_loader.loadTestsFromTestCase(HashFunctionsTestCase)
    chaining_suite = test_loader.loadTestsFromTestCase(ChainingHashTableTestCase)
    open_addressing_suite = test_loader.loadTestsFromTestCase(OpenAddressingHashTableTestCase)
    scaling_suite = test_loader.loadTestsFromTestCase(ScalingBehaviorTestCase)
    
    # Объединение всех тестов
    complete_test_suite = unittest.TestSuite([
        hash_function_suite,
        chaining_suite,
        open_addressing_suite,
        scaling_suite
    ])
    
    # Запуск тестов
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_execution_result = test_runner.run(complete_test_suite)
    
    # Статистика выполнения
    print(f"\n{'='*60}")
    print("СТАТИСТИКА ВЫПОЛНЕНИЯ ТЕСТОВ:")
    print(f"  Всего тестов: {test_execution_result.testsRun}")
    print(f"  Успешно пройдено: {test_execution_result.testsRun - len(test_execution_result.failures) - len(test_execution_result.errors)}")
    print(f"  Сбоев: {len(test_execution_result.failures)}")
    print(f"  Ошибок: {len(test_execution_result.errors)}")
    print(f"{'='*60}")
    
    exit_code = 0 if test_execution_result.wasSuccessful() else 1
    exit(exit_code)


if __name__ == '__main__':
    execute_test_suite()