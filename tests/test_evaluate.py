"""Тесты вычисления выражений калькулятором (Средн. 6)."""
import cmath
import math
import random
import time
import unittest

from structlab.calculator import CalcError, evaluate
from structlab.calculator.operations import (
    MAX_INT_DIGITS,
    TOO_BIG_FLOAT,
    TOO_BIG_INT,
    ZERO_POWER,
)


class PrecedenceTests(unittest.TestCase):
    def check(self, cases: list[tuple[str, object]]) -> None:
        for expression, expected in cases:
            with self.subTest(expression=expression):
                result = evaluate(expression)
                self.assertEqual(result, expected)
                self.assertIs(type(result), type(expected))

    def test_single_operations(self) -> None:
        self.check([
            ("2 + 3", 5),
            ("2 - 3", -1),
            ("2 * 3", 6),
            ("7 / 2", 3.5),
            ("6 / 2", 3.0),
            ("7 // 2", 3),
            ("7 % 3", 1),
            ("2 ** 10", 1024),
            ("2 ^ 10", 1024),
            ("2.5 * 2", 5.0),
            ("42", 42),
        ])

    def test_multiplication_before_addition(self) -> None:
        self.check([
            ("2 + 3 * 4", 14),
            ("(2 + 3) * 4", 20),
            ("10 - 6 / 2", 7.0),
            ("2 * 3 + 4 * 5", 26),
        ])

    def test_left_to_right(self) -> None:
        self.check([
            ("2 - 3 - 4", -5),
            ("2 - (3 - 4)", 3),
            ("100 / 10 / 5", 2.0),
            ("100 // 7 % 4", 2),
        ])

    def test_power_is_right_associative(self) -> None:
        self.check([
            ("2 ^ 3 ^ 2", 512),
            ("(2 ^ 3) ^ 2", 64),
            ("2 ** 3 ^ 2", 512),
        ])

    def test_unary_signs(self) -> None:
        self.check([
            ("-2 ^ 2", -4),
            ("(-2) ^ 2", 4),
            ("2 ^ -1", 0.5),
            ("2 * -3", -6),
            ("2 - -3", 5),
            ("--3", 3),
            ("+3", 3),
            ("-(2 + 3)", -5),
        ])

    def test_floor_division_and_remainder_follow_python(self) -> None:
        # Как в Python: // округляет вниз, остаток имеет знак делителя.
        self.check([
            ("-7 // 2", -4),
            ("-7 % 3", 2),
            ("7 % -3", -2),
            ("7.5 // 2", 3.0),
        ])

    def test_spaces_do_not_matter(self) -> None:
        for expression in ("2+3*4", " 2 + 3 * 4 ", "2 +3*  4"):
            with self.subTest(expression=expression):
                self.assertEqual(evaluate(expression), 14)

    def test_nested_parentheses(self) -> None:
        self.check([
            ("((((1))))", 1),
            ("((2 + 3) * (4 - 1)) ^ 2", 225),
            ("(" * 150 + "1" + ")" * 150, 1),
        ])


class SqrtAndComplexTests(unittest.TestCase):
    def check(self, cases: list[tuple[str, complex]]) -> None:
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertEqual(evaluate(expression), expected)

    def test_sqrt_forms(self) -> None:
        for expression in ("sqrt 16", "sqrt16", "sqrt(16)", "SQRT 16"):
            with self.subTest(expression=expression):
                self.assertEqual(evaluate(expression), 4.0)

    def test_sqrt_binds_like_a_function_call(self) -> None:
        self.check([
            ("sqrt 16 + 9", 13.0),
            ("sqrt(16 + 9)", 5.0),
            ("2 * sqrt 9", 6.0),
            ("-sqrt 4", -2.0),
            ("sqrt 16 ^ 2", 16.0),
            ("sqrt sqrt 16", 2.0),
            ("sqrt(-4) ^ 2", (2j) ** 2),
        ])

    def test_sqrt_of_negative_and_complex_numbers(self) -> None:
        self.check([
            ("sqrt(-4)", 2j),
            ("sqrt(-2)", cmath.sqrt(-2)),
            ("sqrt(3 + 4i)", 2 + 1j),
            ("sqrt(0)", 0.0),
        ])

    def test_imaginary_unit(self) -> None:
        self.check([
            ("i * i", -1 + 0j),
            ("i ^ 2", -1 + 0j),
            ("4i", 4j),
            ("3 + 4i", 3 + 4j),
            ("2.5j", 2.5j),
        ])

    def test_complex_arithmetic_matches_python(self) -> None:
        self.check([
            ("(1 + 2i) * (3 - i)", (1 + 2j) * (3 - 1j)),
            ("(1 + 2i) / (3 - 4i)", (1 + 2j) / (3 - 4j)),
            ("(1 + i) ^ 8", (1 + 1j) ** 8),
            ("2 ^ i", 2 ** 1j),
            ("-(3 - 4i)", -(3 - 4j)),
        ])

    def test_fractional_power_of_negative_number(self) -> None:
        # Главное значение корня, как в Python, а не -2.
        result = evaluate("(-8) ^ (1/3)")
        self.assertEqual(result, (-8) ** (1 / 3))
        self.assertTrue(cmath.isclose(result, 1 + math.sqrt(3) * 1j))
        self.assertEqual(evaluate("(-8) ^ 0.5"), (-8) ** 0.5)


