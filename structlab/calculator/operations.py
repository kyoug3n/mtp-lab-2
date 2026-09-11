"""Арифметические операции калькулятора с проверкой результата.

Операции выполняются обычными операторами Python, поэтому результат
совпадает с тем, что дал бы сам Python. Дополнительно калькулятор:

* превращает ошибки Python (деление на ноль, переполнение) в понятные
  сообщения :class:`CalcError`;
* заранее отказывается возводить в степень, если результат получится
  длиннее ``MAX_INT_DIGITS`` цифр, — иначе ``9 ^ 9 ^ 9`` вычислялось бы
  очень долго, а напечатать такое число Python всё равно не позволит.
"""
import math

from structlab.calculator.errors import CalcError

Number = int | float | complex

# Python по умолчанию отказывается переводить в строку целые числа длиннее
# 4300 цифр (sys.get_int_max_str_digits()), поэтому калькулятор не допускает
# таких результатов.
MAX_INT_DIGITS = 4300
INT_LIMIT = 10 ** MAX_INT_DIGITS

TOO_BIG_INT = f"Результат слишком велик: больше {MAX_INT_DIGITS} цифр"
TOO_BIG_FLOAT = "Результат слишком велик для дробного числа (переполнение)"
NOT_REAL = "Результат не является действительным числом"


def apply_operator(
    operator: str, left: Number, right: Number, position: int | None = None
) -> Number:
    """Выполнить бинарную операцию ``left operator right``.

    ``operator`` — одна из операций Python: ``+ - * / // % **``.
    ``position`` указывает место операции во вводе для сообщения об ошибке.

    :raises CalcError: при делении на ноль или слишком большом результате.
    """
    try:
        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        elif operator == "/":
            result = left / right
        elif operator == "//":
            result = left // right
        elif operator == "%":
            result = left % right
        elif operator == "**":
            result = power(left, right, position)
        else:
            raise ValueError(f"Неизвестная операция {operator!r}")
    except ZeroDivisionError:
        raise CalcError("Деление на ноль", position) from None
    except OverflowError:
        raise CalcError(TOO_BIG_FLOAT, position) from None
    return check_result(result, position)


def power(
    base: Number, exponent: Number, position: int | None = None
) -> Number:
    """Возвести ``base`` в степень ``exponent``.

    Для целых чисел длина результата оценивается заранее: у числа
    ``base ** exponent`` около ``exponent * log10(|base|)`` цифр.
    """
    if base == 0 and exponent < 0:
        raise CalcError(
            "Ноль нельзя возвести в отрицательную степень", position
        )
    if (
        isinstance(base, int)
        and isinstance(exponent, int)
        and exponent > 0
        and abs(base) > 1
        and exponent * math.log10(abs(base)) >= MAX_INT_DIGITS
    ):
        raise CalcError(TOO_BIG_INT, position)
    return base ** exponent


def check_result(value: Number, position: int | None = None) -> Number:
    """Проверить, что результат можно показать пользователю.

    :raises CalcError: если целое число длиннее ``MAX_INT_DIGITS`` цифр,
        дробное переполнилось (стало бесконечностью) или результат
        оказался комплексным.
    """
    if isinstance(value, int):
        if abs(value) >= INT_LIMIT:
            raise CalcError(TOO_BIG_INT, position)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise CalcError(TOO_BIG_FLOAT, position)
    else:
        # Python даёт комплексный результат, например, для (-8) ** 0.5.
        raise CalcError(NOT_REAL, position)
    return value
