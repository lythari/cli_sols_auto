from pathlib import Path
from .tools import dummyparser


def parse_sales(line: str) -> str:
    data = line.split(";")
    data = data + ['0'] if len(data) == 8 else data
    store_code, sales_date, _, receipt_number, barcode, quantity, price, pos_id, _ = data
    new_quantity = f'{quantity:0>5}' if int(quantity) > 0 else f'-{abs(int(quantity)):0>4}'
    return f"{store_code[4:]:0>6}{sales_date.replace('-', '')}{barcode:0>13}{receipt_number:0>10}{new_quantity}" \
           f"{int(float(price.replace(',','.'))*100):0>9}{pos_id[0]}"


def parse_traffic(line: str) -> str:
    data = line.split(";")
    store_code, traffic_date, traffic_number = data[:3]

    return f"{store_code[4:]:0>6}{traffic_date.replace('-', '')}{traffic_number:0>4}"


def parse_interstore_transfer(line: str) -> str:
    data = line.split(";")
    transfer_date, _, sender_code, receiver_code, barcode, quantity = data

    return f"{transfer_date.replace('-', '')}{sender_code[4:]:0>6}{receiver_code[4:]:0>6}{barcode:0>13}{quantity:0>4}"


def parse_delivery_validation(line: str) -> str:
    data = line.split(";")
    store_code, parcel_number, barcode, quantity, reception_date = data[:5]

    return f"{store_code[4:]:0>6}{parcel_number:0>20}{barcode:0>13}{quantity:0>5}{reception_date.replace('-', '')}"


PARSERS = {
    'VEN': parse_sales,
    'TRF': parse_traffic,
    'TRS': parse_interstore_transfer,
    'VAL': parse_delivery_validation,
}


def parse(file: Path, file_type: str) -> str:
    if not file.exists():
        raise RuntimeError("File does not exists.")
    data = file.read_text(encoding="utf-8")
    type_parser = PARSERS.get(file_type, dummyparser)

    return "\n".join(type_parser(line) for line in data.splitlines(False))


if __name__ == '__main__':
    new_line = Path(__file__).parent / 'osef_Sales_osef.csv'
    print(parse(new_line, 'VEN'))
