"""Точка входа консольного сервиса учета результатов спринтов."""

from models import Project, Result, Sprint, Task
from operations import (
    add_project,
    add_sprint,
    add_task,
    create_sprint_result,
    find_projects,
    get_project_by_id,
    get_sprint_by_id,
    get_sprint_statistics,
    get_task_by_id,
    sort_projects,
)
from storage import load_data, save_data
from utils import input_date, input_int, input_text


def show_projects(projects: list[Project]) -> None:
    """Вывести проекты."""
    if not projects:
        print("Проектов пока нет.")
        return
    for project in projects:
        print(project)


def show_sprints(sprints: list[Sprint]) -> None:
    """Вывести спринты."""
    if not sprints:
        print("Спринтов пока нет.")
        return
    for sprint in sprints:
        print(sprint)


def show_tasks(tasks: list[Task]) -> None:
    """Вывести задачи."""
    if not tasks:
        print("Задач пока нет.")
        return
    for task in tasks:
        print(f"{task} (спринт: {task.sprint.name})")


def show_results(results: list[Result]) -> None:
    """Вывести сохраненные итоги спринтов."""
    if not results:
        print("Результатов пока нет.")
        return
    for result in results:
        print(result)


def _print_menu() -> None:
    print(
        "\n=== Учет результатов спринтов ===\n"
        "1. Показать проекты\n"
        "2. Создать проект\n"
        "3. Найти проект\n"
        "4. Создать спринт\n"
        "5. Добавить задачу\n"
        "6. Показать спринты и задачи\n"
        "7. Отметить задачу выполненной\n"
        "8. Показать статистику спринта\n"
        "9. Зафиксировать результат спринта\n"
        "10. Показать результаты\n"
        "0. Сохранить и выйти"
    )


def main() -> None:
    """Загрузить данные и запустить меню приложения."""
    projects, sprints, tasks, results = load_data()
    while True:
        _print_menu()
        choice = input_int("Выберите действие: ")
        try:
            if choice == 0:
                save_data(projects, sprints, tasks, results)
                print("Данные сохранены.")
                return
            if choice == 1:
                show_projects(sort_projects(projects))
            elif choice == 2:
                project = add_project(
                    projects,
                    input_text("Название проекта: "),
                    input("Описание проекта: ").strip(),
                )
                save_data(projects, sprints, tasks, results)
                print(f"Создан проект: {project}")
            elif choice == 3:
                query = input_text("Часть названия: ")
                matches = find_projects(projects, query)
                show_projects(matches)
            elif choice == 4:
                show_projects(projects)
                project_id = input_int("ID проекта: ")
                project = get_project_by_id(projects, project_id)
                sprint = add_sprint(
                    sprints,
                    project,
                    input_text("Название спринта: "),
                    input_date("Дата начала (ГГГГ-ММ-ДД): "),
                    input_date("Дата окончания (ГГГГ-ММ-ДД): "),
                )
                save_data(projects, sprints, tasks, results)
                print(f"Создан спринт: {sprint}")
            elif choice == 5:
                show_sprints(sprints)
                sprint = get_sprint_by_id(sprints, input_int("ID спринта: "))
                task = add_task(
                    tasks,
                    sprint,
                    input_text("Название задачи: "),
                    input("Описание задачи: ").strip(),
                )
                save_data(projects, sprints, tasks, results)
                print(f"Создана задача: {task}")
            elif choice == 6:
                show_sprints(sprints)
                show_tasks(tasks)
            elif choice == 7:
                show_tasks(tasks)
                task = get_task_by_id(tasks, input_int("ID задачи: "))
                task.complete()
                save_data(projects, sprints, tasks, results)
                print(f"Задача выполнена: {task}")
            elif choice == 8:
                show_sprints(sprints)
                sprint_id = input_int("ID спринта: ")
                sprint = get_sprint_by_id(sprints, sprint_id)
                statistics = get_sprint_statistics(sprint)
                print(
                    f"Всего: {statistics['total']}; "
                    f"выполнено: {statistics['completed']}; "
                    f"в работе: {statistics['in_progress']}; "
                    f"запланировано: {statistics['planned']}"
                )
            elif choice == 9:
                show_sprints(sprints)
                sprint = get_sprint_by_id(sprints, input_int("ID спринта: "))
                result = create_sprint_result(
                    results, sprint, input_text("Краткий итог спринта: ")
                )
                save_data(projects, sprints, tasks, results)
                print(result)
            elif choice == 10:
                show_results(results)
            else:
                print("Нет такого пункта меню.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
