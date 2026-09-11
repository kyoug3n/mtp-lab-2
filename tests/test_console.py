"""Тесты функций ввода и подставной консоли."""
import unittest

from structlab.console import ScriptedConsole, read_int, read_line


class ReadLineTests(unittest.TestCase):
    def test_strips_spaces(self) -> None:
        console = ScriptedConsole(["  42  "])
        self.assertEqual(read_line("> ", console.input), "42")

    def test_exit_word_in_any_case(self) -> None:
        for word in ("выход", "ВЫХОД", "  Выход "):
            with self.subTest(word=word):
                console = ScriptedConsole([word])
                self.assertIsNone(read_line("> ", console.input))

    def test_end_of_input(self) -> None:
        console = ScriptedConsole([])
        self.assertIsNone(read_line("> ", console.input))

    def test_keyboard_interrupt(self) -> None:
        def interrupted(prompt: str) -> str:
            raise KeyboardInterrupt

        self.assertIsNone(read_line("> ", interrupted))


class ReadIntTests(unittest.TestCase):
    def test_repeats_until_integer(self) -> None:
        console = ScriptedConsole(["abc", "2.5", "-7"])
        number = read_int("> ", console.input, console.print)
        self.assertEqual(number, -7)
        self.assertEqual(
            console.transcript,
            [
                "> abc",
                "Нужно целое число, например 42.",
                "> 2.5",
                "Нужно целое число, например 42.",
                "> -7",
            ],
        )

    def test_minimum(self) -> None:
        console = ScriptedConsole(["-1", "0"])
        self.assertEqual(read_int("> ", console.input, console.print, 0), 0)
        self.assertIn("Число должно быть не меньше 0.", console.transcript)

    def test_exit(self) -> None:
        console = ScriptedConsole(["выход"])
        self.assertIsNone(read_int("> ", console.input, console.print))


class ScriptedConsoleTests(unittest.TestCase):
    def test_transcript_shows_prompt_with_typed_text(self) -> None:
        console = ScriptedConsole(["да"])
        console.print("Вопрос?")
        console.input("Ответ: ")
        self.assertEqual(console.text, "Вопрос?\nОтвет: да")

    def test_raises_eof_when_lines_run_out(self) -> None:
        console = ScriptedConsole([])
        with self.assertRaises(EOFError):
            console.input("> ")


if __name__ == "__main__":
    unittest.main()
