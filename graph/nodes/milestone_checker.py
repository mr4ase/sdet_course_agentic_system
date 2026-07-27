# graph\nodes\milestone_checker.py

from pathlib import Path

from graph.state import State
from loguru_config import logger
from src.utils import milestone_status, find_by_id
from src.pytest_runner import run_pytest, write_code_to_file
from config import USER_DIR


def milestone_checker(state: State) -> dict:

    progress = state["progress"]
    project_plan = state["project_plan"]
    project_state = state["project_state"]

    current_milestone = project_state["current_milestone"]

    if current_milestone in project_state["closed_milestones"]:
        logger.info(
            f"Current milestone {current_milestone} already in closed milestones list {project_state['closed_milestones']}"
        )
        return {}

    if milestone_status(current_milestone, progress, project_plan):
        milestone = find_by_id(project_plan["milestones"], current_milestone)
        user_dir = Path(USER_DIR).resolve()

        checktest_file = write_code_to_file(
            user_dir,
            f"test_milestone_{current_milestone}.py".replace("-", "_"),
            milestone["done_check"],
        )
        try:
            check_milestone_result = run_pytest(user_dir, checktest_file)
        finally:
            checktest_file.unlink()
            logger.debug(f"Checktest_file {checktest_file} deleted.")
        if check_milestone_result["return_code"] == 0:
            project_state["closed_milestones"].append(current_milestone)
            logger.info(
                f"Check milestone test passed. Current milestone {current_milestone} added to list of closed milestones."
            )
            check_milestone_result["goal"] = milestone["goal"]
        else:
            logger.warning(
                f"Milestone done_check failed. Return code of project folder pytest: {check_milestone_result['return_code']}"
            )

        return {
            "project_state": project_state,
            "milestone_result": check_milestone_result,
        }

    return {}
