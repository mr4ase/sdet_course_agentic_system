# nodes\progress_manager.py

from pathlib import Path

from graph.state import State
from config import PROGRESS_FILE_PATH, THE_USER
from src.curriculum import load_curriculum
from src.progress import load_progress, save_progress, init_progress

progress_file_path = Path(PROGRESS_FILE_PATH)
curriculum = load_curriculum()
the_user = THE_USER

if not progress_file_path.exists():
    progress = init_progress(curriculum, the_user)
    save_progress(progress)


def progress_manager(state: State) -> dict:
    return {
        "curriculum": curriculum,
        "progress": load_progress(),
        "task_result": None,
        "review": None,
    }  # TODO: progress_manager перечитывает progress с диска на каждом новом проходе графа. Неэффективно. Переделать позже, когда мутации данных во время работы графа станут многочисленны и существенны (после ступени 9, например). Нужен будет один источник ответственности для данных progress в state - или MemorySaver или файл progress. Лучше - MemorySaver.
