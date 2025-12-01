"""
Реализация хеш-таблицы с использованием метода цепочек для обработки коллизий.
"""

from typing import Any, Optional, Tuple, List, Callable


class HashTableWithChaining:
    """
    Структура данных хеш-таблицы с цепочками для разрешения коллизий.

    Характеристики:
        - Коллизии обрабатываются через связные списки (цепи)
        - Автоматическое изменение размера при необходимости
        - Амортизированная сложность операций: O(1 + α), где α - коэффициент заполнения
    """

    def __init__(self, initial_capacity: int = 16, 
                 max_load_factor: float = 0.75,
                 hashing_algorithm: Callable[[str, int], int] = None):
        """
        Конструктор для инициализации хеш-таблицы.

        Параметры:
            initial_capacity: Начальная емкость таблицы
            max_load_factor: Максимально допустимый коэффициент загрузки
            hashing_algorithm: Функция для вычисления хеш-кодов
        """
        if hashing_algorithm is None:
            # Встроенная реализация полиномиального хеширования
            def polynomial_hash(key: str, table_size: int) -> int:
                hash_value = 0
                for character in key:
                    hash_value = (hash_value * 31 + ord(character)) % table_size
                return hash_value
            hashing_algorithm = polynomial_hash
        
        self.capacity = initial_capacity
        self.max_load_factor = max_load_factor
        self.hashing_function = hashing_algorithm
        self.storage = self._create_empty_storage(self.capacity)
        self.element_count = 0

    @staticmethod
    def _create_empty_storage(storage_size: int) -> List[List[Tuple[str, Any]]]:
        """Создание пустого хранилища указанного размера."""
        return [[] for _ in range(storage_size)]

    def _compute_hash_index(self, key_string: str) -> int:
        """Вычисление индекса в таблице для заданного ключа."""
        return self.hashing_function(key_string, self.capacity)

    def _perform_resize_operation(self, new_capacity: int) -> None:
        """Изменение размера таблицы с перераспределением элементов."""
        previous_storage = self.storage
        self.capacity = new_capacity
        self.storage = self._create_empty_storage(self.capacity)
        self.element_count = 0

        for bucket_chain in previous_storage:
            for key_value_pair in bucket_chain:
                stored_key, stored_value = key_value_pair
                self.add_entry(stored_key, stored_value)

    def add_entry(self, key_string: str, value_data: Any) -> None:
        """
        Добавление новой пары ключ-значение в таблицу.

        Временные характеристики:
            - Средний случай: O(1)
            - Наихудший случай: O(n)
        """
        current_load = self.element_count / self.capacity
        if current_load > self.max_load_factor:
            self._perform_resize_operation(self.capacity * 2)

        bucket_index = self._compute_hash_index(key_string)
        target_bucket = self.storage[bucket_index]

        # Проверка существования ключа в цепочке
        for position, (existing_key, existing_value) in enumerate(target_bucket):
            if existing_key == key_string:
                target_bucket[position] = (key_string, value_data)
                return

        # Добавление нового элемента
        target_bucket.append((key_string, value_data))
        self.element_count += 1

    def retrieve_value(self, key_string: str) -> Optional[Any]:
        """
        Получение значения по ключу.

        Временные характеристики:
            - Средний случай: O(1)
            - Наихудший случай: O(n)

        Возвращает:
            Значение, ассоциированное с ключом, или None если ключ не найден
        """
        bucket_index = self._compute_hash_index(key_string)
        target_bucket = self.storage[bucket_index]

        for stored_key, stored_value in target_bucket:
            if stored_key == key_string:
                return stored_value
        
        return None

    def remove_entry(self, key_string: str) -> bool:
        """
        Удаление элемента по ключу.

        Возвращает:
            True если элемент был успешно удален, False если ключ не найден
        """
        bucket_index = self._compute_hash_index(key_string)
        target_bucket = self.storage[bucket_index]

        for position, (stored_key, stored_value) in enumerate(target_bucket):
            if stored_key == key_string:
                del target_bucket[position]
                self.element_count -= 1
                return True
        
        return False

    def contains_key(self, key_string: str) -> bool:
        """Проверка наличия ключа в таблице."""
        return self.retrieve_value(key_string) is not None

    def current_load_factor(self) -> float:
        """Вычисление текущего коэффициента загрузки таблицы."""
        return self.element_count / self.capacity

    def analyze_collision_statistics(self) -> Tuple[int, float]:
        """
        Анализ статистики коллизий в таблице.

        Возвращает:
            Кортеж (общее_число_коллизий, среднее_число_коллизий_на_непустую_ячейку)
        """
        total_collision_count = 0
        non_empty_bucket_count = 0

        for bucket_chain in self.storage:
            chain_length = len(bucket_chain)
            if chain_length > 0:
                collisions_in_bucket = chain_length - 1
                total_collision_count += collisions_in_bucket
                non_empty_bucket_count += 1

        if non_empty_bucket_count > 0:
            average_collisions = total_collision_count / non_empty_bucket_count
        else:
            average_collisions = 0.0

        return total_collision_count, average_collisions

    def get_all_entries(self) -> List[Tuple[str, Any]]:
        """Получение всех пар ключ-значение из таблицы."""
        all_entries = []
        for bucket_chain in self.storage:
            all_entries.extend(bucket_chain)
        return all_entries

    def __len__(self) -> int:
        """Возвращает количество элементов в таблице."""
        return self.element_count

    def __contains__(self, key_string: str) -> bool:
        """Проверка наличия ключа через оператор 'in'."""
        return self.contains_key(key_string)

    def __getitem__(self, key_string: str) -> Any:
        """Получение значения через квадратные скобки."""
        value = self.retrieve_value(key_string)
        if value is None:
            raise KeyError(f"Ключ '{key_string}' не найден в таблице")
        return value

    def __setitem__(self, key_string: str, value_data: Any) -> None:
        """Установка значения через квадратные скобки."""
        self.add_entry(key_string, value_data)


