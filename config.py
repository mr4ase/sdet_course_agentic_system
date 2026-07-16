# config.py

LLM_MODEL = "gemini-2.5-flash"
PROGRESS_FILE_PATH = "data/progress.json"
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
