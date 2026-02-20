import os
from dotenv import load_dotenv
from memory_engine import MemoryProfiler, run_list_comprehension, run_generator_expression

# 환경 변수 로드
load_dotenv()

def main():
    # 1. 설정값 로드 (기본값 1,000,000)
    data_size = int(os.getenv("DATA_SIZE", 1000000))
    
    print(f"대용량 데이터 파이프라인 성능 분석")
    print(f"   - 데이터 사이즈: {data_size:,} 개")
    print("=" * 45)

    # 2. List Comprehension 측정
    print("[1] List Comprehension (Eager Evaluation) 측정 중...")
    list_res = MemoryProfiler.profile(run_list_comprehension, data_size)
    
    print(f"Peak Memory: {list_res['peak_memory_mb']:.2f} MB")
    print(f"Time Taken: {list_res['elapsed_time']:.4f} sec")
    print("-" * 45)

    # 3. Generator Expression 측정
    print("[2] Generator Expression (Lazy Evaluation) 측정 중...")
    gen_res = MemoryProfiler.profile(run_generator_expression, data_size)
    
    print(f"Peak Memory: {gen_res['peak_memory_mb']:.2f} MB")
    print(f"Time Taken: {gen_res['elapsed_time']:.4f} sec")
    print("=" * 45)

    # 4. 결론 도출 (비즈니스 인사이트)
    efficiency = list_res['peak_memory_mb'] / (gen_res['peak_memory_mb'] + 1e-9)
    print(f"분석 결과: Generator가 List보다 약 {efficiency:.1f}배 메모리 효율적입니다.")

if __name__ == "__main__":
    main()