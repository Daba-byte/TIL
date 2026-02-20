"""
작성자: 황다빈
작성일: 2026-02-19
코드 목적:
    기술 통계 및 주요 시각화 수행

상세 설명:
    - 기술통계 요약
    - 카테고리별 평균 평점 barplot
    - 평점 vs 감성점수 regplot
    - 텍스트 길이 vs 평점 violinplot
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_reviews.csv")

print("\n기술 통계 요약")
print(df.describe())

# 1. 카테고리별 평균 평점
plt.figure(figsize=(8,5))
sns.barplot(x="category", y="rating", data=df, estimator="mean")
plt.title("Category별 평균 평점")
plt.ylim(0,5)
plt.tight_layout()
plt.savefig("bar_category_rating.png")
plt.close()

# 2. 평점 vs 감성 점수
plt.figure(figsize=(6,5))
sns.regplot(x="sentiment_score", y="rating", data=df)
plt.title("Sentiment Score vs Rating")
plt.tight_layout()
plt.savefig("reg_sentiment_rating.png")
plt.close()

# 3. 텍스트 길이 vs 평점
plt.figure(figsize=(8,5))
sns.violinplot(x="rating", y="review_length", data=df)
plt.title("Review Length by Rating")
plt.tight_layout()
plt.savefig("violin_length_rating.png")
plt.close()

print("\n시각화 완료 (png 파일 생성)")