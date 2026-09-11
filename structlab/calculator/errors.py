"""Ошибка вычисления выражения."""


class CalcError(ValueError):
    """Ошибка в выражении, понятная пользователю.

    ``position`` — индекс символа в исходной строке (с нуля), к которому
    относится ошибка, или ``None``, если место указать нельзя.
    """

    def __init__(self, message: str, position: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.position = position
