"""
작성자: 황다빈
작성일: 2026-02-19

코드 목적:
    asyncio 기반 Concurrent 방식으로 API를 병렬 호출하여
    Latency를 측정한다.

상세 설명:
    - aiohttp 사용
    - asyncio.gather 활용
    - 병렬 실행
"""

import asyncio
import aiohttp
import time

API_LIST = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/1"
]

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, api) for api in API_LIST]
        return await asyncio.gather(*tasks)

start = time.time()
results = asyncio.run(main())
end = time.time()

print("Async Results:", results)
print("Async Latency:", round(end - start, 2), "seconds")