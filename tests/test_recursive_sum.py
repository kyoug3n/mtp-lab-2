"""Тесты рекурсивной суммы (Повыш. 9)."""
import math
import random
import sys
import unittest

from structlab.console import ScriptedConsole
from structlab.recursive_sum import (
    parse_numbers,
    recursive_sum,
    recursive_sum_linear,
    run,
)

BOTH = (recursive_sum_linear, recursive_sum)


class BothSumsTests(unittest.TestCase):
    def test_small_lists(self) -> None:
        cases = [
            ([], 0),
            ([7], 7),
            ([3, 1, 4], 8),
            ([-5, 5], 0),
            ([1.5, 2.5, -1], 3.0),
        ]
        for function in BOTH:
            for numbers, expected in cases:
                with self.subTest(function=function.__name__, numbers=numbers):
                    self.assertEqual(function(numbers), expected)

    def test_works_with_tuples(self) -> None:
        for function in BOTH:
            self.assertEqual(function((1, 2, 3)), 6)

    def test_does_not_change_the_list(self) -> None:
        numbers = [5, 3, 8]
        for function in BOTH:
            function(numbers)
        self.assertEqual(numbers, [5, 3, 8])

    def test_match_builtin_sum_on_random_lists(self) -> None:
        rng = random.Random(4)
        for _ in range(200):
            numbers = [rng.randint(-1000, 1000)
                       for _ in range(rng.randint(0, 300))]
            for function in BOTH:
                self.assertEqual(function(numbers), sum(numbers))

    def test_floats_match_builtin_sum(self) -> None:
        rng = random.Random(9)
        numbers = [rng.uniform(-100, 100) for _ in range(300)]
        for function in BOTH:
            self.assertTrue(math.isclose(function(numbers), sum(numbers),
                                         rel_tol=1e-9, abs_tol=1e-9))


class RecursionDepthTests(unittest.TestCase):
    def test_linear_recursion_hits_the_depth_limit(self) -> None:
        numbers = [1] * (sys.getrecursionlimit() * 5)
        with self.assertRaises(RecursionError):
            recursive_sum_linear(numbers)

    def test_halving_handles_long_lists(self) -> None:
        numbers = list(range(100_000))
        self.assertEqual(recursive_sum(numbers), sum(numbers))


class ParseNumbersTests(unittest.TestCase):
    def test_integers_and_floats(self) -> None:
        self.assertEqual(parse_numbers(" 3  -1 2.5 "), [3, -1, 2.5])
        self.assertIsInstance(parse_numbers("3")[0], int)
        self.assertEqual(parse_numbers(""), [])

    def test_rejects_words_and_infinity(self) -> None:
        for text in ("1 два 3", "1,5", "inf", "nan"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_numbers(text)


class RecursiveSumDialogTests(unittest.TestCase):
    def test_dialog(self) -> None:
        console = ScriptedConsole(["1 два", "3 1 4 1 5"])
        run(console.input, console.print)
        self.assertIn("Ошибка: «два» — не число.", console.transcript)
        self.assertEqual(
            console.transcript[-3:],
            [
                "Количество чисел: 5",
                "Сумма (первый + остальные): 14",
                "Сумма (деление пополам): 14",
            ],
        )

    def test_dialog_reports_recursion_limit(self) -> None:
        console = ScriptedConsole(["1 " * (sys.getrecursionlimit() * 5)])
        run(console.input, console.print)
        self.assertIn("не хватило глубины рекурсии", console.transcript[-2])
        self.assertEqual(
            console.transcript[-1],
            f"Сумма (деление пополам): {sys.getrecursionlimit() * 5}",
        )


if __name__ == "__main__":
    unittest.main()
