"""
Реализация хеш-таблицы с использованием открытой адресации.
"""

from typing import Any, Optional, Tuple, List, Callable


class OpenAddressingHashTable:
    """
    Хеш-таблица с открытой адресацией для хранения пар ключ-значение.

    Особенности:
        - Все элементы хранятся непосредственно в массиве
        - Разрешение коллизий через последовательности пробинга
        - Поддержка различных стратегий разрешения коллизий
    """

    def __init__(self, initial_capacity: int = 16, 
                 max_load_factor: float = 0.75,
                 collision_strategy: str = 'linear',
                 primary_hash_function: Callable[[str, int], int] = None):
        """
        Инициализация экземпляра хеш-таблицы.

        Параметры:
            initial_capacity: Начальный размер внутреннего массива
            max_load_factor: Максимальный допустимый коэффициент заполнения
            collision_strategy: Стратегия разрешения коллизий
            primary_hash_function: Основная функция вычисления хеша
        """
        # Встроенная реализация полиномиального хеширования
        if primary_hash_function is None:
            def compute_polynomial_hash(key_string: str, table_capacity: int) -> int:
                hash_value = 0
                for character in key_string:
                    hash_value = (hash_value * 31 + ord(character)) % table_capacity
                return hash_value
            primary_hash_function = compute_polynomial_hash
        
        # Встроенная реализация двойного хеширования
        def compute_double_hash(key_string: str, table_capacity: int, attempt_num: int) -> int:
            primary_hash = compute_polynomial_hash(key_string, table_capacity)
            # Вторичная хеш-функция
            secondary_hash = 1 + (sum(ord(c) for c in key_string) % (table_capacity - 2))
            return (primary_hash + attempt_num * secondary_hash) % table_capacity
        
        self.capacity = initial_capacity
        self.max_load_factor = max_load_factor
        self.collision_resolution = collision_strategy
        self.primary_hash_func = primary_hash_function
        self.double_hash_func = compute_double_hash
        self.storage = [None] * self.capacity
        self.element_count = 0
        self.DELETED_MARKER = object()  # Маркер для удаленных элементов

    def _compute_probe_index(self, key_string: str, probe_attempt: int) -> int:
        """
        Вычисление индекса с учетом стратегии разрешения коллизий.
        
        Возвращает:
            Индекс в массиве для проверки/вставки
        """
        if self.collision_resolution == 'linear':
            base_index = self.primary_hash_func(key_string, self.capacity)
            return (base_index + probe_attempt) % self.capacity
        
        elif self.collision_resolution == 'double':
            return self.double_hash_func(key_string, self.capacity, probe_attempt)
        
        else:
            raise ValueError(f"Неподдерживаемая стратегия: {self.collision_resolution}")

    def _execute_table_expansion(self, new_capacity: int) -> None:
        """Расширение таблицы с перераспределением всех элементов."""
        previous_storage = self.storage
        self.capacity = new_capacity
        self.storage = [None] * self.capacity
        self.element_count = 0
        
        for storage_entry in previous_storage:
            if storage_entry is not None and storage_entry != self.DELETED_MARKER:
                stored_key, stored_value = storage_entry
                self._insert_entry(stored_key, stored_value)

    def _insert_entry(self, key_string: str, value_data: Any) -> None:
        """Внутренний метод вставки элемента (без проверки расширения)."""
        for probe_attempt in range(self.capacity):
            current_index = self._compute_probe_index(key_string, probe_attempt)
            current_slot = self.storage[current_index]
            
            # Нашли подходящий слот: пустой, удаленный или с тем же ключом
            if (current_slot is None or 
                current_slot == self.DELETED_MARKER or
                (current_slot is not None and current_slot[0] == key_string)):
                
                was_empty_or_deleted = (
                    current_slot is None or 
                    current_slot == self.DELETED_MARKER
                )
                
                self.storage[current_index] = (key_string, value_data)
                
                if was_empty_or_deleted:
                    self.element_count += 1
                
                return
        
        # Если дошли сюда - таблица полностью заполнена
        self._execute_table_expansion(self.capacity * 2)
        self._insert_entry(key_string, value_data)

    def add_element(self, key_string: str, value_data: Any) -> None:
        """
        Добавление нового элемента или обновление существующего.

        Временная сложность:
            - В среднем: O(1/(1-α)), где α - коэффициент заполнения
            - В худшем случае: O(n)
        """
        current_load = self.element_count / self.capacity
        if current_load > self.max_load_factor:
            self._execute_table_expansion(self.capacity * 2)
        
        self._insert_entry(key_string, value_data)

    def find_element(self, key_string: str) -> Optional[Any]:
        """
        Поиск значения по ключу.

        Возвращает:
            Значение или None, если ключ не найден
        """
        for probe_attempt in range(self.capacity):
            current_index = self._compute_probe_index(key_string, probe_attempt)
            current_slot = self.storage[current_index]
            
            if current_slot is None:
                # Пустой слот - элемент не найден
                return None
            
            if (current_slot != self.DELETED_MARKER and 
                current_slot[0] == key_string):
                return current_slot[1]
        
        return None

    def remove_element(self, key_string: str) -> bool:
        """
        Удаление элемента по ключу.

        Возвращает:
            True если элемент удален, False если не найден
        """
        for probe_attempt in range(self.capacity):
            current_index = self._compute_probe_index(key_string, probe_attempt)
            current_slot = self.storage[current_index]
            
            if current_slot is None:
                return False
            
            if (current_slot != self.DELETED_MARKER and 
                current_slot[0] == key_string):
                self.storage[current_index] = self.DELETED_MARKER
                self.element_count -= 1
                return True
        
        return False

    def compute_current_load(self) -> float:
        """Вычисление текущего коэффициента заполнения таблицы."""
        return self.element_count / self.capacity

    def analyze_probing_statistics(self) -> Tuple[int, float]:
        """
        Анализ эффективности стратегии разрешения коллизий.

        Возвращает:
            (общее_число_проб, среднее_число_проб_на_операцию)
        """
        total_probe_count = 0
        successful_operations = 0
        
        for storage_slot in self.storage:
            if storage_slot is not None and storage_slot != self.DELETED_MARKER:
                stored_key, _ = storage_slot
                probes_for_key = 0
                
                for probe_attempt in range(self.capacity):
                    probes_for_key += 1
                    test_index = self._compute_probe_index(stored_key, probe_attempt)
                    
                    test_slot = self.storage[test_index]
                    if (test_slot is not None and 
                        test_slot != self.DELETED_MARKER and
                        test_slot[0] == stored_key):
                        break
                
                total_probe_count += probes_for_key
                successful_operations += 1
        
        average_probes = (
            total_probe_count / successful_operations 
            if successful_operations > 0 else 0.0
        )
        
        return total_probe_count, average_probes

    def contains_key(self, key_string: str) -> bool:
        """Проверка наличия ключа в таблице."""
        return self.find_element(key_string) is not None

    def __len__(self) -> int:
        """Количество элементов в таблице."""
        return self.element_count

    def __contains__(self, key_string: str) -> bool:
        """Поддержка оператора 'in'."""
        return self.contains_key(key_string)

    def __getitem__(self, key_string: str) -> Any:
        """Получение значения через квадратные скобки."""
        value = self.find_element(key_string)
        if value is None:
            raise KeyError(f"Ключ '{key_string}' отсутствует")
        return value

    def __setitem__(self, key_string: str, value_data: Any) -> None:
        """Установка значения через квадратные скобки."""
        self.add_element(key_string, value_data)


