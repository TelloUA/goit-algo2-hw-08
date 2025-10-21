import time
import random
from functools import lru_cache
from custom_lru_cache import LRUCache

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

range_cache = LRUCache(1000)

def range_sum_with_cache(array, L, R):
    cache_key = (id(array), L, R)
    result = range_cache.get(cache_key)
    if result != -1:
        return result
    
    result = sum(array[L:R+1])
    range_cache.put(cache_key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    
    array_id = id(array)
    keys_to_remove = []
    
    for key in range_cache.cache.keys():
        if len(key) == 3 and key[0] == array_id:
            L, R = key[1], key[2]
            if L <= index <= R:
                keys_to_remove.append(key)
    
    for key in keys_to_remove:
        node = range_cache.cache[key]
        range_cache.list.remove(node)
        del range_cache.cache[key]

def create_array(len):
    list = []

    i = 0
    while i < len:
        i += 1
        list.append(random.randint(0, 10_000))

    return list

def make_queries(len, quantity, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, len//2), random.randint(len//2, len-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(quantity):
        if random.random() < p_update:        # ~3% запитів — Update
            idx = random.randint(0, len-1)
            val = random.randint(1, 100)
            queries.append(("update", idx, val))
        else:                                 # ~97% — Range
            if random.random() < p_hot:       # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:                             # 5% — випадкові діапазони
                left = random.randint(0, len-1)
                right = random.randint(left, len-1)
            queries.append(("range", left, right))
    return queries

def run_process_no_cache(array, operations):
    start_time = time.time()
    for operation in operations:
        if operation[0] == 'range':
            range_sum_no_cache(array, operation[1], operation[2])
        elif operation[0] == 'update':
            update_no_cache(array, operation[1], operation[2])

    end_time = time.time()
    elapsed_time = end_time - start_time 
    print(f"Час виконання без кешу: {elapsed_time:.6f} секунд")

def run_process_with_cache(array, operations):
    start_time = time.time()
    for operation in operations:
        if operation[0] == 'range':
            range_sum_with_cache(array, operation[1], operation[2])
        elif operation[0] == 'update':
            update_with_cache(array, operation[1], operation[2])

    end_time = time.time()
    elapsed_time = end_time - start_time 
    print(f"Час виконання з кешем: {elapsed_time:.6f} секунд")

if __name__ == '__main__':
    length = 100_000
    array = create_array(length)
    
    operations = make_queries(length, 50_000)
    run_process_no_cache(array, operations)

    operations = make_queries(length, 50_000)
    run_process_with_cache(array, operations)