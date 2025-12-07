"""
Модуль графического представления структуры данных "Куча" в виде древовидной диаграммы.
"""

from typing import Any, List, Optional
import sys


def represent_heap_as_tree(heap_structure, 
                          node_index: int = 0, 
                          branch_prefix: str = "", 
                          is_left_child: bool = True) -> str:
    """
    Рекурсивное формирование текстового представления кучи в виде дерева.
    
    Параметры:
        heap_structure: Структура кучи с атрибутом .data или .heap
        node_index: Индекс текущего узла в массиве кучи
        branch_prefix: Строка-префикс для форматирования ветвей
        is_left_child: Флаг, указывающий является ли узел левым потомком
        
    Возвращает:
        Многострочное строковое представление дерева
    """
    # Получаем доступ к данным кучи
    try:
        heap_data = heap_structure.data  # Для нового синтаксиса
    except AttributeError:
        heap_data = heap_structure.heap  # Для обратной совместимости
    
    # Если индекс выходит за границы массива
    if node_index >= len(heap_data):
        return ""
    
    representation = ""
    
    # Обрабатываем правого потомка (если существует)
    right_child_idx = 2 * node_index + 2
    if right_child_idx < len(heap_data):
        representation += represent_heap_as_tree(
            heap_structure,
            right_child_idx,
            branch_prefix + ("│   " if is_left_child else "    "),
            False
        )
    
    # Формируем строку текущего узла
    node_connector = "└── " if is_left_child else "┌── "
    current_line = branch_prefix + node_connector + str(heap_data[node_index])
    representation += current_line + "\n"
    
    # Обрабатываем левого потомка (если существует)
    left_child_idx = 2 * node_index + 1
    if left_child_idx < len(heap_data):
        representation += represent_heap_as_tree(
            heap_structure,
            left_child_idx,
            branch_prefix + ("    " if is_left_child else "│   "),
            True
        )
    
    return representation


def display_heap_tree(heap_structure, 
                     title: Optional[str] = None) -> None:
    """
    Отображение структуры кучи в виде дерева с заголовком.
    
    Параметры:
        heap_structure: Объект кучи для визуализации
        title: Заголовок для вывода (если None, используется стандартный)
    """
    # Получаем данные кучи
    try:
        heap_data = heap_structure.data
    except AttributeError:
        heap_data = heap_structure.heap
    
    if not heap_data:
        print("╭─────────────────────╮")
        print("│     ПУСТАЯ КУЧА     │")
        print("╰─────────────────────╯")
        return
    
    if title:
        print(f"\n{title}:")
    else:
        print("\n▌ Древовидная структура кучи ▌")
        print("─" * 40)
    
    print(represent_heap_as_tree(heap_structure))


def visualize_array_as_heap(data_array: List[Any]) -> None:
    """
    Визуализация произвольного массива в виде кучи.
    
    Параметры:
        data_array: Массив элементов для представления
    """
    # Вспомогательный класс для представления массива как кучи
    class ArrayHeapWrapper:
        __slots__ = ('_elements',)
        
        def __init__(self, elements: List[Any]):
            self._elements = elements
        
        @property
        def data(self):
            return self._elements
        
        @property
        def heap(self):
            return self._elements
    
    print(f"\nВизуализация массива как кучи (размер: {len(data_array)}):")
    print("=" * 50)
    
    if not data_array:
        print("Массив пуст")
        return
    
    wrapper = ArrayHeapWrapper(data_array)
    display_heap_tree(wrapper)


