"""
파일명: decorator.py
설명:
- 데코레이터와 클로저 구조를 활용하여 함수 실행 시간을 측정하는 프로그램
- measure_time 데코레이터를 정의하고 slow_function에 적용

작성일: 2026-02-13
작성자: 황다빈

실행 방법:
$ python decorator.py

구성:
1. measure_time(func)
   - 어떤 함수든 감싸서 실행 시간을 측정
   - 실행 결과는 그대로 반환
   - 실행 시간은 콘솔에 출력

2. slow_function(delay)
   - 의도적으로 지연을 발생시키는 테스트 함수
   - delay(초) 만큼 sleep 후 결과 반환
"""

import time


def measure_time(func):
    """
    함수 실행 시간을 측정하는 데코레이터

    매개변수:
    - func: 실행 시간을 측정할 함수

    반환값:
    - wrapper 함수 (클로저)
    """

    def wrapper(*args, **kwargs):
        """
        실제 함수 실행을 감싸는 내부 함수 (클로저)

        *args, **kwargs:
        - 어떤 함수든 받을 수 있도록 가변 인자 처리
        """

        start_time = time.time()  # 시작 시간 기록

        result = func(*args, **kwargs)  # 원래 함수 실행

        end_time = time.time()  # 종료 시간 기록

        execution_time = end_time - start_time

        print(f"{func.__name__} took {execution_time:.4f} seconds")

        return result  # 원래 함수의 결과 그대로 반환

    return wrapper


@measure_time
def slow_function(delay):
    """
    의도적으로 실행 지연을 발생시키는 함수

    매개변수:
    - delay (int or float): 지연시킬 초(second)

    반환값:
    - 문자열 결과
    """

    time.sleep(delay)
    return f"{delay}초 동안 실행 완료"


def main():
    print("프로그램 시작")

    result = slow_function(2)

    print("함수 반환값:", result)

    print("프로그램 종료")


if __name__ == "__main__":
    main()