"""
파일명: benchmark.py
설명:
- A, B 함수 성능 비교
- timeit 사용

작성일: 2026-02-13
작성자: 황다빈
"""

import timeit
from sum_squares import sum_squares_a, sum_squares_b

# 테스트 데이터
data = list(range(1_000_000))

# 실행 횟수
repeat_count = 5

time_a = timeit.timeit(lambda: sum_squares_a(data), number=repeat_count)
time_b = timeit.timeit(lambda: sum_squares_b(data), number=repeat_count)

print("===== 성능 측정 결과 =====")
print(f"A 버전 실행 시간: {time_a:.6f} seconds")
print(f"B 버전 실행 시간: {time_b:.6f} seconds")
print(f"차이: {abs(time_a - time_b):.6f} seconds")
