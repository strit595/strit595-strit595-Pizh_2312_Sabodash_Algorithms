"""
Сравнительный анализ производительности структур данных кучи и алгоритмов сортировки.
"""

import time
import random
import sys
import platform
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Any


# =================== ВСТРОЕННЫЕ РЕАЛИЗАЦИИ ===================

class MinHeapStructure:
    """Структура данных минимальной кучи."""
    
    def __init__(self):
        self.heap_container = []
    
    def add_element(self, value: int) -> None:
        """Добавление нового элемента в кучу."""
        self.heap_container.append(value)
        self._restore_heap_property_upward(len(self.heap_container) - 1)
    
    def _restore_heap_property_upward(self, element_index: int) -> None:
        """Восстановление свойства кучи при движении вверх."""
        while element_index > 0:
            parent_index = (element_index - 1) // 2
            if self.heap_container[element_index] < self.heap_container[parent_index]:
                self._exchange_elements(element_index, parent_index)
                element_index = parent_index
            else:
                break
    
    def extract_minimum(self) -> int:
        """Извлечение минимального элемента из кучи."""
        if not self.heap_container:
            raise IndexError("Куча пуста")
        
        min_element = self.heap_container[0]
        last_element = self.heap_container.pop()
        
        if self.heap_container:
            self.heap_container[0] = last_element
            self._restore_heap_property_downward(0)
        
        return min_element
    
    def _restore_heap_property_downward(self, element_index: int) -> None:
        """Восстановление свойства кучи при движении вниз."""
        heap_size = len(self.heap_container)
        
        while True:
            smallest_index = element_index
            left_child_index = 2 * element_index + 1
            right_child_index = 2 * element_index + 2
            
            if (left_child_index < heap_size and 
                self.heap_container[left_child_index] < self.heap_container[smallest_index]):
                smallest_index = left_child_index
            
            if (right_child_index < heap_size and 
                self.heap_container[right_child_index] < self.heap_container[smallest_index]):
                smallest_index = right_child_index
            
            if smallest_index == element_index:
                break
            
            self._exchange_elements(element_index, smallest_index)
            element_index = smallest_index
    
    def _exchange_elements(self, index_a: int, index_b: int) -> None:
        """Обмен элементов по указанным индексам."""
        self.heap_container[index_a], self.heap_container[index_b] = (
            self.heap_container[index_b], self.heap_container[index_a]
        )
    
    def construct_from_array(self, input_array: List[int]) -> None:
        """Построение кучи из массива за O(n)."""
        self.heap_container = input_array[:]
        
        for position in range(len(self.heap_container) // 2 - 1, -1, -1):
            self._restore_heap_property_downward(position)
    
    def verify_heap_property(self) -> bool:
        """Проверка корректности структуры кучи."""
        heap_size = len(self.heap_container)
        
        for current_index in range(heap_size):
            left_child_index = 2 * current_index + 1
            right_child_index = 2 * current_index + 2
            
            if (left_child_index < heap_size and 
                self.heap_container[left_child_index] < self.heap_container[current_index]):
                return False
            
            if (right_child_index < heap_size and 
                self.heap_container[right_child_index] < self.heap_container[current_index]):
                return False
        
        return True


def perform_heap_sort(input_sequence: List[int]) -> List[int]:
    """Сортировка кучей с использованием дополнительной памяти."""
    heap_instance = MinHeapStructure()
    heap_instance.construct_from_array(input_sequence)
    
    sorted_result = []
    while heap_instance.heap_container:
        sorted_result.append(heap_instance.extract_minimum())
    
    return sorted_result


def perform_inplace_heap_sort(input_sequence: List[int]) -> None:
    """In-place сортировка кучей."""
    def _heapify(array: List[int], size: int, root_index: int) -> None:
        largest_index = root_index
        left_child_index = 2 * root_index + 1
        right_child_index = 2 * root_index + 2
        
        if left_child_index < size and array[left_child_index] > array[largest_index]:
            largest_index = left_child_index
        
        if right_child_index < size and array[right_child_index] > array[largest_index]:
            largest_index = right_child_index
        
        if largest_index != root_index:
            array[root_index], array[largest_index] = array[largest_index], array[root_index]
            _heapify(array, size, largest_index)
    
    array_size = len(input_sequence)
    
    # Построение максимальной кучи
    for current_index in range(array_size // 2 - 1, -1, -1):
        _heapify(input_sequence, array_size, current_index)
    
    # Последовательное извлечение элементов
    for current_index in range(array_size - 1, 0, -1):
        input_sequence[0], input_sequence[current_index] = (
            input_sequence[current_index], input_sequence[0]
        )
        _heapify(input_sequence, current_index, 0)


# =================== ФУНКЦИИ СБОРА ИНФОРМАЦИИ ===================

def collect_system_information() -> Dict[str, str]:
    """Сбор информации о системе выполнения."""
    system_details = {
        "Версия Python": sys.version.split()[0],
        "Платформа": platform.platform(),
        "Процессор": platform.processor(),
        "Операционная система": platform.system(),
        "Архитектура": platform.machine(),
    }
    return system_details


# =================== ФУНКЦИИ СРАВНИТЕЛЬНОГО АНАЛИЗА ===================

def evaluate_heap_construction_performance() -> Tuple[List[int], List[float], List[float]]:
    """
    Сравнительная оценка методов построения кучи.
    
    Возвращает:
        Кортеж (размеры_массивов, время_последовательной_вставки, время_оптимального_построения)
    """
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ: ПОСТРОЕНИЕ КУЧИ")
    print("=" * 60)
    
    test_dimensions = [100, 500, 1000, 5000, 10000, 20000]
    sequential_insertion_times = []
    optimal_construction_times = []
    
    for current_size in test_dimensions:
        print(f"Размер тестового массива: {current_size:,}")
        
        # Генерация тестовых данных
        test_data = [random.randint(1, 100_000) for _ in range(current_size)]
        
        # Метод 1: Последовательная вставка элементов
        performance_start = time.perf_counter()
        heap_sequential = MinHeapStructure()
        for element in test_data:
            heap_sequential.add_element(element)
        performance_end = time.perf_counter()
        sequential_duration = performance_end - performance_start
        sequential_insertion_times.append(sequential_duration)
        
        print(f"  Последовательная вставка: {sequential_duration:.6f} секунд")
        
        if not heap_sequential.verify_heap_property():
            print("  ⚠ Нарушено свойство кучи!")
        
        # Метод 2: Оптимальное построение из массива
        performance_start = time.perf_counter()
        heap_optimal = MinHeapStructure()
        heap_optimal.construct_from_array(test_data)
        performance_end = time.perf_counter()
        optimal_duration = performance_end - performance_start
        optimal_construction_times.append(optimal_duration)
        
        print(f"  Оптимальное построение: {optimal_duration:.6f} секунд")
        
        if not heap_optimal.verify_heap_property():
            print("  ⚠ Нарушено свойство кучи!")
        
        # Расчет коэффициента ускорения
        if optimal_duration > 0:
            acceleration_factor = sequential_duration / optimal_duration
            print(f"  Коэффициент ускорения: {acceleration_factor:.2f}")
    
    # Визуализация результатов
    create_performance_visualization(
        test_dimensions,
        sequential_insertion_times,
        optimal_construction_times,
        "Сравнение методов построения кучи",
        "Размер массива (n)",
        "Время выполнения (секунды)",
        ["Последовательная вставка", "Оптимальное построение"],
        "heap_construction_comparison.png"
    )
    
    return test_dimensions, sequential_insertion_times, optimal_construction_times


def evaluate_heap_sort_performance() -> Tuple[List[int], List[float], List[float]]:
    """
    Сравнительная оценка вариантов сортировки кучей.
    
    Возвращает:
        Кортеж (размеры_массивов, время_стандартной_сортировки, время_inplace_сортировки)
    """
    print("\nСРАВНИТЕЛЬНЫЙ АНАЛИЗ: СОРТИРОВКА КУЧЕЙ")
    print("=" * 60)
    
    test_dimensions = [100, 500, 1000, 5000, 10000, 20000]
    standard_sort_times = []
    inplace_sort_times = []
    
    for current_size in test_dimensions:
        print(f"Размер тестового массива: {current_size:,}")
        
        # Генерация тестовых данных
        test_data = [random.randint(1, 100_000) for _ in range(current_size)]
        
        # Метод 1: Стандартная сортировка кучей
        performance_start = time.perf_counter()
        sorted_result = perform_heap_sort(test_data)
        performance_end = time.perf_counter()
        standard_duration = performance_end - performance_start
        standard_sort_times.append(standard_duration)
        
        print(f"  С дополнительной памятью: {standard_duration:.6f} секунд")
        
        # Проверка корректности сортировки
        if sorted_result != sorted(test_data):
            print("  ⚠ Обнаружена ошибка сортировки!")
        
        # Метод 2: In-place сортировка кучей
        data_copy = test_data[:]
        performance_start = time.perf_counter()
        perform_inplace_heap_sort(data_copy)
        performance_end = time.perf_counter()
        inplace_duration = performance_end - performance_start
        inplace_sort_times.append(inplace_duration)
        
        print(f"  In-place реализация: {inplace_duration:.6f} секунд")
        
        # Проверка корректности сортировки
        if data_copy != sorted(test_data):
            print("  ⚠ Обнаружена ошибка сортировки!")
    
    # Визуализация результатов
    create_performance_visualization(
        test_dimensions,
        standard_sort_times,
        inplace_sort_times,
        "Сравнение вариантов сортировки кучей",
        "Размер массива (n)",
        "Время выполнения (секунды)",
        ["С доп. памятью", "In-place реализация"],
        "heap_sort_comparison.png"
    )
    
    return test_dimensions, standard_sort_times, inplace_sort_times


def evaluate_sorting_algorithm_comparison() -> Tuple[List[int], List[float], List[float], List[float], List[float]]:
    """
    Сравнительный анализ различных алгоритмов сортировки.
    
    Возвращает:
        Кортеж (размеры_массивов, время_heapsort, время_quicksort, время_mergesort, время_timsort)
    """
    print("\nСРАВНИТЕЛЬНЫЙ АНАЛИЗ: АЛГОРИТМЫ СОРТИРОВКИ")
    print("=" * 60)
    
    test_dimensions = [100, 500, 1000, 5000, 10000]
    
    def execute_quicksort(sequence: List[int]) -> List[int]:
        """Реализация быстрой сортировки."""
        if len(sequence) <= 1:
            return sequence
        
        pivot_element = sequence[len(sequence) // 2]
        left_partition = [x for x in sequence if x < pivot_element]
        middle_partition = [x for x in sequence if x == pivot_element]
        right_partition = [x for x in sequence if x > pivot_element]
        
        return execute_quicksort(left_partition) + middle_partition + execute_quicksort(right_partition)
    
    def execute_mergesort(sequence: List[int]) -> List[int]:
        """Реализация сортировки слиянием."""
        if len(sequence) <= 1:
            return sequence
        
        middle_index = len(sequence) // 2
        left_part = execute_mergesort(sequence[:middle_index])
        right_part = execute_mergesort(sequence[middle_index:])
        
        return merge_sorted_sequences(left_part, right_part)
    
    def merge_sorted_sequences(left_seq: List[int], right_seq: List[int]) -> List[int]:
        """Слияние двух отсортированных последовательностей."""
        merged_result = []
        left_index = right_index = 0
        
        while left_index < len(left_seq) and right_index < len(right_seq):
            if left_seq[left_index] < right_seq[right_index]:
                merged_result.append(left_seq[left_index])
                left_index += 1
            else:
                merged_result.append(right_seq[right_index])
                right_index += 1
        
        merged_result.extend(left_seq[left_index:])
        merged_result.extend(right_seq[right_index:])
        return merged_result
    
    heapsort_times = []
    quicksort_times = []
    mergesort_times = []
    timsort_times = []
    
    for current_size in test_dimensions:
        print(f"Размер тестового массива: {current_size:,}")
        
        test_data = [random.randint(1, 100_000) for _ in range(current_size)]
        
        # Heapsort (in-place)
        data_copy = test_data[:]
        performance_start = time.perf_counter()
        perform_inplace_heap_sort(data_copy)
        performance_end = time.perf_counter()
        heapsort_duration = performance_end - performance_start
        heapsort_times.append(heapsort_duration)
        print(f"  Heapsort: {heapsort_duration:.6f} секунд")
        
        # Quicksort
        performance_start = time.perf_counter()
        execute_quicksort(test_data)
        performance_end = time.perf_counter()
        quicksort_duration = performance_end - performance_start
        quicksort_times.append(quicksort_duration)
        print(f"  Quicksort: {quicksort_duration:.6f} секунд")
        
        # Mergesort
        performance_start = time.perf_counter()
        execute_mergesort(test_data)
        performance_end = time.perf_counter()
        mergesort_duration = performance_end - performance_start
        mergesort_times.append(mergesort_duration)
        print(f"  Mergesort: {mergesort_duration:.6f} секунд")
        
        # Timsort (встроенная сортировка Python)
        data_copy = test_data[:]
        performance_start = time.perf_counter()
        sorted(data_copy)
        performance_end = time.perf_counter()
        timsort_duration = performance_end - performance_start
        timsort_times.append(timsort_duration)
        print(f"  Timsort (sorted()): {timsort_duration:.6f} секунд")
    
    # Визуализация результатов
    visualization_figure, visualization_axis = plt.subplots(figsize=(12, 7))
    
    visualization_axis.plot(test_dimensions, heapsort_times, 'o-', 
                           label='Heapsort', linewidth=2.5, markersize=8)
    visualization_axis.plot(test_dimensions, quicksort_times, 's-', 
                           label='Quicksort', linewidth=2.5, markersize=8)
    visualization_axis.plot(test_dimensions, mergesort_times, '^-', 
                           label='Mergesort', linewidth=2.5, markersize=8)
    visualization_axis.plot(test_dimensions, timsort_times, 'D-', 
                           label='Timsort (sorted())', linewidth=2.5, markersize=8)
    
    visualization_axis.set_xlabel('Размер массива (n)', fontsize=13)
    visualization_axis.set_ylabel('Время выполнения (секунды)', fontsize=13)
    visualization_axis.set_title('Сравнительный анализ алгоритмов сортировки', 
                                fontsize=15, fontweight='bold')
    visualization_axis.grid(True, linestyle=':', alpha=0.4)
    visualization_axis.legend(fontsize=12)
    visualization_axis.set_xscale('log')
    visualization_axis.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('sorting_algorithms_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nДиаграмма сохранена как 'sorting_algorithms_comparison.png'")
    
    return test_dimensions, heapsort_times, quicksort_times, mergesort_times, timsort_times


def evaluate_heap_operation_performance() -> Tuple[List[int], List[float], List[float]]:
    """
    Анализ производительности основных операций кучи.
    
    Возвращает:
        Кортеж (размеры_кучи, время_вставки, время_извлечения)
    """
    print("\nАНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ: ОСНОВНЫЕ ОПЕРАЦИИ КУЧИ")
    print("=" * 60)
    
    test_dimensions = [100, 500, 1000, 5000, 10000, 20000]
    insertion_times = []
    extraction_times = []
    
    for current_size in test_dimensions:
        print(f"Размер тестовой кучи: {current_size:,}")
        
        heap_instance = MinHeapStructure()
        test_data = [random.randint(1, 100_000) for _ in range(current_size)]
        heap_instance.construct_from_array(test_data)
        
        # Измерение времени вставки
        operation_count = min(100, current_size)
        performance_start = time.perf_counter()
        for _ in range(operation_count):
            heap_instance.add_element(random.randint(1, 100_000))
        performance_end = time.perf_counter()
        average_insertion_time = (performance_end - performance_start) / operation_count
        insertion_times.append(average_insertion_time)
        
        print(f"  Среднее время вставки: {average_insertion_time * 1e6:.2f} микросекунд")
        
        # Восстановление исходного состояния
        heap_instance.construct_from_array(test_data)
        
        # Измерение времени извлечения
        performance_start = time.perf_counter()
        for _ in range(operation_count):
            heap_instance.extract_minimum()
        performance_end = time.perf_counter()
        average_extraction_time = (performance_end - performance_start) / operation_count
        extraction_times.append(average_extraction_time)
        
        print(f"  Среднее время извлечения: {average_extraction_time * 1e6:.2f} микросекунд")
    
    # Визуализация результатов
    create_performance_visualization(
        test_dimensions,
        [t * 1e6 for t in insertion_times],
        [t * 1e6 for t in extraction_times],
        "Производительность операций кучи",
        "Размер кучи (n)",
        "Время выполнения (микросекунды)",
        ["Операция вставки", "Операция извлечения"],
        "heap_operations_performance.png"
    )
    
    return test_dimensions, insertion_times, extraction_times


def create_performance_visualization(x_values: List[int], 
                                   y_values_1: List[float], 
                                   y_values_2: List[float],
                                   diagram_title: str,
                                   x_label: str,
                                   y_label: str,
                                   legend_labels: List[str],
                                   output_filename: str) -> None:
    """
    Создание визуализации для сравнения производительности.
    """
    visualization_figure, visualization_axis = plt.subplots(figsize=(11, 6))
    
    visualization_axis.plot(x_values, y_values_1, 'o-', 
                           label=legend_labels[0], linewidth=2.5, markersize=7)
    visualization_axis.plot(x_values, y_values_2, 's-', 
                           label=legend_labels[1], linewidth=2.5, markersize=7)
    
    visualization_axis.set_xlabel(x_label, fontsize=12)
    visualization_axis.set_ylabel(y_label, fontsize=12)
    visualization_axis.set_title(diagram_title, fontsize=14, fontweight='bold')
    visualization_axis.grid(True, linestyle=':', alpha=0.3)
    visualization_axis.legend(fontsize=11)
    visualization_axis.set_xscale('log')
    visualization_axis.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Диаграмма сохранена как '{output_filename}'")


def execute_comprehensive_performance_analysis():
    """Запуск комплексного анализа производительности."""
    print("НАЧАЛО КОМПЛЕКСНОГО АНАЛИЗА ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    print("\nИНФОРМАЦИЯ О СИСТЕМЕ:")
    for parameter_name, parameter_value in collect_system_information().items():
        print(f"  {parameter_name}: {parameter_value}")
    
    print("\n" + "=" * 60)
    evaluate_heap_construction_performance()
    
    print("\n" + "=" * 60)
    evaluate_heap_sort_performance()
    
    print("\n" + "=" * 60)
    evaluate_sorting_algorithm_comparison()
    
    print("\n" + "=" * 60)
    evaluate_heap_operation_performance()
    
    print("\n" + "=" * 60)
    print("КОМПЛЕКСНЫЙ АНАЛИЗ УСПЕШНО ЗАВЕРШЕН")
    print("Созданные файлы:")
    print("  - heap_construction_comparison.png")
    print("  - heap_sort_comparison.png")
    print("  - sorting_algorithms_comparison.png")
    print("  - heap_operations_performance.png")


if __name__ == "__main__":
    execute_comprehensive_performance_analysis()