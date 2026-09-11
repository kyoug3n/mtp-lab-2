"""Интерактивный режим калькулятора."""
from structlab.calculator.errors import CalcError
from structlab.calculator.parser import evaluate
from structlab.console import InputFunc, OutputFunc, read_raw_line
from structlab.formatting import format_number

PROMPT = "> "
HELP = (
    "Калькулятор выражений: + - * / // % ^ (или **), скобки, sqrt,",
    "мнимая единица i. Пустая строка пропускается, «выход» — завершить.",
)


def run(
    input_func: InputFunc = input, output_func: OutputFunc = print
) -> None:
    """Вычислять введённые выражения, пока пользователь не завершит ввод.

    При ошибке под введённой строкой выводится указатель ``^`` на место
    ошибки, после чего калькулятор ждёт следующее выражение.
    """
    for line in HELP:
        output_func(line)
    while True:
        text = read_raw_line(PROMPT, input_func)
        if text is None:
            return
        if not text.strip():
            continue
        try:
            result = evaluate(text)
        except CalcError as error:
            if error.position is not None:
                output_func(" " * (len(PROMPT) + error.position) + "^")
            output_func(f"Ошибка: {error.message}.")
            continue
        output_func(f"= {format_number(result)}")
