"""Анализ эффективности различных структур данных."""
import timeit
from collections import deque
import matplotlib.pyplot as plt


class ListNode:
    """Элемент связного списка."""
    
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    """Однонаправленный связный список с указателями на начало и конец."""
    
    def __init__(self):
        self._first = None
        self._last = None
    
    def insert_at_start(self, value) -> None:
        """Добавление элемента в начало списка. O(1)"""
        new_element = ListNode(value)
        
        if not self._first:
            self._first = self._last = new_element
        else:
            new_element.next = self._first
            self._first = new_element
    
    def insert_at_end(self, value) -> None:
        """Добавление элемента в конец списка. O(1)"""
        new_element = ListNode(value)
        
        if not self._last:
            self._first = self._last = new_element
        else:
            self._last.next = new_element
            self._last = new_element
    
    def delete_from_start(self):
        """Извлечение элемента из начала списка. O(1)"""
        if self._first is None:
            return None
        
        extracted_value = self._first.value
        self._first = self._first.next
        
        if self._first is None:
            self._last = None
            
        return extracted_value
    
    def traversal(self) -> list:
        """Преобразование связного списка в обычный список. O(n)"""
        elements = []
        current = self._first
        
        while current is not None:
            elements.append(current.value)
            current = current.next
            
        return elements
    
    def is_empty(self) -> bool:
        """Проверка на отсутствие элементов. O(1)"""
        return self._first is None
    
    def size(self) -> int:
        """Подсчёт количества элементов. O(n)"""
        counter = 0
        current = self._first
        
        while current:
            counter += 1
            current = current.next
            
        return counter


def benchmark_prepend_operations(sizes: list[int]) -> tuple[list[float], list[float]]:
    """Сравнительный анализ добавления элементов в начало."""
    standard_list_durations = []
    custom_list_durations = []

    for operation_count in sizes:
        # Бенчмарк для стандартного списка
        test_list = [x for x in range(1000)]
        standard_time = timeit.Timer(
            stmt="test_list.insert(0, 1)",
            globals={'test_list': test_list}
        ).timeit(number=operation_count)
        standard_list_durations.append(standard_time)

        # Бенчмарк для собственной реализации
        custom_list = LinkedList()
        [custom_list.insert_at_end(x) for x in range(1000)]
        custom_time = timeit.Timer(
            stmt="custom_list.insert_at_start(1)",
            globals={'custom_list': custom_list}
        ).timeit(number=operation_count)
        custom_list_durations.append(custom_time)

    return standard_list_durations, custom_list_durations


def benchmark_queue_operations(sizes: list[int]) -> tuple[list[float], list[float]]:
    """Сравнительный анализ операций извлечения из начала."""
    deque_durations = []
    list_durations = []

    for operation_count in sizes:
        # Бенчмарк для deque
        test_deque = deque(x for x in range(operation_count * 2))
        deque_time = timeit.Timer(
            stmt="test_deque.popleft() if test_deque else None",
            globals={'test_deque': test_deque}
        ).timeit(number=operation_count)
        deque_durations.append(deque_time)

        # Бенчмарк для стандартного списка
        test_list = [x for x in range(operation_count * 2)]
        list_time = timeit.Timer(
            stmt="test_list.pop(0) if test_list else None",
            globals={'test_list': test_list}
        ).timeit(number=operation_count)
        list_durations.append(list_time)

    return deque_durations, list_durations


def visualize_prepend_comparison(sizes: list[int], 
                               standard_times: list[float], 
                               custom_times: list[float]) -> None:
    """Визуализация результатов сравнения добавления в начало."""
    figure, axes = plt.subplots(figsize=(10, 6))
    
    axes.plot(sizes, standard_times, color='red', marker='o', 
             linewidth=2, markersize=6, label='list.insert(0)')
    axes.plot(sizes, custom_times, color='blue', marker='s', 
             linewidth=2, markersize=6, label='LinkedList.insert_at_start')
    
    axes.set_xlabel('Количество операций')
    axes.set_ylabel('Затраченное время (секунды)')
    axes.set_title('Сравнение производительности: добавление в начало')
    axes.grid(visible=True, linestyle='--', alpha=0.7)
    axes.legend()
    
    figure.savefig('prepend_comparison.png', dpi=300, 
                  bbox_inches='tight', facecolor='white')
    plt.close(figure)


def visualize_queue_comparison(sizes: list[int],
                             deque_times: list[float],
                             list_times: list[float]) -> None:
    """Визуализация результатов сравнения операций очереди."""
    figure, axes = plt.subplots(figsize=(10, 6))
    
    axes.plot(sizes, list_times, color='red', marker='o',
             linewidth=2, markersize=6, label='list.pop(0)')
    axes.plot(sizes, deque_times, color='blue', marker='s',
             linewidth=2, markersize=6, label='deque.popleft()')
    
    axes.set_xlabel('Количество операций')
    axes.set_ylabel('Затраченное время (секунды)')
    axes.set_title('Сравнение производительности: извлечение из начала')
    axes.grid(visible=True, linestyle='--', alpha=0.7)
    axes.legend()
    
    figure.savefig('queue_comparison.png', dpi=300,
                  bbox_inches='tight', facecolor='white')
    plt.close(figure)


def execute_benchmarks() -> None:
    """Основная функция выполнения бенчмарков и визуализации."""
    test_sizes = [100, 500, 1000, 2000, 5000]

    print("Выполнение бенчмарков добавления в начало...")
    list_results, linked_list_results = benchmark_prepend_operations(test_sizes)
    
    print("Выполнение бенчмарков операций очереди...")
    deque_results, list_pop_results = benchmark_queue_operations(test_sizes)

    print("Создание графиков...")
    visualize_prepend_comparison(test_sizes, list_results, linked_list_results)
    visualize_queue_comparison(test_sizes, deque_results, list_pop_results)

    system_specs = """
Технические характеристики системы:
- Процессор: AMD Ryzen 5 5600G @ 4.3GHz
- Оперативная память: 16 GB DDR4
- Операционная система: Windows 11
- Версия Python: 3.13
"""
    print(system_specs)
    print("Результаты сохранены в файлы:")
    print("- prepend_comparison.png")
    print("- queue_comparison.png")


if __name__ == "__main__":
    execute_benchmarks()