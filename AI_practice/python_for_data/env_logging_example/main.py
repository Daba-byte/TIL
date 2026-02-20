import logging
import os
from dotenv import load_dotenv

# 1) .env 로드
load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO")
app_name = os.getenv("APP_NAME", "DefaultApp")

# 2) 로그 레벨 설정
numeric_level = getattr(logging, log_level.upper(), logging.INFO)

# 3) 로거 생성
logger = logging.getLogger(app_name)
logger.setLevel(numeric_level)

# 4) 로그 포맷 설정
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# 5) 파일 핸들러 설정
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(numeric_level)
file_handler.setFormatter(formatter)

# 6) 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setLevel(numeric_level)
console_handler.setFormatter(formatter)

# 7) 핸들러 추가
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 8) 로그 출력 테스트
logger.info("앱 실행 시작")
logger.debug("환경 변수 로딩 완료")

try:
    1 / 0
except ZeroDivisionError:
    logger.error("예외 발생 예시", exc_info=True)
