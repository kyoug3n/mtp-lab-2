"""Меню заданий лабораторной работы."""
from collections.abc import Callable

from structlab.console import InputFunc, OutputFunc, read_line

TaskRunner = Callable[[InputFunc, OutputFunc], None]

TITLE = "Лабораторная работа №2 «Структурное программирование на Python»"

# Пункты меню: название задания и функция, запускающая его диалог.
MENU_ITEMS: tuple[tuple[str, TaskRunner], ...] = ()


def show_menu(output_func: OutputFunc = print) -> None:
    """Вывести список заданий."""
    output_func("")
    output_func("Выберите задание:")
    for number, (title, _) in enumerate(MENU_ITEMS, start=1):
        output_func(f"  {number}. {title}")
    output_func("  0. Выход")


def main(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    """Показывать меню и запускать выбранные задания до выхода."""
    output_func(TITLE)
    while True:
        show_menu(output_func)
        choice = read_line("Номер: ", input_func)
        if choice is None or choice == "0":
            output_func("До свидания!")
            break
        try:
            number = int(choice)
        except ValueError:
            number = -1
        if not 1 <= number <= len(MENU_ITEMS):
            output_func(f"Нет такого пункта: {choice!r}.")
            continue
        title, action = MENU_ITEMS[number - 1]
        output_func(f"--- {title} ---")
        action(input_func, output_func)
