"""Средн. 10: словарь квадратов чисел."""
from structlab.console import InputFunc, OutputFunc, read_int


def squares(n: int) -> dict[int, int]:
    """Построить словарь ``{1: 1, 2: 4, ..., n: n²}``.

    Ключи идут по возрастанию: словари Python сохраняют порядок вставки.
    Для ``n == 0`` получается пустой словарь.

    :raises ValueError: если ``n`` отрицательное.
    """
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    result = {}
    for number in range(1, n + 1):
        result[number] = number * number
    return result


def run(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    """Запросить n и вывести словарь квадратов чисел от 1 до n."""
    output_func("Словарь квадратов чисел от 1 до n («выход» — завершить).")
    n = read_int("n = ", input_func, output_func, minimum=0)
    if n is None:
        return
    output_func(str(squares(n)))


if __name__ == "__main__":
    run()
