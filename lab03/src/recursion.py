"""
Реализация классических рекурсивных алгоритмов вычисления.
"""


def compute_factorial(value):
    """
    Рекурсивное вычисление факториала переданного значения.

    Параметры:
        value (int): Целое неотрицательное число.

    Возвращает:
        int: Результат вычисления факториала.

    Исключения:
        ValueError: При передаче отрицательного значения.

    Временная характеристика: O(value)
    Уровень рекурсии: O(value)
    """
    assert isinstance(value, int), "Аргумент должен быть целым числом"
    
    if value < 0:
        error_message = "Факториал вычисляется только для неотрицательных значений"
        raise ValueError(error_message)
    
    match value:
        case 0 | 1:
            return 1
        case _:
            return value * compute_factorial(value - 1)


def generate_fibonacci_number(index):
    """
    Получение числа Фибоначчи по индексу через рекурсивный подход.

    Параметры:
        index (int): Индекс в последовательности Фибоначчи (индекс >= 0).

    Возвращает:
        int: Число Фибоначчи на указанной позиции.

    Исключения:
        ValueError: При отрицательном индексе.

    Временная характеристика: O(2^index)
    Уровень рекурсии: O(index)
    """
    if not isinstance(index, int):
        raise TypeError("Индекс должен быть целым числом")
    
    if index < 0:
        error_message = "Индекс в последовательности не может быть отрицательным"
        raise ValueError(error_message)
    
    match index:
        case 0:
            return 0
        case 1:
            return 1
        case _:
            previous_1 = generate_fibonacci_number(index - 1)
            previous_2 = generate_fibonacci_number(index - 2)
            return previous_1 + previous_2


def exponentiate_number(base, exponent):
    """
    Эффективное возведение числа в степень через рекурсивное разложение.

    Параметры:
        base (float): Число для возведения в степень.
        exponent (int): Целая неотрицательная степень.

    Возвращает:
        float: Результат возведения в степень.

    Исключения:
        ValueError: При отрицательной степени.

    Временная характеристика: O(log(exponent))
    Уровень рекурсии: O(log(exponent))
    """
    if exponent < 0:
        error_message = "Степень должна быть неотрицательным целым числом"
        raise ValueError(error_message)
    
    match exponent:
        case 0:
            return 1.0
        case 1:
            return float(base)
        case _ if exponent % 2 == 0:
            half_exponent = exponentiate_number(base, exponent // 2)
            return half_exponent * half_exponent
        case _:
            return base * exponentiate_number(base, exponent - 1)


def demonstrate_algorithms():
    """Демонстрация работы рекурсивных алгоритмов."""
    test_scenarios = [
        ("Факториал числа 5", compute_factorial, (5,)),
        ("10-е число Фибоначчи", generate_fibonacci_number, (10,)),
        ("2 в 10 степени", exponentiate_number, (2, 10)),
        ("5 в 4 степени", exponentiate_number, (5, 4))
    ]
    
    for description, algorithm, arguments in test_scenarios:
        try:
            computation_result = algorithm(*arguments)
            print(f"{description}: {computation_result}")
        except (ValueError, TypeError) as error_instance:
            print(f"{description}: Ошибка - {error_instance}")


def validate_algorithm_execution():
    """Валидация корректности выполнения алгоритмов."""
    validation_cases = [
        (compute_factorial, [(0, 1), (1, 1), (5, 120)]),
        (generate_fibonacci_number, [(0, 0), (1, 1), (6, 8)]),
        (exponentiate_number, [(2, 3, 8), (5, 0, 1), (3, 4, 81)])
    ]
    
    for algorithm, test_cases in validation_cases:
        algorithm_name = algorithm.__name__
        print(f"\nВалидация {algorithm_name}:")
        
        for *arguments, expected in test_cases:
            actual_result = algorithm(*arguments)
            status = "✓ Пройдено" if actual_result == expected else "✗ Не пройдено"
            print(f"  {arguments} -> {actual_result} {status}")


if __name__ == "__main__":
    print("Демонстрация работы рекурсивных алгоритмов")
    print("=" * 50)
    
    demonstrate_algorithms()
    validate_algorithm_execution()