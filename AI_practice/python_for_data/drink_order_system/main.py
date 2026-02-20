"""
파일명: main.py
설명: 온라인 음료 주문 추천 시스템 실행 파일
작성일: 2026-02-13
작성자: 황다빈

실행 방법:
$ python main.py

기능:
1. 음료 메뉴 정의
2. 사용자 주문 진행
3. 최근 주문 기반 추천
4. 총 금액 및 평균 금액 출력
"""

from models.beverage import Beverage
from models.order import Order
from services.recommendation_service import RecommendationService


def create_menu():
    """메뉴 생성"""
    return [
        Beverage("아이스 아메리카노", 3000, ["커피", "콜드"]),
        Beverage("카페라떼", 3500, ["커피", "밀크"]),
        Beverage("녹차", 2800, ["차", "뜨거운"]),
        Beverage("허브티", 3000, ["차", "차가운"]),
    ]


def main():
    menu = create_menu()
    order = Order()

    print("===== 음료 메뉴 =====")
    for idx, beverage in enumerate(menu):
        print(f"{idx + 1}. {beverage}")

    # 사용자 임의 주문 (예시)
    order.add_order(menu[0])  # 아이스 아메리카노
    order.add_order(menu[1])  # 카페라떼

    print("\n===== 주문 내역 =====")
    for item in order.order_history:
        print(item.name)

    # 추천 시스템 실행
    recent = order.get_recent_order()
    recommendations = RecommendationService.recommend(menu, recent)

    print("\n===== 추천 음료 =====")
    for rec in recommendations:
        print(rec.name)

    print("\n===== 결제 정보 =====")
    print(f"총 금액: {order.calculate_total()}원")
    print(f"평균 금액: {order.calculate_average()}원")


if __name__ == "__main__":
    main()
