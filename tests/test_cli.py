from cli_sols_auto.app import cli


def test_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: cli [OPTIONS] COMMAND [ARGS]")


def test_new2old_help(cli_runner):
    result = cli_runner.invoke(cli, ["new2old", "--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: cli new2old [OPTIONS] INPUT_FILES")


def test_old2new_help(cli_runner):
    result = cli_runner.invoke(cli, ["old2new", "--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: cli old2new [OPTIONS] INPUT_FILES BRAND_CODE")


