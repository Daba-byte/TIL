"""
작성자: 황다빈
작성일: 2026-02-19

과정명: 파이썬 3일차 - Codelab ②
코드 목적:
    bcrypt를 사용하여 비밀번호를 검증하고,
    메모리(Dictionary)에 IP별 로그인 실패 횟수를 기록하며,
    연속 실패 시 지수 백오프(Exponential Backoff)로 재시도를 지연시켜
    무차별 대입 공격을 물리적으로 차단(지연)하는 알고리즘을 구현한다.

상세 설명:
    - bcrypt.hashpw / bcrypt.checkpw로 안전한 패스워드 검증
    - ip_state 딕셔너리에 IP별 상태 저장:
        { ip: {"fails": int, "blocked_until": float} }
    - 실패가 누적될수록 대기 시간이 2^n 형태로 증가(최대 max_delay까지)
    - 성공 시 해당 IP의 실패 카운트와 차단 시간을 초기화
    - 시간 측정은 time.monotonic() 사용(시스템 시간 변경 영향 최소화)

백오프 정책(보고서용 명시):
    - allow_free_fails(기본 1회)까지는 즉시 재시도 허용
    - 그 이후부터는 delay = base_delay * 2^(fails - allow_free_fails - 1)
    - delay는 max_delay를 넘지 않도록 제한
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Tuple

import bcrypt


@dataclass
class IPRecord:
    """IP별 인증 실패/차단 상태를 메모리에 보관하기 위한 데이터 구조"""
    fails: int = 0
    blocked_until: float = 0.0  # time.monotonic() 기준


class LoginProtector:
    """
    bcrypt 기반 로그인 검증 + IP별 실패 기록 + 지수 백오프 차단 로직
    """

    def __init__(
        self,
        correct_password_plain: str,
        base_delay: float = 1.0,
        max_delay: float = 32.0,
        allow_free_fails: int = 1,
    ) -> None:
        """
        Args:
            correct_password_plain: 정답 비밀번호(데모용). 실무에서는 DB/Secret Manager 등에 저장.
            base_delay: 백오프 지연의 기본 단위(초)
            max_delay: 백오프 지연의 상한(초)
            allow_free_fails: 몇 회까지는 지연 없이 재시도 허용할지(사용자 편의)
        """
        self.base_delay = float(base_delay)
        self.max_delay = float(max_delay)
        self.allow_free_fails = int(allow_free_fails)

        # bcrypt는 salt 포함 해시를 저장하는 방식
        self._pw_hash = bcrypt.hashpw(correct_password_plain.encode("utf-8"), bcrypt.gensalt())

        # IP별 상태 저장 (메모리)
        self.ip_state: Dict[str, IPRecord] = {}

    def _now(self) -> float:
        return time.monotonic()

    def _get_record(self, ip: str) -> IPRecord:
        if ip not in self.ip_state:
            self.ip_state[ip] = IPRecord()
        return self.ip_state[ip]

    def _compute_backoff_delay(self, fails: int) -> float:
        """
        fails가 증가할수록 지연 시간을 지수적으로 증가시킴.
        allow_free_fails까지는 지연 0초.
        """
        if fails <= self.allow_free_fails:
            return 0.0

        # 예: allow_free_fails=1
        # fails=2 -> 1s, fails=3 -> 2s, fails=4 -> 4s ...
        exp = fails - self.allow_free_fails - 1
        delay = self.base_delay * (2 ** exp)
        return min(delay, self.max_delay)

    def attempt_login(self, ip: str, password_plain: str) -> Tuple[bool, str]:
        """
        로그인 시도 1회 처리

        Returns:
            (성공 여부, 메시지)
        """
        record = self._get_record(ip)
        now = self._now()

        # 차단 시간 내라면 즉시 거절
        if now < record.blocked_until:
            remaining = record.blocked_until - now
            return False, f"[BLOCKED] IP={ip} 남은 대기시간: {remaining:.2f}s (fails={record.fails})"

        # bcrypt 검증
        ok = bcrypt.checkpw(password_plain.encode("utf-8"), self._pw_hash)

        if ok:
            # 성공 시 초기화
            record.fails = 0
            record.blocked_until = 0.0
            return True, f"[SUCCESS] IP={ip} 로그인 성공 → 실패 카운트 초기화"

        # 실패 처리
        record.fails += 1
        delay = self._compute_backoff_delay(record.fails)
        if delay > 0:
            record.blocked_until = now + delay
            return False, f"[FAIL] IP={ip} 비밀번호 오류 → backoff {delay:.2f}s 적용 (fails={record.fails})"
        else:
            record.blocked_until = 0.0
            return False, f"[FAIL] IP={ip} 비밀번호 오류 → 지연 없음 (fails={record.fails})"