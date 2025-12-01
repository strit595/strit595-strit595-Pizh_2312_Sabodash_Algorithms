"""
Сравнительный анализ эффективности различных реализаций хеш-таблиц.
"""

import time
import random
import string
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any


# =================== ВСТРОЕННЫЕ РЕАЛИЗАЦИИ ХЕШ-ФУНКЦИЙ ===================

def compute_simple_hash(key_string: str, table_capacity: int) -> int:
    """Вычисление хеш-значения методом суммы кодов символов."""
    character_sum = 0
    for character in key_string:
        character_sum += ord(character)
    return character_sum % table_capacity


def compute_polynomial_hash(key_string: str, table_capacity: int) -> int:
    """Вычисление хеш-значения полиномиальным методом."""
    hash_value = 0
    for character in key_string:
        hash_value = (hash_value * 31 + ord(character)) % table_capacity
    return hash_value


def compute_djb2_hash(key_string: str, table_capacity: int) -> int:
    """Вычисление хеш-значения алгоритмом DJB2."""
    hash_value = 5381
    for character in key_string:
        hash_value = ((hash_value << 5) + hash_value) + ord(character)
    return hash_value % table_capacity


# =================== ВСТРОЕННЫЕ РЕАЛИЗАЦИИ ХЕШ-ТАБЛИЦ ===================

