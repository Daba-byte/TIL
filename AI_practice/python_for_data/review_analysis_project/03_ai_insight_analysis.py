"""
작성자: 황다빈
작성일: 2026-02-19
코드 목적:
    AI 분석 관점에서 인사이트 도출

상세 설명:
    - sentiment_score와 rating 상관관계
    - review_length와 임베딩 유사도 관계 분석
    - category별 감성 평균 차이 검정(ANOVA)
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("cleaned_reviews.csv")

# 1. 상관관계 분석
corr = df[["rating", "sentiment_score", "review_length"]].corr()
print("\n상관계수:")
print(corr)

# 2. TF-IDF 기반 유사도 계산
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["review_text"])

categories = df["category"].unique()
centroids = {}

for cat in categories:
    idx = df["category"] == cat
    centroids[cat] = X[idx].mean(axis=0)

similarities = []
for i in range(len(df)):
    cat = df.iloc[i]["category"]
    sim = cosine_similarity(X[i], np.asarray(centroids[cat]))[0][0]
    similarities.append(sim)

df["tfidf_similarity"] = similarities

print("\nreview_length vs similarity 상관:")
print(df[["review_length", "tfidf_similarity"]].corr())

# 3. ANOVA
groups = [df[df["category"] == c]["sentiment_score"] for c in categories]
anova = stats.f_oneway(*groups)

print("\nANOVA 결과:")
print(anova)