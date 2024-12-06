SINGLE_DAY_PYTHON_SCRIPT = '''"""Advent of Code {YEAR}, Day: {DAY}
Link: https://adventofcode.com/{YEAR}/day/{DAY}"""

from aoc_mod.utilities import AOCMod

def parse_input(raw_input):
    # parse the input data
    input_data = raw_input.decode("utf-8").splitlines()
    return input_data


def part_a(parsed_input):
    print("Part A")
    return 0


def part_b(parsed_input):
    print("Part B")
    return 0
    

def main():

    # set up aoc_mod
    aoc_mod = AOCMod()

    print("{YEAR}:Day{DAY}")
    parsed_input = parse_input(aoc_mod.get_puzzle_input({YEAR}, {DAY}))
    instructions = aoc_mod.get_puzzle_instructions({YEAR}, {DAY})
    
    with open("instructions_{YEAR}_{DAY}.md", "w", encoding="utf-8") as f:
        f.write(instructions)

    # uncomment below to submit part A
    # aoc_mod.submit_answer({YEAR}, {DAY}, 1, part_a(parsed_input))

    # uncomment below to submit part B
    # aoc_mod.submit_answer({YEAR}, {DAY}, 2, part_b(parsed_input))


if __name__ == "__main__":
    main()'''
