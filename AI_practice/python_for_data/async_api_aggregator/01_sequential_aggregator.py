"""
작성자: 황다빈
작성일: 2026-02-19

과정명: 파이썬 3일차 - Codelab ①
코드 목적:
    동기 방식(Sequential)으로 여러 API를 순차 호출하여
    전체 응답 시간을 측정한다.

상세 설명:
    - httpbin.org/delay/{n} API 사용
    - 각 요청은 순차적으로 실행
    - 전체 Latency 측정
"""

import requests
import time

API_LIST = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/1"
]

def fetch(url):
    response = requests.get(url)
    return response.status_code

start = time.time()

results = []
for api in API_LIST:
    results.append(fetch(api))

end = time.time()

print("Sequential Results:", results)
print("Sequential Latency:", round(end - start, 2), "seconds")
