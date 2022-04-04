from pathlib import Path
from cli_sols_auto.parser_sols_auto.tools import dummyparser, FileType


def parse_sales(line: str) -> str:
    """
    Transform provided string from new CSV format to old .dat format:
    >>> parse_sales("JAC-778;2022-03-23;;4132369;3603652236628;1;395.00;1")
    '0007782022032336036522366280004132369000010000395001'

    Parsing is not affected by new optional fields time and ShipFromStore store:
    >>> parse_sales("JAC-778;2022-03-23;15-10-05;4132369;3603652236628;1;395.00;1;JAC-123")
    '0007782022032336036522366280004132369000010000395001'

    Handle float price as well as negative quantity:
    >>> parse_sales("JAC-778;2022-03-23;;4132369;3603652236628;-1;395.99;1")
    '0007782022032336036522366280004132369-00010000395991'

    Can also handle price as integer:
    >>> parse_sales("JAC-778;2022-03-23;;4132369;3603652236628;1;395;1")
    '0007782022032336036522366280004132369000010000395001'
    """
    data = line.split(";")
    if len(data) < 8 or len(data) > 9:
        raise ValueError(f"Incorrect input data {line}")
    store_code, sales_date, _, receipt_number, barcode, quantity, price, pos_id = data[:8]
    quantity = f'{quantity:0>5}' if int(quantity) > 0 else f'-{abs(int(quantity)):0>4}'
    sales_date = sales_date.replace('-', '')
    price = int(float(price.replace(',', '.')) * 100)
    return f"{store_code[4:]:0>6}{sales_date}{barcode:0>13}{receipt_number:0>10}{quantity}{price:0>9}{pos_id[0]}"


def parse_traffic(line: str) -> str:
    """
        Transform provided string from new CSV format to old .dat format:
        >>> parse_traffic("JAC-778;2022-03-29;8")
        '000778202203290008'

        Parsing is not affected by new optional field number of receipts:
        >>> parse_traffic("JAC-778;2022-03-29;8;5")
        '000778202203290008'

        Parsing is not affected by new optional fields min and max receipt numbers:
        >>> parse_traffic("JAC-778;2022-03-29;8;5;44;48")
        '000778202203290008'
    """
    data = line.split(";")
    if len(data) < 3 or len(data)>6:
        raise ValueError(f"Incorrect input data {line}")
    store_code, traffic_date, traffic_number = data[:3]
    traffic_date = traffic_date.replace('-', '')
    return f"{store_code[4:]:0>6}{traffic_date}{traffic_number:0>4}"


def parse_interstore_transfer(line: str) -> str:
    """
        Transform provided string from new CSV format to old .dat format:
        >>> parse_interstore_transfer("2021-11-01;;OKA-1210;OKA-1889;3604277211410;5")
        '2021110100121000188936042772114100005'

        Parsing is not affected by new optional field time of transfer:
        >>> parse_interstore_transfer("2021-11-01;11-04-12;OKA-1210;OKA-1889;3604277211410;5")
        '2021110100121000188936042772114100005'
    """
    data = line.split(";")
    if len(data) != 6:
        raise ValueError(f"Incorrect input data {line}")
    transfer_date, _, sender_code, receiver_code, barcode, quantity = data
    transfer_date = transfer_date.replace('-', '')
    if not quantity.isdigit() or int(quantity) < 0:
        raise ValueError("Incorrect input data {line}")
    return f"{transfer_date}{sender_code[4:]:0>6}{receiver_code[4:]:0>6}{barcode:0>13}{quantity:0>4}"


def parse_delivery_validation(line: str) -> str:
    """
        Transform provided string from new CSV format to old .dat format:
        >>> parse_delivery_validation("JAC-778;00000999993057074313;3603652347409;1;2021-04-19")
        '0007780000099999305707431336036523474090000120210419'

        Parsing is not affected by new optional field time of validation:
        >>> parse_delivery_validation("JAC-778;00000999993057074313;3603652347409;1;2021-04-19;16-35-57")
        '0007780000099999305707431336036523474090000120210419'

        Parsing is not affected by empty time field:
        >>> parse_delivery_validation("JAC-778;00000999993057074313;3603652347409;1;2021-04-19;;")
        '0007780000099999305707431336036523474090000120210419'
    """
    data = line.split(";")
    if len(data) < 5 or len(data) > 7:
        raise ValueError(f"Incorrect input data {line}")
    store_code, parcel_number, barcode, quantity, reception_date = data[:5]

    return f"{store_code[4:]:0>6}{parcel_number:0>20}{barcode:0>13}{quantity:0>5}{reception_date.replace('-', '')}"


line_parsers = [parse_traffic, parse_interstore_transfer, parse_delivery_validation, parse_sales]

PARSERS = dict(zip([t for t in FileType], line_parsers))


def parse(file: Path, file_type: FileType) -> str:
    if not file.exists():
        raise RuntimeError("File does not exists.")
    data = file.read_text(encoding="utf-8")
    type_parser = PARSERS.get(file_type, dummyparser)
    print(PARSERS)
    return "\n".join(type_parser(line) for line in data.splitlines(False))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
