"""
prefix_function.py
Реализация вычисления префикс-функции для строки.
Префикс-функция используется в алгоритме Кнута-Морриса-Пратта (KMP).
"""

def compute_prefix_function(pattern):
    """
    Вычисление префикс-функции для строки pattern.
    
    Префикс-функция π[i] - длина наибольшего собственного префикса подстроки pattern[0..i],
    который является суффиксом этой же подстроки.
    
    Args:
        pattern: строка, для которой вычисляется префикс-функция
    
    Returns:
        Список значений префикс-функции
    
    Сложность:
        Время: O(m), где m = len(pattern)
        Память: O(m)
    
    Пример:
        pattern = "abababca"
        prefix = compute_prefix_function(pattern)
        Результат: [0, 0, 1, 2, 3, 4, 0, 1]
    """
    m = len(pattern)
    if m == 0:
        return []
    
    pi = [0] * m  # Префикс-функция
    
    # Вычисляем префикс-функцию для каждого префикса
    for i in range(1, m):
        j = pi[i - 1]  # Длина предыдущего префикса-суффикса
        
        # Пытаемся расширить предыдущий префикс-суффикс
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]  # Откатываемся к более короткому префиксу
        
        # Если символы совпадают, увеличиваем длину префикса-суффикса
        if pattern[i] == pattern[j]:
            j += 1
        
        pi[i] = j
    
    return pi


def visualize_prefix_function(pattern, pi):
    """
    Визуализация префикс-функции для наглядности.
    
    Args:
        pattern: исходная строка
        pi: вычисленная префикс-функция
    """
    print(f"Строка: {pattern}")
    print("Индексы:", " ".join(f"{i:2}" for i in range(len(pattern))))
    print("Символы:", " ".join(f"{c:2}" for c in pattern))
    print("π[i]:   ", " ".join(f"{val:2}" for val in pi))
    
    # Визуализация связей
    print("\nВизуализация префикс-суффиксов:")
    for i in range(len(pattern)):
        if pi[i] > 0:
            prefix = pattern[:pi[i]]
            suffix = pattern[i-pi[i]+1:i+1]
            print(f"π[{i}] = {pi[i]}: префикс '{prefix}' == суффикс '{suffix}'")


def find_period_using_prefix(pattern):
    """
    Нахождение периода строки с использованием префикс-функции.
    
    Args:
        pattern: строка для анализа
    
    Returns:
        period: период строки (0 если строка не периодическая)
        is_periodic: является ли строка периодической
    """
    if len(pattern) == 0:
        return 0, False
    
    pi = compute_prefix_function(pattern)
    n = len(pattern)
    
    # Период = n - π[n-1], если n делится на период
    candidate_period = n - pi[n-1]
    
    if n % candidate_period == 0:
        return candidate_period, True
    else:
        return 0, False


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("ВЫЧИСЛЕНИЕ ПРЕФИКС-ФУНКЦИИ")
    print("=" * 60)
    
    # Пример 1: Базовая строка
    pattern1 = "abababca"
    print(f"\nПример 1: '{pattern1}'")
    pi1 = compute_prefix_function(pattern1)
    visualize_prefix_function(pattern1, pi1)
    
    # Пример 2: Периодическая строка
    pattern2 = "abcabcabc"
    print(f"\n\nПример 2: '{pattern2}'")
    pi2 = compute_prefix_function(pattern2)
    visualize_prefix_function(pattern2, pi2)
    
    # Нахождение периода
    period2, is_periodic2 = find_period_using_prefix(pattern2)
    print(f"\nПериод строки '{pattern2}': {period2}, периодическая: {is_periodic2}")
    
    # Пример 3: Случайная строка
    pattern3 = "algorithm"
    print(f"\n\nПример 3: '{pattern3}'")
    pi3 = compute_prefix_function(pattern3)
    visualize_prefix_function(pattern3, pi3)
    
    # Пример 4: Пустая строка и строка из одного символа
    print(f"\n\nПример 4: Пустая строка")
    pi_empty = compute_prefix_function("")
    print(f"Результат для пустой строки: {pi_empty}")
    
    pattern_single = "a"
    print(f"\nПример 5: Строка из одного символа '{pattern_single}'")
    pi_single = compute_prefix_function(pattern_single)
    print(f"Префикс-функция: {pi_single}")