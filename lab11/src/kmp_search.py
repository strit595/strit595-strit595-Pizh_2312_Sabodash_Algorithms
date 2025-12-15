"""
kmp_search.py
Реализация алгоритма Кнута-Морриса-Пратта (KMP) для поиска подстроки.
Использует префикс-функцию для эффективного поиска.
"""

from prefix_function import compute_prefix_function


def kmp_search(text, pattern):
    """
    Алгоритм Кнута-Морриса-Пратта для поиска всех вхождений подстроки.
    
    Args:
        text: строка, в которой ищем
        pattern: подстрока, которую ищем
    
    Returns:
        Список начальных индексов всех вхождений pattern в text
    
    Сложность:
        Время: O(n + m), где n = len(text), m = len(pattern)
        Память: O(m) для хранения префикс-функции
    
    Пример:
        text = "ababcabcabababd"
        pattern = "ababd"
        Результат: [10] (индекс начала вхождения)
    """
    if not pattern:
        return list(range(len(text) + 1))
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Вычисляем префикс-функцию для паттерна
    pi = compute_prefix_function(pattern)
    
    occurrences = []
    j = 0  # Текущая позиция в паттерне
    
    for i in range(n):  # i - текущая позиция в тексте
        # Пока есть несовпадение, сдвигаем паттерн с использованием префикс-функции
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        
        # Если символы совпали, продвигаемся по паттерну
        if text[i] == pattern[j]:
            j += 1
        
        # Если дошли до конца паттерна - нашли вхождение
        if j == m:
            occurrences.append(i - m + 1)
            j = pi[j - 1]  # Продолжаем поиск
    
    return occurrences


def kmp_search_with_highlight(text, pattern):
    """
    Поиск с визуализацией - подсветка найденных вхождений.
    
    Args:
        text: исходный текст
        pattern: искомый паттерн
    
    Returns:
        occurrences: индексы вхождений
        highlighted_text: текст с подсветкой вхождений
    """
    occurrences = kmp_search(text, pattern)
    
    # Создаем текст с подсветкой
    if not occurrences:
        return occurrences, text
    
    highlighted_parts = []
    prev_end = 0
    
    for start in sorted(occurrences):
        end = start + len(pattern)
        
        # Добавляем часть до вхождения
        if start > prev_end:
            highlighted_parts.append(text[prev_end:start])
        
        # Добавляем подсвеченное вхождение
        highlighted_parts.append(f"[{text[start:end]}]")
        prev_end = end
    
    # Добавляем остаток текста
    if prev_end < len(text):
        highlighted_parts.append(text[prev_end:])
    
    highlighted_text = "".join(highlighted_parts)
    return occurrences, highlighted_text


def naive_search(text, pattern):
    """
    Наивный алгоритм поиска подстроки для сравнения с KMP.
    
    Args:
        text: строка, в которой ищем
        pattern: подстрока, которую ищем
    
    Returns:
        Список начальных индексов всех вхождений
    
    Сложность:
        Время: O(n * m) в худшем случае
        Память: O(1)
    """
    if not pattern:
        return list(range(len(text) + 1))
    
    n, m = len(text), len(pattern)
    occurrences = []
    
    for i in range(n - m + 1):
        found = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                found = False
                break
        if found:
            occurrences.append(i)
    
    return occurrences


def compare_kmp_naive(text, pattern):
    """
    Сравнение результатов KMP и наивного алгоритма.
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
    
    Returns:
        Словарь с результатами сравнения
    """
    import time
    
    # Замер времени для KMP
    start = time.time()
    kmp_result = kmp_search(text, pattern)
    kmp_time = time.time() - start
    
    # Замер времени для наивного алгоритма
    start = time.time()
    naive_result = naive_search(text, pattern)
    naive_time = time.time() - start
    
    # Проверка корректности
    correct = kmp_result == naive_result
    
    return {
        'kmp_result': kmp_result,
        'naive_result': naive_result,
        'kmp_time': kmp_time,
        'naive_time': naive_time,
        'speedup': naive_time / kmp_time if kmp_time > 0 else float('inf'),
        'correct': correct,
        'occurrences': len(kmp_result)
    }


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("АЛГОРИТМ КНУТА-МОРРИСА-ПРАТТА (KMP)")
    print("=" * 60)
    
    # Пример 1: Базовый поиск
    text1 = "ababcabcabababd"
    pattern1 = "ababd"
    
    print(f"\nПример 1:")
    print(f"Текст:    '{text1}'")
    print(f"Паттерн:  '{pattern1}'")
    
    indices = kmp_search(text1, pattern1)
    _, highlighted = kmp_search_with_highlight(text1, pattern1)
    
    print(f"Найдено вхождений: {len(indices)}")
    print(f"Индексы: {indices}")
    print(f"Текст с подсветкой: {highlighted}")
    
    # Пример 2: Множественные вхождения
    text2 = "ABABDABACDABABCABAB"
    pattern2 = "ABAB"
    
    print(f"\nПример 2:")
    print(f"Текст:    '{text2}'")
    print(f"Паттерн:  '{pattern2}'")
    
    indices2 = kmp_search(text2, pattern2)
    _, highlighted2 = kmp_search_with_highlight(text2, pattern2)
    
    print(f"Найдено вхождений: {len(indices2)}")
    print(f"Индексы: {indices2}")
    print(f"Текст с подсветкой: {highlighted2}")
    
    # Пример 3: Сравнение с наивным алгоритмом
    print(f"\nПример 3: Сравнение KMP и наивного алгоритма")
    comparison = compare_kmp_naive(text2, pattern2)
    
    print(f"Результаты KMP: {comparison['kmp_result']}")
    print(f"Результаты наивного: {comparison['naive_result']}")
    print(f"Время KMP: {comparison['kmp_time']:.8f} сек")
    print(f"Время наивного: {comparison['naive_time']:.8f} сек")
    print(f"Ускорение KMP: {comparison['speedup']:.2f}x")
    print(f"Результаты совпадают: {comparison['correct']}")
    
    # Пример 4: Паттерн не найден
    text4 = "abcdefghijklmnop"
    pattern4 = "xyz"
    
    print(f"\nПример 4: Паттерн не найден")
    print(f"Текст:    '{text4}'")
    print(f"Паттерн:  '{pattern4}'")
    
    indices4 = kmp_search(text4, pattern4)
    print(f"Найдено вхождений: {len(indices4)}")
    print(f"Индексы: {indices4}")
    
    # Пример 5: Пустой паттерн
    print(f"\nПример 5: Пустой паттерн")
    indices5 = kmp_search(text4, "")
    print(f"Для пустого паттерна найдено {len(indices5)} вхождений")
    print(f"Первые 10 индексов: {indices5[:10]}...")