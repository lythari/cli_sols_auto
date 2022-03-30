import datetime
import re
from pathlib import Path
from typing import List

import click
from click.exceptions import BadParameter, NoSuchOption

from parser_sols_auto import new_parser
import tools

PARSE_TYPE = ['VEN', 'TRF', 'TRS', 'VAL']


@click.command()
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
    new2old.py --output_dir=/srv/out/ --parse_type=VEN /srv/in/20220301064444_FASHION_GROUP_MK_OKA_Sales_20220301.csv
    new2old.py --output_dir=/srv/out/ --parse_type=TRF /srv/in/
    new2old.py --output_dir=/../304/ --parse_type=VEN /srv/in/*_Sales_*.csv

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
    if parse_type not in PARSE_TYPE:
        print(f"{parse_type} does not exists")
        raise NoSuchOption(f"{parse_type} does not exists")

    for file in file_list:
        handle(output_directory, file, parse_type)


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


def output_file_name(file: Path, parse_type: str) -> str:
    names = {'VEN': 'Sales', 'TRS': 'Transfers', 'TRF': 'Traffic', 'VAL': 'Validation'}
    pattern = f".*{names.get(parse_type, '')}_(.*).csv"
    suffix = re.match(pattern, file.name).groups()[0]
    now = datetime.datetime.now()
    return f"{parse_type.title()}_{suffix}_{now.strftime('%Y%m%d%H%M%S%f')}.dat"


def handle(outdir: Path, file: Path, parse_type: str):
    tools.logger.info(f"handling file {file}")
    tools.logger.info("Running file conversion ...")
    new_content = new_parser(file, parse_type)

    new_name = output_file_name(file, parse_type)
    tools.logger.debug(f"Generation new file : {new_name}")

    new_file = outdir / new_name
    new_file.touch(exist_ok=True)
    new_file.write_text(new_content)
    tools.logger.info(f"File outputs : {new_file}")


if __name__ == '__main__':
    new2old()
