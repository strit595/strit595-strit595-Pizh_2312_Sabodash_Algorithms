"""
Реализация различных методов вычисления хеш-кодов для строковых идентификаторов.
"""


def calculate_character_sum_hash(identifier_string: str, hash_table_capacity: int) -> int:
    """
    Вычисление хеш-кода методом сложения кодов символов.

    Параметры:
        identifier_string: Строка для хеширования
        hash_table_capacity: Максимальный размер хеш-таблицы

    Возвращает:
        int: Целочисленный хеш в интервале [0, hash_table_capacity - 1]
    """
    accumulated_hash_value = 0
    
    for character in identifier_string:
        character_code = ord(character)
        accumulated_hash_value += character_code
    
    final_hash = accumulated_hash_value % hash_table_capacity
    return final_hash


def compute_polynomial_based_hash(identifier_string: str, 
                                 hash_table_capacity: int, 
                                 polynomial_base: int = 31) -> int:
    """
    Вычисление хеш-кода с использованием полиномиального метода.

    Параметры:
        identifier_string: Строка для хеширования
        hash_table_capacity: Максимальный размер хеш-таблицы
        polynomial_base: Основание полинома (по умолчанию 31)

    Возвращает:
        int: Целочисленный хеш в пределах вместимости таблицы
    """
    current_hash_value = 0
    
    for character in identifier_string:
        character_unicode = ord(character)
        current_hash_value = (current_hash_value * polynomial_base + character_unicode) % hash_table_capacity
    
    return current_hash_value


def generate_djb2_hash_code(identifier_string: str, 
                           hash_table_capacity: int) -> int:
    """
    Генерация хеш-кода по алгоритму DJB2.

    Параметры:
        identifier_string: Строка для хеширования
        hash_table_capacity: Максимальный размер хеш-таблицы

    Возвращает:
        int: Целочисленный хеш, приведенный к размеру таблицы
    """
    INITIAL_HASH_CONSTANT = 5381
    hash_result = INITIAL_HASH_CONSTANT
    
    for character in identifier_string:
        # Эквивалент hash_result * 33 + ord(character)
        hash_result = ((hash_result << 5) + hash_result) + ord(character)
        # Используем побитовое И для ограничения размера (опционально)
        hash_result &= 0xFFFFFFFF
    
    final_result = hash_result % hash_table_capacity
    return final_result


def calculate_double_hash_value(identifier_string: str, 
                               hash_table_capacity: int, 
                               iteration_number: int) -> int:
    """
    Вычисление комбинированного хеш-значения для двойного хеширования.

    Параметры:
        identifier_string: Строка для хеширования
        hash_table_capacity: Максимальный размер хеш-таблицы
        iteration_number: Номер текущей итерации поиска

    Возвращает:
        int: Комбинированное хеш-значение для разрешения коллизий
    """
    primary_hash_value = compute_polynomial_based_hash(
        identifier_string, 
        hash_table_capacity
    )
    
    # Вторичная хеш-функция, всегда возвращающая нечетное значение
    secondary_hash_value = 1 + calculate_character_sum_hash(
        identifier_string, 
        hash_table_capacity - 2
    )
    
    combined_hash = (primary_hash_value + 
                    iteration_number * secondary_hash_value) % hash_table_capacity
    
    return combined_hash


def demonstrate_hash_functions():
    """
    Демонстрация работы различных хеш-функций на тестовых данных.
    """
    test_strings = ["hello", "world", "python", "hash", "table", "test"]
    table_size_example = 10
    
    print("Демонстрация хеш-функций:")
    print("=" * 60)
    print(f"{'Строка':<10} {'Простая':<8} {'Полиномиальная':<14} {'DJB2':<8} {'Двойная (1)':<12}")
    print("-" * 60)
    
    for test_string in test_strings:
        simple_hash_result = calculate_character_sum_hash(test_string, table_size_example)
        poly_hash_result = compute_polynomial_based_hash(test_string, table_size_example)
        djb2_hash_result = generate_djb2_hash_code(test_string, table_size_example)
        double_hash_result = calculate_double_hash_value(test_string, table_size_example, 1)
        
        print(f"{test_string:<10} {simple_hash_result:<8} {poly_hash_result:<14} "
              f"{djb2_hash_result:<8} {double_hash_result:<12}")


def evaluate_hash_distribution():
    """
    Оценка равномерности распределения значений хеш-функций.
    """
    sample_strings = [f"key_{i}" for i in range(100)]
    table_size = 20
    
    hash_functions = [
        ("Простая сумма", calculate_character_sum_hash),
        ("Полиномиальная", compute_polynomial_based_hash),
        ("DJB2", generate_djb2_hash_code),
    ]
    
    print("\nОценка распределения хеш-значений (таблица из 20 ячеек):")
    print("=" * 60)
    
    for function_name, hash_function in hash_functions:
        distribution = [0] * table_size
        
        for string_sample in sample_strings:
            hash_value = hash_function(string_sample, table_size)
            distribution[hash_value] += 1
        
        min_count = min(distribution)
        max_count = max(distribution)
        avg_count = sum(distribution) / table_size
        variance = sum((count - avg_count) ** 2 for count in distribution) / table_size
        
        print(f"\n{function_name}:")
        print(f"  Минимальная частота: {min_count}")
        print(f"  Максимальная частота: {max_count}")
        print(f"  Средняя частота: {avg_count:.2f}")
        print(f"  Дисперсия: {variance:.2f}")


if __name__ == "__main__":
    demonstrate_hash_functions()
    evaluate_hash_distribution()