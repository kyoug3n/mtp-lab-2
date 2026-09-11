"""Ввод и вывод для интерактивных заданий.

Интерактивные функции пакета получают функции ввода и вывода параметрами
(по умолчанию — встроенные ``input`` и ``print``). Поэтому их можно проверять
тестами и показывать в демонстрационных сессиях, подставляя заранее заданный
ввод через :class:`ScriptedConsole`.
"""
from collections import deque
from collections.abc import Callable, Iterable

InputFunc = Callable[[str], str]
OutputFunc = Callable[[str], None]

EXIT_WORD = "выход"


def read_line(prompt: str, input_func: InputFunc = input) -> str | None:
    """Прочитать строку и убрать пробелы по краям.

    Возвращает ``None``, если ввод закончился (Ctrl+Z или Ctrl+D, Ctrl+C)
    или введено слово «выход» в любом регистре.
    """
    try:
        text = input_func(prompt)
    except (EOFError, KeyboardInterrupt):
        return None
    text = text.strip()
    if text.lower() == EXIT_WORD:
        return None
    return text


def read_int(
    prompt: str,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
    minimum: int | None = None,
) -> int | None:
    """Запрашивать строку, пока не будет введено целое число.

    Если задан ``minimum``, числа меньше него отклоняются. Возвращает
    ``None``, если пользователь завершил ввод (см. :func:`read_line`).
    """
    while True:
        text = read_line(prompt, input_func)
        if text is None:
            return None
        try:
            number = int(text)
        except ValueError:
            output_func("Нужно целое число, например 42.")
            continue
        if minimum is not None and number < minimum:
            output_func(f"Число должно быть не меньше {minimum}.")
            continue
        return number


class ScriptedConsole:
    """Консоль с заранее заданным вводом — для тестов и демонстрации.

    В ``transcript`` записывается то, что увидел бы пользователь в терминале:
    приглашение вместе с «набранным» текстом и все выведенные строки.
    Когда заданный ввод заканчивается, ``input`` бросает ``EOFError``,
    как встроенная функция при конце ввода.
    """

    def __init__(self, lines: Iterable[str]) -> None:
        self._lines = deque(lines)
        self.transcript: list[str] = []

    def input(self, prompt: str) -> str:
        """Вернуть следующую заданную строку, записав её в протокол."""
        if not self._lines:
            self.transcript.append(prompt)
            raise EOFError
        line = self._lines.popleft()
        self.transcript.append(prompt + line)
        return line

    def print(self, text: str = "") -> None:
        """Записать выведенный текст в протокол."""
        self.transcript.append(text)

    @property
    def text(self) -> str:
        """Весь протокол одной строкой."""
        return "\n".join(self.transcript)
