"""Тесты разбиения выражения на токены."""
import unittest

from structlab.calculator.errors import CalcError
from structlab.calculator.tokenizer import (
    END,
    FUNCTION,
    LEFT_PAREN,
    NUMBER,
    OPERATOR,
    RIGHT_PAREN,
    tokenize,
)


def texts(expression: str) -> list[str]:
    """Тексты токенов без завершающего END."""
    return [token.text for token in tokenize(expression)[:-1]]


class TokenizeTests(unittest.TestCase):
    def test_spaces_are_optional(self) -> None:
        for expression in ("2+3", "2 + 3", "  2 +3 ", "2\t+\t3"):
            with self.subTest(expression=expression):
                self.assertEqual(texts(expression), ["2", "+", "3"])

    def test_numbers(self) -> None:
        tokens = tokenize("12 3.5 .5 2.")
        values = [token.value for token in tokens[:-1]]
        self.assertEqual(values, [12, 3.5, 0.5, 2.0])
        self.assertIsInstance(tokens[0].value, int)
        self.assertIsInstance(tokens[3].value, float)
        self.assertTrue(all(token.kind == NUMBER for token in tokens[:-1]))

    def test_two_character_operators(self) -> None:
        self.assertEqual(texts("2**3//4"), ["2", "**", "3", "//", "4"])
        self.assertEqual(texts("2* *3"), ["2", "*", "*", "3"])

    def test_caret_means_power(self) -> None:
        token = tokenize("2^3")[1]
        self.assertEqual(token.kind, OPERATOR)
        self.assertEqual(token.text, "^")
        self.assertEqual(token.operator, "**")

    def test_parentheses_and_positions(self) -> None:
        tokens = tokenize("(1 - 2)")
        kinds = [token.kind for token in tokens]
        self.assertEqual(
            kinds, [LEFT_PAREN, NUMBER, OPERATOR, NUMBER, RIGHT_PAREN, END]
        )
        positions = [token.position for token in tokens]
        self.assertEqual(positions, [0, 1, 3, 5, 6, 7])

    def test_imaginary_numbers(self) -> None:
        tokens = tokenize("4i + 2.5j + i + J")
        values = [token.value for token in tokens if token.kind == NUMBER]
        self.assertEqual(values, [4j, 2.5j, 1j, 1j])
        self.assertEqual(texts("4i+i"), ["4i", "+", "i"])

    def test_sqrt_in_any_case(self) -> None:
        for expression in ("sqrt 16", "sqrt16", "SQRT(16)", "Sqrt 16"):
            with self.subTest(expression=expression):
                self.assertEqual(tokenize(expression)[0].kind, FUNCTION)

    def test_function_name_after_number_is_separate_token(self) -> None:
        self.assertEqual(texts("2sqrt 4"), ["2", "sqrt", "4"])

    def test_unknown_names(self) -> None:
        for expression, name, position in (
            ("2 + x", "x", 4),
            ("sin(1)", "sin", 0),
            ("2ii", "ii", 1),
        ):
            with self.subTest(expression=expression):
                with self.assertRaises(CalcError) as caught:
                    tokenize(expression)
                self.assertEqual(
                    caught.exception.message, f"Неизвестное имя «{name}»"
                )
                self.assertEqual(caught.exception.position, position)

    def test_empty_expression(self) -> None:
        tokens = tokenize("   ")
        self.assertEqual([token.kind for token in tokens], [END])

    def test_unknown_character(self) -> None:
        with self.assertRaises(CalcError) as caught:
            tokenize("2 & 3")
        self.assertEqual(caught.exception.message, "Неизвестный символ «&»")
        self.assertEqual(caught.exception.position, 2)


if __name__ == "__main__":
    unittest.main()
