"""Вывод чисел в привычном для человека виде.

* целые числа печатаются как есть: ``5``, ``2**100`` полностью;
* дробные — с точностью до 12 значащих цифр, поэтому ошибка округления
  двоичной арифметики не видна (``0.1 + 0.2`` → ``0.3``), а целый результат
  печатается без ``.0`` (``6 / 2`` → ``3``);
* комплексные — в математической записи с мнимой единицей ``i``
  (``1+2i``, ``-i``); часть, которая меньше другой в 10**12 раз и больше,
  считается шумом округления и отбрасывается.
"""
Number = int | float | complex

SIGNIFICANT_DIGITS = 12
NOISE_RATIO = 1e-12


def format_number(value: Number) -> str:
    """Представить число строкой (см. описание модуля)."""
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _format_real(value)
    if isinstance(value, complex):
        return _format_complex(value)
    raise TypeError(f"Не число: {value!r}")


def _format_real(value: float) -> str:
    """Дробное число с ``SIGNIFICANT_DIGITS`` значащими цифрами."""
    if value == 0:
        return "0"  # без знака у -0.0
    return f"{value:.{SIGNIFICANT_DIGITS}g}"


def _format_complex(value: complex) -> str:
    """Комплексное число в виде ``a+bi``."""
    real, imag = value.real, value.imag
    scale = max(abs(real), abs(imag))
    if abs(real) <= scale * NOISE_RATIO:
        real = 0.0
    if abs(imag) <= scale * NOISE_RATIO:
        imag = 0.0
    if imag == 0:
        return _format_real(real)

    coefficient = _format_real(abs(imag))
    if coefficient == "1":
        imag_text = "i"  # 1i записывается просто как i
    else:
        imag_text = coefficient + "i"
    if real == 0:
        return imag_text if imag > 0 else "-" + imag_text
    sign = "+" if imag > 0 else "-"
    return _format_real(real) + sign + imag_text
