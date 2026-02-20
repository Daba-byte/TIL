"""
파일명: recommendation_service.py
설명: 최근 주문 태그 기반 음료 추천 서비스
작성일: 2026-02-13
작성자: 황다빈

기능:
- 최근 주문 음료 태그와 유사한 음료 추천
"""

class RecommendationService:

    @staticmethod
    def recommend(menu: list, recent_beverage):
        if not recent_beverage:
            return []

        recommendations = []

        for beverage in menu:
            # 자기 자신 제외
            if beverage.name == recent_beverage.name:
                continue

            # 태그 교집합 존재 여부 확인
            if set(beverage.tags) & set(recent_beverage.tags):
                recommendations.append(beverage)

        return recommendations
