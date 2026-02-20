import tracemalloc
import time

class MemoryProfiler:
    """
    특정 로직의 메모리 점유율과 실행 시간을 측정하는 엔진
    """
    @staticmethod
    def profile(func, *args, **kwargs):
        # 메모리 추적 시작
        tracemalloc.start()
        start_time = time.time()
        
        # 대상 함수 실행
        result_data = func(*args, **kwargs)
        
        # 측정 값 수집
        current, peak = tracemalloc.get_traced_memory()
        elapsed_time = time.time() - start_time
        tracemalloc.stop()
        
        # 결과 반환 (메모리는 MB 단위로 변환)
        return {
            'peak_memory_mb': peak / 1024 / 1024,
            'elapsed_time': elapsed_time
        }

def run_list_comprehension(n):
    """Eager Evaluation: 리스트 전체를 즉시 생성"""
    return [i for i in range(n)]

def run_generator_expression(n):
    """Lazy Evaluation: 제너레이터 규칙만 생성"""
    return (i for i in range(n))