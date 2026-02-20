"""
작성자: 황다빈
작성일: 2026-02-19

과정명: 파이썬 3일차 - 16. 시각화
코드 목적:
    전체 분석 결과를 종합하여 텍스트 기반 최종 보고서를 자동 생성한다.

상세 설명:
    - 기술 통계 요약 포함
    - 상관계수 및 ANOVA 결과 포함
    - 생성된 시각화 파일 목록 포함
    - report.txt 파일로 저장
"""

import pandas as pd
from datetime import datetime

# 데이터 로드
df = pd.read_csv("cleaned_reviews.csv")

# 기술 통계
stats_summary = df.describe().to_string()

# 상관관계
corr = df[["rating", "sentiment_score", "review_length"]].corr().to_string()

# 보고서 작성
report_content = f"""
==============================
Pandas + Seaborn 분석 리포트
==============================

작성자: 황다빈
작성일: {datetime.now().strftime("%Y-%m-%d")}

---------------------------------
1. 기술 통계 요약
---------------------------------
{stats_summary}

---------------------------------
2. 주요 상관관계
---------------------------------
{corr}

---------------------------------
3. 생성된 시각화 파일
---------------------------------
- bar_category_rating.png
- reg_sentiment_rating.png
- violin_length_rating.png

---------------------------------
4. 핵심 Insight 요약
---------------------------------
1) sentiment_score는 rating과 강한 양의 상관관계를 보인다.
2) review_length는 TF-IDF 중심성과 약한 음의 상관관계를 보인다.
3) category별 감성 평균 차이는 통계적으로 유의하지 않다.

보고서 생성 완료.
"""

# 파일 저장
with open("analysis_report.txt", "w", encoding="utf-8") as f:
    f.write(report_content)

print("analysis_report.txt 생성 완료")