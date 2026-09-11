"""Разбиение строки выражения на токены.

Пробелы между токенами необязательны и могут быть в любом количестве:
``2+3``, ``2 + 3`` и ``  2 +3`` дают одни и те же токены.
"""
import re
from dataclasses import dataclass

from structlab.calculator.errors import CalcError

# Виды токенов.
NUMBER = "число"
OPERATOR = "операция"
LEFT_PAREN = "("
RIGHT_PAREN = ")"
END = "конец"

# Двухсимвольные операции проверяются раньше односимвольных,
# иначе «**» прочиталось бы как два умножения.
OPERATORS = ("**", "//", "+", "-", "*", "/", "%", "^")
# «^» — привычная запись степени; в самом Python «^» означает XOR.
OPERATOR_ALIASES = {"^": "**"}

NUMBER_PATTERN = re.compile(r"[0-9]+(?:\.[0-9]*)?|\.[0-9]+")

Number = int | float | complex


@dataclass(frozen=True)
class Token:
    """Токен выражения.

    ``text`` — токен так, как он записан во вводе (для сообщений об
    ошибках), ``position`` — индекс его первого символа. У чисел в ``value``
    хранится значение, у операций в ``operator`` — операция Python, которую
    нужно выполнить (для «^» это «**»).
    """

    kind: str
    text: str
    position: int
    value: Number | None = None
    operator: str = ""


def tokenize(text: str) -> list[Token]:
    """Разбить строку на токены; последним всегда идёт токен ``END``.

    :raises CalcError: при встрече символа, который не может входить
        в выражение.
    """
    tokens: list[Token] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char.isspace():
            index += 1
            continue

        number_match = NUMBER_PATTERN.match(text, index)
        if number_match:
            literal = number_match.group()
            value = float(literal) if "." in literal else int(literal)
            tokens.append(Token(NUMBER, literal, index, value))
            index = number_match.end()
            continue

        operator = _match_operator(text, index)
        if operator:
            python_operator = OPERATOR_ALIASES.get(operator, operator)
            tokens.append(
                Token(OPERATOR, operator, index, operator=python_operator)
            )
            index += len(operator)
            continue

        if char == "(":
            tokens.append(Token(LEFT_PAREN, char, index))
        elif char == ")":
            tokens.append(Token(RIGHT_PAREN, char, index))
        else:
            raise CalcError(f"Неизвестный символ «{char}»", index)
        index += 1

    tokens.append(Token(END, "", len(text)))
    return tokens


def _match_operator(text: str, index: int) -> str:
    """Вернуть операцию, начинающуюся с позиции ``index``, или ``""``."""
    for operator in OPERATORS:
        if text.startswith(operator, index):
            return operator
    return ""
