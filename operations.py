"""Функции предметной области для проектов, спринтов и задач."""

from datetime import date

from models import Project, Result, Sprint, Task


def _next_id(items: list) -> int:
    largest_id = 0
    for item in items:
        if item.id > largest_id:
            largest_id = item.id
    return largest_id + 1


def add_project(
    projects: list[Project],
    name: str,
    description: str,
) -> Project:
    """Создать проект и добавить его в коллекцию."""
    if not name.strip():
        raise ValueError("Название проекта не должно быть пустым.")
    project = Project(_next_id(projects), name.strip(), description.strip())
    projects.append(project)
    return project


def find_projects(projects: list[Project], query: str) -> list[Project]:
    """Найти проекты по части названия без учета регистра."""
    found_projects = []
    query = query.lower().strip()
    for project in projects:
        if query in project.name.lower():
            found_projects.append(project)
    return found_projects


def sort_projects(projects: list[Project]) -> list[Project]:
    """Вернуть проекты, отсортированные по названию."""
    return sorted(projects, key=lambda project: project.name.lower())


def get_project_by_id(projects: list[Project], project_id: int) -> Project:
    """Найти проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project
    raise ValueError(f"Проект с ID {project_id} не найден.")


def add_sprint(
    sprints: list[Sprint],
    project: Project,
    name: str,
    start_date: str,
    end_date: str,
) -> Sprint:
    """Создать спринт проекта после проверки дат."""
    if not name.strip():
        raise ValueError("Название спринта не должно быть пустым.")
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError as error:
        message = "Даты должны быть в формате ГГГГ-ММ-ДД."
        raise ValueError(message) from error
    if end < start:
        message = "Дата окончания не может быть раньше даты начала."
        raise ValueError(message)

    sprint = Sprint(
        _next_id(sprints),
        project,
        name.strip(),
        start.isoformat(),
        end.isoformat(),
    )
    sprints.append(sprint)
    return sprint


def get_sprint_by_id(sprints: list[Sprint], sprint_id: int) -> Sprint:
    """Найти спринт по идентификатору."""
    for sprint in sprints:
        if sprint.id == sprint_id:
            return sprint
    raise ValueError(f"Спринт с ID {sprint_id} не найден.")


def add_task(
    tasks: list[Task],
    sprint: Sprint,
    title: str,
    description: str,
) -> Task:
    """Создать задачу и связать ее со спринтом."""
    if not title.strip():
        raise ValueError("Название задачи не должно быть пустым.")
    task = Task(_next_id(tasks), sprint, title.strip(), description.strip())
    tasks.append(task)
    sprint.tasks.append(task)
    return task


def get_task_by_id(tasks: list[Task], task_id: int) -> Task:
    """Найти задачу по идентификатору."""
    for task in tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"Задача с ID {task_id} не найдена.")


def get_sprint_statistics(sprint: Sprint) -> dict[str, int]:
    """Посчитать общее количество и статусы задач спринта."""
    completed = 0
    in_progress = 0
    planned = 0
    for task in sprint.tasks:
        if task.status == "done":
            completed += 1
        elif task.status == "in_progress":
            in_progress += 1
        elif task.status == "planned":
            planned += 1
    return {
        "total": len(sprint.tasks),
        "completed": completed,
        "in_progress": in_progress,
        "planned": planned,
    }


def create_sprint_result(
    results: list[Result],
    sprint: Sprint,
    summary: str,
    recorded_at: str | None = None,
) -> Result:
    """Сохранить итог спринта со статистикой его задач."""
    if not summary.strip():
        raise ValueError("Описание результата не должно быть пустым.")
    statistics = get_sprint_statistics(sprint)
    result = Result(
        result_id=_next_id(results),
        sprint=sprint,
        summary=summary.strip(),
        completed_tasks=statistics["completed"],
        unfinished_tasks=statistics["total"] - statistics["completed"],
        recorded_at=recorded_at or date.today().isoformat(),
    )
    results.append(result)
    sprint.results.append(result)
    return result
