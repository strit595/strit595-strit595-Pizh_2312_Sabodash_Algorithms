"""
Модуль создания тестовых наборов данных для алгоритмических экспериментов.
"""

import random
from typing import List, Dict, Optional


def create_random_integer_sequence(element_count: int,
                                  max_multiplier: int = 10) -> List[int]:
    """Создание последовательности случайных целых чисел."""
    upper_bound = element_count * max_multiplier
    integer_sequence = [random.randint(0, upper_bound) 
                       for _ in range(element_count)]
    return integer_sequence


def create_ascending_integer_sequence(element_count: int) -> List[int]:
    """Создание последовательности целых чисел в порядке возрастания."""
    ascending_sequence = [value for value in range(element_count)]
    return ascending_sequence


def create_descending_integer_sequence(element_count: int) -> List[int]:
    """Создание последовательности целых чисел в порядке убывания."""
    descending_sequence = [value for value 
                          in range(element_count, 0, -1)]
    return descending_sequence


def create_nearly_sorted_sequence(element_count: int,
                                  swap_percentage: float = 5.0,
                                  swap_count: Optional[int] = None) -> List[int]:
    """
    Создание почти отсортированной числовой последовательности.

    Параметры:
        element_count: Количество элементов в последовательности
        swap_percentage: Процент элементов для перемешивания
        swap_count: Явное количество перестановок (переопределяет процент)
    
    Возвращает:
        List[int]: Почти отсортированный список чисел
    """
    sequence = list(range(element_count))
    
    if swap_count is None:
        swaps_required = max(1, int(element_count * swap_percentage / 100))
    else:
        swaps_required = max(1, swap_count)
    
    for swap_index in range(swaps_required):
        position_a = random.randrange(0, element_count)
        position_b = random.randrange(0, element_count)
        sequence[position_a], sequence[position_b] = (
            sequence[position_b], sequence[position_a]
        )
    
    return sequence


def construct_data_collection(sequence_sizes: Optional[List[int]] = None,
                             include_types: Optional[List[str]] = None
                             ) -> Dict[str, Dict[int, List[int]]]:
    """
    Формирование коллекции тестовых наборов данных различных типов.

    Параметры:
        sequence_sizes: Размеры генерируемых последовательностей
        include_types: Типы последовательностей для включения
    
    Возвращает:
        Dict[str, Dict[int, List[int]]]: Словарь с тестовыми наборами
    """
    if sequence_sizes is None:
        sequence_sizes = [100, 1000, 5000, 10000]
    
    if include_types is None:
        include_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    
    data_collection = {}
    
    sequence_generators = {
        'random': create_random_integer_sequence,
        'sorted': create_ascending_integer_sequence,
        'reversed': create_descending_integer_sequence,
        'almost_sorted': create_nearly_sorted_sequence
    }
    
    for data_type in include_types:
        if data_type in sequence_generators:
            data_collection[data_type] = {}
            generator_function = sequence_generators[data_type]
            
            for size in sequence_sizes:
                if data_type == 'almost_sorted':
                    data_collection[data_type][size] = generator_function(size)
                else:
                    data_collection[data_type][size] = generator_function(size)
    
    return data_collection


def preview_data_samples(data_collection: Dict[str, Dict[int, List[int]]],
                        sample_size: int = 10) -> None:
    """
    Показательный вывод образцов из тестовых наборов данных.

    Параметры:
        data_collection: Коллекция тестовых данных
        sample_size: Количество элементов для отображения
    """
    for data_type, size_data in data_collection.items():
        print(f"\n{data_type.upper()} данные:")
        for size, sequence in size_data.items():
            preview_elements = sequence[:sample_size]
            print(f"  Размер {size}: образец {preview_elements}")
            if len(sequence) > sample_size:
                print(f"        ... всего {len(sequence)} элементов")


def verify_data_collection_integrity(
    data_collection: Dict[str, Dict[int, List[int]]]
) -> bool:
    """
    Проверка целостности и корректности сгенерированных данных.

    Параметры:
        data_collection: Коллекция данных для проверки
    
    Возвращает:
        bool: True если все данные корректны
    """
    for data_type, size_data in data_collection.items():
        for size, sequence in size_data.items():
            if len(sequence) != size:
                return False
            if not all(isinstance(element, int) for element in sequence):
                return False
    
    return True


if __name__ == "__main__":
    demonstration_sizes = [50, 200]
    test_data_collection = construct_data_collection(demonstration_sizes)
    
    print("Сгенерированные тестовые наборы данных:")
    preview_data_samples(test_data_collection, sample_size=8)
    
    integrity_status = verify_data_collection_integrity(test_data_collection)
    status_message = "✓ Все наборы данных корректны" if integrity_status else "✗ Обнаружены проблемы"
    print(f"\nПроверка целостности: {status_message}")