def demonstrate_hash_table_operations():
    """Демонстрация основных операций с хеш-таблицей."""
    hash_table = HashTableWithChaining(initial_capacity=8)
    
    print("Демонстрация работы хеш-таблицы:")
    print("=" * 60)
    
    # Добавление элементов
    test_data = [
        ("apple", "red fruit"),
        ("banana", "yellow fruit"),
        ("orange", "orange fruit"),
        ("grape", "purple fruit"),
        ("apple", "updated apple description")  # Обновление существующего ключа
    ]
    
    for key, value in test_data:
        print(f"Добавление: '{key}' -> '{value}'")
        hash_table.add_entry(key, value)
    
    # Проверка загрузки
    print(f"\nТекущая загрузка таблицы: {hash_table.current_load_factor():.2f}")
    
    # Поиск элементов
    search_keys = ["apple", "banana", "kiwi"]
    for key in search_keys:
        result = hash_table.retrieve_value(key)
        status = f"'{result}'" if result is not None else "не найден"
        print(f"Поиск '{key}': {status}")
    
    # Удаление элемента
    removed = hash_table.remove_entry("grape")
    print(f"\nУдаление 'grape': {'успешно' if removed else 'не удалось'}")
    
    # Статистика коллизий
    collisions, avg_collisions = hash_table.analyze_collision_statistics()
    print(f"Статистика коллизий: всего {collisions}, в среднем {avg_collisions:.2f} на ячейку")
    
    # Использование операторов Python
    print(f"\nОператор 'in': 'apple' в таблице: {'apple' in hash_table}")
    print(f"Длина таблицы: {len(hash_table)} элементов")
    
    # Получение всех элементов
    all_items = hash_table.get_all_entries()
    print(f"\nВсе элементы ({len(all_items)}):")
    for key, value in all_items:
        print(f"  {key}: {value}")


if __name__ == "__main__":
    demonstrate_hash_table_operations()