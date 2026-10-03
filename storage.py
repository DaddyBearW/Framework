"""Загрузка и сохранение объектной модели в JSON-файлах."""

import json
from pathlib import Path

from models import Project, Result, Sprint, Task

DATA_DIR = Path(__file__).parent / "data"


def _read_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as data_file:
            data = json.load(data_file)
    except json.JSONDecodeError as error:
        message = f"Файл {path.name} содержит некорректный JSON."
        raise ValueError(message) from error
    if not isinstance(data, list):
        raise ValueError(f"Файл {path.name} должен содержать список.")
    return data


def _write_json(path: Path, data: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as data_file:
        json.dump(data, data_file, ensure_ascii=False, indent=2)


def load_data(
    data_dir: Path = DATA_DIR,
) -> tuple[list[Project], list[Sprint], list[Task], list[Result]]:
    """Загрузить JSON и восстановить связи между объектами."""
    project_data = _read_json(data_dir / "projects.json")
    sprint_data = _read_json(data_dir / "sprints.json")
    task_data = _read_json(data_dir / "tasks.json")
    result_data = _read_json(data_dir / "results.json")

    projects = []
    for item in project_data:
        project = Project(item["id"], item["name"], item["description"])
        projects.append(project)

    sprints = []
    for item in sprint_data:
        project = None
        for saved_project in projects:
            if saved_project.id == item["project_id"]:
                project = saved_project
        if project is None:
            raise ValueError("Для спринта не найден проект.")
        sprint = Sprint(
            item["id"],
            project,
            item["name"],
            item["start_date"],
            item["end_date"],
        )
        sprints.append(sprint)

    tasks = []
    for item in task_data:
        sprint = None
        for saved_sprint in sprints:
            if saved_sprint.id == item["sprint_id"]:
                sprint = saved_sprint
        if sprint is None:
            raise ValueError("Для задачи не найден спринт.")
        task = Task(
            item["id"],
            sprint,
            item["title"],
            item["description"],
            item["status"],
        )
        tasks.append(task)

    results = []
    for item in result_data:
        sprint = None
        for saved_sprint in sprints:
            if saved_sprint.id == item["sprint_id"]:
                sprint = saved_sprint
        if sprint is None:
            raise ValueError("Для результата не найден спринт.")
        result = Result(
            item["id"],
            sprint,
            item["summary"],
            item["completed_tasks"],
            item["unfinished_tasks"],
            item["recorded_at"],
        )
        results.append(result)

    for task in tasks:
        task.sprint.tasks.append(task)
    for result in results:
        result.sprint.results.append(result)
    return projects, sprints, tasks, results


def save_data(
    projects: list[Project],
    sprints: list[Sprint],
    tasks: list[Task],
    results: list[Result],
    data_dir: Path = DATA_DIR,
) -> None:
    """Сохранить объекты в отдельные JSON-файлы по сущностям."""
    data_dir.mkdir(parents=True, exist_ok=True)
    project_data = []
    for project in projects:
        project_data.append(
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            }
        )
    _write_json(data_dir / "projects.json", project_data)

    sprint_data = []
    for sprint in sprints:
        sprint_data.append(
            {
                "id": sprint.id,
                "project_id": sprint.project.id,
                "name": sprint.name,
                "start_date": sprint.start_date,
                "end_date": sprint.end_date,
            }
        )
    _write_json(data_dir / "sprints.json", sprint_data)

    task_data = []
    for task in tasks:
        task_data.append(
            {
                "id": task.id,
                "sprint_id": task.sprint.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
        )
    _write_json(data_dir / "tasks.json", task_data)

    result_data = []
    for result in results:
        result_data.append(
            {
                "id": result.id,
                "sprint_id": result.sprint.id,
                "summary": result.summary,
                "completed_tasks": result.completed_tasks,
                "unfinished_tasks": result.unfinished_tasks,
                "recorded_at": result.recorded_at,
            }
        )
    _write_json(data_dir / "results.json", result_data)
