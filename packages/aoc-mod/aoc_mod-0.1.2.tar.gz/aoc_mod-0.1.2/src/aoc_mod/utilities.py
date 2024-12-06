"""Main AOCMod class definition"""

import os
import logging
import time
import requests
import markdownify
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

URL_PUZZLE_MAIN = "https://adventofcode.com/{YEAR}/day/{DAY}"
URL_PUZZLE_INPUT = f"{URL_PUZZLE_MAIN}/input"
URL_PUZZLE_ANSWER = f"{URL_PUZZLE_MAIN}/answer"


class AOCMod:
    def __init__(self):
        """Initialize the AOCMod class and set up the current time and authentication variables."""
        self.current_time = self.get_current_date()
        self.session_id = ""
        self.user_agent = requests.utils.default_headers()["User-Agent"]

    def set_auth_variables(self):
        """Set the authentication variables from environment variables."""
        try:
            self.session_id = os.environ["SESSION_ID"]
        except KeyError as exc:
            LOGGER.warning(
                "missing environment variable for authentication (%s)", str(exc)
            )

    def get_current_date(self):
        """Get the current local time.

        Returns:
            time.struct_time: The current local time.
        """
        return time.localtime(time.time())

    def verify_correct_date(self, year: int, month: int, day: int):
        """Verify if the provided date is valid for Advent of Code.

        Args:
            year (int): The year to verify.
            month (int): The month to verify.
            day (int): The day to verify.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
        if month != 12:
            return False
        if day < 1 or day > 25:
            return False
        if year < 2015 or year > self.current_time.tm_year:
            return False
        return True

    def get_puzzle_instructions(self, year: int = None, day: int = None):
        """Get the puzzle instructions for the specified year and day.

        Args:
            year (int): The year of the puzzle. Defaults to the current year.
            day (int): The day of the puzzle. Defaults to the current day.

        Returns:
            str: The puzzle instructions in markdown format.
        """
        # this is an authenticated method
        self.set_auth_variables()

        # if this function wasn't provided with a date, get current year, day
        if year is None or day is None:
            year = self.current_time.tm_year
            month = self.current_time.tm_mon
            day = self.current_time.tm_mday
        else:
            month = 12
            year = int(year)
            day = int(day)

        # check current date (for better error reporting)
        if not self.verify_correct_date(year, month, day):
            if month == 12:
                LOGGER.error(
                    "unable to grab puzzle instructions due to invalid year and day input (year: %d, day: %d)",
                    year,
                    day,
                )
            else:
                LOGGER.error(
                    "it is not December yet, please try again in December or manually enter the desired year and day"
                )
            return None

        # request the puzzle input for the current year and day
        try:
            res = requests.get(
                URL_PUZZLE_MAIN.format(YEAR=year, DAY=day),
                cookies={"session": self.session_id, "User-Agent": self.user_agent},
                timeout=5,
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            LOGGER.error("HTTP Error (%s)", errh.args[0])
            return None

        # run the instruction output through BeautifulSoup for html parsing
        soup = BeautifulSoup(res.content, "html.parser")

        for entry in soup.main.contents:
            if len(str(entry).strip()) == 0:
                continue

            result_content = str(entry).strip()
            break

        # turn the instructions into markdown
        return markdownify.markdownify(result_content)

    def get_puzzle_input(self, year: int = None, day: int = None):
        """Get the puzzle input for the specified year and day.

        Args:
            year (int): The year of the puzzle. Defaults to the current year.
            day (int): The day of the puzzle. Defaults to the current day.

        Returns:
            str: The puzzle input.
        """
        # this is an authenticated method
        self.set_auth_variables()

        # if this function wasn't provided with a date, get current year, day
        if year is None or day is None:
            year = self.current_time.tm_year
            month = self.current_time.tm_mon
            day = self.current_time.tm_mday
        else:
            month = 12
            year = int(year)
            day = int(day)

        # check current date (for better error reporting)
        if not self.verify_correct_date(year, month, day):
            if month == 12:
                LOGGER.error(
                    "unable to grab puzzle input due to invalid year and day input (year: %d, day: %d)",
                    year,
                    day,
                )
            else:  # only enters this section if we are in the current year and not December
                LOGGER.error(
                    "it is not December yet, please try again in December or manually enter the desired year and day"
                )
            return None

        # request the puzzle input for the current year and day
        try:
            res = requests.get(
                URL_PUZZLE_INPUT.format(YEAR=year, DAY=day),
                cookies={"session": self.session_id, "User-Agent": self.user_agent},
                timeout=5,
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            LOGGER.error("HTTP Error (%s)", errh.args[0])
            return None
        except requests.exceptions.RequestException as err:
            LOGGER.error("Request Exception (%s)", err.args[0])
            return None

        return res.text.strip()

    def submit_answer(self, year: int, day: int, level: int, answer):
        """Submit the puzzle answer for the specified year, day, and level.

        Args:
            year (int): The year of the puzzle.
            day (int): The day of the puzzle.
            level (int): The level of the puzzle (1 or 2).
            answer (str): The answer to submit.

        Returns:
            str: The response from the server.
        """
        # this is an authenticated method
        self.set_auth_variables()

        # just in case the year and day are not integers
        year = int(year)
        day = int(day)

        # check current date (for better error reporting)
        if not self.verify_correct_date(year, 12, day):
            LOGGER.error(
                "unable to submit puzzle answer due to invalid year and day input (year: %d, day: %d)",
                year,
                day,
            )
            return None

        # submit the puzzle answer
        try:
            res = requests.post(
                URL_PUZZLE_ANSWER.format(YEAR=year, DAY=day),
                data={"level": level, "answer": answer},
                cookies={"session": self.session_id, "User-Agent": self.user_agent},
                timeout=5,
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            LOGGER.error("HTTP Error (%s)", errh.args[0])
            return None
        except requests.exceptions.RequestException as err:
            LOGGER.error("Request Exception (%s)", err.args[0])
            return None

        # run the response output through BeautifulSoup for html parsing
        soup = BeautifulSoup(res.content, "html.parser")

        for entry in soup.article.contents:
            if len(str(entry)) == 0:
                continue

            result_content = str(entry)
            break

        print(markdownify.markdownify(result_content))

        return res.text
