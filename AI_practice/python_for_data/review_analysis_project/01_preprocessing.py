"""
작성자: 황다빈
작성일: 2026-02-19
과정명: 파이썬 3일차 - 16. 시각화
코드 목적:
    reviews.csv 데이터를 불러와 결측치 처리,
    텍스트 길이 재계산, 이상치 탐지(IQR) 수행

상세 설명:
    - review_text, sentiment_score 결측 제거
    - review_length 재계산
    - IQR 기반 이상치 탐지
    - 전처리 결과를 cleaned_reviews.csv로 저장
"""

import pandas as pd
import numpy as np

# 1. 데이터 로드
df = pd.read_csv("reviews.csv")

print("원본 데이터 크기:", df.shape)

# 2. 결측치 확인
print("\n결측치 확인:")
print(df.isna().sum())

# 3. 결측치 제거
df = df.dropna(subset=["review_text", "sentiment_score"])

# 4. review_length 재계산
df["review_length"] = df["review_text"].astype(str).str.len()
df["num_words"] = df["review_text"].astype(str).str.split().str.len()

# 5. IQR 이상치 탐지 함수
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return lower, upper

lower, upper = detect_outliers_iqr(df["review_length"])

print("\nReview Length 이상치 범위:", lower, "~", upper)

# 이상치 개수
outliers = df[(df["review_length"] < lower) | (df["review_length"] > upper)]
print("이상치 개수:", len(outliers))

# 저장
df.to_csv("cleaned_reviews.csv", index=False)
print("\n전처리 완료 → cleaned_reviews.csv 저장")