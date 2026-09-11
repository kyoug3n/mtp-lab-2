"""Арифметические операции калькулятора с проверкой результата.

Операции выполняются обычными операторами Python, поэтому результат
совпадает с тем, что дал бы сам Python. Дополнительно калькулятор:

* превращает ошибки Python (деление на ноль, переполнение) в понятные
  сообщения :class:`CalcError`;
* заранее отказывается возводить в степень, если результат получится
  длиннее ``MAX_INT_DIGITS`` цифр, — иначе ``9 ^ 9 ^ 9`` вычислялось бы
  очень долго, а напечатать такое число Python всё равно не позволит.

Комплексные числа обрабатываются теми же операторами. Дробная степень
отрицательного числа, как и в Python, даёт главное значение корня:
``(-8) ^ (1/3)`` — это ``1+1.73205080757i``, а не ``-2``.
"""
import cmath
import math

from structlab.calculator.errors import CalcError

Number = int | float | complex

# Python по умолчанию отказывается переводить в строку целые числа длиннее
# 4300 цифр (sys.get_int_max_str_digits()), поэтому калькулятор не допускает
# таких результатов.
MAX_INT_DIGITS = 4300
INT_LIMIT = 10 ** MAX_INT_DIGITS

TOO_BIG_INT = f"Результат слишком велик: больше {MAX_INT_DIGITS} цифр"
TOO_BIG_FLOAT = "Слишком большое число для дробной арифметики (переполнение)"
ZERO_POWER = "Ноль нельзя возвести в отрицательную или комплексную степень"
INTEGER_ONLY = ("//", "%")


def apply_operator(
    operator: str, left: Number, right: Number, position: int | None = None
) -> Number:
    """Выполнить бинарную операцию ``left operator right``.

    ``operator`` — одна из операций Python: ``+ - * / // % **``.
    ``position`` указывает место операции во вводе для сообщения об ошибке.

    :raises CalcError: при делении на ноль, слишком большом результате
        или ``//`` и ``%`` с комплексным числом.
    """
    if operator in INTEGER_ONLY and (
        isinstance(left, complex) or isinstance(right, complex)
    ):
        raise CalcError(
            f"Операция «{operator}» не определена для комплексных чисел",
            position,
        )
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
    if (
        isinstance(base, int)
        and isinstance(exponent, int)
        and exponent > 0
        and abs(base) > 1
        and exponent * math.log10(abs(base)) >= MAX_INT_DIGITS
    ):
        raise CalcError(TOO_BIG_INT, position)
    try:
        return base ** exponent
    except ZeroDivisionError:
        raise CalcError(ZERO_POWER, position) from None


def square_root(value: Number, position: int | None = None) -> Number:
    """Квадратный корень: ``math.sqrt`` для неотрицательных действительных
    чисел, ``cmath.sqrt`` для отрицательных и комплексных (``sqrt(-4) = 2i``).
    """
    try:
        if isinstance(value, complex) or value < 0:
            result = cmath.sqrt(value)
        else:
            result = math.sqrt(value)
    except OverflowError:
        raise CalcError(TOO_BIG_FLOAT, position) from None
    return check_result(result, position)


def check_result(value: Number, position: int | None = None) -> Number:
    """Проверить, что результат можно показать пользователю.

    :raises CalcError: если целое число длиннее ``MAX_INT_DIGITS`` цифр
        или дробное (комплексное) переполнилось — стало бесконечностью.
    """
    if isinstance(value, int):
        if abs(value) >= INT_LIMIT:
            raise CalcError(TOO_BIG_INT, position)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise CalcError(TOO_BIG_FLOAT, position)
    elif not cmath.isfinite(value):
        raise CalcError(TOO_BIG_FLOAT, position)
    return value
