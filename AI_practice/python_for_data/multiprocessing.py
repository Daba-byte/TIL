"""
파일명: multiprocessing.py
설명:
- 1,000만 개의 난수를 생성한 뒤, 각 숫자가 소수(prime)인지 판별하여
  (a) 단일 프로세스
  (b) multiprocessing.Pool 병렬 처리
  두 방식의 처리 시간과 소수 개수를 비교한다.

작성일: 2026-02-13
작성자: 황다빈

실행 방법:
- Ubuntu/WSL:
  $ python3 multiprocessing.py

주의:
- 1,000만 개 정수 리스트는 메모리를 많이 사용한다(환경에 따라 수백 MB 이상).
- 멀티프로세싱은 OS/CPU/메모리 상황에 따라 성능이 달라질 수 있다.

파라미터(상단 상수로 조절):
- N: 생성할 난수 개수 (요구사항: 10_000_000)
- MIN_VAL, MAX_VAL: 난수 범위 (요구사항: 1 ~ 10_000_000)
- SEED: 재현 가능한 테스트를 위한 시드
- WORKERS: 멀티프로세스 워커 수 (None이면 os.cpu_count())
- CHUNK_SIZE: Pool.map에서 작업 분배 단위(성능에 영향)
"""

import math
import os
import random
import time
import multiprocessing as mp
from typing import List, Iterable


# -----------------------------
# 설정 상수
# -----------------------------
N = 10_000_000
MIN_VAL = 1
MAX_VAL = 10_000_000
SEED = 42

WORKERS = None          # None -> os.cpu_count()
CHUNK_SIZE = 50_000     # 너무 작으면 오버헤드↑, 너무 크면 분배 비효율 가능


# -----------------------------
# 소수 판별 함수
# -----------------------------
def is_prime(n: int) -> bool:
    """
    정수 n이 소수인지 판별한다.

    구현 포인트:
    - 2 미만은 소수 아님
    - 2는 소수
    - 짝수는 소수 아님
    - 3부터 sqrt(n)까지 홀수로 나눠 떨어지는지 확인
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if (n % 2) == 0:
        return False

    limit = int(math.isqrt(n))
    d = 3
    while d <= limit:
        if (n % d) == 0:
            return False
        d += 2
    return True


def count_primes_single(nums: List[int]) -> int:
    """
    단일 프로세스로 소수 개수를 센다.
    """
    cnt = 0
    for x in nums:
        if is_prime(x):
            cnt += 1
    return cnt


def _count_primes_in_chunk(chunk: List[int]) -> int:
    """
    멀티프로세스에서 각 워커가 처리할 단위(청크) 소수 개수 계산 함수.
    """
    cnt = 0
    for x in chunk:
        if is_prime(x):
            cnt += 1
    return cnt


def chunkify(nums: List[int], chunk_size: int) -> Iterable[List[int]]:
    """
    리스트를 chunk_size 단위로 잘라 yield한다.
    Pool.map에 '청크 리스트'들을 넘겨서 워커들이 청크 단위로 처리하도록 만든다.
    """
    for i in range(0, len(nums), chunk_size):
        yield nums[i:i + chunk_size]


def count_primes_multi(nums: List[int], workers: int | None, chunk_size: int) -> int:
    """
    multiprocessing.Pool을 사용해 병렬로 소수 개수를 센다.
    """
    if workers is None:
        workers = os.cpu_count() or 2

    chunks = list(chunkify(nums, chunk_size))

    # Windows에서는 spawn 이슈가 많아 보통 if __name__ == "__main__" 가 필요.
    # WSL/Ubuntu도 동일하게 가드가 안전하다.
    with mp.Pool(processes=workers) as pool:
        partial_counts = pool.map(_count_primes_in_chunk, chunks)

    return sum(partial_counts)


def generate_numbers(n: int, min_val: int, max_val: int, seed: int) -> List[int]:
    """
    random을 사용하여 n개의 정수를 생성해 리스트로 반환한다. (요구사항 충족)
    """
    rng = random.Random(seed)
    # randint(a, b)는 양 끝 포함
    return [rng.randint(min_val, max_val) for _ in range(n)]


def main():
    print("===== 병렬처리 성능 비교: 단일 vs 멀티프로세스 =====")
    print(f"- 난수 개수: {N:,}")
    print(f"- 난수 범위: {MIN_VAL:,} ~ {MAX_VAL:,}")
    print(f"- 워커 수: {WORKERS if WORKERS is not None else (os.cpu_count() or 2)}")
    print(f"- CHUNK_SIZE: {CHUNK_SIZE:,}")
    print()

    # 1) 난수 생성 시간 측정
    t0 = time.perf_counter()
    nums = generate_numbers(N, MIN_VAL, MAX_VAL, SEED)
    t1 = time.perf_counter()
    print(f"[1] 난수 리스트 생성 완료: {t1 - t0:.4f} seconds")
    print()

    # 2) 단일 프로세스 소수 개수 + 시간
    s0 = time.perf_counter()
    primes_single = count_primes_single(nums)
    s1 = time.perf_counter()
    single_time = s1 - s0
    print(f"[2] 단일 프로세스 결과")
    print(f"    - 소수 개수: {primes_single:,}")
    print(f"    - 처리 시간: {single_time:.4f} seconds")
    print()

    # 3) 멀티 프로세스 소수 개수 + 시간
    m0 = time.perf_counter()
    primes_multi = count_primes_multi(nums, WORKERS, CHUNK_SIZE)
    m1 = time.perf_counter()
    multi_time = m1 - m0
    print(f"[3] 멀티 프로세스(Pool) 결과")
    print(f"    - 소수 개수: {primes_multi:,}")
    print(f"    - 처리 시간: {multi_time:.4f} seconds")
    print()

    # 4) 검증 및 비교
    print("[4] 검증/비교")
    print(f"    - 결과 일치 여부: {primes_single == primes_multi}")
    if multi_time > 0:
        print(f"    - 속도 배율(단일/멀티): {single_time / multi_time:.2f}x")


if __name__ == "__main__":
    # 멀티프로세싱 안전 가드
    mp.freeze_support()
    main()
