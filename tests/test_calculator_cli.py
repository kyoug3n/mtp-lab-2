"""Тесты интерактивного режима калькулятора."""
import unittest

from structlab.calculator.cli import HELP, run
from structlab.console import ScriptedConsole


def session(lines: list[str]) -> list[str]:
    """Протокол сессии без приветствия."""
    console = ScriptedConsole(lines)
    run(console.input, console.print)
    return console.transcript[len(HELP):]


class CalculatorDialogTests(unittest.TestCase):
    def test_results_are_formatted(self) -> None:
        self.assertEqual(
            session(["2 + 3 * 4", "7/2", "0.1 + 0.2", "sqrt(-4)", "выход"]),
            [
                "> 2 + 3 * 4",
                "= 14",
                "> 7/2",
                "= 3.5",
                "> 0.1 + 0.2",
                "= 0.3",
                "> sqrt(-4)",
                "= 2i",
                "> выход",
            ],
        )

    def test_error_pointer_under_the_input(self) -> None:
        self.assertEqual(
            session(["2 + * 3", "  1 / 0", "(2 + 3"]),
            [
                "> 2 + * 3",
                "      ^",
                "Ошибка: Ожидалось число или «(», а встретилось «*».",
                ">   1 / 0",
                "      ^",
                "Ошибка: Деление на ноль.",
                "> (2 + 3",
                "  ^",
                "Ошибка: Скобка не закрыта.",
                "> ",
            ],
        )

    def test_error_without_position(self) -> None:
        deep = "(" * 5000 + "1" + ")" * 5000
        transcript = session([deep])
        self.assertEqual(
            transcript[1], "Ошибка: Слишком глубокая вложенность выражения."
        )

    def test_empty_lines_are_skipped(self) -> None:
        self.assertEqual(session(["", "   ", "1+1"]),
                         ["> ", ">    ", "> 1+1", "= 2", "> "])


if __name__ == "__main__":
    unittest.main()
