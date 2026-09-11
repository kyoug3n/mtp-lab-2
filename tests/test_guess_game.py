"""Тесты игры «Угадай число» (Повыш. 5)."""
import random
import unittest

from structlab.console import ScriptedConsole
from structlab.guess_game import (
    CORRECT,
    GREATER,
    HIGH,
    LESS,
    LOW,
    attempts_word,
    check_guess,
    main,
    max_attempts_needed,
    play,
    run,
)


class BisectingPlayer:
    """Игрок, который всегда называет середину оставшегося диапазона.

    Подсказки игры он читает из вывода, поэтому его методы подставляются
    вместо ``input`` и ``print``.
    """

    def __init__(self) -> None:
        self.low, self.high = LOW, HIGH
        self.guess = 0
        self.transcript: list[str] = []

    def input(self, prompt: str) -> str:
        self.guess = (self.low + self.high) // 2
        self.transcript.append(prompt + str(self.guess))
        return str(self.guess)

    def print(self, text: str = "") -> None:
        self.transcript.append(text)
        if text == GREATER:
            self.low = self.guess + 1
        elif text == LESS:
            self.high = self.guess - 1


class CheckGuessTests(unittest.TestCase):
    def test_hints(self) -> None:
        self.assertEqual(check_guess(50, 30), GREATER)
        self.assertEqual(check_guess(50, 70), LESS)
        self.assertEqual(check_guess(50, 50), CORRECT)


class MaxAttemptsTests(unittest.TestCase):
    def test_values(self) -> None:
        cases = [(1, 1, 1), (1, 2, 2), (1, 3, 2), (1, 63, 6), (1, 64, 7),
                 (1, 100, 7), (1, 127, 7), (1, 128, 8)]
        for low, high, expected in cases:
            with self.subTest(high=high):
                self.assertEqual(max_attempts_needed(low, high), expected)

    def test_bisection_always_wins_in_time(self) -> None:
        worst = 0
        for secret in range(LOW, HIGH + 1):
            player = BisectingPlayer()
            attempts = play(secret, player.input, player.print)
            self.assertIsNotNone(attempts)
            worst = max(worst, attempts)
        self.assertEqual(worst, max_attempts_needed(LOW, HIGH))


class AttemptsWordTests(unittest.TestCase):
    def test_forms(self) -> None:
        cases = {1: "попытку", 2: "попытки", 4: "попытки", 5: "попыток",
                 7: "попыток", 11: "попыток", 12: "попыток", 14: "попыток",
                 21: "попытку", 22: "попытки", 25: "попыток", 101: "попытку",
                 111: "попыток", 112: "попыток"}
        for count, word in cases.items():
            with self.subTest(count=count):
                self.assertEqual(attempts_word(count), word)


class PlayTests(unittest.TestCase):
    def test_game_with_invalid_input(self) -> None:
        console = ScriptedConsole(["50", "abc", "0", "101", "25", "37"])
        attempts = play(37, console.input, console.print)
        self.assertEqual(attempts, 3)
        self.assertEqual(
            console.transcript[2:],
            [
                "Ваш вариант: 50",
                LESS,
                "Ваш вариант: abc",
                "Нужно целое число от 1 до 100.",
                "Ваш вариант: 0",
                "Число должно быть от 1 до 100.",
                "Ваш вариант: 101",
                "Число должно быть от 1 до 100.",
                "Ваш вариант: 25",
                GREATER,
                "Ваш вариант: 37",
                CORRECT,
                "Число 37 угадано за 3 попытки.",
                "Если называть середину оставшегося диапазона, любое число "
                "угадывается не больше чем за 7 попыток.",
            ],
        )

    def test_first_try(self) -> None:
        console = ScriptedConsole(["42"])
        self.assertEqual(play(42, console.input, console.print), 1)
        self.assertIn("Число 42 угадано за 1 попытку.", console.transcript)

    def test_giving_up(self) -> None:
        for lines in (["10", "выход"], ["10"]):
            with self.subTest(lines=lines):
                console = ScriptedConsole(lines)
                self.assertIsNone(play(64, console.input, console.print))
                self.assertEqual(console.transcript[-1],
                                 "Жаль! Было загадано число 64.")


class SeedTests(unittest.TestCase):
    def test_run_uses_given_generator(self) -> None:
        secret = random.Random(4).randint(LOW, HIGH)
        player = BisectingPlayer()
        run(player.input, player.print, random.Random(4))
        self.assertIn(f"Число {secret} угадано", player.transcript[-2])

    def test_seed_option_makes_game_repeatable(self) -> None:
        transcripts = []
        for _ in range(2):
            player = BisectingPlayer()
            main(["--seed", "4"], player.input, player.print)
            transcripts.append(player.transcript)
        self.assertEqual(transcripts[0], transcripts[1])
        secret = random.Random(4).randint(LOW, HIGH)
        self.assertIn(f"Число {secret} угадано", transcripts[0][-2])

    def test_secret_is_in_range(self) -> None:
        rng = random.Random(0)
        for _ in range(1000):
            console = ScriptedConsole([])
            run(console.input, console.print, rng)
            secret = int(console.transcript[-1].split()[-1].rstrip("."))
            self.assertTrue(LOW <= secret <= HIGH)


if __name__ == "__main__":
    unittest.main()
