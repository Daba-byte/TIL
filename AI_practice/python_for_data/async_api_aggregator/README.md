# Async API Aggregator

## 작성자
황다빈

## 작성일
2026-02-19

---

## 목적
동기 방식과 asyncio 기반 비동기 방식의 Latency 비교

---

## 실행 방법

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

실행 순서:
python 01_sequential_aggregator.py
python 02_async_aggregator.py
python 03_performance_compare.py