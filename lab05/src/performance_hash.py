"""
Сравнительный анализ эффективности хеш-таблиц с различными методами разрешения коллизий.
"""

import time
import random
import string
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Callable, Optional, Tuple


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

class HashTableWithChaining:
    """Хеш-таблица с методом цепочек."""
    
    def __init__(self, initial_size: int = 16, load_factor: float = 0.75,
                 hash_func=compute_polynomial_hash):
        self.capacity = initial_size
        self.max_load_factor = load_factor
        self.hash_function = hash_func
        self.storage = [[] for _ in range(self.capacity)]
        self.element_count = 0
    
    def insert(self, key: str, value: Any) -> None:
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
                self.insert(k, v)
    
    def search(self, key: str) -> Any:
        """Поиск элемента по ключу."""
        bucket_index = self.hash_function(key, self.capacity)
        for k, v in self.storage[bucket_index]:
            if k == key:
                return v
        return None
    
    def delete(self, key: str) -> bool:
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
    
    def get_collision_stats(self) -> Tuple[int, float]:
        """Получение статистики коллизий."""
        total_collisions = 0
        non_empty_buckets = 0
        
        for bucket in self.storage:
            if len(bucket) > 0:
                total_collisions += len(bucket) - 1
                non_empty_buckets += 1
        
        avg_collisions = total_collisions / non_empty_buckets if non_empty_buckets > 0 else 0
        return total_collisions, avg_collisions


class HashTableOpenAddressing:
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
    
    def insert(self, key: str, value: Any) -> None:
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
        self.insert(key, value)
    
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
                self.insert(k, v)
    
    def search(self, key: str) -> Any:
        """Поиск элемента по ключу."""
        for attempt in range(self.capacity):
            index = self._compute_probe_index(key, attempt)
            slot = self.storage[index]
            
            if slot is None:
                return None
            elif slot != self.DELETED and slot[0] == key:
                return slot[1]
        return None
    
    def delete(self, key: str) -> bool:
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
    
    def get_probe_stats(self) -> Tuple[int, float]:
        """Получение статистики пробирования."""
        total_probes = 0
        operations = 0
        
        for item in self.storage:
            if item is not None and item != self.DELETED:
                key, _ = item
                attempt = 0
                while attempt < self.capacity:
                    index = self._compute_probe_index(key, attempt)
                    total_probes += 1
                    if (self.storage[index] is not None and
                            self.storage[index] != self.DELETED and
                            self.storage[index][0] == key):
                        break
                    attempt += 1
                operations += 1
        
        avg_probes = total_probes / operations if operations > 0 else 0
        return total_probes, avg_probes


# =================== ФУНКЦИИ ДЛЯ АНАЛИЗА ПРОИЗВОДИТЕЛЬНОСТИ ===================

def create_random_string(length: int = 10) -> str:
    """Генерация случайной строки заданной длины."""
    character_pool = string.ascii_letters + string.digits
    return ''.join(random.choices(character_pool, k=length))


def measure_hash_table_performance(
    table_variant: str,
    hash_func: Callable[[str, int], int],
    probe_method: Optional[str] = None,
    initial_size: int = 100,
    load_factors: Optional[List[float]] = None,
    num_operations: int = 1000
) -> Dict[float, Dict[str, Any]]:
    """
    Измерение производительности хеш-таблиц при различных коэффициентах заполнения.
    """
    if load_factors is None:
        load_factors = [0.1, 0.5, 0.7, 0.9]
    
    performance_results = {}
    
    for load_factor in load_factors:
        # Создание экземпляра хеш-таблицы
        if table_variant == 'chaining':
            table_instance = HashTableWithChaining(
                initial_size=initial_size,
                load_factor=load_factor,
                hash_func=hash_func
            )
        else:
            table_instance = HashTableOpenAddressing(
                initial_size=initial_size,
                load_factor=load_factor,
                probe_method=probe_method,
                hash_func=hash_func
            )
        
        # Подготовка тестовых данных
        num_elements = int(initial_size * load_factor)
        test_dataset = [
            (create_random_string(), element_index)
            for element_index in range(num_elements)
        ]
        
        # Измерение времени вставки
        start_time = time.perf_counter()
        for key, value in test_dataset:
            table_instance.insert(key, value)
        insert_duration = time.perf_counter() - start_time
        
        # Измерение времени поиска
        start_time = time.perf_counter()
        for key, _ in test_dataset:
            table_instance.search(key)
        search_duration = time.perf_counter() - start_time
        
        # Измерение времени удаления
        start_time = time.perf_counter()
        for key, _ in test_dataset:
            table_instance.delete(key)
        delete_duration = time.perf_counter() - start_time
        
        # Сбор статистики
        if table_variant == 'chaining':
            collisions, _ = table_instance.get_collision_stats()
        else:
            probes, _ = table_instance.get_probe_stats()
            collisions = probes
        
        # Текущий коэффициент заполнения
        current_load = table_instance.get_load_factor()
        
        # Сохранение результатов
        performance_results[load_factor] = {
            "insert_time": insert_duration,
            "search_time": search_duration,
            "delete_time": delete_duration,
            "collisions": collisions,
            "load_factor": current_load
        }
    
    return performance_results


