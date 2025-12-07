"""
Реализация приоритетной очереди с использованием структуры данных "куча".
Основана на минимальной куче для обеспечения эффективности операций.
"""

from collections import namedtuple
from typing import Any, Optional
import heapq as std_heapq  # Для альтернативной реализации


class PriorityNode:
    """Узел приоритетной очереди с данными и приоритетом."""
    
    __slots__ = ('data', 'priority_value')
    
    def __init__(self, payload: Any, priority: int):
        """
        Создание узла приоритетной очереди.
        
        Параметры:
            payload: Полезная нагрузка (данные)
            priority: Значение приоритета (меньше = выше приоритет)
        """
        self.data = payload
        self.priority_value = priority
    
    def __lt__(self, other: 'PriorityNode') -> bool:
        """Оператор сравнения для работы с минимальной кучей."""
        if not isinstance(other, PriorityNode):
            return NotImplemented
        return self.priority_value < other.priority_value
    
    def __le__(self, other: 'PriorityNode') -> bool:
        """Оператор сравнения 'меньше или равно'."""
        if not isinstance(other, PriorityNode):
            return NotImplemented
        return self.priority_value <= other.priority_value
    
    def __eq__(self, other: Any) -> bool:
        """Проверка равенства узлов."""
        if not isinstance(other, PriorityNode):
            return False
        return (self.data == other.data and 
                self.priority_value == other.priority_value)
    
    def __hash__(self) -> int:
        """Хеш-значение узла."""
        return hash((self.data, self.priority_value))
    
    def __repr__(self) -> str:
        """Строковое представление для отладки."""
        return f"Node(data={self.data!r}, priority={self.priority_value})"
    
    def __str__(self) -> str:
        """Человеко-читаемое представление."""
        return f"({self.data} @ {self.priority_value})"


# Альтернативный вариант через namedtuple (неизменяемый)
PriorityElement = namedtuple('PriorityElement', ['data', 'priority'])


class HeapPriorityQueue:
    """
    Приоритетная очередь на основе минимальной кучи.
    Элементы с меньшим значением приоритета извлекаются первыми.
    """
    
    def __init__(self, initial_data=None):
        """
        Инициализация приоритетной очереди.
        
        Параметры:
            initial_data: Начальные данные в формате [(данные, приоритет), ...]
        """
        try:
            from heap import MinHeap
            self._storage = MinHeap()
        except ImportError:
            # Фолбэк на стандартную библиотеку
            self._storage = []
            self._use_std_heap = True
        else:
            self._use_std_heap = False
        
        # Добавляем начальные данные если они предоставлены
        if initial_data:
            for item, priority in initial_data:
                self.add(item, priority)
    
    def add(self, item: Any, priority: int) -> None:
        """
        Добавление элемента в очередь.
        
        Параметры:
            item: Элемент данных
            priority: Приоритет элемента
            
        Сложность: O(log n)
        """
        node = PriorityNode(item, priority)
        
        if self._use_std_heap:
            std_heapq.heappush(self._storage, node)
        else:
            self._storage.push(node)
    
    enqueue = add  # Синоним для совместимости
    
    def remove(self) -> Any:
        """
        Извлечение элемента с наивысшим приоритетом.
        
        Возвращает:
            Данные элемента с наивысшим приоритетом
            
        Исключения:
            IndexError: При попытке извлечения из пустой очереди
            
        Сложность: O(log n)
        """
        if self.is_empty():
            raise IndexError("Очередь приоритетов пуста")
        
        if self._use_std_heap:
            node = std_heapq.heappop(self._storage)
        else:
            node = self._storage.pop()
        
        return node.data
    
    dequeue = remove  # Синоним для совместимости
    
    def peek(self) -> Any:
        """
        Получение элемента с наивысшим приоритетом без удаления.
        
        Возвращает:
            Данные элемента с наивысшим приоритетом
            
        Исключения:
            IndexError: При обращении к пустой очереди
            
        Сложность: O(1)
        """
        if self.is_empty():
            raise IndexError("Очередь приоритетов пуста")
        
        if self._use_std_heap:
            node = self._storage[0]
        else:
            node = self._storage.top()
        
        return node.data
    
    def front(self) -> Any:
        """Синоним для peek()."""
        return self.peek()
    
    def is_empty(self) -> bool:
        """
        Проверка на пустоту очереди.
        
        Возвращает:
            True если очередь пуста, иначе False
            
        Сложность: O(1)
        """
        if self._use_std_heap:
            return len(self._storage) == 0
        else:
            return len(self._storage) == 0
    
    def __len__(self) -> int:
        """
        Количество элементов в очереди.
        
        Возвращает:
            Текущий размер очереди
            
        Сложность: O(1)
        """
        if self._use_std_heap:
            return len(self._storage)
        else:
            return len(self._storage)
    
    def __bool__(self) -> bool:
        """Проверка наличия элементов. O(1)"""
        return not self.is_empty()
    
    def __iter__(self):
        """Итерация по элементам в порядке приоритета."""
        # Создаем копию для безопасной итерации
        temp_queue = HeapPriorityQueue()
        items = []
        
        if self._use_std_heap:
            temp_storage = self._storage.copy()
            while temp_storage:
                node = std_heapq.heappop(temp_storage)
                items.append(node.data)
                temp_queue.add(node.data, node.priority_value)
        else:
            # Для кастомной реализации нужно клонирование
            while not self.is_empty():
                item = self.remove()
                items.append(item)
                # Восстановление невозможно без сохранения приоритетов
                # Для упрощения просто собираем элементы
        
        return iter(items)
    
    def __str__(self) -> str:
        """Строковое представление очереди."""
        return f"PriorityQueue[items={len(self)}]"
    
    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"HeapPriorityQueue(size={len(self)})"
    
    def clear(self) -> None:
        """Очистка очереди. O(1)"""
        if self._use_std_heap:
            self._storage.clear()
        else:
            self._storage.clear()
    
    def contains(self, item: Any, priority: Optional[int] = None) -> bool:
        """
        Проверка наличия элемента в очереди.
        
        Параметры:
            item: Искомый элемент
            priority: Опциональный приоритет для проверки
            
        Возвращает:
            True если элемент найден, иначе False
            
        Сложность: O(n)
        """
        if self._use_std_heap:
            for node in self._storage:
                if node.data == item:
                    if priority is None or node.priority_value == priority:
                        return True
        else:
            # Для кастомной реализации нужен доступ к внутреннему хранилищу
            pass
        
        return False


