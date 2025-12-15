"""
comparison.py
Сравнительный анализ алгоритмов динамического программирования.
Проведение замеров времени и построение графиков.
"""

import time
import random
import matplotlib.pyplot as plt
from dynamic_programming import fibonacci_bottom_up, fibonacci_optimized, knapsack_01_bottom_up


def measure_fibonacci_performance():
    """Измерение времени работы алгоритмов Фибоначчи."""
    sizes = [10, 50, 100, 200, 500, 1000, 2000, 5000]
    times_bottom_up = []
    times_optimized = []
    
    print("\nИзмерение производительности для чисел Фибоначчи:")
    print("n\tBottom-Up\tOptimized")
    print("-" * 40)
    
    for n in sizes:
        # Замер для bottom-up подхода
        start = time.time()
        fibonacci_bottom_up(n)
        time_bu = time.time() - start
        
        # Замер для оптимизированной версии
        start = time.time()
        fibonacci_optimized(n)
        time_opt = time.time() - start
        
        times_bottom_up.append(time_bu)
        times_optimized.append(time_opt)
        
        print(f"{n}\t{time_bu:.6f}\t{time_opt:.6f}")
    
    return sizes, times_bottom_up, times_optimized


def measure_knapsack_performance():
    """Измерение времени работы алгоритма рюкзака 0-1."""
    # Фиксированная вместимость
    capacity = 100
    sizes = [10, 20, 30, 40, 50, 60, 70, 80]
    times = []
    
    print("\n\nИзмерение производительности для задачи о рюкзаке 0-1:")
    print("n предметов\tВремя (сек)")
    print("-" * 40)
    
    for n in sizes:
        # Генерируем случайные предметы
        values = [random.randint(10, 100) for _ in range(n)]
        weights = [random.randint(1, 30) for _ in range(n)]
        
        # Замер времени
        start = time.time()
        knapsack_01_bottom_up(values, weights, capacity)
        elapsed = time.time() - start
        
        times.append(elapsed)
        print(f"{n}\t\t{elapsed:.6f}")
    
    return sizes, times


def plot_fibonacci_performance(sizes, times_bu, times_opt):
    """Построение графиков для алгоритмов Фибоначчи."""
    plt.figure(figsize=(10, 5))
    
    plt.plot(sizes, times_bu, 'bo-', linewidth=2, markersize=6, label='Bottom-Up (O(n) память)')
    plt.plot(sizes, times_opt, 'ro-', linewidth=2, markersize=6, label='Optimized (O(1) память)')
    
    plt.title('Сравнение алгоритмов вычисления чисел Фибоначчи')
    plt.xlabel('n (номер числа Фибоначчи)')
    plt.ylabel('Время выполнения (сек)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('fibonacci_performance.png', dpi=300)
    plt.show()


def plot_knapsack_performance(sizes, times):
    """Построение графиков для задачи о рюкзаке."""
    plt.figure(figsize=(10, 5))
    
    plt.plot(sizes, times, 'go-', linewidth=2, markersize=6)
    
    plt.title('Производительность алгоритма рюкзака 0-1 (capacity=100)')
    plt.xlabel('Количество предметов (n)')
    plt.ylabel('Время выполнения (сек)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('knapsack_performance.png', dpi=300)
    plt.show()


def plot_comparison_chart():
    """Создание общего графика сравнения."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Данные для демонстрации
    sizes_fib = [10, 50, 100, 200, 500]
    times_fib_bu = [0.00001, 0.00005, 0.0001, 0.0002, 0.0005]
    times_fib_opt = [0.00001, 0.00004, 0.00008, 0.00015, 0.0004]
    
    sizes_knap = [10, 20, 30, 40, 50]
    times_knap = [0.0005, 0.002, 0.004, 0.007, 0.011]
    
    # График 1: Фибоначчи
    ax1.plot(sizes_fib, times_fib_bu, 'bo-', label='Фибоначчи Bottom-Up')
    ax1.plot(sizes_fib, times_fib_opt, 'ro-', label='Фибоначчи Optimized')
    ax1.set_title('Алгоритмы Фибоначчи')
    ax1.set_xlabel('n')
    ax1.set_ylabel('Время (сек)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # График 2: Рюкзак
    ax2.plot(sizes_knap, times_knap, 'go-', label='Рюкзак 0-1')
    ax2.set_title('Алгоритм рюкзака 0-1')
    ax2.set_xlabel('Количество предметов')
    ax2.set_ylabel('Время (сек)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('dp_comparison.png', dpi=300)
    plt.show()


def main():
    print("=" * 60)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ АЛГОРИТМОВ ДИНАМИЧЕСКОГО ПРОГРАММИРОВАНИЯ")
    print("=" * 60)
    
    # Измерение производительности
    sizes_fib, times_bu, times_opt = measure_fibonacci_performance()
    sizes_knap, times_knap = measure_knapsack_performance()
    
    # Построение графиков
    print("\nПостроение графиков производительности...")
    
    plot_fibonacci_performance(sizes_fib, times_bu, times_opt)
    plot_knapsack_performance(sizes_knap, times_knap)
    plot_comparison_chart()
    
    print("\nГрафики сохранены в файлы:")
    print("1. fibonacci_performance.png")
    print("2. knapsack_performance.png")
    print("3. dp_comparison.png")
    
    print("\n" + "=" * 60)
    print("Анализ завершен!")
    print("=" * 60)


if __name__ == "__main__":
    main()