def create_demo_heap():
    """Создание и демонстрация работы с минимальной кучей."""
    try:
        from heap import MinHeap
        heap_demo = MinHeap()
    except ImportError:
        # Альтернативная реализация для демонстрации
        class SimpleMinHeap:
            def __init__(self):
                self.data = []
            
            def add(self, value):
                self.data.append(value)
                # Упрощенное восстановление свойств кучи
                idx = len(self.data) - 1
                while idx > 0:
                    parent = (idx - 1) // 2
                    if self.data[idx] < self.data[parent]:
                        self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
                        idx = parent
                    else:
                        break
            
            def remove_min(self):
                if not self.data:
                    raise IndexError("Куча пуста")
                
                min_val = self.data[0]
                last_val = self.data.pop()
                
                if self.data:
                    self.data[0] = last_val
                    idx = 0
                    n = len(self.data)
                    
                    while True:
                        left = 2 * idx + 1
                        right = 2 * idx + 2
                        smallest = idx
                        
                        if left < n and self.data[left] < self.data[smallest]:
                            smallest = left
                        if right < n and self.data[right] < self.data[smallest]:
                            smallest = right
                        
                        if smallest != idx:
                            self.data[idx], self.data[smallest] = self.data[smallest], self.data[idx]
                            idx = smallest
                        else:
                            break
                
                return min_val
        
        heap_demo = SimpleMinHeap()
    
    return heap_demo


def demonstrate_heap_visualization():
    """
    Интерактивная демонстрация визуализации операций с кучей.
    """
    print("╔═══════════════════════════════════════════════════════╗")
    print("║    ИНТЕРАКТИВНАЯ ВИЗУАЛИЗАЦИЯ СТРУКТУРЫ КУЧИ         ║")
    print("╚═══════════════════════════════════════════════════════╝")
    
    heap_instance = create_demo_heap()
    
    # Определяем последовательность операций для демонстрации
    demonstration_sequence = [
        ("Начальное состояние (пустая куча)", None, None),
        ("Добавление элемента 10", "add", 10),
        ("Добавление элемента 5", "add", 5),
        ("Добавление элемента 15", "add", 15),
        ("Добавление элемента 3", "add", 3),
        ("Добавление элемента 7", "add", 7),
        ("Добавление элемента 12", "add", 12),
        ("Добавление элемента 1", "add", 1),
        ("Удаление минимального элемента", "remove", None),
        ("Удаление минимального элемента", "remove", None),
        ("Добавление элемента 4", "add", 4),
        ("Добавление элемента 8", "add", 8),
        ("Финальная структура", None, None),
    ]
    
    step_counter = 1
    
    for description, operation, value in demonstration_sequence:
        print(f"\n{'═' * 60}")
        print(f"Шаг {step_counter}: {description}")
        print(f"{'─' * 60}")
        
        if operation == "add" and value is not None:
            heap_instance.add(value)
            print(f"✓ Добавлен элемент: {value}")
        elif operation == "remove":
            try:
                removed = heap_instance.remove_min()
                print(f"✓ Удален элемент: {removed}")
            except IndexError:
                print("✗ Куча пуста, удаление невозможно")
        
        # Отображаем текущее состояние кучи
        display_heap_tree(heap_instance)
        
        # Показываем содержимое массива
        try:
            heap_array = heap_instance.data
        except AttributeError:
            heap_array = heap_instance.heap
        
        print(f"\nМассив кучи: {heap_array}")
        step_counter += 1
        
        # Пауза для удобства восприятия
        if step_counter < len(demonstration_sequence):
            input("\nНажмите Enter для продолжения...")
    
    print(f"\n{'═' * 60}")
    print("Демонстрация завершена!")
    print(f"Итоговый размер кучи: {len(heap_instance.data)} элементов")


