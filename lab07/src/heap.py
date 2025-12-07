"""
Реализация структуры данных "Куча" (Heap).
Представлены MinHeap, MaxHeap и обобщенная Heap с измененным синтаксисом.
"""

class Heap:
    """Обобщенная куча с поддержкой min-heap и max-heap режимов."""
    
    def __init__(self, *, min_heap=True):
        """
        Создание кучи.
        
        Параметры:
            min_heap (bool): True для минимальной кучи, False для максимальной.
            
        Сложность: O(1)
        """
        self._data = []
        self._is_min_heap = min_heap
    
    def __len__(self):
        """Количество элементов в куче. O(1)"""
        return len(self._data)
    
    def __bool__(self):
        """Проверка на пустоту. O(1)"""
        return bool(self._data)
    
    def __str__(self):
        """Строковое представление."""
        return f"Heap(data={self._data}, min_heap={self._is_min_heap})"
    
    def __repr__(self):
        """Представление для отладки."""
        return f"Heap(min_heap={self._is_min_heap}, size={len(self)})"
    
    def _should_swap(self, child, parent):
        """
        Определяет необходимость обмена элементов.
        
        Параметры:
            child: Дочерний элемент
            parent: Родительский элемент
            
        Возвращает:
            bool: True если порядок нарушен согласно типу кучи.
            
        Сложность: O(1)
        """
        if self._is_min_heap:
            return child < parent
        return child > parent
    
    def _move_up(self, idx):
        """
        Перемещение элемента вверх по куче.
        
        Параметры:
            idx (int): Индекс перемещаемого элемента.
            
        Сложность: O(log n)
        """
        current_idx = idx
        
        while current_idx > 0:
            parent_idx = (current_idx - 1) // 2
            
            if not self._should_swap(self._data[current_idx], self._data[parent_idx]):
                break
            
            # Обмен элементов
            self._data[current_idx], self._data[parent_idx] = \
                self._data[parent_idx], self._data[current_idx]
            
            current_idx = parent_idx
    
    def _move_down(self, idx):
        """
        Перемещение элемента вниз по куче.
        
        Параметры:
            idx (int): Индекс перемещаемого элемента.
            
        Сложность: O(log n)
        """
        current_idx = idx
        heap_size = len(self)
        
        while True:
            left_idx = 2 * current_idx + 1
            right_idx = 2 * current_idx + 2
            target_idx = current_idx
            
            # Поиск целевого элемента для обмена
            for check_idx in (left_idx, right_idx):
                if (check_idx < heap_size and 
                    self._should_swap(self._data[check_idx], self._data[target_idx])):
                    target_idx = check_idx
            
            if target_idx == current_idx:
                break
            
            # Обмен элементов
            self._data[current_idx], self._data[target_idx] = \
                self._data[target_idx], self._data[current_idx]
            
            current_idx = target_idx
    
    def push(self, value):
        """
        Добавление элемента в кучу.
        
        Параметры:
            value: Добавляемое значение.
            
        Сложность: O(log n)
        """
        self._data.append(value)
        self._move_up(len(self._data) - 1)
    
    insert = push  # Альтернативное имя метода
    
    def pop(self):
        """
        Удаление и возврат корневого элемента.
        
        Возвращает:
            Значение корневого элемента.
            
        Исключения:
            IndexError: При попытке извлечения из пустой кучи.
            
        Сложность: O(log n)
        """
        if not self._data:
            raise IndexError("Извлечение из пустой кучи невозможно")
        
        result = self._data[0]
        
        if len(self._data) == 1:
            self._data.pop()
        else:
            self._data[0] = self._data.pop()
            self._move_down(0)
        
        return result
    
    extract = pop  # Альтернативное имя метода
    
    def top(self):
        """
        Получение корневого элемента без удаления.
        
        Возвращает:
            Значение корневого элемента.
            
        Исключения:
            IndexError: При обращении к пустой куче.
            
        Сложность: O(1)
        """
        if not self._data:
            raise IndexError("Куча пуста")
        return self._data[0]
    
    peek = top  # Альтернативное имя метода
    
    def create_from(self, collection):
        """
        Построение кучи из коллекции.
        
        Параметры:
            collection: Итерируемая коллекция элементов.
            
        Сложность: O(n)
        """
        self._data = list(collection)
        
        # Просеивание всех нелистовых узлов
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self._move_down(i)
    
    def rebuild(self):
        """Восстановление свойств кучи. O(n)"""
        self.create_from(self._data)
    
    def validate(self):
        """
        Проверка корректности структуры кучи.
        
        Возвращает:
            bool: True если свойства кучи соблюдены.
            
        Сложность: O(n)
        """
        heap_size = len(self._data)
        
        for i in range(heap_size):
            left = 2 * i + 1
            right = 2 * i + 2
            
            # Проверка левого потомка
            if left < heap_size:
                if self._should_swap(self._data[left], self._data[i]):
                    return False
            
            # Проверка правого потомка
            if right < heap_size:
                if self._should_swap(self._data[right], self._data[i]):
                    return False
        
        return True
    
    def clear(self):
        """Очистка кучи. O(1)"""
        self._data.clear()
    
    @property
    def items(self):
        """Получение всех элементов кучи (только для чтения). O(1)"""
        return tuple(self._data)


class MinHeap(Heap):
    """Специализированная минимальная куча."""
    
    def __init__(self):
        """Создание минимальной кучи."""
        super().__init__(min_heap=True)


class MaxHeap(Heap):
    """Специализированная максимальная куча."""
    
    def __init__(self):
        """Создание максимальной кучи."""
        super().__init__(min_heap=False)