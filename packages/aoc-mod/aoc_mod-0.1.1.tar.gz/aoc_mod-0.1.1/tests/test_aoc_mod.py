import subprocess


def run_command(command):
    """Run a command in the shell and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result


def test_aoc_mod_help():
    """Test the aoc-mod command with the --help option."""
    result = run_command("aoc-mod --help")
    assert result.returncode == 0
    assert "usage: aoc-mod" in result.stdout


def test_aoc_mod_version():
    """Test the aoc-mod command with the --version option."""
    result = run_command("aoc-mod --version")
    assert result.returncode == 0
    assert "aoc-mod version" in result.stdout
