"""
작성자: 황다빈
작성일: 2026-02-19

과정명: 파이썬 3일차 - Codelab ②
코드 목적:
    LoginProtector를 이용해
    - 동일 IP에서 연속 실패 시 백오프가 증가하는지
    - 차단 구간에서 즉시 거절되는지
    - 성공 시 실패 카운트가 초기화되는지
    를 재현 가능한 형태로 출력하여 화면 캡처가 가능하도록 한다.

상세 설명:
    - IP A: 연속 실패 → 차단 → 재시도 거절 → 시간 경과 후 재시도
    - IP B: 다른 IP는 별도 상태로 관리됨(격리)
"""

import time
from auth_backoff import LoginProtector


def main() -> None:
    protector = LoginProtector(
        correct_password_plain="P@ssw0rd!",
        base_delay=1.0,
        max_delay=8.0,
        allow_free_fails=1,  # 1회까지는 사용자 편의상 지연 없음
    )

    ip_a = "203.0.113.10"
    ip_b = "203.0.113.20"

    print("=== Demo Start: bcrypt + IP별 실패 기록 + Exponential Backoff ===\n")
    print("정답 비밀번호: P@ssw0rd!\n")

    # IP A: 1회 실패(지연 없음) -> 2회 실패(1s 차단) -> 차단 중 재시도 -> 대기 후 재시도
    attempts_a = ["wrong1", "wrong2", "wrong3", "P@ssw0rd!"]

    for i, pw in enumerate(attempts_a, start=1):
        ok, msg = protector.attempt_login(ip_a, pw)
        print(f"[IP A Attempt #{i}] pw='{pw}' => {msg}")

        # 일부러 차단 구간에서 바로 재시도하도록 sleep을 짧게 줌
        time.sleep(0.3)

    print("\n--- IP A: 차단 해제 대기(약 2~3초) 후 재시도 ---")
    time.sleep(3.0)
    ok, msg = protector.attempt_login(ip_a, "P@ssw0rd!")
    print(f"[IP A After Wait] => {msg}")

    # IP B: 다른 IP는 별도 상태(격리)임을 보여줌
    print("\n--- IP B: 별도 IP는 별도 카운트로 관리됨 ---")
    for i in range(1, 4):
        ok, msg = protector.attempt_login(ip_b, "wrongX")
        print(f"[IP B Attempt #{i}] => {msg}")
        time.sleep(0.3)

    print("\n=== Demo End ===")


if __name__ == "__main__":
    main()
