# nodes\progress_manager.py

from pathlib import Path

from graph.state import State
from config import PROGRESS_FILE_PATH, THE_USER, PROJECT_STATE_FILE_PATH
from src.curriculum import load_curriculum
from src.project_plan import load_project_plan
from src.progress import load_progress, save_progress, init_progress
from src.project_state import load_project_state, init_project_state, save_project_state

from loguru_config import logger

progress_file_path = Path(PROGRESS_FILE_PATH)
project_state_file_path = Path(PROJECT_STATE_FILE_PATH)
curriculum = load_curriculum()
project_plan = load_project_plan()
the_user = THE_USER

if not progress_file_path.exists():
    progress = init_progress(curriculum, the_user)
    save_progress(progress)

if not project_state_file_path.exists():
    project_state = init_project_state(project_plan)
    save_project_state(project_state)


# logger.info(f"")


def progress_manager(state: State) -> dict:
    return {
        "curriculum": curriculum,
        "progress": load_progress(),
        "task_result": None,
        "review": None,
        "project_state": load_project_state(),
        "project_plan": project_plan,
    }  # TODO: progress_manager перечитывает progress с диска на каждом новом проходе графа. Неэффективно. Переделать позже, когда мутации данных во время работы графа станут многочисленны и существенны (после ступени 9, например). Нужен будет один источник ответственности для данных progress в state - или MemorySaver или файл progress. Лучше - MemorySaver.
