import datetime
import re
from pathlib import Path
from typing import List

import click
from click.exceptions import BadParameter, NoSuchOption

from cli_sols_auto.parser_sols_auto import new_parser, old_parser
import cli_sols_auto.tools as tools
from cli_sols_auto.parser_sols_auto.tools import FileType


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option('--output_dir', help='Directory where to output converted files. If ommited outputs in the original '
                                   'directory')
@click.option('--parse_type', required=True, help='The type of file and parser to use (VEN, TRF, TRA, VAL)')
@click.option('-v', '--verbose', count=True, help='Enable DEBUG logging verbosity')
@click.argument('input_files')
def new2old(output_dir, parse_type, verbose, input_files):
    """
    Convert file from new to old version

    INPUT_FILES : File(s) to convert. This could consist in a file path, a directory path or a pattern
                 (see examples provided).

    EXAMPLE OF USAGE :
    app.py new2old --output_dir=/srv/out/ --parse_type=VEN /srv/in/Sales_20220301.csv
    app.py new2old --output_dir=/srv/out/ --parse_type=TRF /srv/in/
    app.py new2old --output_dir=/../304/ --parse_type=VEN /srv/in/Sales_*.csv

    """

    if verbose:
        tools.logger.setLevel("DEBUG")
        tools.logger.debug("DEBUG MODE [ON] don't forget to turn it off in production environment")
    else:
        tools.logger.setLevel("INFO")

    if input_files.startswith("'"):
        input_files = input_files[1:-1]
    tools.logger.debug(f"input_files = {input_files}")
    file_list = get_file_list(input_files)

    if not len(file_list):
        raise BadParameter(f"No file found in input {input_files}")

    if output_dir:
        tools.logger.debug(f"Output directory = {output_dir}")
        output_directory = Path(output_dir)
        if not output_directory.exists():
            tools.logger.fatal(f"{output_dir} does not exists")
            raise RuntimeError(f"{output_dir} does not exists")
        if output_directory.is_file():
            output_directory = output_directory.parent
            tools.logger.warning(f"{output_dir} is a file using {output_directory} instead")
    else:
        output_directory = file_list[0].parent
        tools.logger.info(f"output directory is None using {output_directory} instead")

    tools.logger.debug(f"Parse_type = {parse_type}")
    try:
        parse_type = FileType(parse_type)
    except ValueError:
        tools.logger.fatal(f"{parse_type} does not exists")
        raise NoSuchOption(f"{parse_type} does not exists")

    for file in file_list:
        handle(output_directory, file, parse_type)


@cli.command()
@click.option('--output_dir', help='Directory where to output converted files. If ommited outputs in the original '
                                   'directory')
@click.option('--parse_type', required=True, help='The type of file and parser to use (VEN, TRF, TRA, VAL)')
@click.option('-v', '--verbose', count=True, help='Enable DEBUG logging verbosity')
@click.argument('input_files')
@click.argument('brand_code')
def old2new(output_dir, parse_type, verbose, input_files, brand_code):
    """
    Convert file from old to new version

    INPUT_FILES : File(s) to convert. This could consist in a file path, a directory path or a pattern
                 (see examples provided).
    BRAND_CODE : Brand code that will be use to prefix store codes

    EXAMPLE OF USAGE :
    app.py old2new --output_dir=/app/out/ --parse_type=VEN /app/in/Ven_20220301.dat OKA
    app.py old2new --output_dir=/app/out/ --parse_type=TRF /app/in/ JAC
    app.py old2new --output_dir=/../304/ --parse_type=VEN /srv/in/Ven*.dat JAC

    """

    if verbose:
        tools.logger.setLevel("DEBUG")
        tools.logger.debug("DEBUG MODE [ON] don't forget to turn it off in production environment")
    else:
        tools.logger.setLevel("INFO")

    if input_files.startswith("'"):
        input_files = input_files[1:-1]
    tools.logger.debug(f"input_files = {input_files}")
    file_list = get_file_list(input_files)

    if not len(file_list):
        tools.logger.fatal(f"No file found in input {input_files}")
        raise BadParameter(f"No file found in input {input_files}")

    if output_dir:
        tools.logger.debug(f"Output directory = {output_dir}")
        output_directory = Path(output_dir)
        if not output_directory.exists():
            tools.logger.fatal(f"{output_dir} does not exists")
            raise RuntimeError(f"{output_dir} does not exists")
        if output_directory.is_file():
            output_directory = output_directory.parent
            tools.logger.warning(f"{output_dir} is a file using {output_directory} instead")
    else:
        output_directory = file_list[0].parent
        tools.logger.info(f"output directory is None using {output_directory} instead")

    tools.logger.debug(f"Parse_type = {parse_type}")
    tools.logger.debug(f"Brand_code = {brand_code}")
    try:
        parse_type = FileType(parse_type)
    except ValueError:
        tools.logger.fatal(f"{parse_type} does not exists")
        raise NoSuchOption(f"{parse_type} does not exists")

    for file in file_list:
        handle(output_directory, file, parse_type, brand_code)


