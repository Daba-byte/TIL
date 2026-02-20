'''
작성자 : 황다빈
작성일 : 2026-02-12
내용 : 리스트와 딕셔너리를 활용한 데이터 처리 예제
'''

# 데이터-직원 정보 리스트
employees = [
    {"name": "Alice", "department": "Engineering", "age": 30, "salary": 85000},
    {"name": "Bob", "department": "Marketing", "age": 25, "salary": 60000},
    {"name": "Charlie", "department": "Engineering", "age": 35, "salary": 95000},
    {"name": "David", "department": "HR", "age": 45, "salary": 70000},
    {"name": "Eve", "department": "Engineering", "age": 28, "salary": 78000},
]

# 1. Engineering 부서에서 급여가 80000 이상인 직원의 이름을 리스트로 출력
engineering_high_salary = [
    e["name"] for e in employees
    if e["department"] == "Engineering" and e["salary"] >= 80000
]

# 2. 나이가 30세 이상인 직원의 이름과 부서를 튜플로 리스트에 저장
age_30_plus = [
    (e["name"], e["department"]) for e in employees if e["age"] >= 30
]

# 3. 급여가 가장 높은 상위 3명의 직원 이름과 급여를 튜플로 리스트에 저장
top_3_salary = sorted(
    employees, key=lambda x: x["salary"], reverse=True
)[:3]

top_3_result = [(e["name"], e["salary"]) for e in top_3_salary]

# 4. 부서별 평균 급여
from collections import defaultdict

dept_salary = defaultdict(list)
for e in employees:
    dept_salary[e["department"]].append(e["salary"])

avg_salary_by_dept = {
    dept: sum(salaries) / len(salaries)
    for dept, salaries in dept_salary.items()
}