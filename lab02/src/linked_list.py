"""Реализация односвязного списка для ЛР-02"""


class ListNode:
    """Элемент связного списка"""
    
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class SinglyLinkedList:
    """Однонаправленный связный список с указателями на начало и конец"""
    
    def __init__(self):
        self._first = None
        self._last = None
    
    def prepend(self, value) -> None:
        """Добавление элемента в начало списка. O(1)"""
        new_element = ListNode(value)
        
        if not self._first:
            self._first = self._last = new_element
        else:
            new_element.next = self._first
            self._first = new_element
    
    def append(self, value) -> None:
        """Добавление элемента в конец списка. O(1)"""
        new_element = ListNode(value)
        
        if not self._last:
            self._first = self._last = new_element
        else:
            self._last.next = new_element
            self._last = new_element
    
    def pop_front(self):
        """Извлечение элемента из начала списка. O(1)"""
        if self._first is None:
            return None
        
        extracted_value = self._first.value
        self._first = self._first.next
        
        if self._first is None:
            self._last = None
            
        return extracted_value
    
    def to_list(self) -> list:
        """Преобразование связного списка в обычный список. O(n)"""
        elements = []
        current = self._first
        
        while current is not None:
            elements.append(current.value)
            current = current.next
            
        return elements
    
    def empty(self) -> bool:
        """Проверка на отсутствие элементов. O(1)"""
        return self._first is None
    
    def length(self) -> int:
        """Подсчёт количества элементов. O(n)"""
        counter = 0
        current = self._first
        
        while current:
            counter += 1
            current = current.next
            
        return counter


def demonstrate_linked_list():
    """Пример использования связного списка"""
    lst = SinglyLinkedList()
    
    # Добавляем элементы
    lst.prepend(10)
    lst.prepend(20)
    lst.append(5)
    
    # Выводим информацию о списке
    print("Элементы списка:", lst.to_list())
    print("Количество элементов:", lst.length())
    print("Извлечённый элемент:", lst.pop_front())
    print("Список после извлечения:", lst.to_list())


if __name__ == "__main__":
    demonstrate_linked_list()