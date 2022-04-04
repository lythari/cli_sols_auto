from cli_sols_auto.parser_sols_auto.new import (
    parse,
    parse_sales,
    parse_interstore_transfer,
    parse_traffic,
    parse_delivery_validation
)


# Test parsing a line
from cli_sols_auto.parser_sols_auto.tools import FileType


def test_line_new2old_ven():
    new = "JAC-778;2022-03-23;13-15-22;4132369;3603652236628;1;395.00;1"
    expect = "0007782022032336036522366280004132369000010000395001"
    assert parse_sales(new) == expect


def test_line_new2old_trs():
    new = "2021-11-01;11-04-12;OKA-1210;OKA-1889;3604277211410;5"
    expect = "2021110100121000188936042772114100005"
    assert parse_interstore_transfer(new) == expect


def test_line_new2old_trf():
    new = "JAC-778;2022-03-29;8;2"
    expect = "000778202203290008"
    assert parse_traffic(new) == expect


def test_line_new2old_val():
    new = "JAC-778;00000999993057074313;3603652347409;1;2021-04-19;16-35-57"
    expect = "0007780000099999305707431336036523474090000120210419"
    assert parse_delivery_validation(new) == expect


# Test parsing a file
def test_new2old_ven(new_ven_file, old_ven_file):
    expect = old_ven_file.read_text(encoding="utf-8")
    assert parse(new_ven_file, FileType('VEN')) == expect


def test_new2old_val(new_val_file, old_val_file):
    expect = old_val_file.read_text(encoding="utf-8")
    assert parse(new_val_file, FileType('VAL')) == expect


def test_new2old_trf(new_trf_file, old_trf_file):
    expect = old_trf_file.read_text(encoding="utf-8")
    assert parse(new_trf_file, FileType('TRF')) == expect


def test_new2old_trs(new_trs_file, old_trs_file):
    expect = old_trs_file.read_text(encoding="utf-8")
    assert parse(new_trs_file, FileType('TRS')) == expect