class ErrorTests(unittest.TestCase):
    def check_error(
        self, expression: str, message: str, position: int | None
    ) -> None:
        with self.subTest(expression=expression):
            with self.assertRaises(CalcError) as caught:
                evaluate(expression)
            self.assertEqual(caught.exception.message, message)
            self.assertEqual(caught.exception.position, position)

    def test_syntax_errors(self) -> None:
        self.check_error("", "Пустое выражение", None)
        self.check_error(
            "2 +", "Ожидалось число или «(», а встретилось конец выражения", 3
        )
        self.check_error(
            "* 2", "Ожидалось число или «(», а встретилось «*»", 0
        )
        self.check_error("(2 + 3", "Скобка не закрыта", 0)
        self.check_error("2 + 3)", "Лишняя закрывающая скобка", 5)
        self.check_error("()", "Ожидалось число или «(», а встретилось «)»", 1)
        self.check_error("2 $ 3", "Неизвестный символ «$»", 2)

    def test_missing_operator(self) -> None:
        # Умножение не подразумевается: знак операции нужно указать явно.
        cases = [
            ("2 3", "«3»", 2),
            ("2sqrt 4", "«sqrt»", 1),
            ("2 sqrt 4", "«sqrt»", 2),
            ("2(3)", "«(»", 1),
            ("(1 + 2)(3)", "«(»", 7),
            ("(2 3)", "«3»", 3),
            ("4i i", "«i»", 3),
        ]
        for expression, token, position in cases:
            self.check_error(
                expression,
                f"Пропущен знак операции перед {token} (например, «*»)",
                position,
            )

    def test_division_by_zero(self) -> None:
        cases = [("1 / 0", 2), ("5 // 0", 2), ("5 % 0", 2), ("1.5 / 0.0", 4)]
        for expression, position in cases:
            self.check_error(expression, "Деление на ноль", position)

    def test_zero_to_negative_or_complex_power(self) -> None:
        self.check_error("0 ^ -1", ZERO_POWER, 2)
        self.check_error("0.0 ^ -2", ZERO_POWER, 4)
        self.check_error("0 ^ i", ZERO_POWER, 2)

    def test_integer_operations_with_complex_numbers(self) -> None:
        self.check_error(
            "(1 + i) // 2",
            "Операция «//» не определена для комплексных чисел", 8,
        )
        self.check_error(
            "5 % 2i", "Операция «%» не определена для комплексных чисел", 2
        )

    def test_sqrt_errors(self) -> None:
        self.check_error(
            "sqrt", "Ожидалось число или «(», а встретилось конец выражения", 4
        )
        self.check_error(
            "sqrt -4", "Ожидалось число или «(», а встретилось «-»", 5
        )
        self.check_error("sqrt(10 ^ 400)", TOO_BIG_FLOAT, 0)

    def test_huge_integer_powers_are_refused_quickly(self) -> None:
        started = time.perf_counter()
        self.check_error("9 ^ 9 ^ 9", TOO_BIG_INT, 2)
        self.check_error("2 ^ 1000000000000", TOO_BIG_INT, 2)
        self.assertLess(time.perf_counter() - started, 1.0)

    def test_integer_digit_limit(self) -> None:
        self.assertEqual(
            len(str(evaluate(f"10 ^ {MAX_INT_DIGITS - 1}"))), MAX_INT_DIGITS
        )
        self.check_error(f"10 ^ {MAX_INT_DIGITS}", TOO_BIG_INT, 3)
        self.check_error("10 ^ 3000 * 10 ^ 3000", TOO_BIG_INT, 10)

    def test_float_overflow(self) -> None:
        self.check_error("10.0 ^ 400", TOO_BIG_FLOAT, 5)
        self.check_error("10.0 ^ 300 * 10.0 ^ 300", TOO_BIG_FLOAT, 11)
        self.check_error("10 ^ 400 / 3", TOO_BIG_FLOAT, 9)
        self.check_error("(1 + i) ^ 100000", TOO_BIG_FLOAT, 8)

    def test_exponent_notation_is_not_supported(self) -> None:
        self.check_error("1e5", "Неизвестное имя «e»", 1)

    def test_too_deep_nesting(self) -> None:
        self.check_error("(" * 5000 + "1" + ")" * 5000,
                         "Слишком глубокая вложенность выражения", None)