def analyze_hash_distribution():
    """Анализ распределения хеш-функций."""
    hash_functions = {
        'Простая сумма': compute_simple_hash,
        'Полиномиальная': compute_polynomial_hash,
        'DJB2': compute_djb2_hash
    }
    
    table_size = 100
    num_keys = 1000
    test_keys = [create_random_string(10) for _ in range(num_keys)]
    
    distribution_data = {}
    
    for name, hash_func in hash_functions.items():
        buckets = [0] * table_size
        for key in test_keys:
            index = hash_func(key, table_size)
            buckets[index] += 1
        distribution_data[name] = buckets
    
    # Визуализация распределения
    plt.figure(figsize=(15, 5))
    for i, (name, buckets) in enumerate(distribution_data.items(), 1):
        plt.subplot(1, 3, i)
        plt.hist(buckets, bins=20, alpha=0.7, edgecolor='black')
        plt.title(f'Распределение {name}')
        plt.xlabel('Элементов в корзине')
        plt.ylabel('Частота')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('hash_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nСтатистика распределения:")
    for name, buckets in distribution_data.items():
        avg = sum(buckets) / len(buckets)
        variance = sum((x - avg) ** 2 for x in buckets) / len(buckets)
        std_dev = variance ** 0.5
        print(f"{name}: среднее = {avg:.2f}, отклонение = {std_dev:.2f}")


def visualize_performance_comparison(all_results: Dict[str, Dict[float, Dict[str, Any]]]):
    """Визуализация сравнения производительности."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Время вставки
    for label, results in all_results.items():
        loads = list(results.keys())
        times = [results[load]['insert_time'] for load in loads]
        axes[0, 0].plot(loads, times, marker='o', label=label)
    axes[0, 0].set_title('Время вставки')
    axes[0, 0].set_xlabel('Коэффициент заполнения')
    axes[0, 0].set_ylabel('Время (с)')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Время поиска
    for label, results in all_results.items():
        loads = list(results.keys())
        times = [results[load]['search_time'] for load in loads]
        axes[0, 1].plot(loads, times, marker='o', label=label)
    axes[0, 1].set_title('Время поиска')
    axes[0, 1].set_xlabel('Коэффициент заполнения')
    axes[0, 1].set_ylabel('Время (с)')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Время удаления
    for label, results in all_results.items():
        loads = list(results.keys())
        times = [results[load]['delete_time'] for load in loads]
        axes[1, 0].plot(loads, times, marker='o', label=label)
    axes[1, 0].set_title('Время удаления')
    axes[1, 0].set_xlabel('Коэффициент заполнения')
    axes[1, 0].set_ylabel('Время (с)')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Коллизии
    for label, results in all_results.items():
        loads = list(results.keys())
        collisions = [results[load]['collisions'] for load in loads]
        axes[1, 1].plot(loads, collisions, marker='o', label=label)
    axes[1, 1].set_title('Количество коллизий')
    axes[1, 1].set_xlabel('Коэффициент заполнения')
    axes[1, 1].set_ylabel('Коллизии')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def demonstrate_performance_analysis():
    """Демонстрация анализа производительности."""
    print("Демонстрация оценки производительности хеш-таблиц")
    print("=" * 60)
    
    # Тестирование таблицы с цепочками
    print("\n1. Тестирование хеш-таблицы с цепочками:")
    chaining_results = measure_hash_table_performance(
        table_variant='chaining',
        hash_func=compute_polynomial_hash,
        initial_size=50,
        load_factors=[0.3, 0.6, 0.9],
        num_operations=500
    )
    
    for load_factor, metrics in chaining_results.items():
        print(f"  Загрузка {load_factor:.1f}: "
              f"вставка={metrics['insert_time']:.4f}с, "
              f"поиск={metrics['search_time']:.4f}с, "
              f"коллизии={metrics['collisions']}")
    
    # Тестирование таблицы с открытой адресацией
    print("\n2. Тестирование хеш-таблицы с открытой адресацией:")
    open_addr_results = measure_hash_table_performance(
        table_variant='open_addressing',
        hash_func=compute_polynomial_hash,
        probe_method='linear',
        initial_size=50,
        load_factors=[0.3, 0.6, 0.9],
        num_operations=500
    )
    
    for load_factor, metrics in open_addr_results.items():
        print(f"  Загрузка {load_factor:.1f}: "
              f"вставка={metrics['insert_time']:.4f}с, "
              f"поиск={metrics['search_time']:.4f}с, "
              f"пробы={metrics['collisions']}")


def run_comprehensive_performance_analysis():
    """Запуск комплексного анализа производительности."""
    test_configurations = [
        ('chaining', 'polynomial', None, 'Цепочки'),
        ('open_addressing', 'polynomial', 'linear', 'Линейное пробирование'),
        ('open_addressing', 'polynomial', 'double', 'Двойное хеширование'),
    ]
    
    hash_function_map = {
        'simple': compute_simple_hash,
        'polynomial': compute_polynomial_hash,
        'djb2': compute_djb2_hash
    }
    
    all_results = {}
    
    print("=" * 60)
    print("КОМПЛЕКСНЫЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ХЕШ-ТАБЛИЦ")
    print("=" * 60)
    
    print("\n1. Анализ распределения хеш-функций...")
    analyze_hash_distribution()
    
    print("\n2. Сравнение методов разрешения коллизий...")
    for table_type, hash_name, probe_method, label in test_configurations:
        print(f"   Тестирование: {label}")
        results = measure_hash_table_performance(
            table_variant=table_type,
            hash_func=hash_function_map[hash_name],
            probe_method=probe_method,
            initial_size=500,
            num_operations=1000
        )
        all_results[label] = results
    
    print("\n3. Построение графиков...")
    visualize_performance_comparison(all_results)
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН!")
    print("=" * 60)
    print("Созданы файлы:")
    print("  - hash_distribution.png")
    print("  - performance_comparison.png")


if __name__ == '__main__':
    demonstrate_performance_analysis()
    
    proceed = input("\nЗапустить комплексный анализ? (y/n): ")
    if proceed.lower() == 'y':
        run_comprehensive_performance_analysis()