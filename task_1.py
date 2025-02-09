import random
import time
from collections import OrderedDict

cache = OrderedDict()

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R):
    key = (L, R)
    if key not in cache:
        cache[key] = sum(array[L:R+1])
        if len(cache) > K:
            cache.popitem(last=False)
    else:
        cache.move_to_end(key)
    return cache[key]

def update_with_cache(array, index, value):
    array[index] = value
    keys_to_delete = [key for key in cache.keys() if key[0] <= index <= key[1]]
    for key in keys_to_delete:
        del cache[key]

def measure_time(func_range, func_update, queries, array):
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            func_range(array, query[1], query[2])
        else:
            func_update(array, query[1], query[2])
    return time.time() - start

if __name__ == "__main__":
    N = 100_000
    Q = 50_000
    K = 1000

    array = [random.randint(1, 1000) for _ in range(N)]
    queries = [('Range', *sorted(random.sample(range(N), 2))) if random.random() < 0.7
               else ('Update', random.randint(0, N-1), random.randint(1, 1000)) for _ in range(Q)]

    print(f'Час виконання без кешування: {measure_time(range_sum_no_cache, update_no_cache, queries, array):.4f} секунд')
    print(f'Час виконання з LRU-кешем: {measure_time(range_sum_with_cache, update_with_cache, queries, array):.4f} секунд')
    print("\nВисновок:")
    print("Використання кешу LRU для цього завдання не забезпечує значного підвищення продуктивності. "
       "Масив уже забезпечує ефективний доступ до даних, і навіть збільшення повторення \"частих значень\" "
        "або реалізація часткового кешування не дало кращих результатів через часту недійсність кешу, спричинену оновленнями в масиві."
    )