def get_file_list(input_dir: str) -> List[Path]:
    """
    Get files as a list of Path from the CLI argument provided

    :param input_dir: provided input string, can be a file, a path or a pattern
    :return: a list of pathlib's Path like object
    """
    if '*' in input_dir:
        *paths_to_dir, pattern = input_dir.split('/')
        path_to_dir: Path = Path('/').joinpath(*paths_to_dir)
        tools.logger.debug(f"input_files is a pattern : {pattern} in {path_to_dir}")
        files: List[Path] = [file for file in path_to_dir.glob(pattern) if file.is_file()]
    else:
        input_path: Path = Path(input_dir)
        if not input_path.exists():
            tools.logger.fatal(f"{input_path} does not exists")
            raise RuntimeError(f"{input_path} does not exists")

        if input_path.is_file():
            files: List[Path] = [input_path]
        else:
            tools.logger.debug(f"input_files is a directory : {input_path}")
            files: List[Path] = [file for file in input_path.iterdir() if file.is_file()]

    return files


def output_file_name_old(file_name: str, parse_type: FileType) -> str:
    """
        Transform new file name to old style name

        :param file_name: Name of the new file
        :param parse_type: Type of the file (see enum cli_sols_auto.parse_sols_auto.tools.FileType)
        :return: old style name

        Exemples :
        Recognize Sales_*.csv to Ven_*.dat :
        >>> output_file_name_old("20220101120245_Sales_20012022_1234.csv", FileType("VEN"))
        'Ven_20012022_1234_....dat'

        Recognize Trf, Trs and Val as well :
        >>> output_file_name_old("20220101120245_Traffic_20012022_1234.csv", FileType("TRF"))
        'Trf_20012022_1234_....dat'
        >>> output_file_name_old("20220101120245_Transfers_20012022_1234.csv", FileType("TRS"))
        'Trs_20012022_1234_....dat'
        >>> output_file_name_old("20220101120245_Validation_20012022_1234.csv", FileType("VAL"))
        'Val_20012022_1234_....dat'

        Is not bothered by prefix value or the size of suffix :
        >>> output_file_name_old("Traffic_20012022_1234.csv", FileType("TRF"))
        'Trf_20012022_1234_....dat'

        """
    names = dict(zip([t for t in FileType], ('Traffic', 'Transfers', 'Validation', 'Sales')))

    pattern = f".*{names.get(parse_type, '')}_(.*).csv"
    suffix = re.match(pattern, file_name).groups()[0]
    now = datetime.datetime.now()
    return f"{parse_type.title()}_{suffix}_{now.strftime('%Y%m%d%H%M%S%f')}.dat"


def output_file_name_new(file_name: str, parse_type: FileType) -> str:
    """
    Transform old file name to new style name

    :param file_name: Name of the old file
    :param parse_type: Type of the file (see enum cli_sols_auto.parse_sols_auto.tools.FileType)
    :return: New name

    Exemples :
    Recognize Ven_*.dat to Sales_*.csv :
    >>> output_file_name_new("20220101120245_Ven_20012022_1234.dat", FileType("VEN"))
    'Sales_20012022_1234_....csv'

    Recognize Trf, Trs and Val as well :
    >>> output_file_name_new("20220101120245_Trf_20012022_1234.dat", FileType("TRF"))
    'Traffic_20012022_1234_....csv'
    >>> output_file_name_new("20220101120245_Trs_20012022_1234.dat", FileType("TRS"))
    'Transfers_20012022_1234_....csv'
    >>> output_file_name_new("20220101120245_Val_20012022_1234.dat", FileType("VAL"))
    'Validation_20012022_1234_....csv'

    Is not bothered by prefix value or the size of suffix :
    >>> output_file_name_new("Trf_20012022_1234.dat", FileType("TRF"))
    'Traffic_20012022_1234_....csv'
    >>> output_file_name_new("Trf_20012022.dat", FileType("TRF"))
    'Traffic_20012022_....csv'
    >>> output_file_name_new("Trf_20012022_1234_test_1234_init_MCO.dat", FileType("TRF"))
    'Traffic_20012022_1234_test_1234_init_MCO_....csv'

    """

    names = dict(zip([t for t in FileType], ('Traffic', 'Transfers', 'Validation', 'Sales')))

    pattern = f".*{parse_type.title()}_(.*).dat"
    suffix = re.match(pattern, file_name).groups()[0]

    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return f"{names.get(parse_type, '').title()}_{suffix}_{now}.csv"


def handle(outdir: Path, file: Path, parse_type: FileType, brand_code: str = None):
    tools.logger.info(f"handling file {file}")
    tools.logger.info("Running file conversion ...")

    new_content = old_parser(file, parse_type, brand_code) if brand_code else new_parser(file, parse_type)
    tools.logger.debug(f"Content generated : {len(new_content)} bytes")

    new_name = output_file_name_new(file.name, parse_type) if brand_code else output_file_name_old(file.name, parse_type)
    tools.logger.debug(f"Generation new file : {new_name}")

    new_file = outdir / new_name
    new_file.touch(exist_ok=True)
    new_file.write_text(new_content)
    tools.logger.info(f"File outputs : {new_file}")


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
