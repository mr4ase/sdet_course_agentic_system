# config.py

import os

from dotenv import load_dotenv

load_dotenv()

# LLM_MODEL = "gemini-2.5-flash"
LLM_PROVIDER = "deepseek"
PROGRESS_FILE_PATH = "data/progress.json"
PROJECT_STATE_FILE_PATH = "data/project_state.json"
PROJECT_PLAN_FILE_PATH = "data/project_plan.json"
CURRICULUM_FILE_PATH = "data/curriculum.json"
DOCKER_TEMP_DIR = "/sandbox"
USER_DIR = "student_workflow"
THE_USER = "John Doe"
RUN_TEST_TIMEOUT = 15  # parameter for subprocess.run in seconds
CRITERIA_PASSED_SCORE = 10
FAILS_THRESHOLD = 2

# summary parameters
MAX_TOKEN_BEFORE_SUMMARY = 10000
MAX_TOKENS = 4000
MAX_SUMMARY_TOKENS = 2000

MESSAGES_TO_KEEP_IN_HISTORY = 6

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# llm model names and parameters
LLM_MODEL = {
    "deepseek": {
        "model_name": "deepseek-flash",
        "base_url": "https://api.deepseek.com",
        "api_key": DEEPSEEK_API_KEY,
        "client": "openai",
        "structured_output_method": "function_calling",
        "extra_body": {"thinking": {"type": "disabled"}},
    },
    "gemini": {
        "model_name": "gemini-2.5-flash",
        "api_key": GOOGLE_API_KEY,
        "client": "google",
        "structured_output_method": "json_schema",
    },
    "local_lm_studio": {
        "model_name": "meta-llama-3.1-8b-instruct@q6_k",
        "base_url": "http://localhost:1234/v1",
        "api_key": "not-needed",
        "client": "openai",
        "structured_output_method": "json_schema",
    },
}


RETURN_CODES = {
    0: "passed",
    1: "test_failed",
    2: "test_interrupted",
    3: "pytest_internal_error",
    4: "pytest_usage_error",
    5: "no_tests_found",
    6: "max_warnings_exceeded",
    7: "timeout_expired",
    8: "no_code_in_message",
    9: "docker_not_ available",
    10: "docker_memory_is_exceeded",
}

SYSTEM_ERROR_MESSAGES = {
    3: "Не удалось прогнать тест из-за внутренней ошибки среды запуска. "
    "Это сбой на нашей стороне, а не проблема в твоём коде. "
    "Попробуй отправить решение ещё раз через минуту.",
    4: "Тест не удалось запустить из-за ошибки конфигурации системы проверки. "
    "Это не связано с твоим кодом. "
    "Попробуй ещё раз, и если повторится — сообщи преподавателю.",
    6: "Прогон теста был прерван системой из-за слишком большого числа предупреждений. "
    "Это внутреннее ограничение проверки, а не ошибка в твоём решении. "
    "Попробуй отправить код ещё раз.",
    9: "Не удалось запустить среду проверки. "
    "Это сбой на нашей стороне, не связанный с твоим кодом. "
    "Попробуй ещё раз чуть позже.",
}

SYSTEM_ERROR_FALLBACK = (
    "Не удалось прогнать тест по внутренней причине. "
    "Это сбой на нашей стороне, не связанный с твоим кодом. "
    "Попробуй ещё раз чуть позже."
)


# TODO: task-000003 обращается к внешней сети (httpbin.org), а в песочнице
# она отключена (--network none), задание в ней не пройдёт. Решение: второй
# контейнер с локальным тестовым сервером во внутренней сети Docker.
