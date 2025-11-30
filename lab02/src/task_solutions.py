"""Практическое применение структур данных для решения задач."""
from collections import deque


class ListNode:
    """Узел связного списка."""
    
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    """Реализация односвязного списка."""
    
    def __init__(self):
        self._first = None
        self._last = None
    
    def insert_at_start(self, value) -> None:
        """Добавление элемента в начало списка."""
        new_element = ListNode(value)
        
        if not self._first:
            self._first = self._last = new_element
        else:
            new_element.next = self._first
            self._first = new_element
    
    def insert_at_end(self, value) -> None:
        """Добавление элемента в конец списка."""
        new_element = ListNode(value)
        
        if not self._last:
            self._first = self._last = new_element
        else:
            self._last.next = new_element
            self._last = new_element
    
    def delete_from_start(self):
        """Извлечение элемента из начала списка."""
        if self._first is None:
            return None
        
        extracted_value = self._first.value
        self._first = self._first.next
        
        if self._first is None:
            self._last = None
            
        return extracted_value
    
    def traversal(self) -> list:
        """Преобразование связного списка в обычный список."""
        elements = []
        current = self._first
        
        while current is not None:
            elements.append(current.value)
            current = current.next
            
        return elements
    
    def is_empty(self) -> bool:
        """Проверка на отсутствие элементов."""
        return self._first is None
    
    def size(self) -> int:
        """Подсчёт количества элементов."""
        counter = 0
        current = self._first
        
        while current:
            counter += 1
            current = current.next
            
        return counter


def validate_bracket_sequence(expression: str) -> bool:
    """
    Валидация корректности расстановки скобок через стек.

    Временная сложность: O(n), n - длина выражения.
    """
    bracket_pairs = {')': '(', '}': '{', ']': '['}
    stack_holder = []

    for character in expression:
        if character in bracket_pairs.values():
            stack_holder.append(character)
        elif character in bracket_pairs:
            if not stack_holder or stack_holder[-1] != bracket_pairs[character]:
                return False
            stack_holder.pop()

    return not stack_holder


def check_palindrome_sequence(text: str) -> bool:
    """
    Проверка строки на палиндром с применением двусторонней очереди.

    Временная сложность: O(n), n - длина текста.
    """
    processed_text = ''.join(text.lower().split())
    character_deque = deque(processed_text)

    while len(character_deque) > 1:
        first_char = character_deque.popleft()
        last_char = character_deque.pop()
        if first_char != last_char:
            return False

    return True


def simulate_printing_queue(print_jobs: list[str]) -> None:
    """
    Эмуляция системы обработки заданий печати.

    Временная сложность: O(n), n - количество заданий.
    """
    job_queue = deque(print_jobs)
    total_time = 0

    print("Запуск эмуляции системы печати:")
    
    while job_queue:
        current_job = job_queue.popleft()
        total_time += 1
        
        print(f"Момент времени {total_time}: выполняется '{current_job}'")

        if job_queue:
            pending_jobs = [f"'{job}'" for job in job_queue]
            print(f"        ожидают: {', '.join(pending_jobs)}")
        else:
            print("        задания отсутствуют")

    print(f"Обработка всех заданий завершена за {total_time} временных единиц")


def showcase_linked_list_operations() -> None:
    """Демонстрация функциональности связного списка."""
    print("\nЭксплуатация связного списка:")
    linked_list_instance = LinkedList()

    # Добавление элементов
    operations = [
        (linked_list_instance.insert_at_start, 10),
        (linked_list_instance.insert_at_start, 20),
        (linked_list_instance.insert_at_end, 30),
        (linked_list_instance.insert_at_end, 40)
    ]
    
    for operation, value in operations:
        operation(value)

    print(f"Состояние списка после добавлений: {linked_list_instance.traversal()}")
    print(f"Текущий размер: {linked_list_instance.size()}")

    # Извлечение элемента
    extracted_value = linked_list_instance.delete_from_start()
    print(f"Извлеченный элемент: {extracted_value}")
    print(f"Список после извлечения: {linked_list_instance.traversal()}")


def execute_demonstrations() -> None:
    """Главная функция демонстрации решений."""
    print("=== ДЕМОНСТРАЦИЯ РЕШЕНИЙ ПРАКТИЧЕСКИХ ЗАДАЧ ===")

    # Демонстрация 1: Валидация скобочных последовательностей
    bracket_expressions = [
        "({[]})",
        "({[}])",
        "((()))",
        "({[()]})",
        "({[(])})"
    ]

    print("1. Анализ скобочных последовательностей:")
    for expression in bracket_expressions:
        validation_result = validate_bracket_sequence(expression)
        result_description = "Корректная последовательность" if validation_result else "Некорректная последовательность"
        print(f"   '{expression}' → {result_description}")

    # Демонстрация 2: Проверка палиндромов
    test_strings = [
        "А роза упала на лапу Азора",
        "racecar",
        "hello",
        "Madam",
        "12321"
    ]

    print("\n2. Анализ строк на палиндромность:")
    for text in test_strings:
        palindrome_check = check_palindrome_sequence(text)
        check_result = "Является палиндромом" if palindrome_check else "Не является палиндромом"
        print(f"   '{text}' → {check_result}")

    # Демонстрация 3: Эмуляция системы печати
    printing_tasks = ["Документ1", "Отчет", "Презентация", "Фото", "Чертеж"]
    simulate_printing_queue(printing_tasks)

    # Демонстрация связного списка
    showcase_linked_list_operations()


if __name__ == "__main__":
    execute_demonstrations()