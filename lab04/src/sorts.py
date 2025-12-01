"""
Модуль с реализацией алгоритмов сортировки.
"""

from typing import List, Any


def bubble_sort(arr: List[Any]) -> List[Any]:
    """
    Сортировка пузырьком.

    Args:
        arr: Исходный массив

    Returns:
        Отсортированный массив

    Сложность:
        Временная:
            - Худший случай: O(n²)
            - Средний случай: O(n²)
            - Лучший случай: O(n)
        Пространственная: O(1)
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: List[Any]) -> List[Any]:
    """
    Сортировка выбором.

    Args:
        arr: Исходный массив

    Returns:
        Отсортированный массив

    Сложность:
        Временная:
            - Худший случай: O(n²)
            - Средний случай: O(n²)
            - Лучший случай: O(n²)
        Пространственная: O(1)
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr: List[Any]) -> List[Any]:
    """
    Сортировка вставками.

    Args:
        arr: Исходный массив

    Returns:
        Отсортированный массив

    Сложность:
        Временная:
            - Худший случай: O(n²)
            - Средний случай: O(n²)
            - Лучший случай: O(n)
        Пространственная: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: List[Any]) -> List[Any]:
    """
    Сортировка слиянием.

    Args:
        arr: Исходный массив

    Returns:
        Отсортированный массив

    Сложность:
        Временная:
            - Худший случай: O(n log n)
            - Средний случай: O(n log n)
            - Лучший случай: O(n log n)
        Пространственная: O(n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

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


def quick_sort(arr: List[Any]) -> List[Any]:
    """
    Быстрая сортировка.

    Args:
        arr: Исходный массив

    Returns:
        Отсортированный массив

    Сложность:
        Временная:
            - Худший случай: O(n²)
            - Средний случай: O(n log n)
            - Лучший случай: O(n log n)
        Пространственная: O(log n)
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def is_sorted(arr: List[Any]) -> bool:
    """
    Проверка отсортированности массива.

    Args:
        arr: Массив для проверки

    Returns:
        True если массив отсортирован, иначе False
    """
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def test_sorting_correctness():
    """
    Тестирование корректности всех алгоритмов сортировки.

    Returns:
        Словарь с результатами тестирования
    """
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

    results = {}

    for test_name, test_arr in enumerate(test_cases):
        results[test_name] = {}
        print(f"\nТест {test_name}: {test_arr}")

        for algo_name, algorithm in algorithms:
            test_copy = test_arr.copy()
            result = algorithm(test_copy)
            is_correct = is_sorted(result)
            results[test_name][algo_name] = is_correct
            status = "✓" if is_correct else "✗"
            print(f"  {algo_name:12}: {status} -> {result}")

    return results


if __name__ == "__main__":
    print("Тестирование корректности сортировки:")
    test_sorting_correctness()