def demonstrate_open_addressing_table():
    """Демонстрация работы хеш-таблицы с открытой адресацией."""
    
    # Создание таблицы с линейным пробированием
    print("Хеш-таблица с линейным пробированием:")
    linear_table = OpenAddressingHashTable(
        initial_capacity=10,
        collision_strategy='linear'
    )
    
    test_items = [
        ("apple", "red"),
        ("banana", "yellow"),
        ("orange", "orange"),
        ("grape", "purple"),
        ("apple", "red apple"),  # Обновление
        ("kiwi", "green"),
        ("mango", "yellow-orange")
    ]
    
    for key, value in test_items:
        linear_table.add_element(key, value)
        print(f"  Добавлено: {key} -> {value}")
        print(f"  Текущая загрузка: {linear_table.compute_current_load():.2f}")
    
    # Поиск элементов
    print("\nПоиск элементов:")
    for key in ["apple", "banana", "watermelon"]:
        result = linear_table.find_element(key)
        status = f"найдено: {result}" if result is not None else "не найдено"
        print(f"  {key}: {status}")
    
    # Удаление
    removed = linear_table.remove_element("grape")
    print(f"\nУдаление 'grape': {'успешно' if removed else 'не удалось'}")
    
    # Статистика
    total_probes, avg_probes = linear_table.analyze_probing_statistics()
    print(f"Статистика пробирования: всего проб {total_probes}, "
          f"в среднем {avg_probes:.2f} на элемент")
    
    # Демонстрация с двойным хешированием
    print("\n\nХеш-таблица с двойным хешированием:")
    double_table = OpenAddressingHashTable(
        initial_capacity=10,
        collision_strategy='double'
    )
    
    for key, value in test_items[:4]:
        double_table.add_element(key, value)
    
    double_probes, double_avg = double_table.analyze_probing_statistics()
    print(f"Статистика для двойного хеширования: среднее {double_avg:.2f} проб")


if __name__ == "__main__":
    demonstrate_open_addressing_table()