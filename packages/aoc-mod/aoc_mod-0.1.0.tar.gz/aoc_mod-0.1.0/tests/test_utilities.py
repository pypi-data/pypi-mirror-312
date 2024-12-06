import requests
import time
from aoc_mod.utilities import AOCMod


def test_set_auth_variables_session_id_set(monkeypatch):
    monkeypatch.setenv("SESSION_ID", "test_session_id")

    aoc_mod = AOCMod()
    aoc_mod.set_auth_variables()

    assert aoc_mod.session_id == "test_session_id"


def test_set_auth_variables_session_id_missing(monkeypatch, caplog):
    monkeypatch.delenv("SESSION_ID", raising=False)

    aoc_mod = AOCMod()
    aoc_mod.set_auth_variables()

    assert aoc_mod.session_id == ""
    assert (
        "missing environment variable for authentication ('SESSION_ID')" in caplog.text
    )


def test_get_current_date():
    aoc_mod = AOCMod()
    current_date = aoc_mod.get_current_date()
    assert isinstance(current_date, time.struct_time)


def test_verify_correct_date():
    aoc_mod = AOCMod()
    assert aoc_mod.verify_correct_date(2023, 12, 1) == True
    assert aoc_mod.verify_correct_date(2023, 11, 1) == False
    assert aoc_mod.verify_correct_date(2023, 12, 26) == False
    assert aoc_mod.verify_correct_date(2014, 12, 1) == False


def test_get_puzzle_instructions(monkeypatch):
    def mock_get(url, cookies, timeout):
        class MockResponse:
            def __init__(self):
                self.content = (
                    "<main><article>Test Puzzle Instructions</article></main>"
                )

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    aoc_mod = AOCMod()
    instructions = aoc_mod.get_puzzle_instructions(2023, 1)
    assert "Test Puzzle Instructions" in instructions


def test_get_puzzle_input(monkeypatch):
    def mock_get(url, cookies, timeout):
        class MockResponse:
            def __init__(self):
                self.text = "Test Puzzle Input"

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    aoc_mod = AOCMod()
    aoc_mod.session_id = "test_session_id"
    aoc_mod.user_agent = "test_user_agent"
    puzzle_input = aoc_mod.get_puzzle_input(2023, 1)
    assert puzzle_input == "Test Puzzle Input"


def test_submit_answer(monkeypatch):
    def mock_post(url, data, cookies, timeout):
        class MockResponse:
            def __init__(self):
                self.text = "Test Puzzle Answer Response"
                self.content = "<article><p>Test Puzzle Answer Response</p></article>"

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    aoc_mod = AOCMod()
    aoc_mod.session_id = "test_session_id"
    aoc_mod.user_agent = "test_user_agent"
    response = aoc_mod.submit_answer(2023, 1, 1, "test_answer")
    assert response == "Test Puzzle Answer Response"
