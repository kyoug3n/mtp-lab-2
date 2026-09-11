"""Тесты словаря квадратов (Средн. 10)."""
import unittest

from structlab.console import ScriptedConsole
from structlab.squares import run, squares


class SquaresTests(unittest.TestCase):
    def test_first_five(self) -> None:
        self.assertEqual(squares(5), {1: 1, 2: 4, 3: 9, 4: 16, 5: 25})

    def test_small_n(self) -> None:
        self.assertEqual(squares(0), {})
        self.assertEqual(squares(1), {1: 1})

    def test_keys_in_order_and_values_are_squares(self) -> None:
        result = squares(500)
        self.assertEqual(list(result), list(range(1, 501)))
        for number, square in result.items():
            self.assertEqual(square, number ** 2)

    def test_negative_n_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            squares(-1)


class SquaresDialogTests(unittest.TestCase):
    def test_dialog(self) -> None:
        console = ScriptedConsole(["-3", "4"])
        run(console.input, console.print)
        self.assertIn("Число должно быть не меньше 0.", console.transcript)
        self.assertEqual(console.transcript[-1], "{1: 1, 2: 4, 3: 9, 4: 16}")


if __name__ == "__main__":
    unittest.main()
