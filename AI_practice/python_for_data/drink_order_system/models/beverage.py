"""
파일명: beverage.py
설명: 음료 객체를 정의하는 클래스
작성일: 2026-02-13
작성자: 황다빈

파라미터:
- name (str): 음료 이름
- price (int): 음료 가격
- tags (list[str]): 음료 태그 정보
"""

class Beverage:
    def __init__(self, name: str, price: int, tags: list):
        self.name = name
        self.price = price
        self.tags = tags

    def __str__(self):
        return f"{self.name} - {self.price}원 / 태그: {', '.join(self.tags)}"
