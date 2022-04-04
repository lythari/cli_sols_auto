import pytest
from click import BadParameter, ClickException

from cli_sols_auto.app import cli


def test_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: cli [OPTIONS] COMMAND [ARGS]")


def test_wrong_call(cli_runner):
    result = cli_runner.invoke(cli, ["--test"])
    assert result.exit_code != 0
    assert result.output.startswith("Usage: cli [OPTIONS] COMMAND [ARGS]")
    assert "Error: No such option" in result.output


def test_new2old_help(cli_runner):
    result = cli_runner.invoke(cli, ["new2old", "--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: cli new2old [OPTIONS] INPUT_FILES")


def test_old2new_help(cli_runner):
    result = cli_runner.invoke(cli, ["old2new", "--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: cli old2new [OPTIONS] INPUT_FILES BRAND_CODE")


def test_new2old_outdir_verbose(cli_runner, new_ven_file, tmpdir_factory):
    outdir = tmpdir_factory.mktemp('out')
    result = cli_runner.invoke(
        cli,
        [
            "new2old",
            f'--output_dir={outdir}',
            "--parse_type=VEN",
            str(new_ven_file),
            '-v'
        ],
    )

    assert result.exit_code == 0


def test_old2new_outdir(cli_runner, old_ven_file, tmpdir_factory):
    outdir = tmpdir_factory.mktemp('out')
    result = cli_runner.invoke(
        cli,
        [
            "old2new",
            f'--output_dir={outdir}',
            "--parse_type=VEN",
            str(old_ven_file),
            'OKA'
        ],
    )

    assert result.exit_code == 0


def test_new2old(cli_runner, new_ven_file):
    result = cli_runner.invoke(
        cli,
        [
            "new2old",
            "--parse_type=VEN",
            str(new_ven_file),
        ],
    )

    assert result.exit_code == 0


def test_old2new_verbose(cli_runner, old_trs_file):
    result = cli_runner.invoke(
        cli,
        [
            "old2new",
            "--parse_type=TRS",
            str(old_trs_file),
            'OKA',
            '-v'
        ],
    )

    assert result.exit_code == 0


def test_new2old_file_not_found(cli_runner, tmp_new_dir):
    result = cli_runner.invoke(
        cli,
        [
            "new2old",
            "--parse_type=TRS",
            f'{tmp_new_dir}/test',
            '-v'
        ],
    )

    assert result.exit_code == 1
    assert isinstance(result.exception, RuntimeError)


def test_new2old_dir_empty(cli_runner, tmpdir_factory):
    empty_dir = tmpdir_factory.mktemp('empty')
    with pytest.raises(BadParameter):
        result = cli_runner.invoke(
            cli,
            [
                "new2old",
                "--parse_type=TRS",
                str(empty_dir),
                '-v'
            ], catch_exceptions=False
        )
        assert result.exit_code == 2
