"""
파일명: order.py
설명: 사용자 주문 내역을 관리하는 클래스
작성일: 2026-02-13
작성자: 황다빈

기능:
- 주문 추가
- 총 금액 계산
- 평균 금액 계산
"""

from config.settings import TAX_RATE

class Order:
    def __init__(self):
        self.order_history = []

    def add_order(self, beverage):
        """주문 추가"""
        self.order_history.append(beverage)

    def calculate_total(self):
        """총 주문 금액 계산 (세금 포함)"""
        total = sum(item.price for item in self.order_history)
        tax = total * TAX_RATE
        return int(total + tax)

    def calculate_average(self):
        """평균 주문 금액 계산"""
        if not self.order_history:
            return 0
        return int(self.calculate_total() / len(self.order_history))

    def get_recent_order(self):
        """가장 최근 주문 반환"""
        if not self.order_history:
            return None
        return self.order_history[-1]
