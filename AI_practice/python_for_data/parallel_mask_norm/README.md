# parallel_mask_norm

## 목표
- 수백만 건 리뷰 텍스트에서 개인정보(이메일/전화번호)를 마스킹(****)하고
- 금칙어/비표준 표현을 표준 표현으로 정규화(Normalization)하는 배치 프로세서를 구현
- 단일 프로세스 vs 멀티프로세스(Pool)로 실행 시간을 비교

## 실행
```bash
python3 benchmark.py
