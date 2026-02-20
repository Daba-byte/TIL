"""
파일명: processor.py
설명:
- 리뷰 텍스트에서 개인정보(이메일, 전화번호)를 마스킹(****) 처리
- 금칙어/비표준 표현을 표준 표현으로 정규화(normalization) 처리
- 정규표현식(Regex) 컴파일을 워커 프로세스별로 1회만 수행하여 오버헤드를 줄인다.

작성일: 2026-02-13
작성자: 황다빈

주요 함수:
- init_worker(): 멀티프로세스 워커 초기화(Regex 컴파일)
- process_text(text): 마스킹 + 정규화 수행
- process_chunk(chunk): 리스트(청크) 단위 처리 및 처리량/변경량 집계
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Dict


# 워커 프로세스별로 1회 컴파일해서 재사용할 전역(각 프로세스 내부 전역)
EMAIL_RE: re.Pattern | None = None
PHONE_RE: re.Pattern | None = None
BADWORD_RE: re.Pattern | None = None
BADWORD_MAP: Dict[str, str] | None = None


@dataclass(frozen=True)
class ProcessStats:
    """
    처리 통계
    - processed: 처리한 텍스트 개수
    - masked_hits: 마스킹(이메일/전화번호) 치환 발생 횟수 합
    - normalized_hits: 정규화 치환 발생 횟수 합
    """
    processed: int
    masked_hits: int
    normalized_hits: int


def init_worker() -> None:
    """
    multiprocessing.Pool 워커 초기화 함수
    - Regex 컴파일을 워커 시작 시 1회 수행하여 반복 오버헤드를 제거한다.
    """
    global EMAIL_RE, PHONE_RE, BADWORD_RE, BADWORD_MAP

    # 이메일 정규표현식(단순 실습용)
    EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

    # 전화번호(한국형 예시 중심)
    # - 010-1234-5678, 01012345678, 02-123-4567 등 일부 케이스 포함
    PHONE_RE = re.compile(
        r"\b(?:0\d{1,2}[- ]?\d{3,4}[- ]?\d{4})\b"
    )

    # 금칙어/비표준 표현 → 표준 표현(실습용 예시)
    # - 실제 운영에서는 정책에 따라 더 체계적으로 관리(사전/DB/룰셋)
    BADWORD_MAP = {
        "wtf": "what the heck",
        "omg": "oh my gosh",
        "damn": "darn",
        "idiot": "rude person",
        "stupid": "not smart",
    }

    # 여러 금칙어를 한 번에 잡기 위한 패턴(대소문자 무시)
    # 그룹 캡처로 매칭된 단어를 가져와 매핑한다.
    keys = "|".join(map(re.escape, BADWORD_MAP.keys()))
    BADWORD_RE = re.compile(rf"\b({keys})\b", flags=re.IGNORECASE)


def _require_initialized() -> None:
    """
    init_worker()가 호출되어 Regex가 준비되었는지 확인한다.
    단일 실행에서도 benchmark.py에서 init_worker()를 한 번 호출하도록 구성.
    """
    if EMAIL_RE is None or PHONE_RE is None or BADWORD_RE is None or BADWORD_MAP is None:
        raise RuntimeError("Regex not initialized. Call init_worker() before processing.")


def normalize_text(text: str) -> Tuple[str, int]:
    """
    금칙어/비표준 표현을 표준 표현으로 치환한다.
    반환:
    - (변환된 텍스트, 치환 횟수)
    """
    _require_initialized()
    assert BADWORD_RE is not None and BADWORD_MAP is not None

    hits = 0

    def repl(m: re.Match) -> str:
        nonlocal hits
        hits += 1
        word = m.group(1)
        # 대소문자 무시 매칭이므로 lower로 키 통일
        return BADWORD_MAP.get(word.lower(), word)

    new_text = BADWORD_RE.sub(repl, text)
    return new_text, hits


def mask_pii(text: str) -> Tuple[str, int]:
    """
    이메일/전화번호를 ****로 마스킹한다.
    반환:
    - (변환된 텍스트, 마스킹 치환 횟수 합)
    """
    _require_initialized()
    assert EMAIL_RE is not None and PHONE_RE is not None

    masked_hits = 0

    # 이메일 마스킹
    text, n1 = EMAIL_RE.subn("****", text)
    masked_hits += n1

    # 전화번호 마스킹
    text, n2 = PHONE_RE.subn("****", text)
    masked_hits += n2

    return text, masked_hits


def process_text(text: str) -> Tuple[str, int, int]:
    """
    하나의 텍스트를 (마스킹 -> 정규화) 순서로 처리한다.
    반환:
    - (처리된 텍스트, masked_hits, normalized_hits)
    """
    masked_text, masked_hits = mask_pii(text)
    normalized_text, normalized_hits = normalize_text(masked_text)
    return normalized_text, masked_hits, normalized_hits


def process_chunk(chunk: List[str]) -> ProcessStats:
    """
    리스트(청크) 단위로 처리한다.
    주의:
    - IPC 비용을 줄이기 위해, 대규모 결과 텍스트 전체를 부모 프로세스로 반환하지 않고
      통계만 반환한다(실습 목적: 처리량 비교).
    """
    processed = 0
    masked_total = 0
    normalized_total = 0

    for t in chunk:
        _, mh, nh = process_text(t)
        processed += 1
        masked_total += mh
        normalized_total += nh

    return ProcessStats(processed=processed, masked_hits=masked_total, normalized_hits=normalized_total)
