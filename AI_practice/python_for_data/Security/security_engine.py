import ast

class SecurityScanner(ast.NodeVisitor):
    """
    AST를 활용한 정적 코드 분석 엔진
    """
    def __init__(self, forbidden_list):
        self.forbidden_functions = forbidden_list
        self.violations = []

    def visit_Call(self, node):
        func_name = ""
        # 함수 호출 방식에 따른 이름 추출
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                func_name = f"{node.func.value.id}.{node.func.attr}"

        if func_name in self.forbidden_functions:
            self.violations.append({
                'function': func_name,
                'line': node.lineno,
                'column': node.col_offset
            })
        self.generic_visit(node)

def analyze_file(file_path, forbidden_list):
    """파일을 읽어 분석 결과를 반환하는 비즈니스 인터페이스"""
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    tree = ast.parse(source)
    scanner = SecurityScanner(forbidden_list)
    scanner.visit(tree)
    return scanner.violations