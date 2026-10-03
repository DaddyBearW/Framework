"""Функции безопасного ввода для консольного интерфейса."""

from datetime import date


def input_int(prompt: str) -> int:
    """Запросить целое число, повторяя запрос при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_text(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не должно быть пустым.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt).strip()
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД.")
