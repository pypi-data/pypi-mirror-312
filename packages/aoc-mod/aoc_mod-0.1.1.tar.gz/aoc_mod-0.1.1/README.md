# Advent of Code Module

A library for Advent of Code containing utilities to use while solving problems! If any issues or bugs are discovered, please submit an issue and I'll fix it!

## Installation and basic use

To install, simply run the following command.

```sh
pip install aoc-mod
```

AOC Mod can be used interactively from the command line or as a library to import into your Advent of Code challenge solutions with Python.

You may follow the sections below to either utilize the command-line utility or see this example for using the library programmatically.

```py
from aoc_mod.utilites import AOCMod

aoc_mod = AOCMod()

puzz_input = aoc_mod.get_puzzle_input({YEAR}, {DAY})
instructions = aoc_mod.get_puzzle_instructions({YEAR}, {DAY})

sol = do_the_solution_p1()

aoc_mod.submit_answer({YEAR}, {DAY}, 1, sol)
```


## How to set the session ID environment variable

To grab puzzle instructions and input or submit an answer, you'll need the to store session ID from your login to Advent of Code as an environment variable.

```sh
export SESSION_ID=cbef2304aaa12390fbc7absc3892 
```

## Usage `aoc-mod`

```sh
usage: aoc-mod [-h] [--debug] {setup,submit} ...

positional arguments:
  {setup,submit}
    setup         Initiate the setup of the files for AoC.
    submit        Initiate a submission of the answer for an AoC problem.

options:
  -h, --help      show this help message and exit
  --debug         Enable debug print statements.
```

### Usage `aoc-mod setup`

```sh
usage: aoc-mod setup [-h] [-d YEAR:DAY]

options:
  -h, --help            show this help message and exit
  -d YEAR:DAY, --date YEAR:DAY
                        Enter the year and day of the Advent of Code challenge you would like.
```

### Usage `aoc-mod submit`

```sh
usage: aoc-mod submit [-h] -a ANSWER -l {1,2} -d YEAR:DAY

options:
  -h, --help            show this help message and exit
  -a ANSWER, --answer ANSWER
                        Answer to submit.
  -l {1,2}, --level {1,2}
                        Part A = 1; Part B = 2
  -d YEAR:DAY, --date YEAR:DAY
                        Enter the year and day of the Advent of Code challenge you would like.
```

## Class: AOCMod

#### __init__(self)

Initialize the AOCMod class and set up the current time and authentication variables.

#### set_auth_variables(self)

Set the authentication variables from environment variables.

#### get_current_date(self)

Get the current local time.

**Returns:**
- time.struct_time: The current local time.

#### verify_correct_date(self, year: int, month: int, day: int)

Verify if the provided date is valid for Advent of Code.

**Args:**
- year (int): The year to verify.
- month (int): The month to verify.
- day (int): The day to verify.

**Returns:**
- `bool`: True if the date is valid, False otherwise.

### Constants

#### URL_PUZZLE_MAIN

The main URL template for Advent of Code puzzles.

#### URL_PUZZLE_INPUT

The URL template for Advent of Code puzzle input.

#### URL_PUZZLE_ANSWER

The URL template for Advent of Code puzzle answer submission.

### Logging

#### LOGGER

A logger instance for the module.

### Dependencies

- os
- logging
- time
- requests
- markdownify
- bs4.BeautifulSoup

## Contributing

If you feel that you have new features to contribute, don't hesitate to submit a pull request!

### How to build `aoc-mod`

```sh
$(realpath `which python3`) -m venv .venv
source .venv/bin/activate

pip install -e .[build,test]

python -m build
```

### How to test `aoc-mod`

After following the build steps, run `pytest`.

```sh
pytest -vv
```