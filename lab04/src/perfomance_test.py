"""
Эмпирический анализ эффективности алгоритмов упорядочивания.
Полностью автономная версия со встроенными алгоритмами сортировки.
"""

import time
import csv
import random
import statistics
from typing import List, Dict, Any
from copy import deepcopy


# =================== РЕАЛИЗАЦИЯ АЛГОРИТМОВ СОРТИРОВКИ ===================

def bubble_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка пузырьком."""
    element_count = len(sequence)
    
    for iteration in range(element_count):
        exchange_performed = False
        
        for position in range(0, element_count - iteration - 1):
            if sequence[position] > sequence[position + 1]:
                sequence[position], sequence[position + 1] = (
                    sequence[position + 1], sequence[position]
                )
                exchange_performed = True
        
        if not exchange_performed:
            break
    
    return sequence


def selection_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка выбором."""
    element_count = len(sequence)
    
    for current_position in range(element_count):
        position_of_minimum = current_position
        
        for search_position in range(current_position + 1, element_count):
            if sequence[search_position] < sequence[position_of_minimum]:
                position_of_minimum = search_position
        
        sequence[current_position], sequence[position_of_minimum] = (
            sequence[position_of_minimum], sequence[current_position]
        )
    
    return sequence


def insertion_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка вставками."""
    for current_index in range(1, len(sequence)):
        element_to_insert = sequence[current_index]
        compare_position = current_index - 1
        
        while compare_position >= 0 and sequence[compare_position] > element_to_insert:
            sequence[compare_position + 1] = sequence[compare_position]
            compare_position -= 1
        
        sequence[compare_position + 1] = element_to_insert
    
    return sequence


def merge_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка слиянием."""
    if len(sequence) <= 1:
        return sequence
    
    middle_index = len(sequence) // 2
    left_part = merge_sort(sequence[:middle_index])
    right_part = merge_sort(sequence[middle_index:])
    
    return _merge_sorted_sequences(left_part, right_part)


def _merge_sorted_sequences(first_sequence: List[Any], 
                            second_sequence: List[Any]) -> List[Any]:
    """Объединение двух отсортированных последовательностей."""
    combined_result = []
    first_index = second_index = 0
    
    while first_index < len(first_sequence) and second_index < len(second_sequence):
        if first_sequence[first_index] <= second_sequence[second_index]:
            combined_result.append(first_sequence[first_index])
            first_index += 1
        else:
            combined_result.append(second_sequence[second_index])
            second_index += 1
    
    combined_result.extend(first_sequence[first_index:])
    combined_result.extend(second_sequence[second_index:])
    return combined_result


def quick_sort(sequence: List[Any]) -> List[Any]:
    """Быстрая сортировка."""
    if len(sequence) <= 1:
        return sequence
    
    pivot_element = sequence[len(sequence) // 2]
    left_partition = [element for element in sequence if element < pivot_element]
    middle_partition = [element for element in sequence if element == pivot_element]
    right_partition = [element for element in sequence if element > pivot_element]
    
    return quick_sort(left_partition) + middle_partition + quick_sort(right_partition)


def is_sorted(sequence: List[Any]) -> bool:
    """Проверка отсортированности последовательности."""
    for index in range(len(sequence) - 1):
        if sequence[index] > sequence[index + 1]:
            return False
    return True


# =================== ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ ===================

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
                                  swap_percentage: float = 5.0) -> List[int]:
    """Создание почти отсортированной числовой последовательности."""
    sequence = list(range(element_count))
    swaps_required = max(1, int(element_count * swap_percentage / 100))
    
    for _ in range(swaps_required):
        position_a = random.randrange(0, element_count)
        position_b = random.randrange(0, element_count)
        sequence[position_a], sequence[position_b] = (
            sequence[position_b], sequence[position_a]
        )
    
    return sequence


def construct_data_collection(sequence_sizes: List[int] = None) -> Dict[str, Dict[int, List[int]]]:
    """
    Формирование коллекции тестовых наборов данных различных типов.
    """
    if sequence_sizes is None:
        sequence_sizes = [100, 500, 1000, 5000]
    
    data_collection = {}
    
    sequence_generators = {
        'random': create_random_integer_sequence,
        'sorted': create_ascending_integer_sequence,
        'reversed': create_descending_integer_sequence,
        'almost_sorted': create_nearly_sorted_sequence
    }
    
    for data_type, generator_function in sequence_generators.items():
        data_collection[data_type] = {}
        for size in sequence_sizes:
            data_collection[data_type][size] = generator_function(size)
    
    return data_collection


