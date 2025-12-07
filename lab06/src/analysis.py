"""
Модуль анализа производительности BST.
"""
import time
import random
import matplotlib.pyplot as plt
from binary_search_tree import BinarySearchTree


def create_balanced_tree(size):
    """Создание сбалансированного дерева."""
    tree = BinarySearchTree()
    values = list(range(size))
    random.shuffle(values)

    for value in values:
        tree.insert(value)

    return tree, values


def create_degenerate_tree(size):
    """Создание вырожденного дерева."""
    tree = BinarySearchTree()

    for value in range(size):
        tree.insert(value)

    return tree, list(range(size))


def measure_search_time(tree, values, num_searches=1000):
    """Измерение времени поиска."""
    start_time = time.time()

    for _ in range(num_searches):
        value = random.choice(values)
        tree.search(value)

    end_time = time.time()
    return end_time - start_time


def analyze_performance():
    """Основной анализ производительности."""
    print("=== Анализ производительности BST ===\n")

    # Уменьшим размеры деревьев для избежания рекурсии
    sizes = [100, 200, 300, 400, 500]
    balanced_times = []
    degenerate_times = []

    header = "Размер | Время сб. | Время выр. | Выс. сб. | Выс. выр."
    print(header)
    print("-" * len(header))

    for size in sizes:
        # Сбалансированное дерево
        balanced_tree, balanced_vals = create_balanced_tree(size)
        balanced_time = measure_search_time(balanced_tree, balanced_vals, 500)
        balanced_times.append(balanced_time)

        # Вырожденное дерево
        degenerate_tree, degenerate_vals = create_degenerate_tree(size)
        degenerate_time = measure_search_time(degenerate_tree,
                                              degenerate_vals, 500)
        degenerate_times.append(degenerate_time)

        print(f"{size:6} | {balanced_time:9.6f} | "
              f"{degenerate_time:10.6f} | "
              f"{balanced_tree.height():8} | "
              f"{degenerate_tree.height():9}")

    # Построение графика
    plot_results(sizes, balanced_times, degenerate_times)

    return sizes, balanced_times, degenerate_times


def plot_results(sizes, balanced_times, degenerate_times):
    """Построение графиков."""
    plt.figure(figsize=(10, 4))

    # График 1
    plt.subplot(1, 2, 1)
    plt.plot(sizes, balanced_times, 'b-',
             label='Сбалансированное', marker='o')
    plt.plot(sizes, degenerate_times, 'r-',
             label='Вырожденное', marker='s')
    plt.xlabel('Размер дерева')
    plt.ylabel('Время (сек)')
    plt.title('Время 500 операций поиска')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # График 2
    plt.subplot(1, 2, 2)
    ratios = []
    for d_time, b_time in zip(degenerate_times, balanced_times):
        if b_time > 0:
            ratios.append(d_time / b_time)
        else:
            ratios.append(0)

    plt.plot(sizes, ratios, 'g-', marker='^')
    plt.xlabel('Размер дерева')
    plt.ylabel('Отношение времён')
    plt.title('Вырожденное / Сбалансированное')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('bst_analysis.png', dpi=150)
    plt.show()


def analyze_tree_properties():
    """Анализ свойств деревьев разных размеров."""
    print("\n=== Анализ свойств деревьев ===")

    test_sizes = [10, 50, 100, 300]

    for size in test_sizes:
        print(f"\nРазмер: {size}")

        # Сбалансированное
        b_tree, _ = create_balanced_tree(size)
        print("  Сбалансированное:")
        print(f"    Высота: {b_tree.height()}")
        print(f"    Минимум: {b_tree.find_min().value}")
        print(f"    Максимум: {b_tree.find_max().value}")

        # Вырожденное
        d_tree, _ = create_degenerate_tree(size)
        print("  Вырожденное:")
        print(f"    Высота: {d_tree.height()}")
        print(f"    Минимум: {d_tree.find_min().value}")
        print(f"    Максимум: {d_tree.find_max().value}")


def main():
    """Основная функция."""
    # Анализ свойств
    analyze_tree_properties()

    # Анализ производительности
    print("\n" + "=" * 60)
    sizes, b_times, d_times = analyze_performance()

    # Вывод результатов
    print("\n=== Результаты анализа ===")
    print("1. В сбалансированном дереве время поиска растет медленно")
    print("2. В вырожденном дереве время поиска растет линейно")
    print("3. Разница становится заметной при n > 200 элементов")
    print("\nГрафик сохранен в файле 'bst_analysis.png'")


if __name__ == "__main__":
    main()