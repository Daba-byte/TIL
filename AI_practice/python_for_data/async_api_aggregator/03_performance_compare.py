"""
작성자: 황다빈
작성일: 2026-02-19

코드 목적:
    Sequential vs Async Latency 비교

상세 설명:
    - 각각 3회 반복 실행
    - 평균 Latency 계산
"""

import subprocess
import re

def extract_latency(output):
    match = re.search(r"Latency:\s+([\d.]+)", output)
    return float(match.group(1))

seq_times = []
async_times = []

for _ in range(3):
    seq_output = subprocess.check_output(
        ["python", "01_sequential_aggregator.py"]
    ).decode()
    async_output = subprocess.check_output(
        ["python", "02_async_aggregator.py"]
    ).decode()

    seq_times.append(extract_latency(seq_output))
    async_times.append(extract_latency(async_output))

print("Sequential 평균:", sum(seq_times)/3)
print("Async 평균:", sum(async_times)/3)