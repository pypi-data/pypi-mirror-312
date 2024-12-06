"""Script to initialize a new day for Advent of Code.
This script will basically grab the input and puzzle clue
from the Advent of Code website.

If user specifies a year and day, this script will create
the files pertaining to that day and year.

Author: David Eyrich
"""

import os
import logging
import argparse
import importlib.metadata
from aoc_mod.file_templates.py_templates import SINGLE_DAY_PYTHON_SCRIPT
from aoc_mod.utilities import AOCMod


def setup_py_template(year, day):

    # create proper files to be used
    day_path = f"challenges/{year}/day{day}"

    os.system(f"mkdir -p {day_path}")

    soln_path = f"{day_path}/day{day}.py"

    if not os.path.exists(soln_path):
        with open(soln_path, "w", encoding="utf-8") as f_soln:
            f_soln.write(
                SINGLE_DAY_PYTHON_SCRIPT.format(
                    YEAR=year,
                    DAY=day,
                )
            )
        logging.info("%s, Day %s solution file created: %s", year, day, soln_path)
    else:
        logging.warning("%s, Day %s solution file already exists.", year, day)


def generate_parser():
    """Simple argparser."""

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        "--debug", action="store_true", help="Enable debug print statements."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"aoc-mod version {importlib.metadata.version('aoc-mod')}",
    )

    subparsers = parser.add_subparsers(required=True)

    # define the setup subparser
    setup_parser = subparsers.add_parser(
        "setup", help="Initiate the setup of the files for AoC."
    )

    setup_parser.add_argument(
        "-d",
        "--date",
        metavar="YEAR:DAY",
        help="Enter the year and day of the Advent of Code challenge you would like.",
    )

    # define the submit subparser
    submit_parser = subparsers.add_parser(
        "submit", help="Initiate a submission of the answer for an AoC problem."
    )
    submit_parser.add_argument(
        "-a", "--answer", type=str, help="Answer to submit.", required=True
    )
    submit_parser.add_argument(
        "-l",
        "--level",
        choices=["1", "2"],
        help="Part A = 1; Part B = 2",
        required=True,
    )

    submit_parser.add_argument(
        "-d",
        "--date",
        metavar="YEAR:DAY",
        help="Enter the year and day of the Advent of Code challenge you would like.",
        required=True,
    )

    return parser


def interactive():
    parser = generate_parser()
    opts = parser.parse_args()

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)

    aoc_mod = AOCMod()
    if opts.date:
        year, day = opts.date.split(":", 1)
    else:
        current_time = aoc_mod.get_current_date()
        year, day = current_time.tm_year, current_time.tm_mday
    print(f"Year: {year}, Day: {day}")

    if "answer" in opts and "level" in opts:
        print(f"Answer: {opts.answer}, Level: {opts.level}")

        aoc_mod.submit_answer(int(year), int(day), int(opts.level), opts.answer)
    else:

        if aoc_mod.verify_correct_date(int(year), 12, int(day)):

            setup_py_template(int(year), int(day))

        else:
            logging.error("Invalid date entered.")


if __name__ == "__main__":
    interactive()
