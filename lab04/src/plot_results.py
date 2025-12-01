"""
Автономный модуль для анализа и визуализации производительности алгоритмов сортировки.
Не требует внешних импортов - все функции реализованы внутри.
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import random
import csv
import statistics
from copy import deepcopy
from typing import List, Dict, Any, Callable


# =================== РЕАЛИЗАЦИЯ ВСЕХ НЕОБХОДИМЫХ ФУНКЦИЙ ===================

# 1. Функции сортировки
def bubble_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка пузырьком."""
    n = len(sequence)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if sequence[j] > sequence[j + 1]:
                sequence[j], sequence[j + 1] = sequence[j + 1], sequence[j]
                swapped = True
        if not swapped:
            break
    return sequence


def selection_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка выбором."""
    n = len(sequence)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if sequence[j] < sequence[min_idx]:
                min_idx = j
        sequence[i], sequence[min_idx] = sequence[min_idx], sequence[i]
    return sequence


def insertion_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка вставками."""
    for i in range(1, len(sequence)):
        key = sequence[i]
        j = i - 1
        while j >= 0 and sequence[j] > key:
            sequence[j + 1] = sequence[j]
            j -= 1
        sequence[j + 1] = key
    return sequence


def merge_sort(sequence: List[Any]) -> List[Any]:
    """Сортировка слиянием."""
    if len(sequence) <= 1:
        return sequence
    
    mid = len(sequence) // 2
    left = merge_sort(sequence[:mid])
    right = merge_sort(sequence[mid:])
    
    return _merge(left, right)


def _merge(left: List[Any], right: List[Any]) -> List[Any]:
    """Слияние двух отсортированных массивов."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(sequence: List[Any]) -> List[Any]:
    """Быстрая сортировка."""
    if len(sequence) <= 1:
        return sequence
    
    pivot = sequence[len(sequence) // 2]
    left = [x for x in sequence if x < pivot]
    middle = [x for x in sequence if x == pivot]
    right = [x for x in sequence if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def is_sorted(sequence: List[Any]) -> bool:
    """Проверка отсортированности массива."""
    return all(sequence[i] <= sequence[i + 1] for i in range(len(sequence) - 1))


# 2. Функции генерации данных
def generate_random_array(size: int) -> List[int]:
    """Генерация случайного массива."""
    return [random.randint(0, size * 10) for _ in range(size)]


def generate_sorted_array(size: int) -> List[int]:
    """Генерация отсортированного массива."""
    return list(range(size))


def generate_reversed_array(size: int) -> List[int]:
    """Генерация обратно отсортированного массива."""
    return list(range(size, 0, -1))


def generate_almost_sorted_array(size: int, swap_percent: float = 5) -> List[int]:
    """Генерация почти отсортированного массива."""
    arr = list(range(size))
    num_swaps = max(1, size * swap_percent // 100)
    
    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    
    return arr


def generate_test_datasets(sizes: List[int] = None) -> Dict[str, Dict[int, List[int]]]:
    """Генерация всех тестовых наборов данных."""
    if sizes is None:
        sizes = [100, 500, 1000]
    
    datasets = {
        'random': {},
        'sorted': {},
        'reversed': {},
        'almost_sorted': {}
    }
    
    for size in sizes:
        datasets['random'][size] = generate_random_array(size)
        datasets['sorted'][size] = generate_sorted_array(size)
        datasets['reversed'][size] = generate_reversed_array(size)
        datasets['almost_sorted'][size] = generate_almost_sorted_array(size)
    
    return datasets


# 3. Функции измерения производительности
def measure_time(sort_func: Callable, data: List[int]) -> float:
    """Измерение времени выполнения сортировки."""
    data_copy = deepcopy(data)
    start = time.perf_counter()
    sort_func(data_copy)
    end = time.perf_counter()
    return (end - start) * 1000  # в миллисекундах


def save_results_to_csv(results: List[Dict[str, Any]], filename: str = "results.csv") -> None:
    """Сохранение результатов в CSV файл."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['algorithm', 'size', 'data_type', 'time_ms'])
        for result in results:
            writer.writerow([
                result['algorithm'],
                result['size'],
                result['data_type'],
                round(result['time_ms'], 6)
            ])


