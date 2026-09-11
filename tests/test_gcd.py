"""Тесты НОД (Средн. 4)."""
import math
import random
import unittest

from structlab.console import ScriptedConsole
from structlab.gcd import gcd, run


class GcdTests(unittest.TestCase):
    def test_known_values(self) -> None:
        cases = [
            (48, 18, 6),
            (270, 192, 6),
            (17, 5, 1),
            (12, 12, 12),
            (1_000_000, 1, 1),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_order_does_not_matter(self) -> None:
        self.assertEqual(gcd(18, 48), gcd(48, 18))

    def test_zero(self) -> None:
        self.assertEqual(gcd(0, 7), 7)
        self.assertEqual(gcd(7, 0), 7)
        self.assertEqual(gcd(0, 0), 0)

    def test_negative_numbers(self) -> None:
        self.assertEqual(gcd(-24, 36), 12)
        self.assertEqual(gcd(24, -36), 12)
        self.assertEqual(gcd(-24, -36), 12)

    def test_huge_numbers_are_fast(self) -> None:
        # Вычитанием здесь понадобилось бы 10**18 - 1 шагов.
        self.assertEqual(gcd(10**18, 1), 1)
        self.assertEqual(gcd(2**200 * 3, 2**150 * 9), 2**150 * 3)

    def test_matches_math_gcd_on_random_pairs(self) -> None:
        rng = random.Random(4)
        for _ in range(1000):
            a = rng.randint(-10**12, 10**12)
            b = rng.randint(-10**12, 10**12)
            self.assertEqual(gcd(a, b), math.gcd(a, b), msg=f"{a}, {b}")

    def test_rejects_non_integers(self) -> None:
        with self.assertRaises(TypeError):
            gcd(4.0, 6)  # type: ignore[arg-type]


class GcdDialogTests(unittest.TestCase):
    def test_dialog(self) -> None:
        console = ScriptedConsole(["48", "x", "18"])
        run(console.input, console.print)
        self.assertIn("Нужно целое число, например 42.", console.transcript)
        self.assertEqual(console.transcript[-1], "НОД(48, 18) = 6")

    def test_exit_before_second_number(self) -> None:
        console = ScriptedConsole(["48", "выход"])
        run(console.input, console.print)
        self.assertEqual(console.transcript[-1], "Второе число: выход")


if __name__ == "__main__":
    unittest.main()
