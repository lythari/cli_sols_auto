from datetime import datetime
from pathlib import Path

import cli_sols_auto.tools as tools
from .tools import dummyparser, FileType


def parse_sales(line: str, brand: str) -> str:
    sales_date = datetime.strptime(line[6:14], '%Y%m%d').strftime('%Y-%m-%d')
    quantity = int(line[38:42])*-1 if line[37] == '-' else int(line[37:42])

    return f"{brand}-{int(line[:6])};{sales_date};;{int(line[27:37])};{line[14:27]};{quantity};" \
           f"{float(int(line[42:51])/100):.2f};{line[-1]}"


def parse_traffic(line: str, brand: str) -> str:
    traffic_date = datetime.strptime(line[6:14], '%Y%m%d').strftime('%Y-%m-%d')

    return f"{brand}-{int(line[:6])};{traffic_date};{int(line[14:18])}"


def parse_interstore_transfer(line: str, brand: str) -> str:
    transfer_date = datetime.strptime(line[:8], '%Y%m%d').strftime('%Y-%m-%d')

    return f"{transfer_date};;{brand}-{int(line[8:14])};{brand}-{int(line[14:20])};{line[20:33]};{int(line[-4:])}"


def parse_delivery_validation(line: str, brand: str) -> str:
    reception_date = datetime.strptime(line[-8:], '%Y%m%d').strftime('%Y-%m-%d')

    return f"{brand}-{int(line[:6])};{line[6:26]};{line[26:39]};{int(line[39:44])};{reception_date}"


line_parsers = [parse_traffic, parse_interstore_transfer, parse_delivery_validation, parse_sales]

PARSERS = dict(zip([t for t in FileType], line_parsers))


def parse(file: Path, file_type: FileType, brand_code: str) -> str:
    if not file.exists():
        raise RuntimeError("File does not exists.")
    data = file.read_text(encoding='utf-8')
    type_parser = PARSERS.get(file_type, dummyparser)

    return "\n".join(type_parser(line, brand_code) for line in data.splitlines(False))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
