SINGLE_DAY_PYTHON_SCRIPT = '''"""Advent of Code {YEAR}, Day: {DAY}
Link: https://adventofcode.com/{YEAR}/day/{DAY}"""

import os
from aoc_mod.utilities import AOCMod

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def get_instructions(aoc_mod):
    instructions = aoc_mod.get_puzzle_instructions({YEAR}, {DAY})
    with open(CURRENT_PATH + "/instructions_{YEAR}_{DAY}.md", "w", encoding="utf-8") as f:
        f.write(instructions)

def parse_input():
    # read in input data from file
    with open(CURRENT_PATH + "/input_{DAY}.txt", "r", encoding="utf-8") as f:
        raw_input = f.read()

    # parse the input data
    input_data = raw_input.splitlines()
    return input_data


def part_one(parsed_input):
    print("Part One")
    output = dict(result=0, submit=False)

    return output


def part_two(parsed_input):
    print("Part Two")
    output = dict(result=0, submit=False)

    return output


def main():

    # set up aoc_mod
    aoc_mod = AOCMod()

    print("{YEAR}:Day{DAY}")

    # get the answer for part one
    answer_one = part_one(parse_input())

    # submit part one, if ready
    if answer_one["submit"]:
        result = aoc_mod.submit_answer({YEAR}, {DAY}, 1, answer_one["result"])

        # if we get the correct answer for part one, we'll retrieve the instructions for part two
        if "That's the right answer" in result:
            get_instructions(aoc_mod)

    # get the answer for part two
    answer_two = part_two(parse_input())

    # submit part two, if ready
    if answer_two["submit"]:
        result = aoc_mod.submit_answer({YEAR}, {DAY}, 2, answer_two["result"])
        
        # if we get the correct answer for part two, we'll retrieve the rest of the instructions
        if "That's the right answer" in result:
            get_instructions(aoc_mod)


if __name__ == "__main__":
    main()'''
