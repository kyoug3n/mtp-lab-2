"""Разбиение строки выражения на токены.

Пробелы между токенами необязательны и могут быть в любом количестве:
``2+3``, ``2 + 3`` и ``  2 +3`` дают одни и те же токены.

Мнимая единица записывается как ``i`` (или ``j``, как в Python); число
с ней вплотную — мнимое число: ``4i``, ``2.5i``. Имена не зависят
от регистра: ``SQRT`` и ``I`` тоже подходят.
"""
import re
from dataclasses import dataclass

from structlab.calculator.errors import CalcError
from structlab.formatting import Number

# Виды токенов.
NUMBER = "число"
OPERATOR = "операция"
FUNCTION = "функция"
LEFT_PAREN = "("
RIGHT_PAREN = ")"
END = "конец"

# Двухсимвольные операции проверяются раньше односимвольных,
# иначе «**» прочиталось бы как два умножения.
OPERATORS = ("**", "//", "+", "-", "*", "/", "%", "^")
# «^» — привычная запись степени; в самом Python «^» означает XOR.
OPERATOR_ALIASES = {"^": "**"}

FUNCTIONS = ("sqrt",)
IMAGINARY_UNITS = ("i", "j")

NUMBER_PATTERN = re.compile(r"[0-9]+(?:\.[0-9]*)?|\.[0-9]+")
NAME_PATTERN = re.compile(r"[A-Za-z]+")


@dataclass(frozen=True)
class Token:
    """Токен выражения.

    ``text`` — токен так, как он записан во вводе (для сообщений об
    ошибках), ``position`` — индекс его первого символа. У чисел в ``value``
    хранится значение (у мнимых — ``complex``), у операций в ``operator`` —
    операция Python, которую нужно выполнить (для «^» это «**»).
    """

    kind: str
    text: str
    position: int
    value: Number | None = None
    operator: str = ""


def tokenize(text: str) -> list[Token]:
    """Разбить строку на токены; последним всегда идёт токен ``END``.

    :raises CalcError: при встрече символа или имени, которые не могут
        входить в выражение.
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
            value: Number = float(literal) if "." in literal else int(literal)
            end = number_match.end()
            suffix = NAME_PATTERN.match(text, end)
            if suffix and suffix.group().lower() in IMAGINARY_UNITS:
                value = complex(0, value)  # 4i — как 4j в Python
                end = suffix.end()
            tokens.append(Token(NUMBER, text[index:end], index, value))
            index = end
            continue

        name_match = NAME_PATTERN.match(text, index)
        if name_match:
            name = name_match.group()
            if name.lower() in IMAGINARY_UNITS:
                tokens.append(Token(NUMBER, name, index, 1j))
            elif name.lower() in FUNCTIONS:
                tokens.append(Token(FUNCTION, name, index))
            else:
                raise CalcError(f"Неизвестное имя «{name}»", index)
            index = name_match.end()
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