# =================== ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===================

def measure_execution_duration(sorting_function, data_sequence: List[Any]) -> float:
    """
    Измерение длительности выполнения сортировки на копировании данных.
    
    Возвращает:
        float: Время выполнения в миллисекундах
    """
    data_duplicate = deepcopy(data_sequence)
    start_timestamp = time.perf_counter()
    sorting_function(data_duplicate)
    end_timestamp = time.perf_counter()
    
    return (end_timestamp - start_timestamp) * 1000


def store_results_in_csv(experiment_results: List[Dict[str, Any]], 
                         output_filename: str = "performance_results.csv") -> None:
    """
    Сохранение результатов эксперимента в файл формата CSV.
    """
    with open(output_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        column_names = ['алгоритм', 'размер', 'тип_данных', 'время_мс']
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        
        csv_writer.writeheader()
        for measurement in experiment_results:
            csv_writer.writerow({
                'алгоритм': measurement['название_алгоритма'],
                'размер': measurement['размер_данных'],
                'тип_данных': measurement['категория_данных'],
                'время_мс': round(measurement['длительность_мс'], 6)
            })


def perform_performance_benchmarks() -> List[Dict[str, Any]]:
    """
    Проведение серии замеров производительности для всех алгоритмов.
    """
    print("Создание тестовых наборов данных...")
    test_datasets = construct_data_collection()
    benchmark_results = []

    algorithm_collection = {
        "пузырьковая_сортировка": bubble_sort,
        "сортировка_выбором": selection_sort,
        "сортировка_вставками": insertion_sort,
        "сортировка_слиянием": merge_sort,
        "быстрая_сортировка": quick_sort,
    }

    for data_category, size_mappings in test_datasets.items():
        for data_size, number_sequence in size_mappings.items():
            print(f"\nТестирование: {data_category}, размерность {data_size}")
            
            for algorithm_name, algorithm_function in algorithm_collection.items():
                execution_time = measure_execution_duration(algorithm_function, number_sequence)
                
                verification_copy = deepcopy(number_sequence)
                algorithm_function(verification_copy)
                verification_status = "✓" if is_sorted(verification_copy) else "✗"
                
                print(f"{algorithm_name:25} | {execution_time:8.2f} мс {verification_status}")
                
                benchmark_results.append({
                    'название_алгоритма': algorithm_name,
                    'размер_данных': data_size,
                    'категория_данных': data_category,
                    'длительность_мс': execution_time
                })

    store_results_in_csv(benchmark_results)
    print("\nПолные результаты сохранены в файл performance_results.csv")
    return benchmark_results


def analyze_performance_data(experiment_results: List[Dict[str, Any]]) -> None:
    """
    Аналитическая обработка собранных данных производительности.
    """
    print("=" * 65)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ")
    print("=" * 65)

    print("Наиболее быстродействующие алгоритмы (случайные данные):")
    available_sizes = sorted({result['размер_данных'] for result in experiment_results})
    
    for current_size in available_sizes:
        size_specific_results = [
            result for result in experiment_results
            if result['размер_данных'] == current_size 
            and result['категория_данных'] == 'random'
        ]
        
        if size_specific_results:
            optimal_result = min(size_specific_results, 
                                key=lambda x: x['длительность_мс'])
            optimal_algorithm = optimal_result['название_алгоритма']
            optimal_time = optimal_result['длительность_мс']
            
            print(f"  Размерность {current_size:6}: {optimal_algorithm:30} - {optimal_time:8.2f} мс")


def display_statistical_summary(experiment_results: List[Dict[str, Any]]) -> None:
    """
    Отображение статистического обзора результатов экспериментов.
    """
    print("=" * 65)
    print("СТАТИСТИЧЕСКИЙ ОБЗОР РЕЗУЛЬТАТОВ")
    print("=" * 65)

    print(f"Общее количество экспериментов: {len(experiment_results):,}")
    print(f"Количество тестируемых алгоритмов: {5}")
    
    unique_sizes = sorted({result['размер_данных'] for result in experiment_results})
    print(f"Тестируемые размерности данных: {unique_sizes}")

    time_measurements = [result['длительность_мс'] for result in experiment_results]
    
    if time_measurements:
        print(f"Минимальное время выполнения: {min(time_measurements):.2f} мс")
        print(f"Максимальное время выполнения: {max(time_measurements):.2f} мс")
        
        average_duration = statistics.mean(time_measurements)
        print(f"Средняя длительность выполнения: {average_duration:.2f} мс")

        # Определение алгоритма с наилучшей средней производительностью
        algorithm_performance = {}
        algorithm_names = ["пузырьковая_сортировка", "сортировка_выбором", 
                          "сортировка_вставками", "сортировка_слиянием", 
                          "быстрая_сортировка"]
        
        for algorithm_name in algorithm_names:
            algorithm_results = [
                result for result in experiment_results 
                if result['название_алгоритма'] == algorithm_name
            ]
            
            if algorithm_results:
                total_algorithm_time = sum(
                    result['длительность_мс'] for result in algorithm_results
                )
                algorithm_performance[algorithm_name] = (
                    total_algorithm_time / len(algorithm_results)
                )

        if algorithm_performance:
            optimal_algorithm_name = min(
                algorithm_performance, 
                key=algorithm_performance.get
            )
            optimal_average_time = algorithm_performance[optimal_algorithm_name]
            
            print(f"Алгоритм с наилучшей средней производительностью:")
            print(f"  {optimal_algorithm_name} - {optimal_average_time:.2f} мс")


def showcase_sample_data(experiment_results: List[Dict[str, Any]], 
                        sample_count: int = 12) -> None:
    """
    Демонстрация выборки результатов эксперимента.
    """
    print("=" * 65)
    print(f"ОБРАЗЕЦ РЕЗУЛЬТАТОВ (первые {sample_count} записей)")
    print("=" * 65)
    
    for index, measurement in enumerate(experiment_results[:sample_count], 1):
        algorithm = measurement['название_алгоритма']
        size = measurement['размер_данных']
        data_type = measurement['категория_данных']
        duration = measurement['длительность_мс']
        
        print(f"{index:3}. {algorithm:30} | Размер: {size:6} | "
              f"Тип: {data_type:12} | Время: {duration:8.2f} мс")


def conduct_experimental_analysis() -> None:
    """
    Основная процедура проведения и анализа экспериментов производительности.
    """
    print("=" * 65)
    print("НАЧАЛО ЭКСПЕРИМЕНТАЛЬНОГО АНАЛИЗА АЛГОРИТМОВ УПОРЯДОЧИВАНИЯ")
    print("=" * 65)
    print("Этап 1: Генерация тестовых данных...")
    print("Этап 2: Проведение замеров производительности...")
    
    experimental_results = perform_performance_benchmarks()
    
    showcase_sample_data(experimental_results)
    analyze_performance_data(experimental_results)
    display_statistical_summary(experimental_results)
    
    print("=" * 65)
    print("ЭКСПЕРИМЕНТАЛЬНЫЙ АНАЛИЗ УСПЕШНО ЗАВЕРШЕН!")
    print("Детальные результаты сохранены в performance_results.csv")
    print("Протестированные алгоритмы: пузырьковая сортировка, выбором, вставками, слиянием, быстрая")


def demonstrate_algorithms_on_small_example():
    """Демонстрация работы алгоритмов на небольшом примере."""
    print("\n" + "=" * 65)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ НА МАЛОМ ПРИМЕРЕ")
    print("=" * 65)
    
    demonstration_data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"Исходные данные: {demonstration_data}")
    
    algorithms = [
        ("Пузырьковая", bubble_sort),
        ("Выбором", selection_sort),
        ("Вставками", insertion_sort),
        ("Слиянием", merge_sort),
        ("Быстрая", quick_sort)
    ]
    
    for name, func in algorithms:
        test_data = demonstration_data[:]
        sorted_result = func(test_data)
        correct = is_sorted(sorted_result)
        status = "✓" if correct else "✗"
        print(f"{name:12} {status}: {sorted_result}")


if __name__ == "__main__":
    demonstrate_algorithms_on_small_example()
    conduct_experimental_analysis()