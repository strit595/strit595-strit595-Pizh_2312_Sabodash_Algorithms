"""
analysis.py
Анализ производительности жадных алгоритмов.
Проведение замеров времени и построение графиков.
"""

import time
import random
import matplotlib.pyplot as plt
from greedy_algorithms import interval_scheduling, fractional_knapsack


def generate_intervals(n):
    """Генерация n случайных интервалов."""
    intervals = []
    for _ in range(n):
        start = random.randint(0, 100)
        end = start + random.randint(1, 20)
        intervals.append((start, end))
    return intervals


def generate_knapsack_items(n):
    """Генерация n случайных предметов для рюкзака."""
    items = []
    for _ in range(n):
        weight = random.randint(1, 20)
        value = random.randint(10, 100)
        items.append((weight, value))
    return items


def measure_interval_performance():
    """Измерение времени работы алгоритма выбора заявок."""
    sizes = [10, 50, 100, 200, 500, 1000, 2000]
    times = []
    
    for size in sizes:
        intervals = generate_intervals(size)
        
        # Замер времени
        start_time = time.time()
        interval_scheduling(intervals)
        end_time = time.time()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"Размер данных: {size}, Время: {elapsed:.6f} сек")
    
    return sizes, times


def measure_knapsack_performance():
    """Измерение времени работы алгоритма непрерывного рюкзака."""
    sizes = [10, 50, 100, 200, 500, 1000, 2000]
    times = []
    
    for size in sizes:
        items = generate_knapsack_items(size)
        capacity = 100  # Фиксированная вместимость
        
        # Замер времени
        start_time = time.time()
        fractional_knapsack(capacity, items)
        end_time = time.time()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"Размер данных: {size}, Время: {elapsed:.6f} сек")
    
    return sizes, times


def plot_performance(sizes_interval, times_interval, sizes_knapsack, times_knapsack):
    """Построение графиков производительности."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # График 1: Задача о выборе заявок
    ax1.plot(sizes_interval, times_interval, 'bo-', linewidth=2, markersize=6)
    ax1.set_title('Задача о выборе заявок\n(Interval Scheduling)')
    ax1.set_xlabel('Количество интервалов')
    ax1.set_ylabel('Время выполнения (сек)')
    ax1.grid(True, alpha=0.3)
    
    # График 2: Непрерывный рюкзак
    ax2.plot(sizes_knapsack, times_knapsack, 'ro-', linewidth=2, markersize=6)
    ax2.set_title('Непрерывный рюкзак\n(Fractional Knapsack)')
    ax2.set_xlabel('Количество предметов')
    ax2.set_ylabel('Время выполнения (сек)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('performance_plots.png', dpi=300)
    plt.show()


def main():
    print("=" * 60)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ ЖАДНЫХ АЛГОРИТМОВ")
    print("=" * 60)
    
    print("\n1. Задача о выборе заявок:")
    sizes_interval, times_interval = measure_interval_performance()
    
    print("\n2. Непрерывный рюкзак:")
    sizes_knapsack, times_knapsack = measure_knapsack_performance()
    
    print("\n3. Построение графиков...")
    plot_performance(sizes_interval, times_interval, sizes_knapsack, times_knapsack)
    
    print("\nГрафики сохранены в файл 'performance_plots.png'")


if __name__ == "__main__":
    main()