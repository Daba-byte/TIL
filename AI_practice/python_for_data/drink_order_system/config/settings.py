"""
파일명: settings.py
설명: 환경변수(.env) 로드 및 전역 설정 관리 파일
작성일: 2026-02-13
작성자: 황다빈

파라미터:
- TAX_RATE: 주문 총 금액에 적용할 세율
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 세율 설정 (기본값 0.0)
TAX_RATE = float(os.getenv("TAX_RATE", 0.0))
