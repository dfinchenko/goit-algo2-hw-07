import time
import matplotlib.pyplot as plt
from functools import lru_cache


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
        else:
            self._add_node(key, value, self.root)

    def _add_node(self, key, value, current):
        if key < current.key:
            if current.left:
                self._add_node(key, value, current.left)
            else:
                current.left = Node(key, value, current)
        else:
            if current.right:
                self._add_node(key, value, current.right)
            else:
                current.right = Node(key, value, current)

    def find(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node.key, node.value
        return None

    def _splay(self, node):
        while node.parent:
            if not node.parent.parent:
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left = node.left
        if not left:
            return
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.left:
            node.parent.left = left
        else:
            node.parent.right = left
        left.right = node
        node.parent = left

    def _rotate_left(self, node):
        right = node.right
        if not right:
            return
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right


@lru_cache()
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    found = tree.find(n)
    if found:
        return found[1]
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
        tree.insert(n, result)
        return result


if __name__ == "__main__":
    tree = SplayTree()
    test_values = [i * 50 for i in range(19)]
    lru_times = []
    splay_times = []
    lru_results = []
    splay_results = []

    for value in test_values:
        start_time = time.time()
        lru_results.append(fibonacci_lru(value))
        lru_times.append(time.time() - start_time)

        start_time = time.time()
        splay_results.append(fibonacci_splay(value, tree))
        splay_times.append(time.time() - start_time)


    print("n         LRU Cache Time (s)         Splay Tree Time (s)")
    print("-" * 55)
    for idx, n in enumerate(test_values):
        print(f"{n:<10}{lru_times[idx]:<25.8f}{splay_times[idx]:<.8f}")


    plt.figure(figsize=(10, 6))
    plt.plot(test_values, lru_times, label="LRU Cache", color="blue", marker="o")
    plt.plot(test_values, splay_times, label="Splay Tree", color="orange", marker="o")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree", fontsize=14)
    plt.xlabel("Число Фібоначчі (n)", fontsize=12)
    plt.ylabel("Середній час виконання (секунди)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

    print("\nВисновок:")
    print(
        "Згідно з отриманими результатами, реалізація за допомогою LRU Cache загалом є швидшою за підхід із Splay Tree, "
        "особливо для менших значень `n`. Проте, з ростом значення `n`, різниця в часі виконання між підходами стає більш вираженою, "
        "зокрема через накладні витрати на очищення кешу в Splay Tree. Також видно, що час виконання для Splay Tree має деякі коливання, "
        "причому спостерігається значне збільшення часу на більших значеннях, наприклад, для `750`, де час виконання значно перевищує час для LRU Cache."
    )
