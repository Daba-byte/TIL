"""
파일명: sum_squares.py
설명:
- 정수 리스트를 입력받아 각 원소의 제곱의 합을 반환하는 함수
- A 버전: 타입 힌트 없음
- B 버전: 타입 힌트 적용

작성일: 2026-02-13
작성자: 황다빈
"""

# -----------------------------
# A 버전 (타입 힌트 없음)
# -----------------------------
def sum_squares_a(numbers):
    total = 0
    for n in numbers:
        total += n * n
    return total


# -----------------------------
# B 버전 (타입 힌트 적용)
# -----------------------------
from typing import List

def sum_squares_b(numbers: List[int]) -> int:
    total: int = 0
    for n in numbers:
        total += n * n
    return total
