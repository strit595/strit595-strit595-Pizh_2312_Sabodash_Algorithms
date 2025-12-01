"""
Практическое применение рекурсивных алгоритмов для решения задач.
"""


def recursive_binary_lookup(sorted_collection, search_item, start_index=0, end_index=None):
    """
    Поиск элемента в отсортированной коллекции методом деления пополам.

    Параметры:
        sorted_collection (list): Упорядоченный список элементов.
        search_item: Элемент для поиска.
        start_index (int): Начальный индекс диапазона поиска.
        end_index (int): Конечный индекс диапазона поиска.

    Возвращает:
        int: Позиция элемента или -1 при отсутствии.

    Временная характеристика: O(log n)
    Уровень рекурсии: O(log n)
    """
    if end_index is None:
        end_index = len(sorted_collection) - 1

    if start_index > end_index:
        return -1

    middle_position = (start_index + end_index) // 2
    middle_element = sorted_collection[middle_position]

    if middle_element == search_item:
        return middle_position
    elif middle_element < search_item:
        return recursive_binary_lookup(sorted_collection, search_item, middle_position + 1, end_index)
    else:
        return recursive_binary_lookup(sorted_collection, search_item, start_index, middle_position - 1)


def generate_tower_of_hanoi_solution(disk_count, source_rod="A", helper_rod="B", destination_rod="C"):
    """
    Генерация последовательности перемещений для головоломки "Ханойская башня".

    Параметры:
        disk_count (int): Количество дисков для перемещения.
        source_rod (str): Исходный стержень.
        helper_rod (str): Вспомогательный стержень.
        destination_rod (str): Целевой стержень.

    Возвращает:
        list: Перечень необходимых перемещений.

    Временная характеристика: O(2^n)
    Уровень рекурсии: O(n)
    """
    if disk_count <= 0:
        return []

    movement_sequence = []

    def solve_hanoi_puzzle(disks, source, auxiliary, destination):
        if disks == 1:
            movement_sequence.append(f"Перенос диска 1 со стержня {source} на стержень {destination}")
            return
        
        # Перемещение верхних дисков на вспомогательный стержень
        solve_hanoi_puzzle(disks - 1, source, destination, auxiliary)
        
        # Перемещение самого большого диска на целевой стержень
        movement_sequence.append(f"Перенос диска {disks} со стержня {source} на стержень {destination}")
        
        # Перемещение дисков с вспомогательного на целевой стержень
        solve_hanoi_puzzle(disks - 1, auxiliary, source, destination)

    solve_hanoi_puzzle(disk_count, source_rod, helper_rod, destination_rod)
    return movement_sequence


def demonstrate_binary_search_capability():
    """Демонстрация работы алгоритма бинарного поиска."""
    test_data = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    search_values = [8, 5, 20, 1]

    print("Демонстрация рекурсивного бинарного поиска:")
    print(f"Тестовый массив: {test_data}")
    
    for value in search_values:
        found_position = recursive_binary_lookup(test_data, value)
        if found_position != -1:
            print(f"Элемент {value} обнаружен на позиции {found_position}")
        else:
            print(f"Элемент {value} отсутствует в массиве")


def demonstrate_hanoi_tower_solution():
    """Демонстрация решения головоломки Ханойской башни."""
    disk_quantities = [2, 3]
    
    for quantity in disk_quantities:
        print(f"\nРешение для Ханойской башни с {quantity} дисками:")
        solution_steps = generate_tower_of_hanoi_solution(quantity)
        
        for step_number, step_description in enumerate(solution_steps, 1):
            print(f"Шаг {step_number:2d}: {step_description}")


def validate_algorithms_correctness():
    """Проверка корректности работы алгоритмов."""
    # Проверка бинарного поиска
    verification_array = [1, 3, 5, 7, 9, 11]
    test_cases = [
        (1, 0),   # Первый элемент
        (7, 3),   # Элемент в середине
        (11, 5),  # Последний элемент
        (4, -1),  # Отсутствующий элемент
        (0, -1)   # Элемент меньше минимального
    ]
    
    print("\nПроверка корректности бинарного поиска:")
    for target_value, expected_position in test_cases:
        actual_position = recursive_binary_lookup(verification_array, target_value)
        status = "✓" if actual_position == expected_position else "✗"
        print(f"  Поиск {target_value}: ожидалось {expected_position}, получено {actual_position} {status}")


if __name__ == "__main__":
    print("Практическое применение рекурсивных алгоритмов")
    print("=" * 55)
    
    demonstrate_binary_search_capability()
    demonstrate_hanoi_tower_solution()
    validate_algorithms_correctness()