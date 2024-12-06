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


def setup_py_template(year, day, options):

    # set up output options
    input_o = False
    instructions = False

    if options == "both":
        input_o = True
        instructions = True
    elif options == "input":
        input_o = True
    elif options == "instructions":
        instructions = True

    # create proper files to be used
    day_path = f"challenges/{year}/day{day}"

    os.system(f"mkdir -p {day_path}")

    solution_path = f"{day_path}/day{day}.py"
    input_path = f"{day_path}/input_{day}.txt"
    instructions_path = f"{day_path}/instructions_{year}_{day}.md"

    if not os.path.exists(solution_path):
        with open(solution_path, "w", encoding="utf-8") as f_soln:
            f_soln.write(
                SINGLE_DAY_PYTHON_SCRIPT.format(
                    YEAR=year,
                    DAY=day,
                )
            )
        print(f"{year}, Day {day} solution file created: {solution_path}")
    else:
        logging.warning("%s, Day %s solution file already exists.", year, day)

    aoc_mod = AOCMod()

    if input_o:
        input_data = aoc_mod.get_puzzle_input(year, day)
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(input_data)
        print(f"{year}, Day {day} input file created: {input_path}")

    if instructions:
        instructions = aoc_mod.get_puzzle_instructions(year, day)
        with open(instructions_path, "w", encoding="utf-8") as f:
            f.write(instructions)
        print(f"{year}, Day {day} instructions file created: {instructions_path}")


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

    setup_parser.add_argument(
        "-o",
        "--options",
        choices=["input", "instructions", "both"],
        default="both",
        help="Input: Get the puzzle input; Instructions: Get the puzzle instructions; Both: Get both.",
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

            setup_py_template(int(year), int(day), opts.options)

        else:
            logging.error("Invalid date entered.")


if __name__ == "__main__":
    interactive()
