'''
작성자: 황다빈
작성일: 2026-02-12
설명: 제너레이터 기반 메모리 절약형 로직 작성
'''
import sys
import time

N = 1_000_000

# 1) 리스트 방식
start_time_list = time.time()
even_square_list = [i * i for i in range(N) if i % 2 == 0]
list_sum = sum(even_square_list)
end_time_list = time.time()

list_time = end_time_list - start_time_list
list_memory = sys.getsizeof(even_square_list)

# 2) 제너레이터 방식
def even_square_gen(n):
    for i in range(n):
        if i % 2 == 0:
            yield i * i

start_time_gen = time.time()
gen_sum = sum(even_square_gen(N))
end_time_gen = time.time()

gen_time = end_time_gen - start_time_gen

gen_object = even_square_gen(N)
gen_memory = sys.getsizeof(gen_object)