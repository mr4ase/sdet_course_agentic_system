# config.py

LLM_MODEL = "gemini-2.5-flash"
PROGRESS_FILE_PATH = "data/progress.json"
PROJECT_STATE_FILE_PATH = "data/project_state.json"
PROJECT_PLAN_FILE_PATH = "data/project_plan.json"
CURRICULUM_FILE_PATH = "data/curriculum.json"
USER_DIR = "student_workflow/"
THE_USER = "John Doe"
RUN_TEST_TIMEOUT = 5  # parameter for subprocess.run in seconds

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
}

SYSTEM_ERROR_FALLBACK = (
    "Не удалось прогнать тест по внутренней причине. "
    "Это сбой на нашей стороне, не связанный с твоим кодом. "
    "Попробуй ещё раз чуть позже."
)
