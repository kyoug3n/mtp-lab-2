"""Тесты демонстрационного протокола reports/demo.txt."""
import unittest
from pathlib import Path

from structlab.demo import SESSIONS, build_sessions

REPORT = Path(__file__).resolve().parent.parent / "reports" / "demo.txt"


class DemoTests(unittest.TestCase):
    def test_all_sessions_are_present(self) -> None:
        lines = build_sessions()
        for number, (title, _, _) in enumerate(SESSIONS, 1):
            self.assertIn(f"=== {number}. {title} ===", lines)

    def test_committed_report_is_up_to_date(self) -> None:
        """Протокол в репозитории совпадает со свежим прогоном сессий.

        Штамп в начале файла (команда, ревизия, версия Python) не
        сравнивается: он описывает, где и когда протокол был получен.
        Штамп отделён от сессий первой пустой строкой, поэтому для сверки
        не нужен ни git, ни повторное построение штампа.
        """
        committed = REPORT.read_text(encoding="utf-8").splitlines()
        sessions = committed[committed.index(""):]
        self.assertEqual(
            sessions,
            build_sessions(),
            "reports/demo.txt устарел — выполните "
            "python -m structlab.demo reports/demo.txt",
        )


if __name__ == "__main__":
    unittest.main()
