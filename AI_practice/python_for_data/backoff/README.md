# bcrypt + IP별 실패 기록 + Exponential Backoff (Codelab ②)

## 작성자
황다빈

## 작성일
2026-02-19

---

## 1. 실습 목표
- bcrypt로 비밀번호를 안전하게 검증
- 메모리(Dictionary)에 IP별 실패 횟수를 기록
- 연속 실패 시 지수 백오프(Exponential Backoff)로 재시도를 지연시켜
  무차별 대입 공격을 물리적으로 차단(지연)

---

## 2. 프로젝트 파일 구성(권장 파일명)
- auth_backoff.py
- demo_run.py
- requirements.txt

---

## 3. 실행 환경
- VSCode + Ubuntu Terminal
- Python 3.10+ 권장

---

## 4. 가상환경 생성 및 패키지 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. 실행 방법
```bash
python demo_run.py
```