def random_number(rng: random.Random) -> tuple[str, str]:
    """Случайное число: запись для калькулятора и для Python."""
    kind = rng.random()
    if kind < 0.6:
        text = str(rng.randint(0, 20))
        return text, text
    if kind < 0.85:
        text = f"{rng.randint(0, 20)}.{rng.randint(0, 9)}"
        return text, text
    if kind < 0.95:
        coefficient = str(rng.randint(1, 9))
        return coefficient + "i", coefficient + "j"
    return "i", "1j"


def random_expression(rng: random.Random, depth: int) -> tuple[str, str]:
    """Случайное выражение: запись для калькулятора и для Python.

    В выражении встречаются все операции, скобки, знаки, ``sqrt`` и мнимые
    числа. Показатели степени — небольшие целые или 0.5, чтобы числа не
    росли слишком сильно; пробелы между токенами ставятся случайно.
    """
    if depth == 0 or rng.random() < 0.2:
        return random_number(rng)
    space = rng.choice(["", " "])
    kind = rng.random()
    if kind < 0.55:
        operator = rng.choice(["+", "-", "*", "/", "//", "%", "^", "**"])
        left, python_left = random_expression(rng, depth - 1)
        if operator in ("^", "**"):
            right = python_right = rng.choice(["-3", "-1", "0", "1", "2",
                                               "3", "0.5"])
            python_operator = "**"
        else:
            right, python_right = random_expression(rng, depth - 1)
            python_operator = operator
        return (f"{left}{space}{operator}{space}{right}",
                f"{python_left} {python_operator} {python_right}")
    inner, python_inner = random_expression(rng, depth - 1)
    if kind < 0.75:
        return f"({space}{inner}{space})", f"({python_inner})"
    if kind < 0.85:
        return f"sqrt{space}({inner})", f"_sqrt({python_inner})"
    sign = rng.choice(["-", "+"])
    return f"{sign}{space}{inner}", f"{sign}{python_inner}"


def reference_sqrt(value: complex) -> complex:
    """Корень для проверочного выражения на Python (как в калькуляторе).

    Сам корень проверяется в :class:`SqrtAndComplexTests`; здесь важно, что
    ``sqrt`` в выражении применяется к нужному операнду.
    """
    if isinstance(value, complex) or value < 0:
        return cmath.sqrt(value)
    return math.sqrt(value)


def is_finite(value: complex) -> bool:
    """Конечно ли число (для любого из типов int, float, complex)."""
    return isinstance(value, int) or cmath.isfinite(value)


class MatchesPythonTests(unittest.TestCase):
    """Калькулятор должен считать так же, как сам Python.

    Грамматика калькулятора повторяет грамматику Python, а операции
    выполняются операторами Python, поэтому результаты должны совпадать
    точно, вплоть до типа. ``eval`` здесь применяется только к строкам,
    которые тест сгенерировал сам, — в калькуляторе его нет.
    """

    def test_random_expressions(self) -> None:
        rng = random.Random(4)
        checked = errors = 0
        for _ in range(3000):
            expression, python_expression = random_expression(rng, depth=4)
            try:
                expected = eval(python_expression, {"_sqrt": reference_sqrt})
            except (ZeroDivisionError, OverflowError, TypeError):
                expected = None  # Python не смог вычислить выражение
            if expected is None or not is_finite(expected):
                with self.assertRaises(CalcError, msg=expression):
                    evaluate(expression)
                errors += 1
                continue
            result = evaluate(expression)
            self.assertEqual(result, expected, msg=expression)
            self.assertIs(type(result), type(expected), msg=expression)
            checked += 1
        # Убедиться, что проверка не выродилась в одни ошибки.
        self.assertGreater(checked, 2000)
        self.assertGreater(errors, 0)


if __name__ == "__main__":
    unittest.main()
