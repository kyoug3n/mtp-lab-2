"""Тесты вывода чисел."""
import unittest

from structlab.formatting import format_number


class FormatNumberTests(unittest.TestCase):
    def check(self, cases: list[tuple[complex, str]]) -> None:
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(format_number(value), expected)

    def test_integers(self) -> None:
        self.check([
            (5, "5"),
            (-12, "-12"),
            (0, "0"),
            (2**100, "1267650600228229401496703205376"),
        ])

    def test_floats(self) -> None:
        self.check([
            (3.5, "3.5"),
            (6 / 2, "3"),
            (-0.25, "-0.25"),
            (0.1 + 0.2, "0.3"),
            (-0.0, "0"),
            (1 / 3, "0.333333333333"),
            (1e20, "1e+20"),
            (2.5e-7, "2.5e-07"),
        ])

    def test_complex(self) -> None:
        self.check([
            (1 + 2j, "1+2i"),
            (1 - 2j, "1-2i"),
            (1.5 - 0.5j, "1.5-0.5i"),
            (2j, "2i"),
            (1j, "i"),
            (-1j, "-i"),
            (3 + 1j, "3+i"),
            (3 - 1j, "3-i"),
            (complex(-1, 0), "-1"),
            (complex(0, 0), "0"),
        ])

    def test_complex_rounding_noise_is_dropped(self) -> None:
        # (-8) ** 0.5 в Python даёт 1.7319121124709868e-16+2.8284271247461903j
        self.assertEqual(format_number((-8) ** 0.5), "2.82842712475i")
        self.assertEqual(format_number(complex(1, 1e-17)), "1")
        self.assertEqual(format_number(3 + 1.0000000000001j), "3+i")

    def test_rejects_non_numbers(self) -> None:
        with self.assertRaises(TypeError):
            format_number("5")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
