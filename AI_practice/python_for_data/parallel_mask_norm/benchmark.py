"""
파일명: benchmark.py
설명:
- 수백만 건 리뷰 데이터를 가정하여 PII 마스킹 + 금칙어 정규화를 수행한다.
- 단일 프로세스 vs multiprocessing.Pool(병렬)로 처리 시간을 비교한다.
- 데이터 청킹(Chunking) 및 Throughput(건/초)을 출력한다.
- IPC 비용을 관찰하기 위해 청크 사이즈를 바꿔 실험할 수 있도록 상수로 제공한다.

작성일: 2026-02-13
작성자: 황다빈

실행 방법:
$ python3 benchmark.py

주의:
- 기본 N=5_000_000(500만)은 메모리/시간이 매우 크다.
- 캡처용으로는 N을 200_000 ~ 1_000_000 정도로 낮춰도 충분히 비교 가능.
"""

from __future__ import annotations

import os
import random
import time
import multiprocessing as mp
from typing import List, Iterable

from processor import init_worker, process_text, process_chunk, ProcessStats


# -----------------------------
# 실험 설정
# -----------------------------
N = 5_000_000                 # 요구사항 핵심 포인트(500만) 실험용
MIN_WORDS = 8
MAX_WORDS = 20
SEED = 42

# 멀티프로세싱 설정
WORKERS = None                # None이면 os.cpu_count()
CHUNK_SIZE = 100_000          # "코어 수만큼 나눠서"와 유사한 효과: 큰 덩어리로 나눠 IPC 줄이기


# -----------------------------
# 리뷰 데이터 생성(실습용)
# -----------------------------
WORDS = [
    "great", "bad", "delivery", "taste", "service", "fast", "slow", "price",
    "quality", "recommend", "never", "again", "fresh", "hot", "cold", "omg",
    "wtf", "damn", "idiot", "stupid"
]

DOMAINS = ["example.com", "mail.com", "test.org", "sample.net"]


def make_fake_email(rng: random.Random) -> str:
    user = f"user{rng.randint(1, 999999)}"
    domain = rng.choice(DOMAINS)
    return f"{user}@{domain}"


def make_fake_phone(rng: random.Random) -> str:
    # 한국형 예시: 010-1234-5678
    a = "010"
    b = rng.randint(1000, 9999)
    c = rng.randint(1000, 9999)
    return f"{a}-{b}-{c}"


def generate_reviews(n: int, seed: int) -> List[str]:
    """
    n개의 리뷰 텍스트 생성.
    - 일부에 이메일/전화번호/금칙어를 섞어 넣어 마스킹 및 정규화 대상 생성
    """
    rng = random.Random(seed)
    reviews: List[str] = []

    for _ in range(n):
        length = rng.randint(MIN_WORDS, MAX_WORDS)
        base = rng.choices(WORDS, k=length)

        # 일정 확률로 PII 삽입
        if rng.random() < 0.25:
            base.append(make_fake_email(rng))
        if rng.random() < 0.25:
            base.append(make_fake_phone(rng))

        reviews.append(" ".join(base))

    return reviews


def chunkify(data: List[str], chunk_size: int) -> Iterable[List[str]]:
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def merge_stats(stats_list: List[ProcessStats]) -> ProcessStats:
    p = sum(s.processed for s in stats_list)
    m = sum(s.masked_hits for s in stats_list)
    n = sum(s.normalized_hits for s in stats_list)
    return ProcessStats(processed=p, masked_hits=m, normalized_hits=n)


def run_single(reviews: List[str]) -> ProcessStats:
    """
    단일 프로세스 처리.
    """
    # 단일 프로세스에서도 동일 로직(Regex 컴파일)을 사용하기 위해 초기화 수행
    init_worker()
    stats = process_chunk(reviews)
    return stats


def run_multi(reviews: List[str], workers: int | None, chunk_size: int) -> ProcessStats:
    """
    멀티프로세스(Pool) 처리.
    - 워커마다 init_worker로 Regex를 1회 컴파일 후 재사용한다.
    """
    if workers is None:
        workers = os.cpu_count() or 2

    chunks = list(chunkify(reviews, chunk_size))

    with mp.Pool(processes=workers, initializer=init_worker) as pool:
        parts = pool.map(process_chunk, chunks)

    return merge_stats(parts)


def throughput(count: int, seconds: float) -> float:
    return (count / seconds) if seconds > 0 else 0.0


def main():
    print("===== 병렬 마스킹 & 정규화 성능 비교: 단일 vs 멀티프로세스 =====")
    print(f"- 리뷰 개수: {N:,}")
    print(f"- 워커 수: {WORKERS if WORKERS is not None else (os.cpu_count() or 2)}")
    print(f"- CHUNK_SIZE: {CHUNK_SIZE:,}")
    print()

    # 1) 데이터 생성
    t0 = time.perf_counter()
    reviews = generate_reviews(N, SEED)
    t1 = time.perf_counter()
    gen_time = t1 - t0
    print(f"[1] 리뷰 데이터 생성 완료: {gen_time:.4f} seconds")
    print()

    # 샘플(캡처용)
    init_worker()
    sample_in = reviews[0]
    sample_out, mh, nh = process_text(sample_in)
    print("[샘플] 원본 리뷰 1건:")
    print(sample_in)
    print("[샘플] 처리 후 리뷰 1건:")
    print(sample_out)
    print(f"[샘플] masked_hits={mh}, normalized_hits={nh}")
    print()

    # 2) 단일 프로세스
    s0 = time.perf_counter()
    st_single = run_single(reviews)
    s1 = time.perf_counter()
    single_time = s1 - s0
    print("[2] 단일 프로세스 결과")
    print(f"    - 처리 건수: {st_single.processed:,}")
    print(f"    - 마스킹 치환 횟수: {st_single.masked_hits:,}")
    print(f"    - 정규화 치환 횟수: {st_single.normalized_hits:,}")
    print(f"    - 처리 시간: {single_time:.4f} seconds")
    print(f"    - Throughput: {throughput(st_single.processed, single_time):,.2f} reviews/sec")
    print()

    # 3) 멀티 프로세스
    m0 = time.perf_counter()
    st_multi = run_multi(reviews, WORKERS, CHUNK_SIZE)
    m1 = time.perf_counter()
    multi_time = m1 - m0
    print("[3] 멀티 프로세스(Pool) 결과")
    print(f"    - 처리 건수: {st_multi.processed:,}")
    print(f"    - 마스킹 치환 횟수: {st_multi.masked_hits:,}")
    print(f"    - 정규화 치환 횟수: {st_multi.normalized_hits:,}")
    print(f"    - 처리 시간: {multi_time:.4f} seconds")
    print(f"    - Throughput: {throughput(st_multi.processed, multi_time):,.2f} reviews/sec")
    print()

    # 4) 검증/비교
    print("[4] 검증/비교")
    ok = (st_single == st_multi)
    print(f"    - 통계 일치 여부: {ok}")
    if multi_time > 0:
        print(f"    - 속도 배율(단일/멀티): {single_time / multi_time:.2f}x")

    print()
    print("[추가 실험 안내]")
    print("    - IPC 비용 관찰: CHUNK_SIZE를 작게(예: 1_000) 바꾸면 오버헤드가 커져 느려질 수 있습니다.")
    print("    - 메모리 부담 완화: N을 200_000 ~ 1_000_000으로 줄여도 경향 비교는 가능합니다.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