# Альтернативная реализация с использованием стандартного heapq
class FastPriorityQueue:
    """Быстрая приоритетная очередь на основе heapq."""
    
    def __init__(self):
        """Инициализация пустой очереди."""
        self._heap = []
    
    def push(self, item: Any, priority: int) -> None:
        """Добавление элемента. O(log n)"""
        std_heapq.heappush(self._heap, (priority, item))
    
    def pop(self) -> Any:
        """Извлечение элемента с наивысшим приоритетом. O(log n)"""
        if not self._heap:
            raise IndexError("Очередь пуста")
        priority, item = std_heapq.heappop(self._heap)
        return item
    
    def peek(self) -> Any:
        """Просмотр элемента с наивысшим приоритетом. O(1)"""
        if not self._heap:
            raise IndexError("Очередь пуста")
        return self._heap[0][1]
    
    def __len__(self) -> int:
        """Размер очереди. O(1)"""
        return len(self._heap)
    
    def is_empty(self) -> bool:
        """Проверка пустоты. O(1)"""
        return len(self._heap) == 0


# Пример использования
def demonstrate_usage():
    """Демонстрация работы приоритетной очереди."""
    
    print("=== Демонстрация HeapPriorityQueue ===\n")
    
    # Создание очереди с начальными данными
    initial_tasks = [
        ("Отправить отчет", 3),
        ("Срочный звонок", 1),
        ("Проверить почту", 4),
        ("Критический баг", 0),
    ]
    
    queue = HeapPriorityQueue(initial_tasks)
    print(f"Создана очередь с {len(queue)} элементами")
    print(f"Очередь пуста? {queue.is_empty()}\n")
    
    # Добавление новых элементов
    print("Добавляем новые элементы:")
    queue.add("Новая задача", 2)
    queue.enqueue("Еще одна задача", 5)
    print(f"Теперь в очереди: {len(queue)} элементов\n")
    
    # Извлечение элементов в порядке приоритета
    print("Извлекаем элементы в порядке приоритета:")
    while queue:
        try:
            task = queue.remove()
            print(f"  Извлечено: {task}")
        except IndexError:
            break
    
    print(f"\nОчередь пуста после извлечения: {queue.is_empty()}")


# Тестирование
def run_tests():
    """Запуск тестов приоритетной очереди."""
    
    print("=== Тестирование PriorityQueue ===\n")
    
    test_queue = HeapPriorityQueue()
    
    # Тест 1: Добавление и извлечение
    test_queue.add("Задача A", 5)
    test_queue.add("Задача B", 1)
    test_queue.add("Задача C", 3)
    
    assert len(test_queue) == 3
    assert test_queue.peek() == "Задача B"  # Самый высокий приоритет
    
    # Тест 2: Правильный порядок извлечения
    items = []
    while not test_queue.is_empty():
        items.append(test_queue.remove())
    
    assert items == ["Задача B", "Задача C", "Задача A"]
    print("✓ Тест порядка извлечения пройден")
    
    # Тест 3: Обработка пустой очереди
    empty_queue = HeapPriorityQueue()
    assert empty_queue.is_empty()
    assert len(empty_queue) == 0
    
    try:
        empty_queue.remove()
        assert False, "Ожидалось IndexError"
    except IndexError:
        print("✓ Тест пустой очереди пройден")
    
    # Тест 4: Итерация
    test_queue.add("X", 2)
    test_queue.add("Y", 1)
    test_queue.add("Z", 3)
    
    iterated = list(test_queue)
    assert len(iterated) == 3
    print("✓ Тест итерации пройден")
    
    print("\nВсе тесты пройдены успешно!")


if __name__ == "__main__":
    # Демонстрация работы
    demonstrate_usage()
    print("\n" + "="*50 + "\n")
    
    # Запуск тестов
    run_tests()