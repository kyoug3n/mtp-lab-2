"""Демонстрационные сессии всех заданий с заранее заданным вводом.

Запуск: ``python -m structlab.demo reports/demo.txt`` (без аргумента протокол
печатается на экран). Каждая сессия — это вызов той же функции, что
запускается из меню или командой из заголовка сессии; ввод подставляется
через :class:`structlab.console.ScriptedConsole` и виден после приглашений,
как в терминале.
"""
import platform
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from structlab import gcd, guess_game, main, recursive_sum, squares
from structlab.calculator import cli as calculator_cli
from structlab.console import InputFunc, OutputFunc, ScriptedConsole

Session = Callable[[InputFunc, OutputFunc], None]

SEED = 4

CALCULATOR_INPUT = [
    "2 + 3 * 4",
    "(2 + 3) * 4",
    "2 - 3 - 4",
    "2 ^ 3 ^ 2",
    "-2 ^ 2",
    "2 ^ -1",
    "7 / 2",
    "7 // 2",
    "-7 % 3",
    "0.1 + 0.2",
    "2+3*4",
    "2 ^ 100",
    "sqrt 16 + 9",
    "sqrt(16 + 9)",
    "sqrt(-4)",
    "(1 + 2i) * (3 - i)",
    "i ^ 2",
    "(-8) ^ (1/3)",
    "",
    "2 + * 3",
    "(2 + 3",
    "2 + 3)",
    "1 / 0",
    "0 ^ -1",
    "9 ^ 9 ^ 9",
    "10.0 ^ 400",
    "(1 + i) // 2",
    "2 & 3",
    "1e5",
    "выход",
]

# (заголовок, функция, ввод пользователя)
SESSIONS: list[tuple[str, Session, list[str]]] = [
    (
        "Меню заданий: python -m structlab",
        main.main,
        ["7", "1", "48", "18", "0"],
    ),
    (
        "НОД двух чисел (Средн. 4): python -m structlab.gcd",
        gcd.run,
        ["-24", "abc", "36"],
    ),
    (
        "НОД очень больших чисел: python -m structlab.gcd",
        gcd.run,
        ["1000000000000000000", "1"],
    ),
    (
        "Калькулятор (Средн. 6): python -m structlab.calculator",
        calculator_cli.run,
        CALCULATOR_INPUT,
    ),
    (
        "Словарь квадратов чисел (Средн. 10): python -m structlab.squares",
        squares.run,
        ["-1", "10"],
    ),
    (
        "Игра «Угадай число» (Повыш. 5): "
        f"python -m structlab.guess_game --seed {SEED}",
        lambda input_func, output_func: guess_game.main(
            ["--seed", str(SEED)], input_func, output_func
        ),
        ["abc", "150", "50", "25", "37", "31"],
    ),
    (
        "Рекурсивная сумма (Повыш. 9): python -m structlab.recursive_sum",
        recursive_sum.run,
        ["3 1 четыре", "3 1 4 1 5 9 2 6"],
    ),
    (
        "Рекурсивная сумма дробных: python -m structlab.recursive_sum",
        recursive_sum.run,
        ["0.1 0.2 0.3 -1.5"],
    ),
]


def git_revision() -> str:
    """Короткий хеш и дата текущего коммита (с пометкой о правках)."""
    try:
        revision = subprocess.run(
            ["git", "log", "-1", "--format=%h (%ci)"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "неизвестна (git недоступен)"
    if status:
        revision += " + незакоммиченные изменения"
    return revision


def build_sessions() -> list[str]:
    """Выполнить все сессии и вернуть их протокол построчно.

    Каждая сессия начинается с пустой строки — по первой пустой строке
    протокол делится на штамп и сессии.
    """
    lines: list[str] = []
    for number, (title, session, user_input) in enumerate(SESSIONS, 1):
        console = ScriptedConsole(user_input)
        session(console.input, console.print)
        lines += ["", f"=== {number}. {title} ===", *console.transcript]
    return lines


def build_header() -> list[str]:
    """Штамп протокола: команда, ревизия и версия Python (без пустых строк)."""
    return [
        "Демонстрационные сессии лабораторной работы №2 (вариант 4)",
        "Команда: python -m structlab.demo reports/demo.txt",
        f"Ревизия: {git_revision()}",
        f"Python: {platform.python_version()}",
        "Ввод пользователя задан заранее и показан после приглашений.",
    ]


def build_report() -> str:
    """Полный протокол: штамп и все сессии."""
    return "\n".join(build_header() + build_sessions()) + "\n"


def main_demo(argv: list[str]) -> None:
    """Записать протокол в файл из ``argv`` или вывести его на экран."""
    report = build_report()
    if argv:
        Path(argv[0]).write_text(report, encoding="utf-8", newline="\n")
        print(f"Протокол записан в {argv[0]}")
    else:
        print(report, end="")


if __name__ == "__main__":
    main_demo(sys.argv[1:])
