"""Тесты меню заданий."""
import unittest

from structlab.console import ScriptedConsole
from structlab.main import MENU_ITEMS, TITLE, main


class MenuTests(unittest.TestCase):
    def run_menu(self, lines: list[str]) -> list[str]:
        console = ScriptedConsole(lines)
        main(console.input, console.print)
        return console.transcript

    def test_shows_all_items_and_exits_on_zero(self) -> None:
        transcript = self.run_menu(["0"])
        self.assertEqual(transcript[0], TITLE)
        for number, (title, _) in enumerate(MENU_ITEMS, start=1):
            self.assertIn(f"  {number}. {title}", transcript)
        self.assertIn("  0. Выход", transcript)
        self.assertEqual(transcript[-1], "До свидания!")

    def test_exits_on_exit_word_and_end_of_input(self) -> None:
        for lines in (["выход"], []):
            with self.subTest(lines=lines):
                self.assertEqual(self.run_menu(lines)[-1], "До свидания!")

    def test_rejects_unknown_items(self) -> None:
        transcript = self.run_menu(["abc", "99", "0"])
        self.assertIn("Нет такого пункта: 'abc'.", transcript)
        self.assertIn("Нет такого пункта: '99'.", transcript)
        self.assertEqual(transcript[-1], "До свидания!")


if __name__ == "__main__":
    unittest.main()
