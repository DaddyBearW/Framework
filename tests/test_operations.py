from models import Project
from operations import (
    add_project,
    add_sprint,
    add_task,
    create_sprint_result,
    find_projects,
    get_sprint_statistics,
    sort_projects,
)


def test_project_search_and_sort() -> None:
    projects = []
    add_project(projects, "Zebra", "Последний проект")
    add_project(projects, "Alpha", "Первый проект")

    found = find_projects(projects, "ALP")
    assert [item.name for item in found] == ["Alpha"]
    sorted_projects = sort_projects(projects)
    assert [item.name for item in sorted_projects] == ["Alpha", "Zebra"]


def test_sprint_statistics_update_when_task_is_completed() -> None:
    project = Project(1, "Sprint Ledger", "Описание")
    sprints = []
    sprint = add_sprint(
        sprints, project, "Sprint 1", "2026-09-01", "2026-09-14"
    )
    tasks = []
    completed = add_task(tasks, sprint, "Сделать модель", "Классы домена")
    add_task(tasks, sprint, "Добавить тесты", "Проверить операции")

    completed.complete()

    assert get_sprint_statistics(sprint) == {
        "total": 2,
        "completed": 1,
        "in_progress": 0,
        "planned": 1,
    }


def test_result_keeps_sprint_reference_and_statistics() -> None:
    project = Project(1, "Sprint Ledger", "Описание")
    sprint = add_sprint([], project, "Sprint 1", "2026-09-01", "2026-09-14")
    tasks = []
    add_task(tasks, sprint, "Готовая задача", "Описание")
    task = add_task(tasks, sprint, "Незавершенная задача", "Описание")
    task.complete()
    results = []

    result = create_sprint_result(
        results, sprint, "Первый релиз", "2026-09-14"
    )

    assert result.sprint is sprint
    assert result.completed_tasks == 1
    assert result.unfinished_tasks == 1
    assert sprint.results == [result]


def test_add_project_rejects_blank_name() -> None:
    try:
        add_project([], "  ", "Описание")
    except ValueError as error:
        assert "Название проекта" in str(error)
    else:
        raise AssertionError("Пустое название должно быть отклонено")


def test_add_sprint_rejects_reversed_dates() -> None:
    project = Project(1, "Sprint Ledger", "Описание")
    try:
        add_sprint(
            [], project, "Sprint 1", "2026-09-14", "2026-09-01"
        )
    except ValueError as error:
        assert "раньше даты начала" in str(error)
    else:
        raise AssertionError("Неверный интервал дат должен быть отклонен")
