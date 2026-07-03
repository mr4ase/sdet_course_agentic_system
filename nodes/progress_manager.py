# nodes\progress_manager.py

from pathlib import Path

from state import State
from config import PROGRESS_FILE_PATH, THE_USER
from curriculum import load_curriculum
from progress import load_progress, save_progress, init_progress

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
    }  # TODO: progress_manager перечитывает progress с диска на каждом проходе - при мутации прогресса в state (ступень 4+) переделать.
