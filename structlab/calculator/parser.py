"""Разбор и вычисление выражения методом рекурсивного спуска.

Грамматика — от низшего приоритета к высшему, как в Python:

    выражение := слагаемое (("+" | "-") слагаемое)*
    слагаемое := унарное (("*" | "/" | "//" | "%") унарное)*
    унарное   := ("+" | "-") унарное | степень
    степень   := первичное (("**" | "^") унарное)?
    первичное := ЧИСЛО | "(" выражение ")"

Каждому правилу соответствует метод разборщика. Правила ссылаются друг на
друга, отсюда рекурсия: выражение в скобках разбирается тем же кодом, что
и всё выражение. Из грамматики следует:

* ``2 + 3 * 4 = 14`` — умножение выполняется раньше сложения;
* ``2 - 3 - 4 = -5`` — операции одного уровня выполняются слева направо;
* ``2 ^ 3 ^ 2 = 512`` — степень выполняется справа налево: 2 ^ (3 ^ 2);
* ``-2 ^ 2 = -4`` — степень выполняется раньше унарного минуса;
* ``2 ^ -1 = 0.5`` — показатель степени может иметь знак.

Значение вычисляется сразу во время разбора, без построения дерева.
"""
from structlab.calculator.errors import CalcError
from structlab.calculator.operations import Number, apply_operator
from structlab.calculator.tokenizer import (
    END,
    LEFT_PAREN,
    NUMBER,
    OPERATOR,
    RIGHT_PAREN,
    Token,
    tokenize,
)

ADDITIVE = ("+", "-")
MULTIPLICATIVE = ("*", "/", "//", "%")
SIGNS = ("+", "-")
POWER = ("**",)


def evaluate(text: str) -> Number:
    """Вычислить выражение, записанное в строке.

    :raises CalcError: если выражение записано с ошибкой или его нельзя
        вычислить (деление на ноль, слишком большой результат и т. п.).
    """
    tokens = tokenize(text)
    if tokens[0].kind == END:
        raise CalcError("Пустое выражение")
    try:
        return _Parser(tokens).parse()
    except RecursionError:
        # Каждая пара скобок добавляет несколько вложенных вызовов.
        raise CalcError("Слишком глубокая вложенность выражения") from None


class _Parser:
    """Разборщик одного выражения; методы соответствуют правилам грамматики."""

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._index = 0

    def parse(self) -> Number:
        """Разобрать всё выражение и убедиться, что лишних токенов нет."""
        value = self._expression()
        token = self._peek()
        if token.kind == RIGHT_PAREN:
            raise CalcError("Лишняя закрывающая скобка", token.position)
        if token.kind != END:
            raise CalcError(
                f"Ожидалась операция, а встретилось {_describe(token)}",
                token.position,
            )
        return value

    def _peek(self) -> Token:
        """Текущий токен (без перехода к следующему)."""
        return self._tokens[self._index]

    def _advance(self) -> Token:
        """Вернуть текущий токен и перейти к следующему."""
        token = self._tokens[self._index]
        if token.kind != END:
            self._index += 1
        return token

    def _next_is_operator(self, operators: tuple[str, ...]) -> bool:
        """Является ли текущий токен одной из операций ``operators``."""
        token = self._peek()
        return token.kind == OPERATOR and token.operator in operators

    def _expression(self) -> Number:
        """выражение := слагаемое (("+" | "-") слагаемое)*"""
        value = self._term()
        while self._next_is_operator(ADDITIVE):
            token = self._advance()
            right = self._term()
            value = apply_operator(token.operator, value, right,
                                   token.position)
        return value

    def _term(self) -> Number:
        """слагаемое := унарное (("*" | "/" | "//" | "%") унарное)*"""
        value = self._unary()
        while self._next_is_operator(MULTIPLICATIVE):
            token = self._advance()
            right = self._unary()
            value = apply_operator(token.operator, value, right,
                                   token.position)
        return value

    def _unary(self) -> Number:
        """унарное := ("+" | "-") унарное | степень"""
        if self._next_is_operator(SIGNS):
            token = self._advance()
            operand = self._unary()
            return -operand if token.operator == "-" else +operand
        return self._power()

    def _power(self) -> Number:
        """степень := первичное (("**" | "^") унарное)?"""
        base = self._primary()
        if self._next_is_operator(POWER):
            token = self._advance()
            # Показатель разбирается как «унарное», которое само может
            # содержать степень, — так получается порядок справа налево.
            exponent = self._unary()
            return apply_operator("**", base, exponent, token.position)
        return base

    def _primary(self) -> Number:
        """первичное := ЧИСЛО | "(" выражение ")"."""
        token = self._advance()
        if token.kind == NUMBER:
            return token.value
        if token.kind == LEFT_PAREN:
            value = self._expression()
            closing = self._peek()
            if closing.kind == RIGHT_PAREN:
                self._advance()
                return value
            if closing.kind == END:
                raise CalcError("Скобка не закрыта", token.position)
            raise CalcError(
                f"Ожидалась операция или «)», а встретилось "
                f"{_describe(closing)}",
                closing.position,
            )
        raise CalcError(
            f"Ожидалось число или «(», а встретилось {_describe(token)}",
            token.position,
        )


def _describe(token: Token) -> str:
    """Описание токена для сообщения об ошибке."""
    if token.kind == END:
        return "конец выражения"
    return f"«{token.text}»"
