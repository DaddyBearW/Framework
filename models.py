"""Объектная модель учета проектов и спринтов."""


class Project:
    """Проект, в рамках которого выполняются спринты."""

    def __init__(self, project_id: int, name: str, description: str) -> None:
        self.id = project_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"{self.id}. {self.name} — {self.description}"


class Sprint:
    """Спринт, принадлежащий проекту."""

    def __init__(
        self,
        sprint_id: int,
        project: Project,
        name: str,
        start_date: str,
        end_date: str,
    ) -> None:
        self.id = sprint_id
        self.project = project
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks: list["Task"] = []
        self.results: list["Result"] = []

    def __str__(self) -> str:
        return (
            f"{self.id}. {self.name} ({self.start_date} — {self.end_date}), "
            f"проект: {self.project.name}"
        )


class Task:
    """Задача, включенная в спринт."""

    STATUSES = {"planned", "in_progress", "done"}

    def __init__(
        self,
        task_id: int,
        sprint: "Sprint",
        title: str,
        description: str,
        status: str = "planned",
    ) -> None:
        if status not in self.STATUSES:
            raise ValueError(f"Неизвестный статус задачи: {status}")
        self.id = task_id
        self.sprint = sprint
        self.title = title
        self.description = description
        self.status = status

    def complete(self) -> None:
        """Отметить задачу выполненной."""
        self.status = "done"

    def __str__(self) -> str:
        return f"{self.id}. [{self.status}] {self.title}"


class Result:
    """Итог спринта, рассчитанный по его задачам."""

    def __init__(
        self,
        result_id: int,
        sprint: "Sprint",
        summary: str,
        completed_tasks: int,
        unfinished_tasks: int,
        recorded_at: str,
    ) -> None:
        self.id = result_id
        self.sprint = sprint
        self.summary = summary
        self.completed_tasks = completed_tasks
        self.unfinished_tasks = unfinished_tasks
        self.recorded_at = recorded_at

    def __str__(self) -> str:
        return (
            f"Итог спринта «{self.sprint.name}» от {self.recorded_at}: "
            f"выполнено {self.completed_tasks}, осталось "
            f"{self.unfinished_tasks}. {self.summary}"
        )
