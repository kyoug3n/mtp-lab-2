"""Повыш. 9: рекурсивная сумма чисел списка — два способа рекурсии.

1. :func:`recursive_sum_linear` — классическая схема «первый элемент + сумма
   остальных». Каждый элемент добавляет один вложенный вызов, поэтому
   глубина рекурсии равна длине списка. Python ограничивает глубину
   (``sys.getrecursionlimit()``, по умолчанию 1000) и не оптимизирует
   хвостовую рекурсию, так что на списке из нескольких тысяч чисел функция
   падает с ``RecursionError``.
2. :func:`recursive_sum` — «разделяй и властвуй»: сумма левой половины плюс
   сумма правой. Отрезок каждый раз уменьшается вдвое, глубина рекурсии —
   около log₂ n (для миллиона чисел — 21 уровень), и ограничение не мешает.

Обе функции не копируют список (как сделали бы срезы ``numbers[1:]``),
а передают в рекурсивный вызов границы обрабатываемой части.
"""
import math
import sys
from collections.abc import Sequence

from structlab.console import InputFunc, OutputFunc, read_line
from structlab.formatting import format_number

Real = int | float


def recursive_sum_linear(numbers: Sequence[Real]) -> Real:
    """Сумма чисел рекурсией «первый элемент + сумма остальных».

    :raises RecursionError: если список длиннее допустимой глубины рекурсии.
    """
    return _sum_from(numbers, 0)


def _sum_from(numbers: Sequence[Real], start: int) -> Real:
    """Сумма элементов начиная с индекса ``start``."""
    if start == len(numbers):  # базовый случай: элементов не осталось
        return 0
    return numbers[start] + _sum_from(numbers, start + 1)


def recursive_sum(numbers: Sequence[Real]) -> Real:
    """Сумма чисел рекурсией с делением списка пополам."""
    return _sum_range(numbers, 0, len(numbers))


def _sum_range(numbers: Sequence[Real], start: int, stop: int) -> Real:
    """Сумма элементов с индексами от ``start`` до ``stop`` (не включая)."""
    if stop - start == 0:  # базовый случай: пустой отрезок
        return 0
    if stop - start == 1:  # базовый случай: один элемент
        return numbers[start]
    middle = (start + stop) // 2
    left = _sum_range(numbers, start, middle)
    right = _sum_range(numbers, middle, stop)
    return left + right


def parse_numbers(text: str) -> list[Real]:
    """Разобрать строку чисел, разделённых пробелами.

    Целые числа остаются ``int``, остальные становятся ``float``.

    :raises ValueError: если среди слов есть не число.
    """
    numbers: list[Real] = []
    for word in text.split():
        try:
            number: Real = int(word)
        except ValueError:
            try:
                number = float(word)
            except ValueError:
                raise ValueError(f"«{word}» — не число") from None
            if not math.isfinite(number):
                raise ValueError(f"«{word}» — не конечное число")
        numbers.append(number)
    return numbers


def run(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    """Запросить числа и вывести их сумму, найденную обоими способами."""
    output_func("Рекурсивная сумма чисел («выход» — завершить).")
    while True:
        text = read_line("Числа через пробел: ", input_func)
        if text is None:
            return
        try:
            numbers = parse_numbers(text)
        except ValueError as error:
            output_func(f"Ошибка: {error}.")
            continue
        break

    output_func(f"Количество чисел: {len(numbers)}")
    try:
        linear = format_number(recursive_sum_linear(numbers))
    except RecursionError:
        linear = (
            "не хватило глубины рекурсии "
            f"(предел — {sys.getrecursionlimit()} вызовов)"
        )
    output_func(f"Сумма (первый + остальные): {linear}")
    halves = format_number(recursive_sum(numbers))
    output_func(f"Сумма (деление пополам): {halves}")


if __name__ == "__main__":
    run()