def run_performance_tests() -> List[Dict[str, Any]]:
    """Проведение замеров времени для всех алгоритмов и наборов данных."""
    datasets = generate_test_datasets()
    results = []
    
    sort_functions = {
        "bubble_sort": bubble_sort,
        "selection_sort": selection_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "quick_sort": quick_sort,
    }
    
    for data_type, size_dict in datasets.items():
        for size, arr in size_dict.items():
            print(f"Тест: {data_type}, размер {size}")
            for name, func in sort_functions.items():
                elapsed = measure_time(func, arr)
                test_arr = arr.copy()
                func(test_arr)
                status = "OK" if is_sorted(test_arr) else "ERR"
                print(f"{name:15} | {elapsed:8.2f} ms {status}")
                results.append({
                    "algorithm": name,
                    "size": size,
                    "data_type": data_type,
                    "time_ms": elapsed
                })
    
    save_results_to_csv(results)
    print("Все результаты сохранены в results.csv")
    return results


# =================== ФУНКЦИИ ВИЗУАЛИЗАЦИИ ===================

def plot_comprehensive_comparison(results: Dict[str, Dict[str, Dict[int, float]]]):
    """
    Построение всеобъемлющих графиков сравнения.
    """
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    algorithms = list(results.keys())
    sizes = sorted({size for algo in results.values() 
                   for data_type in algo.values() 
                   for size in data_type.keys()})
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, data_type in enumerate(data_types):
        ax = axes[idx]
        for algo in algorithms:
            if data_type in results[algo]:
                times = []
                for size in sizes:
                    time_val = results[algo][data_type].get(size, 0)
                    times.append(time_val)
                ax.plot(sizes, times, marker='o', linewidth=2,
                        label=algo, markersize=6)
        
        ax.set_title(f'Производительность на {data_type} данных',
                     fontsize=14)
        ax.set_xlabel('Размер массива', fontsize=12)
        ax.set_ylabel('Время (мс)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('comprehensive_performance.png', dpi=300,
                bbox_inches='tight')
    plt.close()
    print("График сохранен как 'comprehensive_performance.png'")


def plot_comparison_histogram(results: dict, size: int = 500):
    """Гистограмма сравнения алгоритмов для фиксированного размера."""
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    algorithms = list(results.keys())
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    for idx, data_type in enumerate(data_types):
        ax = axes[idx]
        times = []
        labels = []
        
        for algo in algorithms:
            if (data_type in results[algo] and
                    size in results[algo][data_type]):
                times.append(results[algo][data_type][size])
                labels.append(algo)
        
        if times:
            sorted_indices = np.argsort(times)
            sorted_times = [times[i] for i in sorted_indices]
            sorted_labels = [labels[i] for i in sorted_indices]
            
            colors = plt.cm.viridis(np.linspace(0, 1, len(times)))
            bars = ax.barh(sorted_labels, sorted_times, color=colors)
            ax.set_title(f'{data_type} данные (n={size})', fontsize=12)
            ax.set_xlabel('Время (мс)')
            
            for bar in bars:
                width = bar.get_width()
                ax.text(width + max(sorted_times) * 0.01,
                        bar.get_y() + bar.get_height()/2,
                        f'{width:.2f}ms', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison_histogram.png', dpi=300,
                bbox_inches='tight')
    plt.close()
    print("График сохранен как 'algorithm_comparison_histogram.png'")


