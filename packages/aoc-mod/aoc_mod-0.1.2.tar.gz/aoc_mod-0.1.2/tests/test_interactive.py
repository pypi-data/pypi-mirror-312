import pytest
import logging
import time
from aoc_mod.interactive import interactive, generate_parser
from aoc_mod.utilities import AOCMod


@pytest.fixture
def mock_aoc_mod(monkeypatch):
    class MockAOCMod:
        def __init__(self):
            self.current_time = time.struct_time((2023, 12, 1, 0, 0, 0, 0, 0, 0))
            self.session_id = ""
            self.user_agent = ""

        def set_auth_variables(self):
            self.session_id = "test_session_id"
            self.user_agent = "test_user_agent"

        def get_current_date(self):
            return self.current_time

        def verify_correct_date(self, year, month, day):
            return month == 12 and 1 <= day <= 25

        def submit_answer(self, year, day, level, answer):
            print(
                f"Submitted answer: {answer} for year: {year}, day: {day}, level: {level}"
            )

    monkeypatch.setattr("aoc_mod.interactive.AOCMod", MockAOCMod)


def test_interactive_submit_answer(monkeypatch, capsys, mock_aoc_mod):
    monkeypatch.setattr(
        "sys.argv",
        [
            "interactive.py",
            "submit",
            "--date",
            "2023:1",
            "--level",
            "1",
            "--answer",
            "test_answer",
        ],
    )
    interactive()
    captured = capsys.readouterr()
    assert (
        "Submitted answer: test_answer for year: 2023, day: 1, level: 1" in captured.out
    )


def test_interactive_invalid_date(monkeypatch, caplog, mock_aoc_mod):
    monkeypatch.setattr("sys.argv", ["interactive.py", "setup", "--date", "2023:26"])
    with caplog.at_level(logging.ERROR):
        interactive()
    assert "Invalid date entered." in caplog.text


def test_interactive_setup_py_template(monkeypatch, capsys, mock_aoc_mod):
    def mock_setup_py_template(year, day):
        print(f"Setup template for year: {year}, day: {day}")

    monkeypatch.setattr("aoc_mod.interactive.setup_py_template", mock_setup_py_template)
    monkeypatch.setattr("sys.argv", ["interactive.py", "setup", "--date", "2023:1"])
    interactive()
    captured = capsys.readouterr()
    assert "Setup template for year: 2023, day: 1" in captured.out


def test_interactive_default_date(monkeypatch, capsys, mock_aoc_mod):
    monkeypatch.setattr("sys.argv", ["interactive.py", "setup"])
    interactive()
    captured = capsys.readouterr()
    assert "Year: 2023, Day: 1" in captured.out
