"""
Модуль реализации рекурсивных алгоритмов с применением кэширования.
"""

import functools
import time
import matplotlib.pyplot as plt


def cache_results(target_function):
    """Декоратор для кэширования результатов выполнения функций."""
    stored_results = {}

    @functools.wraps(target_function)
    def cached_function(*arguments):
        if arguments in stored_results:
            return stored_results[arguments]
        computed_result = target_function(*arguments)
        stored_results[arguments] = computed_result
        return computed_result

    return cached_function


@cache_results
def compute_fibonacci_cached(position):
    """
    Вычисление числа Фибоначчи для заданной позиции с кэшированием.

    Аргументы:
        position (int): Позиция в последовательности Фибоначчи.

    Возвращает:
        int: Число Фибоначчи на указанной позиции.

    Сложность по времени: O(n)
    Глубина рекурсивных вызовов: O(n)
    """
    if position < 0:
        raise ValueError(
            "Позиция в последовательности должна быть неотрицательной"
        )
    if position == 0:
        return 0
    if position == 1:
        return 1
    return (compute_fibonacci_cached(position - 1) +
            compute_fibonacci_cached(position - 2))


class RecursionTracker:
    """Класс для отслеживания количества рекурсивных вызовов."""

    def __init__(self):
        """Инициализация трекера вызовов."""
        self.invocation_count = 0

    def compute_fibonacci_tracked(self, position):
        """
        Вычисление чисел Фибоначчи с подсчетом рекурсивных вызовов.

        Аргументы:
            position (int): Позиция в последовательности.

        Возвращает:
            int: Число Фибоначчи на заданной позиции.
        """
        self.invocation_count += 1
        if position < 0:
            raise ValueError(
                "Позиция должна быть неотрицательным числом"
            )
        if position == 0:
            return 0
        if position == 1:
            return 1
        return (self.compute_fibonacci_tracked(position - 1) +
                self.compute_fibonacci_tracked(position - 2))

    def reset_tracker(self):
        """Обнуление счетчика вызовов."""
        self.invocation_count = 0


def evaluate_performance_difference(position=35):
    """
    Сравнительный анализ эффективности базовой и кэшированной реализаций.

    Аргументы:
        position (int): Позиция для тестирования.
    """
    performance_tracker = RecursionTracker()

    print(f"Сравнительный анализ для позиции {position}")
    print("=" * 60)

    # Базовая реализация с отслеживанием вызовов
    start_timestamp = time.perf_counter()
    performance_tracker.reset_tracker()
    basic_result = performance_tracker.compute_fibonacci_tracked(position)
    basic_duration = time.perf_counter() - start_timestamp
    basic_invocations = performance_tracker.invocation_count

    # Кэшированная реализация
    start_timestamp = time.perf_counter()
    cached_result = compute_fibonacci_cached(position)
    cached_duration = time.perf_counter() - start_timestamp

    print(f"Вычисленное значение: {basic_result}")
    print(f"Базовая реализация: {basic_duration:.8f} секунд")
    print(f"Число рекурсивных вызовов: {basic_invocations}")
    print(f"Кэшированная реализация: {cached_duration:.8f} секунд")
    print(f"Коэффициент ускорения: {basic_duration / cached_duration:.1f}")

    # Верификация корректности результатов
    if basic_result == cached_result:
        print("✓ Результаты вычислений идентичны")
    else:
        print("✗ Обнаружено расхождение в результатах")


def visualize_performance_comparison():
    """
    Визуализация сравнения производительности методов вычисления.
    """
    try:
        from recursion import fibonacci as basic_fibonacci
    except ImportError:
        print("Модуль recursion не найден, используется локальная реализация")
        
        def basic_fibonacci(n):
            if n <= 1:
                return n
            return basic_fibonacci(n-1) + basic_fibonacci(n-2)

    positions = list(range(1, 21))
    basic_execution_times = []
    cached_execution_times = []

    print("\nСбор данных для визуализации...")
    for current_position in positions:
        # Замер времени для базовой реализации
        start_moment = time.perf_counter()
        basic_fibonacci(current_position)
        basic_execution_times.append(time.perf_counter() - start_moment)

        # Замер времени для кэшированной реализации
        start_moment = time.perf_counter()
        compute_fibonacci_cached(current_position)
        cached_execution_times.append(time.perf_counter() - start_moment)

    # Создание визуализации
    chart, coordinate_axes = plt.subplots(figsize=(12, 7))
    
    coordinate_axes.plot(positions, basic_execution_times, 
                        color='crimson', marker='o', linestyle='-',
                        linewidth=2.5, markersize=6, 
                        label='Базовая рекурсия')
    
    coordinate_axes.plot(positions, cached_execution_times,
                        color='forestgreen', marker='s', linestyle='-', 
                        linewidth=2.5, markersize=6,
                        label='С кэшированием')

    coordinate_axes.set_xlabel('Позиция в последовательности (n)')
    coordinate_axes.set_ylabel('Продолжительность вычислений (секунды)')
    coordinate_axes.set_title(
        'Сравнение времени выполнения: базовая рекурсия vs кэширование'
    )
    coordinate_axes.legend()
    coordinate_axes.grid(visible=True, linestyle=':', alpha=0.7)
    
    chart.savefig('fibonacci_performance_chart.png', 
                 dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(chart)

    print("Диаграмма сохранена как 'fibonacci_performance_chart.png'")


def execute_demonstration():
    """Основная функция демонстрации работы алгоритмов."""
    evaluate_performance_difference(35)
    visualize_performance_comparison()


if __name__ == "__main__":
    execute_demonstration()