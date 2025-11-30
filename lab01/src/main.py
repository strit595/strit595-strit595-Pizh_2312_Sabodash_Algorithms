# search_analysis.py
import random
import timeit
from typing import List, Optional

import matplotlib.pyplot as plt


def linear_search(arr: List[int], target: int) -> Optional[int]:
    """Линейный поиск элемента в массиве.
    Сложность: O(N), где N - размер массива.
    """
    for i, num in enumerate(arr):  # O(N)
        if num == target:  # O(1)
            return i  # O(1)
    return None  # O(1)


def binary_search(arr: List[int], target: int) -> Optional[int]:
    """Бинарный поиск элемента в отсортированном массиве.
    Сложность: O(log N), где N - размер массива.
    """
    left: int = 0  # O(1)
    right: int = len(arr) - 1  # O(1)
    while left <= right:  # O(log N)
        mid: int = (left + right) // 2  # O(1)
        if arr[mid] == target:  # O(1)
            return mid  # O(1)
        elif arr[mid] < target:  # O(1)
            left = mid + 1  # O(1)
        else:  # O(1)
            right = mid - 1  # O(1)
    return None  # O(1)


def measure_search_time(search_func, arr: List[int], target: int) -> float:
    """Измеряет время выполнения функции поиска в миллисекундах."""
    start_time: float = timeit.default_timer()
    search_func(arr, target)
    end_time: float = timeit.default_timer()
    return (end_time - start_time) * 1000


def run_comparison() -> None:
    """Сравнивает производительность алгоритмов поиска."""
    system_info: str = """
Тестовый стенд:
- Процессор: AMD Ryzen 5 5600G @ 4.3GHz
- Память: 16 GB DDR4
- ОС: Windows 11
- Python: 3.13.2
"""
    print(system_info)

    sizes: List[int] = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    linear_times: List[float] = []
    binary_times: List[float] = []

    print('Сравнение времени поиска (мс):')
    print('{:>10} {:>12} {:>12}'.format(
        'Размер', 'Линейный', 'Бинарный'
    ))

    for size in sizes:
        # Создаем отсортированный массив
        sorted_data: List[int] = (
            sorted([random.randint(1, size * 10) for _ in range(size)])
        )
        # Выбираем целевой элемент (существующий в массиве)
        target: int = random.choice(sorted_data)

        # Измеряем время линейного поиска
        linear_time: float = timeit.timeit(
            lambda: linear_search(sorted_data, target), number=100
        ) * 1000 / 100

        # Измеряем время бинарного поиска
        binary_time: float = timeit.timeit(
            lambda: binary_search(sorted_data, target), number=100
        ) * 1000 / 100

        linear_times.append(linear_time)
        binary_times.append(binary_time)

        print('{:>10} {:>12.4f} {:>12.4f}'.format(
            size, linear_time, binary_time
        ))

    # Построение графиков
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(sizes, linear_times, 'ro-', label='Линейный поиск O(N)')
    plt.plot(sizes, binary_times, 'go-', label='Бинарный поиск O(log N)')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (мс)')
    plt.title('Сравнение алгоритмов поиска')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.subplot(2, 1, 2)
    plt.plot(sizes, linear_times, 'ro-', label='Линейный поиск O(N)')
    plt.plot(sizes, binary_times, 'go-', label='Бинарный поиск O(log N)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Размер массива (log scale)')
    plt.ylabel('Время (мс, log scale)')
    plt.title('Логарифмический масштаб')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('search_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

    print('\nТеоретический анализ сложности:')
    print('• Линейный поиск: O(N)')
    print('  - В худшем случае: N сравнений')
    print('  - В среднем случае: N/2 сравнений')
    print('  - В лучшем случае: 1 сравнение')
    print('• Бинарный поиск: O(log N)')
    print('  - На каждом шаге область поиска уменьшается вдвое')
    print('  - Требует отсортированный массив')
    print('  - Время растет логарифмически с увеличением N')

    print('\nЭкспериментальные выводы:')
    print('• Линейный поиск показывает линейный рост времени')
    print('• Бинарный поиск демонстрирует логарифмическую сложность')
    print('• Для больших массивов бинарный поиск значительно эффективнее')


if __name__ == '__main__':
    run_comparison()