def export_heap_to_file(heap_structure, filename: str) -> None:
    """
    Экспорт визуализации кучи в текстовый файл.
    
    Параметры:
        heap_structure: Объект кучи
        filename: Имя файла для сохранения
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Визуализация структуры кучи\n")
            file.write("=" * 50 + "\n\n")
            
            tree_representation = represent_heap_as_tree(heap_structure)
            file.write(tree_representation)
            
            # Добавляем информацию о данных
            try:
                heap_data = heap_structure.data
            except AttributeError:
                heap_data = heap_structure.heap
            
            file.write(f"\n\nДанные кучи (массив): {heap_data}\n")
            file.write(f"Количество элементов: {len(heap_data)}\n")
            
            if heap_data:
                file.write(f"Корневой элемент: {heap_data[0]}\n")
        
        print(f"✓ Визуализация сохранена в файл: {filename}")
    except Exception as e:
        print(f"✗ Ошибка при сохранении в файл: {e}")


def run_visualization_examples():
    """Запуск примеров визуализации различных куч."""
    print("\n" + "=" * 70)
    print("ПРИМЕРЫ ВИЗУАЛИЗАЦИИ РАЗЛИЧНЫХ СТРУКТУР")
    print("=" * 70)
    
    # Пример 1: Визуализация произвольного массива
    print("\nПример 1: Визуализация массива [7, 3, 10, 1, 6, 14, 4]")
    visualize_array_as_heap([7, 3, 10, 1, 6, 14, 4])
    
    # Пример 2: Построение и визуализация минимальной кучи
    print("\n" + "=" * 70)
    print("\nПример 2: Построение минимальной кучи из массива")
    
    demo_heap = create_demo_heap()
    initial_data = [20, 15, 30, 5, 10, 25, 35]
    
    for value in initial_data:
        demo_heap.add(value)
    
    display_heap_tree(demo_heap, "Минимальная куча после добавления всех элементов")
    
    # Пример 3: Визуализация после нескольких удалений
    print("\n" + "=" * 70)
    print("\nПример 3: Визуализация после удаления двух элементов")
    
    for _ in range(2):
        try:
            removed = demo_heap.remove_min()
            print(f"Удален элемент: {removed}")
        except IndexError:
            break
    
    display_heap_tree(demo_heap, "Куча после удаления двух минимальных элементов")
    
    # Пример 4: Экспорт в файл
    print("\n" + "=" * 70)
    print("\nПример 4: Экспорт визуализации в файл")
    
    export_heap_to_file(demo_heap, "heap_visualization.txt")
    
    print("\n" + "=" * 70)
    print("Все примеры выполнены успешно!")


def interactive_heap_visualization():
    """Интерактивный режим визуализации кучи."""
    import getpass
    
    print("\n" + "═" * 70)
    print("ИНТЕРАКТИВНЫЙ РЕЖИМ ВИЗУАЛИЗАЦИИ КУЧИ")
    print("═" * 70)
    
    heap = create_demo_heap()
    
    while True:
        print("\nТекущее состояние кучи:")
        display_heap_tree(heap)
        
        print("\nДоступные команды:")
        print("  1. Добавить элемент")
        print("  2. Удалить минимальный элемент")
        print("  3. Очистить кучу")
        print("  4. Загрузить массив")
        print("  5. Экспорт в файл")
        print("  6. Выход")
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == '1':
            try:
                value = int(input("Введите целое число для добавления: "))
                heap.add(value)
                print(f"✓ Добавлен элемент: {value}")
            except ValueError:
                print("✗ Некорректный ввод. Введите целое число.")
        
        elif choice == '2':
            try:
                removed = heap.remove_min()
                print(f"✓ Удален элемент: {removed}")
            except IndexError:
                print("✗ Куча пуста, удаление невозможно")
        
        elif choice == '3':
            heap.data.clear()
            print("✓ Куча очищена")
        
        elif choice == '4':
            input_str = input("Введите элементы массива через пробел: ")
            try:
                new_data = list(map(int, input_str.split()))
                heap.data.clear()
                for val in new_data:
                    heap.add(val)
                print(f"✓ Загружено {len(new_data)} элементов")
            except ValueError:
                print("✗ Некорректный ввод. Используйте целые числа.")
        
        elif choice == '5':
            filename = input("Введите имя файла для экспорта: ").strip()
            if not filename:
                filename = "heap_visualization.txt"
            export_heap_to_file(heap, filename)
        
        elif choice == '6':
            print("Выход из интерактивного режима...")
            break
        
        else:
            print("✗ Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    # Определяем режим работы
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "demo"
    
    # Запускаем выбранный режим
    if mode == "demo":
        demonstrate_heap_visualization()
    elif mode == "examples":
        run_visualization_examples()
    elif mode == "interactive":
        interactive_heap_visualization()
    else:
        print(f"Доступные режимы: demo, examples, interactive")
        print(f"Запуск: python {sys.argv[0]} [режим]")
        
        # Запускаем демонстрацию по умолчанию
        print("\nЗапуск демонстрационного режима...")
        demonstrate_heap_visualization()