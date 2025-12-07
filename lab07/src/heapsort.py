"""
Реализация алгоритма сортировки кучей (Heapsort).
Представлены версии с выделением памяти и in-place реализация.
"""

def heap_sort_extra(array):
    """
    Сортировка с использованием дополнительной памяти.
    
    Параметры:
        array: Исходный массив данных
        
    Возвращает:
        Отсортированный массив (по возрастанию)
        
    Сложность: O(n log n)
    """
    # Создаем кучу как список
    heap_data = []
    
    # Построение минимальной кучи
    for element in array:
        # Добавляем элемент в конец
        heap_data.append(element)
        
        # Восстанавливаем свойства кучи
        current_index = len(heap_data) - 1
        
        # Просеивание вверх
        while current_index > 0:
            parent_index = (current_index - 1) // 2
            
            # Если порядок правильный, останавливаемся
            if heap_data[current_index] >= heap_data[parent_index]:
                break
                
            # Меняем местами с родителем
            heap_data[current_index], heap_data[parent_index] = \
                heap_data[parent_index], heap_data[current_index]
                
            current_index = parent_index
    
    # Извлечение элементов из кучи
    sorted_result = []
    
    while heap_data:
        # Получаем минимальный элемент
        min_element = heap_data[0]
        
        # Заменяем корень последним элементом
        if len(heap_data) > 1:
            heap_data[0] = heap_data.pop()
            
            # Восстанавливаем свойства кучи
            current_index = 0
            heap_size = len(heap_data)
            
            while True:
                left_child = 2 * current_index + 1
                right_child = 2 * current_index + 2
                min_index = current_index
                
                # Поиск минимального среди текущего узла и его потомков
                if (left_child < heap_size and 
                    heap_data[left_child] < heap_data[min_index]):
                    min_index = left_child
                    
                if (right_child < heap_size and 
                    heap_data[right_child] < heap_data[min_index]):
                    min_index = right_child
                
                # Если порядок правильный, останавливаемся
                if min_index == current_index:
                    break
                    
                # Меняем местами с минимальным потомком
                heap_data[current_index], heap_data[min_index] = \
                    heap_data[min_index], heap_data[current_index]
                    
                current_index = min_index
        else:
            heap_data.pop()
        
        sorted_result.append(min_element)
    
    return sorted_result


def heap_sort_inplace(collection):
    """
    Сортировка на месте без выделения дополнительной памяти.
    
    Параметры:
        collection: Список для сортировки (изменяется на месте)
        
    Возвращает:
        Отсортированный список
        
    Сложность: O(n log n)
    Память: O(1)
    """
    
    def heapify_down(data, node_index, boundary):
        """
        Просеивание элемента вниз в поддереве.
        
        Параметры:
            data: Массив данных
            node_index: Индекс корня поддерева
            boundary: Граница кучи
        """
        current = node_index
        
        while True:
            # Индекс большего потомка
            left_child = 2 * current + 1
            largest_index = current
            
            # Проверяем левого потомка
            if left_child <= boundary and data[left_child] > data[largest_index]:
                largest_index = left_child
            
            # Проверяем правого потомка
            right_child = left_child + 1
            if (right_child <= boundary and 
                data[right_child] > data[largest_index]):
                largest_index = right_child
            
            # Если текущий элемент уже на своем месте
            if largest_index == current:
                return
            
            # Обмен с большим потомком
            data[current], data[largest_index] = data[largest_index], data[current]
            current = largest_index
    
    size = len(collection)
    
    if size <= 1:
        return collection
    
    # Фаза 1: Построение максимальной кучи
    # Обрабатываем все нелистовые узлы
    for i in range(size // 2 - 1, -1, -1):
        heapify_down(collection, i, size - 1)
    
    # Фаза 2: Сортировка
    for boundary in range(size - 1, 0, -1):
        # Перемещаем максимальный элемент в конец
        collection[0], collection[boundary] = collection[boundary], collection[0]
        
        # Восстанавливаем свойства кучи в оставшейся части
        heapify_down(collection, 0, boundary - 1)
    
    return collection


def heap_sort_with_class(sequence):
    """
    Сортировка с использованием класса Heap.
    
    Параметры:
        sequence: Последовательность для сортировки
        
    Возвращает:
        Отсортированная последовательность
        
    Сложность: O(n log n)
    """
    try:
        # Импорт в локальной области видимости
        from heap import MinHeap
        
        # Создаем кучу
        heap = MinHeap()
        
        # Построение кучи из массива
        heap.create_from(sequence)
        
        # Извлечение элементов в отсортированном порядке
        sorted_sequence = []
        
        while heap:
            sorted_sequence.append(heap.pop())
        
        return sorted_sequence
        
    except ImportError:
        # Фолбэк на стандартную реализацию
        return heap_sort_extra(list(sequence))


# Альтернативные имена функций для обратной совместимости
heapsort = heap_sort_extra
heapsort_inplace = heap_sort_inplace
heap_sort_min = heap_sort_with_class


def test_sort_functions():
    """
    Тестирование всех функций сортировки.
    """
    test_cases = [
        [],
        [1],
        [5, 2, 8, 1, 9],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    ]
    
    for test_data in test_cases:
        original = test_data.copy()
        
        # Тестируем все реализации
        result1 = heap_sort_extra(original)
        result2 = heap_sort_inplace(original.copy())
        result3 = heap_sort_with_class(original)
        
        # Проверяем корректность
        expected = sorted(original)
        
        assert result1 == expected, f"Ошибка в heap_sort_extra: {original}"
        assert result2 == expected, f"Ошибка в heap_sort_inplace: {original}"
        assert result3 == expected, f"Ошибка в heap_sort_with_class: {original}"
        
        print(f"✓ Тест пройден: {original} → {result1}")


if __name__ == "__main__":
    # Пример использования
    sample_data = [9, 3, 7, 1, 5, 8, 2, 6, 4]
    
    print("Исходный массив:", sample_data)
    print()
    
    # Тестируем все реализации
    print("1. С дополнительной памятью:")
    result1 = heap_sort_extra(sample_data.copy())
    print(f"   Результат: {result1}")
    print()
    
    print("2. In-place сортировка:")
    data_copy = sample_data.copy()
    result2 = heap_sort_inplace(data_copy)
    print(f"   Результат: {result2}")
    print(f"   Исходный массив изменен: {data_copy}")
    print()
    
    print("3. С использованием класса Heap:")
    result3 = heap_sort_with_class(sample_data.copy())
    print(f"   Результат: {result3}")
    
    # Запуск тестов
    print("\n" + "="*50)
    print("Запуск тестов...")
    test_sort_functions()
    print("Все тесты пройдены успешно!")