# SDET Course Agentic System

An AI tutor that teaches test automation in Python. A student gets a short lesson and a practical task, sends back their code, and the system **runs it with pytest, reviews its quality, and gives guided feedback**: hints and questions instead of ready-made answers.

It is built as a multi-step workflow with [LangGraph](https://github.com/langchain-ai/langgraph), where each step is a small, separate piece of logic (present a lesson, run tests, review code, re-explain a topic, and so on).

> **Status:** work in progress. The core learning loop works end to end in the console. A chat interface and a full course are not built yet (see [Status and roadmap](#status-and-roadmap)).
>
> The tutor talks to students in **Russian**, so lesson texts and prompts are in Russian.

## What it does

1. **Presents a lesson.** Shows the key points of the topic and gives one practical task.
2. **Runs the student's code.** Code sent in a ```` ```python ```` block is saved to a file and executed with pytest inside a Docker container with no network access, a memory limit and a time limit, so a broken, endless or malicious script cannot hang or harm the host.
3. **Reviews the code.** An LLM checks the code against the task's criteria and four general quality patterns (meaningful names, no magic values, no duplication, readable structure) and returns a structured verdict with comments and a score from 0 to 10.
4. **Tutors, does not solve.** The tutor explains what happened (test passed or failed, and why), points out the main problem and the strengths, and guides the student with questions.
5. **Re-explains when the student is stuck.** If the student writes that they do not understand, or writes without code after failing a task twice in a row, the topic is explained again, simpler each time.
6. **Tracks a growing project.** Some tasks build one test project step by step. Every new submission also re-runs all earlier tests, so the tutor can say "your new code is fine, but it broke a test you wrote before."
7. **Checks milestones.** When all tasks of a project milestone are passed, the system runs a milestone check and the tutor celebrates the achievement.
8. **Waits for confirmation.** When a lesson is finished, the workflow pauses and asks the student before moving on.

## How it works

![Workflow graph](img/graph.png)

Every student message enters at `progress_manager` and is routed by simple rules:

| Student message | Route |
| --- | --- |
| Task not shown yet | `presenter` shows the lesson and the task |
| Contains a Python code block | `test_runner` → `reviewer` → (`milestone_checker`) → `tutor_llm` |
| Plain text, asks for help | `remediation_classifier` → `remediator` (re-explanation) |
| Plain text, anything else | `remediation_classifier` → `tutor_llm` |
| Plain text after two failed attempts in a row | `remediator` (skips the classifier) |
| pytest crashed for internal reasons | `system_error_handler` tells the student it is not their fault |

Two kinds of tasks are supported: **drill** tasks run in an isolated temporary folder, **project** tasks run inside the student's own project folder together with all previous tests.

Conversation memory: when the dialogue gets long, older messages are summarized with [LangMem](https://github.com/langchain-ai/langmem), so the context stays small.

## Project structure

```
main.py              Console entry point (demo session)
config.py            Settings: model name, timeouts, thresholds, file paths
graph/
  graph.py           Builds and compiles the LangGraph workflow
  state.py           Shared state passed between steps
  nodes/             Steps: presenter, test_runner, reviewer, tutor, remediator, ...
  edges/             Routing rules between steps
schema/              Pydantic models for structured LLM output
system_prompts/      Prompts for each LLM role
src/                 Helpers: pytest runner, progress and project-state storage, LLM setup
data/
  curriculum.json    Modules, lessons, tasks and their criteria
  project_plan.json  Project milestones
  patterns.json      Code-quality patterns used by the reviewer
img/graph.png        Diagram of the workflow
```

## Tech stack

Python · LangGraph · LangChain · LangMem · Pydantic · pytest · Docker · Loguru · DeepSeek (main model) · Google Gemini (fallback) · LM Studio (local model)

The model is selected in one place: `LLM_PROVIDER` in `config.py`.

## Getting started

Requirements:

- Linux, or Ubuntu in WSL 2 on Windows. On WSL, clone the repository into the Linux file system (for example `~/dev`), not into `/mnt/c`: files on the Windows drive are slow and break file permissions inside Docker containers.
- Python 3.12+
- Docker (on Windows: Docker Desktop with WSL integration enabled for your Ubuntu distribution)
- An API key for DeepSeek or Google Gemini

```bash
# 1. Create and activate a virtual environment
#    (on Ubuntu, install the venv module first: sudo apt install python3-venv)
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build the sandbox image used to run student code
docker build -t sdet-runner .

# 4. Add your API key(s) to .env
echo "DEEPSEEK_API_KEY=your-key-here" >> .env
echo "GOOGLE_API_KEY=your-key-here" >> .env

# 5. Run the demo session
python main.py
```

### Choosing the model

The model is selected by `LLM_PROVIDER` in `config.py`:

| Value | Model | Needs |
| --- | --- | --- |
| `deepseek` (default) | `deepseek-flash` | `DEEPSEEK_API_KEY` |
| `gemini` | `gemini-2.5-flash` | `GOOGLE_API_KEY` |
| `local_lm_studio` | a local model in LM Studio | LM Studio server running on port 1234 |

Model names, server addresses and provider-specific options live in the `LLM_MODEL` dictionary in `config.py`.

To use LM Studio running on Windows from WSL, enable mirrored networking so that `localhost` is shared between Windows and Linux. Add to `%USERPROFILE%\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

then run `wsl --shutdown` in PowerShell and reopen Ubuntu.

What to expect:

- The first run creates `data/progress.json`, `data/project_state.json` and the `student_workflow/` folder, then shows the first lesson and task. The next run continues from the saved progress.
- `main.py` is a simple demo: it sends one hard-coded student message. To try the review flow, edit `test_msg_for_tutor` in `main.py` so that it contains a ```` ```python ```` block with your solution, then run it again.
- After a lesson is completed, the console asks whether to move on (`да` / `нет`).
- Progress files and the student folder are listed in `.gitignore` and are not committed. To start the course over, delete `data/progress.json`, `data/project_state.json` and `student_workflow/`.

## Status and roadmap

Works now:

- the full loop: lesson → code → pytest → review → feedback → next lesson
- re-explanations with growing simplicity, regression detection across project tests, milestone checks, saved progress, conversation summaries
- student code runs in an isolated Docker sandbox
- the model is switchable in config: DeepSeek, Gemini or a local model in LM Studio
- a small starter curriculum: 2 modules, 3 lessons, 5 tasks (pytest basics, fixtures, a first API status-code check)

Known limitations and next steps:

- no chat interface yet, only the console demo
- the course content is small, and the milestone checks are placeholders
- the "continue to the next lesson?" answer only understands exact `да` / `нет`; an LLM-based intent check is planned
- course completion is not handled yet
- the workflow state is kept in memory only (`MemorySaver`); the student's progress itself is stored in JSON files
- the project has no automated tests of its own yet