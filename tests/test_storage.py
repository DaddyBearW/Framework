from models import Project
from operations import add_project, add_sprint, add_task, create_sprint_result
from storage import load_data, save_data


def test_json_round_trip_restores_object_relationships(tmp_path) -> None:
    projects = []
    project = add_project(projects, "Sprint Ledger", "Учет спринтов")
    sprints = []
    sprint = add_sprint(
        sprints, project, "Sprint 1", "2026-09-01", "2026-09-14"
    )
    tasks = []
    task = add_task(tasks, sprint, "Сделать модели", "Создать классы")
    task.complete()
    results = []
    create_sprint_result(results, sprint, "Модели готовы", "2026-09-14")

    save_data(projects, sprints, tasks, results, tmp_path)
    loaded_projects, loaded_sprints, loaded_tasks, loaded_results = load_data(
        tmp_path
    )

    assert loaded_sprints[0].project is loaded_projects[0]
    assert loaded_tasks[0].sprint is loaded_sprints[0]
    assert loaded_results[0].sprint is loaded_sprints[0]
    assert loaded_sprints[0].tasks == loaded_tasks
    assert loaded_sprints[0].results == loaded_results
    assert loaded_tasks[0].status == "done"


def test_missing_json_files_load_as_empty_collections(tmp_path) -> None:
    assert load_data(tmp_path) == ([], [], [], [])


def test_loaded_objects_are_domain_objects(tmp_path) -> None:
    project = Project(1, "Sprint Ledger", "Описание")
    save_data([project], [], [], [], tmp_path)

    projects, sprints, tasks, results = load_data(tmp_path)

    assert isinstance(projects[0], Project)
    assert (sprints, tasks, results) == ([], [], [])
