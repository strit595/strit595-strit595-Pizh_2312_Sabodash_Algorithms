"""
dynamic_programming.py
Реализация двух алгоритмов динамического программирования:
1. Числа Фибоначчи (восходящий подход)
2. Задача о рюкзаке 0-1 (восходящий подход)
"""

def fibonacci_bottom_up(n):
    """
    Вычисление n-го числа Фибоначчи с использованием восходящего ДП.
    
    Args:
        n: номер числа Фибоначчи (n >= 0)
    
    Returns:
        n-е число Фибоначчи
    
    Сложность:
        Время: O(n)
        Память: O(n) (можно оптимизировать до O(1))
    """
    if n <= 1:
        return n
    
    # Создаем массив для хранения промежуточных результатов
    dp = [0] * (n + 1)
    dp[1] = 1
    
    # Заполняем массив снизу вверх
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def fibonacci_optimized(n):
    """
    Оптимизированная версия вычисления чисел Фибоначчи.
    Использует O(1) памяти.
    
    Args:
        n: номер числа Фибоначчи
    
    Returns:
        n-е число Фибоначчи
    
    Сложность:
        Время: O(n)
        Память: O(1)
    """
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def knapsack_01_bottom_up(values, weights, capacity):
    """
    Решение задачи о рюкзаке 0-1 с использованием восходящего ДП.
    
    Args:
        values: список стоимостей предметов
        weights: список весов предметов
        capacity: максимальная вместимость рюкзака
    
    Returns:
        Максимальная стоимость, которую можно унести в рюкзаке
    
    Сложность:
        Время: O(n * capacity), где n - количество предметов
        Память: O(n * capacity)
    """
    n = len(values)
    if n == 0 or capacity == 0:
        return 0
    
    # Создаем 2D таблицу для хранения результатов
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Заполняем таблицу
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Если предмет i можно взять (его вес <= текущей вместимости)
            if weights[i - 1] <= w:
                # Максимум из двух вариантов:
                # 1. Не брать предмет i
                # 2. Брать предмет i + оптимальное решение для оставшейся вместимости
                dp[i][w] = max(
                    dp[i - 1][w],  # не берем предмет
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]  # берем предмет
                )
            else:
                # Предмет слишком тяжелый, не берем его
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]


def knapsack_01_with_reconstruction(values, weights, capacity):
    """
    Решение задачи о рюкзаке 0-1 с восстановлением выбранных предметов.
    
    Args:
        values: список стоимостей предметов
        weights: список весов предметов
        capacity: максимальная вместимость рюкзака
    
    Returns:
        max_value: максимальная стоимость
        selected_items: индексы выбранных предметов
    """
    n = len(values)
    if n == 0 or capacity == 0:
        return 0, []
    
    # Создаем таблицу
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Заполняем таблицу
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Восстанавливаем решение
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
    
    selected_items.reverse()
    return dp[n][capacity], selected_items


def print_dp_table(dp):
    """Вспомогательная функция для вывода таблицы ДП."""
    for row in dp:
        print(" ".join(f"{val:3}" for val in row))


# Примеры использования
if __name__ == "__main__":
    print("=" * 60)
    print("ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ")
    print("=" * 60)
    
    # Пример 1: Числа Фибоначчи
    print("\n1. Числа Фибоначчи:")
    n = 10
    print(f"F({n}) = {fibonacci_bottom_up(n)}")
    print(f"F({n}) (оптимизированная версия) = {fibonacci_optimized(n)}")
    
    # Пример 2: Задача о рюкзаке 0-1
    print("\n2. Задача о рюкзаке 0-1:")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    
    max_value = knapsack_01_bottom_up(values, weights, capacity)
    print(f"Стоимости предметов: {values}")
    print(f"Веса предметов: {weights}")
    print(f"Вместимость рюкзака: {capacity}")
    print(f"Максимальная стоимость: {max_value}")
    
    # Пример с восстановлением решения
    max_value2, selected = knapsack_01_with_reconstruction(values, weights, capacity)
    print(f"\nС восстановлением решения:")
    print(f"Максимальная стоимость: {max_value2}")
    print(f"Выбранные предметы (индексы): {selected}")
    print(f"Выбранные предметы (стоимости): {[values[i] for i in selected]}")