class ChainingHashTable:
    """Хеш-таблица с методом цепочек."""
    
    def __init__(self, initial_size: int = 16, load_factor: float = 0.75,
                 hash_func=compute_polynomial_hash):
        self.capacity = initial_size
        self.max_load_factor = load_factor
        self.hash_function = hash_func
        self.storage = [[] for _ in range(self.capacity)]
        self.element_count = 0
    
    def add_element(self, key: str, value: Any) -> None:
        """Добавление элемента в таблицу."""
        if self.element_count / self.capacity > self.max_load_factor:
            self._expand_table(self.capacity * 2)
        
        bucket_index = self.hash_function(key, self.capacity)
        target_bucket = self.storage[bucket_index]
        
        for i, (k, v) in enumerate(target_bucket):
            if k == key:
                target_bucket[i] = (key, value)
                return
        
        target_bucket.append((key, value))
        self.element_count += 1
    
    def _expand_table(self, new_capacity: int) -> None:
        """Расширение таблицы с перераспределением элементов."""
        old_storage = self.storage
        self.capacity = new_capacity
        self.storage = [[] for _ in range(self.capacity)]
        self.element_count = 0
        
        for bucket in old_storage:
            for k, v in bucket:
                self.add_element(k, v)
    
    def find_element(self, key: str) -> Any:
        """Поиск элемента по ключу."""
        bucket_index = self.hash_function(key, self.capacity)
        for k, v in self.storage[bucket_index]:
            if k == key:
                return v
        return None
    
    def remove_element(self, key: str) -> bool:
        """Удаление элемента по ключу."""
        bucket_index = self.hash_function(key, self.capacity)
        bucket = self.storage[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.element_count -= 1
                return True
        return False
    
    def get_load_factor(self) -> float:
        """Получение текущего коэффициента заполнения."""
        return self.element_count / self.capacity


class OpenAddressingHashTable:
    """Хеш-таблица с открытой адресацией."""
    
    def __init__(self, initial_size: int = 16, load_factor: float = 0.75,
                 probe_method: str = 'linear', hash_func=compute_polynomial_hash):
        self.capacity = initial_size
        self.max_load_factor = load_factor
        self.probe_strategy = probe_method
        self.hash_function = hash_func
        self.storage = [None] * self.capacity
        self.element_count = 0
        self.DELETED = object()
    
    def add_element(self, key: str, value: Any) -> None:
        """Добавление элемента в таблицу."""
        if self.element_count / self.capacity > self.max_load_factor:
            self._expand_table(self.capacity * 2)
        
        for attempt in range(self.capacity):
            index = self._compute_probe_index(key, attempt)
            slot = self.storage[index]
            
            if slot is None or slot == self.DELETED or slot[0] == key:
                was_empty = slot is None or slot == self.DELETED
                self.storage[index] = (key, value)
                if was_empty:
                    self.element_count += 1
                return
        
        self._expand_table(self.capacity * 2)
        self.add_element(key, value)
    
    def _compute_probe_index(self, key: str, attempt: int) -> int:
        """Вычисление индекса с учетом стратегии пробирования."""
        base_hash = self.hash_function(key, self.capacity)
        
        if self.probe_strategy == 'linear':
            return (base_hash + attempt) % self.capacity
        elif self.probe_strategy == 'double':
            secondary_hash = 1 + compute_simple_hash(key, self.capacity - 2)
            return (base_hash + attempt * secondary_hash) % self.capacity
        else:
            raise ValueError(f"Неподдерживаемая стратегия: {self.probe_strategy}")
    
    def _expand_table(self, new_capacity: int) -> None:
        """Расширение таблицы с перераспределением элементов."""
        old_storage = self.storage
        self.capacity = new_capacity
        self.storage = [None] * self.capacity
        self.element_count = 0
        
        for item in old_storage:
            if item is not None and item != self.DELETED:
                k, v = item
                self.add_element(k, v)
    
    def find_element(self, key: str) -> Any:
        """Поиск элемента по ключу."""
        for attempt in range(self.capacity):
            index = self._compute_probe_index(key, attempt)
            slot = self.storage[index]
            
            if slot is None:
                return None
            elif slot != self.DELETED and slot[0] == key:
                return slot[1]
        return None
    
    def remove_element(self, key: str) -> bool:
        """Удаление элемента по ключу."""
        for attempt in range(self.capacity):
            index = self._compute_probe_index(key, attempt)
            slot = self.storage[index]
            
            if slot is None:
                return False
            elif slot != self.DELETED and slot[0] == key:
                self.storage[index] = self.DELETED
                self.element_count -= 1
                return True
        return False
    
    def get_load_factor(self) -> float:
        """Получение текущего коэффициента заполнения."""
        return self.element_count / self.capacity


# =================== ФУНКЦИИ ДЛЯ АНАЛИЗА ПРОИЗВОДИТЕЛЬНОСТИ ===================

def create_random_identifier(length: int = 10) -> str:
    """Генерация случайной строки заданной длины."""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def evaluate_table_performance(
    table_variant: str,
    hash_function,
    probing_strategy: str = None,
    initial_capacity: int = 100,
    load_levels: List[float] = None,
    operation_count: int = 1000
) -> Dict[float, Dict[str, float]]:
    """
    Оценка производительности хеш-таблиц при различных коэффициентах заполнения.
    
    Возвращает:
        Словарь с результатами для каждого уровня загрузки
    """
    if load_levels is None:
        load_levels = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    performance_results = {}
    
    for load_level in load_levels:
        if table_variant == 'chaining':
            test_table = ChainingHashTable(
                initial_size=initial_capacity,
                load_factor=load_level,
                hash_func=hash_function
            )
        else:
            test_table = OpenAddressingHashTable(
                initial_size=initial_capacity,
                load_factor=load_level,
                probe_method=probing_strategy,
                hash_func=hash_function
            )
        
        elements_to_insert = int(initial_capacity * load_level)
        test_dataset = [
            (create_random_identifier(), index)
            for index in range(elements_to_insert)
        ]
        
        # Измерение времени вставки
        start_time = time.perf_counter()
        for identifier, value in test_dataset:
            test_table.add_element(identifier, value)
        insertion_duration = time.perf_counter() - start_time
        
        # Измерение времени поиска
        start_time = time.perf_counter()
        for identifier, _ in test_dataset:
            test_table.find_element(identifier)
        search_duration = time.perf_counter() - start_time
        
        # Измерение времени удаления
        start_time = time.perf_counter()
        for identifier, _ in test_dataset:
            test_table.remove_element(identifier)
        deletion_duration = time.perf_counter() - start_time
        
        # Расчет коэффициента заполнения
        final_load = test_table.get_load_factor()
        
        performance_results[load_level] = {
            "вставка": insertion_duration,
            "поиск": search_duration,
            "удаление": deletion_duration,
            "загрузка": final_load
        }
    
    return performance_results


def compare_hash_function_distribution():
    """Сравнительный анализ равномерности распределения хеш-функций."""
    hash_functions = {
        'Простая сумма': compute_simple_hash,
        'Полиномиальная': compute_polynomial_hash,
        'DJB2': compute_djb2_hash
    }
    
    table_size = 100
    key_count = 1000
    test_identifiers = [create_random_identifier(10) for _ in range(key_count)]
    
    distribution_results = {}
    
    for function_name, hash_function in hash_functions.items():
        bucket_counts = [0] * table_size
        
        for identifier in test_identifiers:
            bucket_index = hash_function(identifier, table_size)
            bucket_counts[bucket_index] += 1
        
        distribution_results[function_name] = bucket_counts
    
    # Визуализация распределения
    figure, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (function_name, bucket_counts) in enumerate(distribution_results.items()):
        current_axis = axes[idx]
        current_axis.hist(bucket_counts, bins=20, alpha=0.7, edgecolor='black')
        current_axis.set_title(f'Распределение: {function_name}')
        current_axis.set_xlabel('Элементов в ячейке')
        current_axis.set_ylabel('Частота')
        current_axis.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('распределение_хешей.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nСтатистика распределения хеш-функций:")
    for function_name, bucket_counts in distribution_results.items():
        average = sum(bucket_counts) / len(bucket_counts)
        dispersion = sum((count - average) ** 2 for count in bucket_counts) / len(bucket_counts)
        std_deviation = dispersion ** 0.5
        print(f"{function_name:15} среднее: {average:6.2f}, отклонение: {std_deviation:6.2f}")


def visualize_performance_comparison(performance_data: Dict[str, Dict[float, Dict[str, float]]]):
    """
    Визуализация результатов сравнения производительности.
    
    Параметры:
        performance_data: Данные производительности для различных реализаций
    """
    figure, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    operation_types = ["вставка", "поиск", "удаление"]
    visual_positions = [(0, 0), (0, 1), (1, 0)]
    
    for operation_type, (row, col) in zip(operation_types, visual_positions):
        current_axis = axes[row, col]
        
        for implementation_name, results in performance_data.items():
            load_levels = list(results.keys())
            operation_times = [results[load][operation_type] for load in load_levels]
            
            current_axis.plot(load_levels, operation_times, marker='o', 
                            linewidth=2, markersize=6, label=implementation_name)
        
        current_axis.set_title(f'Время {operation_type}')
        current_axis.set_xlabel('Коэффициент заполнения')
        current_axis.set_ylabel('Время (сек.)')
        current_axis.legend()
        current_axis.grid(True, alpha=0.3)
    
    # Визуализация коэффициентов заполнения
    final_axis = axes[1, 1]
    
    for implementation_name, results in performance_data.items():
        load_levels = list(results.keys())
        final_loads = [results[load]["загрузка"] for load in load_levels]
        
        final_axis.plot(load_levels, final_loads, marker='s', 
                       linewidth=2, markersize=6, label=implementation_name)
    
    final_axis.set_title('Фактический коэффициент заполнения')
    final_axis.set_xlabel('Целевой коэффициент')
    final_axis.set_ylabel('Фактический коэффициент')
    final_axis.legend()
    final_axis.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('сравнение_производительности.png', dpi=300, bbox_inches='tight')
    plt.close()


def execute_comprehensive_performance_analysis():
    """Выполнение комплексного анализа производительности хеш-таблиц."""
    test_configurations = [
        ('chaining', 'полиномиальная', None, 'Цепочки'),
        ('open_addressing', 'полиномиальная', 'linear', 'Линейное пробирование'),
        ('open_addressing', 'полиномиальная', 'double', 'Двойное хеширование'),
    ]
    
    available_hash_functions = {
        'простая': compute_simple_hash,
        'полиномиальная': compute_polynomial_hash,
        'djb2': compute_djb2_hash
    }
    
    collected_results = {}
    
    print("=" * 60)
    print("КОМПЛЕКСНЫЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ХЕШ-ТАБЛИЦ")
    print("=" * 60)
    
    print("\n1. Анализ распределения хеш-функций...")
    compare_hash_function_distribution()
    
    print("\n2. Сравнение методов разрешения коллизий...")
    for table_type, hash_name, probe_method, implementation_name in test_configurations:
        print(f"   Тестирование: {implementation_name}")
        
        performance_results = evaluate_table_performance(
            table_variant=table_type,
            hash_function=available_hash_functions[hash_name],
            probing_strategy=probe_method,
            initial_capacity=500,
            operation_count=1000
        )
        
        collected_results[implementation_name] = performance_results
    
    print("\n3. Создание визуализаций...")
    visualize_performance_comparison(collected_results)
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ УСПЕШНО ЗАВЕРШЕН!")
    print("=" * 60)
    print("Созданные файлы:")
    print("  - распределение_хешей.png")
    print("  - сравнение_производительности.png")


def quick_demonstration():
    """Быстрая демонстрация работы хеш-таблиц."""
    print("\nБыстрая демонстрация хеш-таблиц:")
    print("-" * 40)
    
    # Тест цепочек
    chaining_table = ChainingHashTable(initial_size=10)
    test_items = [("яблоко", "красное"), ("банан", "желтый"), ("апельсин", "оранжевый")]
    
    for key, value in test_items:
        chaining_table.add_element(key, value)
    
    print("Таблица с цепочками:")
    for key, _ in test_items:
        result = chaining_table.find_element(key)
        print(f"  '{key}' -> '{result}'")
    
    # Тест открытой адресации
    open_table = OpenAddressingHashTable(initial_size=10, probe_method='linear')
    
    for key, value in test_items:
        open_table.add_element(key, value)
    
    print("\nТаблица с открытой адресацией:")
    for key, _ in test_items:
        result = open_table.find_element(key)
        print(f"  '{key}' -> '{result}'")


if __name__ == '__main__':
    quick_demonstration()
    input("\nНажмите Enter для запуска комплексного анализа...")
    execute_comprehensive_performance_analysis()