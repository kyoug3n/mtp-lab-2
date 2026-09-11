"""Тесты вычисления выражений калькулятором (Средн. 6)."""
import random
import time
import unittest

from structlab.calculator import CalcError, evaluate
from structlab.calculator.operations import (
    MAX_INT_DIGITS,
    NOT_REAL,
    TOO_BIG_FLOAT,
    TOO_BIG_INT,
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
        ])


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
        self.check_error("2 3", "Ожидалась операция, а встретилось «3»", 2)
        self.check_error("(2 + 3", "Скобка не закрыта", 0)
        self.check_error("2 + 3)", "Лишняя закрывающая скобка", 5)
        self.check_error(
            "(2 3)", "Ожидалась операция или «)», а встретилось «3»", 3
        )
        self.check_error("()", "Ожидалось число или «(», а встретилось «)»", 1)
        self.check_error("2 $ 3", "Неизвестный символ «$»", 2)

    def test_division_by_zero(self) -> None:
        cases = [("1 / 0", 2), ("5 // 0", 2), ("5 % 0", 2), ("1.5 / 0.0", 4)]
        for expression, position in cases:
            self.check_error(expression, "Деление на ноль", position)

    def test_zero_to_negative_power(self) -> None:
        self.check_error(
            "0 ^ -1", "Ноль нельзя возвести в отрицательную степень", 2
        )

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

    def test_complex_results_are_refused(self) -> None:
        self.check_error("(-8) ^ 0.5", NOT_REAL, 5)

    def test_too_deep_nesting(self) -> None:
        self.check_error("(" * 5000 + "1" + ")" * 5000,
                         "Слишком глубокая вложенность выражения", None)


def random_number(rng: random.Random) -> str:
    """Случайное целое или дробное число в записи калькулятора."""
    if rng.random() < 0.7:
        return str(rng.randint(0, 20))
    return f"{rng.randint(0, 20)}.{rng.randint(0, 9)}"


def random_expression(rng: random.Random, depth: int) -> str:
    """Случайное выражение со всеми операциями, скобками и знаками.

    Показатели степени — небольшие целые, чтобы числа не росли слишком
    сильно; пробелы между токенами ставятся или не ставятся случайно.
    """
    if depth == 0 or rng.random() < 0.2:
        return random_number(rng)
    space = rng.choice(["", " "])
    kind = rng.random()
    if kind < 0.6:
        operator = rng.choice(["+", "-", "*", "/", "//", "%", "^", "**"])
        left = random_expression(rng, depth - 1)
        if operator in ("^", "**"):
            right = str(rng.randint(-3, 3))
        else:
            right = random_expression(rng, depth - 1)
        return f"{left}{space}{operator}{space}{right}"
    if kind < 0.85:
        return f"({space}{random_expression(rng, depth - 1)}{space})"
    sign = rng.choice(["-", "+"])
    return f"{sign}{space}{random_expression(rng, depth - 1)}"


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
            expression = random_expression(rng, depth=4)
            python_expression = expression.replace("^", "**")
            try:
                expected = eval(python_expression)
            except (ZeroDivisionError, OverflowError):
                with self.assertRaises(CalcError, msg=expression):
                    evaluate(expression)
                errors += 1
                continue
            if isinstance(expected, complex):
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
