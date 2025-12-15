"""
greedy_algorithms.py
Реализация двух жадных алгоритмов:
1. Задача о выборе заявок (Interval Scheduling)
2. Непрерывный рюкзак (Fractional Knapsack)
"""

def interval_scheduling(intervals):
    """
    Жадный алгоритм для задачи о выборе заявок.
    Выбирает максимальное количество непересекающихся интервалов.
    
    Args:
        intervals: список интервалов в формате [(start1, end1), (start2, end2), ...]
    
    Returns:
        selected: список выбранных интервалов
    
    Сложность: O(n log n) из-за сортировки.
    """
    if not intervals:
        return []
    
    # Сортируем интервалы по времени окончания
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    
    selected = []
    last_end_time = -float('inf')
    
    for interval in sorted_intervals:
        start, end = interval
        if start >= last_end_time:
            selected.append(interval)
            last_end_time = end
    
    return selected


def fractional_knapsack(capacity, items):
    """
    Жадный алгоритм для непрерывного рюкзака.
    Максимизирует стоимость рюкзака с возможностью брать части предметов.
    
    Args:
        capacity: вместимость рюкзака
        items: список предметов в формате [(weight1, value1), (weight2, value2), ...]
    
    Returns:
        total_value: максимальная стоимость
        knapsack_items: список взятых предметов (вес, стоимость)
    
    Сложность: O(n log n) из-за сортировки по удельной стоимости.
    """
    if capacity <= 0 or not items:
        return 0.0, []
    
    # Рассчитываем удельную стоимость для каждого предмета
    items_with_ratio = []
    for weight, value in items:
        if weight > 0:
            ratio = value / weight
            items_with_ratio.append((weight, value, ratio))
    
    # Сортируем по удельной стоимости по убыванию
    items_with_ratio.sort(key=lambda x: x[2], reverse=True)
    
    total_value = 0.0
    knapsack_items = []
    remaining_capacity = capacity
    
    for weight, value, ratio in items_with_ratio:
        if remaining_capacity <= 0:
            break
        
        if weight <= remaining_capacity:
            # Берем предмет целиком
            taken_weight = weight
            taken_value = value
            remaining_capacity -= weight
        else:
            # Берем часть предмета
            taken_weight = remaining_capacity
            taken_value = value * (remaining_capacity / weight)
            remaining_capacity = 0
        
        total_value += taken_value
        knapsack_items.append((taken_weight, taken_value))
    
    return total_value, knapsack_items


# Примеры использования
if __name__ == "__main__":
    # Пример 1: Задача о выборе заявок
    intervals = [(1, 3), (2, 5), (3, 6), (5, 7), (6, 8)]
    selected_intervals = interval_scheduling(intervals)
    print("Задача о выборе заявок:")
    print(f"Все интервалы: {intervals}")
    print(f"Выбранные интервалы: {selected_intervals}")
    print(f"Количество выбранных: {len(selected_intervals)}")
    print()
    
    # Пример 2: Непрерывный рюкзак
    capacity = 50
    items = [(10, 60), (20, 100), (30, 120)]
    max_value, knapsack = fractional_knapsack(capacity, items)
    print("Непрерывный рюкзак:")
    print(f"Вместимость рюкзака: {capacity}")
    print(f"Предметы (вес, стоимость): {items}")
    print(f"Максимальная стоимость: {max_value:.2f}")
    print(f"Предметы в рюкзаке: {knapsack}")