"""Повыш. 5: игра «Угадай число».

Программа загадывает целое число от ``LOW`` до ``HIGH`` модулем ``random``,
пользователь называет варианты и получает подсказки «больше» или «меньше».
Некорректный ввод не считается попыткой.

Для демонстрации партию можно сделать воспроизводимой, задав зерно
генератора: ``python -m structlab.guess_game --seed 4``.
"""
import argparse
import math
import random

from structlab.console import InputFunc, OutputFunc, read_line

LOW = 1
HIGH = 100

GREATER = "Загаданное число больше."
LESS = "Загаданное число меньше."
CORRECT = "Угадали!"


def check_guess(secret: int, guess: int) -> str:
    """Сравнить вариант с загаданным числом и вернуть подсказку."""
    if guess < secret:
        return GREATER
    elif guess > secret:
        return LESS
    else:
        return CORRECT


def max_attempts_needed(low: int, high: int) -> int:
    """Число попыток, которого всегда хватает стратегии «делить пополам».

    Каждая попытка с серединой диапазона оставляет не больше половины
    чисел, поэтому для n чисел нужно ⌊log₂ n⌋ + 1 попыток: для 1..100 — 7.
    """
    return math.floor(math.log2(high - low + 1)) + 1


def attempts_word(count: int) -> str:
    """Слово для фразы «за N …»: попытку, попытки или попыток."""
    if count % 10 == 1 and count % 100 != 11:
        return "попытку"
    if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return "попытки"
    return "попыток"


def play(
    secret: int,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> int | None:
    """Провести партию с загаданным числом ``secret``.

    Возвращает число попыток или ``None``, если игрок сдался.
    """
    output_func(f"Я загадал целое число от {LOW} до {HIGH}. Угадайте его!")
    output_func("«выход» — сдаться.")
    attempts = 0
    while True:
        text = read_line("Ваш вариант: ", input_func)
        if text is None:
            output_func(f"Жаль! Было загадано число {secret}.")
            return None
        try:
            guess = int(text)
        except ValueError:
            output_func(f"Нужно целое число от {LOW} до {HIGH}.")
            continue
        if not LOW <= guess <= HIGH:
            output_func(f"Число должно быть от {LOW} до {HIGH}.")
            continue

        attempts += 1
        hint = check_guess(secret, guess)
        output_func(hint)
        if hint == CORRECT:
            output_func(
                f"Число {secret} угадано за {attempts} "
                f"{attempts_word(attempts)}."
            )
            best = max_attempts_needed(LOW, HIGH)
            output_func(
                "Если называть середину оставшегося диапазона, любое число "
                f"угадывается не больше чем за {best} {attempts_word(best)}."
            )
            return attempts


def run(
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
    rng: random.Random | None = None,
) -> None:
    """Загадать число генератором ``rng`` и провести партию."""
    generator = rng if rng is not None else random.Random()
    play(generator.randint(LOW, HIGH), input_func, output_func)


def main(
    argv: list[str] | None = None,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> None:
    """Запуск из командной строки с необязательным ключом ``--seed``."""
    parser = argparse.ArgumentParser(description="Игра «Угадай число».")
    parser.add_argument(
        "--seed",
        type=int,
        help="зерно генератора случайных чисел, чтобы повторить партию",
    )
    args = parser.parse_args(argv)
    rng = random.Random(args.seed) if args.seed is not None else None
    run(input_func, output_func, rng)


if __name__ == "__main__":
    main()