def plot_performance_heatmap(results: dict):
    """Тепловая карта производительности."""
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    algorithms = list(results.keys())
    sizes = sorted({size for algo in results.values() 
                   for data_type in algo.values() 
                   for size in data_type.keys()})
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    heatmap_data = []
    row_labels = []
    
    for algo in algorithms:
        row_data = []
        for data_type in data_types:
            for size in sizes:
                time_val = results[algo].get(data_type, {}).get(size, 0)
                row_data.append(time_val)
        heatmap_data.append(row_data)
        row_labels.append(algo)
    
    heatmap_data = np.array(heatmap_data)
    
    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(data_types) * len(sizes)))
    ax.set_yticks(np.arange(len(algorithms)))
    ax.set_yticklabels(row_labels)
    
    x_labels = []
    for data_type in data_types:
        for size in sizes:
            x_labels.append(f"{data_type[0]}{size}")
    ax.set_xticklabels(x_labels, rotation=45)
    
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Время (мс)', rotation=-90, va="bottom")
    
    ax.set_title("Тепловая карта производительности алгоритмов сортировки",
                 fontsize=14, pad=20)
    
    plt.tight_layout()
    plt.savefig('performance_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("График сохранен как 'performance_heatmap.png'")


def analyze_results(results: List[Dict[str, Any]]):
    """Анализ результатов тестирования."""
    print("=" * 50)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("=" * 50)
    
    # Самые быстрые алгоритмы для каждого размера
    print("Самые быстрые алгоритмы (случайные данные):")
    sizes = sorted(set(r['size'] for r in results))
    for size in sizes:
        size_results = [r for r in results
                        if r['size'] == size and r['data_type'] == 'random']
        if size_results:
            fastest = min(size_results, key=lambda x: x['time_ms'])
            algo = fastest['algorithm']
            time_val = fastest['time_ms']
            print(f"  Размер {size:5}: {algo:15} - {time_val:8.2f} ms")


def print_summary_statistics(results: List[Dict[str, Any]]):
    """Выводит сводную статистику по результатам."""
    print("=" * 50)
    print("СВОДНАЯ СТАТИСТИКА")
    print("=" * 50)
    
    print(f"Всего тестов: {len(results)}")
    print(f"Уникальных алгоритмов: {5}")
    sizes = sorted(set(r['size'] for r in results))
    print(f"Размеры массивов: {sizes}")
    
    times = [r['time_ms'] for r in results]
    if times:
        print(f"Минимальное время: {min(times):.2f} ms")
        print(f"Максимальное время: {max(times):.2f} ms")
        avg_time = statistics.mean(times)
        print(f"Среднее время: {avg_time:.2f} ms")
    
    # Лучший алгоритм в среднем
    algo_times = {}
    for algo in ["bubble_sort", "selection_sort", "insertion_sort", 
                 "merge_sort", "quick_sort"]:
        algo_results = [r for r in results if r['algorithm'] == algo]
        if algo_results:
            total_time = sum(r['time_ms'] for r in algo_results)
            algo_times[algo] = total_time / len(algo_results)
    
    if algo_times:
        best_algo = min(algo_times, key=algo_times.get)
        best_time = algo_times[best_algo]
        print(f"Лучший алгоритм в среднем: {best_algo} ({best_time:.2f} ms)")


def convert_to_nested_format(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[int, float]]]:
    """Конвертирует плоский список результатов во вложенный словарь."""
    nested_results = {}
    
    for result in results:
        algo = result['algorithm']
        data_type = result['data_type']
        size = result['size']
        time_ms = result['time_ms']
        
        if algo not in nested_results:
            nested_results[algo] = {}
        
        if data_type not in nested_results[algo]:
            nested_results[algo][data_type] = {}
        
        nested_results[algo][data_type][size] = time_ms
    
    return nested_results


# =================== ОСНОВНАЯ ФУНКЦИЯ ===================

def main() -> None:
    """Основной запуск: замеры, анализ и построение графиков."""
    print("=" * 60)
    print("ЗАПУСК АНАЛИЗА ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 60)
    
    print("\n1. Проведение замеров производительности...")
    flat_results = run_performance_tests()
    
    print("\n2. Конвертация результатов...")
    nested_results = convert_to_nested_format(flat_results)
    
    print("\n3. Предварительный просмотр данных...")
    print("=" * 50)
    print("ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР ДАННЫХ")
    print("=" * 50)
    for i, result in enumerate(flat_results[:10]):
        algo = result['algorithm']
        size = result['size']
        data_type = result['data_type']
        time_ms = result['time_ms']
        print(f"{i+1:2}. {algo:15} | {size:5} | {data_type:12} | "
              f"{time_ms:8.2f} ms")
    
    print("\n4. Анализ результатов...")
    analyze_results(flat_results)
    print_summary_statistics(flat_results)
    
    print("\n5. Построение графиков...")
    try:
        plot_comprehensive_comparison(nested_results)
        plot_comparison_histogram(nested_results, 500)
        plot_performance_heatmap(nested_results)
        print("\nВсе графики успешно сохранены!")
    except Exception as e:
        print(f"\nОшибка при построении графиков: {e}")
        print("Установите matplotlib: pip install matplotlib")
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН!")
    print("=" * 60)
    print("Созданные файлы:")
    print("- results.csv (табличные данные)")
    print("- comprehensive_performance.png")
    print("- algorithm_comparison_histogram.png")
    print("- performance_heatmap.png")


def test_algorithms():
    """Тестирование корректности всех алгоритмов сортировки."""
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ КОРРЕКТНОСТИ АЛГОРИТМОВ")
    print("=" * 60)
    
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1]
    ]
    
    algorithms = [
        ("Пузырьковая", bubble_sort),
        ("Выбором", selection_sort),
        ("Вставками", insertion_sort),
        ("Слиянием", merge_sort),
        ("Быстрая", quick_sort),
    ]
    
    for test_name, test_arr in enumerate(test_cases):
        print(f"\nТест {test_name}: {test_arr}")
        
        for algo_name, algorithm in algorithms:
            test_copy = test_arr.copy()
            result = algorithm(test_copy)
            is_correct = is_sorted(result)
            status = "✓" if is_correct else "✗"
            print(f"  {algo_name:12}: {status} -> {result}")


if __name__ == "__main__":
    # Сначала протестируем алгоритмы
    test_algorithms()
    
    # Затем запустим основной анализ
    input("\nНажмите Enter для начала анализа производительности...")
    main()